"""Чтение сценария Ren'Py в модель для режима сценариста.

Модель строится заново на каждый запрос: файлы маленькие, а кэш расходился бы
с правками, сделанными параллельно в VS Code.
"""

import os
import re
import struct

IMAGE_EXTS = (".png", ".jpg", ".jpeg", ".webp")
SKIP_DIRS = {"tl", "dev", "libs", "cache", "saves", "gui", "audio", "fonts"}
STORY_DIR_RE = re.compile(r"^\d_[a-z0-9_]+$")

## Ключевые слова, после которых строка — не реплика, даже если дальше идёт строка в кавычках.
NOT_SPEAKERS = {
    "show", "scene", "hide", "play", "stop", "queue", "voice", "call", "jump", "pause",
    "with", "window", "image", "define", "default", "label", "if", "elif", "else", "while",
    "for", "return", "translate", "camera", "at", "style", "screen", "transform", "init",
    "python", "menu", "nvl", "old", "new", "pass", "on", "use",
}

## Блоки, чьи дети — сценарий; остальные блоки (ATL, python, screen) пропускаются целиком.
SCRIPT_BLOCK_RE = re.compile(r"^(if|elif|else|while|for|menu)\b")

FULL_FRAME_MIN = (1600, 900)


class Line:
    __slots__ = ("no", "raw", "text", "indent")

    def __init__(self, no, raw):
        self.no = no
        self.raw = raw
        self.text = raw.strip()
        self.indent = len(raw) - len(raw.lstrip(" \t"))


LINE_RE = re.compile(r"[^\r\n]*(?:\r\n|\n|\r)|[^\r\n]+$")


def split_keepends(text):
    """Строки с концами; в отличие от splitlines не режет по form feed и разделителям Unicode."""
    return LINE_RE.findall(text)


def read_lines(path):
    """Строки файла без концов строк (их сохраняет file_io при записи)."""
    with open(path, "rb") as f:
        data = f.read()
    text = data.decode("utf-8-sig")
    return [l.rstrip("\r\n") for l in split_keepends(text)]


# ---------------------------------------------------------------- строки-литералы

def scan_string(s, i):
    """s[i] — открывающая кавычка. Возвращает (конец_исключительно, значение) или None."""
    q = s[i]
    triple = s[i:i + 3] == q * 3
    j = i + (3 if triple else 1)
    out = []
    while j < len(s):
        c = s[j]
        if c == "\\" and j + 1 < len(s):
            n = s[j + 1]
            out.append("\n" if n == "n" else n)
            j += 2
            continue
        if triple and s[j:j + 3] == q * 3:
            return j + 3, "".join(out)
        if not triple and c == q:
            return j + 1, "".join(out)
        out.append(c)
        j += 1
    return None


def encode_string(value):
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n") + '"'


def string_literals(s):
    """Все однострочные литералы строки: [(начало, конец, значение)]."""
    res = []
    i = 0
    while i < len(s):
        c = s[i]
        if c == "#":
            break
        if c in "\"'":
            r = scan_string(s, i)
            if r is None:
                break
            res.append((i, r[0], r[1]))
            i = r[0]
            continue
        i += 1
    return res


def bracket_balance(s):
    depth = 0
    i = 0
    while i < len(s):
        c = s[i]
        if c == "#":
            break
        if c in "\"'":
            r = scan_string(s, i)
            if r is None:
                break
            i = r[0]
            continue
        if c in "([{":
            depth += 1
        elif c in ")]}":
            depth -= 1
        i += 1
    return depth


def parse_say(text):
    """Реплика/пункт меню: (who, start, end, value, rest) в координатах text или None."""
    m = re.match(r"(?:([A-Za-z_]\w*)\s+)?([\"'])", text)
    if not m:
        return None
    who = m.group(1)
    if who in NOT_SPEAKERS:
        return None
    start = m.start(2)
    r = scan_string(text, start)
    if r is None:
        return None
    end, value = r
    return who, start, end, value, text[end:].strip()


