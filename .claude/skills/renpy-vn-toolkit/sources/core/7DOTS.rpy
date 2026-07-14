# замена str(), чтобы не вылетала на линуксе
define mystr = eval("lambda i: '%s' % i")

# для увеличения пиксельной графики
# define config.nearest_neighbor = True

# аналоги with ease*** с одновременным растворением
define dissolveleft   = ComposeTransition(dissolve, before=easeoutleft,   after=easeinleft)
define dissolveright  = ComposeTransition(dissolve, before=easeoutright,  after=easeinright)
define dissolvetop    = ComposeTransition(dissolve, before=easeouttop,    after=easeintop)
define dissolvebottom = ComposeTransition(dissolve, before=easeoutbottom, after=easeinbottom)

init -999 python:
    # своя версия Composite, можно задать anchor (по умолчанию якорь в центре)
    def Comp(size, *args, **kwarg):
        kwarg.setdefault('anchor', (.5, .5))
        kwarg.setdefault('style', 'image_placement')
        width, height = size
        rv = renpy.display.layout.Fixed(xmaximum=width, ymaximum=height, xminimum=width, yminimum=height, **kwarg)
        if len(args) % 2 != 0:
            raise Exception("Comp (7DOTS.rpy) requires an odd number of arguments.")
        for pos, widget in zip(args[0::2], args[1::2]):
            xpos, ypos = pos
            xanchor, yanchor = kwarg.get("anchor")
            rv.add(renpy.display.layout.Position(widget, xpos=xpos, xanchor=xanchor, ypos=ypos, yanchor=yanchor))
        return rv

    # выставить одинаковый эффект для всех переходов в IDE
    def transitions(transition=dissolve):
        config.enter_replay_transition = transition
        config.exit_replay_transition = transition

        config.game_main_transition = transition

        config.intra_transition = transition
        config.enter_yesno_transition = transition
        config.enter_transition = transition
        config.after_load_transition = transition

        config.end_splash_transition = transition
        config.end_game_transition = transition
        config.exit_transition = transition

        config.adv_nvl_transition = transition
        config.nvl_adv_transition = transition

    # дополняем список команд, при запуске которых текстбокс будет прятаться в режиме config.window = "auto"
    # [ "scene", "call screen", "menu", "say-centered", "say-bubble" ]
    def auto_hide(cmd_list=[ "pause", "hide", "show", "call", "show screen", "screen", "return" ]):
        for i in cmd_list:
            if not i in config.window_auto_hide:
                config.window_auto_hide.append(i)

    # отмена auto_hide
    def auto_hide_off():
        config.window_auto_hide = [ "scene", "call screen", "menu", "say-centered", "say-bubble" ]

    # деление с переводом в целочисленное для нового ренпая
    def d2(x, d=2):
        return int(x / d)

    # % для дробных
    def modf(x, y, precision=1000):
        precision *= 1.
        x *= precision
        y *= precision
        return (x % y) / precision

    # секунды в строку
    def sec_to_hms(s):
        m, s = divmod(s, 60)
        h, m = divmod(m, 60)
        if h > 0:
            return '{}:{:0>2}:{:0>2}'.format(h, m, s)
        # только минуты и секунды, если часов ноль
        return '{:0>2}:{:0>2}'.format(m, s)

    # задаём пределы
    clip = lambda i, mini, maxi: max(min(maxi, i), mini)

    # получить переменную из словаря с зашитой от дурака
    def dict_get(dictionary, key, default=None):
        if key in dictionary.keys():
            return dictionary[key]

        return default

    # строка в целочисленное или в дробное
    def fint(x, default=0): # можно None
        try:
            x = int(x)
            return x
        except:
            try:
                x = float(x)
                return x
            except:
                return default

    # префиксы спрайтов, теги в которых нужно делить не пробелами, а "_"
    layered_prefixes = []

    # для плавных переходов между мелодиями и звуками
    default_fade = 1.5

init:
    # эффект для смены "говорящих голов" в текстбоксе с помощью xoffset
    transform side_move(old, new):
        contains:
            old
            align(.0, 1.)
            alpha 1
            xoffset 0
            ease .25 alpha 0 xoffset -config.screen_width // 6
        contains:
            new
            align(.0, 1.)
            alpha 0
            xoffset -config.screen_width // 6
            .25
            ease .25 alpha 1 xoffset 0

    # если меняются только эмоции у того же персонажа
    transform side_same(old, new):
        contains:
            old
            new with Dissolve(.25, alpha=True, mipmap=True)

