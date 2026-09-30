## RMB EDITOR (dev-only): Shift+ПКМ в игре → промпт Claude в новой вкладке VS Code.
## Здесь сбор контекста клика и сборка запроса; жест, пауза и поле ввода — в rmb_editor_ui.rpy.
## Строки намеренно не локализуются.

## Экраны инструмента — на слое top (имя слоя вычисляется при объявлении экрана, раньше define,
## поэтому записано в них литералом). Порядок на слое: зерно (0) → поле с фоном → перехватчик.
define -30 RMB_FIELD_ZORDER = 1200
define -30 RMB_CATCHER_ZORDER = 1300

define -30 RMB_DIR = ".rmb_editor"
define -30 RMB_KEEP = 10

define -30 RMB_URL = "vscode://anthropic.claude-code/open?prompt="
## Проверено: ссылка в 3308 символов доходит до расширения целиком.
define -30 RMB_URL_MAX = 3000

## Полноэкранные служебные экраны: без исключения попадали бы в каждый запрос.
define -30 RMB_SKIP_SCREENS = ("fx_noise_screen", "fx_vignette_screen", "fx_flash_screen")

define -30 RMB_MAX_LINES = 12
define -30 RMB_MAX_WIDGETS = 40
define -30 RMB_TEXT_MAX = 80

## Сколько обёрток-трансформов просматривать между записью scene list и displayable из дерева.
define -30 RMB_CHILD_DEPTH = 4


init -20 python:

    import io as _rmb_io
    import os as _rmb_os
    import re as _rmb_re
    import shutil as _rmb_shutil
    import struct as _rmb_struct
    import time as _rmb_time
    import urllib.parse as _rmb_urlparse

    _RMB_REQ_RE = _rmb_re.compile(r"^req_\d{8}_\d{6}_\d{3}$")
    _RMB_LABEL_RE = _rmb_re.compile(r"^label\s+([A-Za-z_]\w*)")
    _RMB_SCENE_RE = _rmb_re.compile(r"^(\s*)scene\b")

    ## Подмены для тестов. Не в renpy.session: перезагрузку скриптов они переживать не должны.
    _rmb_override = python_dict(opener=None, root=None, shift=None)

    def rmb_data():
        """Данные запроса. renpy.session переживает перезагрузку скриптов и не входит
        в сейвы и rollback; внутри — только простые типы, без объектов классов store."""
        d = renpy.session.get("_rmb_editor")
        if d is None:
            d = python_dict(open=False, text="", files=python_list(), ctx=None, dir=None, error="")
            renpy.session["_rmb_editor"] = d
        return d

    ## Путь от корня проекта через /; вне проекта — абсолютный.
    def _rmb_rel(path):
        path = path.replace("\\", "/")
        if not _rmb_os.path.isabs(path):
            return path
        try:
            rel = _rmb_os.path.relpath(path, config.basedir).replace("\\", "/")
        except ValueError:
            return path
        return path if rel.startswith("../") else rel

    def _rmb_file_lines(path, cache):
        lines = cache.get(path)
        if lines is None:
            try:
                with _rmb_io.open(path, encoding="utf-8-sig") as f:
                    lines = f.read().splitlines()
            except Exception:
                lines = python_list()
            cache[path] = lines
        return lines

    def _rmb_num(v):
        return None if v is None else round(float(v), 3)


