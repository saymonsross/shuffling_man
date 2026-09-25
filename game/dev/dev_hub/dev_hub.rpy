## DEV HUB (dev-only): точка входа во все dev-инструменты, шпаргалка клавиш и статус.
## Строки намеренно не локализуются. Панель на слое top и не modal для клавиатуры:
## встроенный keymap работает; мышь забирает затемнение, клик мимо панели её закрывает.

define -30 DEV_HUB_HOTKEY = "K_F12"

## screen — показать поверх игры, menu — открыть как игровое меню,
## label — прыгнуть (только внутри игры, не из меню); hotkey — имя константы с keysym.
define -30 DEV_HUB_TOOLS = (
    {"title": "Position Tuner", "hotkey": "PT_HOTKEY", "screen": "position_tuner",
        "about": "позиция, якорь и угол спрайтов → ATL в буфер"},
    {"title": "FX Tuner", "hotkey": "FXT_HOTKEY", "screen": "fx_tuner",
        "about": "эффекты вживую → game/fx_config.yaml"},
    {"title": "Сцены", "menu": "dev_scene_navigator",
        "about": "запуск любой сцены с чистым состоянием"},
    {"title": "Заморозить кадр", "label": "dev_hold",
        "about": "сценарий стоит, картинка остаётся — удобно для F9/F10"},
    {"title": "Песочница позиций", "label": "dev_position_sandbox",
        "about": "сцена без камеры: призрак тюнера совпадает пиксель в пиксель"},
)

## Имена из config.keymap: подписи клавиш читаются из актуальной раскладки.
define -30 DEV_HUB_BUILTINS = (
    ("Консоль", "console"),
    ("Dev-меню Ren'Py", "developer"),
    ("Перезагрузка скриптов", "reload_game"),
    ("Инспектор стилей", "inspector"),
    ("Interactive Director", "director"),
    ("Производительность", "performance"),
    ("Лог загрузки картинок", "image_load_log"),
    ("Открыть в редакторе", "launch_editor"),
    ("Прогресс игры", "progress_screen"),
    ("Скриншот", "screenshot"),
)

define -30 DEV_HUB_WATCH = ("PSY_HP", "fx_posterize_strength")


init -5 python:

    ## python_dict — вне rollback и сейвов.
    _dev_hub_state = python_dict(label=None)

    def _dev_hub_on_label(name, abnormal):
        _dev_hub_state["label"] = name

    def _dev_hub_quote(text):
        return text.replace("{", "{{")

    _DEV_HUB_KEY_NAMES = python_dict(
        ESCAPE="Esc", RETURN="Enter", SPACE="Space", PAGEUP="PgUp", PAGEDOWN="PgDn",
        PERIOD=".", SLASH="/", BACKSPACE="Backspace",
    )

    def dev_hub_key_label(keysym):
        """shift_K_o → Shift+O; мышь и геймпад не показываются."""
        if keysym.startswith(("mouse", "pad_", "K_AC")):
            return None
        mods = python_list()
        rest = keysym
        while "_" in rest and not rest.startswith("K_"):
            mod, rest = rest.split("_", 1)
            if mod in ("noshift", "anyrepeat", "repeat", "anymod", "osctrl"):
                continue
            mods.append({"meta": "Cmd", "ctrl": "Ctrl", "alt": "Alt", "shift": "Shift"}.get(mod, mod.title()))
        if rest.startswith("K_"):
            rest = rest[2:]
        rest = _DEV_HUB_KEY_NAMES.get(rest, rest.upper() if len(rest) == 1 else rest)
        return "+".join(mods + [rest])

    def dev_hub_keys(name):
        labels = python_list()
        for k in config.keymap.get(name, ()):
            label = dev_hub_key_label(k)
            if label and label not in labels:
                labels.append(label)
        labels.sort(key=lambda s: s.count("+"))
        return " / ".join(labels[:2]) or "—"

    def dev_hub_tool_keys(entry):
        keysym = getattr(store, entry.get("hotkey", ""), None)
        return (dev_hub_key_label(keysym) or "") if keysym else ""

    def dev_hub_in_game():
        return not main_menu and not renpy.context()._menu

    def dev_hub_tool_ok(entry):
        if "screen" in entry:
            return renpy.has_screen(entry["screen"])
        if "menu" in entry:
            return renpy.has_screen(entry["menu"])
        return renpy.has_label(entry["label"]) and dev_hub_in_game()

    def dev_hub_tool_action(entry):
        if "screen" in entry:
            return [Hide("dev_hub"), Show(entry["screen"])]
        if "menu" in entry:
            return [Hide("dev_hub"), ShowMenu(entry["menu"])]
        return [Hide("dev_hub"), Jump(entry["label"])]

    def dev_hub_builtin_action(name):
        """None — действие доступно только по клавише."""
        run = {
            "console": _console.enter,
            "developer": _developer,
            "reload_game": _reload_game,
            "launch_editor": _launch_editor,
            "progress_screen": _progress_screen,
        }.get(name)
        if run is not None:
            return [Hide("dev_hub"), Function(run)]
        if name == "director":
            return [Hide("dev_hub"), director.Start()]
        if name == "performance":
            return [Hide("dev_hub"), ToggleScreen("_performance")]
        return None

    def dev_hub_status_text():
        lines = python_list()
        where = renpy.get_filename_line()
        lines.append("{color=#aaa}строка{/color} %s:%s   {color=#aaa}лейбл{/color} %s"
            % (_dev_hub_quote(where[0]), where[1], _dev_hub_quote(_dev_hub_state["label"] or "—")))
        watch = python_list()
        for name in DEV_HUB_WATCH:
            v = getattr(store, name, None)
            if isinstance(v, float):
                v = "%.2f" % v
            watch.append("{color=#aaa}%s{/color} %s" % (name, "—" if v is None else _dev_hub_quote(str(v))))
        lines.append("   ".join(watch))
        dirty = len(fx_cfg_dirty_keys())
        lines.append("{color=#aaa}fx_config.yaml{/color} %s   {color=#aaa}Ren'Py{/color} %s · %s"
            % ("{color=#ffd166}не сохранено: %d{/color}" % dirty if dirty else "как в файле",
                renpy.version_only, renpy.get_renderer_info().get("renderer", "?")))
        return "\n".join(lines)

    ## substitute=False: значения переменных и имена лейблов — данные, не шаблон.
    def dev_hub_status_dd(st, at):
        return Text(dev_hub_status_text(), style="dev_hub_status", substitute=False), 0.25

    if config.developer:
        config.label_callbacks.append(_dev_hub_on_label)


