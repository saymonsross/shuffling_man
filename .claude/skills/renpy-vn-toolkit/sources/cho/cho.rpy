## НАСТРОЙКИ ДЛЯ СВОИХ КНОПОК ВЫБОРА

# ширина в треть экрана
define gui.cho_button_width = config.screen_width // 3
define gui.cho_button_height = None

# замостить кнопку фоном
define gui.cho_button_tile = False

# отступы
define gui.cho_button_borders = Borders(48, 48, 48, 48)

# шрифт и размер текста кнопок
define gui.cho_button_text_font = gui.text_font
define gui.cho_button_text_size = gui.text_size

# положение текста в кнопках
define gui.cho_button_text_xalign = .5
define gui.cho_button_text_yalign = .5

# цвета текста кнопок
define gui.cho_button_text_idle_color = "#fff"
define gui.cho_button_text_hover_color = "#fed"
define gui.cho_button_text_selected_color = "#fed"
define gui.cho_button_text_insensitive_color = "#8888"

# расстояние между кнопками
define gui.cho_spacing = 64

init:
    # плавное появление
    transform ch_at(t=.5):
        on show:
            alpha 0
            linear t alpha 1

        on hide:
            linear t alpha 0

    # подкрашивание при наведении
    transform ch_hover_at(t=.5, color="#fd8", brightness=.25):
        on idle:
            ease t matrixcolor TintMatrix("#fff") * SaturationMatrix(1) * BrightnessMatrix(0)

        on insensitive:
            ease t matrixcolor TintMatrix("#fff") * SaturationMatrix(.25) * BrightnessMatrix(brightness)

        on hover, selected:
            ease t matrixcolor TintMatrix(color) * SaturationMatrix(1) * BrightnessMatrix(brightness)

## СТИЛИ ДЛЯ ВИДЖЕТОВ СВОЕГО ОКНА ВЫБОРОВ

    # заголовок
    style cho_label is label:
        align(.5, .5)

    style cho_label_text is label_text:
        align(.5, .5)
        text_align .5
        layout "subtitle"

    # контейнер для кнопок
    style cho_vbox:
        align(.5, .5)
        spacing gui.cho_spacing

    # кнопки
    style cho_button is default:
        properties gui.button_properties("cho_button")
        # середина кнопки
        background Frame("cho", 516 // 2, 55)
        yminimum 140

    # текст кнопок
    style cho_button_text is default:
        properties gui.text_properties("cho_button")

    # движение по восьмёрке ∞
    transform infinity(t=10):
        subpixel True
        align (.5, .5)
        around (.55, .5)
        linear t*.5 counterclockwise circles 1
        around (0.45, 0.5)
        linear t*.5 clockwise circles 1
        repeat

init python:
    # превратить в список, если это не список
    def make_list(x):
        if not x: return [ ]
        x = x if isinstance(x, list) else [ x ]
        return x

    # обновить экраны
    def refresh():
        renpy.restart_interaction()

    Refresh = renpy.curry(refresh)

    # аналог with для экранов
    def transition(transition=Dissolve(.15)):
        if transition:
            renpy.transition(transition)
            refresh()

    Transition = renpy.curry(transition)

# экран своего окна выборов
screen cho(items, label="", align=None, pos=None, anchor=(0, 0), at_list=[ ]):
    style_prefix "cho"

    vbox:
        at [ ch_at ] + make_list(at_list)

        if align:
            align align

        elif pos:
            pos pos

            if anchor:
                anchor anchor

        if label:
            label label

        for i in items:
            textbutton i.caption action Transition(), i.action at ch_hover_at sensitive (i.kwargs.get("sensitive", True))
