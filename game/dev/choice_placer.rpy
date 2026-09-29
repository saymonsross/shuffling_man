## CHOICE PLACER (dev-only): расстановка сценовых кнопок мышью, как dev_align_tool в TVARUK_HD.
## F7 — вкл/выкл (F5 занят сохранением FX Tuner). Пока включён, кнопки menu(screen="scene_choice") показаны рамками;
## отпустил рамку — pos=(x, y) пункта меню переписывается в .rpy, кнопка остаётся на новом
## месте до перезагрузки. Координаты — в кадре сцены: кнопка едет за камерой, как и раньше.
## Строки намеренно не локализуются.

define -30 CP_HOTKEY = "K_F7"

init python:

    import io as _cp_io
    import os as _cp_os
    import re as _cp_re

    _CP_POS_RE = _cp_re.compile(r"pos\s*=\s*\(\s*-?\d+\s*,\s*-?\d+\s*\)")

    _cp_state = python_dict(msg="")

    def _cp_source(where):
        path = _cp_os.path.join(config.basedir, where[0])
        if not _cp_os.path.exists(path):
            path = _cp_os.path.join(config.gamedir, where[0])
        return path

    def dev_cp_write(where, caption, pos):
        """Переписывает pos=(x, y) пункта caption в menu из where. Возвращает «файл:строка» или None."""
        path = _cp_source(where)
        if not _cp_os.path.exists(path):
            return None
        with _cp_io.open(path, encoding="utf-8", newline="") as f:
            lines = f.read().splitlines(True)
        needle = '"%s"' % caption
        start = max(where[1] - 1, 0)
        for i in range(start, min(start + 120, len(lines))):
            if needle not in lines[i]:
                continue
            ## Аргументы пункта могут переноситься на следующие строки до «):».
            for j in range(i, min(i + 6, len(lines))):
                if _CP_POS_RE.search(lines[j]):
                    lines[j] = _CP_POS_RE.sub("pos=(%d, %d)" % pos, lines[j], count=1)
                    with _cp_io.open(path, "w", encoding="utf-8", newline="") as f:
                        f.write("".join(lines))
                    return "%s:%d" % (where[0], j + 1)
                if lines[j].rstrip().endswith(":"):
                    break
            return None
        return None

    def dev_cp_dragged(where, caption, anchor, size, drags, drop):
        d = drags[0]
        pos = (int(round(d.x + anchor[0] * size[0])), int(round(d.y + anchor[1] * size[1])))
        _sm_choice_moved[(where, caption)] = pos
        written = dev_cp_write(where, caption, pos)
        if written:
            _cp_state["msg"] = "%s  pos=(%d, %d)  →  %s" % (caption, pos[0], pos[1], written)
        else:
            _cp_state["msg"] = "%s  pos=(%d, %d)  →  строка с pos=(…) не найдена, впиши руками" % (caption, pos[0], pos[1])
        renpy.restart_interaction()
        return None

    if config.developer:
        config.always_shown_screens.append("dev_cp_hotkey_controller")


## zorder выше модальных экранов игры — иначе хоткей глохнет внутри интерактивов.
screen dev_cp_hotkey_controller():
    zorder 1100
    key CP_HOTKEY action [SetDict(_cp_state, "msg", ""), ToggleScreen("dev_choice_placer")]

screen dev_choice_placer():
    zorder 1050
    frame:
        style "dev_cp_panel"
        align (0.5, 0.0)
        yoffset 8
        vbox:
            spacing 4
            text "CHOICE PLACER · тащи сценовые кнопки мышью · отпустил — pos пишется в .rpy · F7 — выкл" style "dev_cp_text"
            if not renpy.get_screen("scene_choice"):
                text "на экране нет сценовых кнопок — дойди до menu(screen=\"scene_choice\")" style "dev_cp_text" color "#ffcc44"
            if _cp_state["msg"]:
                text _cp_state["msg"] style "dev_cp_text" color "#ff8080" substitute False

## Рамка вместо кнопки: тот же прямоугольник, что у glow_button (pos, anchor, size).
screen dev_choice_drag(item, where):
    $ _cp_kw = sm_choice_kwargs(where, item)
    $ _cp_size = _cp_kw.get("size") or GLOW_BASE_SIZE
    $ _cp_pos = _cp_kw.get("pos", (0.5, 0.5))
    $ _cp_anchor = _cp_kw.get("anchor", (0.5, 0.5))
    $ _cp_rect = sm_rift_rect(_cp_pos, _cp_anchor, _cp_size)
    drag:
        draggable True
        droppable False
        drag_raise True
        pos (int(round(_cp_rect[0])), int(round(_cp_rect[1])))
        dragged renpy.partial(dev_cp_dragged, where, item.caption, _cp_anchor, _cp_size)
        fixed:
            xysize _cp_size
            add Solid("#b01e1e40")
            add gui_outline(_cp_size[0], _cp_size[1], color="#ff4040")
            vbox:
                align (0.5, 0.5)
                text item.caption style "dev_cp_text" xalign 0.5 substitute False
                text "pos=(%s, %s)" % _cp_pos style "dev_cp_text" xalign 0.5 color "#ffcc44" substitute False

style dev_cp_panel is frame:
    background "#000000e0"
    padding (16, 8)

style dev_cp_text is text:
    font "DejaVuSans.ttf"
    size 18
    color "#dddddd"
