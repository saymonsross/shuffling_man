## FONT PICKER (dev-only): ←/→ перебирают шрифты game/fonts/ у того, что сейчас на экране
## (sm_font_preview_text / sm_font_preview_style), R — шрифт из кода, Ctrl+S — вписать
## выбор строкой font в стиль в исходнике. Строки намеренно не локализуются.

define -30 FP_HOTKEY = "K_F8"
define -30 FP_APPLY_KEY = "ctrl_K_s"

init -5 python:

    def dev_font_list():
        return sorted(f for f in renpy.list_files()
            if f.startswith("fonts/") and f.lower().endswith((".ttf", ".otf")))

    def dev_font_step(delta):
        fonts = dev_font_list()
        if not fonts:
            return
        cur = _sm_font_override["font"]
        i = fonts.index(cur) if cur in fonts else (-1 if delta > 0 else 0)
        _sm_font_override["font"] = fonts[(i + delta) % len(fonts)]
        _fp_live()

    ## Исходные шрифты стилей, подменённых вживую: «из кода» возвращает их.
    _fp_original = python_dict()

    def dev_font_targets():
        import time
        now = time.time()
        return sorted(n for n, t in _sm_font_override["seen"].items() if now - t < 1.0)

    def _fp_live():
        """Шрифт стилей на экране — сразу, без правки исходника."""
        font = _sm_font_override["font"]
        for name in dev_font_targets() if font else ():
            st = getattr(style, name)
            if name not in _fp_original:
                _fp_original[name] = st.font
            st.font = font
        if not font:
            for name, orig in _fp_original.items():
                getattr(style, name).font = orig
            _fp_original.clear()
        renpy.style.rebuild()
        renpy.restart_interaction()

    import os as _fp_os
    import re as _fp_re

    ## python_dict — строка статуса панели, вне rollback.
    _fp_state = python_dict(status="")

    def _fp_write_style(name, font):
        """Вписывает font в блок style <name>: первого .rpy, где он объявлен."""
        head = _fp_re.compile(r"^style %s(\s+is\s+\w+)?\s*:\s*$" % _fp_re.escape(name))
        for root, dirs, files in _fp_os.walk(config.gamedir):
            if "tl" in dirs and root == config.gamedir:
                dirs.remove("tl")
            for fn in files:
                if not fn.endswith(".rpy"):
                    continue
                path = _fp_os.path.join(root, fn)
                with open(path, encoding="utf-8") as f:
                    lines = f.read().splitlines()
                for i, line in enumerate(lines):
                    if not head.match(line):
                        continue
                    new = '    font "%s"' % font
                    ## Своя строка font в блоке стиля заменяется, иначе вставляется первой.
                    j = i + 1
                    while j < len(lines) and (lines[j].startswith("    ") or not lines[j].strip()):
                        if _fp_re.match(r"^    font\s", lines[j]):
                            lines[j] = new
                            break
                        j += 1
                    else:
                        lines.insert(i + 1, new)
                    with open(path, "w", encoding="utf-8", newline="") as f:
                        f.write("\n".join(lines) + "\n")
                    return _fp_os.path.relpath(path, config.gamedir).replace("\\", "/")
        return None

    def dev_font_apply():
        font = _sm_font_override["font"]
        styles = dev_font_targets()
        if not font:
            _fp_state["status"] = "шрифт не выбран — нечего применять"
        elif not styles:
            _fp_state["status"] = "на экране нет текста со стилем — некуда писать"
        else:
            done = python_list()
            for name in styles:
                where = _fp_write_style(name, font)
                done.append("%s → %s" % (name, where) if where else "%s: стиль не найден" % name)
            _fp_state["status"] = "записано: " + "; ".join(done) + " · Shift+R — перечитать"
        renpy.restart_interaction()

    def dev_font_reset():
        _sm_font_override["font"] = None
        _fp_live()

    def dev_font_label():
        fonts = dev_font_list()
        cur = _sm_font_override["font"]
        if cur not in fonts:
            return "шрифт из кода · в fonts/ файлов: %d · на экране: %s" % (
                len(fonts), ", ".join(dev_font_targets()) or "—")
        return "%s   %d / %d" % (cur, fonts.index(cur) + 1, len(fonts))


screen dev_font_picker():

    layer "top"

    frame:
        style "dev_fp_panel"
        align (0.5, 0.0)

        hbox:
            spacing 14
            text "FONT PICKER" style "dev_fp_title"
            textbutton "←" style "dev_fp_button" text_style "dev_fp_button_text" action Function(dev_font_step, -1)
            text dev_font_label() style "dev_fp_text" substitute False yalign 0.5
            textbutton "→" style "dev_fp_button" text_style "dev_fp_button_text" action Function(dev_font_step, 1)
            textbutton "применить" style "dev_fp_button" text_style "dev_fp_button_text" action Function(dev_font_apply)
            textbutton "из кода" style "dev_fp_button" text_style "dev_fp_button_text" action Function(dev_font_reset)
            textbutton "закрыть" style "dev_fp_button" text_style "dev_fp_button_text" action Hide("dev_font_picker")

    if _fp_state["status"]:
        frame:
            style "dev_fp_panel"
            align (0.5, 0.0)
            yoffset 56
            text _fp_state["status"] style "dev_fp_text" substitute False

    key "anyrepeat_K_LEFT" action Function(dev_font_step, -1)
    key "anyrepeat_K_RIGHT" action Function(dev_font_step, 1)
    key "noshift_K_r" action Function(dev_font_reset)
    key FP_APPLY_KEY action Function(dev_font_apply)
    key "K_ESCAPE" action Hide("dev_font_picker")


## zorder выше модальных экранов игры — иначе хоткей глохнет внутри интерактивов.
screen dev_fp_hotkey_controller():
    zorder 1100
    key FP_HOTKEY action ToggleScreen("dev_font_picker")

init python:
    if config.developer:
        config.always_shown_screens.append("dev_fp_hotkey_controller")


style dev_fp_panel is frame:
    background "#000000e0"
    padding (16, 10)

## Шрифт движка: панель читается одинаково при любом примеряемом шрифте.
style dev_fp_text is text:
    font "DejaVuSans.ttf"
    size 18
    color "#dddddd"

style dev_fp_title is dev_fp_text:
    size 20
    bold True
    color "#ffffff"
    yalign 0.5

style dev_fp_button is button:
    background "#ffffff14"
    hover_background "#ffffff30"
    padding (10, 4)
    yalign 0.5

style dev_fp_button_text is dev_fp_text:
    hover_color "#ffffff"