init -222:
    # эффект для плавного появления/исчезновения
    transform show_hide(t=.25):
        on show:
            alpha 0
            linear t alpha 1
        on hide:
            linear t alpha 0

    # трансформ для реакции виджетов на курсор мышки (якорь по центру!)
    # не работает корректно совместно с другими трансформами, например: at hover_at, show_hide
    transform hover_at(hover_brightness=.15, hover_zoom=.15, t=.25):
        anchor(.5, .5)

        on idle:
            ease t zoom 1 matrixcolor BrightnessMatrix(0)

        on hover, selected:
            parallel:
                ease t * .4 zoom 1 + hover_zoom
                ease t * .4 zoom 1 - hover_zoom / 3.
                ease t * .1 zoom 1 + hover_zoom * 3. / 4.
                ease t * .1 zoom 1 + hover_zoom
            parallel:
                ease t matrixcolor BrightnessMatrix(hover_brightness)

    # переход для with (параметры на входе можно менять)
    # аналог leap для спрайтов (см. ниже), но по умолчанию якорь в центре
    transform zpunch(old_widget=None, new_widget=None, dt=.5, dyz=.05, dxz=.05, align=(.5, .5), anchor=(.5, .5)):
        # пауза на время эффекта
        delay dt

        contains:
            # новый кадр (или прежний, если ничего не меняли)
            new_widget
            # якорь
            anchor anchor
            # относительное положение
            align align
            # более плавная анимация
            subpixel True
            # начинается с обычных размеров
            xzoom 1 yzoom 1
            # несколько раз растягивается в разные стороны
            easein dt*.25 yzoom 1+dyz xzoom 1+dxz/2.
            easeout dt*.25 yzoom 1 xzoom 1
            easein dt*.15 yzoom 1+dyz/2. xzoom 1+dxz
            easeout dt*.15 yzoom 1 xzoom 1
            easein dt*.1 yzoom 1+dyz/4. xzoom 1+dxz/2
            easeout dt*.1 yzoom 1 xzoom 1

        # на случай смены кадра - старый плавно, но быстро исчезает
        contains:
            # все слои собираются в один, чтобы избежать эффекта рентгена
            Flatten(old_widget)
            alpha 1
            ease .15 alpha 0

    # "дыхание" - просто небольшое сплющивание-вытягивание по вертикали
    transform breath(t=2.5, dz=.005):
        subpixel True

        yalign 1.
        ease t*.35 yzoom 1-dz
        t*.15
        ease t*.35 yzoom 1
        t*.15
        repeat

    # масштабирование
    transform zoom(zoom=1):
        subpixel True
        zoom zoom
    transform xzoom(zoom=1):
        subpixel True
        xzoom zoom
    transform yzoom(zoom=1):
        subpixel True
        yzoom zoom
    transform zooming(zoom1=1., zoom2=1., t=1):
        subpixel True
        zoom zoom1
        ease t zoom zoom2
    transform xyzooming(xzoom1=1., yzoom1=1., xzoom2=1., yzoom2=1., t=1):
        subpixel True
        xzoom xzoom1 yzoom yzoom1
        ease t xzoom xzoom2 yzoom yzoom2

    # прозрачность
    transform alpha(alpha=1.):
        alpha alpha
    transform alphing(alpha1=0, alpha2=1, t=1):
        alpha alpha1
        ease t alpha alpha2

    # размытость
    transform blur(blur=4):
        blur blur
    transform bluring(blur1=0, blur2=16, t=1):
        blur blur1
        ease t blur blur2

    # яркость
    transform brightness(brightness=.25):
        matrixcolor BrightnessMatrix(brightness)

    transform brightnessing(brightness1=0, brightness2=.25, t=2):
        matrixcolor BrightnessMatrix(brightness1)
        ease t matrixcolor BrightnessMatrix(brightness2)

    # контраст
    transform contrast(contrast=1.25):
        matrixcolor ContrastMatrix(contrast)

    transform contrasting(contrast1=1, contrast2=1.25, t=2):
        matrixcolor ContrastMatrix(contrast1)
        ease t matrixcolor ContrastMatrix(contrast2)

    # насыщенность
    transform saturation(saturation=1.):
        matrixcolor SaturationMatrix(saturation)

    transform saturationing(saturation1=1., saturation2=.5, t=2):
        matrixcolor SaturationMatrix(saturation1)
        ease t matrixcolor SaturationMatrix(saturation2)

    # подкрашивание картинок
    transform color(color="#000"):
        matrixcolor TintMatrix(color)

    # силуэт цвета color color1 переходит в color2
    transform coloring(color1="#fff", color2="#fff", t=2):
        matrixcolor TintMatrix(color1)
        ease t matrixcolor TintMatrix(color2)

    # спрайт цвета color1 переливается в color2
    transform color2(color1="#fff", color2="#def", t=2):
        matrixcolor TintMatrix(color1)
        ease_quad t*.5 matrixcolor TintMatrix(color2)
        ease_quad t*.5 matrixcolor TintMatrix(color1)
        repeat

    # силуэт цвета color
    transform paint(color="#fff"):
        matrixcolor TintMatrix(color) * InvertMatrix(1.) * TintMatrix("#000")

    # силуэт цвета color color1 переходит в color2
    transform painting(color1="#fff", color2="#fff", t=2):
        matrixcolor TintMatrix(color1) * InvertMatrix(1.) * TintMatrix("#000")
        ease t matrixcolor TintMatrix(color2) * InvertMatrix(1.) * TintMatrix("#000")

    # силуэт цвета color1 переливается в color2 циклично
    transform paint2(color1="#fff", color2="#def", t=2):
        matrixcolor TintMatrix(color1) * InvertMatrix(1.) * TintMatrix("#000")
        ease_quad t*.5 matrixcolor TintMatrix(color2) * InvertMatrix(1.) * TintMatrix("#000")
        ease_quad t*.5 matrixcolor TintMatrix(color1) * InvertMatrix(1.) * TintMatrix("#000")
        repeat

    # относительное положение
    transform xalign(xalign=.5):
        xalign xalign
    transform yalign(yalign=1.):
        yalign yalign
    transform align(xalign=.5, yalign=1.):
        align (xalign, yalign)
    transform aligning(xalign1=.5, yalign1=1., xalign2=.5, yalign2=1., t=1):
        subpixel True
        align (xalign1, yalign1)
        ease t align (xalign2, yalign2)

    # размеры
    transform xysize(width, height):
        xysize (width, height)
    transform xsize(width):
        xsize width
    transform ysize(height):
        ysize height

    # положение
    transform xpos(xpos=.5):
        xpos xpos
    transform ypos(ypos=.0):
        ypos ypos
    transform pos(xpos=.5, ypos=.0):
        pos (xpos, ypos)
    transform posing(xpos1=.5, ypos1=1., xpos2=.5, ypos2=1., t=1):
        subpixel True
        pos (xpos1, ypos1)
        ease t pos (xpos2, ypos2)

    transform zpos(zpos=0, depth=True, zzoom=False):
        gl_depth depth
        zzoom zzoom
        zpos zpos
    transform zposing(zpos=0, t=1, depth=True, zzoom=False):
        gl_depth depth
        zzoom zzoom
        ease t zpos zpos

    transform gl_depth(gl_depth=True):
        gl_depth gl_depth

    # размер
    transform xysize(width=config.screen_width, height=config.screen_height):
        xysize(width, height)
    transform xsize(width=config.screen_width):
        ysize width
    transform ysize(height=config.screen_height):
        ysize height

    # смещение
    transform xoffset(xoffset=0):
        xoffset xoffset
    transform yoffset(yoffset=0):
        yoffset yoffset
    transform offset(xoffset=5, yoffset=0):
        offset (xoffset, yoffset)
    transform offseting(xoffset1=0, yoffset1=0, xoffset2=0, yoffset2=10, t=1):
        subpixel True
        offset (xoffset1, yoffset1)
        ease t offset (xoffset2, yoffset2)

    # якорь
    transform xanchor(xanchor=.5):
        xanchor xanchor
    transform yanchor(yanchor=1.):
        yanchor yanchor
    transform anchor(xanchor=.5, yanchor=1.):
        anchor (xanchor, yanchor)
    transform anchoring(xanchor1=.5, yanchor1=.5, xanchor2=.5, yanchor2=.5, t=1):
        anchor (xanchor1, yanchor1)
        ease t anchor (xanchor2, yanchor2)

    # отзеркаливание
    transform hflip:
        subpixel True
        xzoom -1
    transform vflip:
        subpixel True
        yzoom -1

    # поворот против часовой
    transform rotate(a=45, rotate_pad=False):
        subpixel True
        rotate_pad rotate_pad
        rotate a
    transform rotating(a1=0, a2=360, t=1, rotate_pad=False):
        subpixel True
        rotate_pad rotate_pad
        rotate a1
        ease t rotate a2

    # повороты с перспективой
    ## вверх-вниз
    transform turnx(x=45, depth=True):
        subpixel True
        perspective True
        gl_depth depth
        matrixtransform RotateMatrix(x, 0, 0)

    transform turningx(x=45, t=1, depth=True):
        subpixel True
        perspective True
        gl_depth depth
        ease t matrixtransform RotateMatrix(x, 0, 0)

    ## влево-вправо
    transform turny(y=45, depth=True):
        subpixel True
        perspective True
        gl_depth depth
        matrixtransform RotateMatrix(0, y, 0)

    transform turningy(y=45, t=1, depth=True):
        subpixel True
        perspective True
        gl_depth depth
        ease t matrixtransform RotateMatrix(0, y, 0)

    ## против часовой-по часовой
    transform turnz(z=45, depth=True):
        subpixel True
        perspective True
        gl_depth depth
        matrixtransform RotateMatrix(0, 0, z)

    transform turningz(z=45, t=1, depth=True):
        subpixel True
        perspective True
        gl_depth depth
        ease t matrixtransform RotateMatrix(0, 0, z)

    ## по всем направлениям
    transform turn(x=0, y=45, z=0, depth=True):
        subpixel True
        perspective True
        gl_depth depth
        matrixtransform RotateMatrix(x, y, z)

    transform turning(x=0, y=45, z=0, t=1, depth=True):
        subpixel True
        perspective True
        gl_depth depth
        ease t matrixtransform RotateMatrix(x, y, z)

    # вырезание
    transform crop(x=0, y=0, w=1., h=1.):
        crop(x, y, w, h)

    # подпрыгивание персонажа
    transform leap(dt=.25, dyz=.01, dxz=.005):
        subpixel True
        xzoom 1 yzoom 1
        easein dt*.35 yzoom 1+dyz xzoom 1-dxz
        easeout dt*.35 yzoom 1 xzoom 1
        easein dt*.15 yzoom 1-dyz xzoom 1+dxz
        easeout dt*.15 yzoom 1 xzoom 1

    # слева, но не у самого края
    transform left2(xa=.35):
        anchor (.5, 1.)
        align(xa, 1.)

    # справа, но не у самого края
    transform right2(xa=.65):
        anchor (.5, 1.)
        align(xa, 1.)

    # слева, за краем
    transform left0():
        anchor (1., 1.)
        pos (.0, 1.)

    # справа, за краем
    transform right0():
        anchor (1., 1.)
        pos (1., 1.)

    # сиськотряс
    transform boobs(t=2):
        subpixel True
        yanchor 0 yzoom 1
        easeout (t*.075) yzoom 1.05
        easein  (t*.1)   yzoom .95
        easeout (t*.125) yzoom 1.025
        easein  (t*.125) yzoom .975
        easeout (t*.125) yzoom 1.01
        easein  (t*.15)  yzoom .99
        easeout (t*.15)  yzoom 1.005
        easein  (t*.15)  yzoom 1.

