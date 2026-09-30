## Глава 1: лампа → метроном → пианино → стук → холл → дверь → замки.
## Переходы в цепочке стука склеены с ударами.

## Изображения

## Позы «тянет шнур» и «к метроному» на общем холсте 937×1012: при сдвиге (-272, 21)
## силуэты рук совпадают, и Dissolve между ними ничего не обрезает.
## Холст «тянет шнур» лежит в нём со сдвигом (272, 0).
image chapter_1_lamp_hand pull_wide = Fixed(
    Transform("chapter_1_lamp_hand light_pull", pos=(272, 0)), xysize=(937, 1012))
image chapter_1_lamp_hand metronome_wide = Fixed(
    Transform("chapter_1_lamp_hand light_metronome", pos=(0, 21)), xysize=(937, 1012))

## Телевизоры с помехами на экране.
image chapter_1 scene_1_tv_close = sm_tv_scene("images/1_chapter/chapter_1 scene_1_tv_close.png",
    C1S1_TV_NOISE_POS, C1S1_TV_NOISE_SIZE, C1S1_TV_NOISE_CORNERS)
image chapter_1 scene_1_sofa_tv_night = sm_tv_scene("images/1_chapter/chapter_1 scene_1_sofa_tv_night.png",
    C1S1_TV_WIDE_POS, C1S1_TV_WIDE_SIZE, ((2, 2), (402, 2), (402, 282), (2, 282)))
image chapter_1 scene_1_tv_close_night = sm_tv_scene("images/1_chapter/chapter_1 scene_1_tv_close_night.png",
    C1S1_TV_NOISE_POS, C1S1_TV_NOISE_SIZE, C1S1_TV_NOISE_CORNERS)

image chapter_1 scene_1_living_room_mess = "images/1_chapter/cleanup/chapter_1_cleanup_mess.png"

## Константы сцены

## Внутренний проём рамки, а не меньшая белая заглушка PSD Layer 20.
define C1S1_TV_NOISE_POS = (812, 109)
define C1S1_TV_NOISE_SIZE = (603, 443)
define C1S1_TV_NOISE_CORNERS = ((2, 2), (601, 19), (600, 438), (5, 441))
define C1S1_TV_WIDE_POS = (1228, 118)
define C1S1_TV_WIDE_SIZE = (404, 284)

## Полкачания стрелки между щелчками — 85 BPM, темп мелодии пианино (мини-игра идёт в этот такт).
define C1S1_ARROW_HALF_T = 60.0 / 85.0

define C1S1_LAMP_FOCUS = (0.44, 0.44)

## Вторая серия ударов у пианино сильнее первой.
define c1s1_knock_punch = Move((0, 12), (0, -12), 0.09, bounce=True, repeat=True, delay=0.26)
define c1s1_knock_punch_hard = Move((0, 20), (0, -20), 0.08, bounce=True, repeat=True, delay=0.24)

## В холле три удара слабее, чем у пианино.
define c1s1_hall_knock_punch = Move((0, 6), (0, -6), 0.09, bounce=True, repeat=True, delay=0.22)

define c1s1_door_hit_punch = Move((0, 14), (0, -14), 0.08, bounce=True, repeat=True, delay=0.24)

## Сумка заякорена в нижнем левом углу обрезанного холста.
define C1S1_DOOR_BAG_POS = (0, 1080)
define C1S1_DOOR_BAG_ANCHOR = (0.0, 1.0)
define C1S1_Z_DOOR_BAG = 5

define C1S1_LOCKS_FOCUS = (0.50, 0.32)

define c1s1_locks_knock_punch = Move((0, 16), (0, -16), 0.08, bounce=True, repeat=True, delay=0.26)
define c1s1_locks_knock_punch_hard = Move((0, 22), (0, -22), 0.08, bounce=True, repeat=True, delay=0.24)

## Звук сцены. Файлы лежат в game/audio/sfx/c1s1/, кортеж = варианты удара.
define C1S1_METRONOME_TICK_VOL = 0.55
## WAV содержит полпериода тишины перед щелчком; длительность равна C1S1_ARROW_HALF_T.
define C1S1_METRONOME_LOOP_SOUND = "c1s1/metronome_loop"
## Щелчок — на середине loop.
define C1S1_METRONOME_PHASE = 0.5

default c1s1_metronome_audio = None

## Стук слышен с разных мест. "outside" — со стороны Вити, чистый; с нашей стороны он глуше:
## "door" — у двери, "hall" — из холла, "room" — из комнаты. Число — доля звука, которую
## заменяет low-pass (0 — чистый, больше — глуше).
define C1S1_KNOCK_MUFFLE = {"outside": 0.0, "door": 0.1, "hall": 0.22, "room": 0.35}
define C1S1_KNOCK_LOWPASS_HZ = 700.0
default c1s1_knock_audio = None

default c1s1_gg_pose = 1
## Доля пути за кадр 60 Гц: ≈0.2 с на смену позы.
define C1S1_GG_POSE_RELAX = 0.25

## Поза — целый кадр (фон пианино + фигура): растворение между кадрами не просвечивает фон
## и не показывает две пары рук, как было бы у вырезанных фигур.
image c1s1_gg_frame_1 = Fixed("chapter_1_piano", "chapter_1_piano_gg 1", xysize=(1920, 1080))
image c1s1_gg_frame_2 = Fixed("chapter_1_piano", "chapter_1_piano_gg 2", xysize=(1920, 1080))

