## Vendored 7dots из renpy_7dots_tools/test_parallax_mm.
## Не заменять без миграции и smoke-тестов проекта.
# Linux-safe замена str().

define mystr = eval("lambda i: '%s' % i")

init -999 python:
    # Дополнительные команды, скрывающие textbox при config.window="auto".
    def auto_hide(cmd_list=[ "pause", "hide", "with", "scene", "call", "show screen", "screen", "menu", "renpy.pause"]):
        for i in cmd_list:
            if not i in config.window_auto_hide:
                config.window_auto_hide.append(i)

    # Совместимость целочисленного деления с новыми Ren'Py.
    def d2(x, d=2):
        return int(x / d)

    def sec_to_hms(s):
        m, s = divmod(s, 60)
        h, m = divmod(m, 60)
        if h > 0:
            return '{}:{:0>2}:{:0>2}'.format(h, m, s)
        return '{:0>2}:{:0>2}'.format(m, s)

    clip = lambda i, mini, maxi: max(min(maxi, i), mini)

    def fint(x, default=0):
        try:
            x = int(x)
            return x
        except:
            try:
                x = float(x)
                return x
            except:
                return default

    # Префиксы LayeredImage, чьи теги соединяются через "_".
    layered_prefixes = []

    default_fade = 1.5

init:
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

    # При смене только эмоции сохраняем направление перехода.
    transform side_same(old, new):
        contains:
            old
            new with Dissolve(.25, alpha=True, mipmap=True)

