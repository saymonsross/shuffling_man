################################################################################
## Пролог — сцена 1: тёмная комната → затылок ГГ → записка (интерактив: клик
## по бумаге/карандашу выравнивает стол) → взятие карандаша → рука к строке.
################################################################################

## Изображения ##################################################################

image prologue_dark_room = "images/0_prologue/prologue dark_room.jpg"
image prologue_head = "images/0_prologue/prologue head.jpg"

## Композит ровной записки — только визуальный референс, в сцене собирается
## из частей (bg + бумага + карандаш), чтобы анимировать их порознь.
image prologue_note_center = "images/0_prologue/prologue_note center.jpg"
image prologue_note_bg = "images/0_prologue/prologue_note bg.jpg"
image prologue_note_paper = "images/0_prologue/prologue_note_paper.png"
image prologue_note_pencil = "images/0_prologue/prologue_note_pencil.png"

image prologue_pencil_close = "images/0_prologue/prologue pencil_close.jpg"

image prologue_hand_left = "images/0_prologue/prologue_hand_left.png"
image prologue_hand_right = "images/0_prologue/prologue_hand_right rest.png"
image prologue_hand_right_move = "images/0_prologue/prologue_hand_right move.png"
image prologue_hand_right_write = "images/0_prologue/prologue_hand_right write.png"

## Константы сцены ##############################################################

## Покачивание камеры на кадрах с затылком.
define PROLOGUE_SWAY_DRIFT = 12.0   # px
define PROLOGUE_SWAY_TILT = 0.6     # градусы

## Параллакс за мышкой на сцене записки.
define NOTE_PARALLAX = 10.0
define NOTE_PARALLAX_SMOOTH = 0.06

## Беспорядок: центры (px) и повороты (градусы). Плейсхолдеры, подгонять по месту.
define NOTE_PAPER_POS = (790, 415)
define NOTE_PAPER_ANGLE = -8.0
define NOTE_PENCIL_POS = (845, 180)
define NOTE_PENCIL_ANGLE = 80.0

define NOTE_HAND_LEFT_POS = (310, 391)
define NOTE_HAND_RIGHT_POS = (1358, 468)
## Y подобран так, чтобы жёсткий нижний обрез PNG ушёл за край экрана.
define NOTE_HAND_MOVE_POS = (904, 270)

define NOTE_HOVER_BRIGHTNESS = 0.35
define NOTE_HOVER_FLAGS = ("note_hover_paper", "note_hover_pencil")

## Порядок: позиции измерены по prologue_note center.jpg.
define NOTE_PAPER_NEAT_POS = (990, 455)
define NOTE_PENCIL_NEAT_POS = (1345, 432)

## Взятие карандаша. Холст write-позы крупнее холста move — своя позиция,
## подобранная по alpha-маскам PNG, чтобы кончик карандаша не прыгал при смене поз.
define NOTE_HAND_AT_PENCIL_POS = (1237, 211)
define NOTE_HAND_WRITE_GRIP_POS = (1237, 211)
define NOTE_HAND_REACH_T = 0.9   # сек; pause после show должен длиться столько же
define NOTE_HAND_HOVER_T = 0.5   # заминка над карандашом, сек

## Движение к началу первой строки — в системе координат write-позы.
define NOTE_HAND_LINE_START_POS = (767, 158)
define NOTE_HAND_TO_LINE_T = 1.1

define NOTE_HAND_JITTER_AMP = 3.0      # дрожь руки при взятии, px
define NOTE_WRITE_TENSION_NOISE = 0.2  # шум-помехи с момента взятия

## Крупный план руки с карандашом: лёгкий тремор фона поверх параллакса, px.
define PENCIL_CLOSE_SHAKE_AMP = 1.5

## Образы и трансформы ##########################################################

## Единственная видимая копия предметов; светлеют по hover-флагам экрана.
image note_paper = hover_lit("prologue_note_paper", "note_hover_paper", NOTE_HOVER_BRIGHTNESS)
image note_pencil = hover_lit("prologue_note_pencil", "note_hover_pencil", NOTE_HOVER_BRIGHTNESS)

transform prologue_slow_zoom:
    xalign 0.5 yalign 0.45 zoom 1.0
    ease 22.0 zoom 1.25

define prologue_fade_in = Dissolve(4.0)
define prologue_dissolve = Dissolve(1.2)

transform note_paper_messy:
    anchor (0.5, 0.5)
    pos NOTE_PAPER_POS
    rotate NOTE_PAPER_ANGLE

