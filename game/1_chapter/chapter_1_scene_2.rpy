## Глава 1, сцена 2: утро после ссоры → спальня → темнота под ладонями → кухня → бутерброды.

## Изображения

## Бутерброды — один образ на все четыре стадии (StageDissolve, common/transforms.rpy):
## сцена поднимает счётчик c1s2_bite, и через c1s2_bite_delay секунд — посреди реплики —
## очередной бутерброд растворяется. Над обеими чашками пар (steam, common/shaders.rpy) —
## столбы от поверхности чая, px картинки 2352×1080.
## Приоритет 10: transform steam объявляется в common позже этого файла.
default c1s2_bite = 0
default c1s2_bite_delay = 1.0
define 10 c1s2_sandwiches_steam = steam(((420, 120, 130, 320), (1735, 50, 150, 320)), amp=4.5, glow=0.55)
image chapter_1 scene_2_sandwiches = At(StageDissolve((
    "images/1_chapter/chapter_1 scene_2_sandwiches.png",
    "images/1_chapter/owner_review/chapter_1_review_sandwiches stage_1.png",
    "images/1_chapter/owner_review/chapter_1_review_sandwiches stage_2.png",
    "images/1_chapter/owner_review/chapter_1_review_sandwiches stage_3.png"),
    "c1s2_bite", "c1s2_bite_delay", fade=0.3), c1s2_sandwiches_steam)

## Спальня из коридора — планы глубины (depth_scene, common/parallax.rpy): задник комнаты,
## перед ним стена слева и створка справа. По наведению на проём (c1s2_door_hover) комната
## чуть светлеет, а закрытая створка гаснет (flag_fade), открывая приоткрытую, которая всегда
## лежит под ней. Клик по проёму замораживает это состояние (c1s2_door_open) до конца кадра.
default c1s2_door_hover = False
default c1s2_door_open = False

image c1s2_door_bg_lit = At("chapter_1_scene_2_parents_room_door_1_in", brightness(0.03))
image chapter_1 scene_2_parents_room_door = depth_scene(
    ("chapter_1_scene_2_parents_room_door_1_in",
        At("c1s2_door_bg_lit", flag_fade((0, 0), ("c1s2_door_hover", "c1s2_door_open")))),
    ("chapter_1_scene_2_parents_room_door_left_wall",
        "chapter_1_scene_2_parents_room_door_right_open",
        At("chapter_1_scene_2_parents_room_door_right_close",
            flag_fade((0, 0), ("c1s2_door_hover", "c1s2_door_open"), False))))

## Тот же проём в конце сцены: створка приоткрыта, в комнате Марина на кровати. Задник
## сдвинут влево, чтобы она стояла в просвете двери.
image chapter_1 scene_2_parents_room_door_marina = depth_scene(
    At("chapter_1_scene_2_parents_room_door_2_in", offset(-60, 0)),
    ("chapter_1_scene_2_parents_room_door_left_wall",
        "chapter_1_scene_2_parents_room_door_right_open"))

## Зона проёма между стеной и створкой; едет за камерой, как сценовые кнопки.
## Развилки нет: пропуск проходит насквозь.
screen c1s2_door_hover_zone():
    zorder 50
    modal True
    if renpy.is_skipping():
        timer 0.01 action Return()
    fixed:
        at follow_camera()
        button:
            area (930, 0, 305, 1080)
            background None
            alt _("Заглянуть в спальню")
            action Return()
            hovered [SetVariable("c1s2_door_hover", True), SPlay("c1s2/door_hover", volume=0.4)]
            unhovered SetVariable("c1s2_door_hover", False)

## Марина крупно — планы глубины: задник и героиня. На её репликах губы приоткрываются
## по слогам: кадры gg (сомкнуты) и gg_say (приоткрыты). Вариант со слезой на щеке
## (water, старт по c1s2_tear) пока выключен.
default c1s2_tear = False

# пока рано плакать
# image chapter_1 scene_2_marina_close = depth_scene(
#     "ch1_2_mc_close_3_bg",
#     ("ch1_2_mc_close_3_gg",
#         At("ch1_2_mc_close_3_gg_tears", water(flow=(455, 602), start="c1s2_tear", delay=2.0))))

