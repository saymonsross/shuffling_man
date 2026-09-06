## Пролог: тёмная комната → записка → воспоминание → начало письма.

## Изображения

image prologue_dark_room = "images/0_prologue/prologue dark_room.jpg"
image prologue_head = "images/0_prologue/prologue head.jpg"

## prologue_note_center — референс; сцена собирается из отдельных частей.
image prologue_note_center = "images/0_prologue/prologue_note center.jpg"
image prologue_note_bg = "images/0_prologue/prologue_note bg.jpg"
image prologue_note_paper = "images/0_prologue/prologue_note_paper.png"
image prologue_note_pencil = "images/0_prologue/prologue_note_pencil.png"

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

## Позиции беспорядка: центры в px, повороты в градусах.
define NOTE_PAPER_POS = (790, 415)
define NOTE_PAPER_ANGLE = -8.0
define NOTE_PENCIL_POS = (937, 157)
define NOTE_PENCIL_ANGLE = 80.0

define NOTE_HAND_LEFT_POS = (310, 391)
define NOTE_HAND_RIGHT_POS = (1358, 468)
define NOTE_HAND_MOVE_POS = (904, 270)

define NOTE_HOVER_BRIGHTNESS = 0.35
define NOTE_HOVER_FLAGS = ("note_hover_note",)

define NOTE_FIX_BUTTON_POS = (864, 286)
define NOTE_FIX_BUTTON_SIZE = (310, 155)

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

image note_paper = hover_lit("prologue_note_paper", "note_hover_note", NOTE_HOVER_BRIGHTNESS)
image note_pencil = hover_lit("prologue_note_pencil", "note_hover_note", NOTE_HOVER_BRIGHTNESS)

transform prologue_slow_zoom:
    subpixel True
    xalign 0.5 yalign 0.45 zoom 1.0
    ease sm_motion_time(22.0) zoom 1.25

define prologue_fade_in = Dissolve(4.0)
define prologue_dissolve = Dissolve(1.2)

define 1 note_paper_messy = placed(NOTE_PAPER_POS, (0.5, 0.5), NOTE_PAPER_ANGLE)
define 1 note_pencil_messy = placed(NOTE_PENCIL_POS, (0.5, 0.5), NOTE_PENCIL_ANGLE)

default note_hover_note = False

## Экраны

screen prologue_note_fix():
    modal True
    use sm_skippable_interaction
    ## Кнопка использует мировые координаты и следует за камерой.
    fixed:
        at follow_camera()
        xysize (config.screen_width, config.screen_height)
        use glow_button(
            _("Поправить"),
            Return("done"),
            bg="light",
            pos=NOTE_FIX_BUTTON_POS,
            size=NOTE_FIX_BUTTON_SIZE,
            hovered=SetVariable("note_hover_note", True),
            unhovered=SetVariable("note_hover_note", False))

## Сцена

label prologue_scene_1:

    scene black

    scene prologue_dark_room at prologue_slow_zoom
    with prologue_fade_in

    "Чтобы заговорить о чём-то тяжёлом, лучше всего для начала представиться."

    "Так сказать, вспомнить, кто ты есть."

    scene prologue_head at uneasy_sway(PROLOGUE_SWAY_DRIFT, PROLOGUE_SWAY_TILT)
    with prologue_dissolve

    "Меня зовут Марина Александровна Шрайбер. Я пишу эти строки не в первый раз."

    "Я нахожусь довольно далеко от места, что называла домом."

    "Сейчас у меня нет дома."

    "Кажется, осталось позади всё, что было мне ценно."

    ## Интерактив с запиской.
    $ note_hover_note = False
    camera at mouse_parallax(NOTE_PARALLAX, NOTE_PARALLAX_SMOOTH)
    scene prologue_note_bg
    show note_paper at note_paper_messy
    show note_pencil at note_pencil_messy
    show prologue_hand_left at placed(NOTE_HAND_LEFT_POS)
    show prologue_hand_right at flag_fade(NOTE_HAND_RIGHT_POS, NOTE_HOVER_FLAGS, visible_when=False)
    show prologue_hand_right_move at flag_fade(NOTE_HAND_MOVE_POS, NOTE_HOVER_FLAGS)
    with prologue_dissolve

    "Пора начинать. Но не так. Не с такого стола."

    "Листы лежат криво. И карандаш. Сначала нужно всё поправить — иначе не выйдет ни строчки."

    window hide

    ## Интерактив не создаёт развилку и пропускается вместе со сценой.
    if not renpy.is_skipping():
        call screen prologue_note_fix

    ## После закрытия экрана unhovered не вызывается.
    $ note_hover_note = False
    window auto

    camera
    scene prologue_note_bg
    show prologue_note_paper at placed(NOTE_PAPER_NEAT_POS, (0.5, 0.5))
    show prologue_note_pencil at placed(NOTE_PENCIL_NEAT_POS, (0.5, 0.5))
    show prologue_hand_left at placed(NOTE_HAND_LEFT_POS)
    show prologue_hand_right at flag_fade(NOTE_HAND_RIGHT_POS, NOTE_HOVER_FLAGS, visible_when=False)
    with Dissolve(0.6)

    "Теперь всё ровно. Можно начинать."

    "Я здесь после нервного срыва, что разрушил мою и без того распадавшуюся на части жизнь и подорванное здоровье."

    "Это письмо... должно помочь мне пережить произошедшее."

    return
