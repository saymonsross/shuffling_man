## Глава 1, сцена 1: лампа → метроном → пианино → стук → холл → дверь → замки →
## Витя дома → телевизор → уборка → ссора у телевизора.
## Переходы в цепочке стука склеены с ударами.

## Изображения

## Позы «тянет шнур» и «к метроному» на общем холсте 937×1012: при сдвиге (-272, 21)
## силуэты рук совпадают, и Dissolve между ними ничего не обрезает.
## Холст «тянет шнур» лежит в нём со сдвигом (272, 0).
image chapter_1_lamp_hand pull_wide = Fixed(
    Transform("chapter_1_lamp_hand light_pull", pos=(272, 0)), xysize=(937, 1012))
image chapter_1_lamp_hand metronome_wide = Fixed(
    Transform("chapter_1_lamp_hand light_metronome", pos=(0, 21)), xysize=(937, 1012))

## Телевизор работает (sm_tv_set, common/tv_noise.rpy): днём — новости, вечером — футбол
## на общем плане и «Конан-варвар» крупно. Крупно — планы глубины (depth_scene,
## common/parallax.rpy): комната с экраном и перед ней рука с пультом. Задник — путём к
## файлу: по имени образ сослался бы сам на себя. Прямоугольник экрана — на 4 px шире
## прозрачной дыры в фоне, углы картинки — на 3 px за её краем: корпус перекрывает шов.
## Ночью свет экрана мерцает и ложится на верхний слой (sm_tv_light): на крупном плане — на
## руку с пультом, на общем — на весь кадр, Витя там нарисован вместе с комнатой.
## Ведущая новостей говорит без остановки: рот (эллипс в px картинки) приоткрывается в
## ровном темпе mouth.rate; губы нарисованы сомкнутыми — сила отрицательная.
## В бегущей строке — отсылка к «Штанишкам на мальчика» Романа Чёрного (рынок «Жилмаш»);
## лента стартует с неё: на кадре одна реплика.
image c1s1_tv_news = Fixed(
    At("images/1_chapter/tv/tv_news.png", mouth_talk((175, 163), (16, 8), strength=-1.3)),
    sm_tv_ticker([
        # _("В МОСКВЕ ОЖИДАЕТСЯ ПОХОЛОДАНИЕ ДО МИНУС 15"),
        # _("МЭРИЯ ОБЪЯВИЛА О РЕМОНТЕ ТРЁХ СТАНЦИЙ МЕТРО"),
        _("РАЗЫСКИВАЕТСЯ МАЛЬЧИК 7 ЛЕТ, ПРОПАВШИЙ НА РЫНКЕ «ЖИЛМАШ». БЫЛ ОДЕТ В СИНЮЮ КУРТКУ. ВИДЕВШИХ ПРОСЯТ ПОЗВОНИТЬ ПО ТЕЛЕФОНУ 02"),
        # _("СБОРНАЯ РОССИИ ПО ФУТБОЛУ ПРОВЕДЁТ ТОВАРИЩЕСКИЙ МАТЧ"),
        ], (0, 354, 572, 34), first=2, lead=1.5, speed=50.0),
    xysize=(591, 416))
## У Конана рот по кругу плавно приоткрывается на 2 с и смыкается, волосы за головой
## развеваются — эллипсы и корень волос в px картинки.
image c1s1_tv_konan = At("images/1_chapter/tv/tv_konan.png",
    mouth_loop((315, 147), (8, 7), strength=-2.0, period=4.0, hold=2.0, ease=0.6, dark=0.5),
    wind_warp((250, 150), (60, 62), (300, 108), amp=1.6, speed=1.0))
## Днём телевизор сначала выключен (кадр _off: чёрная картинка в том же стекле). Рука с
## пультом — отдельный тег c1s1_tv_hand поверх кадра, на плане глубины 1, как в
## depth_scene: выползает снизу вдоль предплечья посреди разговора, жмёт кнопку и на hide
## уходит обратно вниз, пока кадр под ней сменяется на рабочий. Смена атрибута руки и кадра
## под ней не перезапускает подъём: клик посреди выползания руку не дёргает. Рабочий кадр
## ставят в момент включения: его экран начинает с чёрного и разгорается сам (sm_tv_power,
## common/crt_tv.rpy), бегущая строка стартует с этой же секунды.
transform c1s1_tv_hand_motion:
    subpixel True
    on show:
        alpha 0.0
        offset (-420, 560)
        parallel:
            easein 1.5 offset (0, 0)
        parallel:
            linear 1.0 alpha 1.0
    on hide:
        parallel:
            easeout 1.0 offset (-420, 560)
        parallel:
            pause 0.5
            linear 0.5 alpha 0.0

image chapter_1 scene_1_tv_close_off = depth_scene(
    sm_tv_set("images/1_chapter/chapter_1 scene_1_tv_close.png", Solid("#000", xysize=(591, 416)),
        (831, 111), (579, 420), ((1, 1), (577, 17), (576, 418), (1, 417)), turn=(0.2, 0.04)))
image chapter_1 scene_1_tv_close = depth_scene(
    sm_tv_set("images/1_chapter/chapter_1 scene_1_tv_close.png", At("c1s1_tv_news", sm_tv_power(0.58)),
        (831, 111), (579, 420), ((1, 1), (577, 17), (576, 418), (1, 417)), turn=(0.2, 0.04)))
image c1s1_tv_hand = "images/1_chapter/chapter_1 scene_1_tv_close_hand.png"
## Нажатие кнопки пульта без отдельного кадра: кисть коротко подаётся вперёд, к экрану,
## пульт клюёт носом (поворот вокруг запястья) — и возвращается. Сдвиг, px; поворот, °.
transform c1s1_tv_hand_press:
    subpixel True
    transform_anchor True
    anchor (0.0, 1.0)
    pos (0, 1080)
    xoffset 0.0 yoffset 0.0 rotate 0.0
    easein 0.07 xoffset (4.0 * sm_motion_scale()) yoffset (5.0 * sm_motion_scale()) rotate (0.8 * sm_motion_scale())
    easeout 0.22 xoffset 0.0 yoffset 0.0 rotate 0.0