init -998:
    # transition для with и для переходов между экранами в виде перелистывания страницы
    transform TurnPageAt(delay=.5, vertical=False, reverse=False, sound=def_list_sound, new_widget=None, old_widget=None):
        delay delay
        contains:
            events False
            function renpy.curry(s_play)(def_list_sound)
            Transform(new_widget, mesh=True)
        contains:
            perspective True
            Transform(old_widget, mesh=True)
            matrixanchor ( (.5 if vertical else 1. if reverse else .0), (.5 if not vertical else .0 if reverse else 1.) )
            matrixtransform RotateMatrix(0, 0, 0)
            ease delay matrixtransform RotateMatrix( bool(vertical) * (90 if reverse else -90), bool(not vertical) * (90 if reverse else -90), 0)

init -999 python:
    # можно задать звук для перелистывания:
    # def_list_sound = "turnpage"
    def_list_sound = None

init python:
    # регистрируем шейдер градиента
    renpy.register_shader("example.gradient", variables="""
        uniform vec4 u_gradient_left;
        uniform vec4 u_gradient_right;
        uniform vec2 u_model_size;
        varying float v_gradient_done;
        attribute vec4 a_position;
    """, vertex_300="""
        v_gradient_done = a_position.x / u_model_size.x;
    """, fragment_300="""
        float gradient_done = v_gradient_done;
        gl_FragColor *= mix(u_gradient_left, u_gradient_right, gradient_done);
    """)

    # антибаговый костыль
    def TurnPage(delay=.5, vertical=False, reverse=False, new_widget=None, old_widget=None):
        return ComposeTransition(CropMove(delay, mode="custom", startcrop=(.0, .0, .0, .0), startpos=(.0, .0), endcrop=(.0, .0, .0, .0), endpos=(.0, .0)), before=TurnPageAt(delay, vertical, reverse, new_widget, old_widget))

    # перечень перелистываний в разные стороны
    turn2left = TurnPage()
    turn2right = TurnPage(reverse=True)
    turn2up = TurnPage(vertical=True, reverse=True)
    turn2down = TurnPage(vertical=True)

    # вызвать метку, если она есть
    # метку можно задать списком, тогда будет вызов первой же рабочей метки из этого списка
    # пример: $ dlc([ "dlc_label", "default_label" ])
    # в этом случае, если был скачан файл, содержащий метку dlc_label со сценой 18+, то вызовет её,
    # иначе будет вызвана метка default_label, где сцена сокращённая, без 18+
    def dlc(label, *args, **kwarg):
        label = make_list(label)
        i = 0
        while i < len(label):
            if renpy.has_label(label[i]):
                renpy.call(label[i], *args, from_current=False, **kwarg)
                i = len(label)
            i += 1

init -222 python:
    # обрубаем длинный текст (allow - разрешённые теги, по умолчанию таких нет)
    def str_cut(s, max_len=11, dots="…", allow=[ ]):
        s = renpy.filter_text_tags(s, allow=allow)
        return s[:max_len] + dots if len(s) > max_len and len(s) > 0 and max_len > 0 else s

    # получить содержимое поля ввода
    # например, можно на экран input добавить кнопки:
    # textbutton "OK" align(.5, 1.) action Return(get_input_text())
    # textbutton "Cancel" align(.5, 1.) action Return("")
    def get_input_text(screen="input", id="input"):
        widget = renpy.get_widget(screen=screen, id=id)
        if widget:
            return str(widget.content)
        return None

    # получить элемент списка, перед x
    def prev_x(x, lst):
        i = lst.index(x) if x in lst else len(lst)
        i = (i - 1) % len(lst)
        return lst[i]

    # получить элемент списка, следующий за x
    def next_x(x, lst):
        i = lst.index(x) if x in lst else -1
        i = (i + 1) % len(lst)
        return lst[i]

    # смена языка на указанный
    # или на следующий в списке имеющихся, если язык не указывать
    def lang(language="next"):
        lst = [None] + list(renpy.known_languages())
        if language == "next":
            language = next_x(_preferences.language, lst)
        if language in lst:
            renpy.change_language(language)
    Lang = renpy.curry(lang)

    # переменная для хранения скорости вывода текста
    CPS = preferences.text_cps

    # сохранить значение скорости
    def cps_save():
        global CPS
        CPS = preferences.text_cps

    # узнать скорость
    def cps_get():
        return preferences.text_cps

    # изменить скорость
    def cps_set(cps):
        preferences.text_cps = cps

    # восстановить сохраненное значение скорости
    def cps_restore():
        preferences.text_cps = CPS

    # единоразовый dismiss
    def skip_once():
        renpy.end_interaction(True)
    SkipOnce = renpy.curry(skip_once)

    # остановить перемотку
    def skip_stop():
        renpy.config.skipping = None
    SkipStop = renpy.curry(skip_stop)

    # нужно, чтобы включить/отключить dismiss
    can_dismiss = True

    def dismiss_block():
        global can_dismiss
        return can_dismiss

    # включить dismiss
    def dismiss_on():
        store.can_dismiss = True
    DismissOn = renpy.curry(dismiss_on)

    # отключить dismiss
    def dismiss_off():
        if config.say_allow_dismiss is None:
            config.say_allow_dismiss = dismiss_block
        store.can_dismiss = False
    DismissOff = renpy.curry(dismiss_off)

    # для отладки
    def log(*args):
        for i in args:
            print(str(i))
    Log = renpy.curry(log)

    # секундный эффект вспышки нужного цвета для смены фонов
    # без лишних параметров
    def Flash(color="#fff", t=1):
        return Fade(t*.3, t*.1, t*.6, color=color)

    # белая вспышка
    flash = Flash()

    # показан ли экран (или один из экранов)
    def has_screen(*args, **kwarg):
        layer = kwarg.get("layer", None)

        for i in make_list(args):
            if renpy.get_screen(i, layer):
                return True

        return False

    # существует ли экран в принципе
    def screen_exists(name):
        for i in renpy.config.variants:
            if renpy.display.screen.screens.get((name, i), None) is not None:
                return True
        return False

    # показать/скрыть экран
    def showhide(screen, effect=dissolve):
        if has_screen(screen):
            renpy.hide_screen(screen)
        else:
            renpy.show_screen(screen)
        renpy.transition(effect)
        renpy.restart_interaction()
    ShowHide = renpy.curry(showhide)

    # поменять глобальные переменные. например:
    # textbutton _("Выход") action Quit() hovered SetVal(mm_bg="black") unhovered SetVal(mm_bg=None)
    # по умолчанию применяется эффект dissolve, но его можно отменить, экран сразу не поменяется:
    # textbutton _("Выход") action Quit() hovered SetVal(mm_bg="black", transition=None)
    def set_val(**kwarg):
        transition = kwarg.pop("transition", dissolve)

        for i in kwarg.keys():
            globals()[i] = kwarg[i]

        if transition:
            renpy.transition(transition)
            renpy.restart_interaction()

    SetVal = renpy.curry(set_val)

    # директории для хранение звуков и музыки
    audio_dir = "audio"
    music_dir = "music"

    # жёсткая пауза
    def pause(t=1, hard=True):
        renpy.pause(t, hard=hard)

    # получить скриншот заданного размера, по умолчанию весь экран
    def shot(w=config.screen_width, h=config.screen_height):
        renpy.take_screenshot((w, h))
        renpy.restart_interaction()
        return FileCurrentScreenshot()

    # сканируем папку музыки, на выходе - список мелодий без указанного расширения и папки
    def get_music_list(folder=music_dir, ext="ogg"):
        res = []
        lst = renpy.list_files()
        for i in lst:
            if str(i).startswith(str(folder)):
                s = i[(len(folder) + 1):]
                if s.endswith("." + ext):
                    res.append(s[:(-len(ext) - 1)])
        return res

    # сканируем папку, на выходе - список файлов нужного расширения
    # по умолчанию расширения убираются
    def get_file_list(folder="", ext="", hideext=True):
        res = []
        lst = renpy.list_files()
        for i in lst:
            if i.startswith(folder) or (not folder):
                if folder:
                    s = i[(len(folder) + 1):]
                else:
                    s = i
                if ext:
                    if s.endswith("." + ext):
                        if hideext:
                            s = s[:(-len(ext) - 1)]
                        res.append(s)
                else:
                    res.append(s)
        if len(res) > 1:
            # сортировка без учета регистра
            res = sorted(res, key=lambda s: s.lower())
        return res

    # окно игры в центре экрана (вызывается из init)
    def window_center():
        import os
        os.environ['SDL_VIDEO_CENTERED'] = '1'

    # автоматическое объявление изображений (вызывается из init)
    def images_auto(folders=[ ], spaces=[ ' ', '_', '/' ], minimum=1, dlc="DLC"):
        # если задано имя папки, то нумеруем сотню копий и добавляем к проверяемым папкам
        # если dlc == "DLC", то ищем "DLC1", "DLC2", "DLC3" и т.д.
        folders = [ "images" ] + make_list(folders)
        if isinstance(dlc, (str, unicode)):
            folders = folders + [ str(dlc) + str(i) for i in range(1, 101) ]
        for i in folders:
            if not i in config.automatic_images_strip:
                config.automatic_images_strip.append(i)
        config.automatic_images = spaces
        config.automatic_images_minimum_components = minimum

    # остановить перемотку
    def stop_skip():
        renpy.config.skipping = None

    # строку в displayable
    def img2disp(displayable):
        if isinstance(displayable, (str, unicode)):
            return renpy.displayable(displayable)

        return displayable

    # узнать текущие размеры изображения типа displayable
    # например, после масштабирования и других операций
    # не работает в разделе init
    def get_size(displayable):
        w, h = renpy.render(img2disp(displayable), config.screen_width, config.screen_height, 0, 0).get_size()
        return int(w), int(h)
    def get_width(displayable):
        return get_size(displayable)[0]
    def get_height(displayable):
        return get_size(displayable)[1]

    # получить прозрачность пикселя
    # по умолчанию правый нижний угол
    def get_opaque(img, x=None, y=None):
        r = renpy.render(renpy.displayable(img), 0, 0, 0, 0)
        w, h = get_size(img)
        w, h = int(w), int(h)
        if x is None:
            x = w - 1
        if y is None:
            y = h - 1
        return r.is_pixel_opaque(x, y)

    # True - пиксель на спрайте непрозрачный
    # то есть его прозрачность выше минимального значения min_a
    def is_opaque(img, x=None, y=None, min_a=0):
        a = get_opaque(img, x, y)
        return a > min_a

    # если это не список, то сделать единственным элементом списка
    def make_list(param):
        if param is None: return None
        if not isinstance(param, list): param = [ param ]
        return param

    # если в кортеже или списке не хватает элементов,
    # можно добавить значения по умолчанию (или отсечь лишние t = [ 1, 2, 3, 4 ])
    # t = (1, 2)
    # x, y, z = get_tuple(t, None, None, None)
    # на выходе - кортеж
    def get_tuple(value, *args):
        if not isinstance(value, tuple): value = make_list(value)
        if value is None: value = [ ]
        args = make_list(list(args))
        res = make_list(list(value))
        value = res
        if len(value) > len(args): res = value[:len(args)]
        if len(value) < len(args): res = value + args[len(value):]
        return tuple(res)

    # промежуточная функция, чтобы привязать трансформом к курсору (для transform xy_at)
    def xy_at_f(trans, st, at):
        x, y = renpy.get_mouse_pos()
        trans.anchor = (.5, .5)
        trans.xpos, trans.ypos = int(x), int(y)
        return 1/30.