image chapter_1 scene_2_marina_close = depth_scene("ch1_2_mc_close_3_bg",
    TalkFrames("ch1_2_mc_close_3_gg", "ch1_2_mc_close_3_gg_say", "mar"))

## Лицо и руки дрожат всё сильнее (shake_grow: размах, px, и секунды до максимума).
## Слеза лежит между лицом и руками и склеена с лицом в одну группу — дрожит вместе с ним.
## Слезы нет, пока сцена не взвела c1s2_tear_2 (после первой реплики кадра); с этого
## момента она 15 с стекает по щеке (flow — участок слоя по вертикали, px), затем за 6 с
## тускнеет до половины и такой остаётся.
default c1s2_tear_2 = False
## Плач Марины в этом кадре; handle нужен, чтобы посреди звука включить фильтр.
default c1s2_crying_audio = None

image chapter_1 scene_2_marina_close_face = depth_scene(
    "ch1_2_mc_close_3_bg",
    (At(Fixed("ch1_2_mc_close_3_gg_2",
            At("ch1_2_mc_close_3_gg_2_tears",
                water(flow=(455, 602), start="c1s2_tear_2", run=15.0, hold=0.0, fade=6.0, fade_to=0.5)),
            xysize=(1920, 1080)),
        shake_grow(1.05, 20.0)),
    At("ch1_2_mc_close_3_gg_2_hands", shake_grow(1.3, 20.0))))

## Темнота под ладонями — планы глубины: фон, дальняя ладонь, ближняя ладонь, каждая в
## своём плане. Ладони мелко дрожат, каждая сама по себе. У фона своя добавка яркости
## поверх дыхания всего кадра из сцены; периоды здесь и в сцене одинаковые, добавки
## складываются.
default c1s2_dark_shake = False
## Титры последней фразы этого кадра гаснут с момента, как сцена взвела c1s2_whisper_out;
## с c1s2_whisper_rush один раз еле заметно вспыхивают и гаснут вдвое быстрее.
default c1s2_whisper_out = False
default c1s2_whisper_rush = False

image chapter_1 scene_2_dark = depth_scene(
    At("prologue_head_bg", breath_brightness(0.02, 0.07, 8.0)),
    At("ch2_dark_r_hand", shake(0.6)),
    At("ch2_dark_l_hand", shake(0.6)),
    step=1.0)

## Спальня, общий план — слои: задник (пол и стена), Витя, кровать с Мариной. step=0 —
## слои склеены в один план: фигуры стоят вплотную, глубина между ними ломала бы кадр;
## за мышью кадр едет целиком.

## Кровать с Мариной. На её репликах губы чуть приоткрываются (mouth_talk — эллипс рта в
## px картинки; сила отрицательная: рот нарисован закрытым).
image c1s2_parents_bed = At("ch1_2_parents_krovvat_gg",
    mouth_talk((864, 641), (20, 11), who="mar", strength=-1.3))

## Образы отличаются только Витей. Рот у него двигается на каждой его реплике сам (ключ
## "vit" в characters.rpy), пока молчит — закрыт; сцена только ставит позы.
## Поза 1, у двери: слои «рот закрыт» и «зубы» меняются по слогам (TalkFrames). Имена файлов
## перепутаны относительно содержимого: зубы — ch1_2_parents_vitya_1.
image chapter_1 scene_2_parents_room_vitya_1 = depth_scene(
    "ch1_2_parents_bg",
    TalkFrames("ch1_2_parents_vitya_1_say", "ch1_2_parents_vitya_1", "vit"),
    "c1s2_parents_bed", step=0)

## Крик — только на начало реплики («Знаешь что?! Хватит!»): орущая поза говорит кадрами
## (TalkFrames), и через 1.3 с от момента, когда сцена взвела c1s2_vitya_shout, ещё на этой
## же реплике сама растворяется в спокойную позу 1, а та договаривает остаток
## (FlagDissolve). В исходнике орущая поза нарисована рядом с позой 1 — offset ставит её на
## то же место.
default c1s2_vitya_shout = False

