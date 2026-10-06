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
    ## Пробел и Enter — как клик по проёму; клик мышью мимо проёма ничего не делает.
    key "K_SPACE" action Return()
    key "K_RETURN" action Return()
    key "K_KP_ENTER" action Return()
    fixed:
        at follow_camera()
        button:
            area (930, 0, 305, 1080)
            background None
            alt _("Заглянуть в спальню")
            action Return()
            hovered [SetVariable("c1s2_door_hover", True), SPlay("c1s2/door_hover", volume=0.3)]
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

## Параллакс вдвое слабее обычного (step=0.5).
## Слой героини с момента, когда сцена взвела c1s2_vitya_hand, за 1.5 с растворяется в
## слой с рукой Вити на плече (FlagDissolve) и за те же 1.5 с перестаёт дрожать; остальные
## слои кадра не трогаются.
default c1s2_vitya_hand = False

image chapter_1 scene_2_marina_close_face = depth_scene(
    "ch1_2_mc_close_3_bg",
    (At(Fixed(FlagDissolve("ch1_2_mc_close_3_gg_2",
                "images/1_chapter/chapter_1 scene_2_parents_room/Ch1_2_MC_Close_3_gg withtitya_2.png",
                "c1s2_vitya_hand", 0.0, fade=1.5),
            At("ch1_2_mc_close_3_gg_2_tears",
                water(flow=(455, 602), start="c1s2_tear_2", run=15.0, hold=0.0, fade=6.0, fade_to=0.5)),
            xysize=(1920, 1080)),
        shake_grow(1.05, 20.0, stop="c1s2_vitya_hand", stop_fade=1.5)),
    At("ch1_2_mc_close_3_gg_2_hands", shake_grow(1.3, 20.0))), step=0.5)

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

## Крик («Знаешь что?! Хватит!»): кадр выглядит как поза 1, пока сцена не взвела
## c1s2_vitya_shout. С этого момента — с первой буквы реплики — сразу орущая поза, и через
## 1.5 с она сама растворяется обратно в позу 1, даже если реплика ещё идёт (FlagDissolve).
## Обе позы говорят кадрами (TalkFrames). В исходнике орущая поза нарисована рядом с
## позой 1 — offset ставит её на то же место.
default c1s2_vitya_shout = False

image chapter_1 scene_2_parents_room_vitya_2 = depth_scene(
    "ch1_2_parents_bg",
    FlagDissolve(
        FlagDissolve(
            TalkFrames("ch1_2_parents_vitya_1_say", "ch1_2_parents_vitya_1", "vit"),
            At(TalkFrames("ch1_2_parents_vitya_2", "ch1_2_parents_vitya_2_say", "vit", fade=0.1, hold=0.18, gap=0.135),
                offset(-139, 0)),
            "c1s2_vitya_shout", 0.0, fade=0.2),
        TalkFrames("ch1_2_parents_vitya_1_say", "ch1_2_parents_vitya_1", "vit"),
        "c1s2_vitya_shout", 1.5, fade=0.4),
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
        hflip, offset(-35, 13)),
    "c1s2_parents_bed", step=0)
