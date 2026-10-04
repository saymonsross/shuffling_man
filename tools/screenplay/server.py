"""Режим сценариста: локальный сервер. Запуск: python tools/screenplay/server.py

Правит .rpy построчно: каждая операция приходит с ожидаемым текстом строки и
отклоняется (409), если файл успел измениться, например в VS Code.
"""

import argparse
import codecs
import json
import os
import re
import sys
import threading
import webbrowser
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import unquote, urlparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import story_parser as sp  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(HERE, "static")
GAME_DIR = os.path.normpath(os.path.join(HERE, "..", "..", "game"))

LOCK = threading.Lock()
UNDO = []
UNDO_LIMIT = 200


class OpError(Exception):
    def __init__(self, status, message):
        super().__init__(message)
        self.status = status
        self.message = message


# ---------------------------------------------------------------- файл с сохранением BOM и концов строк

class SourceFile:
    def __init__(self, rel):
        self.rel = rel
        self.path = safe_game_path(rel, (".rpy",))
        with open(self.path, "rb") as f:
            self.original = f.read()
        self.bom = self.original.startswith(codecs.BOM_UTF8)
        self.parts = sp.split_keepends(self.original.decode("utf-8-sig"))

    def _check_no(self, no):
        if not 1 <= no <= len(self.parts):
            raise OpError(HTTPStatus.CONFLICT, "Строка %d вне файла %s" % (no, self.rel))

    def line(self, no):
        self._check_no(no)
        return self.parts[no - 1].rstrip("\r\n")

    def ending(self, no):
        part = self.parts[no - 1]
        return part[len(part.rstrip("\r\n")):]

    def eol(self):
        for p in self.parts:
            e = p[len(p.rstrip("\r\n")):]
            if e:
                return e
        return "\n"

    def expect(self, no, raw):
        if self.line(no) != raw:
            raise OpError(HTTPStatus.CONFLICT,
                          "Строка %s:%d изменилась снаружи — обновляю." % (self.rel, no))

    def set_line(self, no, content):
        self._check_no(no)
        self.parts[no - 1] = content + self.ending(no)

    def insert_after(self, no, content):
        self._check_no(no)
        if not self.ending(no):
            self.parts[no - 1] += self.eol()
            self.parts.insert(no, content)
        else:
            self.parts.insert(no, content + self.ending(no))

    def delete(self, no):
        self._check_no(no)
        if no == len(self.parts) and no > 1 and not self.ending(no):
            prev = self.parts[no - 2]
            self.parts[no - 2] = prev.rstrip("\r\n")
        del self.parts[no - 1]

    def data(self):
        text = "".join(self.parts)
        return (codecs.BOM_UTF8 if self.bom else b"") + text.encode("utf-8")


def safe_game_path(rel, exts):
    rel = rel.replace("\\", "/").lstrip("/")
    full = os.path.normpath(os.path.join(GAME_DIR, rel))
    if not full.startswith(GAME_DIR + os.sep) or not full.lower().endswith(exts):
        raise OpError(HTTPStatus.FORBIDDEN, "Путь вне game/: %s" % rel)
    if not os.path.isfile(full):
        raise OpError(HTTPStatus.NOT_FOUND, "Нет файла: %s" % rel)
    return full


def write_atomic(path, data):
    tmp = path + ".screenplay.tmp"
    with open(tmp, "wb") as f:
        f.write(data)
    os.replace(tmp, path)


def commit(files, label):
    """Пишет изменённые файлы одним шагом отмены."""
    entry = []
    for f in files:
        new = f.data()
        if new != f.original:
            entry.append((f.path, f.original, new))
    for path, _old, new in entry:
        write_atomic(path, new)
    if entry:
        UNDO.append({"label": label, "files": entry})
        del UNDO[:-UNDO_LIMIT]


# ---------------------------------------------------------------- операции

def split_indent(raw):
    t = raw.lstrip(" \t")
    return raw[:len(raw) - len(t)], t