image chapter_1 scene_2_parents_room_vitya_2 = depth_scene(
    "ch1_2_parents_bg",
    FlagDissolve(
        At(TalkFrames("ch1_2_parents_vitya_2", "ch1_2_parents_vitya_2_say", "vit"), offset(-139, 0)),
        TalkFrames("ch1_2_parents_vitya_1_say", "ch1_2_parents_vitya_1", "vit", rate=0.7),
        "c1s2_vitya_shout", 1.3, fade=0.6),
    "c1s2_parents_bed", step=0)

## Позы у кровати говорят сменой кадров. Орущая — слои vitya_2 (рот приоткрыт) и vitya_2_say
## (раскрыт). С разведёнными руками — vitya_3 (рот закрыт) и vitya_4 (говорит): одна поза, в
## исходнике в 223 px друг от друга, отличаются только ртом.
## Ноги у слоёв 3 и 4 не дорисованы и должны оставаться за кроватью.
image chapter_1 scene_2_parents_room_vitya_3 = depth_scene(
    "ch1_2_parents_bg",
    At(TalkFrames("ch1_2_parents_vitya_2", "ch1_2_parents_vitya_2_say", "vit"), offset(653 - 400, 0)),
    "c1s2_parents_bed", step=0)
image chapter_1 scene_2_parents_room_vitya_4 = depth_scene(
    "ch1_2_parents_bg",
    At(TalkFrames(At("ch1_2_parents_vitya_3", offset(223, 0)), "ch1_2_parents_vitya_4", "vit"),
        hflip, offset(-35, 30)),
    "c1s2_parents_bed", step=0)
image chapter_1 scene_2_parents_room_vitya_4_1 = depth_scene(
    "ch1_2_parents_bg",
    At(TalkFrames(At("ch1_2_parents_vitya_3", offset(223, 0)), "ch1_2_parents_vitya_4", "vit"),
        hflip, offset(15, 30), rotate(-2), zoom(1.02)),
    "c1s2_parents_bed", step=0)
image chapter_1 scene_2_parents_room_vitya_5 = depth_scene(
    "ch1_2_parents_bg",
    At(TalkFrames("ch1_2_parents_vitya_3", At("ch1_2_parents_vitya_4", offset(-223, 0)), "vit"),
        hflip, zoom(1.03), rotate(3), offset(493 - 400, 10)),
    "c1s2_parents_bed", step=0)

## Сцена

