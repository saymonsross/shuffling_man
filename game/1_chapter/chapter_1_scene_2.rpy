## Глава 1, сцена 2: утро после ссоры → спальня → темнота под ладонями → кухня → бутерброды.

## Изображения

image chapter_1 scene_2_sandwiches_1 = At("images/1_chapter/owner_review/chapter_1_review_sandwiches stage_1.png", xysize(1920, 1080))
image chapter_1 scene_2_sandwiches_2 = At("images/1_chapter/owner_review/chapter_1_review_sandwiches stage_2.png", xysize(1920, 1080))
image chapter_1 scene_2_sandwiches_3 = At("images/1_chapter/owner_review/chapter_1_review_sandwiches stage_3.png", xysize(1920, 1080))

## Сцена

label chapter_1_scene_2:

    $ quick_menu = True

    ## ══════════ КАДР 1 · ДВЕРЬ В СПАЛЬНЮ ══════════
    ## Из чёрного. Долгий наезд в дверной проём, к кровати.
    window auto hide
    camera at camera_push((0.72, 0.52), 1.0, 1.12, 40.0)
    scene chapter_1 scene_2_parents_room_door:
        breath_brightness(-0.04, -0.09, 6.0)
    with Dissolve(3.0)

    "Я потеряла способность закрывать на эти мелочи глаза."
    "А Витя не хотел понимать меня. Не воспринимал серьёзно."
    vit "Доброе утро... А, ой, сейчас уже три часа дня!"

    ## ══════════ КАДР 2 · МАРИНА ══════════
    ## Наезд на лицо под ладонью.
    window auto hide
    camera at camera_push((0.17, 0.40), 1.03, 1.10, 28.0)
    scene chapter_1 scene_2_marina_close:
        breath_brightness(-0.04, -0.09, 6.0)
    with Dissolve(1.5)

    mar "Я не могу подняться. Извини."
    vit "Просто бери пример с меня. Сделай над собой усилие..."
    "Я много раз предлагала мужу сходить к семейному психологу, но он, как типичный мужик, боялся терапии, словно огня. Смешно!"

    ## ══════════ КАДР 3 · ВИТЯ НАД КРОВАТЬЮ ══════════
    ## Общий план: камера тянется между ним и Мариной.
    window auto hide
    camera at camera_push((0.30, 0.42), 1.02, 1.08, 20.0)
    scene chapter_1 scene_2_parents_room_vitya_1:
        breath_brightness(-0.04, -0.09, 6.0)
    with Dissolve(1.5)

    mar "Тамара Витальевна говорит, что ты тоже должен прийти. Семейная терапия..."
    vit "Нахуя? У меня-то с головой всё в порядке."

    ## ══════════ КАДР 4 · ССОРА ══════════
    ## Короткое растворение: Витя уже разводит руками. Один наезд на него — на всю ссору.
    window auto hide
    camera at camera_push((0.66, 0.30), 1.02, 1.16, 60.0)
    scene chapter_1 scene_2_parents_room_vitya_2:
        breath_brightness(-0.04, -0.09, 6.0)
    with Dissolve(0.5)

    mar "Это нелепо..."
    vit "Знаешь что? Хватит. Это невозможно."
    mar "О чём ты говоришь?!"
    vit "Сумасшедший дом. Только решёток на окнах нет. А стоило бы, да?"
    vit "Тамара не помогает! Не знал, что на болтовню с подружкой можно сжечь столько денег..."
    mar "Это терапия! У меня есть диагноз!"
    vit "Какой? Тоска гробовая?"
    vit "Выйди на улицу. Перестань копаться в себе. Поговори с дочкой в конце концов!"

    ## ══════════ КАДР 5 · ЛАДОНИ ══════════
    ## Самый долгий наезд сцены: Марина прячется в ладонях, Витя говорит за кадром.
    window auto hide
    camera at camera_push((0.17, 0.45), 1.03, 1.18, 70.0)
    scene chapter_1 scene_2_marina_hands:
        breath_brightness(-0.04, -0.09, 6.0)
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
