## Глава 1, сцена 2: утро после ссоры → спальня → темнота под ладонями → кухня → бутерброды.

## Изображения

image chapter_1 scene_2_sandwiches_1 = At("images/1_chapter/owner_review/chapter_1_review_sandwiches stage_1.png", xysize(1920, 1080))
image chapter_1 scene_2_sandwiches_2 = At("images/1_chapter/owner_review/chapter_1_review_sandwiches stage_2.png", xysize(1920, 1080))
image chapter_1 scene_2_sandwiches_3 = At("images/1_chapter/owner_review/chapter_1_review_sandwiches stage_3.png", xysize(1920, 1080))

## Спальня из коридора — планы глубины (depth_scene, common/parallax.rpy): задник комнаты,
## перед ним стена слева и створка справа. По наведению на проём (c1s2_door_hover) комната
## чуть светлеет, а закрытая створка гаснет (flag_fade), открывая приоткрытую, которая всегда
## лежит под ней. Клик по проёму замораживает это состояние (c1s2_door_open) до конца кадра.
default c1s2_door_hover = False
default c1s2_door_open = False

image c1s2_door_bg_lit = At("chapter_1_scene_2_parents_room_door_1_in", brightness(0.08))
image chapter_1 scene_2_parents_room_door = depth_scene(
    ("chapter_1_scene_2_parents_room_door_1_in",
        At("c1s2_door_bg_lit", flag_fade((0, 0), ("c1s2_door_hover", "c1s2_door_open")))),
    ("chapter_1_scene_2_parents_room_door_left_wall",
        "chapter_1_scene_2_parents_room_door_right_open",
        At("chapter_1_scene_2_parents_room_door_right_close",
            flag_fade((0, 0), ("c1s2_door_hover", "c1s2_door_open"), False))))

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

## Марина крупно — планы глубины: задник; перед ним героиня и слеза на её щеке (water).
## Слеза стекает от века до капли у губ: flow — этот участок слоя по вертикали, px.
## Стартует через 2 с после реплики, перед которой сцена взводит c1s2_tear.
default c1s2_tear = False

image chapter_1 scene_2_marina_close = depth_scene(
    "ch1_2_mc_close_3_bg",
    ("ch1_2_mc_close_3_gg",
        At("ch1_2_mc_close_3_gg_tears", water(flow=(455, 602), start="c1s2_tear", delay=2.0))))

## Руки на лице дрожат всё сильнее: от нуля до 0.1 px за 20 с с момента показа кадра.
image chapter_1 scene_2_marina_close_face = depth_scene(
    "ch1_2_mc_close_3_bg",
    (At("ch1_2_mc_close_3_gg_2", shake_grow(1.05, 20.0)),
    At("ch1_2_mc_close_3_gg_2_hands", shake_grow(1.3, 20.0)))
    )

## Спальня, общий план — слои: задник (пол и стена), Витя, кровать с Мариной. step=0 —
## слои склеены в один план: фигуры стоят вплотную, глубина между ними ломала бы кадр;
## за мышью кадр едет целиком.
## Кровать с Мариной. На её репликах губы чуть приоткрываются 1.5 с: сцена перед каждой
## делает $ c1s2_marina_talk += 1 (mouth_talk — эллипс рта в px картинки, сила отрицательная).
default c1s2_marina_talk = 0

image c1s2_parents_bed = At("ch1_2_parents_krovvat_gg",
    mouth_talk((864, 641), (20, 11), time=1.5, start="c1s2_marina_talk", strength=-1.0))