def literal_span(raw, kind):
    indent, t = split_indent(raw)
    if kind == "title":
        lits = [x for x in sp.string_literals(t) if t[max(0, x[0] - 2):x[0]] == "_("]
        if not lits:
            raise OpError(HTTPStatus.CONFLICT, "В строке нет титра _(\"…\")")
        s, e, _v = lits[0]
        return len(indent) + s, len(indent) + e, None
    say = sp.parse_say(t)
    if not say:
        raise OpError(HTTPStatus.CONFLICT, "Строка не похожа на реплику")
    who, s, e, _v, _rest = say
    return len(indent) + s, len(indent) + e, who


def say_line(indent, who, text, tail=""):
    return indent + (who + " " if who else "") + sp.encode_string(text) + tail


def op_edit(req):
    f = SourceFile(req["file"])
    no = int(req["line"])
    f.expect(no, req["expect"])
    raw = f.line(no)
    kind = req.get("kind", "say")
    s, e, who = literal_span(raw, kind)
    new = raw[:s] + sp.encode_string(req["text"]) + raw[e:]
    if kind == "say" and "who" in req and (req["who"] or None) != who:
        indent, _t = split_indent(raw)
        new = say_line(indent, req["who"] or None, req["text"], raw[e:])
    f.set_line(no, new)
    commit([f], "правка строки")
    return {"focus": {"file": f.rel, "line": no}}


def block_end(f, no):
    """Последняя строка оператора no вместе с продолжениями скобок и дочерним блоком."""
    indent = len(split_indent(f.line(no))[0])
    last = no
    bal = sp.bracket_balance(f.line(no).strip())
    while bal > 0 and last < len(f.parts):
        last += 1
        bal += sp.bracket_balance(f.line(last).strip())
    if f.line(no).rstrip().endswith(":") or f.line(last).rstrip().endswith(":"):
        k = last + 1
        while k <= len(f.parts):
            t = f.line(k)
            if t.strip() and len(split_indent(t)[0]) <= indent:
                break
            if t.strip():
                last = k
            k += 1
    return last


def op_insert(req):
    f = SourceFile(req["file"])
    no = int(req["line"])
    f.expect(no, req["expect"])
    raw = f.line(no)
    indent, t = split_indent(raw)
    if req.get("into_block"):
        ## Первая реплика внутри пункта меню/условия: отступ первого ребёнка.
        child = None
        for k in range(no + 1, len(f.parts) + 1):
            c = f.line(k)
            if c.strip():
                ci = split_indent(c)[0]
                child = ci if len(ci) > len(indent) else None
                break
        at, new_indent = no, child or indent + "    "
    else:
        at, new_indent = block_end(f, no), indent
        ## Переход show/scene стоит отдельной строкой «with …» — реплика встаёт после него.
        k = at + 1
        while k <= len(f.parts):
            nxt = f.line(k)
            if nxt.strip():
                if split_indent(nxt)[0] == indent and nxt.strip().startswith("with "):
                    at = k
                else:
                    break
            k += 1
    f.insert_after(at, say_line(new_indent, req.get("who") or None, req.get("text", "")))
    commit([f], "новая строка")
    return {"focus": {"file": f.rel, "line": at + 1}}


def op_delete(req):
    f = SourceFile(req["file"])
    no = int(req["line"])
    f.expect(no, req["expect"])
    raw = f.line(no)
    if raw.rstrip().endswith(":") or not sp.parse_say(raw.strip()):
        raise OpError(HTTPStatus.CONFLICT, "Удалять можно только реплики")
    f.delete(no)
    commit([f], "удаление строки")
    return {"focus": {"file": f.rel, "line": max(1, no - 1)}}


def op_swap(req):
    f = SourceFile(req["file"])
    a, b = int(req["a"]), int(req["b"])
    f.expect(a, req["expect_a"])
    f.expect(b, req["expect_b"])
    ra, rb = f.line(a), f.line(b)
    for r in (ra, rb):
        if r.rstrip().endswith(":") or not sp.parse_say(r.strip()):
            raise OpError(HTTPStatus.CONFLICT, "Переставлять можно только реплики")
    ## Реплика уезжает на место соседки, но с собственным отступом соседкиной строки.
    ia, ib = split_indent(ra)[0], split_indent(rb)[0]
    f.set_line(a, ia + rb.lstrip(" \t"))
    f.set_line(b, ib + ra.lstrip(" \t"))
    commit([f], "перестановка строк")
    return {"focus": {"file": f.rel, "line": b}}


