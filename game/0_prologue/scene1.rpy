################################################################################
## Пролог — Сцена 1
##
## Тёмная комната → записка → затылок ГГ → записка (интерактив: выровнять
## листы и карандаш, анимация по слоям) → записка ровно.
##
## Кликами игрок постепенно перемещает предметы из положения как на
## prologue_note.jpg в положение как на prologue_note center.jpg, после чего
## сцена кросфейдом переходит в сам prologue_note center.jpg.
################################################################################

## Изображения ##################################################################

image prologue_dark_room = "images/0_prologue/prologue dark_room.jpg"
image prologue_note_messy = "images/0_prologue/prologue_note.jpg"
image prologue_note_center = "images/0_prologue/prologue_note center.jpg"
image prologue_head = "images/0_prologue/prologue head.jpg"

## Слои записки для интерактива. Кропы центрированы на центр масс предмета,
## чтобы вращение через anchor (0.5, 0.5) шло вокруг центра предмета.
## Поля кропов дают запас под обводку контура при наведении.
image note2_bg = "images/0_prologue/prologue_note 2_bg.jpg"
image note2_paper = Crop((435, 4, 700, 820), "images/0_prologue/prologue_note 2_papaer.png")
image note2_pencil = Crop((581, 164, 550, 100), "images/0_prologue/prologue_note 2_pencil.png")

## Настройки эффектов ###########################################################
##
## Сами эффекты — общие трансформы из common/camera_fx.rpy, здесь только
## параметры этой сцены.

## Покачивание камеры на кадре с затылком ГГ (тревога, нестабильность).
define PROLOGUE_SWAY_DRIFT = 12.0    # амплитуда дрейфа, px
define PROLOGUE_SWAY_TILT = 0.6     # амплитуда наклона, градусы

## Сцена записки: параллакс за мышкой + дрожь и помехи от напряжения.
define NOTE2_PARALLAX = 10.0        # сдвиг камеры за мышкой, px
define NOTE2_PARALLAX_SMOOTH = 0.06 # сглаживание параллакса за кадр (0..1)
define NOTE2_SHAKE_AMP = 1.5        # дрожь при полном напряжении, px
define NOTE2_NOISE = 0.10           # сила помех при полном напряжении (0..1)
define NOTE2_RELAX = 0.04           # скорость спадания напряжения за кадр

## Напряжение Марины: 1.0 — беспорядок на столе, 0.0 — всё выровнено.
## Управляет дрожью камеры и помехами; спадает с каждым кликом.
default note2_tension = 1.0

## Трансформы и переходы ########################################################

## Медленный наезд камеры на ГГ в центре комнаты.
transform prologue_slow_zoom:
    xalign 0.5 yalign 0.45 zoom 1.0
    ease 22.0 zoom 1.25

define prologue_fade_in = Dissolve(4.0)
define prologue_dissolve = Dissolve(1.2)

## Предмет на столе: плавный переход из старого состояния в новое.
transform note2_move(ox, oy, oa, oz, nx, ny, na, nz):
    anchor (0.5, 0.5)
    transform_anchor True
    pos (ox, oy) rotate oa zoom oz
    ease 0.5 pos (nx, ny) rotate na zoom nz

## Статичная постановка предмета в состояние st = (x, y, angle, zoom).
transform note2_place(st):
    anchor (0.5, 0.5)
    transform_anchor True
    pos (st[0], st[1])
    rotate st[2]
    zoom st[3]

## Хайлайты: только контур (шейдер sm.outline и трансформы — common/shaders.rpy).
image note2_paper_hl = At("note2_paper", outline_hover(), hover_pulse())
image note2_pencil_hl = At("note2_pencil", outline_hover(), hover_pulse())

## Интерактив: выравнивание листов и карандаша #################################
##
## Диалоговое окно скрыто, игрок кликает по предметам на столе.
## Каждый предмет требует нескольких кликов — Марине непросто начать,
## тревожность и ОКР заставляют «готовиться».
##
## Параметры измерены по prologue_note.jpg (from) и prologue_note center.jpg
## (to): центр предмета, итоговый поворот (градусы) и масштаб.

define NOTE2_PAPER = {"from": (785, 414), "to": (967, 438), "angle": 15.0, "zoom": 0.95, "clicks": 3}
define NOTE2_PENCIL = {"from": (856, 214), "to": (1318, 415), "angle": -94.0, "zoom": 0.98, "clicks": 2}