# автоматическое объявление анимации
    # описание функции Ani:
    # автоматическое объявление картинки с анимацией,
    # например есть кадры "images/neko%s.png",
    # где %s - числа от 1 до 5, тогда объявляем анимацию так:
    # image neko = Ani("neko", 5, 0.5, reverse = False)
    # где:
    # img_name - имя файла без номера (например, "neko")
    # frames - количество кадров
    # delay - пауза между кадрами в секундах
    # если delay это кортеж, например (1, 2), то скорость будет меняться от 1 до 2 секунд
    # loop - зациклить анимацию (по умолчанию включено)
    # reverse - нужно ли проигрывание анимации в обратную сторону
    # effect - эффект для смены кадров
    # start - с какой цифры начинать отсчет кадров
    # ext - расширение, если оно отлично от Null, то работаем с файлами,
    # при ext=Null - с displayable (уже объявленными или даже измененными изображениями)
    # так же можно добавлять любые стандартные для изображений параметры, типа масштабирования или прозрачности:
    # image neko = Ani("neko", 5, 0.5, zoom=2.0, alpha=0.75)
    def Ani(img_name, frames, delay=.1, loop=True, reverse=False, effect=Dissolve(.1, alpha=True), start=1, ext=None, **properties):
        args = []
        # если пауза переменная, то вычисляем ее шаг
        if isinstance(delay, (tuple, list)):
            d0 = delay[0]
            d1 = delay[1]
            f = (frames - 1)
            if f <= 0:
                dp = 0
            else:
                dp = (d1 - d0) * 1. / f
            delay = d0
        else:
            dp = 0
        # перебираем все кадры анимации
        for i in range(start, start + frames):
            if ext:
                img = img_name + str(i) + "." + ext
            else:
                img = img_name + str(i)
            # применяем дополнительные параметры при их наличии
            if properties:
                img = Transform(img, **properties)
            args.append(img)
            if reverse or loop or (i < start + frames - 1):
                args.append(delay)
                delay += dp
                # добавляем эффект для смены кадров
                args.append(effect)
        if reverse: # обратная анимация, если нужна
            dp = -dp
            delay += dp
            for i in range(start + frames - 2, start, -1):
                if ext:
                    img = img_name + str(i) + "." + ext
                else:
                    img = img_name + str(i)
                if properties:
                    img = Transform(img, **properties)
                args.append(img)
                if loop or (i > start + 1):
                    args.append(delay)
                    delay += dp
                    args.append(effect)
        return anim.TransitionAnimation(*args)

    # аналог AlphaMask - тоже маска, но не по альфа-каналу, а по красному
    # чёрный - прозрачный, белый - нет, при reverse=True всё наоборот
    def ImageMask(image, mask, reverse=False):
        if renpy.display.render.models:
            if not reverse:
                # Copies red -> alpha
                matrix = renpy.display.matrix.Matrix([0, 0, 0, 0,
                                                      0, 0, 0, 0,
                                                      0, 0, 0, 0,
                                                      1, 0, 0, 0, ])
            else:
                # Copies alpha-red -> alpha
                matrix = renpy.display.matrix.Matrix([0, 0, 0, 0,
                                                      0, 0, 0, 0,
                                                      0, 0, 0, 0,
                                                      -1, 0, 0, 1, ])
            mask = renpy.display.motion.Transform(mask, matrixcolor=matrix)
        else:
            if not reverse:
                # Copies red -> alpha
                matrix = renpy.display.im.matrix(
                    0, 0, 0, 0, 1,
                    0, 0, 0, 0, 1,
                    0, 0, 0, 0, 1,
                    1, 0, 0, 0, 0)
            else:
                # Copies 1-red -> alpha
                matrix = renpy.display.im.matrix(
                    0, 0, 0, 0, 1,
                    0, 0, 0, 0, 1,
                    0, 0, 0, 0, 1,
                    -1, 0, 0, 0, 1)
            mask = renpy.display.im.MatrixColor(mask, matrix)
        return AlphaMask(image, mask)

    # показать фон с именем bg указанного цвета color
    def bg(color="#000", bg="bg"):
        renpy.scene()
        renpy.show(bg, what=img2disp(color))

    # меняем стандартное время всех или некоторых эффектов для появления/исчезновения спрайтов
    def move_time(delay=.5, effects=["move", "ease"]):
        effects = make_list(effects)
        for i in effects:
            define.move_transitions(i, delay)

    # формат времени или текст
    clock_tformat = "%H:%M:%S"

    # текущее время или заданное в переменной clock_tformat
    # если нет знака %, то выводится просто текст из tformat
    # если tformat == None, то берётся формат или значение из clock_tformat
    def cur_time(tformat=None):
        if not tformat:
            tformat = clock_tformat
        if "%" in tformat:
            return datetime.datetime.now().strftime(tformat)
        return str(tformat)

    # список полных имён спрайтов на экране (а не отдельных тегов)
    def get_showing_images(layer="master"):
        images = []
        tags = renpy.get_showing_tags(layer, True)
        for i in tags:
            tag = i
            atrs = renpy.get_attributes(i, layer)
            for a in atrs:
                tag += ' ' + a
            images.append(tag)
        return images

    # найти на экране картинку, которая содержит заданный тег
    # (чтобы выделение не учитывало эмоции и прочие дополнительные теги)
    def get_showing_sprite(tag, default=None):
        # если среди всех спрайтов на экране
        images = get_showing_images()
        for i in images:
            # есть тот, что содержит нужный тэг
            if str(tag) in str(i):
                return str(i)
        # если на экране нет спрайта
        return default

    import datetime

    # для цифровых часиков (не менять, не вызывать)
    # в tformat может быть просто текст без %, если требуется не реальное время, а сюжетное
    def clock_f(st, at, tformat=None, **kwarg):
        return Text(cur_time(tformat), **kwarg), 1.

    # создать цифровые часики:
    # image clock = Clock(size=48, color="#fff8", outlines=[(2, "#0008", 0, 0)], align=(.05, .05))
    def Clock(**kwarg):
        return DynamicDisplayable(clock_f, **kwarg)

    # показать экран на слое "мастер",
    # чтобы он не исчезал, когда прячем интерфейс
    def show_s(screen, *arg, **kwarg):
        renpy.show_screen(screen, _layer="master", *arg, **kwarg)

    # убрать экран со слоя "мастер"
    def hide_s(screen, **kwarg):
        renpy.hide_screen(screen, layer="master", **kwarg)

    # показать неубирающийся по нажатию "h" экран
    def show_forever(screen):
        # добавляем неубирающийся по hide_interface слой
        if not "forever" in config.layers:
            config.layers.insert(config.layers.index("screens"), "forever")
        renpy.show_screen(screen, _layer="forever")

    # спрятать неубирающийся по нажатию "h" экран
    def hide_forever(screen):
        renpy.hide_screen(screen, layer="forever")

    # показать совсем неубирающийся по нажатию "h" экран
    def show_foreverest(screen):
        if not screen in config.always_shown_screens:
            config.always_shown_screens.append(screen)
        renpy.show_screen(screen)

    # спрятать совсем неубирающийся по нажатию "h" экран
    def hide_foreverest(screen):
        if screen in config.always_shown_screens:
            config.always_shown_screens.remove(screen)
        renpy.hide_screen(screen)

    # получить английское название времени суток
    # если не указывать время в часах,
    # то будет взято системное время
    # можно задать начало утра, дня, вечера и ночи в часах от 0 до 23
    def time_of_day(hours=None, morning=7, day=11, evening=18, night=23):
        if hours is None:
            hours = int(datetime.datetime.now().strftime("%H"))
        res = "night" # по умолчанию ночь
        # границы любого времени суток можно поменять
        if (hours >= morning) and (hours <= day):
            res = "morning"
        if (hours > day) and (hours <= evening):
            res = "day"
        if (hours > evening) and (hours < night):
            res = "evening"
        return res

    # словарь цветов для времен суток
    color_filters = {"morning": "#8404", "day": "#0000", "evening": "#0484", "night": "#000b"}

    # получить цвет фильтра, соответствующий времени суток
    def color_of_day(hours=None):
        return color_filters[time_of_day(hours)]

    # удалить все сохранения
    def delete_saves_now():
        all = renpy.list_saved_games(fast=True)
        for i in all:
            renpy.unlink_save(i)
        renpy.restart_interaction()
    DeleteSavesNow = renpy.curry(delete_saves_now)

    # удаление всех сохранений с запросом подтверждения
    def delete_saves(confirm=True):
        if confirm:
            layout.yesno_screen(message=_("Удалить все сохранения?"), yes=DeleteSavesNow(), no=NullAction())
        else:
            delete_saves_now()
    DeleteSaves = renpy.curry(delete_saves)

    # очистить постоянные данные и сохранения
    def delete_data_now(quit=False):
        # удаление сохранений
        delete_saves(False)
        # удаление ачивок
        # achievement.clear_all()
        # achievement.sync()
        # удаление постоянных данных
        persistent._clear(progress=True)
        if quit:
            renpy.quit()
    DeleteDataNow = renpy.curry(delete_data_now)

    # удаление всех данных и сохранений с запросом подтверждения
    def delete_data(confirm=True):
        if confirm:
            layout.yesno_screen(message=_("Удалить все данные?\nИгра будет закрыта."), yes=DeleteDataNow(True), no=NullAction())
    DeleteData = renpy.curry(delete_data)

    # действие - продолжить игру оттуда, где закончили
    # если загружать пока нечего, то кнопка неактивна
    # textbutton _("Продолжить игру") action Continue()
    class Continue(Action, DictEquality):
        def __call__(self):
            FileLoad(1, confirm=False, page="auto", newest=True)()
        # кликабельность кнопки
        def get_sensitive(self):
            return FileLoadable(1, page="auto")

    # объявлена ли картинка с именем name
    def has_image(name):
        for i in renpy.display.image.images:
            # такая конструкция позволяет исключить пустые теги
            if name == " ".join(" ".join(i).split()):
                return True
        return False

    # проверить существование нескольких изображений через запятую
    def has_images(*args):
        res = True
        for i in args:
            # вместо какой-то картинки может быть список или кортеж
            if isinstance(i, (list, dict)):
                res = res & has_images(i)
            else:
                res = res & has_image(i)
        return res

    # одна из картинок на входе была открыта
    def seen_one(*args):
        res = False
        for i in args:
            res |= renpy.seen_image(i)
        return res

    # все картинки на входе были открыты
    def seen_all(*args):
        res = True
        for i in args:
            res &= renpy.seen_image(i)
        return res

    # задан ли курсор с таким именем
    def has_mouse(mouse):
        if config.mouse:
            if mouse in config.mouse.keys():
                return True
        return False

    # рандомный элемент из параметров на входе
    # просто сокращаем писанину
    def rnds(*args):
        return renpy.random.choice(args)

    # рандомное целое число в заданных пределах
    # второй предел НЕ включительно, как в питоне
    # (i_to можно не указывать, тогда максимум берется из i_from)
    def rnd(i_from=0, i_to=None):
        if i_to is None:
            i_to = i_from
            i_from = 0
        i_from = int(i_from)
        i_to = int(i_to)
        i_from, i_to = min(i_from, i_to), max(i_from, i_to)
        return renpy.random.randint(i_from, i_to - 1)

    # рандомное дробное число в заданных пределах
    # (f_to можно не указывать, тогда максимум берется из f_from)
    def rndf(f_from=0, f_to=None):
        if f_to is None:
            f_to = f_from
            f_from = .0
        return f_from + renpy.random.random() * (f_to - f_from)

    # канал для зацикленного эффекта
    renpy.music.register_channel("effect", "sfx", loop=True, tight=True)

    # зацикленный звуковой эффект, не музыка
    def sfxplay(name, channel="effect", loop=True, fadein=default_fade, fadeout=default_fade, ext="ogg", audio_dir=audio_dir):
        if name:
            renpy.music.play(add_ext(audio_dir + "/" + name, ext), channel=channel, loop=loop, fadein=fadein, fadeout=fadeout)

    # костыли для звуков и музыки - сокращают писанину
    # можно запускать музыку или звуки, не указывая папки и расширения
    # по умолчанию для музыки music/*.ogg
    # по умолчанию для звуков audio/*.ogg

    # запустить музыку или плейлист
    def mplay(mname, fadein=default_fade, fadeout=default_fade, loop=True, channel="music", ext="ogg"):
        lst = []
        mname = make_list(mname)
        for i in mname:
            lst.append(add_ext(music_dir + "/" + i, ext))
        renpy.music.play(lst, channel=channel, loop=loop, fadein=fadein, fadeout=fadeout)

    # запустить музыку или случайно перемешанный плейлист
    def rndplay(mname, fadein=default_fade, fadeout=default_fade, loop=True, channel="music", ext="ogg"):
        lst = make_list(mname)
        if len(lst) > 1:
            renpy.random.shuffle(lst)
        mplay(lst, fadein, fadeout, loop, channel, ext)

    # перезапустить музыку, даже если уже играет она же
    def mreplay(mname, fadein=default_fade, fadeout=default_fade, loop=True, channel="music", ext="ogg"):
        new_fn = add_ext(music_dir + "/" + mname, ext)
        renpy.music.play(new_fn, channel=channel, loop=loop, fadein=fadein, fadeout=fadeout)

    # убрать из строки теги типа <from 0.2>
    def mdeletetags(str):
        return re.sub(re.compile('<.*?>'), '', str)

    # запустить музыку для имени файла и пути
    def fnplay(new_fn, fadein=default_fade, fadeout=default_fade, channel="music", loop=True, if_changed=False):
        old_fn = renpy.music.get_playing()
        renpy.music.play(new_fn, channel=channel, loop=loop, fadein=fadein, fadeout=fadeout, if_changed=if_changed)

    # последняя сохраненная мелодия
    last_music_fn = ""

    # сохранить в памяти играющую мелодию
    def msave():
        store.last_music_fn = renpy.music.get_playing()

    # восстановить игравшую при сохранении мелодию
    def mrestore(fadein=default_fade, fadeout=default_fade, channel="music"):
        if last_music_fn:
            fnplay(last_music_fn, fadein=fadein, fadeout=fadeout, channel=channel)

    # добавить расширение, если такого нет
    def add_ext(fn, ext="ogg"):
        if not fn.endswith("." + ext):
            fn = fn + "." + ext
        return fn

    # воспроизвести звук для канала audio, который поддерживает многопоточность
    def splay(mname, fadein=0, fadeout=0, channel=config.play_channel, ext="ogg", audio_dir=audio_dir):
        if mname:
            mname = make_list(mname)
            lst = []
            for i in mname:
                lst.append(add_ext(audio_dir + "/" + i, ext))
            renpy.play(lst, channel=channel, fadein=fadein, fadeout=fadeout)

    # воспроизвести звук
    def sndplay(mname, fadein=0, fadeout=0, channel="sound", ext="ogg", audio_dir=audio_dir):
        if mname:
            mname = make_list(mname)
            lst = []
            for i in mname:
                lst.append(add_ext(audio_dir + "/" + i, ext))
            renpy.play(lst, channel=channel, fadein=fadein, fadeout=fadeout)

    # голос
    def vplay(mname, fadein=0, fadeout=0, channel="voice", ext="ogg"):
        if mname:
            renpy.play(add_ext("voices/" + mname, ext), channel=channel, fadein=fadein, fadeout=fadeout)

    # остановить звук
    def sstop(fadeout=None, channel='audio'):
        renpy.music.stop(channel=channel, fadeout=fadeout)

    # остановить звук
    def sndstop(fadeout=0, channel='sound'):
        renpy.music.stop(channel=channel, fadeout=fadeout)

    # остановить музыку
    def mstop(fadeout=default_fade, channel='music'):
        renpy.music.stop(channel=channel, fadeout=fadeout)

    # остановить зацикленный эффект
    def sfxstop(fadeout=default_fade, channel='effect'):
        renpy.music.stop(channel=channel, fadeout=fadeout)

    # превращаем функции в action для экранов screen
    SPlay = renpy.curry(splay)
    SFXPlay = renpy.curry(sfxplay)
    SFXStop = renpy.curry(sfxstop)
    MPlay = renpy.curry(mplay)
    FNPlay = renpy.curry(fnplay)
    VPlay = renpy.curry(vplay)
    SStop = renpy.curry(sstop)
    MStop = renpy.curry(mstop)

    # для воспроизведения звуков картинками, пример:
    # image tree:
        # "tree"
        # function renpy.curry(s_play)("creak")
    def s_play(sound, trans, st, at):
        if sound:
            splay(sound)

    # для воспроизведения лупов картинками
    def sfx_play(sound, trans, st, at):
        if sound:
            sfxplay(sound)

    def sfx_stop(trans, st, at):
        sfxstop()

    S_Play = renpy.curry(splay)
    SFX_Play = renpy.curry(sfxplay)

    # удалить из 2D-массива пустые ряды и колонки
    def blank_list(a):
        def transpose(grid):
            return zip(*grid)

        def del_blank_rows(grid):
            return [list(row) for row in grid if any(row)]

        return del_blank_rows(transpose(del_blank_rows(transpose(a))))

    import re

    # получить словарь с найденными в строке тегами и их значением
    # недостаток: после = не может быть другого =
    def get_tags(text, prefix='#'):
        res = {}
        # выуживаем все теги ремарок
        tags = re.findall('{' + prefix + '([^}]+)}', text)
        # перебираем полученные теги
        for i in tags:
            parts = i.split('=')
            if len(parts) > 0:
                key = parts[0].strip()
                val = None
                if len(parts) > 1:
                    val = parts[1]
                # добавляем тэг и его значение в словарь
                res[key] = val
        # возвращаем значения тэгов в виде словаря
        return res

    # убрать все тэги из строки (по умолчанию убрать только теги, начинающиеся с prefix)
    from renpy.text.textsupport import PARAGRAPH, TAG #, DISPLAYABLE
    import renpy.text.textsupport as textsupport
    def del_tags(s, prefix="#"):
        if s is None:
            return None

        tokens = textsupport.tokenize(str(s))

        rv = [ ]

        for tokentype, text in tokens:

            if tokentype == PARAGRAPH:
                rv.append("\n")

            elif tokentype == TAG:
                kind = text.partition("=")[0]

                if kind and (kind[0] == "/"):
                    kind = kind[1:]

                if not prefix:
                    rv.append("{" + text + "}")

                else:
                    k, v = get_key_val(text)
                    k = k.strip()
                    if not k.startswith(prefix):
                        rv.append("{" + text + "}")

            else:
                rv.append(text.replace("{", "{{"))

        return "".join(rv)

    # удаление всех текстовых тегов функцией ренпая
    def del_all_tags(txt):
        return renpy.filter_text_tags(txt, allow=[ ])

    # получить тэги и вернуть их в виде списка строк
    def get_tags_str(text, prefix='#'):
        # выуживаем все теги ремарок
        return re.findall('{' + prefix + '([^}]+)}', text)

    # разделить строку на две части - до и после знака равно
    # (или другого разделителя) и убрать пробелы вокруг этих частей
    def get_key_val(text, sep='='):
        txt = text.split(sep, 1)
        val, key = None, None
        if len(txt) > 0:
            key = txt[0].strip()
        if len(txt) > 1:
            val = txt[1].strip()
        return key, val

    # поиск в строке значения невидимого читателю тега
    # пример использования:
    # $ text = "Текст текст {#image=logo.png} текст."
    # $ img = get_tag(text, 'image')
    # на выходе в img будет logo.png
    # недостаток: после = не может быть другого =
    def get_tag(text, tag, default=None, prefix='#'):
        tag = tag.strip()
        tags = get_tags(text, prefix)
        if tag in tags.keys():
            return tags[tag]
        return default

    # есть ли тэг в строке
    # недостаток: после = не может быть другого =
    def has_tag(text, tag, prefix='#'):
        return tag in get_tags(text, prefix).keys()

    # получить список с кортежами тегов и их значений "{tag=value}" -> [ (tag, value) ]
    def get_tags_list(s):
        res = [ ]
        opened = False
        key = False
        if s:
            for i in s:
                if i == "{":
                    opened, key = True, True
                    k, v = "", ""
                elif i == "}":
                    opened = False
                    if k:
                        res.append((k.strip(), v.strip()))
                    k, v = "", ""
                elif opened:
                    if key:
                        if i == "=":
                            key = False
                        else:
                            k = k + i
                    else:
                        v = v + i
        return res

    # получить значение первого тега равного tag
    # если не найден тег, то можно задать значение по умолчанию
    # а если это строка типа "eval(выражение)", то выполняем код и возвращаем значение выражения
    def get_tag_first(s, tag, default=None):
        for k, v in get_tags_list(s):
            if k == tag.strip():
                if isinstance(v, (str, unicode)):
                    vv = str(v.strip())
                    if vv.startswith("eval(") and vv.endswith(")"):
                        vv = str(vv[5:-1])
                        if vv:
                            v = eval(vv)
                return v
        return default

    # выполняется ли условие в теге
    def tag_if(s, tag="#if", default=True):
        res = default
        if get_tag_first(s, tag):
            res = eval(str(get_tag_first(s, tag)))
        return res

    # узнать имя переменной
    import inspect
    def get_var_name(var, default=""):
        for i in reversed(inspect.stack()):
            names = [var_name for var_name, var_val in i.frame.f_locals.items() if var_val is var]
            if len(names) > 0:
                return names[0]
        return default

    # нужно включить автоматические сохранения, чтобы работала Continue
    config.has_autosave = True

    # список спрайтов на экране (не только тегов)
    def get_showing_sprites(layer='master'):
        images = []
        tags = renpy.get_showing_tags(layer, True)
        for i in tags:
            tag = i
            atrs = renpy.get_attributes(i, layer)
            for a in atrs:
                tag += " " + a
            images.append(tag)
        return images

    # получить из словаря значение с защитой от дурака
    def get_by_key(key, dict):
        if key in dict.keys():
            return dict[key]
        return None

    # показан ли спрайт на экране
    def sprite_showed(image, layer='master'):
        return image in get_showing_sprites(layer)

    # найти на экране спрайт, содержащий тег
    def get_sprite_by_tag(tag, layer='master'):
        if tag:
            # если среди всех спрайтов на экране
            images = get_showing_sprites(layer)
            for i in images:
                # есть тот, что содержит нужный тэг
                if str(tag) in str(i):
                    return str(i)
        # если на экране нет говорящего персонажа
        return None

    # получить параметры спрайта
    def get_sprite_bounds(tag, layer="master"):
        # ищем спрайт на экране
        spr = get_sprite_by_tag(tag, layer)
        # если спрайт на экране
        if spr:
            x, y, w, h = renpy.get_image_bounds(spr, layer=layer)
            return int(x), int(y), int(w), int(h)
        # если не нашли спрайт
        return None, None, None, None

    # текст между скобками/кавычками и пр.
    def get_between(s, b1="(", b2=")"):
        return s[s.find(b1) + 1: s.find(b2)]

    # полное копирование
    import copy as dcopy
    def copy(*args):
        return dcopy.deepcopy(*args)

    # входит ли в строку where подстрока what
    # или одна из подстрок, если what - список или кортеж
    def has_text(where, what):
        if isinstance(what, (str, unicode)):
            what = [what]
        for i in what:
            if i in where:
                return True
        return False

    # существует ли переменная с заданным именем
    def has_val(key):
        return key in globals().keys()

    # действие для кнопок слотов (позволяет сохранять последний текст из текстбокса)
    # но тогда его нужно подрезать по размерам
    # text FileSaveName(slot) style "slot_name_text" at crop(0, 0, config.thumbnail_width, gui.text_size + 4)
    def MyFileAction(name, page=None, **kwargs):
        global save_name
        if renpy.get_screen("load"):
            return FileLoad(name, page=page, **kwargs)
        else:
            # перед сохранением удаляются все теги
            s = del_tags(_last_say_what, "")
            if not s:
                s = ". . ."
            save_name = s
            return FileSave(name, page=page, **kwargs)