image c1s1_tv_hand click = At("images/1_chapter/chapter_1 scene_1_tv_close_hand.png", c1s1_tv_hand_press)
## Футбол живой: камера трансляции чуть плывёт, игроки едва заметно двигаются; трибуны
## выше доли top высоты картинки стоят.
## Три кадра трансляции идут по кругу с растворением: 1 → 2 → 3 → 1, каждый держится 0.5 с и
## перетекает в следующий за 0.7 с.
image c1s1_tv_football_frames:
    "images/1_chapter/tv/tv_football 1.png"
    pause 0.5
    "images/1_chapter/tv/tv_football 2.png" with Dissolve(0.7)
    pause 0.5
    "images/1_chapter/tv/tv_football 3.png" with Dissolve(0.7)
    pause 0.5
    "images/1_chapter/tv/tv_football 1.png" with Dissolve(0.7)
    repeat
image c1s1_tv_football = At("c1s1_tv_football_frames", sm_tv_players(top=0.36, amp=1.5, pan=10.0, pan_t=26.0))
## Ночью крупно сначала идёт тот же футбол, что на общем плане. Витя переключает канал той
## же рукой с пультом, что днём (тег c1s1_tv_hand_night, свет экрана мерцает и на ней):
## кадр _switch встаёт на нажатии: экран на миг гаснет в чёрное, «Конан» проступает из него
## (свет экрана берёт ту же картинку — комната тоже на миг темнеет). Дальше — кадр без
## затемнения: им же сцена потом затемняет экран.
image chapter_1 scene_1_tv_close_night_football = depth_scene(
    sm_tv_set("images/1_chapter/chapter_1 scene_1_tv_close_night.png", "c1s1_tv_football",
        (831, 111), (579, 420), ((1, 1), (577, 17), (576, 418), (1, 417)), turn=(0.2, 0.04),
        glow="images/1_chapter/tv/tv_football 1.png"))
transform c1s1_tv_switch_blank:
    alpha 1.0
    pause 0.08
    easeout 0.25 alpha 0.0
image c1s1_tv_konan_switch = Fixed("c1s1_tv_konan",
    At(Solid("#050505"), c1s1_tv_switch_blank), xysize=(591, 416))
image chapter_1 scene_1_tv_close_night_switch = depth_scene(
    sm_tv_set("images/1_chapter/chapter_1 scene_1_tv_close_night.png", "c1s1_tv_konan_switch",
        (831, 111), (579, 420), ((1, 1), (577, 17), (576, 418), (1, 417)), turn=(0.2, 0.04)))
image chapter_1 scene_1_tv_close_night = depth_scene(
    sm_tv_set("images/1_chapter/chapter_1 scene_1_tv_close_night.png", "c1s1_tv_konan",
        (831, 111), (579, 420), ((1, 1), (577, 17), (576, 418), (1, 417)), turn=(0.2, 0.04)))
transform c1s1_tv_night_light:
    sm_tv_light((835, 115, 1406, 527), (1.0, 0.82, 0.62), radius=260.0, strength=0.3)
image c1s1_tv_hand_night = At("images/1_chapter/chapter_1 scene_1_tv_close_night_hand.png", c1s1_tv_night_light)
image c1s1_tv_hand_night click = At("images/1_chapter/chapter_1 scene_1_tv_close_night_hand.png", c1s1_tv_hand_press, c1s1_tv_night_light)
## Контур Вити, подсвеченный экраном, — отдельный слой с нарисованным бликом на прозрачном
## (sm_tv_rim), мерцает синхронно со светом экрана на кадре. Пока файла нет, слой пустой.
image chapter_1 scene_1_sofa_tv_night = Fixed(
    At(sm_tv_set(
        "images/1_chapter/chapter_1 scene_1_sofa_tv_night.png", "c1s1_tv_football",
        (1237, 121), (396, 277), ((1, 1), (394, 1), (394, 275), (1, 275)),
        glow="images/1_chapter/tv/tv_football 1.png"),
        sm_tv_light((1241, 125, 1629, 394), (0.85, 1.0, 0.72))),
    At("images/1_chapter/chapter_1 scene_1_sofa_tv_night_rim.png", sm_tv_rim())
        if renpy.loadable("images/1_chapter/chapter_1 scene_1_sofa_tv_night_rim.png") else Null(),
    xysize=(1920, 1080))
## Витя на диване кричит: кадры «молчит» и «кричит» меняются по репликам. Движение одно
## на четыре слога (rate), рот открыт почти всё движение (share): на «Не ори!» открывается
## на «Н» и закрывается в конце фразы; на «Ты опять начинаешь?!» движения два, между ними
## рот закрыт не меньше gap секунд. Кадры растворяются друг в друга за fade секунд.
## Кадр «кричит» лежит под именем образа, поэтому оба — путями к файлам.
image chapter_1 scene_1_vitya_sofa = TalkFrames(
    "images/1_chapter/chapter_1 scene_1_vitya_sofa_silence.png",
    "images/1_chapter/chapter_1 scene_1_vitya_sofa.png", "vit", rate=0.5, share=0.95, fade=0.08, gap=0.25, trim=0.1)

## Витя в дверях — планы глубины: прихожая сзади, Витя спереди. Рот двигается сам на его
## репликах (ключ "vit" в characters.rpy): кадры «молчит» и «говорит» меняются по слогам
## и растворяются друг в друга за 0.1 с.
## Слои — путями к файлам: под этим именем лежит и старый цельный кадр.
image chapter_1 scene_1_vitya_door = depth_scene(
    "images/1_chapter/chapter_1 scene_1_vitya_door_bg.png",
    TalkFrames("images/1_chapter/chapter_1 scene_1_vitya_door_vitya_silence.png",
        "images/1_chapter/chapter_1 scene_1_vitya_door_vitya_say.png", "vit", fade=0.1))

## Витя в холле — слои: холл сзади, Витя спереди. step=0 — слои едут за мышью вместе:
## Витя стоит в глубине, в дверях, и отдельный сдвиг отрывал бы его от проёма.
## Слои — путями к файлам: фон лежит под тем же именем.
image chapter_1 scene_1_hall_vitya = depth_scene(
    "images/1_chapter/chapter_1 scene_1_hall_vitya.png",
    "images/1_chapter/chapter_1 scene_1_hall_vitya with_vitya.png", step=0)

