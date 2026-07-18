################################################################################
## Пролог — Сцена 1
##
## Тёмная комната → затылок ГГ → записка (интерактив: наведи и клинкни по бумаге
## или карандашу, сцена перетекает в состояние порядка) → записка ровно, монолог
## → взятие карандаша → рука едет к началу строки на листе (весь хвост —
## автопроигрыш, без действия игрока).
##
## Интерактив упрощён до одного клика: игрок наводит курсор на любой из двух
## предметов (объект чуть светлеет + рука «тянется»), клик — и весь кадр
## кросфейдом переходит в ровную записку, собранную из тех же частей (bg +
## бумага + карандаш), что и беспорядок — только без поворота. Готовый
## композит prologue_note_center используется лишь как визуальный референс.
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

## Правая рука, поза письма — уже держит карандаш (см. взятие карандаша ниже).
image prologue_hand_right_write = "images/0_prologue/prologue_hand_right write.png"

## Настройки эффектов ###########################################################
##
## Сами эффекты — общие трансформы из common/camera_fx.rpy, здесь только
## параметры этой сцены.

## Покачивание камеры на кадре с затылком ГГ (тревога, нестабильность).
define PROLOGUE_SWAY_DRIFT = 12.0    # амплитуда дрейфа, px
define PROLOGUE_SWAY_TILT = 0.6     # амплитуда наклона, градусы

## Сцена записки: лёгкий параллакс за мышкой. Без тряски и без нарастания/
## спадания — уровень фиксирован. Зерно-помехи — общее для всей игры (см.
## common/camera_fx.rpy).
define NOTE_PARALLAX = 10.0        # сдвиг камеры за мышкой, px
define NOTE_PARALLAX_SMOOTH = 0.06 # сглаживание параллакса за кадр (0..1)

## Плейсхолдеры положения предметов и рук на prologue_note_messy — подобраны на
## глаз, финально подгоняются по месту в игре (см. верификацию в плане задачи).
define NOTE_PAPER_POS = (790, 415)   # (x, y) центра бумаги, px
define NOTE_PAPER_ANGLE = -8.0        # поворот бумаги, градусы
define NOTE_PENCIL_POS = (845, 180)  # (x, y) центра карандаша, px
define NOTE_PENCIL_ANGLE = 80.0       # поворот карандаша, градусы

define NOTE_HAND_LEFT_POS = (310, 391)   # левая рука, статична
define NOTE_HAND_RIGHT_POS = (1358, 468) # правая рука, поза покоя
## Правая рука, поза «тянется» (на экране). Y подобран так, чтобы нижний край
## картинки (жёсткий обрез рукава, без сглаживания) уходил за нижнюю границу
## экрана (1080px) — иначе виден шов обреза посреди предплечья.
define NOTE_HAND_MOVE_POS = (904, 270)

define NOTE_HOVER_BRIGHTNESS = 0.35 # насколько светлеет предмет при наведении

## Записка "в порядке" — те же объекты, что в беспорядке, но ровно (без поворота).
## Позиции бумаги/карандаша измерены по prologue_note center.jpg.
define NOTE_PAPER_NEAT_POS = (990, 455)
define NOTE_PENCIL_NEAT_POS = (1345, 432)

## Взятие карандаша (плейсхолдеры — подогнать по месту в игре). Рука move
## дотягивается ровно до карандаша и застывает над ним.
define NOTE_HAND_REACH_FROM = (1450, 980)              # рука move стартует за нижним-правым краем
define NOTE_HAND_AT_PENCIL_POS = (1237, 211)  # цель "дотянулась" — над карандашом (для move)