init -222:
    transform show_hide(t=.25):
        on show:
            alpha 0
            linear t alpha 1
        on hide:
            linear t alpha 0

    # Hover-transform требует центральный anchor и конфликтует с другими at.
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

    # Переход для with; аналог leap с центральным anchor.
    transform zpunch(old_widget=None, new_widget=None, dt=.5, dyz=.05, dxz=.05, align=(.5, .5), anchor=(.5, .5)):
        delay dt

        contains:
            new_widget
            anchor anchor
            align align
            subpixel True
            xzoom 1 yzoom 1
            easein dt*.25 yzoom 1+dyz xzoom 1+dxz/2.
            easeout dt*.25 yzoom 1 xzoom 1
            easein dt*.15 yzoom 1+dyz/2. xzoom 1+dxz
            easeout dt*.15 yzoom 1 xzoom 1
            easein dt*.1 yzoom 1+dyz/4. xzoom 1+dxz/2
            easeout dt*.1 yzoom 1 xzoom 1

        # Старый кадр быстро гаснет при смене изображения.
        contains:
            # Flatten предотвращает просвечивание слоёв.
            Flatten(old_widget)
            alpha 1
            ease .15 alpha 0

    transform breath(t=2, dz=.005):
        subpixel True

        yalign 1.
        ease t*.5 yzoom 1-dz
        ease t*.5 yzoom 1
        repeat

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

    transform alpha(alpha=1.):
        alpha alpha
    transform alphing(alpha1=0, alpha2=1, t=1):
        alpha alpha1
        ease t alpha alpha2

    transform blur(blur=4):
        blur blur
    transform bluring(blur1=0, blur2=16, t=1):
        blur blur1
        ease t blur blur2

    transform brightness(brightness=.25):
        matrixcolor BrightnessMatrix(brightness)

    transform brightnessing(brightness1=0, brightness2=.25, t=2):
        matrixcolor BrightnessMatrix(brightness1)
        ease t matrixcolor BrightnessMatrix(brightness2)

    transform contrast(contrast=1.25):
        matrixcolor ContrastMatrix(contrast)

    transform contrasting(contrast1=1, contrast2=1.25, t=2):
        matrixcolor ContrastMatrix(contrast1)
        ease t matrixcolor ContrastMatrix(contrast2)

    transform saturation(saturation=1.):
        matrixcolor SaturationMatrix(saturation)

    transform saturationing(saturation1=1., saturation2=.5, t=2):
        matrixcolor SaturationMatrix(saturation1)
        ease t matrixcolor SaturationMatrix(saturation2)

    transform color(color_="#000"):
        matrixcolor TintMatrix(color_)

    transform coloring(color1="#fff", color2="#fff", t=2):
        matrixcolor TintMatrix(color1)
        ease t matrixcolor TintMatrix(color2)

    transform color2(color1="#fff", color2="#def", t=2):
        matrixcolor TintMatrix(color1)
        ease_quad t*.5 matrixcolor TintMatrix(color2)
        ease_quad t*.5 matrixcolor TintMatrix(color1)
        repeat

    transform paint(color_="#fff"):
        matrixcolor TintMatrix(color_) * InvertMatrix(1.) * TintMatrix("#000")

    transform painting(color1="#fff", color2="#fff", t=2):
        matrixcolor TintMatrix(color1) * InvertMatrix(1.) * TintMatrix("#000")
        ease t matrixcolor TintMatrix(color2) * InvertMatrix(1.) * TintMatrix("#000")

    transform paint2(color1="#fff", color2="#def", t=2):
        matrixcolor TintMatrix(color1) * InvertMatrix(1.) * TintMatrix("#000")
        ease_quad t*.5 matrixcolor TintMatrix(color2) * InvertMatrix(1.) * TintMatrix("#000")
        ease_quad t*.5 matrixcolor TintMatrix(color1) * InvertMatrix(1.) * TintMatrix("#000")
        repeat

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

    transform xysize(width, height):
        xysize (width, height)
    transform xsize(width):
        xsize width
    transform ysize(height):
        ysize height

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

    transform xysize(width=config.screen_width, height=config.screen_height):
        xysize(width, height)
    transform xsize(width=config.screen_width):
        ysize width
    transform ysize(height=config.screen_height):
        ysize height

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

    transform xanchor(xanchor=.5):
        xanchor xanchor
    transform yanchor(yanchor=1.):
        yanchor yanchor
    transform anchor(xanchor=.5, yanchor=1.):
        anchor (xanchor, yanchor)
    transform anchoring(xanchor1=.5, yanchor1=.5, xanchor2=.5, yanchor2=.5, t=1):
        anchor (xanchor1, yanchor1)
        ease t anchor (xanchor2, yanchor2)

    transform hflip:
        subpixel True
        xzoom -1
    transform vflip:
        subpixel True
        yzoom -1

    transform rotate(a=45, rotate_pad=False):
        subpixel True
        rotate_pad rotate_pad
        rotate a
    transform rotating(a1=0, a2=360, t=1, rotate_pad=False):
        subpixel True
        rotate_pad rotate_pad
        rotate a1
        ease t rotate a2

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

    transform crop(x=0, y=0, w=1., h=1.):
        crop(x, y, w, h)

    transform leap(dt=.25, dyz=.01, dxz=.005):
        subpixel True
        xzoom 1 yzoom 1
        easein dt*.35 yzoom 1+dyz xzoom 1-dxz
        easeout dt*.35 yzoom 1 xzoom 1
        easein dt*.15 yzoom 1-dyz xzoom 1+dxz
        easeout dt*.15 yzoom 1 xzoom 1

    transform left2(xa=.35):
        anchor (.5, 1.)
        align(xa, 1.)

    transform right2(xa=.65):
        anchor (.5, 1.)
        align(xa, 1.)

    transform left0():
        anchor (1., 1.)
        pos (.0, 1.)

    transform right0():
        anchor (1., 1.)
        pos (1., 1.)

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
    def_list_sound = None

init python:
    # Dummy сохраняет совместимость transition со старыми Ren'Py.
    def TurnPage(delay=.5, vertical=False, reverse=False, new_widget=None, old_widget=None):
        return ComposeTransition(CropMove(delay, mode="custom", startcrop=(.0, .0, .0, .0), startpos=(.0, .0), endcrop=(.0, .0, .0, .0), endpos=(.0, .0)), before=TurnPageAt(delay, vertical, reverse, new_widget, old_widget))

    turn2left = TurnPage()
    turn2right = TurnPage(reverse=True)
    turn2up = TurnPage(vertical=True, reverse=True)
    turn2down = TurnPage(vertical=True)

