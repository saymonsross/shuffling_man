## FX TUNER · ядро (dev-only)
## Правит значения реестра fx_param (common/fx_config.rpy) вживую и пишет
## game/fx_config.yaml. Сейвы и rollback не затрагиваются.

define -30 FXT_HOTKEY = "K_F10"
## Не Ctrl+S: Ctrl — клавиша пропуска, движок ловит её раньше экранов.
define -30 FXT_SAVE_KEY = "K_F5"
define -30 FXT_BIG = 10

define -30 FXT_HEADER = (
    "# Сквозные параметры визуальных эффектов проекта.",
    "# Правка вживую: FX Tuner (F10 в dev-сборке) → «Сохранить».",
    "# Читается при запуске игры; число вне диапазона прижимается к границе,",
    "# значение чужого типа заменяется дефолтом из кода (fx_param).",
)


init -5 python:

    import os as _fxt_os
    import re as _fxt_re

    _FXT_PLAIN = _fxt_re.compile(r"^[A-Za-z_][A-Za-z0-9_.\-]*$")
    _FXT_RESERVED = ("true", "false", "yes", "no", "on", "off", "null")

    def _fxt_scalar(v):
        if v is None:
            return "null"
        if isinstance(v, bool):
            return "true" if v else "false"
        if isinstance(v, int):
            return str(v)
        if isinstance(v, float):
            return repr(v)
        if isinstance(v, (list, tuple)):
            return "[" + ", ".join(_fxt_scalar(i) for i in v) + "]"
        s = str(v)
        if _FXT_PLAIN.match(s) and s.lower() not in _FXT_RESERVED:
            return s
        s = s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n").replace("\t", "\\t")
        return '"' + s + '"'

    def _fxt_comment(p):
        if p.kind == "choice":
            extra = "" if p.doc else " | ".join(p.choices)
        elif p.lo is not None and p.hi is not None:
            extra = "%s..%s" % (_fxt_scalar(p.lo), _fxt_scalar(p.hi))
        else:
            extra = ""
        return " · ".join(i for i in (p.doc, extra) if i)

    def fx_cfg_dump():
        """Текст fx_config.yaml: параметры реестра с описаниями, затем чужие
        ключи файла — запись не теряет настройки удалённого или чужого кода."""
        top = python_list()
        groups = python_dict()
        titles = python_dict(fx_cfg_groups())
        for p in fx_cfg_params():
            groups.setdefault(p.group, python_list()).append((p.name, fx_cfg(p.key), _fxt_comment(p)))
        for key, value in fx_cfg_foreign():
            if "." not in key:
                top.append((key, value))
                continue
            group, name = key.split(".", 1)
            groups.setdefault(group, python_list()).append((name, value, "не используется кодом"))

        lines = python_list(FXT_HEADER)
        if top:
            lines.append("")
            lines.extend("%s: %s" % (k, _fxt_scalar(v)) for k, v in top)
        for group, rows in groups.items():
            title = titles[group]["title"] if group in titles else None
            lines.append("")
            lines.append(group + ":" + ("  # " + title if title and title != group else ""))
            body = ["  %s: %s" % (name, _fxt_scalar(v)) for name, v, _c in rows]
            width = max(len(b) for b in body)
            for b, (_n, _v, comment) in zip(body, rows):
                lines.append((b.ljust(width) + "  # " + comment) if comment else b)
        return "\n".join(lines) + "\n"

    def fx_cfg_path():
        return _fxt_os.path.join(config.gamedir, FX_CONFIG_FILE)

    def fx_cfg_save(path=None):
        """Атомарно пишет YAML; базой «сохранённого» становится только основной файл."""
        if not config.developer:
            raise FxConfigError("запись доступна только в dev-сборке")
        main = fx_cfg_path()
        path = path or main
        text = fx_cfg_dump()
        tmp = path + ".tmp"
        try:
            with open(tmp, "w", encoding="utf-8", newline="\n") as f:
                f.write(text)
            _fxt_os.replace(tmp, path)
        except OSError:
            if _fxt_os.path.exists(tmp):
                _fxt_os.remove(tmp)
            raise
        if _fxt_os.path.normcase(_fxt_os.path.abspath(path)) == _fxt_os.path.normcase(_fxt_os.path.abspath(main)):
            fx_cfg_commit(text)
        return path


