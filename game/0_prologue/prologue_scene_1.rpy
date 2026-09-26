## Пролог: тёмная комната → записка → воспоминание → начало письма.

## Изображения

image prologue_dark_room = "images/0_prologue/prologue dark_room.png"
image prologue_head = "images/0_prologue/prologue head.png"

## prologue_note_center — референс; сцена собирается из отдельных частей.
image prologue_note_center = "images/0_prologue/prologue_note center.png"
image prologue_note_bg = "images/0_prologue/prologue_hand anim bg.png"
image prologue_note_paper = "images/0_prologue/prologue_note_paper.png"
image prologue_note_pencil = hover_lit("images/0_prologue/prologue_note_pencil.png", "note_hover_pencil", 0.35)

image prologue_pencil_close = "images/0_prologue/prologue pencil_close.png"

image prologue_hand_left = "images/0_prologue/prologue_hand_left.png"
image prologue_hand_right = "images/0_prologue/prologue_hand_right rest.png"
image prologue_hand_right_move = "images/0_prologue/prologue_hand_right move.png"
image prologue_hand_right_write = "images/0_prologue/prologue_hand_right write.png"

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

    "start"

    scene black with Dissolve(3.0)

    pause 1.0

    scene prologue_dark_room with Dissolve(5.0):
        zoom 1.0
        truecenter
        subpixel True
        linear 30.5 zoom 1.05

    "Чтобы заговорить о чём-то тяжёлом, лучше всего для начала представиться."

    "Так сказать, вспомнить, кто ты есть."

    scene prologue_head with Dissolve(2.0):
        zoom 1.0
        truecenter
        subpixel True
        linear 30.5 zoom 1.15
    

    "Меня зовут Марина Александровна Шрайбер.\nЯ пишу эти строки не в первый раз."

    "Я нахожусь довольно далеко от места, что называла домом."

    "Сейчас у меня нет дома."

    "Кажется, осталось позади всё, что было мне ценно."

    "Я здесь после нервного срыва, что разрушил мою и без того распадавшуюся на части жизнь и подорванное здоровье."

    "Это письмо... должно помочь мне пережить произошедшее."

    return