# создаём трансформ для мигалки на основе шейдера градиента
# t - время смены цвета, b - яркость
transform flasher(t=.25, b1=1, b2=.25):
    truecenter
    shader "example.gradient"
    parallel:
        ease t u_gradient_left (b1, b2, b2, 1)
    parallel:
        ease t u_gradient_right (b2, b2, b1, 1)
    pass
    parallel:
        ease t u_gradient_right (b1, b2, b2, 1)
    parallel:
        ease t u_gradient_left (b2, b2, b1, 1)
    pass
    repeat

# отключить мигалку (он же - стартовая инициализация)
transform flasher_off(t=.5):
    parallel:
        ease t u_gradient_left (1, 1, 1, 1)
    parallel:
        ease t u_gradient_right (1, 1, 1, 1)

# БЛОК ДЛЯ РАБОТЫ С ВРЕМЕНАМИ СУТОК
# как пользоваться:

# 1) если есть нужные рисунки, то назвать файлы по временам суток:
# bg_street_night, bg_street_morning и т.д. по списку
# в противном случае будет перекрашиваться основная картинка
# например, "bg street day" или скопированная в неё "bg street"
# первый суффикс в списке времён суток можно и не указывать: bg street

# 2) воспользоваться автоматическим объявлением спрайтов в блоке init:
# $ images_auto()