screen dev_hub():

    layer "top"

    ## Затемнение гасит клики по игре и закрывает хаб по клику мимо панели.
    button:
        style "dev_hub_dim"
        action Hide("dev_hub")

    frame:
        style "dev_hub_panel"
        modal True
        align (0.5, 0.5)

        vbox:
            spacing 8

            hbox:
                spacing 12
                text "DEV HUB" style "dev_hub_title"
                text (dev_hub_key_label(DEV_HUB_HOTKEY) + " — закрыть") style "dev_hub_caption" yalign 0.5

            frame:
                style "dev_hub_card"
                add DynamicDisplayable(dev_hub_status_dd)

            text "ИНСТРУМЕНТЫ ПРОЕКТА" style "dev_hub_caption"
            for entry in DEV_HUB_TOOLS:
                button:
                    style "dev_hub_item"
                    sensitive dev_hub_tool_ok(entry)
                    action dev_hub_tool_action(entry)
                    hbox:
                        spacing 12
                        text dev_hub_tool_keys(entry) style "dev_hub_key"
                        text entry["title"] style "dev_hub_name"
                        text entry["about"] style "dev_hub_about"

            null height 4
            text "ВСТРОЕННОЕ В REN'PY" style "dev_hub_caption"
            $ builtin_rows = (len(DEV_HUB_BUILTINS) + 1) // 2
            grid 2 builtin_rows:
                transpose True
                spacing 2
                for title, name in DEV_HUB_BUILTINS:
                    $ builtin_action = dev_hub_builtin_action(name)
                    button:
                        style "dev_hub_item"
                        xsize 520
                        action builtin_action
                        sensitive (builtin_action is not None)
                        hbox:
                            spacing 12
                            text dev_hub_keys(name) style "dev_hub_key"
                            text title style "dev_hub_name"
                if len(DEV_HUB_BUILTINS) % 2:
                    null

            text "Серые пункты: инструмент недоступен здесь (лейблы — только внутри игры) или работает только по клавише." style "dev_hub_caption"

    key "game_menu" action Hide("dev_hub")


screen dev_hub_hotkey_controller():
    zorder 1100
    key DEV_HUB_HOTKEY action ToggleScreen("dev_hub")

init python:
    if config.developer:
        config.always_shown_screens.append("dev_hub_hotkey_controller")


style dev_hub_dim is empty:
    background "#00000088"
    xfill True
    yfill True

style dev_hub_panel is frame:
    background "#0b0b0bf0"
    padding (24, 20)
    xsize 1100

style dev_hub_card is frame:
    background "#ffffff10"
    padding (12, 8)
    xfill True

## Шрифт движка, а не игровой gui.text_font: служебная панель читается одинаково
## при любом оформлении игры.
style dev_hub_text is text:
    font "DejaVuSans.ttf"

style dev_hub_title is dev_hub_text:
    size 26
    bold True
    color "#ffffff"

style dev_hub_caption is dev_hub_text:
    size 13
    color "#888888"

style dev_hub_status is dev_hub_text:
    size 15
    color "#dddddd"
    line_spacing 3

style dev_hub_item is button:
    padding (8, 5)
    background "#ffffff0c"
    hover_background "#ffffff26"
    insensitive_background None
    xfill True

style dev_hub_key is dev_hub_text:
    size 15
    bold True
    color "#9fffcf"
    min_width 200
    insensitive_color "#4a6a5a"

style dev_hub_name is dev_hub_text:
    size 16
    color "#eeeeee"
    min_width 220
    insensitive_color "#666666"

style dev_hub_about is dev_hub_text:
    size 13
    color "#8a8a8a"
    yalign 0.5
    insensitive_color "#555555"