## Бабл реплики Вити поверх кадра, не останавливает сцену: show screen / hide screen.
## Рамка — общая рамка проекта (стиль frame: заливка и контур со штрихом); текст — штрих
## группы show_text. line — строка или displayable (в замках — меняющийся текст).
## side "top" — бабл сверху по центру, хвостик вниз к двери; "left" — бабл у левого края,
## хвостик влево, за кадр. pos — свой якорь вместо стандартного.
## line — строка или кортеж строк: показывается строка с номером index() (в замках — номер
## текущего замка), последняя держится. pos: side "left" — левый край и центр по вертикали;
## "top"/"up" — центр по горизонтали и верх. При включённом Choice Placer (F7) бабл
## перетаскивается, pos пишется в вызов.
screen c1s1_vitya_bark(line, side="top", pos=None, index=None):
    zorder 60
    $ _b_key = line if isinstance(line, str) else line[0]
    $ _b_pos = _cp_bark_moved.get((side, _b_key)) or pos or ((48, 300) if side == "left" else (960, 44))
    $ _b_anchor = (0.0, 0.5) if side == "left" else (0.5, 0.0)
    if config.developer and renpy.get_screen("dev_choice_placer") is not None:
        drag:
            draggable True
            droppable False
            drag_raise True
            pos _b_pos
            anchor _b_anchor
            dragged renpy.partial(dev_cp_bark_dragged, side, _b_key, _b_anchor)
            use c1s1_vitya_bark_body(line, side, index)
    else:
        fixed:
            fit_first True
            pos _b_pos
            anchor _b_anchor
            at (c1s1_bark_in_left if side == "left" else c1s1_bark_in)
            ## Дрожь — на вложенном контейнере: выезд пишет те же offset снаружи.
            fixed:
                fit_first True
                at shake(1.0)
                use c1s1_vitya_bark_body(line, side, index)

## Перетащенные Choice Placer позиции баблов этой сессии: (side, текст) → pos. В релизе пуст.
init python:
    _cp_bark_moved = {}

init python:
    def c1s1_vitya_indexed_line(lines, i):
        """Строка с номером i, последняя держится."""
        return lines[max(0, min(int(i), len(lines) - 1))]

    def c1s1_vitya_indexed_dd(st, at, lines, index):
        return Text(c1s1_vitya_indexed_line(lines, index()), style="c1s1_vitya_bark_text"), 0.1

screen c1s1_vitya_bark_body(line, side, index=None):
    if side == "up":
        vbox:
            spacing 0
            add "c1s1_bark_tail_up" xalign 0.5 yoffset 4
            use c1s1_vitya_bark_frame(line, index)
    elif side == "left":
        hbox:
            ## Хвостик перекрывает контур рамки: тёмный треугольник продолжает заливку.
            spacing -4
            add "c1s1_bark_tail_left" yalign 0.5
            use c1s1_vitya_bark_frame(line, index)
    else:
        vbox:
            spacing 0
            use c1s1_vitya_bark_frame(line, index)
            add "c1s1_bark_tail" xalign 0.5 yoffset -4

screen c1s1_vitya_bark_frame(line, index=None):
    frame:
        background "c1s1_bark_bg"
        xmaximum 1500
        padding (40, 18, 40, 22)
        vbox:
            spacing 2
            text _("ВИТЯ") style "c1s1_vitya_bark_name" at scratch("show_text", tint=0.0, mix=0.5)
            if isinstance(line, str):
                text line style "c1s1_vitya_bark_text" at scratch("show_text", tint=0.0, mix=0.5)
            else:
                add DynamicDisplayable(c1s1_vitya_indexed_dd, line, index) at scratch("show_text", tint=0.0, mix=0.5)

## Рамка бабла: заливка окон проекта, контур толще (C1S1_BARK_LINE px) — только линии по
## краям, середина остаётся прозрачной.
define C1S1_BARK_LINE = 3
image c1s1_bark_border = At(Frame(Fixed(
        Solid(gui.frame_line_color, xsize=40, ysize=C1S1_BARK_LINE),
        Solid(gui.frame_line_color, ypos=40 - C1S1_BARK_LINE, xsize=40, ysize=C1S1_BARK_LINE),
        Solid(gui.frame_line_color, xsize=C1S1_BARK_LINE, ysize=40),
        Solid(gui.frame_line_color, xpos=40 - C1S1_BARK_LINE, xsize=C1S1_BARK_LINE, ysize=40),
        xysize=(40, 40)), 6, 6, 6, 6),
    scratch("ui_frame", tint=0.0))
image c1s1_bark_bg = Fixed(Solid("#000000c7"), "c1s1_bark_border")

## Половины ромба: треугольник с контуром по скошенным сторонам. tail — нижняя половина,
## остриё вниз; tail_up — верхняя, остриё вверх (мини-игры); tail_left — левая, остриё влево.
image c1s1_bark_tail = At(Transform(Fixed(
        Transform(Solid(gui.frame_line_color, xysize=(32, 32)), rotate=45, align=(0.5, 0.5)),
        Transform(Solid("#000000c7", xysize=(24, 24)), rotate=45, align=(0.5, 0.5)),
        xysize=(46, 46)), crop=(0, 23, 46, 23)),
    scratch("ui_frame", tint=0.0))