# ---------------------------------------------------------------- картинки

def image_size(path):
    try:
        with open(path, "rb") as f:
            head = f.read(26)
            if head[:8] == b"\x89PNG\r\n\x1a\n":
                return struct.unpack(">II", head[16:24])
            if head[:2] == b"\xff\xd8":
                f.seek(2)
                while True:
                    marker = f.read(2)
                    if len(marker) < 2 or marker[0] != 0xFF:
                        return None
                    seg_len = struct.unpack(">H", f.read(2))[0]
                    if marker[1] in (0xC0, 0xC1, 0xC2):
                        h, w = struct.unpack(">xHH", f.read(5))
                        return w, h
                    f.seek(seg_len - 2, 1)
    except (OSError, struct.error):
        return None
    return None


def norm_image_name(name):
    return re.sub(r"[\s_]+", " ", name.strip().lower())


class ImageIndex:
    def __init__(self, game_dir):
        self.game_dir = game_dir
        self.files = {}        # нормализованное имя → путь относительно game/
        self.defs = {}         # нормализованное имя → [литералы определения]
        self.sizes = {}
        self.cache = {}

        img_root = os.path.join(game_dir, "images")
        for root, _dirs, names in os.walk(img_root):
            for n in names:
                base, ext = os.path.splitext(n)
                if ext.lower() not in IMAGE_EXTS:
                    continue
                rel = os.path.relpath(os.path.join(root, n), game_dir).replace("\\", "/")
                self.files.setdefault(norm_image_name(base), rel)

    def add_definition(self, name, literals):
        self.defs.setdefault(norm_image_name(name), literals)

    def _resolve_ref(self, ref, depth):
        if ref.lower().endswith(IMAGE_EXTS):
            full = os.path.join(self.game_dir, ref)
            return ref if os.path.isfile(full) else None
        return self.resolve(ref, depth + 1)

    def resolve(self, name, depth=0):
        """Имя образа → файл-представитель (относительно game/) или None."""
        if depth > 8 or not name:
            return None
        key = norm_image_name(name)
        if key in self.cache:
            return self.cache[key]
        self.cache[key] = None
        found = None
        if key in self.defs:
            for lit in self.defs[key]:
                found = self._resolve_ref(lit, depth)
                if found:
                    break
        if not found and key in self.files:
            found = self.files[key]
        if not found:
            ## show tag attr: у образа может не быть точного файла, только с доп. атрибутами.
            prefix = key + " "
            for k in sorted(self.files):
                if k.startswith(prefix):
                    found = self.files[k]
                    break
        self.cache[key] = found
        return found

    def is_full_frame(self, rel):
        if rel not in self.sizes:
            self.sizes[rel] = image_size(os.path.join(self.game_dir, rel))
        size = self.sizes[rel]
        return bool(size and size[0] >= FULL_FRAME_MIN[0] and size[1] >= FULL_FRAME_MIN[1])


# ---------------------------------------------------------------- обход файлов

def story_files(game_dir):
    """Все .rpy проекта, кроме dev/tl/libs: (относительный путь, абсолютный)."""
    res = []
    for root, dirs, names in os.walk(game_dir):
        rel_root = os.path.relpath(root, game_dir).replace("\\", "/")
        if rel_root == ".":
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for n in names:
            if n.endswith(".rpy"):
                full = os.path.join(root, n)
                res.append((os.path.relpath(full, game_dir).replace("\\", "/"), full))
    res.sort()
    return res


def is_story_path(rel):
    return "/" in rel and STORY_DIR_RE.match(rel.split("/")[0]) is not None


