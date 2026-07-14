### СОДЕРЖИМОЕ МОДУЛЯ НЕ МЕНЯТЬ!!! ПРОСТО ЧИТАЙТЕ ИНСТРУКЦИИ И ПОЛЬЗУЙТЕСЬ

## 1) РАЗМЫТАЯ ПОЛУПРОЗРАЧНАЯ ВИНЬЕТКА НУЖНОГО ЦВЕТА

# пример использования - показать/спрятать:
# $ vignette_on()
# $ vignette_off()

# возможно применение параметров для кастомизации виньетки:
# $ vignette_on(color="#000", a=.75, b=50, mask="bw_oval")
# color - цвет, a - прозрачность, b - размытие, mask - изображение рамки с прозрачным центром

init -1:
    # размеры экрана (для сокращения писанины)
    $ scr_w, scr_h = config.screen_width, config.screen_height

    # чёрный круг на белом фоне
    # генерируется программно на основе символов unicode «⚫︎»
    image bw_circle = Flatten(Composite(
        (scr_h, scr_h),
        (0, 0), At("#fff", crop(0, 0, scr_h, scr_h)),
        (0, 0), At(Text("⚫︎", font="DejaVuSans.ttf", size=int(scr_h*0.8531)), paint("#000"), crop(int(scr_h*0.031), 0, scr_h, scr_h))))

    # чёрный овал на белом фоне
    # круг, растянутый на весь экран
    image bw_oval = At("bw_circle", xzoom(scr_w / scr_h))

init -1 python:
    # можно получить рамку с разными параметрами (цвет, размытие, прозрачность, форма)
    # пример: show expression Vignette("#124", a=.25)
    def Vignette(color="#000", a=.75, b=50, mask="bw_oval"):
        return At(ImageMask(color, mask), alpha(a), blur(b))

    # добавим слой для виньетки, который не будет прятаться по нажатию h
    renpy.add_layer("vignette", above="screens")

    # показать виньетку
    def vignette_on(color="#000", a=.75, b=50, mask="bw_oval"):
        renpy.show_screen("vignette", color, a, b, mask)

    # скрыть виньетку
    def vignette_off():
        renpy.hide_screen("vignette")

# экран с виньеткой
# color - цвет, a - прозрачность, b - размытие, mask - изображение рамки с прозрачным центром
# transition - трансформ, содержащий on show и on hide
screen vignette(color="#000", a=.75, b=50, mask="bw_oval"):
    layer "vignette"
    add Vignette(color, a, b, mask)

## 2) ЦВЕТОКОР И МЕРЦАНИЕ

# пример использования - применить к слою master / отменить:
# $ color_on(brightness=.1) # чуть повышена яркость
# $ color_off()

# параметров может быть несколько:
# blink - мерцание (задаётся максимальная добавочная яркость)
# brightness - добавочная яркость
# tint - цвет для перекрашивания слоя
# saturation - насыщенность слоя
# contrast - контрастность слоя

# пример мерцающей киноплёнки:
# $ color_on(tint="#bcf", saturation=0, contrast=1.5, blink=.05)

init -1 python:

    # значения по умолчанию
    default_matrixcolor = {
        "blink": 0,
        "brightness": 0,
        "tint": "'#fff'",
        "saturation": 1,
        "contrast": 1
    }

    # текущие значения
    current_matrixcolor = { }

    # получить матрицу всех значений из current_matrixcolor
    def get_matrixcolor(matrixcolor):
        s = ""
        for i in matrixcolor.keys():
            ii = i
            value = matrixcolor[ii]

            if i == "blink":
                ii = "brightness"
                value = renpy.random.random() * value

            s = s + "*" + str(ii).title() + "Matrix(" + str(value) + ")"

        if s.startswith("*"):
            s = s[1:]

        if s:
            return eval(s)

        return None

    # функция цветокора, вызываемая из трансформа
    def color_at_f(trans, st, at):
        m = get_matrixcolor(current_matrixcolor)

        if not m is None:
            trans.matrixcolor = m

        if "blink" in current_matrixcolor.keys():
            return 1/8.

init:
    # трансформ для цветокора
    transform color_on_at():
        function color_at_f

    # выставить значения по умолчанию для цветокора
    transform color_off_at():
        matrixcolor get_matrixcolor(default_matrixcolor)

init -1 python:
    # применить цветокор на слое master
    def color_on(**kwarg):
        res = { }

        # применяем только разрешённые параметры
        # (для которых есть значения по умолчанию)
        for i in kwarg.keys():
            if str(i) == "tint" and isinstance(kwarg[i], (str, unicode)):
                kwarg[i] = "'" + str(kwarg[i]) + "'"

            if i in default_matrixcolor.keys():
                res[i] = kwarg[i]

        if res:
            store.current_matrixcolor = res
            renpy.show_layer_at(color_on_at(), "master", camera=True)

    # отменить эффект цветокора на слое master
    def color_off():
        store.current_matrixcolor = { }
        renpy.show_layer_at(color_off_at, "master", camera=True)