image chapter_1 scene_2_parents_room_vitya_4_1 = depth_scene(
    "ch1_2_parents_bg",
    At(TalkFrames(At("ch1_2_parents_vitya_3", offset(223, 0)), "ch1_2_parents_vitya_4", "vit"),
        hflip, offset(15, 5), rotate(-2), zoom(1.02)),
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

    $ mplay("chapter_1/sora_chapter_start", fadein=0.0, tag="chapter_1_music_1", loop=True)

    pause 1.5

    $ click_skip_block = False
    # "Я потеряла способность закрывать на эти мелочи глаза."
    # "А Витя не хотел понимать меня. Не воспринимал серьёзно."
    "Хуже всего было Витино полное нежелание понимать меня и серьёзно воспринимать мои проблемы со здоровьем."
    "Циклические депрессии, стоившие мне столько нервов и седых волос, он вообще не признавал настоящей болезнью."
    # "Так, бабья придурь, — полагал, вероятно, он. "

    # # под вопросом
    # "Сочувствие? Участие? Ха. Я не чувствовала от него никакой поддержки даже в самые тяжёлые для меня дни."

    # "Он, состроив скептическую мину, оплачивал психотерапевтов, да мог ещё время от времени рявкнуть, чтобы я “прекратила чёртову истерику”, на этом всё."
    # "Справляйся, Мариночка, сама, как знаешь."
    # "И не смей демонстрировать, что у тебя не всё так гладко, не нарушай семейную идиллию."

    ## Шаги Вити по коридору — на паузе перед его репликой.
    $ sm_sfx("c1s2/c1s2_footsteps")
    window auto hide
    pause 1.3

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

    pause 0.8

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
    mar "Тамара Виталиевна говорит, что ты тоже должен прийти. Семейная терапия..."
    vit "Мне-то она зачем? У меня с головой всё в порядке."

    pause 0.5

    mar "Это нелепо..."

    $ click_skip_block = True
    pause 0.8

    ## ▶ Срывается на крик — орущая поза встаёт с первой буквой реплики и через 1.5 с
    ## уходит сама. Кадр крика до флага выглядит как поза 1: подмена незаметна.
    show chapter_1 scene_2_parents_room_vitya_2
    $ mplay("chapter_1/sora_suspense_chapter_1", fadein=18.0, volume=0.9, tag="chapter_1_music_2")
    $ c1s2_vitya_shout = True
    $ click_skip_block = False
    ## Крик — три одинаковых раскрытия рта подряд, как у соседки в сцене 3, на 10% быстрее;
    ## кончаются к 0.8 с — поза уходит в 1.5 с уже с закрытым ртом.
    vit "Знаешь что?! Хватит!" (callback=talk_callback("vit", moves=3, hold=0.18, step=0.315))

    ## ▶ Поза 1 закрепляется. Если реплику пролистнули раньше 1.5 с — начатое раскрытие рта
    ## доигрывает и закрывается (до 0.28 с), и только потом поза доходит растворением.
    $ click_skip_block = "hard"
    pause 0.3
    $ click_skip_block = False
    $ renpy.transition(Dissolve(0.3), layer="master")
    show chapter_1 scene_2_parents_room_vitya_1

    ## Медленнее обычного: говорит, остывая.
    vit "Это невозможно." (callback=talk_callback("vit", rate=0.7))

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

    pause 0.5

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
    $ c1s2_crying_audio = sm_sfx("c1s2/c1s2_female_crying", volume=0.5, fadein=10.5, loop=True, tag="c1s2_crying")
    "Мы ещё не заходили так далеко. Ни разу за восемь лет брака."
    $ c1s2_tear_2 = True
    "Трещина между нами росла, дна не видно..."

    pause 0.5

    vit "Какой пример ты подаёшь Насте?"
    vit "Я тяну наше семейство, как могу. За всё плачу, всё покупаю, всё дома есть."
    vit "И прошу совсем немного! Здоровой атмосферы, счастливых лиц!"

    $ click_skip_block = True
    pause 0.5

    ## Рука Вити ложится на плечо: слой героини перетекает за 1.5 с, реплика — когда рука легла.
    $ c1s2_vitya_hand = True

    pause 1.5
    $ click_skip_block = False

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
    "А тогда я не смогла тебе ответить: меня ломало изнутри."
    "Я пряталась в темноте своих ладоней, как хочется спрятаться и сейчас."
    
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

    ## Тема финала сцены — без fadein; гасит её общий mstop перед последней репликой бутербродов.
    $ mplay("chapter_1/after_sora_sound", fadein=0.0, tag="chapter_1_music_after_sora", loop=True)

    pause 0.5

    mar "Х-хорошо..."

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
            camera_travel((0.465, 0.50), (0.62, 0.50), 1.08, 1.12, 50.0)
        parallel:
            linear 140.0 zoom 1.2
    scene chapter_1 scene_2_sandwiches:
        breath_brightness(-0.05, -0.09, 7.0)
    with Dissolve(4.0)

    $ click_skip_block = False

    "Наш брак давно был не идеален."
    "Понимала ли я это? Не совсем."
    "После каждого такого скандала я старалась притворяться, подыгрывать."

    pause 0.8

    $ c1s2_bite_delay = renpy.random.uniform(0.6, 2.4)
    $ c1s2_bite += 1
    "Для него, для Настеньки..."
    "...для себя."

    pause 0.8

    $ c1s2_bite_delay = renpy.random.uniform(0.6, 2.4)
    $ c1s2_bite += 1
    "Трещины можно спрятать. Сделать вид, что их нет."
    "Представить, что процесс разрушения остановлен."

    pause 0.8

    $ mstop(fadeout=7.2)

    $ c1s2_bite_delay = renpy.random.uniform(0.6, 2.4)
    $ c1s2_bite += 1
    "Все ведь притворяются. Почему мы не могли?.."

    $ click_skip_block = True
    pause 0.8

    window auto hide
    scene black:
        zoom 2.0        
    with Dissolve(2.0)
    $ fx_bloom_strength = FX_BLOOM_DEFAULT

    pause 0.6

    $ click_skip_block = False
    jump chapter_1_scene_3
