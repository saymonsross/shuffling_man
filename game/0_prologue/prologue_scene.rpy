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

## Экраны

screen prologue_note_start():
    modal True
    use sm_skippable_interaction
    ## Камера здесь сброшена; координаты совпадают с положением карандаша,
    ## а контейнер повторяет параллакс слоя master.
    fixed:
        at parallax_follow()
        xysize (config.screen_width, config.screen_height)
        use glow_button(
            _("Взять ручку"),
            Return("done"),
            bg="light",
            pos=(1264, 431),
            size=(260, 140),
            hovered=[SetVariable("note_hover_pencil", True), SPlay("click")],
            unhovered=SetVariable("note_hover_pencil", False))

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

    jump prologue_scene

## Сцена

label prologue_scene:

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

    ## Голова — ближний план. Картинка упирается в края кадра: стартовый зум 1.05
    ## закрывает сдвиг parallax.near до 48 px, при большем near поднять.
    show prologue head:
        zoom 1.05 alpha 0.0
        truecenter
        subpixel True
        parallel:
            function parallax_near_f
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
    ## Без стартовых значений: zoom и alpha наследуются, фон не прыгает.
    show prologue_head_bg behind prologue:
        parallel:
            linear 50.5 zoom 1.2
        parallel:
            linear 22.0 alpha 0.0

    "Кажется, осталось позади всё, что было мне ценно."

    "Я здесь после нервного срыва, что разрушил мою и без того распадавшуюся на части жизнь и подорванное здоровье."

    show prologue head:
        linear 8.0 alpha 0.0
    show prologue_dark_room:
        blur 3.0 matrixcolor BrightnessMatrix(-0.25)
        parallel:
            linear 25.0 zoom 1.05
        parallel:
            linear 11.0 blur 0.0 matrixcolor BrightnessMatrix(-0.02)
    with Dissolve(3.0)

    "Это письмо..."
    "...должно помочь мне пережить произошедшее."

## Начало письма; отдельный вход каталога сцен.

label .letter:

    $ note_hover_pencil = False

    ## Погашенные голова и фон ещё на экране: alpha задаётся явно, иначе новый ATL унаследует 0.
    show prologue_head_bg:
        zoom 1.0 alpha 1.0
        truecenter
        subpixel True
        linear 40.5 zoom 1.2
    ## Ближний план; зум 1.05 — запас под сдвиг parallax.near.
    show prologue head:
        zoom 1.05 alpha 1.0
        truecenter
        subpixel True
        function parallax_near_f
    with Dissolve(2.0)

    "Долго я не находила в себе сил, чтобы записать случившееся. Ушло много попыток."

    show prologue head_blink

    "Не было сил вспоминать: меня трясло, рвало, руки непроизвольно тянулись закрыть лицо."

    scene prologue_note_bg
    show prologue_note_paper at placed((990, 455), (0.5, 0.5))
    show prologue_note_pencil at placed((1264, 431), (0.5, 0.5))
    show prologue_hand_left at placed((271, 417))
    show prologue_hand_right at placed((1358, 468))
    with prologue_dissolve

    "Обо всём случившемся невыносимо думать."
    "Но я должна излить наружу то, что пожирает меня изнутри."

    window hide

    if not renpy.is_skipping():
        call screen prologue_note_start

    ## После закрытия экрана unhovered не вызывается.
    $ note_hover_pencil = False
    window auto

    $ dismiss_off()

    show prologue_hand_right_move:
        subpixel True
        anchor (0.0, 0.0)
        pos (1358, 468)
        linear 0.4 pos (1217, 211)
    hide prologue_hand_right
    with Dissolve(0.1)
    $ pause(0.2)

    ## Позы на разных холстах совмещены по кончику карандаша.
    show prologue_hand_right_write:
        subpixel True
        anchor (0.0, 0.0)
        pos (1217, 211)
        linear 0.4 pos (1100, 198)
    hide prologue_hand_right_move
    hide prologue_note_pencil
    with Dissolve(0.2)
    $ pause(0.1)
    $ dismiss_on()

    # camera at camera_rest(shake_amp=1.5)

    scene black with Dissolve(1.0)

    show prologue_pencil_close 
    show prologue_pensil_close_hand at shake(1.5)
    with Dissolve(1.3)

    "Я не осмелюсь вернуться к карандашу и бумаге позже."
    "Это будет моя последняя попытка. Так сказать, спринтерский забег."
    "Я Расскажу всё на одном дыхании. Здесь и сейчас."

    ## Граница между прологом и первой главой.
    scene black
    with Dissolve(2.0)
    $ pause(1.2)

    jump chapter_1_scene_1
