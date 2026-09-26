## POSITION TUNER · запись в код (dev-only)
## Ищет в .rpy строку `show <спрайт> ... at <вызов>(pos, anchor, angle)` с текущими
## значениями сцены и переписывает литералы. Константы и выражения не трогает:
## если в вызове не литерал, строка пропускается с сообщением.

## Вызовы, чьи аргументы можно переписывать: имя → (индекс pos, индекс/ключ anchor, индекс/ключ angle).
## None — параметра у вызова нет.
define -30 PT_WRITE_CALLS = {
    "placed": ((0, "pos_xy"), (1, "anchor_xy"), (2, "angle")),
    "placed_jitter": ((0, "pos_xy"), (1, "anchor_xy"), None),
}

## Каталоги game/, в которых запись не ищется.
define -30 PT_WRITE_SKIP_DIRS = ("dev", "tl", "libs", "cache", "saves")


init -20 python:

    import ast as _pt_ast
    import io as _pt_io
    import os as _pt_os

    _PT_SHOW_RE = _pt_re.compile(r"^(\s*)show\s+(.+?)(?=\s+(?:as|at|zorder|onlayer|behind|with)\b|\s*:?\s*$)")
    _PT_AS_RE = _pt_re.compile(r"\bas\s+(\w+)")

    def _pt_rpy_files():
        root = config.gamedir
        for base, dirs, files in _pt_os.walk(root):
            rel = _pt_os.path.relpath(base, root).replace("\\", "/")
            if rel.split("/")[0] in PT_WRITE_SKIP_DIRS:
                dirs[:] = []
                continue
            for f in files:
                if f.endswith(".rpy"):
                    yield _pt_os.path.join(base, f)

    def _pt_call_span(line, name, start):
        """(начало имени, конец скобки) первого вызова name( после start."""
        m = _pt_re.compile(r"\b%s\(" % _pt_re.escape(name)).search(line, start)
        if not m:
            return None
        depth = 0
        for i in range(m.end() - 1, len(line)):
            if line[i] == "(":
                depth += 1
            elif line[i] == ")":
                depth -= 1
                if depth == 0:
                    return m.start(), i + 1
        return None

    ## Маркер «не литерал»: None — законное значение angle.
    _PT_NOT_LITERAL = python_object()

    def _pt_literal(node):
        try:
            return _pt_ast.literal_eval(node)
        except Exception:
            return _PT_NOT_LITERAL

    def _pt_arg(call, spec):
        """(узел, где) аргумента по спецификации (индекс, ключ); где — ("pos", i) или ("kw", k)."""
        idx, kw = spec
        for k in call.keywords:
            if k.arg == kw:
                return k.value, ("kw", kw)
        if idx < len(call.args):
            return call.args[idx], ("pos", idx)
        return None, None

    def _pt_same(a, b, eps=0.51):
        if a is None or b is None:
            return a is None and b is None
        if isinstance(a, (tuple, list)):
            return (isinstance(b, (tuple, list)) and len(a) == len(b)
                    and all(_pt_same(x, y, eps) for x, y in zip(a, b)))
        try:
            return abs(float(a) - float(b)) < eps
        except Exception:
            return False

    def _pt_lit(v):
        if isinstance(v, tuple):
            return "(%s)" % ", ".join(_pt_lit(x) for x in v)
        if isinstance(v, float):
            return _pt_num(v)
        return repr(v)

    def _pt_rewrite_call(text, specs, t):
        """Новый текст вызова или (None, причина)."""
        try:
            call = _pt_ast.parse(text, mode="eval").body
        except Exception:
            return None, "не разобрать вызов"
        pos_spec, anchor_spec, angle_spec = specs
        s = t.scene

        node, _ = _pt_arg(call, pos_spec)
        if node is None or _pt_literal(node) is _PT_NOT_LITERAL:
            return None, "pos не литерал"
        if not _pt_same(_pt_literal(node), s["pos"]):
            return None, "pos в коде не совпадает со сценой"

        edits = [(pos_spec, tuple(int(round(v)) for v in t.pos), None)]
        if tuple(t.anchor) != tuple(s["anchor"]):
            if anchor_spec is None:
                return None, "у вызова нет anchor"
            edits.append((anchor_spec, tuple(round(float(v), 4) for v in t.anchor), (0.0, 0.0)))
        if t.rotate != s["rotate"]:
            if angle_spec is None:
                return None, "у вызова нет угла"
            edits.append((angle_spec, t.rotate, None))

        for spec, value, default in edits:
            node, where = _pt_arg(call, spec)
            if node is not None and _pt_literal(node) is _PT_NOT_LITERAL:
                return None, "аргумент %s не литерал" % spec[1]
            new = _pt_ast.parse(_pt_lit(value), mode="eval").body
            if where is None:
                ## Пропущенные позиционные аргументы дописываем ключом, чтобы не сдвигать остальные.
                call.keywords.append(_pt_ast.keyword(arg=spec[1], value=new))
            elif where[0] == "kw":
                for k in call.keywords:
                    if k.arg == where[1]:
                        k.value = new
            else:
                call.args[where[1]] = new
        return _pt_ast.unparse(call), None

    def _pt_show_matches(line, t):
        m = _PT_SHOW_RE.match(line)
        if not m:
            return False
        name = m.group(2).split()
        tag = t.name.split(" ")[0]
        alias = _PT_AS_RE.search(line[m.end():])
        if alias:
            return alias.group(1) == tag
        if not name or name[0] != tag:
            return False
        ## Атрибуты в show должны быть подмножеством показанных.
        return set(name[1:]) <= set(t.name.split(" ")[1:])

    def pt_write_target(t):
        """Список (файл, строка) переписанных мест и список причин пропуска."""
        written, skipped = python_list(), python_list()
        for path in _pt_rpy_files():
            with _pt_io.open(path, encoding="utf-8", newline="") as f:
                lines = f.read().splitlines(True)
            changed = False
            for i, line in enumerate(lines):
                if not _pt_show_matches(line, t):
                    continue
                at = line.find(" at ")
                if at < 0:
                    continue
                for name, specs in PT_WRITE_CALLS.items():
                    span = _pt_call_span(line, name, at)
                    if span is None:
                        continue
                    new, why = _pt_rewrite_call(line[span[0]:span[1]], specs, t)
                    rel = _pt_os.path.relpath(path, config.gamedir).replace("\\", "/")
                    if new is None:
                        skipped.append("%s:%d — %s" % (rel, i + 1, why))
                    else:
                        lines[i] = line[:span[0]] + new + line[span[1]:]
                        written.append("%s:%d" % (rel, i + 1))
                        changed = True
                    break
            if changed:
                with _pt_io.open(path, "w", encoding="utf-8", newline="") as f:
                    f.write("".join(lines))
        return written, skipped

    def _pt_apply_live(t):
        """Двигает живой спрайт, чтобы сцена совпала с записанным кодом до перезагрузки."""
        d = _pt_live(t.name)
        if d is None:
            return
        d.xpos, d.ypos = (absolute(t.pos[0]), absolute(t.pos[1]))
        d.xanchor, d.yanchor = t.anchor
        if t.rotate is not None:
            d.rotate = t.rotate
            d.transform_anchor = True
        renpy.redraw(d, 0)

    def pt_write():
        dirty = [t for t in pt_model.targets.values() if t.dirty]
        if not dirty:
            pt_model.status = "записывать нечего: изменений нет"
            return
        report = python_list()
        for t in dirty:
            written, skipped = pt_write_target(t)
            if written:
                _pt_apply_live(t)
                t.resync(pt_scene_state(t.name))
                report.append("%s → %s" % (t.name, ", ".join(written)))
            elif skipped:
                report.append("{color=#f66}%s не записан: %s{/color}" % (t.name, "; ".join(skipped)))
            else:
                report.append("{color=#f66}%s: не нашёл show ... at placed(...){/color}" % t.name)
        pt_model.undo.clear()
        pt_model.redo.clear()
        pt_model.status = "\n".join(report)
