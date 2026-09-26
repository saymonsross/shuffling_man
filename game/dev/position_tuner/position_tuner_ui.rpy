## POSITION TUNER · интерфейс (dev-only)
## Логика — в position_tuner.rpy; строки намеренно не локализуются.

init -20 python:

    def pt_copy(which="atl"):
        text = pt_call_text() if which == "call" else pt_atl_text()
        if not text:
            return
        try:
            CopyToClipboard(text)()
            pt_model.status = "в буфере: " + text.replace("\n", " · ")
        except Exception:
            pt_model.status = "буфер обмена недоступен"

    def pt_flip_side():
        pt_model.side = "right" if pt_model.side == "left" else "left"

    def pt_toggle_panel():
        pt_model.collapsed = not pt_model.collapsed

    def pt_head_dd(st, at):
        return Text(pt_head_text(), style="pt_head"), 0.25

    def pt_mini_dd(st, at):
        t = pt_model.target()
        body = "%s  pos %s  rotate %s°" % (t.name, _pt_pair(t.pos), _pt_num(t.rotate)) if t \
               else "на сцене нет спрайтов"
        return Text("POSITION TUNER · " + body + "   {size=13}{color=#888}H — панель{/color}{/size}",
                    style="pt_head"), (0.0 if pt_model.dragging else 0.15)

    def pt_rows():
        rows = python_list()
        for name in sorted(pt_model.targets):
            t = pt_model.targets[name]
            mark = "● " if t.dirty else ""
            info = "pos %s" % _pt_pair(t.pos)
            if t.rotate:
                info += "  %s°" % _pt_num(t.rotate)
            rows.append((name, mark + name, info))
        return rows


screen position_tuner():

    modal True
    zorder 1000

    on "show" action Function(pt_open)

    ## Mouse-layer использует геометрию панели, чтобы пропускать её клики.
    python:
        _pt_pw = 620
        _pt_ph = min(1000, config.screen_height - 20)
        _pt_px = 0 if pt_model.side == "left" else (config.screen_width - _pt_pw)
        pt_model.panel_rect = (0, 0, 0, 0) if pt_model.collapsed else (_pt_px, 0, _pt_pw, _pt_ph)

    ## Ren'Py рисует детей вперёд, а события раздаёт назад: порядок здесь важен.
    add pt_ghost

    if pt_model.collapsed:
        frame:
            style "pt_panel"
            align (0.5, 0.0)
            add DynamicDisplayable(pt_mini_dd)
    else:
        use pt_panel(_pt_px, _pt_pw, _pt_ph)

    add pt_grab

    ## noshift/shift разделены, чтобы модификаторы не давали двойной action.

    key "anyrepeat_noshift_K_LEFT" action Function(pt_nudge, -1, 0)
    key "anyrepeat_noshift_K_RIGHT" action Function(pt_nudge, 1, 0)
    key "anyrepeat_noshift_K_UP" action Function(pt_nudge, 0, -1)
    key "anyrepeat_noshift_K_DOWN" action Function(pt_nudge, 0, 1)

    key "anyrepeat_shift_K_LEFT" action Function(pt_nudge, -1, 0, True)
    key "anyrepeat_shift_K_RIGHT" action Function(pt_nudge, 1, 0, True)
    key "anyrepeat_shift_K_UP" action Function(pt_nudge, 0, -1, True)
    key "anyrepeat_shift_K_DOWN" action Function(pt_nudge, 0, 1, True)

    key "noshift_K_TAB" action Function(pt_model.cycle_anchor, 1)
    key "shift_K_TAB" action Function(pt_model.cycle_anchor, -1)

    key "anyrepeat_noshift_K_LEFTBRACKET" action Function(pt_turn, -1)
    key "anyrepeat_noshift_K_RIGHTBRACKET" action Function(pt_turn, 1)
    key "anyrepeat_shift_K_LEFTBRACKET" action Function(pt_turn, -1, True)
    key "anyrepeat_shift_K_RIGHTBRACKET" action Function(pt_turn, 1, True)

    key "anyrepeat_ctrl_noshift_K_z" action Function(pt_undo)
    key "anyrepeat_ctrl_shift_K_z" action Function(pt_redo)
    key "anyrepeat_ctrl_K_y" action Function(pt_redo)
    key "anyrepeat_meta_noshift_K_z" action Function(pt_undo)
    key "anyrepeat_meta_shift_K_z" action Function(pt_redo)

    key "ctrl_K_s" action Function(pt_write)
    key "meta_K_s" action Function(pt_write)
    key "ctrl_K_c" action Function(pt_copy, "atl")
    key "meta_K_c" action Function(pt_copy, "atl")

    key "noshift_K_h" action Function(pt_toggle_panel)
    key "noshift_K_r" action Function(pt_reset)

    key PT_HOTKEY action Hide("position_tuner")
    key "game_menu" action Hide("position_tuner")


