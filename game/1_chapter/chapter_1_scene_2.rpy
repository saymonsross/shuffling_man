## Глава 1, сцена 2.

## Изображения

image chapter_1 scene_2_sandwiches_1 = At("images/1_chapter/owner_review/chapter_1_review_sandwiches stage_1.png", xysize(1920, 1080))
image chapter_1 scene_2_sandwiches_2 = At("images/1_chapter/owner_review/chapter_1_review_sandwiches stage_2.png", xysize(1920, 1080))
image chapter_1 scene_2_sandwiches_3 = At("images/1_chapter/owner_review/chapter_1_review_sandwiches stage_3.png", xysize(1920, 1080))

label chapter_1_scene_2:

    camera
    scene chapter_1 scene_2_parents_room_door

    "Я потеряла способность закрывать на эти мелочи глаза."
    "А Витя не хотел понимать меня. Не воспринимал серьёзно."
    vit "Доброе утро... А, ой, сейчас уже три часа дня!"

    scene chapter_1 scene_2_marina_close

    mar "Я не могу подняться. Извини."
    vit "Просто бери пример с меня. Сделай над собой усилие..."
    "Я много раз предлагала мужу сходить к семейному психологу, но он, как типичный мужик, боялся терапии, словно огня. Смешно!"

    scene chapter_1 scene_2_parents_room_vitya_1

    mar "Тамара Витальевна говорит, что ты тоже должен прийти. Семейная терапия..."
    vit "Нахуя? У меня-то с головой всё в порядке."

    scene chapter_1 scene_2_parents_room_vitya_2

    mar "Это нелепо..."
    vit "Знаешь что? Хватит. Это невозможно."
    mar "О чём ты говоришь?!"
    vit "Сумасшедший дом. Только решёток на окнах нет. А стоило бы, да?"
    vit "Тамара не помогает! Не знал, что на болтовню с подружкой можно сжечь столько денег..."
    mar "Это терапия! У меня есть диагноз!"
    vit "Какой? Тоска гробовая?"
    vit "Выйди на улицу. Перестань копаться в себе. Поговори с дочкой в конце концов!"

    scene chapter_1 scene_2_marina_hands

    "Мы ещё не заходили так далеко. Впервые за восемь лет брака."
    "Трещина между нами росла, дна не видно..."
    vit "Какой пример ты подаёшь Насте?"
    vit "Я тяну наше семейство, как могу. За всё плачу, всё покупаю, всё дома есть."
    vit "И прошу совсем немного! Здоровой атмосферы, счастливых лиц!"
    vit "Ты же знаешь... Я очень вас люблю..."
    "И я тебя, Вить. До сих пор."
    "А тогда я не смогла тебе ответить: меня ломало изнутри, я пряталась в собственных ладонях, как хочется спрятаться и сейчас."

    scene chapter_1 scene_2_dark

    "В этой темноте есть кто-то ещё."

    scene chapter_1 scene_2_parents_room_door_marina

    vit "Ладно, пойдём поедим. Я состряпаю чего-нибудь."
    mar "Л-ладно..."

    scene chapter_1 scene_2_kitchen

    "Наш брак давно был не идеален, понимала ли я это? Не совсем."
    "После каждого такого скандала я старалась притворяться, подыгрывать."

label .sandwiches:

    scene chapter_1 scene_2_sandwiches

    "Для него, для Настеньки. Для себя."

    scene chapter_1 scene_2_sandwiches_1
    with Dissolve(0.22)

    "Трещины можно спрятать. Сделать вид, что их нет."

    scene chapter_1 scene_2_sandwiches_2
    with Dissolve(0.22)

    "Представить, что процесс разрушения остановлен."

    scene chapter_1 scene_2_sandwiches_3
    with Dissolve(0.22)

    "Все люди притворяются. Почему мы не могли?.."

    jump chapter_1_scene_3
