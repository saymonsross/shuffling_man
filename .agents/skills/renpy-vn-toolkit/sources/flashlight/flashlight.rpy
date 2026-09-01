init -2 python:
    # цвет темноты
    fl_color = "#012"

    # масштабирование пятна света
    fl_z = 1

    # картинка с дырявой темнотой
    flashlight = "flashlight"

# ДАЛЬШЕ НЕ МЕНЯТЬ
    def light_f(trans, st, at):
        trans.zoom = fl_z
        trans.anchor = (.5, .5)
        # координаты центра пятна по координатам мыши
        x, y = renpy.get_mouse_pos()
        trans.xpos, trans.ypos = int(x), int(y)
        return 1/30

    # изменение размеров пятна
    def light_z_plus(plus=.1):
        global fl_z
        fl_z += plus
        if fl_z > 2:
            fl_z = 2
        if fl_z < .5:
            fl_z = .5
    LightZPlus = renpy.curry(light_z_plus)

init:
    # трансформ для управления мышкой
    transform light_at:
        function light_f

    # силуэт цвета color
    transform paint(color="#fff"):
        matrixcolor TintMatrix(color) * InvertMatrix(1.) * TintMatrix("#000")

# экран для затемнения
screen flashlight:
    layer "master"
    zorder 200

    # управление зумом с помощью колёсика мыши
    key "rollback" action LightZPlus()
    key "rollforward" action LightZPlus(-.1)

    # вариант с тачскринами
    if renpy.variant("touch"):

        # темнота с пятном
        button:
            add flashlight at paint(fl_color)
            at light_at
            # чтобы прикосновение к экрану не продолжало игру
            action NullAction()

        # следующая сцена/текст - продолжить игру
        textbutton "»" text_size 250 align(1., .0) action renpy.curry(renpy.end_interaction)

    # вариант с мышкой
    else:

        # темнота с пятном
        add flashlight:
            at paint(fl_color), light_at