## Поза письма (prologue_hand_right_write) — ДРУГОЙ, намного более крупный
## холст (798x954 против 630x836 у move), и оба позиционируются как центр
## своего холста. Простое переиспользование NOTE_HAND_AT_PENCIL_POS для write
## смещает видимый кончик карандаша почти на 60px выше, чем он был у move —
## заметный скачок при кроссфейде. Ниже — своя позиция для write, подобранная
## по фактическому положению кончика карандаша внутри каждого PNG (измерено
## по alpha-маске), чтобы кончик не двигался при смене позы.
define NOTE_HAND_WRITE_GRIP_POS = (1237, 211)  # поза write в момент хвата (кончик там же, где был у move)
define NOTE_HAND_REACH_T = 0.9  # скорость движения руки, сек. Меняешь тут — не забудь,
                                 # что дальше по коду $ pause(NOTE_HAND_REACH_T) должен
                                 # длиться ровно столько же, иначе смена позы обрежет
                                 # движение или будет ждать после его окончания.
define NOTE_HAND_HOVER_T = 0.5  # задержка: рука висит над карандашом перед тем, как
                                 # взять его (герой медлит, преодолевая себя), сек.

## Рука с карандашом едет к началу первой строки на листе (плейсхолдер —
## подогнать по месту в игре). Позиция — в той же системе (центр холста
## write-позы), что и NOTE_HAND_WRITE_GRIP_POS, иначе движение снова "прыгнет".
define NOTE_HAND_LINE_START_POS = (767, 158)
define NOTE_HAND_TO_LINE_T = 1.1  # скорость этого движения, сек

## Напряжение на взятии карандаша: дрожь руки + заметно усиленный шум-помехи.
## Носитель шума — глобальный fx_noise_strength (common/camera_fx.rpy),
## 0.10 ниже — его дефолт, к которому возвращаемся, когда рука берёт карандаш.
define NOTE_HAND_JITTER_AMP = 3.0     # амплитуда дрожи руки при взятии, px
define NOTE_WRITE_TENSION_NOISE = 0.3 # сила шума-помех на время взятия карандаша

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
    anchor (0.0, 0.0)
    pos pos_xy

## Ровная постановка бумаги/карандаша (без поворота).
transform note_paper_neat:
    anchor (0.5, 0.5)
    pos NOTE_PAPER_NEAT_POS

transform note_pencil_neat:
    anchor (0.5, 0.5)
    pos NOTE_PENCIL_NEAT_POS

## Рука тянется к карандашу: въезжает движением из-за кадра с проявлением,
## поверх — лёгкая дрожь (герой в напряжении, преодолевает себя, чтобы начать
## писать). Дрожь — через общий хелпер object_jitter_f (common/camera_fx.rpy),
## offset складывается с движением аддитивно (parallel-трек поверх pos).
transform note_hand_reach_in(from_xy, to_xy, t=0.9, jitter_amp=NOTE_HAND_JITTER_AMP):
    anchor (0.0, 0.0)
    pos from_xy
    alpha 0.0
    xoffset 0.0 yoffset 0.0
    parallel:
        ease t alpha 1.0
    parallel:
        ease t pos to_xy
    parallel:
        function renpy.curry(object_jitter_f)(jitter_amp, 0.5, "note_hand")