# Начальное состояние блокировки пропуска реплик.
default can_dismiss = True

init -222 python:
    def str_cut(s, max_len=11, dots="…", allow=[ ]):
        s = renpy.filter_text_tags(s, allow=allow)
        return s[:max_len] + dots if len(s) > max_len and len(s) > 0 and max_len > 0 else s

    def get_input_text(screen="input", id="input"):
        widget = renpy.get_widget(screen=screen, id=id)
        if widget:
            return str(widget.content)
        return None

    def prev_x(x, lst):
        i = lst.index(x) if x in lst else len(lst)
        i = (i - 1) % len(lst)
        return lst[i]

    def next_x(x, lst):
        i = lst.index(x) if x in lst else -1
        i = (i + 1) % len(lst)
        return lst[i]

    def lang(language="next"):
        lst = [None] + list(renpy.known_languages())
        if language == "next":
            language = next_x(_preferences.language, lst)
        if language in lst:
            renpy.change_language(language)
    Lang = renpy.curry(lang)

    CPS = preferences.text_cps

    def cps_save():
        global CPS
        CPS = preferences.text_cps

    def cps_get():
        return preferences.text_cps

    def cps_set(cps):
        preferences.text_cps = cps

    def cps_restore():
        preferences.text_cps = CPS

    def skip_once():
        renpy.end_interaction(True)
    SkipOnce = renpy.curry(skip_once)

    def skip_stop():
        renpy.config.skipping = None
    SkipStop = renpy.curry(skip_stop)

    def dismiss_block():
        return store.can_dismiss

    # Не затираем callback, установленный проектом до 7dots.
    if config.say_allow_dismiss is None:
        config.say_allow_dismiss = dismiss_block

    def dismiss_on():
        store.can_dismiss = True
    DismissOn = renpy.curry(dismiss_on)

    def dismiss_off():
        store.can_dismiss = False
    DismissOff = renpy.curry(dismiss_off)

    def log(*args):
        for i in args:
            print(str(i))
    Log = renpy.curry(log)

    def Flash(color="#fff", t=1):
        return Fade(t*.3, t*.1, t*.6, color=color)

    flash = Flash()

    def has_screen(*args, **kwarg):
        if not "layer" in kwarg.keys():
            layer = None
        else:
            layer = kwarg["layer"]
        args = make_list(args)
        for i in args:
            if renpy.get_screen(i, layer):
                return True
        return False

    def screen_exists(name):
        for i in renpy.config.variants:
            if renpy.display.screen.screens.get((name, i), None) is not None:
                return True
        return False

    def showhide(screen, effect=dissolve):
        if has_screen(screen):
            renpy.hide_screen(screen)
        else:
            renpy.show_screen(screen)
        renpy.transition(effect)
        renpy.restart_interaction()
    ShowHide = renpy.curry(showhide)

    audio_dir = "audio/sfx"
    music_dir = "audio/music"
    voice_dir = "audio/voice"

    def pause(t=1, hard=True):
        renpy.pause(t, hard=hard)

    def shot(w=config.screen_width, h=config.screen_height):
        renpy.take_screenshot((w, h))
        renpy.restart_interaction()
        return FileCurrentScreenshot()

    def get_music_list(folder=music_dir, ext="ogg"):
        res = []
        lst = renpy.list_files()
        for i in lst:
            if str(i).startswith(str(folder)):
                s = i[(len(folder) + 1):]
                if s.endswith("." + ext):
                    res.append(s[:(-len(ext) - 1)])
        return res

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
            res = sorted(res, key=lambda s: s.lower())
        return res

    def window_center():
        import os
        os.environ['SDL_VIDEO_CENTERED'] = '1'

    def images_auto(folders=[ "images" ], spaces=[ ' ', '_', '/' ], minimum=1):
        config.automatic_images_strip = folders
        config.automatic_images = spaces
        config.automatic_images_minimum_components = minimum

    def stop_skip():
        renpy.config.skipping = None

    def img2disp(displayable):
        if isinstance(displayable, (str, unicode)):
            return renpy.displayable(displayable)
        return displayable

    # Render-размер displayable; недоступен в init.
    def get_size(displayable):
        w, h = renpy.render(img2disp(displayable), config.screen_width, config.screen_height, 0, 0).get_size()
        return int(w), int(h)
    def get_width(displayable):
        return get_size(displayable)[0]
    def get_height(displayable):
        return get_size(displayable)[1]

    def get_opaque(img, x=None, y=None):
        r = renpy.render(renpy.displayable(img), 0, 0, 0, 0)
        w, h = get_size(img)
        w, h = int(w), int(h)
        if x is None:
            x = w - 1
        if y is None:
            y = h - 1
        return r.is_pixel_opaque(x, y)

    def is_opaque(img, x=None, y=None, min_a=0):
        a = get_opaque(img, x, y)
        return a > min_a

    def make_list(param):
        if param is None:
            return None
        if not isinstance(param, list):
            param = [param]
        return param

    def xy_at_f(trans, st, at):
        x, y = renpy.get_mouse_pos()
        trans.anchor = (.5, .5)
        trans.xpos, trans.ypos = int(x), int(y)
        return 1/30.

