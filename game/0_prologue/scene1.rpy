################################################################################
## Пролог — Сцена 1
##
## Тёмная комната → записка → затылок ГГ → записка (интерактив: наведи и клинкни
## по бумаге или карандашу, сцена перетекает в состояние порядка) → записка ровно.
##
## Интерактив упрощён до одного клика: игрок наводит курсор на любой из двух
## предметов (объект чуть светлеет + рука «тянется»), клик — и весь кадр
## кросфейдом переходит в prologue_note_center.
################################################################################

## Изображения ##################################################################

image prologue_dark_room = "images/0_prologue/prologue dark_room.jpg"
image prologue_head = "images/0_prologue/prologue head.jpg"

## Готовый композит записки в порядке — конечная точка кросфейда.
image prologue_note_center = "images/0_prologue/prologue_note center.jpg"

## Фон записки без бумаги и карандаша — они отдельные объекты (см. ниже), чтобы
## подсветка при наведении точно совпадала с их формой.
image prologue_note_bg = "images/0_prologue/prologue_note bg.jpg"

## Бумага и карандаш — отдельные вырезанные объекты, видимые слои поверх фона.
## Хит-зона для клика — попиксельно по этим же изображениям (focus_mask).
image prologue_note_paper = "images/0_prologue/prologue_note_paper.png"
image prologue_note_pencil = "images/0_prologue/prologue_note_pencil.png"

## Руки Марины на столе. Правая рука «тянется» к предмету при наведении —
## перетекание между позами покоя и движения (см. hand_reach ниже; без
## слежения за курсором).
image prologue_hand_left = "images/0_prologue/prologue_hand_left.png"
image prologue_hand_right = "images/0_prologue/prologue_hand_right rest.png"
image prologue_hand_right_move = "images/0_prologue/prologue_hand_right move.png"

## Настройки эффектов ###########################################################
##
## Сами эффекты — общие трансформы из common/camera_fx.rpy, здесь только
## параметры этой сцены.

## Покачивание камеры на кадре с затылком ГГ (тревога, нестабильность).
define PROLOGUE_SWAY_DRIFT = 12.0    # амплитуда дрейфа, px
define PROLOGUE_SWAY_TILT = 0.6     # амплитуда наклона, градусы

## Сцена записки: лёгкий параллакс за мышкой и постоянное зерно-помехи от
## напряжения. Без тряски и без нарастания/спадания — уровень фиксирован.
define NOTE_PARALLAX = 10.0        # сдвиг камеры за мышкой, px
define NOTE_PARALLAX_SMOOTH = 0.06 # сглаживание параллакса за кадр (0..1)
define NOTE_NOISE = 0.10           # сила помех (0..1)

## Плейсхолдеры положения предметов и рук на prologue_note_messy — подобраны на
## глаз, финально подгоняются по месту в игре (см. верификацию в плане задачи).
define NOTE_PAPER_POS = (790, 415)   # (x, y) центра бумаги, px
define NOTE_PAPER_ANGLE = -8.0        # поворот бумаги, градусы
define NOTE_PENCIL_POS = (845, 180)  # (x, y) центра карандаша, px
define NOTE_PENCIL_ANGLE = 80.0       # поворот карандаша, градусы

define NOTE_HAND_LEFT_POS = (500, 820)   # левая рука, статична
define NOTE_HAND_RIGHT_POS = (1340, 820) # правая рука, поза покоя
## Правая рука, поза «тянется» (на экране). Y подобран так, чтобы нижний край
## картинки (жёсткий обрез рукава, без сглаживания) уходил за нижнюю границу
## экрана (1080px) — иначе виден шов обреза посреди предплечья.
define NOTE_HAND_MOVE_POS = (950, 700)

define NOTE_HOVER_BRIGHTNESS = 0.35 # насколько светлеет предмет при наведении

## Предметы на столе — единственная видимая копия каждого (кнопки в экране
## невидимы, см. ниже). При наведении тот же объект показывается светлее
## (7dots brightness); флаги ставит экран интерактива.
image note_paper = ConditionSwitch(
    "note_hover_paper", At("prologue_note_paper", brightness(NOTE_HOVER_BRIGHTNESS)),
    True, "prologue_note_paper",
    predict_all=True)

image note_pencil = ConditionSwitch(
    "note_hover_pencil", At("prologue_note_pencil", brightness(NOTE_HOVER_BRIGHTNESS)),
    True, "prologue_note_pencil",
    predict_all=True)

## Трансформы и переходы ########################################################

## Медленный наезд камеры на ГГ в центре комнаты.
transform prologue_slow_zoom:
    xalign 0.5 yalign 0.45 zoom 1.0
    ease 22.0 zoom 1.25

define prologue_fade_in = Dissolve(4.0)
define prologue_dissolve = Dissolve(1.2)