label chapter_1_scene_2:

    $ mstop(fadeout=8.5)

    $ quick_menu = True
    ## Виньетка на всю сцену; при входе прямо сюда её некому включить.
    $ fx_vignette = True

    ## Клик проматывает только реплики. Постановка — выход из чёрного, смены кадра, паузы
    ## под звук — идёт под click_skip_block; Ctrl/«Пропуск» работают всегда.
    $ click_skip_block = True

    ## ══════════ КАДР 1 · ДВЕРЬ В СПАЛЬНЮ ══════════
    ## Из чёрного. Долгий наезд в дверной проём, к кровати.
    window auto hide

    ## Камера стоит до клика; явный трансформ сбрасывает наезд прошлой сцены и отдаёт
    ## зоне проёма (follow_camera) своё положение.
    camera at camera_push((0.72, 0.52), 1.0, 1.0, 0.0)
    scene black with Dissolve(2.0)
    scene chapter_1 scene_2_parents_room_door:
        breath_brightness(-0.03, -0.07, 6.0)
    with Dissolve(3.0)

    ## Клик по проёму: створка остаётся приоткрытой, начинается наезд.
    ## Блокировщик выше зоны проёма и съел бы клик по ней.
    $ click_skip_block = False
    if not renpy.is_skipping():
        call screen c1s2_door_hover_zone
    $ c1s2_door_open = True
    ## После закрытия экрана unhovered не приходит.
    $ c1s2_door_hover = False

    $ click_skip_block = True
    camera at camera_push((0.72, 0.52), 1.0, 1.15, 25.0)

    $ mplay("chapter_1/sora_chapter_start", fadein=0.0, volume=2.0, tag="chapter_1_music_1", loop=True)

    pause 1.5

    $ click_skip_block = False
    # "Я потеряла способность закрывать на эти мелочи глаза."
    # "А Витя не хотел понимать меня. Не воспринимал серьёзно."
    "Хуже всего было его полное нежелание понимать меня и серьёзно воспринимать мои проблемы со здоровьем."
    "Циклические депрессии, стоившие мне столько нервов и седых волос, он вообще не признавал настоящей болезнью."
    # "Так, бабья придурь, — полагал, вероятно, он. "

    # # под вопросом
    # "Сочувствие? Участие? Ха. Я не чувствовала от него никакой поддержки даже в самые тяжёлые для меня дни."

    # "Он, состроив скептическую мину, оплачивал психотерапевтов, да мог ещё время от времени рявкнуть, чтобы я “прекратила чёртову истерику”, на этом всё."
    # "Справляйся, Мариночка, сама, как знаешь."
    # "И не смей демонстрировать, что у тебя не всё так гладко, не нарушай семейную идиллию."

    ## Шаги Вити по коридору — на паузе перед его репликой.
    $ sm_sfx("c1s2/c1s2_footsteps")
    $ click_skip_block = True
    window auto hide
    pause 1.5
    $ click_skip_block = False

    vit "Доброе утро... А, ой, сейчас уже три часа дня!"

    ## ══════════ КАДР 2 · МАРИНА ══════════
    ## Наезд на лицо под ладонью.
    $ click_skip_block = True
    window auto hide
    camera at camera_push((0.17, 0.40), 1.03, 1.10, 28.0)
    ## Крупные планы Марины — без виньетки; она возвращается со следующим кадром.
    $ fx_vignette = False
    scene chapter_1 scene_2_marina_close:
        breath_brightness(-0.04, -0.09, 6.0)
    with Dissolve(3.5)

    $ c1s2_tear = True
    $ click_skip_block = False
    ## «Извини» — почти беззвучно: последнее движение рта убрано.
    mar "Я не могу подняться. Извини." (callback=talk_callback("mar", drop=1))
    vit "Просто бери пример с меня. Сделай над собой усилие..."

    $ click_skip_block = True
    pause 1.0
    $ click_skip_block = False

    "Я много раз предлагала мужу сходить к семейному психологу, но он, как типичный мужик, боялся терапии, словно огня. Смешно!"

    ## ══════════ КАДР 3 · ССОРА В СПАЛЬНЕ ══════════
    ## Один план и один наезд на весь разговор. Витя меняет позу через show без ATL:
    ## камера, дыхание и параллакс кадра не сбрасываются. Переход — renpy.transition по
    ## слою master: оператор with спрятал бы окно диалога посреди ссоры.
    $ click_skip_block = True
    window auto hide
    ## Долгий наезд на Марину — на весь разговор. Зум и сдвиг идут одним ease, поэтому край
    ## кадра не открывается.
    ## xoffset: лицо (x 864) съезжает к центру экрана; конечный = 96 * зум.
    ## yoffset: низ кадра стоит на нижней кромке экрана, кадр растёт вверх;
    ## на любом зуме = -540 * (зум - 1). Меньше по модулю — низ уезжает под экран.
    camera:
        subpixel True
        align (0.5, 0.5)
        rotate 0.0
        zoom 1.05 xoffset 2 yoffset -11
        ## При «меньше движения» наезда нет вовсе: кадр остаётся общим, Витя не уходит за край.
        pause (86400.0 * (1.0 - sm_motion_scale()))
        linear 50.0 zoom 1.5 xoffset 134 yoffset -246
    $ fx_vignette = True
    ## Виньетка на ссоре на 25% слабее (fx_frame); позы Вити меняются show без ATL — доля
    ## держится на весь разговор.
    scene chapter_1 scene_2_parents_room_vitya_1:
        parallel:
            breath_brightness(-0.04, -0.09, 6.0)
        parallel:
            fx_frame(vignette=0.75)
    with Dissolve(3.0)

    $ click_skip_block = False
    mar "Тамара Витальевна говорит, что ты тоже должен прийти. Семейная терапия..."
    vit "Мне то оно зачем? У меня-то с головой всё в порядке."

    $ click_skip_block = True
    pause 0.5
    $ click_skip_block = False

    mar "Это нелепо..."

    ## Переход позы длиной в паузу: клик оборвал бы его, блок при любой настройке.
    $ click_skip_block = "hard"
    pause 0.5

    ## ▶ Срывается на крик.
    $ renpy.transition(Dissolve(0.3), layer="master")
    show chapter_1 scene_2_parents_room_vitya_2

    pause 0.5

    $ mplay("chapter_1/sora_suspense_chapter_1", fadein=18.0, volume=0.9, tag="chapter_1_music_2")

    $ c1s2_vitya_shout = True
    $ click_skip_block = False
    vit "Знаешь что?! Хватит! Это невозможно."

    ## ▶ Обратно в позу 1: кадр перетёк в неё сам ещё на реплике, здесь поза закрепляется
    ## (и доигрывает переход, если кликнули раньше). Флаг не снимать: уходящий кадр на
    ## растворении снова показал бы крик.
    $ renpy.transition(Dissolve(0.2), layer="master")
    show chapter_1 scene_2_parents_room_vitya_1

    mar "О чём ты говоришь?!"

    $ click_skip_block = "hard"
    pause 0.1

    ## ▶ У кровати, разводит руками. Пауза после show — длиной в переход: Витя доходит до
    ## кровати, пока окна нет. Без неё переход позы накладывается на появление окна диалога
    ## и идёт рывком.
    $ renpy.transition(Dissolve(0.4), layer="master")
    show chapter_1 scene_2_parents_room_vitya_4
    pause 0.4
    $ click_skip_block = False

    vit "Сумасшедший дом..."
    vit "Только решёток на окнах нет. А стоило бы, да?"

    $ click_skip_block = True
    pause 0.5

    $ renpy.transition(Dissolve(0.3), layer="master")
    show chapter_1 scene_2_parents_room_vitya_4_1
    $ click_skip_block = False
    vit "Тамара не помогает! Не знал, что на болтовню с подружкой можно сжечь столько денег..."

    $ click_skip_block = True
    pause 0.5
    $ click_skip_block = False

    mar "Витя, это терапия... У меня есть диагноз."

    $ click_skip_block = True
    pause 0.5

    $ renpy.transition(Dissolve(0.3), layer="master")
    show chapter_1 scene_2_parents_room_vitya_5

    $ mstop(tag="chapter_1_music_1", fadeout=120.2)

    $ click_skip_block = False
    vit "Какой?!"
    vit "Тоска гробовая?"

    $ click_skip_block = True
    pause 0.5

    $ renpy.transition(Dissolve(0.2), layer="master")
    show chapter_1 scene_2_parents_room_vitya_3
    $ click_skip_block = False
    vit "Выйди на улицу. Перестань копаться в себе. Поговори с дочкой в конце концов!"

    ## ══════════ КАДР 4 · ЛАДОНИ ══════════
    ## Самый долгий наезд сцены: Марина прячется в ладонях, Витя говорит за кадром.
    $ click_skip_block = True
    window auto hide
    scene black with Dissolve(2.0)
    camera at camera_push((0.17, 0.45), 1.03, 1.18, 70.0)
    $ fx_vignette = False
    scene chapter_1 scene_2_marina_close_face:
        fade_brightness(-0.03, -0.11, 20.0)
    with Dissolve(2.0)

    $ click_skip_block = False
    "Мы ещё не заходили так далеко. Впервые за восемь лет брака."
    $ c1s2_tear_2 = True
    $ c1s2_crying_audio = sm_sfx("c1s2/c1s2_female_crying", volume=0.5, fadein=10.5, loop=True, tag="c1s2_crying")
    "Трещина между нами росла, дна не видно..."
    vit "Какой пример ты подаёшь Насте?"
    vit "Я тяну наше семейство, как могу. За всё плачу, всё покупаю, всё дома есть."
    vit "И прошу совсем немного! Здоровой атмосферы, счастливых лиц!"
    vit "Ты же знаешь... Я очень вас люблю..."

    ## Плач уходит вглубь, как метроном перед стуком: за duration секунд глохнет (low-pass,
    ## Гц) и обрастает эхом (wet — доля эха, dry — доля чистого звука).
    $ sm_audio_set_filter(c1s2_crying_audio, [
        renpy.audio.filter.Lowpass(2200.0),
        renpy.audio.filter.Reverb(resonance=0.72, dampening=2400.0, wet=0.60, dry=0.80, delay_multiplier=1.8),
        ], duration=16.0)

    $ click_skip_block = True
    pause 1.0

    ## ══════════ КАДР 5 · ТЕМНОТА ══════════
    ## Камера стоит, кадр сам медленно растёт. Дрожь ждёт флага c1s2_dark_shake.
    camera
    $ fx_vignette = True
    scene chapter_1 scene_2_dark:
        truecenter
        subpixel True
        zoom 1.0
        parallel:
            breath_brightness(-0.05, -0.09, 8.0)
        parallel:
            linear 30 zoom 1.13
        parallel:
            shake_grow(3, 15.0, start="c1s2_dark_shake")
    with Dissolve(3.0)

    $ click_skip_block = False
    $ c1s2_dark_shake = True

    "И я тебя, Вить... До сих пор."
    "А тогда я не смогла тебе ответить: меня ломало изнутри, я пряталась в собственных ладонях, как хочется спрятаться и сейчас."

    ## Титры печатаются по буквам и гаснут по флагам — блок при любой настройке.
    $ click_skip_block = "hard"
    pause 1.0

    ## Последняя фраза — не в окне, а титром лесенкой по центру: куски печатаются по буквам
    ## (slow_cps) и дрожат всё сильнее ({sc}, px). С появлением последнего гаснут все разом
    ## (fade_out_on: секунды, вспышка pulse) и догорают поверх головы в КАДРЕ 6.
    show expression prologue_title(_("{sc=1.3:2.5}И мне до сих пор мерещится...{/sc}"), 70, slow_cps=15, color="#ebebeb") as c1s2_whisper_1:
        anchor (0.0, 0.5) pos (370, 400)
        fade_out_on("c1s2_whisper_out", 7.0, faster="c1s2_whisper_rush", pulse=0.3, pulse_out=0.5)
    pause 2.5
    show expression prologue_title(_("{sc=2.5:4.5}что в этой темноте...{/sc}"), 70, slow_cps=15, color="#ebebeb") as c1s2_whisper_2:
        anchor (0.0, 0.5) pos (750, 520)
        fade_out_on("c1s2_whisper_out", 7.0, faster="c1s2_whisper_rush", pulse=0.3, pulse_out=0.5)
    pause 1.6
    show expression prologue_title(_("{sc=4.5:6.6}есть кто-то ещё.{/sc}"), 70, slow_cps=15, color="#ebebeb") as c1s2_whisper_3:
        anchor (0.0, 0.5) pos (1070, 640)
        fade_out_on("c1s2_whisper_out", 7.0, faster="c1s2_whisper_rush", pulse=0.3, pulse_out=0.5)
    $ c1s2_whisper_out = True
    pause 3.0

    ## ══════════ КАДР 6 · КТО-ТО ЕЩЁ ══════════
    ## Голова из пролога в темноте и шарканье. Тёмный кадр уходит через hide, а не scene:
    ## scene убрала бы и титры фразы, а они догорают поверх головы. Чёрная подложка
    ## закрывает углы под повёрнутой головой.
    ## Голова и шарканье идут под звук — блок при любой настройке.
    $ click_skip_block = "hard"

    ## Сам плач гаснет за cut секунд, его эхо — за fadeout; tail — секунды от этой строки
    ## до освобождения канала, запас на хвост эха.
    $ sm_audio_stop_tail(c1s2_crying_audio, cut=1.2, fadeout=2.0, tail=12.0)

    hide chapter_1
    show black behind c1s2_whisper_1
    show prologue_head_bg behind c1s2_whisper_1:
        truecenter
        zoom 1.0
        xpos 0.44 ypos 0.45
        parallel:
            breath_brightness(-0.15, -0.17, 1.0)
        parallel:
            shake_grow(3, 4.0)
        parallel:
            linear 26 zoom 1.43 rotate -25.0
    with Dissolve(1.5)

    $ mstop(fadeout=0.2)
    $ c1s2_whisper_rush = True

    pause 0.5

    $ sm_sfx("c1s2/c1s2_shakr_shark_shark", volume=1.7)

    pause 6.0

    camera
    scene black with Dissolve(2.0)

    ## ══════════ КАДР 7 · МАРИНА НА КРОВАТИ ══════════
    ## Обратный ход первого кадра: камера отъезжает от Марины к двери.
    camera at camera_settle((0.72, 0.58), 1.14, 1.02, 46.0)
    scene chapter_1 scene_2_parents_room_door_marina:
        breath_brightness(-0.04, -0.09, 6.0)
    with Dissolve(3.5)

    $ click_skip_block = False
    vit "Ладно, пойдём поедим. Я состряпаю чего-нибудь."
    mar "Л-ладно..."

    # ## ══════════ КАДР 8 · КУХНЯ ══════════
    # ## Наезд на Марину за столом.
    # $ click_skip_block = True
    # window auto hide
    # camera at camera_push((0.30, 0.50), 1.02, 1.08, 24.0)
    # scene chapter_1 scene_2_kitchen:
    #     breath_brightness(-0.03, -0.08, 6.0)
    # with Dissolve(2.0)

    # $ click_skip_block = False
    # "Наш брак давно был не идеален, понимала ли я это? Не совсем."
    # "После каждого такого скандала я старалась притворяться, подыгрывать."

