# за курсором следят только глаза в виде спрайтов на слое master!
# на экранах screen работать не будет

## ПРИМЕР:
# init:
    # тег должен быть тот же, что и после слова image!
    # image eye1 = Eye("eye1")

    # можно добавить цвет радужки
    # image eye1 = Eye("eye1", "#348")

# label start:
    # show eye1 as truecenter

# для работы требуется папка eye и 4 png оттуда с именами от "0" до "3"

init -2 python:
    # цвет глаз по умолчанию
    eye_default_color = "#589"

    # частота обновления глаз
    eyes_fps = 30

## ДАЛЕЕ ЛУЧШЕ НИЧЕГО НЕ ТРОГАТЬ
init:
    # eye 1 (радужка) и eye 2 (зрачок) должны быть меньше, чем eye 0 (белок)
    # чем меньше картинки, тем сильнее может поворачиваться глаз
    # eye 2 (зрачок) чуть меньше eye 1 (радужки), чтобы зрачок двигался сильнее, изображая поворот

    # белок, он же - маска прозрачности
    image eye 0 = Image("eye/0.png")

    # радужка
    image eye 1 = Image("eye/1.png")

    # зрачок
    image eye 2 = Image("eye/2.png")

    # веки
    image eye 3 = Image("eye/3.png")

    # подкрашивание картинок
    transform color(color=eye_default_color):
        matrixcolor TintMatrix(color)

    # для получения координат
    transform get_bounds_at(tag):
        function renpy.curry(get_bounds_at_f)(tag)

init -2 python:
    # своя версия Composite, вместо pos - align
    def AlignComposite(size, *args, **kwarg):
        kwarg.setdefault('anchor', (.5, .5))
        kwarg.setdefault('style', 'image_placement')
        width, height = size
        rv = renpy.display.layout.Fixed(xmaximum=width, ymaximum=height, xminimum=width, yminimum=height, **kwarg)
        if len(args) % 2 != 0:
            raise Exception(_("Нечётное число аргументов в функции Box (не считая размера)."))
        for align, widget in zip(args[0::2], args[1::2]):
            xalign, yalign = align
            rv.add(renpy.display.layout.Position(widget, xalign=xalign, yalign=yalign))
        return rv

    def get_size(displayable):
        w, h = renpy.render(renpy.displayable(displayable), config.screen_width, config.screen_height, 0, 0).get_size()
        return int(w), int(h)

    # конструктор глаза с учётом курсора
    def eye_f(st, at, tag="eye", eye_color=eye_default_color):
        global ax, ay, mx, x0
        
        x, y, w, h = eyes_data[tag]

        # центр глаза
        x0, y0 = x + w // 2, y + h // 2

        w, h = get_size("eye 0")

        # уйти от деления на ноль
        if x0 in (0, config.screen_width): x0 += 1
        if y0 in (0, config.screen_height): y0 += 1

        # курсор
        mx, my = renpy.get_mouse_pos()
        mx, my = int(mx), int(my)

        # положение радужки и зрачка
        ax = min(1., .5 * mx / x0)
        ay = min(1., .5 * my / y0)

        # глаз без века
        args = [ (w, h) ]

        # белок, радужка и зрачок
        for i in range(3):
            align=(.5, .5)

            # радужка и зрачок двигаются
            if i in (1, 2): align = (ax, ay)

            args.append(align)

            img = "eye " + str(i)

            # перекрашиваем в указанный цвет глаз
            if i == 1: img = At(img, color(eye_color))

            args.append(img)

        # обрезаем по контуру белка
        img = AlphaMask(Flatten(AlignComposite(*args)), "eye 0")

        # добавляем веко
        args = [ (w, h) ]

        align=(.5, .5)
        args.append(align)
        args.append(img)
        args.append(align)
        args.append("eye 3")

        return Flatten(AlignComposite(*args)), 1./eyes_fps

    # для сокращения писанины
    def Eye(tag="eye", eye_color=eye_default_color):
        global eyes_data

        eyes_data[tag] = ( 0, 0, 0, 0 )

        return DynamicDisplayable(eye_f, tag=tag, eye_color=eye_color)

## ПОСТОЯННО ПРОВЕРЯЕМ ПОЛОЖЕНИЕ КАЖДОГО ГЛАЗА
# такие вот костыли, чтобы избежать рекурсии
    eyes_data = { }

    def eyes_check_bounds():
        global eyes_data

        for tag in eyes_data.keys():
            # координаты и размеры этой картинки на экране
            temp = renpy.get_image_bounds(tag)

            # картинка не на экране
            if temp is None:
                x, y, w, h = eyes_data[tag]

            # есть на экране, узнаем положение
            else:
                x, y, w, h = temp

            if 0 in (w, h):
                w, h = get_size("eye 0")

            eyes_data[tag] = ( int(x), int(y), int(w), int(h) )

    EyesCheckBounds = renpy.curry(eyes_check_bounds)

    config.overlay_screens.append("eyes_data")

screen eyes_data():
    timer 1./eyes_fps repeat True action EyesCheckBounds()