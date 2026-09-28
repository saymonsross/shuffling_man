## FX TUNER · интерфейс (dev-only)
## Строки намеренно не локализуются. Панель живёт на слое top: постеризация
## с охватом screen её не задевает. Экран не modal: встроенный keymap
## (Shift+R, консоль) работает, игра под панелью идёт дальше.

init -5 python:

    class FxtValue(BarValue, FieldEquality):
        """Слайдер пишет через fx_cfg_set: тип и диапазон соблюдаются."""

        identity_fields = ()
        equality_fields = ("key",)

        def __init__(self, key):
            self.key = key

        def get_adjustment(self):
            p = fx_cfg_param(self.key)
            return ui.adjustment(range=p.hi - p.lo, value=fx_cfg(self.key) - p.lo,
                step=p.step, force_step=True, changed=self.changed)

        def changed(self, value):
            fxt_model.key = self.key
            fx_cfg_set(self.key, fx_cfg_param(self.key).lo + value)
            renpy.restart_interaction()

        def get_style(self):
            return "fxt_bar", "fxt_bar"

    def fxt_hint_text():
        return ("↑↓ — параметр · ←→ — шаг, с Shift ×%d · R — дефолт · B — A/B · P — превью\n"
                "%s — сохранить · %s/Esc — закрыть · клики мимо панели идут в игру"
                % (FXT_BIG, fxt_key_label(FXT_SAVE_KEY), fxt_key_label(FXT_HOTKEY)))

    ## substitute=False: в статусе бывают «[a, b]» и «[Errno 13]», а подстановка
    ## вычисляла бы их как выражения.
    def fxt_head_dd(st, at):
        return Text(fxt_head_text(), style="fxt_head", substitute=False), 0.2

    def fxt_status_dd(st, at, status):
        return Text(fxt_quote(status()), style="fxt_hint", substitute=False), 0.1


screen fx_tuner(groups=None, title="FX TUNER"):

    layer "top"

    on "show" action Function(fxt_open, groups)

    if fxt_model.collapsed:
        frame:
            style "fxt_panel"
            modal True
            align (0.5, 0.0)
            hbox:
                spacing 10
                text title style "fxt_title" substitute False
                add DynamicDisplayable(fxt_head_dd)
                textbutton "развернуть" style "fxt_button" action SetField(fxt_model, "collapsed", False)
                textbutton "закрыть" style "fxt_button" action Hide("fx_tuner")
    else:
        use fxt_panel(title)

    ## Клавиши панели перехватываются раньше игры; остальные проходят в игру.
    key "anyrepeat_noshift_K_UP" action Function(fxt_move, -1)
    key "anyrepeat_noshift_K_DOWN" action Function(fxt_move, 1)
    key "anyrepeat_noshift_K_LEFT" action Function(fxt_nudge, -1)
    key "anyrepeat_noshift_K_RIGHT" action Function(fxt_nudge, 1)
    key "anyrepeat_shift_K_LEFT" action Function(fxt_nudge, -1, True)
    key "anyrepeat_shift_K_RIGHT" action Function(fxt_nudge, 1, True)
    key "noshift_K_r" action Function(fxt_reset)
    key "noshift_K_b" action Function(fxt_toggle, "bypass")
    key "noshift_K_p" action Function(fxt_toggle, "preview")
    key FXT_SAVE_KEY action Function(fxt_save)
    ## Только Esc: правый клик остаётся игре (game_menu).
    key "K_ESCAPE" action Hide("fx_tuner")


screen fxt_panel(title="FX TUNER"):

    default pw = 600

    frame:
        style "fxt_panel"
        modal True
        xpos (0 if fxt_model.side == "left" else config.screen_width - pw)
        xsize pw
        ysize config.screen_height

        vbox:
            spacing 6

            hbox:
                spacing 8
                text title style "fxt_title" substitute False
                textbutton ("вправо" if fxt_model.side == "left" else "влево"):
                    style "fxt_button"
                    action SetField(fxt_model, "side", "right" if fxt_model.side == "left" else "left")
                textbutton "свернуть" style "fxt_button" action SetField(fxt_model, "collapsed", True)
                textbutton "закрыть" style "fxt_button" action Hide("fx_tuner")

            text FX_CONFIG_FILE style "fxt_caption" substitute False
            add DynamicDisplayable(fxt_head_dd)

            for issue in fx_cfg_issues():
                text fxt_quote(issue) style "fxt_warn" substitute False

            hbox:
                spacing 4
                viewport:
                    id "fxt_vp"
                    xsize (pw - 46)
                    ysize (config.screen_height - 330)
                    mousewheel True

                    vbox:
                        spacing 2
                        xsize (pw - 50)

                        for group, info in fx_cfg_groups():
                            if fxt_group_shown(group):
                                null height 6
                                text fxt_quote(info["title"]) style "fxt_group" substitute False
                                if info["status"]:
                                    add DynamicDisplayable(fxt_status_dd, info["status"])
                                for key in fxt_group_keys(group):
                                    use fxt_row(key)

                vbar:
                    value YScrollValue("fxt_vp")
                    style "fxt_vscroll"
                    ysize (config.screen_height - 330)

            hbox:
                spacing 6
                textbutton "Сохранить":
                    style "fxt_button"
                    action Function(fxt_save)
                    sensitive (len(fx_cfg_dirty_keys()) > 0)
                textbutton "Откатить к файлу":
                    style "fxt_button"
                    action Function(fxt_revert)
                    sensitive (len(fx_cfg_dirty_keys()) > 0)
                textbutton "Перечитать файл" style "fxt_button" action Function(fxt_reload)

            hbox:
                spacing 6
                textbutton "A/B: без эффектов":
                    style "fxt_button"
                    selected fx_cfg_runtime["bypass"]
                    action Function(fxt_toggle, "bypass")
                textbutton "Превью: игнорировать сцену":
                    style "fxt_button"
                    selected fx_cfg_runtime["preview"]
                    action Function(fxt_toggle, "preview")

            text fxt_hint_text() style "fxt_hint"