## Образы отличаются только Витей. Позы парные: 1 и 2 — у двери, 3 и 4 — за кроватью;
## в исходниках пары нарисованы рядом, offset ставит вторую позу на место первой.
## Поза 1 в двух вариантах: рот закрыт и говорит. Разговор — покадровый: слои «зубы» и
## «рот закрыт» меняются туда-сюда по слогам ~2.5 с с момента показа и замирают на
## закрытом. Имена файлов перепутаны относительно содержимого: зубы — ch1_2_parents_vitya_1.
## При «меньше движения» рот не мелькает.
image c1s2_vitya_1_talk_anim:
    block:
        "ch1_2_parents_vitya_1"
        pause 0.13
        "ch1_2_parents_vitya_1_say"
        pause 0.09
        "ch1_2_parents_vitya_1"
        pause 0.16
        "ch1_2_parents_vitya_1_say"
        pause 0.11
        repeat 5
image c1s2_vitya_1_talk = ConditionSwitch(
    "sm_reduced_motion()", "ch1_2_parents_vitya_1",
    "True", "c1s2_vitya_1_talk_anim")
image chapter_1 scene_2_parents_room_vitya_1_say = depth_scene(
    "ch1_2_parents_bg", "c1s2_vitya_1_talk", "c1s2_parents_bed", step=0)
image chapter_1 scene_2_parents_room_vitya_1 = depth_scene(
    "ch1_2_parents_bg", "ch1_2_parents_vitya_1_say", "c1s2_parents_bed", step=0)
## В этой позе он орёт: рот двигается 3 с от реплики, перед которой сцена взводит
## c1s2_vitya_shout (mouth_talk — эллипс рта в px картинки). Через те же 3 с, ещё на этой
## реплике, орущая поза сама растворяется в позу 1 (FlagDissolve).
default c1s2_vitya_shout = False

image chapter_1 scene_2_parents_room_vitya_2 = depth_scene(
    "ch1_2_parents_bg",
    FlagDissolve(
        At("ch1_2_parents_vitya_2", mouth_talk((426, 213), (26, 19), time=3.0, start="c1s2_vitya_shout"),
            offset(-139, 0)),
        "ch1_2_parents_vitya_1_say", "c1s2_vitya_shout", 3.0, fade=0.2),
    "c1s2_parents_bed", step=0)