def logical_statements(lines):
    """Склеивает строки с незакрытыми скобками: [(Line первой строки, номер последней)]."""
    i = 0
    res = []
    while i < len(lines):
        ln = Line(i + 1, lines[i])
        last = i
        if ln.text and not ln.text.startswith("#"):
            bal = bracket_balance(ln.text)
            while bal > 0 and last + 1 < len(lines):
                last += 1
                bal += bracket_balance(lines[last].strip())
        res.append((ln, last + 1))
        i = last + 1
    return res


def collect_image_defs(lines, index):
    stmts = logical_statements(lines)
    for k, (ln, last) in enumerate(stmts):
        m = re.match(r"image\s+([^=:]+?)\s*(=|:)\s*(.*)$", ln.text)
        if not m:
            continue
        name = m.group(1)
        if m.group(2) == "=":
            body = " ".join(l.strip() for l in lines[ln.no - 1:last])
            body = body.split("=", 1)[1]
        else:
            parts = []
            for ln2, _last2 in stmts[k + 1:]:
                if ln2.text and ln2.indent <= ln.indent:
                    break
                parts.append(ln2.text)
            body = " ".join(parts)
        index.add_definition(name, [v for _s, _e, v in string_literals(body)])


def parse_characters(game_dir):
    chars = {}
    path = os.path.join(game_dir, "characters.rpy")
    if not os.path.isfile(path):
        return chars
    for raw in read_lines(path):
        m = re.match(r"\s*define\s+(\w+)\s*=\s*Character\(\s*_\(\s*\"([^\"]*)\"", raw)
        if m:
            chars[m.group(1)] = m.group(2)
    return chars


def parse_nav_titles(game_dir):
    """Подписи сцен из dev-навигатора: label → title."""
    path = os.path.join(game_dir, "dev", "scene_navigation", "scene_navigator.rpy")
    titles = {}
    if not os.path.isfile(path):
        return titles
    text = "\n".join(read_lines(path))
    for m in re.finditer(r'"title":\s*_\("([^"]*)"\),\s*"label":\s*"([^"]+)"', text):
        titles[m.group(2)] = m.group(1)
    return titles


def parse_translations(game_dir, lang="english"):
    """(файл, оригинал) → перевод для реплик; оригинал → перевод для строк _()."""
    say_map, str_map = {}, {}
    root = os.path.join(game_dir, "tl", lang)
    if not os.path.isdir(root):
        return say_map, str_map
    for dirpath, _dirs, names in os.walk(root):
        for n in names:
            if not n.endswith(".rpy"):
                continue
            lines = read_lines(os.path.join(dirpath, n))
            src_file = None
            pending_orig = None
            old = None
            for raw in lines:
                t = raw.strip()
                m = re.match(r"#\s*(game/\S+\.rpy):\d+", t)
                if m:
                    src_file = m.group(1)[5:]
                    continue
                if t.startswith("translate "):
                    pending_orig = None
                    continue
                if t.startswith("#"):
                    say = parse_say(t[1:].strip())
                    if say:
                        pending_orig = say[3]
                    continue
                if t.startswith("old "):
                    lit = string_literals(t[4:])
                    old = lit[0][2] if lit else None
                    continue
                if t.startswith("new ") and old is not None:
                    lit = string_literals(t[4:])
                    if lit:
                        str_map[old] = lit[0][2]
                    old = None
                    continue
                if pending_orig is not None and t:
                    say = parse_say(t)
                    if say:
                        say_map[(src_file, pending_orig)] = say[3]
                    pending_orig = None
    return say_map, str_map


# ---------------------------------------------------------------- разбор лейблов

AUDIO_RE = re.compile(r"\$\s*(mplay|splay|sfxplay|vplay)\(\s*[\"']([^\"']+)")
VISUAL_KEYWORDS = {"at", "as", "behind", "with", "onlayer", "zorder", "expression"}