init -20 python:

    def _rmb_script_pos(cache):
        """Позиция базового контекста: в меню renpy.get_filename_line() указывает на renpy/common."""
        if main_menu:
            return None
        try:
            node = renpy.game.script.namemap.get(renpy.game.contexts[0].current)
        except Exception:
            node = None
        if node is None:
            return None
        fn = node.filename.replace("\\", "/")
        if fn.startswith("renpy/"):
            return None
        lines = _rmb_file_lines(_rmb_os.path.join(config.basedir, fn), cache)
        return python_dict(file=fn, line=node.linenumber, label=_rmb_label_at(lines, node.linenumber))

    def _rmb_label_at(lines, line):
        """Ближайший глобальный лейбл выше строки; служебные (с _) не называются."""
        for i in range(min(line, len(lines)) - 1, -1, -1):
            m = _RMB_LABEL_RE.match(lines[i])
            if m:
                return None if m.group(1).startswith("_") else m.group(1)
        return None

    def _rmb_foreign(loc):
        if not loc:
            return False
        fn = loc[0].replace("\\", "/")
        return fn.startswith("renpy/") or fn.startswith("game/dev/")

    def _rmb_tree(x, y, layers):
        """Дерево отрисовки под точкой, как у инспектора Ren'Py: (depth, width, height, displayable)."""
        surftree = renpy.game.interface.surftree
        if surftree is None:
            return python_list()
        return surftree.main_displayables_at_point(x, y, layers)

    class _RMBName(python_object):
        def __init__(self, name):
            self.name = name

    def _rmb_code_lines(name, script_file, cache):
        target = _RMBName(name)
        found = python_list()
        for path in _pt_rpy_files():
            rel = _rmb_rel(path)
            for i, line in enumerate(_rmb_file_lines(path, cache)):
                ## _pt_show_matches знает только show; scene сопоставляется тем же правилом.
                if _pt_show_matches(_RMB_SCENE_RE.sub(r"\1show", line, count=1), target):
                    found.append((rel != script_file, rel, i + 1, line.strip()))
        found.sort()
        return python_list(
            python_dict(file=rel, line=n, text=text, current=not other)
            for other, rel, n, text in found)

    def _rmb_in_tree(d, hit):
        for _i in range(RMB_CHILD_DEPTH):
            if d is None:
                return False
            if id(d) in hit:
                return True
            d = getattr(d, "child", None)
        return False

    def _rmb_sprites(x, y, script_file, cache):
        out = python_list()
        ## pt_showing() заодно заполняет карту «тег → слой» для pt_scene_state.
        names = python_dict((name.split(" ")[0], name) for name in pt_showing())
        sl = renpy.scene_lists()
        for layer in _pt_layers():
            hit = set(id(d) for _depth, _w, _h, d in _rmb_tree(x, y, (layer,)))
            if not hit:
                continue
            for sle in sl.layers.get(layer, ()):
                name = names.get(sle.tag)
                if name is None or isinstance(sle.displayable, renpy.display.screen.ScreenDisplayable):
                    continue
                if not _rmb_in_tree(sle.displayable, hit):
                    continue
                st = pt_scene_state(name)
                lines = _rmb_code_lines(name, script_file, cache)
                out.append(python_dict(
                    name=name, layer=layer,
                    pos=tuple(st["pos"]), anchor=tuple(st["anchor"]),
                    rotate=_rmb_num(st["rotate"]), zoom=_rmb_num(st["zoom"]),
                    size=tuple(st["bounds"][2:]) if st["bounds"] else tuple(st["natural"]),
                    lines=python_list(lines[:RMB_MAX_LINES]),
                    lines_more=max(0, len(lines) - RMB_MAX_LINES)))
        return out

    def _rmb_what(d):
        parts = python_list((type(d).__name__,))
        try:
            info = d._repr_info()
        except Exception:
            info = None
        if info:
            parts.append(str(info))
        if getattr(d, "id", None):
            parts.append("id %s" % d.id)
        return " ".join(parts)

    def _rmb_widgets(x, y):
        out = python_list()
        screen = None
        ## Последний записанный элемент и его глубина: текст без _location приписывается только потомку.
        last = None
        for depth, w, h, d in _rmb_tree(x, y, config.layers):
            if screen is not None and depth <= screen[0]:
                screen = None
            if last is not None and depth <= last[0]:
                last = None
            ## Экран рендерится на весь кадр и сам элементом не считается — от него только имя.
            if isinstance(d, renpy.display.screen.ScreenDisplayable):
                name = d.screen_name[0]
                screen = (depth, name, name in RMB_SKIP_SCREENS or _rmb_foreign(d._location))
                last = None
                continue
            if screen is None or screen[2]:
                continue
            loc = getattr(d, "_location", None)
            if not loc:
                ## _location есть только у главного displayable оператора экрана:
                ## текст кнопки описывает ближайшего предка.
                if last is not None and not last[1]["text"] and isinstance(d, renpy.text.text.Text):
                    last[1]["text"] = "".join(p for p in d.text if isinstance(p, str))[:RMB_TEXT_MAX]
                continue
            if _rmb_foreign(loc):
                last = None
                continue
            last = (depth, python_dict(
                screen=screen[1], what=_rmb_what(d), size=(int(w), int(h)),
                file=loc[0].replace("\\", "/"), line=loc[1], text=""))
            out.append(last[1])
        return python_list(out[-RMB_MAX_WIDGETS:])

    def _rmb_screens():
        out = python_list()
        sl = renpy.scene_lists()
        for layer in tuple(config.layers) + tuple(config.top_layers):
            for sle in sl.layers.get(layer, ()):
                d = sle.displayable
                if not isinstance(d, renpy.display.screen.ScreenDisplayable):
                    continue
                name = d.screen_name[0]
                if name in RMB_SKIP_SCREENS or name in out or _rmb_foreign(d._location):
                    continue
                out.append(name)
        return out

    def _rmb_part(fn, *args):
        """Сбой одной части контекста не роняет запрос: часть остаётся пустой."""
        try:
            return fn(*args)
        except Exception:
            renpy.display.log.write("rmb_editor: %s failed", fn.__name__)
            renpy.display.log.exception()
            return python_list()

    def rmb_context(x=None, y=None):
        """Контекст клика; без точки (бросок файла, Dev Hub) — только сценарий и экраны."""
        cache = python_dict()
        script = _rmb_script_pos(cache)
        in_menu = bool(main_menu or renpy.context()._menu)
        ctx = python_dict(
            point=None, shot=None, menu=in_menu, main_menu=bool(main_menu), script=script,
            sprites=python_list(), widgets=python_list(),
            screens=_rmb_part(_rmb_screens))
        if x is None or y is None or x < 0 or y < 0:
            return ctx
        ctx["point"] = (int(x), int(y))
        if not in_menu:
            ctx["sprites"] = _rmb_part(_rmb_sprites, x, y, script["file"] if script else None, cache)
        ctx["widgets"] = _rmb_part(_rmb_widgets, x, y)
        return ctx

    def rmb_summary(ctx):
        """Строка над полем: самый мелкий объект под точкой, как выбор в Position Tuner."""
        best = None
        at = ctx["script"]["line"] if ctx["script"] else 0
        for s in ctx["sprites"]:
            ## Строка кода называется, только если она однозначна: ближайшая выше позиции
            ## сценария в текущем файле или единственная на весь проект.
            line = None
            current = [l for l in s["lines"] if l["current"]]
            if current:
                above = [l for l in current if l["line"] <= at]
                line = above[-1] if above else current[0]
            elif len(s["lines"]) + s["lines_more"] == 1:
                line = s["lines"][0]
            where = "%s:%d" % (line["file"], line["line"]) if line else "слой %s" % s["layer"]
            area = s["size"][0] * s["size"][1]
            if best is None or area <= best[0]:
                best = (area, "%s · %s" % (s["name"], where))
        for w in ctx["widgets"]:
            area = w["size"][0] * w["size"][1]
            if best is None or area <= best[0]:
                label = " «%s»" % w["text"] if w["text"] else ""
                best = (area, "%s%s · %s:%d" % (w["screen"], label, w["file"], w["line"]))
        if best is not None:
            return best[1]
        if ctx["script"]:
            return "%s:%d" % (ctx["script"]["file"], ctx["script"]["line"])
        return "главное меню" if ctx["main_menu"] else "—"