## Гостиная перед уборкой — чистая комната и те же предметы на тех же местах, что в
## мини-игре: склейка в неё незаметна.
image chapter_1 scene_1_living_room_mess = Fixed("chapter_1_cleanup_room",
    *[Transform(item[1], pos=item[2]) for item in C1S1_CLEANUP_ITEMS], xysize=(1920, 1080))

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

## Сумка заякорена в нижнем левом углу обрезанного холста.
define C1S1_DOOR_BAG_POS = (0, 1080)
define C1S1_DOOR_BAG_ANCHOR = (0.0, 1.0)
define C1S1_Z_DOOR_BAG = 5

define C1S1_LOCKS_FOCUS = (0.50, 0.32)

## Звук сцены. Файлы лежат в game/audio/sfx/c1s1/, кортеж = варианты удара.
define C1S1_METRONOME_TICK_VOL = 0.52
## WAV содержит полпериода тишины перед щелчком; длительность равна C1S1_ARROW_HALF_T.
define C1S1_METRONOME_LOOP_SOUND = "c1s1/metronome_loop"
## Щелчок — на середине loop.
define C1S1_METRONOME_PHASE = 0.5

default c1s1_metronome_audio = None
default c1s1_knock_audio = None

default c1s1_gg_pose = 1

## Поза — целый кадр (фон пианино + фигура): растворение между кадрами не просвечивает фон
## и не показывает две пары рук, как было бы у вырезанных фигур.
image c1s1_gg_frame_1 = Fixed("chapter_1_piano", "chapter_1_piano_gg 1", xysize=(1920, 1080))
image c1s1_gg_frame_2 = Fixed("chapter_1_piano", "chapter_1_piano_gg 2", xysize=(1920, 1080))

## Бабл реплики Вити поверх кадра, не останавливает сцену: show screen / hide screen.
## Рамка — общая рамка проекта (стиль frame: заливка и контур со штрихом); текст — штрих
## группы show_text. line — строка или displayable (в замках — меняющийся текст).
## side "top" — бабл сверху по центру, хвостик вниз к двери; "left" — бабл у левого края,
## хвостик влево, за кадр; "right" — хвостик вправо, к источнику звука (телевизор).
## pos — свой якорь вместо стандартного; name — подпись вместо «ВИТЯ»; width — ширина рамки,
## px: длинная фраза переносится в несколько строк.
## line — строка или кортеж строк: показывается строка с номером index() (в замках — номер
## текущего замка), последняя держится. pos: side "left" — левый край и центр по вертикали;
## "right" — правый край (кончик хвостика) и центр; "top"/"up" — центр по горизонтали и верх. При включённом Choice Placer (F7) бабл
## перетаскивается, pos пишется в вызов.
## jitter — размах дрожи бабла, px; 0 — бабл стоит.
screen c1s1_vitya_bark(line, side="top", pos=None, index=None, name=_("ВИТЯ"), width=1500, jitter=1.0):
    zorder 60
    $ _b_key = line if isinstance(line, str) else line[0]
    $ _b_pos = _cp_bark_moved.get((side, _b_key)) or pos or {"left": (48, 300), "right": (1200, 300)}.get(side, (960, 44))
    $ _b_anchor = {"left": (0.0, 0.5), "right": (1.0, 0.5)}.get(side, (0.5, 0.0))
    if config.developer and renpy.get_screen("dev_choice_placer") is not None:
        drag:
            draggable True
            droppable False
            drag_raise True
            pos _b_pos
            anchor _b_anchor
            dragged renpy.partial(dev_cp_bark_dragged, side, _b_key, _b_anchor)
            use c1s1_vitya_bark_body(line, side, index, name, width)
    else:
        fixed:
            fit_first True
            pos _b_pos
            anchor _b_anchor
            at {"left": c1s1_bark_in_left, "right": c1s1_bark_in_right}.get(side, c1s1_bark_in)
            ## Дрожь — на вложенном контейнере: выезд пишет те же offset снаружи.
            fixed:
                fit_first True
                at shake(jitter)
                use c1s1_vitya_bark_body(line, side, index, name, width)

## Реплика баблом вместо окна диалога — экран say для Character(screen="c1s1_bark_say"):
## клик, откат, пропуск и история работают как у обычной реплики. side, pos и width — как у
## c1s1_vitya_bark, задаются в Character через show_side / show_pos / show_width. Перед
## такими репликами окно диалога прячут (window hide): иначе window auto показал бы пустое.
screen c1s1_bark_say(who, what, side="right", pos=None, width=760):
    zorder 60
    $ _b_pos = pos or {"left": (48, 300), "right": (1200, 300)}.get(side, (960, 44))
    $ _b_anchor = {"left": (0.0, 0.5), "right": (1.0, 0.5)}.get(side, (0.5, 0.0))
    fixed:
        fit_first True
        pos _b_pos
        anchor _b_anchor
        at {"left": c1s1_bark_in_left, "right": c1s1_bark_in_right}.get(side, c1s1_bark_in)
        fixed:
            fit_first True
            at shake(1.0)
            hbox:
                spacing -4
                if side == "left":
                    add "c1s1_bark_tail_left" yalign 0.5
                frame:
                    background "c1s1_bark_bg"
                    xmaximum width
                    padding (40, 18, 40, 22)
                    vbox:
                        spacing 2
                        text (who or "") style "c1s1_vitya_bark_name" at scratch("show_text", tint=0.0, mix=0.5)
                        text what id "what" xmaximum (width - 80) at scratch("show_text", tint=0.0, mix=0.5)
                if side == "right":
                    add "c1s1_bark_tail_right" yalign 0.5

## Перетащенные Choice Placer позиции баблов этой сессии: (side, текст) → pos. В релизе пуст.
init python:
    _cp_bark_moved = {}

