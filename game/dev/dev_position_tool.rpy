################################################################################
## Dev-инструмент позиционирования спрайтов (только разработка).
##
## Перетаскиваемый «призрак» спрайта поверх сцены; реальный спрайт не трогаем
## (сохраняются его rotate/матрицы). HUD выдаёт готовую пару anchor+pos.
## Запуск: F9 в любой сцене; Shift+O → jump dev_position_sandbox — изолированно.
##
## Из билда исключено дважды: config.developer=False не регистрирует хоткей,
## а game/dev/ вырезана из дистрибутива (build.classify в options.rpy).
## Строки HUD — dev-only, намеренно без _().
################################################################################

## Якори, которые перебирает Tab; центр — самый частый в проекте.
define _dev_pos_anchors = [(0.5, 0.5), (0.0, 0.0), (0.5, 1.0), (1.0, 1.0)]

default dev_pos_tag = None      # выбранный спрайт (тег+атрибуты)
default dev_pos_drag_x = 0      # позиция призрака, левый верхний угол, px
default dev_pos_drag_y = 0
default dev_pos_w = 0           # размер выбранного спрайта, px
default dev_pos_h = 0
default dev_pos_anchor_i = 0    # индекс якоря в _dev_pos_anchors
default dev_pos_mark_x = 0      # точка якоря внутри призрака, px
default dev_pos_mark_y = 0
default dev_pos_readout_text = ""

init -10 python:

    def dev_pos_select(tag):
        """Выбрать спрайт: старт призрака — его текущие bounds. None — первый показанный."""
        if tag is None:
            sprites = get_showing_sprites()
            tag = sprites[0] if sprites else None

        store.dev_pos_tag = tag

        if tag:
            x, y, w, h = get_sprite_bounds(tag, layer="master")
        else:
            x, y, w, h = None, None, None, None

        if x is None:
            x, y, w, h = 100, 100, 0, 0

        store.dev_pos_drag_x = x
        store.dev_pos_drag_y = y
        store.dev_pos_w = w
        store.dev_pos_h = h
        store.dev_pos_anchor_i = 0

    def dev_pos_dragging(drags):
        d = drags[0]
        store.dev_pos_drag_x = int(d.x)
        store.dev_pos_drag_y = int(d.y)

    def dev_pos_dragged(drags, drop):
        dev_pos_dragging(drags)

    def dev_pos_anchor():
        i = dev_pos_anchor_i % len(_dev_pos_anchors)
        return _dev_pos_anchors[i]

    def dev_pos_line():
        """Пара строк anchor+pos для вставки в .rpy под текущий якорь."""
        ax, ay = dev_pos_anchor()
        pos_x = int(round(dev_pos_drag_x + ax * dev_pos_w))
        pos_y = int(round(dev_pos_drag_y + ay * dev_pos_h))
        return "anchor (%s, %s)\npos (%d, %d)" % (ax, ay, pos_x, pos_y)

transform dev_pos_ghost_look:
    alpha 0.6

## zorder выше модальных экранов игры — иначе F9 глохнет в интерактивах
## вроде hover_click (common/interactions.rpy).
screen dev_hotkey_controller():
    zorder 1100
    key "K_F9" action ToggleScreen("dev_position_tuner")

init python:
    if config.developer:
        config.always_shown_screens.append("dev_hotkey_controller")