# Автообъявление покадровой анимации; ext=None использует displayable.
    def Ani(img_name, frames, delay=.1, loop=True, reverse=False, effect=Dissolve(.1, alpha=True), start=1, ext=None, **properties):
        args = []
        # Tuple delay задаёт диапазон скоростей по кадрам.
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
        for i in range(start, start + frames):
            if ext:
                img = img_name + str(i) + "." + ext
            else:
                img = img_name + str(i)
            if properties:
                img = Transform(img, **properties)
            args.append(img)
            if reverse or loop or (i < start + frames - 1):
                args.append(delay)
                delay += dp
                args.append(effect)
        if reverse:
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

    # AlphaMask по красному каналу; reverse инвертирует маску.
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

    def bg(color="#000", bg="bg"):
        renpy.scene()
        renpy.show(bg, what=img2disp(color))

    def move_time(delay=.5, effects=["move", "ease"]):
        effects = make_list(effects)
        for i in effects:
            define.move_transitions(i, delay)

    clock_tformat = "%H:%M:%S"

    # Без % значение выводится буквально; None использует clock_tformat.
    def cur_time(tformat=None):
        if not tformat:
            tformat = clock_tformat
        if "%" in tformat:
            return datetime.datetime.now().strftime(tformat)
        return str(tformat)

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

    def get_showing_sprite(tag):
        images = get_showing_images()
        for i in images:
            if str(tag) in str(i):
                return str(i)
        return None

    import datetime

    # Внутренний callback Clock; напрямую не вызывать.
    def clock_f(st, at, tformat=None, **kwarg):
        return Text(cur_time(tformat), **kwarg), .25

    def Clock(**kwarg):
        return DynamicDisplayable(clock_f, **kwarg)

    # Экраны на master не скрываются вместе с интерфейсом.
    def show_s(screen, *arg, **kwarg):
        renpy.show_screen(screen, _layer="master", *arg, **kwarg)

    def hide_s(screen, **kwarg):
        renpy.hide_screen(screen, layer="master", **kwarg)

    # Экраны, не скрываемые клавишей h.
    def show_forever(screen):
        if not "forever" in config.layers:
            config.layers.insert(config.layers.index("screens"), "forever")
        renpy.show_screen(screen, _layer="forever")

    def hide_forever(screen):
        renpy.hide_screen(screen, layer="forever")

    def show_foreverest(screen):
        if not screen in config.always_shown_screens:
            config.always_shown_screens.append(screen)
        renpy.show_screen(screen)

    def hide_foreverest(screen):
        if screen in config.always_shown_screens:
            config.always_shown_screens.remove(screen)
        renpy.hide_screen(screen)

    # Английское имя времени суток; без hour берётся системное время.
    def time_of_day(hours=None, morning=7, day=11, evening=18, night=23):
        if hours is None:
            hours = int(datetime.datetime.now().strftime("%H"))
        res = "night"
        if (hours >= morning) and (hours <= day):
            res = "morning"
        if (hours > day) and (hours <= evening):
            res = "day"
        if (hours > evening) and (hours < night):
            res = "evening"
        return res

    color_filters = {"morning": "#8404", "day": "#0000", "evening": "#0484", "night": "#000b"}

    def color_of_day(hours=None):
        return color_filters[time_of_day(hours)]

    def delete_saves_now():
        all = renpy.list_saved_games(fast=True)
        for i in all:
            renpy.unlink_save(i)
        renpy.restart_interaction()
    DeleteSavesNow = renpy.curry(delete_saves_now)

    def delete_saves(confirm=True):
        if confirm:
            layout.yesno_screen(message=_("Удалить все сохранения?"), yes=DeleteSavesNow(), no=NullAction())
        else:
            delete_saves_now()
    DeleteSaves = renpy.curry(delete_saves)

    def delete_data_now():
        delete_saves(False)
        persistent._clear(progress=True)
    DeleteDataNow = renpy.curry(delete_data_now)

    def delete_data(confirm=True):
        if confirm:
            layout.yesno_screen(message=_("Удалить все данные?\nИгра будет закрыта."), yes=DeleteDataNow(), no=NullAction())
    DeleteData = renpy.curry(delete_data)

    class Continue(Action, DictEquality):
        def __call__(self):
            FileLoad(1, confirm=False, page="auto", newest=True)()
        def get_sensitive(self):
            return FileLoadable(1, page="auto")

    def has_image(name):
        for i in renpy.display.image.images:
            if name == " ".join(" ".join(i).split()):
                return True
        return False

    def has_images(*args):
        res = True
        for i in args:
            if isinstance(i, (list, dict)):
                res = res & has_images(i)
            else:
                res = res & has_image(i)
        return res

    def seen_one(*args):
        res = False
        for i in args:
            res |= renpy.seen_image(i)
        return res

    def seen_all(*args):
        res = True
        for i in args:
            res &= renpy.seen_image(i)
        return res

    def has_mouse(mouse):
        if config.mouse:
            if mouse in config.mouse.keys():
                return True
        return False

    def rnds(*args):
        return renpy.random.choice(args)

    def rnd(i_from=0, i_to=None):
        if i_to is None:
            i_to = i_from
            i_from = 0
        return renpy.random.randint(int(i_from), int(i_to - 1))

    def rndf(f_from=0, f_to=None):
        if f_to is None:
            f_to = f_from
            f_from = .0
        return f_from + renpy.random.random() * (f_to - f_from)

    renpy.music.register_channel("effect", "sfx", loop=True, tight=True)

    def sfxplay(name, channel="effect", loop=True, fadein=default_fade, fadeout=default_fade, ext="ogg", audio_dir=audio_dir):
        if name:
            renpy.music.play(add_ext(audio_dir + "/" + name, ext), channel=channel, loop=loop, fadein=fadein, fadeout=fadeout)

    # Аудио helpers добавляют стандартные каталоги и расширения.

    def mplay(mname, fadein=default_fade, fadeout=default_fade, loop=True, channel="music", ext="ogg"):
        lst = []
        mname = make_list(mname)
        for i in mname:
            lst.append(add_ext(music_dir + "/" + i, ext))
        renpy.music.play(lst, channel=channel, loop=loop, fadein=fadein, fadeout=fadeout)

    def rndplay(mname, fadein=default_fade, fadeout=default_fade, loop=True, channel="music", ext="ogg"):
        lst = make_list(mname)
        if len(lst) > 1:
            renpy.random.shuffle(lst)
        mplay(lst, fadein, fadeout, loop, channel, ext)

    def mreplay(mname, fadein=default_fade, fadeout=default_fade, loop=True, channel="music", ext="ogg"):
        new_fn = add_ext(music_dir + "/" + mname, ext)
        renpy.music.play(new_fn, channel=channel, loop=loop, fadein=fadein, fadeout=fadeout)

    def mdeletetags(str):
        return re.sub(re.compile('<.*?>'), '', str)

    def fnplay(new_fn, fadein=default_fade, fadeout=default_fade, channel="music", loop=True, if_changed=False):
        old_fn = renpy.music.get_playing()
        renpy.music.play(new_fn, channel=channel, loop=loop, fadein=fadein, fadeout=fadeout, if_changed=if_changed)

    last_music_fn = ""

    def msave():
        store.last_music_fn = renpy.music.get_playing()

    def mrestore(fadein=default_fade, fadeout=default_fade, channel="music"):
        if last_music_fn:
            fnplay(last_music_fn, fadein=fadein, fadeout=fadeout, channel=channel)

    def add_ext(fn, ext="ogg"):
        if not fn.endswith("." + ext):
            fn = fn + "." + ext
        return fn

    def splay(mname, fadein=0, fadeout=0, channel=config.play_channel, ext="ogg", audio_dir=audio_dir):
        if mname:
            mname = make_list(mname)
            lst = []
            for i in mname:
                lst.append(add_ext(audio_dir + "/" + i, ext))
            renpy.play(lst, channel=channel, fadein=fadein, fadeout=fadeout)

    def sndplay(mname, fadein=0, fadeout=0, channel="sound", ext="ogg", audio_dir=audio_dir):
        if mname:
            mname = make_list(mname)
            lst = []
            for i in mname:
                lst.append(add_ext(audio_dir + "/" + i, ext))
            renpy.play(lst, channel=channel, fadein=fadein, fadeout=fadeout)

    def vplay(mname, fadein=0, fadeout=0, channel="voice", ext="ogg", voice_dir=voice_dir):
        if mname:
            renpy.play(add_ext(voice_dir + "/" + mname, ext), channel=channel, fadein=fadein, fadeout=fadeout)

    def sstop(fadeout=None, channel='audio'):
        renpy.music.stop(channel=channel, fadeout=fadeout)

    def sndstop(fadeout=0, channel='sound'):
        renpy.music.stop(channel=channel, fadeout=fadeout)

    def mstop(fadeout=default_fade, channel='music'):
        renpy.music.stop(channel=channel, fadeout=fadeout)

    def sfxstop(fadeout=default_fade, channel='effect'):
        renpy.music.stop(channel=channel, fadeout=fadeout)

    SPlay = renpy.curry(splay)
    SFXPlay = renpy.curry(sfxplay)
    SFXStop = renpy.curry(sfxstop)
    MPlay = renpy.curry(mplay)
    FNPlay = renpy.curry(fnplay)
    VPlay = renpy.curry(vplay)
    SStop = renpy.curry(sstop)
    MStop = renpy.curry(mstop)

    def s_play(sound, trans, st, at):
        if sound:
            splay(sound)

    def sfx_play(sound, trans, st, at):
        if sound:
            sfxplay(sound)

    def sfx_stop(trans, st, at):
        sfxstop()

    S_Play = renpy.curry(splay)
    SFX_Play = renpy.curry(sfxplay)

    def blank_list(a):
        def transpose(grid):
            return zip(*grid)

        def del_blank_rows(grid):
            return [list(row) for row in grid if any(row)]

        return del_blank_rows(transpose(del_blank_rows(transpose(a))))

    import re

    # Парсинг tag=value; value не может содержать ещё один "=".
    def get_tags(text, prefix='#'):
        res = {}
        tags = re.findall('{' + prefix + '([^}]+)}', text)
        for i in tags:
            parts = i.split('=')
            if len(parts) > 0:
                key = parts[0].strip()
                val = None
                if len(parts) > 1:
                    val = parts[1]
                res[key] = val
        return res

    def del_tags(txt, prefix='#'):
        if txt:
            res = ""
            tag = False
            for i in range(len(txt)):
                t = txt[i:i+len(prefix)+1]
                close = True
                if tag:
                    if txt[i] == "}":
                        tag = False
                        close = False
                elif t == "{" + prefix:
                    tag = True
                if not tag or close:
                    res = res + txt[i]
            txt = res
        return txt

    def del_all_tags(txt):
        return renpy.filter_text_tags(txt, allow=[ ])

    def get_tags_str(text, prefix='#'):
        return re.findall('{' + prefix + '([^}]+)}', text)

    def get_key_val(text, sep='='):
        txt = text.split(sep, 1)
        val, key = None, None
        if len(txt) > 0:
            key = txt[0].strip()
        if len(txt) > 1:
            val = txt[1].strip()
        return key, val

    # Значение скрытого тега; value не может содержать "=".
    def get_tag(text, tag, default=None, prefix='#'):
        tag = tag.strip()
        tags = get_tags(text, prefix)
        if tag in tags.keys():
            return tags[tag]
        return None

    def have_tag(text, tag, prefix='#'):
        return tag in get_tags(text, prefix).keys()

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

    # Первый tag либо default; eval(...) вычисляется как выражение.
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

    def tag_if(s, tag="#if", default=True):
        res = default
        if get_tag_first(s, tag):
            res = eval(str(get_tag_first(s, tag)))
        return res

    import inspect
    def get_var_name(var, default=""):
        for i in reversed(inspect.stack()):
            names = [var_name for var_name, var_val in i.frame.f_locals.items() if var_val is var]
            if len(names) > 0:
                return names[0]
        return default

    # Continue требует включённых autosave.
    config.has_autosave = True

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

    def get_by_key(key, dict):
        if key in dict.keys():
            return dict[key]
        return None

    def sprite_showed(image, layer='master'):
        return image in get_showing_sprites(layer)

    def get_sprite_by_tag(tag, layer='master'):
        if tag:
            images = get_showing_sprites(layer)
            for i in images:
                if str(tag) in str(i):
                    return str(i)
        return None

    def get_sprite_bounds(tag, layer="master"):
        spr = get_sprite_by_tag(tag, layer)
        if spr:
            x, y, w, h = renpy.get_image_bounds(spr, layer=layer)
            return int(x), int(y), int(w), int(h)
        return None, None, None, None

    import copy as dcopy
    def copy(*args):
        return dcopy.deepcopy(*args)

    def has_text(where, what):
        if isinstance(what, (str, unicode)):
            what = [what]
        for i in what:
            if i in where:
                return True
        return False

    def has_val(key):
        return key in globals().keys()

    def MyFileAction(name, page=None, **kwargs):
        global save_name
        if renpy.get_screen("load"):
            return FileLoad(name, page=page, **kwargs)
        else:
            s = del_tags(_last_say_what, "")
            if not s:
                s = ". . ."
            save_name = s
            return FileSave(name, page=page, **kwargs)