init -20 python:

    def _rmb_root():
        return _rmb_override["root"] or _rmb_os.path.join(config.basedir, RMB_DIR)

    def _rmb_prune(root, keep):
        ## Удаляются только папки своего формата имени. Возраст — по времени создания, а не по
        ## имени: имя строится от местного времени и при переводе часов идёт не по порядку.
        dirs = [
            _rmb_os.path.join(root, n) for n in _rmb_os.listdir(root)
            if _RMB_REQ_RE.match(n) and _rmb_os.path.isdir(_rmb_os.path.join(root, n))]
        dirs = [p for p in dirs if p != keep]
        dirs.sort(key=lambda p: (_rmb_os.path.getmtime(p), p))
        for p in dirs[:max(0, len(dirs) - (RMB_KEEP - 1))]:
            _rmb_shutil.rmtree(p, ignore_errors=True)

    def _rmb_new_dir():
        root = _rmb_root()
        now = _rmb_time.time()
        while True:
            name = _rmb_time.strftime("req_%Y%m%d_%H%M%S", _rmb_time.localtime(now)) + "_%03d" % (int(now * 1000) % 1000)
            path = _rmb_os.path.join(root, name)
            if not _rmb_os.path.exists(path):
                break
            now += 0.001
        _rmb_os.makedirs(path)
        _rmb_prune(root, path)
        return path

    def _rmb_remove_dir(path):
        if not path or not _RMB_REQ_RE.match(_rmb_os.path.basename(path)):
            return
        if _rmb_os.path.abspath(_rmb_os.path.dirname(path)) != _rmb_os.path.abspath(_rmb_root()):
            return
        _rmb_shutil.rmtree(path, ignore_errors=True)

    def _rmb_png_size(path):
        try:
            with _rmb_io.open(path, "rb") as f:
                head = f.read(24)
        except Exception:
            return None
        if len(head) < 24 or head[:8] != b"\x89PNG\r\n\x1a\n":
            return None
        return tuple(_rmb_struct.unpack(">II", head[16:24]))

    def rmb_begin(x=None, y=None, files=()):
        """Вызывается до показа поля: скриншот — последний отрисованный кадр."""
        d = rmb_data()
        ctx = rmb_context(x, y)
        path = _rmb_new_dir()
        shot = _rmb_os.path.join(path, "shot.png")
        try:
            saved = renpy.screenshot(shot)
        except Exception:
            saved = False
        size = _rmb_png_size(shot) if saved else None
        if size:
            ## Скриншот снят в размере окна, а координаты клика — виртуальные.
            point = None
            if ctx["point"]:
                point = (
                    int(round(ctx["point"][0] * size[0] / float(config.screen_width))),
                    int(round(ctx["point"][1] * size[1] / float(config.screen_height))))
            ctx["shot"] = python_dict(size=size, point=point)
        d.update(open=True, text="", files=python_list(files), ctx=ctx, dir=path, error="")

    def rmb_add_file(path):
        d = rmb_data()
        if path not in d["files"]:
            d["files"].append(path)

    def rmb_remove_file(i):
        d = rmb_data()
        if 0 <= i < len(d["files"]):
            d["files"].pop(i)