def parse_visual(stmt, index):
    """show/scene → (kind, name, file, full) или титр show expression с _("...")."""
    m = re.match(r"(show|scene)\s+(.*?)\s*:?\s*$", stmt)
    if not m:
        return None
    kind, rest = m.group(1), m.group(2)
    if rest.startswith("expression"):
        return {"kind": "expr", "rest": rest}
    words = []
    for w in rest.split():
        if w in VISUAL_KEYWORDS:
            break
        words.append(w)
    name = " ".join(words)
    if not name:
        return None
    if name == "black":
        return {"kind": kind, "name": name, "file": None, "full": True, "black": True}
    rel = index.resolve(name)
    full = kind == "scene" or (rel is not None and index.is_full_frame(rel))
    return {"kind": kind, "name": name, "file": rel, "full": full}


def parse_file(rel, lines, index, say_tl, str_tl):
    """Элементы сценария файла, сгруппированные по глобальным лейблам."""
    labels = []
    current = None
    stack = []           # отступы открытых сценарных блоков внутри лейбла
    skip_indent = None   # отступ блока, который пропускается целиком (ATL, python, screen)
    menu_indents = []
    calls = []

    for ln, last in logical_statements(lines):
        t = ln.text
        if not t or t.startswith("#"):
            continue
        if skip_indent is not None:
            if ln.indent > skip_indent:
                ## Конец сцены считается вместе с ATL-блоком: туда дописывается jump при перестановке.
                if current is not None:
                    current["end_line"] = last
                continue
            skip_indent = None

        if ln.indent == 0:
            m = re.match(r"label\s+([\w.]+)", t)
            if m:
                name = m.group(1)
                if name.startswith("."):
                    if current is not None:
                        full = current["label"] + name
                        current["elements"].append({"type": "sublabel", "label": full,
                                                    "line": ln.no, "depth": 0})
                else:
                    current = {"label": name, "file": rel, "line": ln.no, "elements": [],
                               "end_line": ln.no}
                    labels.append(current)
                stack = [0]
                menu_indents = []
                continue
            current = None
            if t.endswith(":"):
                skip_indent = 0
            continue

        if current is None:
            continue

        while stack and stack[-1] >= ln.indent:
            stack.pop()
        while menu_indents and menu_indents[-1] >= ln.indent:
            menu_indents.pop()
        depth = max(0, len(stack) - 1)
        current["end_line"] = last
        el = None
        opens_block = t.endswith(":")
        script_block = False

        in_menu = bool(menu_indents) and ln.indent > menu_indents[-1] and \
            stack and stack[-1] == menu_indents[-1]

        say = parse_say(t)
        if say and in_menu and say[4].endswith(":"):
            who, s, e, value, _rest = say
            el = {"type": "choice", "text": value, "span": [ln.indent + s, ln.indent + e],
                  "en": str_tl.get(value)}
            script_block = True
        elif say and not opens_block:
            who, s, e, value, _rest = say
            el = {"type": "say", "who": who, "text": value,
                  "span": [ln.indent + s, ln.indent + e],
                  "en": say_tl.get((rel, value))}
        elif SCRIPT_BLOCK_RE.match(t):
            script_block = opens_block
            if t.startswith("menu"):
                menu_indents.append(ln.indent)
                el = {"type": "menu"}
            elif t.startswith(("if", "elif", "else", "while")):
                el = {"type": "cond", "text": t.rstrip(":")}
        elif t.startswith(("show ", "scene ")):
            vis = parse_visual(t.rstrip(":") if opens_block else t, index)
            if vis and vis["kind"] == "expr":
                lits = [x for x in string_literals(t) if t[max(0, x[0] - 2):x[0]] == "_("]
                if lits:
                    s, e, value = lits[0]
                    el = {"type": "title", "text": value, "span": [ln.indent + s, ln.indent + e],
                          "en": str_tl.get(value)}
            elif vis:
                el = dict(vis, type="visual")
        elif t.startswith("call "):
            m = re.match(r"call\s+(screen\s+)?([\w.]+)", t)
            if m:
                if m.group(1):
                    el = {"type": "interact", "target": m.group(2)}
                else:
                    el = {"type": "call", "target": m.group(2)}
                    calls.append(m.group(2))
        elif t.startswith("jump "):
            m = re.match(r"jump\s+([\w.]+)\s*$", t)
            if m:
                el = {"type": "jump", "target": m.group(1)}
        elif t == "return" or t.startswith("return "):
            el = {"type": "return"}
        elif re.match(r"pause\b|\$\s*pause\(|\$\s*renpy\.pause\(", t):
            m = re.search(r"([\d.]+)", t)
            el = {"type": "pause", "text": m.group(1) if m else ""}
        else:
            m = AUDIO_RE.match(t)
            if m:
                el = {"type": "audio", "kind": m.group(1), "text": m.group(2)}

        if opens_block:
            if script_block:
                stack.append(ln.indent)
            else:
                skip_indent = ln.indent

        if el is not None:
            el["line"] = ln.no
            el["depth"] = depth
            el.setdefault("raw", ln.raw)
            current["elements"].append(el)

    return labels, calls