init python:
    def c1s1_vitya_indexed_line(lines, i):
        """Строка с номером i, последняя держится."""
        return lines[max(0, min(int(i), len(lines) - 1))]

    def c1s1_vitya_indexed_dd(st, at, lines, index):
        return Text(c1s1_vitya_indexed_line(lines, index()), style="c1s1_vitya_bark_text"), 0.1

screen c1s1_vitya_bark_body(line, side, index=None, name=_("ВИТЯ"), width=1500):
    if side == "up":
        vbox:
            spacing 0
            add "c1s1_bark_tail_up" xalign 0.5 yoffset 4
            use c1s1_vitya_bark_frame(line, index, name, width)
    elif side == "left":
        hbox:
            ## Хвостик перекрывает контур рамки: тёмный треугольник продолжает заливку.
            spacing -4
            add "c1s1_bark_tail_left" yalign 0.5
            use c1s1_vitya_bark_frame(line, index, name, width)
    elif side == "right":
        hbox:
            spacing -4
            use c1s1_vitya_bark_frame(line, index, name, width)
            add "c1s1_bark_tail_right" yalign 0.5
    else:
        vbox:
            spacing 0
            use c1s1_vitya_bark_frame(line, index, name, width)
            add "c1s1_bark_tail" xalign 0.5 yoffset -4

screen c1s1_vitya_bark_frame(line, index=None, name=_("ВИТЯ"), width=1500):
    frame:
        background "c1s1_bark_bg"
        xmaximum width
        padding (40, 18, 40, 22)
        vbox:
            spacing 2
            text name style "c1s1_vitya_bark_name" at scratch("show_text", tint=0.0, mix=0.5)
            ## Ширина строки — по рамке за вычетом полей: стиль сам ограничивает только 1420 px.
            if isinstance(line, str):
                text line style "c1s1_vitya_bark_text" xmaximum (width - 80) at scratch("show_text", tint=0.0, mix=0.5)
            else:
                add DynamicDisplayable(c1s1_vitya_indexed_dd, line, index) at scratch("show_text", tint=0.0, mix=0.5)

## Рамка бабла: заливка окон проекта, контур толще (3 px) — только линии по краям,
## середина остаётся прозрачной.
image c1s1_bark_border = At(Frame(Fixed(
        Solid(gui.frame_line_color, xsize=40, ysize=3),
        Solid(gui.frame_line_color, ypos=37, xsize=40, ysize=3),
        Solid(gui.frame_line_color, xsize=3, ysize=40),
        Solid(gui.frame_line_color, xpos=37, xsize=3, ysize=40),
        xysize=(40, 40)), 6, 6, 6, 6),
    scratch("ui_frame", tint=0.0))
image c1s1_bark_bg = Fixed(Solid("#000000c7"), "c1s1_bark_border")

## Половины ромба: треугольник с контуром по скошенным сторонам. tail — нижняя половина,
## остриё вниз; tail_up — верхняя, остриё вверх (мини-игры); tail_left — левая, остриё влево;
## tail_right — правая, остриё вправо.
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

image c1s1_bark_tail_right = At(Transform(Fixed(
        Transform(Solid(gui.frame_line_color, xysize=(32, 32)), rotate=45, align=(0.5, 0.5)),
        Transform(Solid("#000000c7", xysize=(24, 24)), rotate=45, align=(0.5, 0.5)),
        xysize=(46, 46)), crop=(23, 0, 23, 46)),
    scratch("ui_frame", tint=0.0))

transform c1s1_bark_in():
    on show:
        alpha 0.0 yoffset -7
        easeout 0.3 alpha 1.0 yoffset 0
    on hide:
        easein 0.3 alpha 0.0 yoffset -5

transform c1s1_bark_in_left():
    on show:
        alpha 0.0 xoffset -80
        parallel:
            linear 0.06 alpha 1.0
        parallel:
            easeout 0.5 xoffset 0
    on hide:
        easein 0.3 alpha 0.0 xoffset -5