init -5 python:

    class FXTModel(python_object):
        """python_object — состояние панели вне rollback и сейвов."""

        def __init__(self):
            self.key = None
            self.side = "right"
            self.collapsed = False
            self.status = ""

    fxt_model = FXTModel()

    def fxt_key_label(keysym):
        return keysym[2:] if keysym.startswith("K_") else keysym

    def fxt_quote(text):
        """Строка для Text(substitute=False): теги текста в ней не разбираются."""
        return text.replace("{", "{{")

    def fxt_open():
        if not config.developer:
            return
        fxt_model.status = ""
        keys = fxt_keys()
        if fxt_model.key not in keys:
            fxt_model.key = keys[0] if keys else None

    def fxt_keys():
        return [p.key for p in fx_cfg_params()]

    def fxt_group_keys(group):
        return [p.key for p in fx_cfg_params() if p.group == group]

    def fxt_select(key):
        fxt_model.key = key

    def fxt_move(delta):
        keys = fxt_keys()
        if not keys:
            return
        i = keys.index(fxt_model.key) if fxt_model.key in keys else -1
        fxt_model.key = keys[(i + delta) % len(keys)]

    def fxt_set(key, value):
        fxt_model.key = key
        fx_cfg_set(key, value)
        renpy.restart_interaction()

    def fxt_step(key, sign, big=False):
        p = fx_cfg_param(key)
        v = fx_cfg(key)
        if p.kind == "bool":
            v = not v
        elif p.kind == "choice":
            v = p.choices[(p.choices.index(v) + sign) % len(p.choices)]
        else:
            v = v + sign * p.step * (FXT_BIG if big else 1)
        fxt_set(key, v)

    def fxt_nudge(sign, big=False):
        if fxt_model.key in fxt_keys():
            fxt_step(fxt_model.key, sign, big)

    def fxt_reset(key=None):
        key = key or fxt_model.key
        if key in fxt_keys():
            fxt_set(key, fx_cfg_param(key).default)

    def fxt_revert():
        n = fx_cfg_revert()
        fxt_model.status = "откачено к файлу: %d" % n if n else "правок нет"

    def fxt_reload():
        try:
            fx_cfg_reload()
        except (FxConfigError, OSError) as e:
            fxt_model.status = "файл не перечитан: %s" % e
            return
        fxt_model.status = "перечитано из " + FX_CONFIG_FILE

    def fxt_save():
        try:
            fx_cfg_save()
        except (FxConfigError, OSError) as e:
            fxt_model.status = "не сохранено: %s" % e
            return
        fxt_model.status = "сохранено в " + FX_CONFIG_FILE

    def fxt_toggle(flag):
        fx_cfg_runtime[flag] = not fx_cfg_runtime[flag]

    def fxt_value_text(key):
        v = fx_cfg(key)
        if isinstance(v, bool):
            return "вкл" if v else "выкл"
        if isinstance(v, float):
            s = ("%.4f" % v).rstrip("0")
            return s + "0" if s.endswith(".") else s
        return str(v)

    def fxt_head_text():
        bits = python_list()
        n = len(fx_cfg_dirty_keys())
        bits.append("{color=#ffd166}● не сохранено: %d{/color}" % n if n
                    else "{color=#6c6}как в файле{/color}")
        if fx_cfg_runtime["bypass"]:
            bits.append("{color=#ff6b6b}A/B: эффекты выключены{/color}")
        if fx_cfg_runtime["preview"]:
            bits.append("{color=#7bd}превью: сцена игнорируется{/color}")
        if fxt_model.status:
            bits.append("{color=#9ab}%s{/color}" % fxt_quote(fxt_model.status))
        return "   ".join(bits)