screen dev_position_tuner(initial_tag=None):

    modal True
    zorder 1000

    on "show" action Function(dev_pos_select, initial_tag)

    ## Производные значения — безопасно пересчитывать каждый кадр.
    python:
        _dp_ax, _dp_ay = dev_pos_anchor()
        dev_pos_mark_x = int(round(_dp_ax * dev_pos_w))
        dev_pos_mark_y = int(round(_dp_ay * dev_pos_h))
        dev_pos_readout_text = dev_pos_line()

    if dev_pos_tag:
        drag:
            drag_name "dev_pos_ghost"
            xpos dev_pos_drag_x
            ypos dev_pos_drag_y
            xanchor 0
            yanchor 0

            draggable True
            droppable False
            focus_mask True

            dragging dev_pos_dragging
            dragged dev_pos_dragged

            fixed:
                xysize (dev_pos_w, dev_pos_h)

                add dev_pos_tag at dev_pos_ghost_look

                ## Контур bbox.
                add Solid("#3f3c") xysize (dev_pos_w, 2) pos (0, 0)
                add Solid("#3f3c") xysize (dev_pos_w, 2) pos (0, dev_pos_h - 2)
                add Solid("#3f3c") xysize (2, dev_pos_h) pos (0, 0)
                add Solid("#3f3c") xysize (2, dev_pos_h) pos (dev_pos_w - 2, 0)

                ## Крестик в точке якоря.
                add Solid("#3f3") xysize (16, 2) pos (dev_pos_mark_x, dev_pos_mark_y) anchor (0.5, 0.5)
                add Solid("#3f3") xysize (2, 16) pos (dev_pos_mark_x, dev_pos_mark_y) anchor (0.5, 0.5)

    frame:
        align (0.01, 0.01)
        padding (16, 12)
        background "#000c"

        vbox:
            spacing 4

            text "POSITION TUNER" size 20 color "#fff" bold True

            null height 6

            text "sprite: [dev_pos_tag!q]" size 16 color "#fff"

            vbox:
                spacing 2
                for s in get_showing_sprites():
                    textbutton "[s]":
                        style "dev_pos_list_button"
                        selected (s == dev_pos_tag)
                        action Function(dev_pos_select, s)

            null height 8

            text "[dev_pos_readout_text!q]" size 18 color "#9f9"

            text "top-left: ([dev_pos_drag_x], [dev_pos_drag_y])   size: [dev_pos_w]x[dev_pos_h]" size 14 color "#ccc"

            null height 8

            text "drag мышью · стрелки 1px · Shift+стрелки 10px · Tab — якорь" size 13 color "#999"

            hbox:
                spacing 8
                textbutton "Копировать" action CopyToClipboard(dev_pos_readout_text)
                textbutton "Готово" action Hide("dev_position_tuner")

    ## noshift/shift взаимоисключающи — иначе двойное срабатывание при Shift.
    key "noshift_K_LEFT" action SetVariable("dev_pos_drag_x", dev_pos_drag_x - 1)
    key "noshift_K_RIGHT" action SetVariable("dev_pos_drag_x", dev_pos_drag_x + 1)
    key "noshift_K_UP" action SetVariable("dev_pos_drag_y", dev_pos_drag_y - 1)
    key "noshift_K_DOWN" action SetVariable("dev_pos_drag_y", dev_pos_drag_y + 1)

    key "shift_K_LEFT" action SetVariable("dev_pos_drag_x", dev_pos_drag_x - 10)
    key "shift_K_RIGHT" action SetVariable("dev_pos_drag_x", dev_pos_drag_x + 10)
    key "shift_K_UP" action SetVariable("dev_pos_drag_y", dev_pos_drag_y - 10)
    key "shift_K_DOWN" action SetVariable("dev_pos_drag_y", dev_pos_drag_y + 10)

    key "K_TAB" action SetVariable("dev_pos_anchor_i", dev_pos_anchor_i + 1)

    key "K_F9" action Hide("dev_position_tuner")
    key "game_menu" action Hide("dev_position_tuner")

style dev_pos_list_button is button:
    padding (4, 1)

style dev_pos_list_button_text is button_text:
    size 13
    color "#ccc"
    selected_color "#9f9"


## Песочница: тюнинг спрайта на чистом фоне. Скопировать под нужный спрайт
## (scene/show и тег в call screen). Запуск: Shift+O → jump dev_position_sandbox.
label dev_position_sandbox:

    scene black

    show prologue_hand_right rest

    call screen dev_position_tuner("prologue_hand_right rest")

    "Готово. Координаты — в консоли/буфере обмена."

    return