## Бутерброды; отдельный вход каталога сцен.

label .sandwiches:

    $ fx_vignette = True

    ## ══════════ КАДР 9 · БУТЕРБРОДЫ ══════════
    ## Одна проводка слева направо с лёгким наездом — на весь кадр. Бутерброды исчезают
    ## внутри образа по счётчику c1s2_bite: каждый — посреди своей реплики, через случайные
    ## c1s2_bite_delay секунд после её начала. Без bloom: он плавно гаснет на растворении
    ## и возвращается на чёрном.
    $ click_skip_block = True
    $ fx_bloom_strength = 0.0
    $ c1s2_bite = 0
    window auto hide
    camera:
        parallel:
            camera_travel((0.465, 0.50), (0.57, 0.50), 1.08, 1.12, 40.0)
        parallel:
            linear 140.0 zoom 1.2
    scene chapter_1 scene_2_sandwiches:
        breath_brightness(-0.05, -0.09, 7.0)
    with Dissolve(4.0)

    $ click_skip_block = False

    "Наш брак давно был не идеален, понимала ли я это? Не совсем."
    "После каждого такого скандала я старалась притворяться, подыгрывать."

    $ click_skip_block = True
    pause 0.8
    $ click_skip_block = False

    $ c1s2_bite_delay = renpy.random.uniform(0.6, 2.4)
    $ c1s2_bite += 1
    "Для него, для Настеньки..."
    "...для себя."

    $ click_skip_block = True
    pause 0.8
    $ click_skip_block = False

    $ c1s2_bite_delay = renpy.random.uniform(0.6, 2.4)
    $ c1s2_bite += 1
    "Трещины можно спрятать. Сделать вид, что их нет."
    "Представить, что процесс разрушения остановлен."

    $ click_skip_block = True
    pause 0.8
    $ click_skip_block = False

    $ c1s2_bite_delay = renpy.random.uniform(0.6, 2.4)
    $ c1s2_bite += 1
    "Все ведь притворяются. Почему мы не могли?.."

    $ click_skip_block = True
    pause 0.8

    window auto hide
    scene black with Dissolve(2.0)
    $ fx_bloom_strength = FX_BLOOM_DEFAULT

    pause 0.6

    $ click_skip_block = False
    jump chapter_1_scene_3