init python:
    def note2_state(item, clicks):
        """(x, y, angle, zoom) предмета после указанного числа кликов."""
        f = min(max(clicks, 0), item["clicks"]) / float(item["clicks"])
        fx, fy = item["from"]
        tx, ty = item["to"]
        ## Координаты — только int: float в pos Ren'Py трактует как долю экрана.
        return (int(round(fx + (tx - fx) * f)),
                int(round(fy + (ty - fy) * f)),
                item["angle"] * f,
                1.0 + (item["zoom"] - 1.0) * f)

## Кнопки повторяют текущее положение предметов; хит-зона — попиксельно по
## альфа-каналу (focus_mask), при наведении — пульсирующий контур по объекту.
screen prologue_note_align(paper_st, pencil_st, sheets_done, pencil_done):
    modal True

    ## Стопка листов.
    if not sheets_done:
        imagebutton:
            at note2_place(paper_st)
            idle Transform("note2_paper", alpha=0.0)
            hover "note2_paper_hl"
            focus_mask "note2_paper"
            action Return("sheets")

    ## Карандаш поверх листов (объявлен позже — приоритет при наложении).
    if not pencil_done:
        imagebutton:
            at note2_place(pencil_st)
            idle Transform("note2_pencil", alpha=0.0)
            hover "note2_pencil_hl"
            focus_mask "note2_pencil"
            action Return("pencil")

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

    ## Записка из слоёв — предметы лежат как на prologue_note.jpg.
    ## Камера чуть следует за мышкой и мелко дрожит от напряжения, поверх —
    ## зерно-помехи. Оба эффекта спадают по мере наведения порядка на столе.
    $ note2_tension = 1.0
    camera at mouse_parallax(NOTE2_PARALLAX, NOTE2_PARALLAX_SMOOTH, NOTE2_SHAKE_AMP, NOTE2_RELAX, "note2_tension")
    scene note2_bg
    show note2_paper at note2_move(*(note2_state(NOTE2_PAPER, 0) * 2))
    show note2_pencil at note2_move(*(note2_state(NOTE2_PENCIL, 0) * 2))
    show fx_noise at noise_overlay(NOTE2_NOISE, NOTE2_RELAX, "note2_tension")
    with prologue_dissolve

    "Пора начинать. Но не так. Не с такого стола."

    "Листы лежат криво. И карандаш. Сначала нужно всё поправить — иначе не выйдет ни строчки."

    window hide

    $ _sheets = 0
    $ _pencil = 0

    while _sheets < NOTE2_PAPER["clicks"] or _pencil < NOTE2_PENCIL["clicks"]:

        call screen prologue_note_align(note2_state(NOTE2_PAPER, _sheets), note2_state(NOTE2_PENCIL, _pencil), _sheets >= NOTE2_PAPER["clicks"], _pencil >= NOTE2_PENCIL["clicks"])

        ## Каждый клик снимает часть напряжения — дрожь и помехи слабеют.
        if _return in ("sheets", "pencil"):
            $ note2_tension = 1.0 - (_sheets + _pencil + 1) / float(NOTE2_PAPER["clicks"] + NOTE2_PENCIL["clicks"])

        if _return == "sheets":
            $ _sheets += 1
            ## Стопка сдвигается и доворачивается к положению с финальной картинки.
            show note2_paper at note2_move(*(note2_state(NOTE2_PAPER, _sheets - 1) + note2_state(NOTE2_PAPER, _sheets)))
            $ renpy.pause(0.55, hard=True)
            if _sheets == 1:
                "Я подравняла стопку. Ближе к центру. Но верхний лист всё ещё выступает. Совсем чуть-чуть."
            elif _sheets == 2:
                "Это «чуть-чуть» невыносимо. Ещё раз."
            elif _sheets == 3:
                "Вот. Края совпали. Кажется... Да. Совпали."
        elif _return == "pencil":
            $ _pencil += 1
            show note2_pencil at note2_move(*(note2_state(NOTE2_PENCIL, _pencil - 1) + note2_state(NOTE2_PENCIL, _pencil)))
            $ renpy.pause(0.55, hard=True)
            if _pencil == 1:
                "Карандаш лежал поперёк листа. Косо. Так нельзя."
            elif _pencil == 2:
                "Вдоль правого края. Идеально параллельно. Только так."

        window hide

    ## Теперь листы бумаги и карандаш лежат ровно — слои совпадают с финальной
    ## картинкой, кросфейд лишь сглаживает разницу в тенях. Параллакс, дрожь
    ## и помехи выключаются: порядок наведён, камера успокаивается.
    camera
    scene prologue_note_center
    with prologue_dissolve

    "Теперь всё ровно. Можно начинать."

    "Я здесь после нервного срыва, что разрушил мою и без того распадавшуюся на части жизнь и подорванное здоровье."

    "Это письмо... должно помочь мне пережить произошедшее."

    return