screen fxt_row(key):

    $ p = fx_cfg_param(key)
    $ v = fx_cfg(key)
    $ dirty = v != fx_cfg_saved(key)

    frame:
        style ("fxt_row_selected" if fxt_model.key == key else "fxt_row")

        vbox:
            hbox:
                spacing 6
                textbutton (("● " if dirty else "") + p.name):
                    style "fxt_name"
                    action Function(fxt_select, key)

                if p.kind == "bool":
                    textbutton ("вкл" if v else "выкл"):
                        style "fxt_button"
                        selected v
                        action Function(fxt_set, key, not v)
                elif p.kind == "choice":
                    for c in p.choices:
                        textbutton c:
                            style "fxt_button"
                            selected (v == c)
                            action Function(fxt_set, key, c)
                else:
                    textbutton "−" style "fxt_button" action Function(fxt_step, key, -1)
                    if p.lo is not None and p.hi is not None:
                        bar value FxtValue(key) yalign 0.5
                    textbutton "+" style "fxt_button" action Function(fxt_step, key, 1)
                    text fxt_value_text(key) style "fxt_value"

                textbutton "↺":
                    style "fxt_button"
                    sensitive (v != p.default)
                    action Function(fxt_reset, key)

            if p.doc:
                text fxt_quote(p.doc) style "fxt_doc" substitute False


## zorder выше модальных экранов игры — иначе хоткей глохнет внутри интерактивов.

screen fxt_hotkey_controller():
    zorder 1100
    key FXT_HOTKEY action ToggleScreen("fx_tuner")

init python:
    if config.developer:
        config.always_shown_screens.append("fxt_hotkey_controller")


style fxt_panel is frame:
    background "#000000e0"
    padding (16, 14)

style fxt_row is frame:
    background None
    padding (6, 3)
    xfill True

style fxt_row_selected is fxt_row:
    background "#00ff8818"

## Шрифт движка, а не игровой gui.text_font: служебная панель читается одинаково
## при любом оформлении игры.
style fxt_text is text:
    font "DejaVuSans.ttf"

style fxt_title is fxt_text:
    size 22
    bold True
    color "#ffffff"

style fxt_head is fxt_text:
    size 15
    color "#cccccc"

style fxt_caption is fxt_text:
    size 13
    color "#888888"

style fxt_group is fxt_text:
    size 18
    bold True
    color "#9fffcf"

style fxt_hint is fxt_text:
    size 13
    color "#999999"
    line_spacing 2

style fxt_warn is fxt_text:
    size 13
    color "#ff6b6b"

style fxt_doc is fxt_text:
    size 12
    color "#7a7a7a"

style fxt_value is fxt_text:
    size 15
    color "#ffffff"
    min_width 60
    yalign 0.5

style fxt_button is button:
    padding (8, 4)
    background "#ffffff18"
    hover_background "#ffffff33"
    selected_background "#00ff8840"
    insensitive_background "#ffffff08"
    yalign 0.5

style fxt_button_text is button_text:
    font "DejaVuSans.ttf"
    size 15
    color "#dddddd"
    hover_color "#ffffff"
    selected_color "#9fffcf"
    insensitive_color "#555555"

style fxt_name is button:
    padding (4, 4)
    background None
    xminimum 140
    yalign 0.5

style fxt_name_text is button_text:
    font "DejaVuSans.ttf"
    size 15
    color "#bbbbbb"
    hover_color "#ffffff"

style fxt_bar is bar:
    xsize 190
    ysize 18
    left_bar Solid("#00ff8866")
    right_bar Solid("#ffffff18")
    thumb None
    thumb_shadow None
    thumb_offset 0

style fxt_vscroll is vbar:
    xsize 6
    top_bar Solid("#ffffff44")
    bottom_bar Solid("#ffffff14")
    thumb None
    thumb_shadow None
    thumb_offset 0