transform c1s1_bark_in_right():
    on show:
        alpha 0.0 xoffset 80
        parallel:
            linear 0.2 alpha 1.0
        parallel:
            easeout 0.5 xoffset 0
    on hide:
        easein 0.3 alpha 0.0 xoffset 5

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
        ## 0.25 — доля пути за кадр 60 Гц: ≈0.2 с на смену позы.
        trans.alpha = _fx_step("c1s1_gg_pose_2", 1.0 if store.c1s1_gg_pose == 2 else 0.0, 0.25, 0.0)
        return fx_tick()

    def c1s1_pendulum_f(amp, trans, st, at):
        """Маятник на пианино качается от такта метронома: щелчок — в крайней точке."""
        m = piano_metro
        t = 0.0 if m.t0 is None else piano_now() - m.t0
        trans.rotate = amp * sm_motion_scale() * math.sin(math.pi * t / m.beat)
        return fx_tick()

    ## Стук слышен с разных мест. "outside" — со стороны Вити, чистый; с нашей стороны он глуше:
    ## "door" — у двери, "hall" — из холла, "room" — из комнаты. Число — доля звука, которую
    ## заменяет low-pass 700 Гц (0 — чистый, больше — глуше).
    def c1s1_knock_filter(place):
        k = {"outside": 0.0, "door": 0.1, "hall": 0.22, "room": 0.35}.get(place, 0.0)
        if k <= 0.0:
            return None
        return renpy.audio.filter.WetDry(renpy.audio.filter.Lowpass(700.0), wet=k, dry=1.0 - k)

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

    ## От лампы до замков — кино без реплик: быстрое меню возвращается на первой реплике
    ## после замков.
    $ quick_menu = False

    ## Лампа.
    $ fx_vignette = True

    ## Постановка до замков — кино без реплик: клик её не проматывает; Ctrl/«Пропуск»
    ## работают. Блокировщик снимается только перед сценовыми кнопками и мини-играми.
    $ click_skip_block = True
    camera at camera_push(C1S1_LAMP_FOCUS, 1.04, 1.14, 25.0)
    scene chapter_1 lamp_dark:
        breath_brightness(-0.05, -0.08, 6.0)
    show chapter_1_lampshade dark zorder 10:
        placed((183, 0))
        breath_brightness(-0.05, -0.08, 6.0)
    with Dissolve(4.0)

    # pause 1.0

    ## Интерактивы не создают развилок и пропускаются вместе со сценой.
    $ click_skip_block = False
    if not renpy.is_skipping():
        menu(screen="scene_choice", follow=follow_camera(), skippable=True):
            "ВКЛЮЧИТЬ" (pos=(475, 530), size=(330, 165)):
                pass
            with Dissolve(0.5)

    ## Рука, шнур и щелчок света идут по таймингам ATL: клик сбил бы их.
    $ click_skip_block = "hard"
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
    $ fx_bloom_snap(1.4)
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
    $ click_skip_block = False
    if not renpy.is_skipping():
        menu(screen="scene_choice", follow=follow_camera(), skippable=True):
            "ЗАПУСТИТЬ" (pos=(1017, 547), size=(430, 190)):
                pass
            with Dissolve(0.5)

    ## Та же рука из качания дотягивается кончиками пальцев до палки маятника. Толчок,
    ## стрелка и такт звука синхронны — клик их не проматывает ни при какой настройке.
    $ click_skip_block = "hard"
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

    ## Блокировщик выше клавиш мини-игры и съел бы клики по ним.
    $ click_skip_block = False
    call chapter_1_scene_1_minigame_piano from _call_c1s1_minigame_piano_scene

    ## Стук — постановка целиком под звук: клик её не проматывает до самых замков ни при
    ## какой настройке; Ctrl/«Пропуск» работают.
    $ click_skip_block = "hard"

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
    show chapter_1_hall_door zorder 3 at c1s1_hall_item((634, 128), 0.3)
    show chapter_1_hall_boots zorder 10 at c1s1_hall_item((1077, 564))
    show chapter_1_hall_packet zorder 10 + 1 at c1s1_hall_item((1075, 594))
    show chapter_1_hall_toy zorder 10 + 2 at c1s1_hall_item((1102, 618), 1.0)
    show chapter_1_hall_paper zorder 20 at c1s1_hall_item((343, 521))
    show chapter_1_hall_bag zorder 20 + 1 at c1s1_hall_item((431, 413))
    show chapter_1_hall_bottles zorder 20 + 2 at c1s1_hall_item((334, 463), 0.0)
    show chapter_1_hall_umbrella_1 zorder 30 at c1s1_hall_item((267, 562), 1.0)
    show chapter_1_hall_umbrella_2 zorder 30 + 1 at c1s1_hall_item((374, 655), 1.0)
    show chapter_1_hall_mirror zorder 35 at c1s1_hall_item((328, 86), 1.0)
    show chapter_1_hall_mop zorder 40 at c1s1_hall_item((924, 302), 2.0)
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

    # scene black with Dissolve(2.0)

    # jump end_dev_yet

label .after_locks:

    $ sfxstop(handle=c1s1_metronome_audio, fadeout=1.2)
    $ mstop(fadeout=5.5)
    $ c1s1_metronome_audio = None

    if c1s1_locks_outcome == "timeout":
        $ c1s1_locks_outcome = "normal"

    $ mplay("chapter_1/after_lock_game", fadein=0.5, fadeout=5.5, loop=True)

    ## ══════════ КАДР 6 · ВИТЯ В ДВЕРЯХ ══════════
    ## Открыла быстро — мягкое растворение и медленный наезд на лицо. Возилась — склейка
    ## почти встык, камера оседает с крупного плана: Витя на взводе.
    ## Постановка до самой ссоры — смены кадра, паузы — идёт под click_skip_block: клик
    ## проматывает только реплики; Ctrl/«Пропуск» работают всегда.
    $ click_skip_block = True
    window auto hide
    if c1s1_locks_outcome == "fast":
        camera at camera_push((0.47, 0.30), 1.00, 1.05, 26.0)
        scene chapter_1 scene_1_vitya_door:
            breath_brightness(-0.02, -0.06, 6.0)
        with Dissolve(1.5)
    else:
        camera at camera_settle((0.47, 0.30), 1.00, 1.05, 21.2)
        scene chapter_1 scene_1_vitya_door:
            breath_brightness(-0.02, -0.06, 6.0)
        with Dissolve(0.3)
    $ quick_menu = True
    $ click_skip_block = False

    if c1s1_locks_outcome == "fast":
        vit "Привет."

        $ click_skip_block = True
        pause 0.5
        $ click_skip_block = False

        ## Цедит сквозь зубы: рот открывается всего дважды — кадр проявляется за 0.2 с и
        ## сразу гаснет за 0.2.
        vit "Что, опять уснула?" (callback=talk_callback("vit", moves=2, hold=0.2, fade=0.2, step=0.5))
    else:
        vit "Не прошло и полгода!.."

        $ click_skip_block = True
        pause 0.5
        $ click_skip_block = False

        vit "Я уже думал, снова выбивать дверь придётся."

    ## ══════════ КАДР 7 · ВИТЯ В ХОЛЛЕ ══════════
    ## Общий план. Долгий наезд на дверь идёт через этот и следующий кадр.
    $ click_skip_block = True
    window auto hide
    camera at camera_push((0.39, 0.45), 1.02, 1.12, 40.0)
    scene chapter_1 scene_1_hall_vitya:
        breath_brightness(-0.02, -0.04, 7.0)
    with Dissolve(2.0)
    pause 0.5
    $ click_skip_block = False

    "Часто Витя бывал просто невыносим."
    "Ничего серьёзного: какие-то банальности, быт...  "
    
    # "Раньше мне хватало сил их не замечать. Терпеть."
    # "Существующий только в своём темпе, со своими ценностями."
    # "И на первом месте всегда были его эти привычки."
    # "Типичнейшие, неискоренимые бытовые ритуалы."
    # "Наверное, наш брак давно был не идеален, а понимала ли я это?"
    # "Выходит, что нет."

    ## ══════════ КАДР 8 · ХОЛЛ БЕЗ ВИТИ ══════════
    ## Витя растворяется посреди мысли, в холле остаются его вещи; камера не сбрасывается.
    ## Переход — renpy.transition по слою master: scene и with спрятали бы окно диалога.
    ## Шорох вещей, брошенных на комод, — вместе с появлением кадра.
    $ sm_sfx("c1s1/c1s1_hall_clothes_drop", volume=0.35)
    $ renpy.transition(Dissolve(0.6), layer="master")
    show chapter_1 scene_1_hall_mess:
        breath_brightness(-0.04, -0.09, 6.0)

    # "Наверное, наш брак давно был не идеален, а понимала ли я это?"
    # "Выходит, что нет."
    # "По привычке притворялась даже перед собой..."
    # "...пока не стало слишком поздно."

    "И эти его дурацкие, неискоренимые привычки."
    "\"Мелочи\". Так он их называл."

    $ click_skip_block = True
    pause 2.0

    # "Разбросанные носки, не опускающийся стульчак, как типично!"
    # "Казалось бы, ну какая мелочь, плюнь, пройди мимо!"

    # # ## Кадр темнеет до нижней границы и замирает.
    # # show chapter_1 scene_1_hall_mess:
    # #     brightness_to(-0.09, 5.0)
    # # # "Раньше мне хватало сил их не замечать. Терпеть."

    # "Но когда раз за разом просишь, напоминаешь, умоляешь..."
    # "Скандалишь, наконец, а тебя абсолютно не слышат — о, как это выводило меня из себя."

    # "Кто-то из мудрых сказал, что залог счастливого супружества — взаимные компромиссы."
    # "Но, боюсь... за все восемь лет брака, я поняла, что одних компромисов мало."

