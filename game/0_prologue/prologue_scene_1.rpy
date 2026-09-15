## Пролог: тёмная комната → записка → воспоминание → начало письма.

## Изображения

image prologue_dark_room = "images/0_prologue/prologue dark_room.jpg"
image prologue_head = "images/0_prologue/prologue head.jpg"

## prologue_note_center — референс; сцена собирается из отдельных частей.
image prologue_note_center = "images/0_prologue/prologue_note center.jpg"
image prologue_note_bg = "images/0_prologue/prologue_note bg.jpg"
image prologue_note_paper = "images/0_prologue/prologue_note_paper.png"
image prologue_note_pencil = hover_lit("images/0_prologue/prologue_note_pencil.png", "note_hover_pencil", NOTE_HOVER_BRIGHTNESS)

image prologue_pencil_close = "images/0_prologue/prologue pencil_close.jpg"

image prologue_hand_left = "images/0_prologue/prologue_hand_left.png"
image prologue_hand_right = "images/0_prologue/prologue_hand_right rest.png"
image prologue_hand_right_move = "images/0_prologue/prologue_hand_right move.png"
image prologue_hand_right_write = "images/0_prologue/prologue_hand_right write.png"

## Константы сцены

## Покачивание камеры на кадрах с затылком.
define PROLOGUE_SWAY_DRIFT = 12.0   # px
define PROLOGUE_SWAY_TILT = 0.6     # градусы

## Параллакс за мышкой на сцене записки.
define NOTE_PARALLAX = 10.0
define NOTE_PARALLAX_SMOOTH = 0.06

define NOTE_HAND_LEFT_POS = (310, 391)
define NOTE_HAND_RIGHT_POS = (1358, 468)

define NOTE_HOVER_BRIGHTNESS = 0.35
define NOTE_START_BUTTON_SIZE = (260, 140)

define NOTE_PAPER_NEAT_POS = (990, 455)
define NOTE_PENCIL_NEAT_POS = (1264, 431)

## Разные холсты поз совмещены по кончику карандаша.
define NOTE_HAND_AT_PENCIL_POS = (1237, 211)
define NOTE_HAND_WRITE_GRIP_POS = (1237, 211)
define NOTE_HAND_REACH_T = 0.9   # синхронно с pause после show
define NOTE_HAND_HOVER_T = 0.5

## Движение к началу первой строки — в системе координат write-позы.
define NOTE_HAND_LINE_START_POS = (767, 158)
define NOTE_HAND_TO_LINE_T = 1.1

define NOTE_HAND_JITTER_AMP = 3.0      # px
define NOTE_WRITE_TENSION_NOISE = 0.2

define PENCIL_CLOSE_SHAKE_AMP = 1.5

## Образы и трансформы

transform prologue_slow_zoom:
    subpixel True
    xalign 0.5 yalign 0.45 zoom 1.0
    ease sm_motion_time(22.0) zoom 1.25

define prologue_fade_in = Dissolve(4.0)
define prologue_dissolve = Dissolve(1.2)

default note_hover_pencil = False

## Сцена

label prologue_scene_1:

    scene black

    scene prologue_dark_room at prologue_slow_zoom
    with prologue_fade_in

    "Чтобы заговорить о чём-то тяжёлом, лучше всего для начала представиться."

    "Так сказать, вспомнить, кто ты есть."

    scene prologue_head at uneasy_sway(PROLOGUE_SWAY_DRIFT, PROLOGUE_SWAY_TILT)
    with prologue_dissolve

    "Меня зовут Марина Александровна Шрайбер.\nЯ пишу эти строки не в первый раз."

    "Я нахожусь довольно далеко от места, что называла домом."

    "Сейчас у меня нет дома."

    "Кажется, осталось позади всё, что было мне ценно."

    "Я здесь после нервного срыва, что разрушил мою и без того распадавшуюся на части жизнь и подорванное здоровье."

    "Это письмо... должно помочь мне пережить произошедшее."

    return