## Рука (уже видима, держит карандаш) едет к точке на листе — без проявления,
## только перемещение.
transform note_hand_move_to(from_xy, to_xy, t=0.8):
    anchor (0.0, 0.0)
    pos from_xy
    ease t pos to_xy

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
    anchor (0.0, 0.0)
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
    ## следует за мышкой.
    $ note_hover_paper = False
    $ note_hover_pencil = False
    camera at mouse_parallax(NOTE_PARALLAX, NOTE_PARALLAX_SMOOTH)
    scene prologue_note_bg
    show note_paper at note_paper_messy
    show note_pencil at note_pencil_messy
    show prologue_hand_left at note_hand_pos(NOTE_HAND_LEFT_POS)
    show prologue_hand_right at hand_reach(NOTE_HAND_RIGHT_POS, visible_when_reaching=False)
    show prologue_hand_right_move at hand_reach(NOTE_HAND_MOVE_POS, visible_when_reaching=True)
    with prologue_dissolve

    "Пора начинать. Но не так. Не с такого стола."

    "Листы лежат криво. И карандаш. Сначала нужно всё поправить — иначе не выйдет ни строчки."

    window hide

    call screen prologue_note_align

    ## Экран закрылся — unhovered кнопки уже не сработает, гасим подсветку сами.
    $ note_hover_paper = False
    $ note_hover_pencil = False
    window auto

    ## Порядок наведён — кросфейд в ровную записку, собранную из частей (bg +
    ## бумага + карандаш, без рук), чтобы дальше анимировать карандаш. Камера
    ## сброшена — кадр статичен. Референс "как должно выглядеть" — готовый
    ## композит prologue_note_center (см. объявление образов выше).
    camera
    scene prologue_note_bg
    show prologue_note_paper at note_paper_neat
    show prologue_note_pencil at note_pencil_neat
    show prologue_hand_left at note_hand_pos(NOTE_HAND_LEFT_POS)
    show prologue_hand_right at hand_reach(NOTE_HAND_RIGHT_POS, visible_when_reaching=False)
    with Dissolve(0.6)

    "Теперь всё ровно. Можно начинать."

    "Я здесь после нервного срыва, что разрушил мою и без того распадавшуюся на части жизнь и подорванное здоровье."

    "Это письмо... должно помочь мне пережить произошедшее."

    ## Уход в воспоминание — снова кадр с затылком ГГ (тот же мотив тревоги).
    scene prologue_head at uneasy_sway(PROLOGUE_SWAY_DRIFT, PROLOGUE_SWAY_TILT)
    with prologue_dissolve

    "Долго я не находила в себе сил, чтобы записать случившееся. Ушло много попыток."

    "Не было сил вспоминать: меня трясло, рвало, руки непроизвольно тянулись закрыть лицо."

    ## Возврат к записке с карандашом.
    scene prologue_note_bg
    show prologue_note_paper at note_paper_neat
    show prologue_note_pencil at note_pencil_neat
    with prologue_dissolve

    show prologue_hand_left at note_hand_pos(NOTE_HAND_LEFT_POS)
    show prologue_hand_right at hand_reach(NOTE_HAND_RIGHT_POS, visible_when_reaching=False)

    "Обо всём случившемся невыносимо думать."

    "Но я должна излить наружу то, что пожирает меня изнутри."

    ## Взятие карандаша (без участия игрока). Рука тянется движением к
    ## карандашу, дрожа от напряжения — герой преодолевает себя, чтобы начать
    ## писать; шум-помехи на это время заметно усиливается. Рука застывает
    ## точно над карандашом, немного медлит (NOTE_HAND_HOVER_T) и на этом же
    ## месте плавно перетекает в позу письма — без скачка позиции; дрожь и
    ## усиленный шум спадают, табличный карандаш убирается синхронно (поза
    ## write уже держит его).
    $ dismiss_off()
    $ fx_noise_strength = NOTE_WRITE_TENSION_NOISE
    $ pause(0.5)
    hide prologue_hand_right
    show prologue_hand_right_move at note_hand_reach_in(NOTE_HAND_RIGHT_POS, NOTE_HAND_AT_PENCIL_POS, t=NOTE_HAND_REACH_T)
    $ pause(NOTE_HAND_REACH_T)
    $ pause(NOTE_HAND_HOVER_T)

    $ fx_noise_strength = 0.10
    show prologue_hand_right_write at note_hand_pos(NOTE_HAND_WRITE_GRIP_POS)
    hide prologue_hand_right_move
    hide prologue_note_pencil
    with Dissolve(0.4)
    $ pause(0.7)

    ## Рука с карандашом едет от места взятия к началу первой строки на листе.
    show prologue_hand_right_write at note_hand_move_to(NOTE_HAND_WRITE_GRIP_POS, NOTE_HAND_LINE_START_POS, t=NOTE_HAND_TO_LINE_T)
    $ pause(NOTE_HAND_TO_LINE_T)
    $ dismiss_on()

    return