# Время суток: images_auto() связывает daytime_prefix с суффиксами alldaytime.
# setdaytime() циклически переключает вариант; без ассета применяется tint.

init -222:
    transform daytime_light(matrix):
        matrixcolor matrix

    transform daytime_empty():
        pass

    transform xy_at:
        function xy_at_f

init -99 python:

    def get_name_color(char, color=None):
        if color is None:
            color = gui.text_color

        col = color

        if isinstance(char, (str, unicode)):
            name = char
        else:
            name = char.name

            for arg in [ "color", "who_color" ]:
                if arg in char.who_args.keys():
                    col = char.who_args[arg]

        return name, col

    # "night" обязателен для fallback-логики.
    alldaytime = ["day", "night"]

    daytime_prefix = []

    # Матрицы времени суток: color, brightness, saturation, contrast.
    day_bg_attrs = ("#000", 0, 1, 1)
    day_attrs = ("#000", 0, 1, 1)
    evening_bg_attrs = ("#9af", -.2, .8, 1)
    evening_attrs = ("#9af", 0, .9, 1)
    night_bg_attrs = ("#9af", -.475, .375, .575)
    night_attrs = ("#9af", -.1, .375, 1)
    morning_bg_attrs = ("#fca", .1, 1, 1)
    morning_attrs = ("#fca", .1, 1, 1)

    curdaytime = alldaytime[0]

    daytime_suffix = alldaytime[0]

    daytime_suffixed = []

    bg_prefix = "bg"

    def setdaytime(newdaytime=None, effect=dissolve):
        if newdaytime is None:
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

    # Матрица текущего освещения; bg=True использует фоновые настройки.
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

    all_image_extensions = [ ".png", ".jpg", ".jpeg", ".webp" ]

    all_video_extensions = [ ".webm", ".ogv", ".mp4" ]

    def endswith(s, exts=None, case=False):
        if exts is None:

            exts = all_image_extensions
        for i in exts:
            t = s if case else s.lower()

            if t.endswith(i):
                return i
        return None