# 3) указать перфиксы спрайтов, которые будут зависеть от времени суток
# например, чтобы все фоны и все спрайты eileen и pytom зависели от времени суток:
# daytime_prefix = ["bg", "eileen", "pytom"]

# 4) при необходимости задать список времён суток, по умолчанию он:
# alldaytime = ["day", "night"]

# 5) в скрипте просто задавать время суток $ setdaytime("night")
# или переключение на следующее по списку (зациклено): $ setdaytime()
# спрайты на экране сразу поменяются

init -222:
    # настройки нового освещения, на входе сразу матрица
    transform daytime_light(matrix):
        matrixcolor matrix

    transform daytime_empty():
        pass

    # привязать положение какого-нибудь объекта к курсору
    # якорь всегда в центре
    transform xy_at:
        function xy_at_f

init -99 python:

    # узнать имя и цвет персонажа
    def get_name_color(char, color=None):
        if color is None:
            color = gui.accent_color

        col = color

        if isinstance(char, (str, unicode)):
            name = char
        else:
            name = char.name

            for arg in [ "color", "who_color" ]:
                if arg in char.who_args.keys():
                    col = char.who_args[arg]

        return name, col

    # если не существует персонажа Character из переменной ch,
    # то получаем текст с форматированием под имя
    # пример:
    # "[CH(unit.caption)] не хочет общаться..."
    def CH(ch, tag=True):
        name, color = get_name_color(ch, gui.accent_color)

        if isinstance(ch, (str, unicode)) or tag:
            return "%s{color=%s}%s{/color}%s" % ("{font=" + gui.name_text_font + "}", color, name, "{/font}")

        else:
            return ch

    # список допустимых времён суток
    # "night" - обязательно!
    alldaytime = ["day", "night"]

    # список префиксов-меток для динамических спрайтов,
    # освещение которых будет зависеть от времени суток в curdaytime
    # например, все фоны и пара героев:
    # daytime_prefix = ["bg", "eileen", "pytom"]
    # к таким именам будет добавлен суффикс из daytime_suffix
    # а потом они будут превращены в динамические уже со своими именами без суффикса
    daytime_prefix = []

    # настройки каждого времени суток для перекрашивания фонов и спрайтов
    # (color, brightness, saturation, contrast)
    day_bg_attrs = ("#000", 0, 1, 1)
    day_attrs = ("#000", 0, 1, 1)
    evening_bg_attrs = ("#9af", -.2, .8, 1)
    evening_attrs = ("#9af", 0, .9, 1)
    night_bg_attrs = ("#9af", -.475, .375, .575)
    night_attrs = ("#9af", -.1, .375, 1)
    morning_bg_attrs = ("#fca", .1, 1, 1)
    morning_attrs = ("#fca", .1, 1, 1)

    # по умолчанию первое в списке время суток
    curdaytime = alldaytime[0]

    # суффикс для динамических спрайтов - первое в списке время суток
    daytime_suffix = alldaytime[0]

    # здесь будут храниться имена изменённых спрайтов, зависимых от curdaytime
    daytime_suffixed = []

    # префикс-метка для фонов
    bg_prefix = "bg"

    # переключение времени суток на новое или на следующее, если не указывать, на какое
    def setdaytime(newdaytime=None, effect=dissolve):
        if newdaytime is None:
            # если новое время суток == None,
            # то переключаемся на следующее в списке (по кругу)
            i = alldaytime.index(curdaytime) + 1
            if i >= len(alldaytime):
                i = 0
            newdaytime = alldaytime[i]
        if effect:
            renpy.show("black", tag="daytimeblack")
            renpy.with_statement(effect)
        store.curdaytime = newdaytime
        if effect:
            renpy.hide("daytimeblack")
            renpy.with_statement(effect)

    # получить трансформ с матрицей для ночного освещения
    # по умолчанию для спрайта, True - для фона
    def atdaytime(bg=False):
        if bg:
            key = "_" + bg_prefix + "_"
        else:
            key = "_"
        key = curdaytime + key + "attrs"
        attrs = ("#000", 0, 1, 0)
        if key in globals().keys():
            color, brightness, saturation, contrast = globals()[key]
            matrix = BrightnessMatrix(brightness) * ContrastMatrix(contrast) * TintMatrix(color) * SaturationMatrix(saturation)
            return daytime_light(matrix)
        return daytime_empty()

    # все поддерживаемые расширения картинок
    all_image_extensions = [ ".png", ".jpg", ".jpeg", ".webp" ]

    # все поддерживаемые расширения видео
    all_video_extensions = [ ".webm", ".ogv", ".mp4" ]

    # получить расширение из тех, что есть на входе, на которое оканчивается строка s
    # case=False - нечувствительно к регистру
    def endswith(s, exts=None, case=False):
        if exts is None:

            exts = all_image_extensions
        for i in exts:
            t = s if case else s.lower()

            if t.endswith(i):
                return i
        return None