image c1s1_bark_tail_up = At(Transform(Fixed(
        Transform(Solid(gui.frame_line_color, xysize=(32, 32)), rotate=45, align=(0.5, 0.5)),
        Transform(Solid("#000000c7", xysize=(24, 24)), rotate=45, align=(0.5, 0.5)),
        xysize=(46, 46)), crop=(0, 0, 46, 23)),
    scratch("ui_frame", tint=0.0))

image c1s1_bark_tail_left = At(Transform(Fixed(
        Transform(Solid(gui.frame_line_color, xysize=(32, 32)), rotate=45, align=(0.5, 0.5)),
        Transform(Solid("#000000c7", xysize=(24, 24)), rotate=45, align=(0.5, 0.5)),
        xysize=(46, 46)), crop=(0, 0, 23, 46)),
    scratch("ui_frame", tint=0.0))

transform c1s1_bark_in():
    on show:
        alpha 0.0 yoffset -14
        easeout 0.3 alpha 1.0 yoffset 0
    on hide:
        easein 0.3 alpha 0.0 yoffset -10

transform c1s1_bark_in_left():
    on show:
        alpha 0.0 xoffset -160
        parallel:
            linear 0.06 alpha 1.0
        parallel:
            easeout 0.5 xoffset 0
    on hide:
        easein 0.3 alpha 0.0 xoffset -10

style c1s1_vitya_bark_name is default:
    font gui.dialogue_text_font
    size 28
    color gui.accent_color

style c1s1_vitya_bark_text is default:
    properties gui.text_properties("dialogue")
    size 40
    color "#dad4ca"
    xmaximum 1420

transform c1s1_gg_pose_at(pose):
    truecenter
    subpixel True
    parallel:
        breath_brightness(-0.04, -0.09, 6.0)
    parallel:
        function renpy.curry(c1s1_gg_pose_f)(pose)

## ══════════ СТУК: КАК УСТРОЕНО ══════════
## Звук — строка $ sfxplay(...) в сцене. Толчки картинки — ATL ниже, расписанный по секундам
## от ПОЯВЛЕНИЯ кадра (или от строки show с этим ATL). Звук и толчки совпадают, только если
## sfxplay стоит в ту же секунду, на которую рассчитан ATL. Переставляешь паузы/звук —
## двигай и соответствующий pause внутри ATL (подписано в сцене у каждого стука).
## Файлы: стук А = knock_door_1.ogg, стук Б = knock_door_2.ogg, в каждом 6 ударов за ~1.4 с.

## Рука над клавишами: выезжает снизу на rise px за rise_t, потом дышит — вверх на breath px
## за up_t, вниз за down_t. Параллакс ближнего плана — внутри. При «меньше движения» стоит.
transform c1s1_hand(xy, rise=0, rise_t=0.0, breath=0, up_t=3.0, down_t=3.0):
    subpixel True
    anchor (0, 0)
    pos xy
    xoffset 0.0 yoffset 0.0
    parallel:
        function parallax_near_f
    parallel:
        ypos absolute(xy[1] + rise * sm_motion_scale())
        easeout sm_motion_time(rise_t) ypos xy[1]
        block:
            ease up_t ypos absolute(xy[1] - breath * sm_motion_scale())
            ease down_t ypos xy[1]
            repeat

## Стук. Толчок удара: рывок, отскок и затухание ровно за t — до следующего удара,
## поэтому цепочка толчков не расходится со звуком.
transform c1s1_hit(amp, t):
    linear 0.03 yoffset (amp * sm_motion_scale())
    easein ((min(t, 0.4) - 0.03) * 0.4) yoffset (-0.3 * amp * sm_motion_scale())
    easein ((min(t, 0.4) - 0.03) * 0.6) yoffset 0.0
    pause (t - min(t, 0.4))

## Удары в knock_door_1.ogg: 0.055, 0.315, 0.595, 0.865, 1.11, 1.365 с от начала файла.
transform c1s1_knocks_1(amp):
    pause 0.055
    c1s1_hit(amp * 0.8, 0.26)
    c1s1_hit(amp, 0.28)
    c1s1_hit(amp * 0.94, 0.27)
    c1s1_hit(amp * 0.89, 0.245)
    c1s1_hit(amp * 0.86, 0.255)
    c1s1_hit(amp * 0.71, 0.4)

## Удары в knock_door_2.ogg: 0.095, 0.25, 0.455, 0.73, 0.985, 1.235 с.
transform c1s1_knocks_2(amp):
    pause 0.095
    c1s1_hit(amp * 0.6, 0.155)
    c1s1_hit(amp, 0.205)
    c1s1_hit(amp * 0.72, 0.275)
    c1s1_hit(amp * 0.77, 0.255)
    c1s1_hit(amp * 0.86, 0.25)
    c1s1_hit(amp * 0.72, 0.4)

## Обрушение нот (стук А): наезд до первого удара даёт запас краёв
## под толчки — на зуме 1.0 сдвиг открывал бы края кадра.
transform c1s1_break_camera():
    subpixel True
    align (0.5, 0.5)
    rotate 0.0
    xoffset 0.0 yoffset 0.0
    parallel:
        linear 0.05 zoom 1.03
    parallel:
        c1s1_knocks_1(5.0)

## Кулак за дверью: «hit» на ударе, «wind» — замах до следующего.
transform c1s1_fist(hold, wind):
    "chapter_1_door_hand hit"
    pos (1158, 147)
    pause hold
    "chapter_1_door_hand wind"
    pos (769, 131)
    pause wind