## Телевизор; отдельный вход каталога сцен.

label .tv:

    ## ══════════ КАДР 9 · ПУЛЬТ ══════════
    ## Наезд на тёмный экран. Телевизор включает Витя.
    $ click_skip_block = True
    window auto hide
    camera at camera_push((0.58, 0.30), 1.00, 1.07, 24.0)
    scene chapter_1 scene_1_tv_close_off:
        breath_brightness(-0.03, -0.07, 6.0)
    with Dissolve(3.0)
    $ click_skip_block = False

    mar "Вить, по поводу..."

    # ты в магазин зашёл?"

    $ click_skip_block = True
    pause 1.0
    $ click_skip_block = False

    vit "Всё потом, Марин!"

    ## Рука с пультом выползает, пока Витя договаривает.
    show c1s1_tv_hand at c1s1_tv_hand_motion, float_drift((5.0, 4.0), speed=1.0, side=(-1, 1)), parallax_plane(1.0), breath_brightness(-0.03, -0.07, 6.0)

    vit "Сейчас — новости."

    ## Витя жмёт кнопку — телевизор включается на нажатии пальца; потом рука уходит вниз.
    $ click_skip_block = True
    window auto hide
    pause 0.3
    $ sm_sfx("c1s1/c1s1_tv_remote_click", volume=0.6)
    show c1s1_tv_hand click
    pause 0.1

    ## Рабочий кадр встаёт вместо тёмного без перехода: его экран разгорается сам. show без
    ## ATL оставляет кадру дыхание, камера не сбрасывается. Звук включения — в тот же кадр.
    $ sm_sfx("c1s1/tv_turn_on", volume=0.8)
    ## Шипение кинескопа — один раз, при первом включении; 0.026 — уровень исходника.
    $ sm_sfx("c1s1/c1s1_tv_hiss", volume=0.026)
    ## Сводка о пропавшем мальчике — один раз, с экрана: чуть справа, как телевизор в кадре.
    $ sm_audio_set_pan(sm_sfx("c1s1/tv_news_malchik_lost", volume=0.65, tag="c1s1_news"), 0.1)
    show chapter_1 scene_1_tv_close
    pause 0.9
    hide c1s1_tv_hand


label .tv_dialogue:

    pause 3.5
    $ click_skip_block = False

    "И каждый наш день состоял из этих \"мелочей\"."
    "Снова пропустили запись? Мелочь. Потом сходим."
    "Опять разбросаны носки по всей квартире? Мелочь. Пусть лежат."

    # "Наверное, наш брак давно был не идеален, а понимала ли я это?"
    # "Выходит, что нет."
    # "По привычке притворялась даже перед собой..."
    # "...пока не стало слишком поздно."

    $ click_skip_block = True
    pause 1.0
    $ click_skip_block = False

    vit "Кошмар какой... слышала?"
    vit "Как хорошо, что у нас всё в порядке."

    $ click_skip_block = True
    pause 1.0

## Уборка; отдельный вход каталога сцен.