def plan_reorder(order):
    story = sp.build_story(GAME_DIR)
    scenes = story["scenes"]
    chain = story["chain"]
    if not order or len(set(order)) != len(order) or any(n not in scenes for n in order):
        raise OpError(HTTPStatus.BAD_REQUEST, "Порядок сцен некорректен")

    changes = []   # {file, line, old, new, mode: replace|insert, note}
    warnings = []

    def replace_exit(sc, new_stmt, note):
        ex = sc["exit"]
        raw = sp.read_lines(os.path.join(GAME_DIR, sc["file"]))[ex["line"] - 1]
        indent = split_indent(raw)[0]
        changes.append({"file": sc["file"], "line": ex["line"], "old": raw,
                        "new": indent + new_stmt, "mode": "replace", "note": note})

    for i, name in enumerate(order):
        sc = scenes[name]
        ex = sc["exit"]
        nxt = order[i + 1] if i + 1 < len(order) else None
        if nxt:
            if ex and ex["type"] == "jump" and ex["target"] == nxt:
                continue
            if ex:
                replace_exit(sc, "jump " + nxt, "%s → %s" % (sc["title"], scenes[nxt]["title"]))
            else:
                lines = sp.read_lines(os.path.join(GAME_DIR, sc["file"]))
                changes.append({"file": sc["file"], "line": sc["end_line"],
                                "old": lines[sc["end_line"] - 1], "new": "    jump " + nxt,
                                "mode": "insert",
                                "note": "%s → %s (переход дописан в конец)" % (sc["title"], scenes[nxt]["title"])})
                warnings.append("У «%s» не было перехода в конце — jump дописан после последней строки. "
                                "Проверь, что сцена не уходит раньше в главное меню." % sc["title"])
        elif ex and ex["type"] == "jump" and ex["target"] in scenes:
            replace_exit(sc, "return", "%s — теперь последняя (return)" % sc["title"])
            warnings.append("«%s» стала последней: её jump заменён на return — выход в главное меню."
                            % sc["title"])

    if chain and order[0] != chain[0] and story["start"]:
        st = story["start"]
        raw = sp.read_lines(os.path.join(GAME_DIR, st["file"]))[st["exit_line"] - 1]
        changes.append({"file": st["file"], "line": st["exit_line"], "old": raw,
                        "new": split_indent(raw)[0] + "jump " + order[0], "mode": "replace",
                        "note": "Начало игры → %s" % scenes[order[0]]["title"]})

    dropped = [n for n in chain if n not in order]
    for n in dropped:
        warnings.append("«%s» выпала из цепочки: в игре до неё больше не дойти." % scenes[n]["title"])
    return changes, warnings


def op_reorder(req):
    changes, warnings = plan_reorder(req["order"])
    if not req.get("apply"):
        return {"changes": changes, "warnings": warnings}
    files = {}
    for ch in changes:
        if ch["file"] not in files:
            files[ch["file"]] = SourceFile(ch["file"])
        files[ch["file"]].expect(ch["line"], ch["old"])
    ## Снизу вверх: вставка не сдвигает номера ещё не применённых правок.
    for ch in sorted(changes, key=lambda c: (c["file"], -c["line"])):
        f = files[ch["file"]]
        if ch["mode"] == "replace":
            f.set_line(ch["line"], ch["new"])
        else:
            f.insert_after(ch["line"], ch["new"])
    commit(list(files.values()), "порядок сцен")
    return {"changes": changes, "warnings": warnings}


def op_undo(_req):
    if not UNDO:
        raise OpError(HTTPStatus.CONFLICT, "Отменять нечего")
    entry = UNDO[-1]
    for path, _old, new in entry["files"]:
        with open(path, "rb") as f:
            if f.read() != new:
                UNDO.pop()
                raise OpError(HTTPStatus.CONFLICT,
                              "Файл %s правили снаружи — отмена «%s» невозможна."
                              % (os.path.relpath(path, GAME_DIR), entry["label"]))
    for path, old, _new in entry["files"]:
        write_atomic(path, old)
    UNDO.pop()
    return {"undone": entry["label"]}