def scene_exit(scene):
    """Последний переход сцены на верхнем уровне: элемент jump/return или None."""
    for el in reversed(scene["elements"]):
        if el["depth"] != 0 or el["type"] in ("sublabel",):
            continue
        if el["type"] in ("jump", "return"):
            return el
        return None
    return None


def build_story(game_dir):
    index = ImageIndex(game_dir)
    files = story_files(game_dir)
    file_lines = {}
    for rel, full in files:
        file_lines[rel] = read_lines(full)
        collect_image_defs(file_lines[rel], index)

    chars = parse_characters(game_dir)
    titles = parse_nav_titles(game_dir)
    say_tl, str_tl = parse_translations(game_dir)

    all_labels = {}
    called = set()
    headers = {}
    for rel, _full in files:
        labels, calls = parse_file(rel, file_lines[rel], index, say_tl, str_tl)
        called.update(calls)
        for lab in labels:
            all_labels[lab["label"]] = lab
        head = next((l for l in file_lines[rel] if l.strip()), "")
        if head.startswith("##"):
            headers[rel] = head.lstrip("#").strip()

    scenes = {name: lab for name, lab in all_labels.items()
              if is_story_path(lab["file"]) and name not in called}

    for name, sc in scenes.items():
        sc["title"] = titles.get(name, name)
        first_in_file = min((s["line"] for s in scenes.values() if s["file"] == sc["file"]))
        sc["synopsis"] = headers.get(sc["file"]) if sc["line"] == first_in_file else None
        for el in sc["elements"]:
            if el["type"] == "sublabel":
                el["title"] = titles.get(el["label"], el["label"].split(".", 1)[1])
            if el["type"] == "visual" and el.get("file"):
                el["url"] = "/game/" + el["file"]
        ex = scene_exit(sc)
        sc["exit"] = {"type": ex["type"], "target": ex.get("target"), "line": ex["line"]} if ex else None
        sc["words"] = sum(len(el["text"].split()) for el in sc["elements"]
                          if el["type"] in ("say", "choice", "title"))

    start = all_labels.get("start")
    start_exit = scene_exit(start) if start else None
    head = start_exit["target"] if start_exit and start_exit["type"] == "jump" else None

    chain = []
    seen = set()
    cur = head
    while cur in scenes and cur not in seen:
        chain.append(cur)
        seen.add(cur)
        ex = scenes[cur]["exit"]
        cur = ex["target"] if ex and ex["type"] == "jump" else None

    orphans = sorted((n for n in scenes if n not in seen),
                     key=lambda n: (scenes[n]["file"], scenes[n]["line"]))

    return {
        "chain": chain,
        "orphans": orphans,
        "scenes": scenes,
        "characters": chars,
        "start": {"file": start["file"], "exit_line": start_exit["line"]} if start_exit else None,
    }