label .cleanup:

    ## ══════════ КАДР 10 · РАКОВИНА ══════════
    ## Наезд на гору посуды.
    $ click_skip_block = True
    window auto hide
    camera at camera_push((0.45, 0.62), 1.0, 1.14, 40.0)
    scene chapter_1 scene_1_kitchen_sink:
        breath_brightness(-0.04, -0.09, 6.0)
    with Dissolve(2.0)
    # pause 11.5
    $ click_skip_block = False

    "Утешать себя чужими плохими вестями — это важно."
    "А вот гора немытой посуды — это мелочь. Встань и помой. Ты же тут хозяйка."
    "Потом будет ещё одна мелочь."
    "И ещё одна. И ещё одна. Снова и снова."

    # "Утешаем себя чужими плохими вестями, пока на кухне уже неделю стоит засор."
    # "Казалось бы, ничего серьёзного: какие-то банальности, быт... "
    # "И эти его дурацкие, неискоренимые привычки."
    # "Разбросанные носки, гора не мытой посуды, не опускающийся стульчак, как типично!"

    ## ══════════ КАДР 11 · ГОСТИНАЯ ══════════
    ## Отъезд открывает бардак и медленно оседает на зуме 1.0 — уже во время уборки: её
    ## комната повторяет эту камеру. Дыхание — по часам кадра и с теми же числами, что у
    ## мини-игры (C1S1_CLEANUP_BREATH_*): на стыке яркость не скачет.
    ## Гостиная и уборка — без bloom (светлые обои под ним уходят в белёсую дымку) и с
    ## виньеткой на 40% слабее; те же доли — у комнаты мини-игры (C1S1_CLEANUP_FX_*).
    $ click_skip_block = True
    window auto hide
    camera at camera_settle((0.5, 0.5), 1.00, 1.07, 32.5)
    scene chapter_1 scene_1_living_room_mess:
        parallel:
            breath_brightness_clock(0.0, -0.04, 6.0)
        parallel:
            fx_frame(bloom=0.0, vignette=0.6)
    with Dissolve(2.5)
    ## Блокировщик снят и на мини-игру: он выше её предметов и съел бы клики по ним.
    $ click_skip_block = False

    "Как же это выводит из себя."
    "Ты раз за разом просишь, напоминаешь, умоляешь..."
    "Скандалишь, наконец, а тебя абсолютно не слышат."
    "Потому что твои причитания — это мелочь."

    call chapter_1_scene_1_minigame_cleanup from _call_c1s1_household_cleanup

    # ## ══════════ КАДР 11 · РАКОВИНА ══════════
    # ## Наезд на гору посуды.
    # $ click_skip_block = True
    # window auto hide
    # camera at camera_push((0.45, 0.62), 1.0, 1.10, 40.0)
    # scene chapter_1 scene_1_kitchen_sink:
    #     breath_brightness(-0.04, -0.09, 6.0)
    # with Dissolve(2.0)
    # pause 1.5

    ## ══════════ КАДР 12 · ВИТЯ У ТЕЛЕВИЗОРА, НОЧЬ ══════════
    ## День сменился ночью: через чёрное кадр проявляется 11 с, разговор начинается ещё в
    ## полутьме; один медленный наезд на весь разговор.
    $ click_skip_block = True
    window auto hide
    scene black with Dissolve(3.0)
    camera at camera_push((0.60, 0.38), 1.02, 1.12, 40.0)
    ## Футбол слышен чуть справа, со стороны телевизора, — пока он на экране.
    $ sm_audio_set_pan(sfxplay("c1s1/c1s1_footbal_tv", fadein=3.0, tag="c1s1_football", volume=0.0875), 0.1)
    show chapter_1 scene_1_sofa_tv_night:
        alpha 0.0
        parallel:
            linear 11.0 alpha 1.0
        parallel:
            breath_brightness(-0.05, -0.09, 6.0)
    pause 3.0
    $ click_skip_block = False

    vit "Ну же! Давай!"

    ## Марина заговаривает с Витей — три подхода, ответ один: ему не до неё. Развилки нет:
    ## ветки сходятся на штанге, пропуск проходит меню насквозь. Кнопки разбросаны по
    ## тёмным местам кадра; двигать — Choice Placer (F7).
    $ click_skip_block = True
    pause 1.0
    $ click_skip_block = False
    if not renpy.is_skipping():
        menu(screen="scene_choice", follow=follow_camera(), drift=True, skippable=True):
            "Нужно поговорить" (pos=(540, 332), size=(330, 165)):
                pause 0.5
                mar "Я хотела обсудить кое-что..."
                $ click_skip_block = True
                pause 1.0
                $ click_skip_block = False
                vit "Да погоди, Марин! Если наши сейчас не забьют, то..."
            "Как игра?" (pos=(1045, 378), size=(330, 165)):
                pause 0.5
                mar "Наши выигрывают?"
                $ click_skip_block = True
                pause 1.0
                $ click_skip_block = False
                vit "Да какой там! Если сейчас не забьют, то всё!.."
            "Скоро закончишь?" (pos=(781, 624), size=(330, 165)):
                pause 0.5
                mar "Долго до конца матча?"
                $ click_skip_block = True
                pause 1.0
                $ click_skip_block = False
                vit "Сейчас уже всё решится. Пан или пропал. Гол или..."

    $ click_skip_block = True
    pause 1.0
    $ click_skip_block = False

    ## Голос из телевизора — баблом у экрана, хвостиком к нему; ждёт клика.
    window hide
    ## Звук комментатора — с бабла, из той же точки, что трансляция (панорама).
    $ sm_audio_set_pan(sm_sfx("c1s1/tv_sports_football", volume=0.4), 0.1)
    tvv "И!.. Это штанга! Всё! Похоже, сегодня уже не отыграться! Конец надеждам!"
    window auto

    $ click_skip_block = True
    pause 1.0
    $ click_skip_block = False

    vit "Вершинин, ну какой же ты кривоногий! Нет слов! Марин, ты это видела?"
    vit "Кто так играет?!"
    

    ## Прежний разговор — до схемы с выборами.
    # "Нарушенные обещания..."
    # vit "Не-а."
    # mar "Витя, ты помнишь у нас на завтра..."
    # vit "Нет, завтра не могу никак."
    # mar "Но мы договаривались!"

    $ click_skip_block = True
    pause 1.0

    ## ══════════ КАДР 13 · ЭКРАН ══════════
    ## Наезд на экран: Витя смотрит в него, не на Марину. Идёт тот же футбол; рука с пультом
    ## выползает, Витя переключает на «Конана», рука уходит.
    window auto hide
    camera at camera_push((0.58, 0.30), 1.04, 1.12, 14.0)
    scene chapter_1 scene_1_tv_close_night_football:
        breath_brightness(-0.05, -0.09, 6.0)
    with Dissolve(1.5)
    show c1s1_tv_hand_night at c1s1_tv_hand_motion, float_drift((5.0, 4.0), speed=1.0, side=(-1, 1)), parallax_plane(1.0), breath_brightness(-0.05, -0.09, 6.0)
    
    pause 1.0

    vit "Не могу дальше на это смотреть..."

    pause 0.3

    $ sm_sfx("c1s1/c1s1_tv_remote_click", volume=0.6)
    show c1s1_tv_hand_night click
    ## Канал щёлкает на нажатии пальца: кадр под рукой меняется без перехода, show без ATL
    ## оставляет ему дыхание.
    pause 0.1
    show chapter_1 scene_1_tv_close_night_switch
    ## Звук канала меняется вместе с картинкой. «Конан» в файле на 5 дБ тише футбола —
    ## громкость выше на столько же; затихает вместе с затемнением в конце сцены.
    $ sfxstop(tag="c1s1_football", fadeout=0.15)
    $ sm_audio_set_pan(sfxplay("c1s1/c1s1_konan_tv", fadein=0.3, tag="c1s1_konan", volume=0.16), 0.1)
    pause 1.0
    hide c1s1_tv_hand_night
    pause 1.0
    $ click_skip_block = False

    ## Второй заход Марины — три темы, и все сводятся к его «завтра». Затем — запись к
    ## Тамаре: три реакции, сходятся на его срыве. Развилок нет, пропуск проходит меню
    ## насквозь; кнопки двигать — Choice Placer (F7).
    if not renpy.is_skipping():
        menu(screen="scene_choice", follow=follow_camera(), drift=True, skippable=True):
            "Почему ты мне не помогаешь?" (pos=(521, 254), size=(330, 165)):
                pause 0.5
                mar "Почему так сложно не разбрасывать грязные вонючие носки по всей квартире?"
                $ click_skip_block = True
                pause 1.0
                $ click_skip_block = False
                vit "Опять ты про эти мелочи. Ну, не мешают же эти носки. Дорогу не перегораживают."
                vit "Мне после работы иногда ложку до рта нормально не донести."
                vit "Вот ты сидишь весь день дома. Я зарабатываю — ты убираешься."
            "Как дела на работе?" (pos=(417, 460), size=(330, 165)):
                pause 0.5
                mar "Как у тебя на работе дела? Ничего не рассказываешь..."
                $ click_skip_block = True
                pause 1.0
                $ click_skip_block = False
                vit "Да завал полный. В отпуск не отпускают, угрожают сокращениями."
                vit "Но ты не переживай, у нас всё нормально будет."
            "По поводу завтра..." (pos=(515, 728), size=(330, 165)):
                pause 0.5
                mar "Ты помнишь? Тамара Виталиевна ждёт нас троих завтра..."
                $ click_skip_block = True
                pause 1.0
                $ click_skip_block = False
                vit "Завтра не получится. Прости."

    $ click_skip_block = True
    pause 1.0
    $ click_skip_block = False

    vit "Завтра мне надо с коллегами встретиться."
    vit "Так что с Тамарой как-нибудь в следующий раз..."

    $ click_skip_block = True
    pause 1.0
    $ click_skip_block = False

    if not renpy.is_skipping():
        menu(screen="scene_choice", follow=follow_camera(), drift=True, skippable=True):
            "Опять отменяем запись?!" (pos=(464, 294), size=(330, 165)):
                pause 0.5
                mar "Это уже четвёртая отмена! Тамара Виталиевна..."
                $ click_skip_block = True
                pause 1.0
                $ click_skip_block = False
                vit "Тамара Виталиевна потерпит! Она очень хорошо получает за каждый приём."
            "Понятно" (pos=(442, 478), size=(330, 165)):
                pause 0.5
                mar "Понятно..."
                $ click_skip_block = True
                pause 1.0
                $ click_skip_block = False
                vit "Что тебе понятно?! Ну не могу я шляться с тобой по твоим подружкам."
            "Достал!" (pos=(541, 662), size=(330, 165)):
                pause 0.5
                mar "Тебе ещё самому не надоело?! Каждый раз одно и то же!"
                mar "Что ты скажешь теперь? \"Это мелочь, Марин, просто запишемся ещё раз\"?!"

    $ click_skip_block = True
    pause 1.0
    $ click_skip_block = False

    vit "У меня есть и другие дела, понятно?! Помимо собственной работы и этих твоих \"терапий\"!"
    vit "Я не могу весь день валяться дома, а потом ныть какой-то старой мымре о том, как в жизни всё хреново!"
    
    vit "Кто-то должен оплачивать такие развлечения!"
    vit "Вставать по утрам, а не к обеду. А потом пахать весь день."
    vit "Возьми себя уже в руки!"

    $ click_skip_block = True
    pause 1.0

    ## ══════════ КАДР 14 · ССОРА ══════════
    ## Кадр растворяется под окном диалога (show, не scene; переход — renpy.transition по
    ## слою master: оператор with спрятал бы окно). Камера входит крупно и плавно оседает;
    ## каждый следующий наезд начинается с зума, на котором кончился предыдущий, — без
    ## рывков.
    # $ renpy.transition(Dissolve(0.6), layer="master")
    # camera at camera_settle((0.40, 0.38), 1.0, 1.08, 31.2)
    # show chapter_1 scene_1_vitya_sofa:
    #     breath_brightness(-0.05, -0.09, 6.0)
    # ## Пауза не короче перехода: иначе он оборвётся.

    # $ click_skip_block = False

    # vit "Не ори!"

    # $ click_skip_block = True
    # pause 0.7
    # $ click_skip_block = False

    # mar "Сам не ори!"

    # # $ click_skip_block = True
    # # pause 0.5
    # # $ click_skip_block = False

    # # "Скандалишь, наконец. Но тебя не слышат."
    # # "Как жэ это выводило меня из себя."

    # $ click_skip_block = True
    # pause 1.0
    # $ click_skip_block = False

    # vit "Марин, ну ты опять начинаешь?!"

    # $ click_skip_block = True
    # pause 1.0
    # $ click_skip_block = False

    # ## Кадр темнеет до нижней границы и замирает.
    # show chapter_1 scene_1_tv_close_night:
    #     brightness_to(-0.09, 4.0)

    # "И так по кругу. Снова и снова..."

    # $ click_skip_block = True
    # pause 1.0
    # $ click_skip_block = False
    
    "Кто-то из мудрых сказал, что залог счастливого супружества — взаимные компромиссы."
    "Но, боюсь... за все восемь лет брака, я поняла, что одних компромиссов мало."

    # "Наверное, наш брак давно был не идеален, а понимала ли я это?"
    # "Выходит, что нет."
    # "По привычке притворялась даже перед собой..."
    # "...пока не стало слишком поздно."

    ## Дальше блокировщик держит и начало второй сцены: она сама ставит его заново.
    $ click_skip_block = True
    window auto hide
    $ sfxstop(tag="c1s1_konan", fadeout=7.0)
    scene black with Dissolve(2.0)
    camera

    pause 1.0

    jump chapter_1_scene_2
