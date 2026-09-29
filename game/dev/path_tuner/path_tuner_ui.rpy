## PATH TUNER · интерфейс (dev-only)
## Логика — в path_tuner.rpy; строки намеренно не локализуются.

init -20 python:

    def path_copy(which="atl"):
        text = path_show_text() if which == "show" else path_atl_text()
        if not text:
            path_model.status = "нужны минимум две точки"
            return
        try:
            CopyToClipboard(text)()
            path_model.status = "в буфере: " + ("show-блок" if which == "show" else "ATL-строки")
        except Exception:
            path_model.status = "буфер обмена недоступен"

    def path_flip_side():
        path_model.side = "right" if path_model.side == "left" else "left"

    def path_toggle_panel():
        path_model.collapsed = not path_model.collapsed

    def path_head_dd(st, at):
        return Text(path_head_text(), style="path_head"), 0.25

    def path_mini_dd(st, at):
        m = path_model
        body = "%d точек · %s с · %s" % (len(m.points), _pt_num(m.duration), m.warper)
        return Text("PATH TUNER · " + body + "   {size=13}{color=#888}H — панель{/color}{/size}",
                    style="path_head"), (0.0 if m.dragging else 0.15)


screen path_tuner():

    modal True
    zorder 1000

    on "show" action Function(path_open)

    ## Mouse-слой пропускает клики по площади панели кнопкам.
    python:
        _path_pw = 620
        _path_ph = min(980, config.screen_height - 20)
        _path_px = 0 if path_model.side == "left" else (config.screen_width - _path_pw)
        path_model.panel_rect = (0, 0, 0, 0) if path_model.collapsed else (_path_px, 0, _path_pw, _path_ph)

    ## Ren'Py рисует детей вперёд, а события раздаёт назад: порядок важен.
    add path_draw

    if path_model.collapsed:
        frame:
            style "path_panel"
            align (0.5, 0.0)
            add DynamicDisplayable(path_mini_dd)
    else:
        use path_panel(_path_px, _path_pw, _path_ph)

    add path_grab

    key "anyrepeat_noshift_K_LEFT" action Function(path_nudge, -1, 0)
    key "anyrepeat_noshift_K_RIGHT" action Function(path_nudge, 1, 0)
    key "anyrepeat_noshift_K_UP" action Function(path_nudge, 0, -1)
    key "anyrepeat_noshift_K_DOWN" action Function(path_nudge, 0, 1)

    key "anyrepeat_shift_K_LEFT" action Function(path_nudge, -1, 0, True)
    key "anyrepeat_shift_K_RIGHT" action Function(path_nudge, 1, 0, True)
    key "anyrepeat_shift_K_UP" action Function(path_nudge, 0, -1, True)
    key "anyrepeat_shift_K_DOWN" action Function(path_nudge, 0, 1, True)

    key "K_DELETE" action Function(path_delete_sel)
    key "K_SPACE" action Function(path_toggle_play)

    key "noshift_K_TAB" action Function(path_cycle_anchor, 1)
    key "shift_K_TAB" action Function(path_cycle_anchor, -1)

    key "anyrepeat_ctrl_noshift_K_z" action Function(path_undo)
    key "anyrepeat_ctrl_shift_K_z" action Function(path_redo)
    key "anyrepeat_ctrl_K_y" action Function(path_redo)
    key "anyrepeat_meta_noshift_K_z" action Function(path_undo)
    key "anyrepeat_meta_shift_K_z" action Function(path_redo)

    key "ctrl_noshift_K_c" action Function(path_copy, "atl")
    key "meta_noshift_K_c" action Function(path_copy, "atl")
    key "ctrl_shift_K_c" action Function(path_copy, "show")
    key "meta_shift_K_c" action Function(path_copy, "show")

    key "noshift_K_h" action Function(path_toggle_panel)

    key PATH_HOTKEY action Hide("path_tuner")
    key "game_menu" action Hide("path_tuner")