init -20 python:

    def rmb_request_text(d):
        ctx = d["ctx"]
        out = python_list()
        out.append("# Запрос из игры")
        out.append("")
        out.append("## Что сделать")
        out.append("")
        out.append(d["text"] if d["text"].strip() else "(текст не задан — задача описана в сообщении чата)")
        out.append("")
        if d["files"]:
            out.append("## Приложенные файлы")
            out.append("")
            for f in d["files"]:
                out.append("- `%s`" % f)
            out.append("")
        out.append("## Клик")
        out.append("")
        out.append("- объект: %s" % rmb_summary(ctx))
        if ctx["point"]:
            out.append("- точка: (%d, %d) в координатах игры %d×%d" % (
                ctx["point"][0], ctx["point"][1], config.screen_width, config.screen_height))
        else:
            out.append("- точки нет: запрос открыт без клика")
        if ctx["shot"]:
            line = "- скриншот кадра: `shot.png` рядом с этим файлом, %d×%d" % ctx["shot"]["size"]
            if ctx["shot"]["point"]:
                line += ", клик на нём — (%d, %d)" % ctx["shot"]["point"]
            out.append(line)
        out.append("")
        if ctx["sprites"]:
            out.append("## Спрайты под курсором")
            out.append("")
            out.append("Попадание — по прямоугольнику нарисованного спрайта, без учёта прозрачности. Числа — как в коде.")
            out.append("")
            for s in ctx["sprites"]:
                out.append("### `%s` (слой %s)" % (s["name"], s["layer"]))
                out.append("")
                out.append("- pos %s, anchor %s, rotate %s, zoom %s" % (s["pos"], s["anchor"], s["rotate"], s["zoom"]))
                for l in s["lines"]:
                    out.append("- %s:%d%s — `%s`" % (
                        l["file"], l["line"], " (текущий файл сценария)" if l["current"] else "", l["text"]))
                if s["lines_more"]:
                    out.append("- …и ещё строк: %d" % s["lines_more"])
                if not s["lines"]:
                    out.append("- строк show/scene в сценарных файлах не найдено")
                out.append("")
        if ctx["widgets"]:
            out.append("## Элементы экранов под курсором")
            out.append("")
            for w in ctx["widgets"]:
                out.append("- экран `%s` · %s%s · %d×%d — %s:%d" % (
                    w["screen"], w["what"], " «%s»" % w["text"] if w["text"] else "",
                    w["size"][0], w["size"][1], w["file"], w["line"]))
            out.append("")
        out.append("## Сценарий")
        out.append("")
        if ctx["script"]:
            out.append("- позиция: %s:%d%s" % (
                ctx["script"]["file"], ctx["script"]["line"],
                ", лейбл `%s`" % ctx["script"]["label"] if ctx["script"]["label"] else ""))
        else:
            out.append("- позиции нет%s" % (": главное меню" if ctx["main_menu"] else ""))
        if ctx["menu"]:
            out.append("- клик сделан в меню: спрайты сцены не собирались")
        if ctx["screens"]:
            out.append("- показаны экраны: %s" % ", ".join("`%s`" % n for n in ctx["screens"]))
        out.append("")
        return "\n".join(out)

    def rmb_prompt(d):
        rel = _rmb_rel(_rmb_os.path.join(d["dir"], "request.md"))
        parts = python_list()
        if d["text"].strip():
            parts.append(d["text"])
            parts.append("")
        parts.append("Поймано в игре: %s" % rmb_summary(d["ctx"]))
        if d["files"]:
            parts.append("Файлы:")
            for f in d["files"]:
                parts.append("- %s" % f)
        parts.append("Контекст и скриншот: %s" % rel)
        full = "\n".join(parts)
        if len(RMB_URL + _rmb_urlparse.quote(full, safe="")) <= RMB_URL_MAX:
            return full
        return "Запрос из игры: прочитай %s и выполни его." % rel

    def rmb_url(d):
        ## Расширение разбирает запрос через URLSearchParams, где «+» — пробел: quote_plus нельзя.
        return RMB_URL + _rmb_urlparse.quote(rmb_prompt(d), safe="")

    def _rmb_startfile(url):
        ## Потомок extension host VS Code наследует ELECTRON_RUN_AS_NODE: с ней Code.exe
        ## запускается как Node и отбрасывает ссылку, а os.startfile исключения не даёт.
        saved = _rmb_os.environ.pop("ELECTRON_RUN_AS_NODE", None)
        try:
            _rmb_os.startfile(url)
        finally:
            if saved is not None:
                _rmb_os.environ["ELECTRON_RUN_AS_NODE"] = saved

    def _rmb_open_url(url):
        if renpy.is_in_test():
            return
        _rmb_startfile(url)

    def rmb_send():
        """True — отправлено; None — ошибка, поле остаётся открытым."""
        d = rmb_data()
        try:
            if not _rmb_os.path.isdir(d["dir"]):
                _rmb_os.makedirs(d["dir"])
            with _rmb_io.open(_rmb_os.path.join(d["dir"], "request.md"), "w", encoding="utf-8", newline="\n") as f:
                f.write(rmb_request_text(d))
            (_rmb_override["opener"] or _rmb_open_url)(rmb_url(d))
        except Exception as e:
            d["error"] = "не отправлено: %s" % e
            return None
        d["error"] = ""
        return True

    def rmb_cancel():
        _rmb_remove_dir(rmb_data()["dir"])
        return False