## Позы у кровати. Рот Вити двигается на каждой его реплике сам (ключ "vit" в characters.rpy):
## орущая поза — деформацией рта (mouth_talk), позы с разведёнными руками — сменой кадров:
## слои vitya_3 (рот закрыт) и vitya_4 (говорит) — одна поза, в исходнике в 223 px друг от
## друга, отличаются только ртом (TalkFrames). Пока он молчит, рот закрыт.
## Ноги у слоёв 3 и 4 не дорисованы и должны оставаться за кроватью.
image chapter_1 scene_2_parents_room_vitya_3 = depth_scene(
    "ch1_2_parents_bg",
    At("ch1_2_parents_vitya_2", mouth_talk((426, 213), (26, 19), who="vit"), offset(653 - 400, 0)),
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

    $ quick_menu = True

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
    if not renpy.is_skipping():
        call screen c1s2_door_hover_zone
    $ c1s2_door_open = True
    ## После закрытия экрана unhovered не приходит.
    $ c1s2_door_hover = False

    camera at camera_push((0.72, 0.52), 1.0, 1.15, 25.0)

    "Я потеряла способность закрывать на эти мелочи глаза."
    "А Витя не хотел понимать меня. Не воспринимал серьёзно."

    window auto hide
    pause 1.5

    vit "Доброе утро... А, ой, сейчас уже три часа дня!"

    ## ══════════ КАДР 2 · МАРИНА ══════════
    ## Наезд на лицо под ладонью.
    window auto hide
    camera at camera_push((0.17, 0.40), 1.03, 1.10, 28.0)
    scene chapter_1 scene_2_marina_close:
        breath_brightness(-0.04, -0.09, 6.0)
    with Dissolve(1.5)

    $ c1s2_tear = True
    mar "Я не могу подняться. Извини."
    vit "Просто бери пример с меня. Сделай над собой усилие..."
    "Я много раз предлагала мужу сходить к семейному психологу, но он, как типичный мужик, боялся терапии, словно огня. Смешно!"

    ## ══════════ КАДР 3 · ССОРА В СПАЛЬНЕ ══════════
    ## Один план и один наезд на весь разговор. Витя меняет позу через show без ATL:
    ## камера, дыхание и параллакс кадра не сбрасываются. Переход — renpy.transition по
    ## слою master: оператор with спрятал бы окно диалога посреди ссоры.
    window auto hide
    ## Долгий наезд на Марину — на весь разговор, не дальше 1.4. Зум и сдвиг идут одним
    ## ease, поэтому край кадра не открывается.
    ## xoffset: лицо (x 864) съезжает к центру экрана; конечный = 96 * зум.
    ## yoffset: низ кадра стоит на нижней кромке экрана, кадр растёт вверх;
    ## на любом зуме = -540 * (зум - 1). Меньше по модулю — низ уезжает под экран.
    camera:
        subpixel True
        align (0.5, 0.5)
        rotate 0.0
        zoom 1.05 xoffset 2 yoffset -11
        ease sm_motion_time(44.0) zoom 1.4 xoffset 134 yoffset -216
    scene chapter_1 scene_2_parents_room_vitya_1:
        breath_brightness(-0.04, -0.09, 6.0)
    with Dissolve(1.5)

    $ c1s2_marina_talk += 1
    mar "Тамара Витальевна говорит, что ты тоже должен прийти. Семейная терапия..."

    ## ▶ ПОЗА 2 — шагнул к кровати, орёт.
    $ renpy.transition(Dissolve(0.2), layer="master")
    show chapter_1 scene_2_parents_room_vitya_1_say

    vit "Мне то оно зачем? У меня-то с головой всё в порядке."

    ## ▶ ПОЗА 3 — за спиной Марины, разводит руками.
    $ renpy.transition(Dissolve(0.2), layer="master")
    show chapter_1 scene_2_parents_room_vitya_1

    $ c1s2_marina_talk += 1
    mar "Это нелепо..."

    pause 0.5

    $ renpy.transition(Dissolve(0.3), layer="master")
    show chapter_1 scene_2_parents_room_vitya_2

    pause 0.5

    $ c1s2_vitya_shout = True
    vit "Знаешь что? Хватит. Это невозможно."

    ## ▶ Обратно в позу 1: через 3 с реплики кадр уже перетёк в неё сам, здесь поза
    ## закрепляется (и доигрывает переход, если кликнули раньше). Флаг не снимать: уходящий
    ## кадр на растворении снова показал бы крик.
    $ renpy.transition(Dissolve(0.2), layer="master")
    show chapter_1 scene_2_parents_room_vitya_1

    $ c1s2_marina_talk += 1
    mar "О чём ты говоришь?!"

    pause 0.5

    ## ▶ ПОЗА 4 — обошёл кровать, выговаривает.
    $ renpy.transition(Dissolve(0.3), layer="master")
    show chapter_1 scene_2_parents_room_vitya_4

    vit "Сумасшедший дом..."
    vit "Только решёток на окнах нет. А стоило бы, да?"

    pause 0.5
    $ renpy.transition(Dissolve(0.3), layer="master")
    show chapter_1 scene_2_parents_room_vitya_4_1
    vit "Тамара не помогает! Не знал, что на болтовню с подружкой можно сжечь столько денег..."

    pause 0.5

    $ c1s2_marina_talk += 1
    mar "Витя, это терапия... У меня есть диагноз."

    pause 0.5

    $ renpy.transition(Dissolve(0.3), layer="master")
    show chapter_1 scene_2_parents_room_vitya_5

    vit "Какой?!"
    vit "Тоска гробовая?"

    pause 0.5

    $ renpy.transition(Dissolve(0.2), layer="master")
    show chapter_1 scene_2_parents_room_vitya_3    
    vit "Выйди на улицу. Перестань копаться в себе. Поговори с дочкой в конце концов!"

    ## ══════════ КАДР 5 · ЛАДОНИ ══════════
    ## Самый долгий наезд сцены: Марина прячется в ладонях, Витя говорит за кадром.
    window auto hide
    scene black with Dissolve(2.0)
    camera at camera_push((0.17, 0.45), 1.03, 1.18, 70.0)
    scene chapter_1 scene_2_marina_close_face:
        fade_brightness(-0.01, -0.13, 20.0)
    with Dissolve(2.0)


    "Мы ещё не заходили так далеко. Впервые за восемь лет брака."
    "Трещина между нами росла, дна не видно..."
    vit "Какой пример ты подаёшь Насте?"
    vit "Я тяну наше семейство, как могу. За всё плачу, всё покупаю, всё дома есть."
    vit "И прошу совсем немного! Здоровой атмосферы, счастливых лиц!"
    vit "Ты же знаешь... Я очень вас люблю..."
    "И я тебя, Вить. До сих пор."

    ## Кадр темнеет до нижней границы и замирает: дальше — темнота под ладонями.
    show chapter_1 scene_2_marina_hands:
        brightness_to(-0.09, 5.0)

    "А тогда я не смогла тебе ответить: меня ломало изнутри, я пряталась в собственных ладонях, как хочется спрятаться и сейчас."

    ## ══════════ КАДР 6 · ТЕМНОТА ══════════
    ## Единственный кадр без движения камеры.
    window auto hide
    camera
    scene chapter_1 scene_2_dark:
        breath_brightness(-0.05, -0.09, 8.0)
    with Dissolve(3.0)

    pause 1.0

    "В этой темноте есть кто-то ещё."

    window auto hide

    pause 1.0

    ## ══════════ КАДР 7 · МАРИНА НА КРОВАТИ ══════════
    ## Обратный ход первого кадра: камера отъезжает от Марины к двери.
    camera at camera_settle((0.72, 0.58), 1.14, 1.02, 16.0)
    scene chapter_1 scene_2_parents_room_door_marina:
        breath_brightness(-0.04, -0.09, 6.0)
    with Dissolve(2.5)

    vit "Ладно, пойдём поедим. Я состряпаю чего-нибудь."
    mar "Л-ладно..."

    ## ══════════ КАДР 8 · КУХНЯ ══════════
    ## Наезд на Марину за столом.
    window auto hide
    camera at camera_push((0.30, 0.50), 1.02, 1.08, 24.0)
    scene chapter_1 scene_2_kitchen:
        breath_brightness(-0.03, -0.08, 6.0)
    with Dissolve(2.0)

    "Наш брак давно был не идеален, понимала ли я это? Не совсем."
    "После каждого такого скандала я старалась притворяться, подыгрывать."

## Бутерброды; отдельный вход каталога сцен.

label .sandwiches:

    ## ══════════ КАДР 9 · БУТЕРБРОДЫ ══════════
    ## Один наезд на тарелку — через все четыре кадра. Бутерброды исчезают по репликам:
    ## show без ATL оставляет кадру его дыхание, камера не сбрасывается.
    window auto hide
    camera at camera_push((0.35, 0.50), 1.02, 1.12, 40.0)
    scene chapter_1 scene_2_sandwiches:
        breath_brightness(-0.03, -0.08, 6.0)
    with Dissolve(1.0)

    "Для него, для Настеньки. Для себя."

    show chapter_1 scene_2_sandwiches_1
    with Dissolve(0.22)

    "Трещины можно спрятать. Сделать вид, что их нет."

    show chapter_1 scene_2_sandwiches_2
    with Dissolve(0.22)

    "Представить, что процесс разрушения остановлен."

    show chapter_1 scene_2_sandwiches_3
    with Dissolve(0.22)

    "Все люди притворяются. Почему мы не могли?.."

    window auto hide
    scene black with Dissolve(2.0)

    pause 0.6

    jump chapter_1_scene_3