# Автообъявление поддерживает webp, LayeredImage-префиксы и время суток.
# Выполняется после остальных image declarations.
init 999 python hide:
    def create_automatic_images():

        seps = config.automatic_images

        if seps is True:
            seps = [ ' ', '/', '_' ]

        for dir, fn in renpy.loader.listdirfiles():

            if fn.startswith("_"):
                continue

            if not endswith(fn) and not endswith(fn, all_video_extensions):
                continue

            ext = endswith(fn, all_image_extensions + all_video_extensions)
            shortfn = fn[:-len(ext)].replace("\\", "/")

            name = ( shortfn, )
            for sep in seps:
                name = tuple(j for i in name for j in i.split(sep))

            while name:
                for i in config.automatic_images_strip:
                    if name[0] == i:
                        name = name[1:]
                        break
                else:
                    break

            prefix = name[0]
            suffix = name[len(name) - 1]

            # Первый daytime-суффикс считается вариантом по умолчанию.
            if suffix == daytime_suffix:
                name = name[:-1]

            name0 = name

            sname = " ".join(name)

            # LayeredImage-префиксы соединяются, а не делятся на теги.
            layered = False
            if prefix in layered_prefixes:
                name = "_".join(name)
                sname = name
                layered = True

            # Динамическим префиксам добавляется суффикс по умолчанию.
            if prefix in daytime_prefix:
                # Именованные daytime-варианты создаются через DynamicImage ниже.
                if not suffix in alldaytime[1:]:
                    if not sname in daytime_suffixed:
                        store.daytime_suffixed.append(sname)
                        if layered:
                            name = name + " " + daytime_suffix
                        else:
                            name = name + (daytime_suffix,)

            if name0 in daytime_suffixed:
                continue

            if len(name) < config.automatic_images_minimum_components:
                continue

            if name in renpy.display.image.images:
                continue

            # Однотеговый LayeredImage получает завершающий "_".
            if layered and not "_" in name:
                name = name + "_"

            if ext in all_video_extensions:
                renpy.image(name, Movie(play=fn))
            else:
                renpy.image(name, fn)

    if config.automatic_images:
        create_automatic_images()

    # DynamicImage либо матричный fallback текущего времени суток.
    def def_daytime(st, at, img):
        new = img + " " + curdaytime
        if has_image(new):
            return new, None
        new = img + " " + daytime_suffix
        if img.startswith(bg_prefix):
            return At(new, atdaytime(True)), None
        return At(new, atdaytime()), None

    if len(daytime_suffixed) > 0:
        for i in daytime_suffixed:
            renpy.image(i, DynamicDisplayable(def_daytime, i))