## Дверь снаружи на стуке Б: кулак бьёт по всем шести ударам knock_door_2
## (0.095, 0.25, 0.455, 0.73, 0.985, 1.235 с от старта звука) и замирает с замахом.
transform c1s1_door_fist_b():
    anchor (0, 0)
    "chapter_1_door_hand wind"
    pos (769, 131)
    pause 0.095
    c1s1_fist(0.08, 0.075)
    c1s1_fist(0.1, 0.105)
    c1s1_fist(0.12, 0.155)
    c1s1_fist(0.12, 0.135)
    c1s1_fist(0.12, 0.13)
    c1s1_fist(0.12, 0.3)

## Дверь снаружи: хвост knock_door_1 (удары 4–6) и через 1.1 с — knock_door_2 до склейки.
transform c1s1_door_fist():
    anchor (0, 0)
    c1s1_fist(0.12, 0.125)
    c1s1_fist(0.12, 0.135)
    c1s1_fist(0.12, 0.575)
    c1s1_fist(0.08, 0.075)
    c1s1_fist(0.1, 0.105)
    c1s1_fist(0.12, 0.155)

## Вещь холла дышит вместе с фоном; через 1.0 с (растворение сцены) подпрыгивает от ударов
## knock_door_1, amp 0 — стоит.
transform c1s1_hall_item(xy, amp=0.0):
    placed(xy)
    subpixel True
    parallel:
        linear 10 zoom 1.05
    parallel:
        fade_brightness(-0.04, -0.09, 3.0)
    parallel:
        pause 1.0
        c1s1_knocks_1(amp)

## Дверь изнутри темнеет к ложной тишине и проседает на возвращении стука (3.505 с).
transform c1s1_inside_dark():
    fade_brightness(-0.04, -0.07, 3.3)
    ease 0.2 u_breath_brightness -0.09
    ease 3.3 u_breath_brightness -0.08
    block:
        ease 6.0 u_breath_brightness -0.04
        ease 6.0 u_breath_brightness -0.08
        repeat

## Дверь изнутри: хвост knock_door_2 (удары 4–6), ложная тишина 2.0 с, усиленный knock_door_1
## (стартует на 2.505 с после склейки — pause сцены перед стуком А).
transform c1s1_inside_knocks(amp):
    c1s1_hit(amp * 0.77, 0.255)
    c1s1_hit(amp * 0.86, 0.25)
    c1s1_hit(amp * 0.72, 2.0)
    c1s1_knocks_1(amp * 1.4)

init python:
    import math

    def c1s1_metronome_start():
        """Звук метронома с начала такта: его щелчки, маятник на пианино и мини-игра — от одного t0."""
        sfxstop(handle=store.c1s1_metronome_audio, fadeout=0)
        store.c1s1_metronome_audio = sfxplay(C1S1_METRONOME_LOOP_SOUND, ext="wav", fadein=0, fadeout=0,
            tag="c1s1_metronome", volume=C1S1_METRONOME_TICK_VOL)
        piano_metro.start(store.c1s1_metronome_audio, C1S1_ARROW_HALF_T, C1S1_METRONOME_PHASE, piano_now())

    ## Ren'Py восстанавливает loop метронома при загрузке; такт (NoRollback) связывается заново.
    def c1s1_metronome_after_load():
        if store.c1s1_metronome_audio is not None:
            piano_metro.bind(store.c1s1_metronome_audio, C1S1_ARROW_HALF_T, C1S1_METRONOME_PHASE)

    config.after_load_callbacks.append(c1s1_metronome_after_load)

    ## Поза рук героини за пианино: каждая собранная нота переключает 1 ↔ 2, кроссфейд по
    ## _fx_state — переход не блокирует ввод, поза сохраняется и откатывается вместе с нотой.
    def c1s1_piano_hand_step(part, pos):
        store.c1s1_gg_pose = 2 if store.c1s1_gg_pose == 1 else 1

    def c1s1_gg_pose_f(pose, trans, st, at):
        ## Поза 1 всегда непрозрачна под позой 2: два полупрозрачных слоя на середине
        ## кроссфейда просвечивали бы фон.
        if pose == 1:
            trans.alpha = 1.0
            return None
        trans.alpha = _fx_step("c1s1_gg_pose_2", 1.0 if store.c1s1_gg_pose == 2 else 0.0, C1S1_GG_POSE_RELAX, 0.0)
        return 0

    def c1s1_pendulum_f(amp, trans, st, at):
        """Маятник на пианино качается от такта метронома: щелчок — в крайней точке."""
        m = piano_metro
        t = 0.0 if m.t0 is None else piano_now() - m.t0
        trans.rotate = amp * sm_motion_scale() * math.sin(math.pi * t / m.beat)
        return 0

    def c1s1_knock_filter(place):
        k = C1S1_KNOCK_MUFFLE.get(place, 0.0)
        if k <= 0.0:
            return None
        return renpy.audio.filter.WetDry(renpy.audio.filter.Lowpass(C1S1_KNOCK_LOWPASS_HZ), wet=k, dry=1.0 - k)

    def c1s1_knock(name, place, volume=1.0):
        """Серия стука, слышная из place."""
        store.c1s1_knock_audio = sfxplay(name, loop=False, fadein=0, fadeout=0, overlap=True, volume=volume)
        sm_audio_set_filter(store.c1s1_knock_audio, c1s1_knock_filter(place), duration=0)
        return store.c1s1_knock_audio

    def c1s1_knock_place(place, t=0.05):
        """Склейка посреди серии: тот же стук слышен уже из другого места."""
        sm_audio_set_filter(store.c1s1_knock_audio, c1s1_knock_filter(place), duration=t)

    def c1s1_metronome_tension():
        return sm_audio_set_filter(c1s1_metronome_audio, [
            renpy.audio.filter.Lowpass(2200.0),
            renpy.audio.filter.Reverb(resonance=0.72,
                dampening=2400.0, wet=0.55,
                dry=0.85, delay_multiplier=1.8),
        ], duration=7.0)

