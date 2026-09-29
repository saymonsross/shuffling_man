## Сквозные параметры визуальных эффектов; значения — game/fx_config.yaml.
## Это настройка проекта, а не состояние игры: python_dict держит значения
## вне rollback и сейвов. Пишет файл только dev-сборка (FX Tuner, F10).

define -20 FX_CONFIG_FILE = "fx_config.yaml"

init -15 python:

    import math as _fxc_math
    import re as _fxc_re

    class FxConfigError(Exception):
        pass

    class FxParam(python_object):
        """Тип выводится из default: bool, int, float, str с choices или цвет "#rrggbb"."""

        def __init__(self, key, default, lo, hi, step, choices, doc):
            self.key = key
            self.group, self.name = key.split(".", 1)
            self.default = default
            self.choices = tuple(choices) if choices else None
            self.doc = doc
            if isinstance(default, bool):
                self.kind = "bool"
            elif isinstance(default, str) and default.startswith("#"):
                self.kind = "color"
            elif self.choices:
                self.kind = "choice"
            elif isinstance(default, int):
                self.kind = "int"
            else:
                self.kind = "float"
            ## Границы приводятся к типу параметра, иначе прижатие сменит тип значения.
            cast = {"float": float, "int": int}.get(self.kind, lambda v: v)
            self.lo = None if lo is None else cast(lo)
            self.hi = None if hi is None else cast(hi)
            if step is None:
                if self.kind == "int":
                    step = 1
                elif lo is not None and hi is not None:
                    step = (hi - lo) / 100.0
                else:
                    step = 0.01
            self.step = step
            self.coerce(default)

        def coerce(self, value):
            """ValueError для чужого типа; число вне диапазона прижимается."""
            if self.kind == "bool":
                if not isinstance(value, bool):
                    raise ValueError("ожидалось true/false")
                return value
            if self.kind == "choice":
                if value not in self.choices:
                    raise ValueError("ожидалось одно из: " + ", ".join(self.choices))
                return value
            if self.kind == "color":
                if not isinstance(value, str) or not _FXC_COLOR.match(value):
                    raise ValueError("ожидался цвет \"#rrggbb\"")
                value = value.lower()
                ## #rgb → #rrggbb: в файле и в сравнении «несохранённого» одна запись.
                return value if len(value) == 7 else "#" + "".join(c * 2 for c in value[1:])
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise ValueError("ожидалось число")
            if not _fxc_math.isfinite(value):
                raise ValueError("ожидалось конечное число")
            ## round(…, 6) убирает шум float от шагов слайдера из YAML.
            value = int(round(value)) if self.kind == "int" else round(float(value), 6)
            if self.lo is not None:
                value = max(value, self.lo)
            if self.hi is not None:
                value = min(value, self.hi)
            return value

    _fxc_params = python_dict()
    _fxc_groups = python_dict()
    _fxc_values = python_dict()
    ## Значения, которые дал бы файл на диске: база для маркера несохранённого.
    _fxc_saved = python_dict()
    ## Плоский «group.key → значение» последнего чтения, включая незарегистрированные ключи.
    _fxc_file = python_dict()
    ## Сообщения о значениях файла, отброшенных при последнем чтении.
    fx_cfg_warnings = python_list()
    ## Dev-переключатели тюнера, в файл не пишутся.
    fx_cfg_runtime = python_dict(bypass=False, preview=False)

    _FXC_KEY = _fxc_re.compile(r"^[A-Za-z0-9_][A-Za-z0-9_.\-]*$")
    _FXC_INT = _fxc_re.compile(r"^[-+]?[0-9]+$")
    _FXC_COLOR = _fxc_re.compile(r"^#(?:[0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})$")

    def _fxc_strip_comment(line):
        quote = None
        escaped = False
        for i, ch in enumerate(line):
            if quote:
                if escaped:
                    escaped = False
                elif ch == "\\" and quote == '"':
                    escaped = True
                elif ch == quote:
                    quote = None
            elif ch in "\"'" and (i == 0 or line[i - 1] in " \t:[,"):
                quote = ch
            elif ch == "#" and (i == 0 or line[i - 1] in " \t"):
                return line[:i]
        return line

    def _fxc_split_flow(body, n):
        items = python_list()
        cur = ""
        quote = None
        escaped = False
        for ch in body:
            if quote:
                cur += ch
                if escaped:
                    escaped = False
                elif ch == "\\" and quote == '"':
                    escaped = True
                elif ch == quote:
                    quote = None
            elif ch in "\"'":
                quote = ch
                cur += ch
            elif ch == ",":
                items.append(cur)
                cur = ""
            else:
                cur += ch
        if quote:
            raise FxConfigError("строка %d: незакрытая кавычка" % n)
        if cur.strip() or items:
            items.append(cur)
        return [_fxc_scalar(i.strip(), n) for i in items]

    def _fxc_scalar(s, n):
        if not s:
            return None
        if s[0] in "\"'":
            q = s[0]
            if len(s) < 2 or s[-1] != q:
                raise FxConfigError("строка %d: незакрытая кавычка" % n)
            body = s[1:-1]
            if q == "'":
                return body.replace("''", "'")
            out = ""
            i = 0
            while i < len(body):
                ch = body[i]
                if ch == "\\" and i + 1 < len(body):
                    i += 1
                    out += {"n": "\n", "t": "\t"}.get(body[i], body[i])
                else:
                    out += ch
                i += 1
            return out
        if s[0] == "[":
            if s[-1] != "]":
                raise FxConfigError("строка %d: незакрытый список" % n)
            return _fxc_split_flow(s[1:-1], n)
        low = s.lower()
        if low in ("true", "yes", "on"):
            return True
        if low in ("false", "no", "off"):
            return False
        if low in ("null", "~"):
            return None
        try:
            if _FXC_INT.match(s):
                return int(s)
            v = float(s)
        except ValueError:
            return s
        return v if _fxc_math.isfinite(v) else s

    def fx_cfg_parse(text):
        """Подмножество YAML: вложенные словари, скаляры, [списки], # комментарии.
        Возвращает плоский словарь с ключами через точку."""
        out = python_dict()
        ## [отступ ключа-родителя, префикс, отступ его детей]
        stack = [[-1, "", None]]
        scalar_indent = None
        for n, raw in enumerate(text.lstrip(chr(0xFEFF)).splitlines(), 1):
            line = _fxc_strip_comment(raw).rstrip()
            if not line.strip():
                continue
            body = line.lstrip(" ")
            if body[0] == "\t":
                raise FxConfigError("строка %d: табуляция в отступе" % n)
            if body.startswith("- ") or body == "-":
                raise FxConfigError("строка %d: блочные списки не поддерживаются, пишите [a, b]" % n)
            indent = len(line) - len(body)
            key, sep, rest = body.partition(":")
            key = key.strip()
            if not sep or not _FXC_KEY.match(key) or (rest and rest[0] not in " \t"):
                raise FxConfigError("строка %d: ожидалось «ключ: значение»" % n)
            if scalar_indent is not None and indent > scalar_indent:
                raise FxConfigError("строка %d: отступ под значением, а не под группой" % n)
            while indent <= stack[-1][0]:
                stack.pop()
            parent = stack[-1]
            if parent[2] is None:
                parent[2] = indent
            elif indent != parent[2]:
                raise FxConfigError("строка %d: неровный отступ" % n)
            full = parent[1] + key
            rest = rest.strip()
            if rest:
                out[full] = _fxc_scalar(rest, n)
                scalar_indent = indent
            else:
                stack.append([indent, full + ".", None])
                scalar_indent = None
        return out

    def _fxc_read_file():
        ## open_file, а не loadable: loadable кеширует и отрицательный ответ.
        try:
            f = renpy.open_file(FX_CONFIG_FILE)
        except FileNotFoundError:
            return python_dict()
        except OSError as e:
            raise FxConfigError(str(e))
        with f:
            data = f.read()
        try:
            return fx_cfg_parse(data.decode("utf-8-sig"))
        except UnicodeDecodeError:
            raise FxConfigError("файл не в UTF-8")

    def _fxc_resolve(param):
        if param.key not in _fxc_file:
            return param.default
        raw = _fxc_file[param.key]
        try:
            return param.coerce(raw)
        except ValueError as e:
            fx_cfg_warnings.append("%s: %r — %s, взят дефолт" % (param.key, raw, e))
            return param.default

    def fx_param(key, default, lo=None, hi=None, step=None, choices=None, doc=""):
        """Регистрирует параметр «группа.имя»; значение берётся из файла или default."""
        if key.count(".") != 1:
            raise FxConfigError("ключ %r: нужен формат «группа.имя»" % key)
        if key in _fxc_params:
            raise FxConfigError("параметр %r уже зарегистрирован" % key)
        param = FxParam(key, default, lo, hi, step, choices, doc)
        _fxc_params[key] = param
        _fxc_groups.setdefault(param.group, python_dict(title=param.group, status=None))
        value = _fxc_resolve(param)
        _fxc_values[key] = value
        _fxc_saved[key] = value
        return value

    def fx_group(name, title, status=None):
        """Подпись группы в тюнере; status() возвращает строку живого состояния."""
        _fxc_groups[name] = python_dict(title=title, status=status)

    def fx_cfg(key):
        return _fxc_values[key]

    def fx_cfg_rgba(key):
        """Цветовой параметр как (r, g, b, 1.0) для uniform шейдера."""
        return Color(_fxc_values[key]).rgb + (1.0,)

    def fx_cfg_set(key, value):
        value = _fxc_params[key].coerce(value)
        _fxc_values[key] = value
        return value

    def fx_cfg_bypassed():
        return fx_cfg_runtime["bypass"]

    def fx_cfg_param(key):
        return _fxc_params[key]

    def fx_cfg_params():
        return list(_fxc_params.values())

    def fx_cfg_groups():
        """[(группа, {title, status})] в порядке регистрации параметров."""
        order = python_list()
        for p in _fxc_params.values():
            if p.group not in order:
                order.append(p.group)
        return [(g, _fxc_groups[g]) for g in order]

    def fx_cfg_saved(key):
        return _fxc_saved[key]

    def fx_cfg_dirty_keys():
        return [k for k in _fxc_params if _fxc_values[k] != _fxc_saved[k]]

    def fx_cfg_revert():
        keys = fx_cfg_dirty_keys()
        for k in keys:
            _fxc_values[k] = _fxc_saved[k]
        return len(keys)

    def fx_cfg_foreign():
        """Ключи файла без параметра в коде: запись файла их сохраняет."""
        return [(k, v) for k, v in _fxc_file.items() if k not in _fxc_params]

    def fx_cfg_issues():
        return list(fx_cfg_warnings) + ["%s: ключ не используется кодом" % k for k, _v in fx_cfg_foreign()]

    def fx_cfg_reload():
        """Перечитывает файл; при ошибке разбора или чтения значения не меняются."""
        parsed = _fxc_read_file()
        _fxc_file.clear()
        _fxc_file.update(parsed)
        del fx_cfg_warnings[:]
        for key, param in _fxc_params.items():
            value = _fxc_resolve(param)
            _fxc_values[key] = value
            _fxc_saved[key] = value

    def fx_cfg_commit(text):
        """Текущие значения записаны в основной файл: он становится базой."""
        _fxc_file.clear()
        _fxc_file.update(fx_cfg_parse(text))
        _fxc_saved.update(_fxc_values)
        del fx_cfg_warnings[:]

    ## Запись файла тюнером не должна перезапускать игру при включённом autoreload.
    config.autoreload_blacklist.append(FX_CONFIG_FILE)

    ## Битый или недоступный файл в релизе не мешает игре: остаются дефолты кода.
    try:
        _fxc_file.update(_fxc_read_file())
    except Exception:
        if config.developer:
            raise
