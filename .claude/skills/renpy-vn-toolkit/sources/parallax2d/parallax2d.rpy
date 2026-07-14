# пример кнопки переключения параллакса в настройках или quick_menu:
# textbutton _("Параллакс") action Parallax()

# картинка для тестирования в скрипте, девочка справа
# image cg test = Par( "bg forest",  Pos("girl", xalign=.75) )

# фон для меню, девочка в центре, но отзеркалена
# image mm bg = Par( "mm 1", Pos("mm 2", xzoom=-1) )

# создаётся копия стройта image, но размещается поверх пустого экрана,
# чтобы параллакс мог работать с маленькими спрайтами и корректно их размещал,
# в параметрах на входе могут быть любые искажения и положение спрайта
# Pos(image, **kwarg)

## СЕЙЧАС НАСТРОЙКИ НАИБОЛЕЕ ОПТИМАЛЬНЫЕ
init -2 python:
    # плавность: ближе к 0 - медленнее
    par_easing_factor = .1

    # шаг зума для каждого следующего слоя
    par_zoom_plus = .05

## ДАЛЕЕ ЛУЧШЕ НИЧЕГО НЕ МЕНЯТЬ
    # по умолчанию параллакс выключен на мобильных устройствах
    if persistent.parallax is None:
        if renpy.variant("pc") or renpy.variant("web"):
            persistent.parallax = True
        else:
            persistent.parallax = False

    # класс для переключения параллакса
    class Parallax(Action):
        def __init__(self, blink=False):
            self.blink = blink
            if persistent.parallax is None:
                persistent.parallax = True

        def __call__(self):
            persistent.parallax = not persistent.parallax
            if self.blink:
                if persistent.parallax:
                    renpy.transition(Fade(.075, 0, .075, color="#f45"))
                else:
                    renpy.transition(Fade(.075, 0, .075, color="#2b7"))
            renpy.restart_interaction()

        def get_selected(self):
            return persistent.parallax

    # обработчик параллакса
    def par_f(index, trans, st, at, xaxis=True, yaxis=True):
        if trans.xalign is None:
            trans.xalign = .5
        if trans.yalign is None:
            trans.yalign = .5

        if persistent.parallax:
            x, y = renpy.display.draw.get_mouse_pos()

            target_zoom = 1 + par_zoom_plus * (index + 1)
            trans.zoom += (target_zoom - trans.zoom) * par_easing_factor

            target_xalign = x / config.screen_width
            target_yalign = y / config.screen_width

            if xaxis:
                trans.xalign += (target_xalign - trans.xalign) * par_easing_factor
            else:
                trans.xalign -= trans.xalign * par_easing_factor

            if yaxis:
                trans.yalign += (target_yalign - trans.yalign) * par_easing_factor
            else:
                trans.yalign -= trans.yalign * par_easing_factor

        else:
            trans.zoom += (1 - trans.zoom) * par_easing_factor

            trans.xalign -= trans.xalign * par_easing_factor
            trans.yalign -= trans.yalign * par_easing_factor

        return 1/30.

init -2:
    # трансформ для слоя параллакса
    # index - порядковый номер слоя (начиная с 0)
    # xaxis и yaxis - вкл/откл смещение по заданной оси
    transform par(index=0, xaxis=True, yaxis=True):
        subpixel True
        function renpy.curry(par_f)(index, xaxis=xaxis, yaxis=yaxis)

init -2 python:
    # аналог Composite, но без координат
    def Comp(size, *args, **properties):
        properties.setdefault('style', 'image_placement')
        width, height = size
        rv = Fixed(xmaximum=width, ymaximum=height, xminimum=width, yminimum=height, **properties)

        for widget in args:
            rv.add(widget)
        return rv

    # получить картинку с параллаксом
    # если картинка задана текстом типа "bg room", то добавляем к ней трансформ truecenter
    # остальные картинки считаются уже пропущенными через трансформы
    def Par(*layers, xaxis=True, yaxis=True, w=config.screen_width, h=config.screen_height, **kwarg):
        args = [ (w, h) ]
        for i in range(len(layers)):
            img = layers[i]
            if isinstance(img, (str, unicode)):
                img = At(str(img), truecenter)
            args.append(At(img, par(i, xaxis=True, yaxis=True)))
        return Comp(*args, **kwarg)

    # поместить спрайт в пустой экран на нужной позиции, чтобы слой занимал весь экран
    def Pos(image, xysize=(config.screen_width, config.screen_height), **kwarg):
        keys = kwarg.keys()
        # по умолчанию спрайт в центре
        if not "align" in keys:
            xa, ya = .5, .5
            # но могут быть варианты
            if "xalign" in keys:
                xa = kwarg["xalign"]
                del kwarg["xalign"]
            if "yalign" in keys:
                ya = kwarg["yalign"]
                del kwarg["yalign"]
            kwarg["align"] = (xa, ya)
        return Comp(xysize, Transform(image, **kwarg))
