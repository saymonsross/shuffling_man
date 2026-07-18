################################################################################
## Dev-инструмент позиционирования спрайтов — ТОЛЬКО для разработки.
##
## Перетаскиваемый полупрозрачный "призрак" выбранного спрайта поверх текущей
## сцены — реальный спрайт в дереве сцены не двигаем (иначе слетели бы rotate
## и матрицы времени суток из его собственного трансформа). HUD показывает
## готовую пару anchor+pos для вставки в define/трансформ — см. пример стиля
## позиционирования в 0_prologue/scene1.rpy: anchor (0.5, 0.5) или (0.0, 0.0)
## + pos (x, y) в пикселях.
##
## Запуск:
##   F9 в любой сцене                      — оверлей поверх текущего кадра.
##   Shift+O -> jump dev_position_sandbox   — изолированный тюнинг на чистом
##                                            фоне (см. label в конце файла).
##
## Из билда исключено ДВАЖДЫ:
##   1) config.developer=False в собранной игре не регистрирует F9-хоткей
##      (см. init python ниже) — Shift+O и console тоже недоступны без
##      developer-режима, так что label из этого файла в принципе не вызвать;
##   2) сама папка game/dev/ физически вырезана из дистрибутива —
##      build.classify('game/dev/**', None) в options.rpy.
##
## Строки HUD ниже — служебные, для разработчика, никогда не видны игроку
## (dev-only файл, исключён из билда и из tl-экстракта) — намеренно без _().
################################################################################

## Якори, которые перебирает Tab. Центр — дефолт: самый частый способ
## позиционирования спрайтов в проекте (anchor (0.5, 0.5) + pos (x, y)).
define _dev_pos_anchors = [(0.5, 0.5), (0.0, 0.0), (0.5, 1.0), (1.0, 1.0)]

default dev_pos_tag = None      # выбранный спрайт — полное имя (тег+атрибуты)
default dev_pos_drag_x = 0      # позиция призрака, левый верхний угол, px
default dev_pos_drag_y = 0
default dev_pos_w = 0           # размер выбранного спрайта, px
default dev_pos_h = 0
default dev_pos_anchor_i = 0    # индекс текущего якоря в _dev_pos_anchors
default dev_pos_mark_x = 0      # точка текущего якоря внутри призрака, px
default dev_pos_mark_y = 0
default dev_pos_readout_text = ""  # готовая строка "anchor (...)\npos (...)"

init -10 python:

    def dev_pos_select(tag):
        """Выбрать спрайт для тюнинга: взять его текущие bounds как старт
        позиции призрака. Без аргумента — первый показанный спрайт."""
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
        """Колбэк Drag: во время перетаскивания синхронизируем store."""
        d = drags[0]
        store.dev_pos_drag_x = int(d.x)
        store.dev_pos_drag_y = int(d.y)

    def dev_pos_dragged(drags, drop):
        dev_pos_dragging(drags)

    def dev_pos_anchor():
        """Текущий якорь (ax, ay) из _dev_pos_anchors."""
        i = dev_pos_anchor_i % len(_dev_pos_anchors)
        return _dev_pos_anchors[i]

    def dev_pos_line():
        """Готовая пара строк для вставки в .rpy: anchor + pos под текущий
        якорь, пересчитанный из левого-верхнего угла призрака и его размера."""
        ax, ay = dev_pos_anchor()
        pos_x = int(round(dev_pos_drag_x + ax * dev_pos_w))
        pos_y = int(round(dev_pos_drag_y + ay * dev_pos_h))
        return "anchor (%s, %s)\npos (%d, %d)" % (ax, ay, pos_x, pos_y)

## Полупрозрачный "призрак" — не мешает видеть исходное изображение под
## собой, но легко отличим от него.
transform dev_pos_ghost_look:
    alpha 0.6

## Всегда в памяти при config.developer (регистрация — в init python ниже);
## слушает F9 независимо от того, что сейчас показано на экране.
## zorder выше любых модальных экранов игры (modal True блокирует события
## только для того, что НИЖЕ по zorder) — иначе F9 глохнет в интерактивах
## вроде prologue_note_align.
screen dev_hotkey_controller():
    zorder 1100
    key "K_F9" action ToggleScreen("dev_position_tuner")

init python:
    if config.developer:
        config.always_shown_screens.append("dev_hotkey_controller")

screen dev_position_tuner(initial_tag=None):

    modal True
    zorder 1000

    ## Инициализация выбранного спрайта — один раз при каждом показе экрана.
    on "show" action Function(dev_pos_select, initial_tag)

    ## Пересчёт readout и точки якоря — производные значения, не игровая
    ## логика, безопасно пересчитывать каждый кадр.
    python:
        _dp_ax, _dp_ay = dev_pos_anchor()
        dev_pos_mark_x = int(round(_dp_ax * dev_pos_w))
        dev_pos_mark_y = int(round(_dp_ay * dev_pos_h))
        dev_pos_readout_text = dev_pos_line()

    ## Перетаскиваемый призрак выбранного спрайта.
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

                ## Тонкий контур bbox — сверка размеров.
                add Solid("#3f3c") xysize (dev_pos_w, 2) pos (0, 0)
                add Solid("#3f3c") xysize (dev_pos_w, 2) pos (0, dev_pos_h - 2)
                add Solid("#3f3c") xysize (2, dev_pos_h) pos (0, 0)
                add Solid("#3f3c") xysize (2, dev_pos_h) pos (dev_pos_w - 2, 0)

                ## Крестик в точке текущего якоря.
                add Solid("#3f3") xysize (16, 2) pos (dev_pos_mark_x, dev_pos_mark_y) anchor (0.5, 0.5)
                add Solid("#3f3") xysize (2, 16) pos (dev_pos_mark_x, dev_pos_mark_y) anchor (0.5, 0.5)

    ## Панель управления и readout.
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

    ## Клавиши точной подгонки позиции (noshift/shift взаимоисключающи —
    ## иначе K_LEFT сработал бы одновременно с shift_K_LEFT при зажатом Shift).
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


################################################################################
## Песочница для тюнинга спрайта в изоляции, на чистом фоне (без соседних
## объектов сцены). Скопировать под нужный спрайт: задать scene/show и тег в
## call screen. Запуск через консоль разработчика: Shift+O -> jump
## dev_position_sandbox.
################################################################################

label dev_position_sandbox:

    scene black

    show prologue_hand_right rest

    ## call screen — не core `call`-статement, from-клаус к нему не относится
    ## (правило CLAUDE.md про from — только для `call <label>`).
    call screen dev_position_tuner("prologue_hand_right rest")

    "Готово. Координаты — в консоли/буфере обмена."

    return