OPS = {
    "edit": op_edit,
    "insert": op_insert,
    "delete": op_delete,
    "swap": op_swap,
    "reorder": op_reorder,
    "undo": op_undo,
}


def version_stamp():
    stamp = 0
    count = 0
    for _rel, full in sp.story_files(GAME_DIR):
        stamp = max(stamp, os.stat(full).st_mtime_ns)
        count += 1
    return "%d-%d" % (stamp, count)


# ---------------------------------------------------------------- HTTP

class Handler(SimpleHTTPRequestHandler):
    ## Реестр Windows бывает отдаёт .css/.js как text/plain — браузер тогда не применит стили.
    extensions_map = {
        "": "application/octet-stream",
        ".html": "text/html; charset=utf-8",
        ".css": "text/css; charset=utf-8",
        ".js": "text/javascript; charset=utf-8",
    }

    def __init__(self, *args, **kwargs):
        self.cache_header_sent = False
        super().__init__(*args, directory=STATIC_DIR, **kwargs)

    def end_headers(self):
        if not self.cache_header_sent:
            self.send_header("Cache-Control", "no-cache")
        super().end_headers()

    def log_message(self, fmt, *args):
        if not self.path.startswith(("/api/version", "/game/")):
            sys.stderr.write("%s\n" % (fmt % args))

    def send_json(self, obj, status=HTTPStatus.OK):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.cache_header_sent = True
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = urlparse(self.path).path
        try:
            if path == "/api/story":
                with LOCK:
                    story = sp.build_story(GAME_DIR)
                    story["version"] = version_stamp()
                    story["undo"] = [e["label"] for e in UNDO[-1:]]
                    story["game_dir"] = GAME_DIR.replace("\\", "/")
                return self.send_json(story)
            if path == "/api/version":
                return self.send_json({"version": version_stamp()})
            if path.startswith("/game/"):
                return self.send_game_file(unquote(path[len("/game/"):]))
        except OpError as e:
            return self.send_json({"error": e.message}, e.status)
        return super().do_GET()

    def send_game_file(self, rel):
        full = safe_game_path(rel, sp.IMAGE_EXTS)
        ctype = "image/png" if full.lower().endswith(".png") else \
            "image/webp" if full.lower().endswith(".webp") else "image/jpeg"
        with open(full, "rb") as f:
            data = f.read()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "max-age=30")
        self.cache_header_sent = True
        self.end_headers()
        self.wfile.write(data)

    def do_POST(self):
        m = re.match(r"^/api/(\w+)$", urlparse(self.path).path)
        if not m or m.group(1) not in OPS:
            return self.send_json({"error": "unknown op"}, HTTPStatus.NOT_FOUND)
        try:
            length = int(self.headers.get("Content-Length") or 0)
            req = json.loads(self.rfile.read(length).decode("utf-8") or "{}")
            with LOCK:
                res = OPS[m.group(1)](req)
                res["version"] = version_stamp()
                res["undo"] = [e["label"] for e in UNDO[-1:]]
            return self.send_json(res)
        except OpError as e:
            return self.send_json({"error": e.message}, e.status)
        except (KeyError, ValueError, TypeError) as e:
            return self.send_json({"error": "Некорректный запрос: %s" % e}, HTTPStatus.BAD_REQUEST)


class Server(ThreadingHTTPServer):
    ## На Windows SO_REUSEADDR даёт второму экземпляру молча занять тот же порт.
    allow_reuse_address = os.name != "nt"
    daemon_threads = True


def main():
    ap = argparse.ArgumentParser(description="Режим сценариста для Shuffling Man")
    ap.add_argument("--port", type=int, default=8765)
    ap.add_argument("--no-browser", action="store_true")
    args = ap.parse_args()

    server = None
    for port in range(args.port, args.port + 10):
        try:
            server = Server(("127.0.0.1", port), Handler)
            break
        except OSError:
            continue
    if server is None:
        sys.exit("Нет свободного порта в %d..%d" % (args.port, args.port + 9))

    url = "http://127.0.0.1:%d/" % server.server_address[1]
    print("Режим сценариста: %s  (Ctrl+C — выход)" % url)
    if not args.no_browser:
        threading.Timer(0.4, webbrowser.open, (url,)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