# БЛОК ДЛЯ ДОПОЛНЕННОГО АВТООБЪЯВЛЕНИЯ СПРАЙТОВ
# стандартное автообъявление картинок, но с webp
# плюс не разбиваются на теги имена, предназначенные для LayerdImage
# вместо этого объединяются через нижний минус "_"
# префиксы, по которым определяются такие имена берутся из layered_prefixes
# выполняется после всего остального
init 1900 python hide:
    def create_automatic_images():

        seps = config.automatic_images

        if seps is True:
            seps = [ ' ', '/', '_' ]

        for dir, fn in renpy.loader.listdirfiles():

            if fn.startswith("_"):
                continue

            # только .png и .jpg и .jpeg и .webp
            if not endswith(fn) and not endswith(fn, all_video_extensions):
                continue

            # убираем расширения и заменяем слеши.
            ext = endswith(fn, all_image_extensions + all_video_extensions)
            shortfn = fn[:-len(ext)].replace("\\", "/")

            # делим строку на части
            name = ( shortfn, )
            for sep in seps:
                name = tuple(j for i in name for j in i.split(sep))

            # выбрасываем имя папок из тегов
            while name:
                for i in config.automatic_images_strip:
                    if name[0] == i:
                        name = name[1:]
                        break
                else:
                    break

            # для проверки префиксов и суффиксов после
            # возможной склейки тегов
            prefix = name[0]
            suffix = name[len(name) - 1]

            # убираем суффикс, если это первое время суток
            if suffix == daytime_suffix:
                name = name[:-1]

            # имя без суффикса
            name0 = name

            # теги одной строкой
            sname = " ".join(name)

            # не делим на части имена, которые начинаются с префиксов для LayeredImage
            layered = False
            if prefix in layered_prefixes:
                name = "_".join(name)
                sname = name
                layered = True

            # добавляем суффикс по умолчанию, если начинается
            # с префикса из списка меток для динамических спрайтов,
            # которые будут менять освещение в зависимости от времени суток
            if prefix in daytime_prefix:
                # нельзя автоматизировать файлы с суффиксами времён суток,
                # потому что они станут частью автоматизированного спрайта
                if not suffix in alldaytime[1:]:
                    if not sname in daytime_suffixed:
                        # запоминаем имя изменённого спрайта
                        store.daytime_suffixed.append(sname)
                        # добавляем суффикс
                        if layered:
                            name = name + " " + daytime_suffix
                        else:
                            name = name + (daytime_suffix,)
                            # name = (*name, daytime_suffix)

            # игнорируем, если уже создана одноимённая копия с суффиксом
            if name0 in daytime_suffixed:
                continue

            # игнорируем, если не набирается указанное в переменной количество тегов
            if len(name) < config.automatic_images_minimum_components:
                continue

            # игнорируем, если такой спрайт уже есть
            if name in renpy.display.image.images:
                continue

            # если тег один, но требуется для многослойных картинок, то добавляем в конце "_"
            if layered and not "_" in name:
                name = name + "_"

            # объявляем видео-спрайт
            if ext in all_video_extensions:
                renpy.image(name, Movie(play=fn))
            # объявляем обычный спрайт
            else:
                renpy.image(name, fn)

    # если заданы параметры, то объявляем спрайты автоматом
    if config.automatic_images:
        create_automatic_images()

    # функция для динамического освещения спрайтов и фонов
    def def_daytime(st, at, img):
        # ищем картинку для текущего времени суток
        new = img + " " + curdaytime
        if has_image(new):
            return new, None
        # если не нашли, то берем основную
        new = img + " " + daytime_suffix
        # и перекрашиваем в соответствии с настройками
        if img.startswith(bg_prefix):
            return At(new, atdaytime(True)), None
        return At(new, atdaytime()), None

    # если заданы параметры, то создаём динамически освещённые спрайты
    if len(daytime_suffixed) > 0:
        # перебираем все спрайты, для которых нужна реакция на освещение
        for i in daytime_suffixed:
            # создаём такие спрайты
            renpy.image(i, DynamicDisplayable(def_daytime, i))