## Статичная постановка бумаги/карандаша в положении беспорядка.
transform note_paper_messy:
    anchor (0.5, 0.5)
    pos NOTE_PAPER_POS
    rotate NOTE_PAPER_ANGLE

transform note_pencil_messy:
    anchor (0.5, 0.5)
    pos NOTE_PENCIL_POS
    rotate NOTE_PENCIL_ANGLE

## Статичное положение руки на слое master (без слежения за курсором).
transform note_hand_pos(pos_xy):
    anchor (0.5, 0.5)
    pos pos_xy

## Правая рука «тянется» к предмету при наведении: обе позы (покоя и
## движения) показаны на слое master один раз и никогда не прячутся — alpha
## каждой плавно идёт к 0/1 по текущему hover, отчего одна поза кросфейдом
## перетекает в другую. 7dots show_hide тут не годится: он лишь показывает
## или прячет один спрайт, а не сменяет один на другой.
init -10 python:

    def _hand_reach_alpha_f(visible_when_reaching, relax, trans, st, at):
        reaching = note_hover_paper or note_hover_pencil
        target = 1.0 if reaching == visible_when_reaching else 0.0
        a = getattr(trans, "fx_a", target)
        a += (target - a) * relax
        trans.fx_a = a
        trans.alpha = a
        return 1.0 / 60.0

transform hand_reach(pos_xy, visible_when_reaching=True, relax=0.15):
    anchor (0.5, 0.5)
    pos pos_xy
    function renpy.curry(_hand_reach_alpha_f)(visible_when_reaching, relax)

## Интерактив: наведи и клинкни ##################################################
##
## Диалоговое окно скрыто. Сами предметы лежат на слое master (note_paper и
## note_pencil), кнопки здесь только ловят курсор: они полностью прозрачны, а
## хит-зона задана попиксельно по альфе предмета (focus_mask). Наведение
## поднимает флаг — предмет на master светлеет, правая рука «тянется».
## Клик по любому из двух завершает мини-игру.

default note_hover_paper = False
default note_hover_pencil = False

screen prologue_note_align():
    modal True

    imagebutton:
        at note_paper_messy
        idle Transform("prologue_note_paper", alpha=0.0)
        focus_mask "prologue_note_paper"
        hovered SetVariable("note_hover_paper", True)
        unhovered SetVariable("note_hover_paper", False)
        action Return("done")

    imagebutton:
        at note_pencil_messy
        idle Transform("prologue_note_pencil", alpha=0.0)
        focus_mask "prologue_note_pencil"
        hovered SetVariable("note_hover_pencil", True)
        unhovered SetVariable("note_hover_pencil", False)
        action Return("done")

## Сцена ########################################################################

label prologue_s1:

    scene black

    ## Сразу фейд из чёрного в комнату с ГГ, камера медленно приближается —
    ## первая реплика идёт уже поверх картинки, без зависания на чёрном экране.
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

    ## Записка в беспорядке: фон + бумага и карандаш отдельными слоями (карандаш
    ## поверх листов — объявлен позже, приоритет при наложении). Камера чуть
    ## следует за мышкой, поверх — постоянное зерно-помехи от напряжения.
    $ note_hover_paper = False
    $ note_hover_pencil = False
    camera at mouse_parallax(NOTE_PARALLAX, NOTE_PARALLAX_SMOOTH)
    scene prologue_note_bg
    show note_paper at note_paper_messy
    show note_pencil at note_pencil_messy
    show prologue_hand_left at note_hand_pos(NOTE_HAND_LEFT_POS)
    show prologue_hand_right at hand_reach(NOTE_HAND_RIGHT_POS, visible_when_reaching=False)
    show prologue_hand_right_move at hand_reach(NOTE_HAND_MOVE_POS, visible_when_reaching=True)
    show fx_noise at noise_overlay(NOTE_NOISE)
    with prologue_dissolve

    "Пора начинать. Но не так. Не с такого стола."

    "Листы лежат криво. И карандаш. Сначала нужно всё поправить — иначе не выйдет ни строчки."

    window hide

    call screen prologue_note_align

    ## Экран закрылся — unhovered кнопки уже не сработает, гасим подсветку сами.
    $ note_hover_paper = False
    $ note_hover_pencil = False
    window auto

    ## Порядок наведён — кросфейд всей картинки в готовый композит. Параллакс,
    ## руки и помехи уходят вместе со сменой сцены.
    camera
    scene prologue_note_center
    with Dissolve(0.6)

    "Теперь всё ровно. Можно начинать."

    "Я здесь после нервного срыва, что разрушил мою и без того распадавшуюся на части жизнь и подорванное здоровье."

    "Это письмо... должно помочь мне пережить произошедшее."

    return