## Сцена

label chapter_1_scene_1:

    ## От лампы до замков — кино без реплик: быстрое меню возвращается в .after_locks.
    $ quick_menu = False

    ## Лампа.
    $ fx_vignette = True

    camera at camera_push(C1S1_LAMP_FOCUS, 1.04, 1.14, 25.0)
    scene chapter_1 lamp_dark:
        breath_brightness(-0.05, -0.08, 6.0)
    show chapter_1_lampshade dark zorder 10:
        placed((183, 0))
        breath_brightness(-0.05, -0.08, 6.0)
    with Dissolve(4.0)

    # pause 1.0

    ## Интерактивы не создают развилок и пропускаются вместе со сценой.
    if not renpy.is_skipping():
        menu(screen="scene_choice", follow=follow_camera(), skippable=True):
            "ВКЛЮЧИТЬ" (pos=(475, 530), size=(330, 165)):
                pass
            with Dissolve(0.5)

    show chapter_1_lamp_hand dark_reach zorder 5:
        subpixel True
        anchor (0, 0)
        pos (-360, 700) alpha 0.0
        ease 1.1 pos (0, 108) alpha 1.0
    pause 1.1

    ## Холст «тянет» совмещён с «тянется» сдвигом (6, -16): растворение без двоения.
    ## Пальцы под абажуром нащупывают шнурок, короткая заминка — и рывок вниз.
    show chapter_1_lamp_hand dark_pull zorder 5:
        pos (6, 92)
        easeout 0.5 pos (0, 58)
        pause 0.15
        easein 0.12 yoffset 22
    with Dissolve(0.3)
    pause (0.5 + 0.15 + 0.12 - 0.3)

    ## Щелчок и мгновенная смена освещения без сброса камеры.
    $ sm_sfx("lamp_on", volume=0.9)
    $ fx_bloom_strength = 1.4
    ## Нижняя часть корпуса закрывает пивот стрелки, руки остаются перед метрономом.
    scene chapter_1 lamp_light:
        breath_brightness(-0.04, -0.08, 6.0)
    ## Якорь стрелки совпадает с нижним креплением маятника (спрайт 45×368, bbox (985, 292)).
    show chapter_1_metronome_arrow zorder 3:
        subpixel True
        transform_anchor True
        anchor (0.5, 1.0)
        pos (1007, 660)
        rotate 0.0
        brightness(-0.1)
    ## Точный фрагмент светлого фона ниже прорези: (835, 640, 1171, 777).
    show chapter_1_metro_patch zorder 4:
        breath_brightness(-0.04, -0.08, 6.0)
    show chapter_1_lampshade light zorder 10:
        anchor (0, 0)
        pos (183, 0)
        
    ## Рука отпускает шнур: из рывка вниз подскакивает и оседает.
    show chapter_1_lamp_hand light_pull zorder 5:
        subpixel True
        anchor (0, 0)
        pos (0, 58)
        yoffset 22
        easein 0.45 yoffset -10
        # ease 0.35 yoffset 0
        easein 2.0 xoffset 240 yoffset 350

    ## Поза перерастворяется в «метроном» внутри ATL: позиция и качание не прерываются.
    ## Переход на общий холст — в том же кадре: pos компенсирует его сдвиг (272, 0).
    show chapter_1_lamp_hand metronome_wide:
        "chapter_1_lamp_hand pull_wide"
        pos (-272, 58)
        "chapter_1_lamp_hand metronome_wide" with Dissolve(0.4)
        block:
            ease 1.25 xoffset 230 yoffset 360
            ease 1.25 xoffset 240 yoffset 350
            repeat

    ## Метроном доступен только после включения света.
    if not renpy.is_skipping():
        menu(screen="scene_choice", follow=follow_camera(), skippable=True):
            "ЗАПУСТИТЬ" (pos=(1017, 547), size=(430, 190)):
                pass
            with Dissolve(0.5)

    ## Та же рука из качания дотягивается кончиками пальцев до палки маятника.
    show chapter_1_lamp_hand metronome_wide:
        ease 0.6 xoffset 372 yoffset 251
    pause 0.6

    ## Толчок руки и стрелка стартуют в один кадр.
    $ c1s1_metronome_start()
    show chapter_1_lamp_hand metronome_wide:
        easein 0.15 xoffset 386
        ease 0.3 xoffset 372
    ## Положительный rotate продолжает толчок руки вправо; loop звука и стрелка — в одном такте.
    show chapter_1_metronome_arrow zorder 3:
        easein (C1S1_ARROW_HALF_T / 2.0) rotate (20.0 * sm_motion_scale())
        block:
            ease C1S1_ARROW_HALF_T rotate (-20.0 * sm_motion_scale())
            ease C1S1_ARROW_HALF_T rotate (20.0 * sm_motion_scale())
            repeat
    pause 0.5

    show chapter_1_lamp_hand metronome_wide:
        ease 1.1 pos (-320, 739) xoffset 0 yoffset 0 alpha 0.0
    pause 1.1
    hide chapter_1_lamp_hand

    ## Пауза учитывает уже прошедшее время ухода руки.
    pause (C1S1_ARROW_HALF_T / 2.0 + (4 - 1) * C1S1_ARROW_HALF_T - 0.5 - 1.1)

    # ## Пианино: отъезд от ГГ к рукам.
    # scene chapter_1 piano:
    #     truecenter
    #     subpixel True
    #     zoom 1.0
    #     parallel:
    #         linear 40.0 zoom 1.07
    #     parallel:
    #         breath_brightness(-0.03, -0.09, 6.0)
    # with Dissolve(2.2)

    # pause 4.0

    # "sol"

    ## Камера рук подхватывает отъезд до его завершения: скорости зума
    ## согласованы, ≈0.038/с у ГГ и ≈0.037/с у рук.
    camera at camera_settle((0.51, 0.61), 1.03, 1.0, 13.4)
    $ fx_bloom_strength = FX_BLOOM_DEFAULT
    scene black
    show chapter_1 piano_hands:
        truecenter
        alpha 1.0
        subpixel True
        parallel:
            breath_brightness(-0.03, -0.08, 6.0)
        parallel:
            linear 10 alpha 0.0
    ## Руки — ближний план: parallax_near отделяет их от фона. Дыхание — ypos в absolute:
    ## float без обёртки Ren'Py трактует как долю экрана.
    ## Рука: место на клавишах, откуда выезжает (px снизу), за сколько секунд, размах дыхания
    ## в px, время вверх и вниз.
    show chapter_1_piano_hand_left:
        alpha 1.0
        parallel:
            c1s1_hand((330, 364), rise=40, rise_t=3.0, breath=2, up_t=2.9, down_t=3.6)
    show chapter_1_piano_hand_right:
        alpha 1.0
        parallel:
            c1s1_hand((1113, 366), rise=40, rise_t=3.0, breath=2, up_t=3.3, down_t=2.7)
    with Dissolve(2.0)

    pause 2.0