transform note_pencil_messy:
    anchor (0.5, 0.5)
    pos NOTE_PENCIL_POS
    rotate NOTE_PENCIL_ANGLE

default note_hover_paper = False
default note_hover_pencil = False

## Сцена ########################################################################

label prologue_scene_1:

    scene black

    ## Фейд из чёрного сразу в комнату — первая реплика поверх картинки.
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

    ## Записка в беспорядке; карандаш объявлен позже бумаги — лежит поверх.
    $ note_hover_paper = False
    $ note_hover_pencil = False
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

    call screen hover_click([
        ("prologue_note_paper", note_paper_messy, "note_hover_paper", "done"),
        ("prologue_note_pencil", note_pencil_messy, "note_hover_pencil", "done"),
    ])

    $ note_hover_paper = False
    $ note_hover_pencil = False
    window auto

    ## Кроссфейд в ровную записку из тех же частей; камера сброшена — кадр статичен.
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

    ## Уход в воспоминание.
    scene prologue_head at uneasy_sway(PROLOGUE_SWAY_DRIFT, PROLOGUE_SWAY_TILT)
    with prologue_dissolve

    "Долго я не находила в себе сил, чтобы записать случившееся. Ушло много попыток."

    "Не было сил вспоминать: меня трясло, рвало, руки непроизвольно тянулись закрыть лицо."

    ## Возврат к записке.
    scene prologue_note_bg
    show prologue_note_paper at placed(NOTE_PAPER_NEAT_POS, (0.5, 0.5))
    show prologue_note_pencil at placed(NOTE_PENCIL_NEAT_POS, (0.5, 0.5))
    with prologue_dissolve

    show prologue_hand_left at placed(NOTE_HAND_LEFT_POS)
    show prologue_hand_right at flag_fade(NOTE_HAND_RIGHT_POS, NOTE_HOVER_FLAGS, visible_when=False)

    "Обо всём случившемся невыносимо думать."

    "Но я должна излить наружу то, что пожирает меня изнутри."

    ## Взятие карандаша (автопроигрыш): рука с дрожью тянется, медлит и на том
    ## же месте перетекает в позу письма. Лёгкий шум-помехи включается здесь и
    ## держится до конца сцены; дрожь руки (общий jitter_key) не прерывается.
    $ dismiss_off()
    $ fx_noise_strength = NOTE_WRITE_TENSION_NOISE
    $ pause(0.5)
    hide prologue_hand_right
    show prologue_hand_right_move at slide_in(NOTE_HAND_RIGHT_POS, NOTE_HAND_AT_PENCIL_POS, t=NOTE_HAND_REACH_T, jitter_amp=NOTE_HAND_JITTER_AMP, jitter_key="note_hand")
    $ pause(NOTE_HAND_REACH_T)
    $ pause(NOTE_HAND_HOVER_T)

    show prologue_hand_right_write at placed_jitter(NOTE_HAND_WRITE_GRIP_POS, jitter_amp=NOTE_HAND_JITTER_AMP, jitter_key="note_hand")
    hide prologue_hand_right_move
    hide prologue_note_pencil
    with Dissolve(0.4)
    $ pause(0.7)

    ## Рука с карандашом едет к началу первой строки, дрожь сохраняется.
    show prologue_hand_right_write at move_between(NOTE_HAND_WRITE_GRIP_POS, NOTE_HAND_LINE_START_POS, t=NOTE_HAND_TO_LINE_T, jitter_amp=NOTE_HAND_JITTER_AMP, jitter_key="note_hand")
    $ pause(NOTE_HAND_TO_LINE_T)
    $ dismiss_on()

    ## Крупный план руки с карандашом: тот же параллакс, что и на записке,
    ## шум остаётся лёгким, фон чуть дрожит — тремор / нервное напряжение.
    camera at mouse_parallax(NOTE_PARALLAX, NOTE_PARALLAX_SMOOTH, shake_amp=PENCIL_CLOSE_SHAKE_AMP)
    scene prologue_pencil_close
    with prologue_dissolve

    "Я не осмелюсь вернуться к карандашу и бумаге позже. Это будет моя последняя попытка. Спринтерский забег."

    "Я расскажу всё на одном дыхании. Здесь и сейчас."

    ## Возврат фоновых значений при выходе из сцены.
    $ fx_noise_strength = FX_NOISE_DEFAULT

    return