screen path_panel(px, pw, ph):

    frame:
        style "path_panel"
        xpos px
        ypos 0
        xsize pw
        ysize ph

        vbox:
            spacing 6

            hbox:
                spacing 8
                text "PATH TUNER" style "path_title"
                textbutton ("вправо" if path_model.side == "left" else "влево"):
                    style "path_button"
                    action Function(path_flip_side)
                textbutton "свернуть" style "path_button" action Function(path_toggle_panel)
                textbutton "закрыть" style "path_button" action Hide("path_tuner")

            add DynamicDisplayable(path_head_dd)

            frame:
                style "path_card"
                add DynamicDisplayable(path_info_dd)

            hbox:
                spacing 6
                textbutton ("пауза" if path_model.playing else "играть"):
                    style "path_button"
                    action Function(path_toggle_play)
                ## Во время проигрывания скраб только показывает t.
                bar:
                    value (StaticValue(path_model.scrub, 1.0) if path_model.playing
                        else FieldValue(path_model, "scrub", range=1.0, step=0.01))
                    style "path_scrub"
                    yalign 0.5

            hbox:
                spacing 6
                text "длительность" style "path_caption" yalign 0.5
                textbutton "−0.5" style "path_button" action Function(path_set_duration, -0.5)
                textbutton "−0.1" style "path_button" action Function(path_set_duration, -0.1)
                text _pt_num(path_model.duration) style "path_value" yalign 0.5
                textbutton "+0.1" style "path_button" action Function(path_set_duration, 0.1)
                textbutton "+0.5" style "path_button" action Function(path_set_duration, 0.5)

            hbox:
                spacing 6
                text "warper" style "path_caption" yalign 0.5
                textbutton "◀" style "path_button" action Function(path_cycle_warper, -1)
                text path_model.warper style "path_value" yalign 0.5 min_width 180
                textbutton "▶" style "path_button" action Function(path_cycle_warper, 1)

            hbox:
                spacing 6
                text "поворот" style "path_caption" yalign 0.5
                textbutton PATH_ROT_TITLES[path_model.rot_mode]:
                    style "path_button"
                    action Function(path_cycle_rot_mode)
                if path_model.rot_mode == "fixed":
                    text ("%s → %s" % (_pt_num(path_model.rot_from), _pt_num(path_model.rot_to))) style "path_value" yalign 0.5
                elif path_model.rot_mode == "tangent":
                    textbutton "−5" style "path_button" action Function(path_adjust, "rot_offset", -5.0)
                    text ("офсет %s°" % _pt_num(path_model.rot_offset)) style "path_value" yalign 0.5
                    textbutton "+5" style "path_button" action Function(path_adjust, "rot_offset", 5.0)
            if path_model.rot_mode == "fixed":
                hbox:
                    spacing 6
                    textbutton "старт −5" style "path_button" action Function(path_adjust, "rot_from", -5.0)
                    textbutton "старт +5" style "path_button" action Function(path_adjust, "rot_from", 5.0)
                    textbutton "конец −5" style "path_button" action Function(path_adjust, "rot_to", -5.0)
                    textbutton "конец +5" style "path_button" action Function(path_adjust, "rot_to", 5.0)

            hbox:
                spacing 6
                textbutton "Копировать ATL" style "path_button" action Function(path_copy, "atl")
                textbutton "Копировать show" style "path_button" action Function(path_copy, "show")
            hbox:
                spacing 6
                textbutton "Отменить":
                    style "path_button"
                    action Function(path_undo)
                    sensitive (len(path_model.undo) > 0)
                textbutton "Вернуть":
                    style "path_button"
                    action Function(path_redo)
                    sensitive (len(path_model.redo) > 0)
                textbutton "Удалить точку":
                    style "path_button"
                    action Function(path_delete_sel)
                    sensitive (path_model.sel is not None and path_model.sel[0] == "p")
                textbutton "Ручки авто" style "path_button" action Function(path_reset_handles)
                textbutton "Очистить" style "path_button" action Function(path_clear)

            null height 4

            text "ПРИЗРАК: СПРАЙТ СО СЦЕНЫ" style "path_caption"
            $ _path_rows = pt_showing()
            hbox:
                spacing 4
                viewport:
                    id "path_vp"
                    xsize (pw - 46)
                    ysize max(120, ph - 700)
                    mousewheel True
                    draggable True
                    vbox:
                        spacing 1
                        textbutton "плейсхолдер (110×110)":
                            style "path_item"
                            selected (path_model.sprite is None)
                            action Function(path_pick_sprite, None)
                        for _path_name in _path_rows:
                            textbutton _path_name:
                                style "path_item"
                                selected (_path_name == path_model.sprite)
                                action Function(path_pick_sprite, _path_name)
                vbar:
                    value YScrollValue("path_vp")
                    style "path_vbar"
                    ysize max(120, ph - 700)

            null height 4

            text "клик по сцене — добавить точку · тащить точку/ручку мышью · стрелки ±[PATH_STEP] (Shift ±[PATH_STEP_BIG])\nDel — удалить точку · Tab — anchor призрака · Space — пауза (скраб — баром на паузе)\nКрайние ручки задают касательные; внутри пути Catmull-Rom считает их сам\nCtrl+Z — отменить · Ctrl+C — ATL · Ctrl+Shift+C — show-блок · H — панель · F6/Esc — закрыть" style "path_hint"


## zorder выше модальных экранов игры — иначе хоткей глохнет внутри интерактивов.

screen path_hotkey_controller():
    zorder 1100
    key PATH_HOTKEY action ToggleScreen("path_tuner")

init python:
    if config.developer:
        config.always_shown_screens.append("path_hotkey_controller")


style path_panel is frame:
    background "#000000d8"
    padding (16, 14)

style path_card is frame:
    background "#ffffff10"
    padding (10, 8)
    xfill True

## Шрифт движка, а не игровой gui.text_font: служебная панель читается одинаково
## при любом оформлении игры.
style path_text is text:
    font "DejaVuSans.ttf"

style path_title is path_text:
    size 22
    bold True
    color "#ffffff"

style path_head is path_text:
    size 15
    color "#cccccc"

style path_info is path_text:
    size 17
    color "#ffffff"
    line_spacing 2

style path_caption is path_text:
    size 13
    color "#888888"

style path_value is path_text:
    size 16
    color "#9fffcf"

style path_hint is path_text:
    size 13
    color "#999999"
    line_spacing 2

style path_button is button:
    padding (10, 5)
    background "#ffffff18"
    hover_background "#ffffff33"
    insensitive_background "#ffffff08"

style path_button_text is button_text:
    font "DejaVuSans.ttf"
    size 15
    color "#dddddd"
    hover_color "#ffffff"
    insensitive_color "#666666"

style path_scrub is bar:
    xsize 420
    ysize 22
    left_bar Solid("#4db8ff88")
    right_bar Solid("#ffffff14")
    thumb None
    thumb_offset 0
    thumb_shadow None

style path_vbar is vbar:
    xsize 6
    top_bar Solid("#ffffff44")
    bottom_bar Solid("#ffffff14")
    thumb None
    thumb_shadow None
    thumb_offset 0

style path_item is button:
    padding (5, 2)
    background None
    hover_background "#ffffff20"
    selected_background "#4db8ff30"

style path_item_text is button_text:
    font "DejaVuSans.ttf"
    size 14
    color "#bbbbbb"
    hover_color "#ffffff"
    selected_color "#9fdcff"