## Пианино под метроном; отдельный вход каталога сцен.

label .piano:

    ## Вход из каталога сцен: метроном ещё не запущен.
    if c1s1_metronome_audio is None:
        $ c1s1_metronome_start()
    
    ## Заглушка сборки для команды: дальше пропуск не идёт.
    $ skip_stop()

    # "start"

    $ quick_menu = False

    show chapter_1_piano:
        truecenter
        subpixel True
        breath_brightness(-0.04, -0.09, 6.0)
    $ c1s1_gg_pose = 1
    show c1s1_gg_frame_1 as c1s1_gg_1 at c1s1_gg_pose_at(1)
    show c1s1_gg_frame_2 as c1s1_gg_2 at c1s1_gg_pose_at(2)
    show metro_arrow_single:
        subpixel True
        transform_anchor True
        anchor (0.5, 1.0)
        pos (825, 392)
        function renpy.curry(c1s1_pendulum_f)(14.0)
    with Dissolve(3.2)

    call chapter_1_scene_1_minigame_piano from _call_c1s1_minigame_piano_scene

    ## Стук — постановка целиком: клик её не проматывает до самых замков; Ctrl/«Пропуск» работают.
    $ click_skip_block = True

    ## ▶ СТУК А — мини-игра вернулась в момент обрушения нот (игрок собрал предпоследний
    ## шаг). Вместо нот — фальшь, муж долбит в дверь, камера вздрагивает по ударам.
    ## Строки до show screen идут в один кадр с обрушением: паузы сюда не ставить.
    $ sfxplay("wrong/1", audio_dir="audio/chapter_1_piano_minigame", loop=False, fadein=0, fadeout=0, overlap=True, volume=1.0)
    $ c1s1_knock("c1s1/knock_door_1", "room")
    camera:
        subpixel True
        align (0.5, 0.5)
        rotate 0.0
        xoffset 0.0 yoffset 0.0
        parallel:
            linear 60.05 zoom 1.65
        parallel:
            c1s1_knocks_1(5.0)

    ## ══════════ ОБРУШЕНИЕ ПИАНИНО ══════════
    ## Ноты и клавиши разлетаются сами поверх кадра; за 1.8 с (PIANO_COLLAPSE_T) слой падения
    ## гаснет. Пока экран показан, здесь можно ставить что угодно: show, camera, pause.
    ## Время обрушения — сумма pause до hide screen.
    show screen minigame_piano_screen

    $ fnplay("audio/chapter_1/chapter_1_suspense_before_locker_game.ogg", fadein=1.0)

    ## ══════════ КАДР 1 · РУКИ ══════════
    ## Сразу на руки над клавишами: вздрагивают от стука А (c1s1_hit), мелко дрожат и за 2.4 с
    ## сползают с клавиш (ypos); осколки нот падают поверх. Растворение 0.5 + пауза 1.3 = 1.8 с
    ## обрушения.
    scene chapter_1 piano_hands:
        truecenter
        subpixel True
        breath_brightness(-0.04, -0.11, 3.0)
    show chapter_1_piano_hand_left:
        subpixel True
        anchor (0, 0)
        pos (330, 284)
        xoffset 0.0 yoffset 0.0
        parallel:
            breath_brightness(-0.02, -0.05, 6.0)
        parallel:
            c1s1_hit(8.0, 2.4)
            pause 0.6
            easein 2.4 ypos 318
        parallel:
            block:
                linear 0.05 xoffset (1.2 * sm_motion_scale())
                linear 0.05 xoffset (-1.2 * sm_motion_scale())
                repeat
    show chapter_1_piano_hand_right:
        subpixel True
        anchor (0, 0)
        pos (1113, 276)
        xoffset 0.0 yoffset 0.0
        parallel:
            breath_brightness(-0.02, -0.05, 6.0)
        parallel:
            c1s1_hit(8.0, 2.4)
            pause 0.8
            easein 2.4 ypos 306
        parallel:
            pause 0.03
            block:
                linear 0.05 xoffset (-1.0 * sm_motion_scale())
                linear 0.05 xoffset (1.0 * sm_motion_scale())
                repeat
    ## ▶ ВИТЯ: «Это я, открывай!» — плашка висит до холла (hide screen перед КАДРОМ 3).
    show screen c1s1_vitya_bark(_("Это я, открывай!"), side="left", pos=(32, 162))
    with Dissolve(0.5)

    # >>>>>>>>>>>> КАДР СЦЕНЫ ВО ВРЕМЯ ОБРУШЕНИЯ — сюда

    pause 1.3

    hide screen minigame_piano_screen
    $ piano_collapse_end()


    # >>>>>>>>>>>> ВОТ ТУТ

    pause 2.0

    ## ▶ СТУК Б — звук стартует на строке sfxplay ниже, кадр склеен с ним.
    ## Второй заход ближе и злее; метроном глохнет.
    $ c1s1_metronome_tension()
    $ c1s1_knock("c1s1/knock_door_2", "outside")

    ## ══════════ КАДР 2 · ДВЕРЬ СНАРУЖИ ══════════
    ## Кулак (c1s1_door_fist_b) и толчки камеры (c1s1_knocks_2) — по ударам стука Б.
    camera:
        subpixel True
        align (0.5, 0.5)
        rotate 0.0
        xoffset 0.0 yoffset 0.0
        parallel:
            easein 7.0 zoom 1.08
        parallel:
            c1s1_knocks_2(3.0)
    scene chapter_1 door:
        breath_brightness(-0.04, -0.09, 6.0)
    show chapter_1_door_hand hit at c1s1_door_fist_b, breath_brightness(-0.04, -0.09, 6.0)
    ## Длина кадра двери.
    pause 1.0
    hide screen c1s1_vitya_bark

    ## ══════════ КАДР 3 · ХОЛЛ ══════════
    ## Холл: взгляд тянется к двери, стук слышен отсюда.
    camera at camera_push((0.41, 0.44), 1.02, 1.08, 16.0)
    scene chapter_1 hall:
        breath_brightness(-0.04, -0.09, 6.0)
    ## Внутри групп zorder растёт по порядку предметов; швабра поверх всех.
    ## Второе число — сила подскока от стука.
    show chapter_1_hall_door zorder 3 at c1s1_hall_item((634, 128), 1.0)
    show chapter_1_hall_boots zorder 10 at c1s1_hall_item((1077, 564))
    show chapter_1_hall_packet zorder 10 + 1 at c1s1_hall_item((1075, 594))
    show chapter_1_hall_toy zorder 10 + 2 at c1s1_hall_item((1102, 618))
    show chapter_1_hall_paper zorder 20 at c1s1_hall_item((343, 521))
    show chapter_1_hall_bag zorder 20 + 1 at c1s1_hall_item((431, 413))
    show chapter_1_hall_bottles zorder 20 + 2 at c1s1_hall_item((334, 463), 2.0)
    show chapter_1_hall_umbrella_1 zorder 30 at c1s1_hall_item((267, 562), 3.0)
    show chapter_1_hall_umbrella_2 zorder 30 + 1 at c1s1_hall_item((374, 655), 2.5)
    show chapter_1_hall_mirror zorder 35 at c1s1_hall_item((328, 86), 1.5)
    show chapter_1_hall_mop zorder 40 at c1s1_hall_item((924, 302), 4.0)
    with Dissolve(1.0)

    ## ▶ СТУК А (тише, 0.75) — сразу после растворения (1.0 с). Вещи подпрыгивают сами через
    ## 1.0 с после появления кадра — это pause 1.0 в c1s1_hall_item. Ставишь паузу перед
    ## стуком — прибавь её и там.
    ## Удары отдаются в дверь и вещи у стен.
    $ c1s1_knock("c1s1/knock_door_1", "hall", 0.75)
    ## 0.865 с — до 4-го удара стука А: на нём склейка на дверь снаружи.
    pause 0.865
    $ c1s1_knock_place("outside")

    ## ══════════ КАДР 4 · ДВЕРЬ СНАРУЖИ ══════════
    ## Толчки камеры: три c1s1_hit — удары 4, 5, 6 стука А (он ещё звучит), потом
    ## c1s1_knocks_2 — стук Б через 1.1 с после склейки. Кулак (c1s1_door_fist) расписан
    ## под те же моменты.
    ## Четвёртый удар склеен с дверью снаружи; кулак бьёт в такт звуку.
    camera:
        subpixel True
        align (0.5, 0.5)
        rotate 0.0
        xoffset 0.0 yoffset 0.0
        zoom 1.04
        parallel:
            linear 3.0 zoom 1.07
        parallel:
            c1s1_hit(12.0, 0.245)
            c1s1_hit(11.0, 0.255)
            c1s1_hit(9.0, 0.6)
            c1s1_knocks_2(14.0)
    scene chapter_1 door:
        breath_brightness(-0.04, -0.09, 6.0)
    show chapter_1_door_hand hit at c1s1_door_fist, breath_brightness(-0.04, -0.09, 6.0)
    pause 1.1

    ## ▶ СТУК Б — ровно через 1.1 с после склейки: камера и кулак ждут его в эту секунду.
    $ c1s1_knock("c1s1/knock_door_2", "outside")
    pause 0.73
    $ c1s1_knock_place("door")

    ## 0.73 с — до 4-го удара стука Б: на нём склейка на дверь изнутри.

    ## ══════════ КАДР 5 · ДВЕРЬ ИЗНУТРИ ══════════
    ## Стена и сумка: c1s1_inside_knocks — удары 5, 6 стука Б, 2 с тишины, потом стук А
    ## (громкий). Наезд на замки — 17 с; мини-игра стартует на 4-й секунде и доводит его сама
    ## (C1S1_MG_ZOOM / C1S1_MG_CAMERA_T в замках) — менять вместе.
    ## Четвёртый удар склеен с дверью изнутри: наезд на замки, сумка вздрагивает.
    camera at camera_push(C1S1_LOCKS_FOCUS, 1.02, 1.09, 9.0)
    scene chapter_1 hall_door:
        subpixel True
        parallel:
            breath_brightness(-0.05, -0.09, 4.0)
        parallel:
            c1s1_inside_knocks(6.0)
    show chapter_1_hall_door_bag zorder C1S1_Z_DOOR_BAG:
        placed(C1S1_DOOR_BAG_POS, C1S1_DOOR_BAG_ANCHOR)
        subpixel True
        parallel:
            breath_brightness(-0.05, -0.09, 4.0)
        parallel:
            c1s1_inside_knocks(9.0)

    ## Ложная тишина.
    pause 2.505

    ## ▶ СТУК А (громкий) — через 2.505 с после склейки: c1s1_inside_knocks ждёт его
    ## в эту секунду. Двигаешь паузу — двигай и 2.0 в c1s1_inside_knocks.
    ## Стук возвращается сильнее.
    $ c1s1_knock("c1s1/knock_door_1", "door")
    pause 1.495

    # "end"

    ## ══════════ ЗАМКИ ══════════
    ## Саспенс замков наплывает на предыдущий: старый гаснет 18 с, новый входит 10 с.
    $ fnplay("audio/chapter_1/chapter_1_suspense_locker_game.ogg", fadein=10.0, fadeout=18.0)
    ## Блокировщик выше кнопок мини-игры и съел бы клик по «Открывай дверь».
    $ click_skip_block = False
    ## Переход к мини-игре с замками.
    call chapter_1_scene_1_minigame_locks from _call_c1s1_minigame_locks

    jump end_dev_yet