screen pt_panel(px, pw, ph):

    frame:
        style "pt_panel"
        xpos px
        ypos 0
        xsize pw
        ysize ph

        vbox:
            spacing 6

            hbox:
                spacing 8
                text "POSITION TUNER" style "pt_title"
                textbutton ("вправо" if pt_model.side == "left" else "влево"):
                    style "pt_button"
                    action Function(pt_flip_side)
                textbutton "свернуть" style "pt_button" action Function(pt_toggle_panel)
                textbutton "закрыть" style "pt_button" action Hide("position_tuner")

            add DynamicDisplayable(pt_head_dd)

            null height 4

            frame:
                style "pt_card"
                add DynamicDisplayable(pt_info_dd)

            hbox:
                spacing 6
                textbutton "Записать в код":
                    style "pt_button"
                    action Function(pt_write)
                    sensitive (pt_dirty_count() > 0)
                textbutton "Копировать ATL" style "pt_button" action Function(pt_copy, "atl")
                textbutton "Копировать вызов" style "pt_button" action Function(pt_copy, "call")
            hbox:
                spacing 6
                textbutton "Отменить":
                    style "pt_button"
                    action Function(pt_undo)
                    sensitive (len(pt_model.undo) > 0)
                textbutton "Вернуть":
                    style "pt_button"
                    action Function(pt_redo)
                    sensitive (len(pt_model.redo) > 0)
                textbutton "Сбросить" style "pt_button" action Function(pt_reset)

            text "«Записать в код» (Ctrl+S) переписывает литералы в show ... at placed(...) — остальное только в буфер" style "pt_hint"

            null height 4

            text "СПРАЙТЫ НА ЭКРАНЕ" style "pt_caption"
            hbox:
                spacing 4
                viewport:
                    id "pt_vp"
                    xsize (pw - 46)
                    ysize (ph - 460)
                    mousewheel True
                    draggable True
                    vbox:
                        spacing 1
                        for name, label, info in pt_rows():
                            textbutton "[label]\n{size=11}{color=#7a7a7a}[info]{/color}{/size}":
                                style "pt_item"
                                selected (name == pt_model.name)
                                action Function(pt_pick, name)
                ## Solid не привязывает переносимый инструмент к gui/-ассетам.
                vbar:
                    value YScrollValue("pt_vp")
                    style "pt_vbar"
                    ysize (ph - 460)

            null height 4

            text "мышь — взять спрайт и тащить · стрелки ±[PT_STEP] · Shift+стрелки ±[PT_STEP_BIG] · Tab — точка привязки\n[[ и ]] — наклон ±[PT_STEP_ANGLE]° (с Shift ±[PT_STEP_ANGLE_BIG]°) · Ctrl+Z — отменить · Ctrl+S — записать в код · Ctrl+C — копировать\nR — вернуть значения сцены · H — свернуть панель · F9/Esc — закрыть" style "pt_hint"


## zorder выше модальных экранов игры — иначе хоткей глохнет внутри интерактивов.

screen pt_hotkey_controller():
    zorder 1100
    key PT_HOTKEY action ToggleScreen("position_tuner")

init python:
    if config.developer:
        config.always_shown_screens.append("pt_hotkey_controller")


style pt_panel is frame:
    background "#000000d8"
    padding (16, 14)

style pt_card is frame:
    background "#ffffff10"
    padding (10, 8)
    xfill True

## Шрифт движка, а не игровой gui.text_font: служебная панель читается одинаково
## при любом оформлении игры.
style pt_text is text:
    font "DejaVuSans.ttf"

style pt_title is pt_text:
    size 22
    bold True
    color "#ffffff"

style pt_head is pt_text:
    size 15
    color "#cccccc"

style pt_info is pt_text:
    size 17
    color "#ffffff"
    line_spacing 2

style pt_caption is pt_text:
    size 13
    color "#888888"

style pt_hint is pt_text:
    size 13
    color "#999999"
    line_spacing 2

style pt_button is button:
    padding (10, 5)
    background "#ffffff18"
    hover_background "#ffffff33"
    insensitive_background "#ffffff08"

style pt_button_text is button_text:
    font "DejaVuSans.ttf"
    size 15
    color "#dddddd"
    hover_color "#ffffff"
    insensitive_color "#666666"

style pt_vbar is vbar:
    xsize 6
    top_bar Solid("#ffffff44")
    bottom_bar Solid("#ffffff14")
    thumb None
    thumb_shadow None
    thumb_offset 0

style pt_item is button:
    padding (5, 2)
    background None
    hover_background "#ffffff20"
    selected_background "#00ff8830"

style pt_item_text is button_text:
    font "DejaVuSans.ttf"
    size 14
    color "#bbbbbb"
    hover_color "#ffffff"
    selected_color "#9fffcf"
