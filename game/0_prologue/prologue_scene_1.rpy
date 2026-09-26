## Пролог: титры → тёмная комната → воспоминание → начало письма.

## Изображения

image prologue_dark_room = "images/0_prologue/prologue dark_room.png"

## Моргание играет внутри образа и не останавливает реплики; трансформ тега сохраняется.
image prologue head_blink:
    "prologue head"
    pause 0.1
    "prologue head_flick" with Dissolve(0.2)
    pause 0.6
    "prologue head" with Dissolve(0.2)

## prologue_note_center — референс; сцена собирается из отдельных частей.
image prologue_note_center = "images/0_prologue/prologue_note center.jpg"
image prologue_note_bg = "images/0_prologue/prologue_hand anim bg.png"
image prologue_note_paper = "images/0_prologue/prologue_note_paper.png"
image prologue_note_pencil = hover_lit("images/0_prologue/prologue_note_pencil.png", "note_hover_pencil", 0.35)

image prologue_pencil_close = "images/0_prologue/prologue pencil_close.png"

image prologue_hand_left = "images/0_prologue/prologue_hand_left.png"
image prologue_hand_right = "images/0_prologue/prologue_hand_right rest.png"
image prologue_hand_right_move = "images/0_prologue/prologue_hand_right move.png"
image prologue_hand_right_write = "images/0_prologue/prologue_hand_right write.png"

## Стили, переходы, состояние

style prologue_titles_text is default:
    color "#ff0000"
    outlines [(2, "#1a1712d9", 0, 0)]
    slow_cps 0

define prologue_dissolve = Dissolve(1.2)

default note_hover_pencil = False

## Вступительные титры

label prologue_titles:

    "start"

    $ quick_menu = False
    $ sm_parallax_off = True

    $ mplay("opening/opening_titles", fadein=4.0)

    scene black with Dissolve(1.0)

    pause 1.0

    show expression Text(_("HINTERLAND MOOD"), style="prologue_titles_text", size=130) as prologue_titles_text:
        align (0.5, 0.5)
        subpixel True
    with Dissolve(2.0)

    pause 3.0

    hide prologue_titles_text with Dissolve(2.0)

    pause 1.0

    show expression Text(_("ПО РАССКАЗУ РОМАНА ЧЕРНОГО"), style="prologue_titles_text", size=50) as prologue_titles_text_2:
        align (0.5, 0.5)
        subpixel True
    with Dissolve(3.0)

    pause 3.0

    jump prologue_scene_1

## Сцена

label prologue_scene_1:

    $ auto_hide()

    scene black with Dissolve(3.0)

    $ quick_menu = True
    $ sm_parallax_off = False

    pause 1.0

    scene prologue_dark_room with Dissolve(5.0):
        zoom 1.0
        truecenter
        subpixel True
        parallel:
            linear 30.5 zoom 1.05
        parallel:    
            linear 6.0 matrixcolor BrightnessMatrix(0.0)
            linear 6.0 matrixcolor BrightnessMatrix(-0.03)
            repeat

    $ mplay("opening/prologue_1", fadein=10.0, fadeout=18.0)

    "Чтобы заговорить о чём-то тяжёлом, лучше всего для начала представиться."

    show prologue head:
        zoom 1.0 alpha 0.0
        truecenter
        subpixel True
        parallel:
            linear 36.5 zoom 1.2
        parallel:
            linear 8.0 alpha 1.0

    ## Новый ATL наследует текущий zoom комнаты: наезд продолжается без скачка.
    show prologue_dark_room:
        blur 0.0 matrixcolor BrightnessMatrix(0.0)
        parallel:
            linear 25.0 zoom 1.05
        parallel:
            linear 11.0 blur 3.0 matrixcolor BrightnessMatrix(-0.25)

    "Так сказать.."
    "...вспомнить, кто ты есть."

    # window hide

    show prologue_head_bg behind prologue:
        zoom 1.0 alpha 0.0
        parallel:
            linear 50.5 zoom 1.2
        parallel:
            linear 4.0 alpha 1.0

    "Меня зовут Марина Александровна Шрайбер."
    
    show prologue head_blink

    "Я пишу эти строки не в первый раз."

    "Я нахожусь довольно далеко от места, что называла домом."

    "Сейчас у меня нет дома."

    show prologue head_blink

    "Кажется, осталось позади всё, что было мне ценно."

    scene prologue_dark_room with Dissolve(3.0):
        zoom 1.0
        truecenter
        subpixel True
        linear 30.5 zoom 1.05

    "Я здесь после нервного срыва, что разрушил мою и без того распадавшуюся на части жизнь и подорванное здоровье."

    "Это письмо..."
    "...должно помочь мне пережить произошедшее."

    jump prologue_scene_2