label .after_locks:

    $ sfxstop(handle=c1s1_metronome_audio, fadeout=1.2)
    $ c1s1_metronome_audio = None
    camera
    $ quick_menu = True

    if c1s1_locks_outcome == "timeout":
        $ c1s1_locks_outcome = "normal"

    if c1s1_locks_outcome == "fast":
        scene chapter_1 scene_1_vitya_outcome_fast

        vit "Привет."

        scene chapter_1 scene_1_hall_vitya

        "Часто Витя бывал просто невыносим."

        scene chapter_1 scene_1_hall_mess

        "Ничего серьёзного: какие-то банальности, быт... И эти его дурацкие, неискоренимые привычки."

    else:
        scene chapter_1 scene_1_vitya_outcome_normal

        vit "Ну наконец-то, бля."

        scene chapter_1 scene_1_hall_vitya

        "Часто Витя бывал просто невыносим."

        scene chapter_1 scene_1_hall_mess

        "Ничего серьёзного: какие-то банальности, быт... И эти его дурацкие, неискоренимые привычки."

    "Раньше мне хватало сил их не замечать. Терпеть."

label .tv:
    camera
    scene chapter_1 scene_1_tv_close

label .tv_dialogue:
    vit "Наконец-то..."

label .cleanup:
    camera
    scene chapter_1 scene_1_living_room_mess

    "Разбросанные носки, не опускающийся стульчак, как типично!"

    call chapter_1_scene_1_minigame_cleanup from _call_c1s1_household_cleanup

    scene chapter_1 scene_1_kitchen_sink

    mar "Ты в магазин зашёл?"
    "Нарушенные обещания..."

    scene chapter_1 scene_1_sofa_tv_night

    vit "Не-а."
    "Ну, мелочь. И ещё одна. И ещё одна. День за днём."
    mar "У нас на завтра..."
    "Раз за разом просишь, напоминаешь, умоляешь…"

    scene chapter_1 scene_1_tv_close_night

    vit "Не, завтра не могу никак."
    mar "Но мы договаривались!"

    scene chapter_1 scene_1_vitya_sofa

    vit "Не ори!"
    mar "Сам не ори!"
    "Скандалишь, наконец. Но тебя не слышат. Как это выводило меня из себя."
    vit "Ты опять начинаешь?!"
    "И так по кругу. Снова и снова."

    jump chapter_1_scene_2
