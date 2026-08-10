################################################################################
## Глава 1 — сцена 1, мини-игра «Замки». Снаружи не перестают колотить, а
## игрок отпирает дверь. Каждый замок открывается по-своему: щеколду вывести
## из прорези и отвести вправо; у большого замка сдвинуть щеколду и провернуть
## вертушку против часовой; дверную ручку потянуть вниз. Новые замки
## добавляются в C1S1_MG_LOCK_ORDER.
##
## Щеколда — не «потяни в сторону», а три колена прорези корпуса (см.
## C1S1_LATCH_PATH): ушко заперто в нижней прорези, его проворачивают вверх в
## канал, ведут вправо и снова вверх — в верхнюю прорезь. Движение мыши
## проецируется на ось текущего колена, поэтому мимо прорези засов не пойдёт.
##
## Два плана. Мини-игра отделена от сцены: игрок возится не с дверью в кадре,
## а с отдельной моделью замка.
##
##   master (мир)  — та же дверь: продолжает вздрагивать от ударов, дрожит
##                   сумка; поверх неё ложится оверлей и уводит кадр в темноту.
##   lockgame      — свой слой: модель текущего замка, одна, по центру экрана,
##                   крупно. Камера его не трогает (`camera at` работает по
##                   master), поэтому замок не вздрагивает — это другой план.
##                   Слой, а не экран: детали остаются обычными спрайтами
##                   сцены, их видит Position Tuner (F9).
##   screens (UI)  — экран мини-игры: ловит мышь, держит модальность, ничего
##                   не рисует. Зерно (fx_noise_screen) идёт выше всех.
##
## Замки открываются по одному в порядке C1S1_MG_LOCK_ORDER: открытый уходит,
## на его месте проявляется следующий.
##
## Стук ведёт один драйвер (chapter_1_mg_driver): невидимый спрайт, чей
## трансформ тикает каждый кадр. Он же двигает засов и считает время. Всё
## состояние — в _fx_state (правило .claude/rules/function-transform-state.md),
## поэтому анимация идёт на 60 fps и не дёргает интеракцию: экран нужен только
## чтобы ловить нажатие/отпускание мыши и держать модальность.
################################################################################

## Слой мини-игры ###############################################################

init python:

    ## Модель замка живёт отдельным планом. Ниже screens — зерно и вспышки
    ## накрывают её вместе со сценой; выше master — камера, вздрагивающая от
    ## ударов, до неё не дотягивается.
    if "lockgame" not in config.layers:
        renpy.add_layer("lockgame", below="screens")

## Изображения ##################################################################

## Щеколда (PSD Ch_1_Door _locks_2_RE). Композит-«бутерброд»: шток лежит МЕЖДУ
## основой корпуса и накладками, поэтому виден только в сквозных прорезях
## накладок, а всё остальное время прячется под ними. Порядок показа — в
## лейбле .show_latch, он и есть композиция.
##
## Требования к ассетам, код на них опирается:
##   1. Все PNG экспортированы С ОБЩЕГО ХОЛСТА, без обрезки по содержимому.
##      Тогда детали совпадают сами: каждая ставится центром в одну точку и
##      знать их размеры не нужно (см. c1s1_lock_part).
##   2. latch_stroke — шток целиком, во всю длину, включая часть, спрятанную
##      под накладками в запертом положении. Слева он должен быть длиннее хода
##      (C1S1_LATCH_PATH), иначе, уехав вправо, оголит пустоту.
##   3. latch_knob — только ушко: единственная деталь, идущая всем путём по
##      прорези, поэтому она отдельно от штока.
##   4. latch_shadow — тень НЕПОДВИЖНОЙ части. Тень штока, если понадобится,
##      заводится отдельным слоем и вешается на c1s1_latch_rod.
##
## В именах файлов накладок опечатка автора (owerlay) — пути оставлены как
## есть, чтобы не расходиться с ассетами; имена образов написаны правильно.
image chapter_1_latch_shadow = "images/1_chapter/lock_mini_game/latch/latch_shadow.png"
image chapter_1_latch_body = "images/1_chapter/lock_mini_game/latch/latch_body.png"
image chapter_1_latch_stroke = "images/1_chapter/lock_mini_game/latch/latch_stroke.png"
image chapter_1_latch_overlay_body = "images/1_chapter/lock_mini_game/latch/latch_body_owerlay_1.png"
image chapter_1_latch_overlay_keeper = "images/1_chapter/lock_mini_game/latch/latch_body_owerlay_2.png"
image chapter_1_latch_knob = "images/1_chapter/lock_mini_game/latch/latch_knob.png"

## Большой замок (папка big_lock). Корпус — цельный: и коробка, и ответная
## планка с прорезью, отдельной накладки нет. Язычок ходит ПОД корпусом и
## виден только в прорези планки и в зазоре между ней и коробкой.
##
## Холсты у деталей всё ещё разные: корпус ≈902×650, щеколда с тенью и тень
## вертушки — с прежнего ≈873×650, язычок — с ≈900×900, вертушка обрезана по
## силуэту. Расхождения вшиты в C1S1_BIG_*_OFF.
image chapter_1_big_lock_body = "images/1_chapter/lock_mini_game/big_lock/big_lock_body.png"
image chapter_1_big_lock_stroke = "images/1_chapter/lock_mini_game/big_lock/big_lock_stroke.png"
image chapter_1_big_lock_latch_shadow = "images/1_chapter/lock_mini_game/big_lock/big_lock_latch_shadow.png"
image chapter_1_big_lock_latch = "images/1_chapter/lock_mini_game/big_lock/big_lock_latch.png"
image chapter_1_big_lock_spin_shadow = "images/1_chapter/lock_mini_game/big_lock/big_lock_knob_spinner_shadow.png"
## Вертушка — обрезанная по силуэту (_crop), а не с холста всего замка: она
## единственная деталь, которая вращается, и крутиться должна вокруг СВОЕЙ оси.
## У обрезанного файла ось совпадает с центром холста, поэтому хватает обычного
## anchor (0.5, 0.5), а место на корпусе задаёт C1S1_BIG_SPIN_OFF.
image chapter_1_big_lock_spin = "images/1_chapter/lock_mini_game/big_lock/big_lock_knob_spinner_crop.png"

## Дверная ручка (папка door_handle). Обе детали с общего холста ≈640×940,
## поэтому смещения нулевые. Рычаг вращается вокруг своего основания, а не
## центра холста, — ось задаётся отдельно (C1S1_HANDLE_PIVOT).
image chapter_1_handle_body = "images/1_chapter/lock_mini_game/door_handle/door_handle_body.png"
image chapter_1_handle_lever = "images/1_chapter/lock_mini_game/door_handle/door_handle.png"

## Невидимый носитель драйвера: ATL-трансформ спрайта тикает каждый кадр, даже
## когда на экране ничего не меняется.
image chapter_1_mg_driver = Solid("#0000", xysize=(1, 1))

## Оверлей: сцена уходит в темноту, взаимодействие идёт уже не с ней.
image chapter_1_mg_overlay = Solid("#0a0806")

## Игровое состояние ############################################################

## Флаги замков — default: попадают в сохранения.
default c1s1_latch_open = False
default c1s1_big_lock_open = False
default c1s1_door_handle_open = False
## Время прохождения, сек. Развилки по нему появятся, когда будут все три
## замка; пока только замеряем.
default c1s1_locks_time = 0.0
## Стук идёт (драйвер бьёт в дверь) / мини-игра принимает ввод и считает время.
default c1s1_mg_knocking = False
default c1s1_mg_active = False
## Какой замок сейчас на экране — индекс в C1S1_MG_LOCK_ORDER.
default c1s1_mg_lock_i = 0

## Порядок замков и их флаги. Добавляя новый замок — дописывать сюда, заводить
## ему свои шаг/захват по образцу щеколды и лейбл показа .show_<замок>.
define C1S1_MG_LOCK_ORDER = ("latch", "big_lock", "door_handle")
define C1S1_MG_LOCK_FLAGS = {
    "latch": "c1s1_latch_open",
    "big_lock": "c1s1_big_lock_open",
    "door_handle": "c1s1_door_handle_open",
}

## Константы ####################################################################

## Кадр мини-игры. Камера встаёт неподвижно и по центру: кнопка «Открыть
## дверь» живёт в мировых координатах и не должна разъезжаться с дверью.
define C1S1_MG_ZOOM = 1.06
define C1S1_MG_SETTLE_T = 1.4   # доводка наезда до кадра мини-игры

## Оверлей и зерно.
define C1S1_MG_OVERLAY_ALPHA = 0.72
define C1S1_MG_OVERLAY_T = 0.9
define C1S1_MG_NOISE = 0.34     # покой сцены — FX_NOISE_DEFAULT

## Кнопка «Открыть дверь» — поверх замков на двери, тревожно моргает.
define C1S1_LOCKS_BTN_POS = (960, 800)
define C1S1_LOCKS_BTN_SIZE = (430, 190)

## Стук во время мини-игры. Интенсивность гуляет медленной волной: то
## нарастает (паузы короче, вспышки ярче, тряска сильнее), то стихает.
## Пары значений — (в тишине, на пике волны).
define C1S1_MG_KNOCK_GAP = (1.35, 0.40)     # пауза между ударами, сек
define C1S1_MG_KNOCK_FLASH = (0.13, 0.42)   # пик вспышки, доля белого
define C1S1_MG_KNOCK_FALL = (0.30, 0.14)    # спад вспышки, сек
define C1S1_MG_KNOCK_SHAKE = (7.0, 22.0)    # амплитуда вздрагивания кадра, px
define C1S1_MG_BAG_TREMBLE = (0.6, 4.4)     # дрожь сумки: покой → на ударе
define C1S1_MG_KNOCK_WAVE_T = 17.0          # период волны интенсивности, сек
define C1S1_MG_KNOCK_WAVE_NOISE = 0.15      # случайный разброс волны
define C1S1_MG_KNOCK_GAP_NOISE = 0.35       # случайный разброс паузы, доля
define C1S1_MG_SHAKE_TAU = 0.16             # затухание вздрагивания, сек
define C1S1_MG_SHAKE_FREQ = 9.0             # частота колебания вздрагивания, Гц

## Модель замка: одно место на все замки — центр экрана, крупно.
define C1S1_MG_LOCK_CENTER = (960, 540)
define C1S1_MG_LOCK_FADE_T = 0.45   # проявление модели и уход открытой

## Щеколда. Холст ассетов ≈ 750×350, поэтому в родном размере модель заняла бы
## меньше половины кадра — увеличиваем. Смещения деталей, ход и хит-зона
## заданы в пикселях АССЕТА и масштабируются вместе с моделью, поэтому zoom
## можно менять, не переподбирая остальное.
define C1S1_LATCH_ZOOM = 2.0

## Смещения центров деталей от центра модели. У слоёв с общего холста — нули,
## детали совпадают сами. Ненулевым остаётся только то, что экспортировано
## обрезанным по содержимому: такой слой встаёт центром своего силуэта в центр
## модели, и его надо доводить руками (Position Tuner, F9).
define C1S1_LATCH_SHADOW_OFF = (0, 0)
define C1S1_LATCH_BODY_OFF = (0, 0)
define C1S1_LATCH_STROKE_OFF = (0, -15)
define C1S1_LATCH_OVERLAY_BODY_OFF = (0, 0)
define C1S1_LATCH_OVERLAY_KEEPER_OFF = (0, 0)
define C1S1_LATCH_KNOB_OFF = (-15, 25)

## Путь ушка по прорези корпуса — три колена, как у настоящего шпингалета.
## Геометрия снята с latch_body_owerlay_1: сквозной канал идёт поперёк планки,
## слева от него прорезь ВНИЗ (заперто), справа — прорезь ВВЕРХ (открыто).
## Отсюда и порядок: ушко проворачивают ВВЕРХ из нижней прорези в канал, ведут
## ВПРАВО по каналу и в конце уводят ВВЕРХ, в верхнюю прорезь.
##
## Смещения — px ассета (масштабируются вместе с моделью), отрицательный y —
## вверх. Прогресс латча p ∈ [0, 3]: целая часть — номер пройденного колена.
define C1S1_LATCH_PATH = ((0, -40), (165, 0), (0, -38))

## Шток и ушко двигаются по-разному: шток только едет вправо (вертикаль — это
## его проворот вокруг оси, не сдвиг), ушко идёт всем путём.
define C1S1_LATCH_ROD_AXIS_ONLY = True

## Хит-зона захвата (dx, dy, w, h) в px ассета: центр зоны относительно центра
## ушка в запертом положении и её габариты. Зона едет вместе с ушком.
## Прямоугольник, а не маска по альфе: у ушка мелкий силуэт, попиксельная зона
## на нём ощущалась бы как случайная.
##
## dx/dy — ноль, пока ушко стоит центром своего холста в центре модели: зона
## тогда совпадает с ним сама. Правятся только если у ушка свой сдвиг
## (C1S1_LATCH_KNOB_OFF) или зону надо смещать намеренно.
define C1S1_LATCH_GRAB_BOX = (0, 0, 110, 90)

## Обвести хит-зону на экране — для подбора зоны и отладки промахов.
define C1S1_MG_DEBUG_HIT = False

## Отпустили на полпути — ушко сползает к началу текущего колена за это время
## (сек на колено). Пройденные колена остаются: ушко лежит в канале.
define C1S1_LATCH_RETURN_T = 0.45

## Большой замок ################################################################

## Порядок действий жёсткий: сдвинуть щеколду ВПРАВО и только после этого
## крутить вертушку ПРОТИВ ЧАСОВОЙ — язычок при этом уезжает вправо, в корпус.
## Прогресс big_p ∈ [0, 2]: 0→1 щеколда, 1→2 оборот вертушки с язычком.
## Назад ничего не сползает: и щеколда, и вертушка держатся сами.
define C1S1_BIG_LOCK_ZOOM = 1.4

## Смещения центров деталей от центра модели, px ассета. Ноль — у корпуса, он
## задаёт систему координат модели; остальным сдвиг нужен ровно настолько,
## насколько их холст расходится с корпусом.
define C1S1_BIG_BODY_OFF = (0, 0)
define C1S1_BIG_STROKE_OFF = (159, 125)
define C1S1_BIG_LATCH_SHADOW_OFF = (0, 0)
define C1S1_BIG_LATCH_OFF = (0, 0)
define C1S1_BIG_SPIN_SHADOW_OFF = (0, 0)
## Вертушка обрезана по силуэту, поэтому её смещение — это и есть ось: точка
## на корпусе, вокруг которой она крутится.
define C1S1_BIG_SPIN_OFF = (206, -15)

## Щеколда большого замка: ход вправо и зона хвата (dx, dy, w, h) от центра
## модели, px ассета. Зона едет вместе с щеколдой.
define C1S1_BIG_LATCH_TRAVEL = 70
define C1S1_BIG_LATCH_GRAB_BOX = (261, 205, 300, 150)

## Зона хвата вертушки — радиус от оси, px ассета.
define C1S1_BIG_SPIN_RADIUS = 135
define C1S1_BIG_SPIN_TURN = 360.0   # полный оборот до открытия, градусов

## Ход язычка вправо (в коробку) за полный оборот вертушки, px ассета. Снаружи
## он виден только в прорези планки и в зазоре за ней — этого хода хватает,
## чтобы оба опустели; остальная длина язычка и так под корпусом.
define C1S1_BIG_STROKE_TRAVEL = 120

## Дверная ручка ################################################################

## Самый простой замок: рычаг тянут вниз до упора. Отпустили на полпути —
## возвращается сам, как настоящая подпружиненная ручка.
define C1S1_HANDLE_ZOOM = 1.0

## Смещения деталей от центра модели: обе с общего холста, поэтому нули.
define C1S1_HANDLE_BODY_OFF = (0, 0)
define C1S1_HANDLE_OFF = (0, 0)

## Ось рычага — центр его круглого основания, px ассета от центра холста.
## Размер холста нужен, чтобы пересчитать ось в якорь (доли стороны): вращать
## вокруг центра холста нельзя, рычаг бы вымахивал по дуге целиком.
define C1S1_HANDLE_CANVAS = (640, 940)
define C1S1_HANDLE_PIVOT = (-178, -105)

## Ход рычага вниз до открытия, градусов. Положительный rotate в Ren'Py крутит
## по часовой — свободный конец рычага при этом идёт вниз, что и нужно.
define C1S1_HANDLE_TURN = 45.0

## Зона хвата (dx, dy, w, h) в px ассета от ОСИ, в системе самого рычага:
## поворачивается вместе с ним, поэтому держать можно за любую его точку.
define C1S1_HANDLE_GRAB_BOX = (240, 0, 520, 180)

## Отпустили — рычаг возвращается вверх за это время (сек на весь ход).
define C1S1_HANDLE_RETURN_T = 0.35
## Пауза после открытия замка перед сменой на следующий (и перед выходом).
define C1S1_MG_DONE_HOLD_T = 0.7
define C1S1_MG_POLL_T = 0.15    # период опроса готовности экраном

## Порядок слоёв. Оверлей на master поверх сцены и сумки; модель замка живёт
## на слое экранов и в этот порядок не входит.
define C1S1_Z_MG_DRIVER = 1
define C1S1_Z_MG_OVERLAY = 50

## Логика #######################################################################

init -5 python:

    import math

    ## Всё состояние мини-игры — в _fx_state под общим префиксом: трансформы
    ## пересобираются на каждом restart_interaction, атрибуты trans при этом
    ## теряются (правило function-transform-state).
    C1S1_MG_KEY = "c1s1_mg_"

    def _mg_get(name, default=0.0):
        return _fx_state.get(C1S1_MG_KEY + name, default)

    def _mg_set(name, value):
        _fx_state[C1S1_MG_KEY + name] = value
        return value

    def _mg_lerp(a, b, t):
        return a + (b - a) * max(0.0, min(1.0, t))

    def c1s1_mg_reset():
        """Чистый старт мини-игры: время, расписание ударов, ход засова."""
        for name in ("st", "elapsed", "play_t", "wave", "shake_a", "shake_t",
                     "latch_p", "latch_grab", "latch_last_mx", "latch_last_my",
                     "big_p", "big_grab", "big_last_mx", "big_last_a",
                     "handle_p", "handle_grab", "handle_last_a"):
            _mg_set(name, 0.0)
        ## Отрицательные — «ещё не было»: первый удар и момент готовности.
        _mg_set("knock_next", -1.0)
        _mg_set("done", -1.0)

    def c1s1_mg_stop():
        """Гасим вздрагивание перед снятием драйвера: без его тика shake_t
        перестаёт расти, и кадр застыл бы в середине колебания."""
        _mg_set("shake_a", 0.0)
        _mg_set("shake_t", 0.0)

    def c1s1_mg_elapsed():
        """Время именно прохождения замков: часы идут, пока экран мини-игры
        принимает ввод. Ожидание у кнопки «Открыть дверь» в счёт не идёт —
        там тикают только часы стука (elapsed)."""
        return _mg_get("play_t")

    ## Последовательность замков #################################################

    def c1s1_mg_lock():
        """Замок, который сейчас на экране; None — все открыты."""
        i = store.c1s1_mg_lock_i
        if 0 <= i < len(C1S1_MG_LOCK_ORDER):
            return C1S1_MG_LOCK_ORDER[i]
        return None

    def c1s1_mg_lock_open(lock=None):
        """Текущий (или названный) замок уже открыт?"""
        lock = lock or c1s1_mg_lock()
        if lock is None:
            return True
        return getattr(store, C1S1_MG_LOCK_FLAGS[lock], False)

    def c1s1_mg_check_done():
        """Опрос из таймера экрана. Замок открывается внутри трансформа, минуя
        action, поэтому сам экран о готовности не узнаёт. Выдержав паузу (чтобы
        игрок увидел результат), закрываем экран — дальше лейбл убирает модель
        и берётся за следующий замок."""
        if not store.c1s1_mg_active or not c1s1_mg_lock_open():
            return

        t = _mg_get("play_t")
        if _mg_get("done") < 0.0:
            _mg_set("done", t)
            return
        if t - _mg_get("done") >= C1S1_MG_DONE_HOLD_T:
            _mg_set("done", -1.0)
            renpy.end_interaction("done")

    ## Вздрагивание кадра ########################################################

    def c1s1_mg_shake_env():
        """Огибающая вздрагивания 0..1: 1 сразу после удара, дальше затухает."""
        amp = _mg_get("shake_a")
        if amp <= 0.01:
            return 0.0
        decay = math.exp(-_mg_get("shake_t") / max(0.01, C1S1_MG_SHAKE_TAU))
        return min(1.0, amp * decay / max(1.0, C1S1_MG_KNOCK_SHAKE[1]))

    def c1s1_mg_shake_offset():
        """Смещение кадра по вертикали: затухающее колебание после удара."""
        amp = _mg_get("shake_a")
        if amp <= 0.01:
            return 0.0
        t = _mg_get("shake_t")
        decay = math.exp(-t / max(0.01, C1S1_MG_SHAKE_TAU))
        return amp * decay * math.sin(2.0 * math.pi * C1S1_MG_SHAKE_FREQ * t)

    ## Драйвер ###################################################################

    def c1s1_mg_knock_step():
        """Расписание ударов. Волна интенсивности (косинус периодом
        C1S1_MG_KNOCK_WAVE_T плюс шум) задаёт и паузу до следующего удара, и
        его силу: стук то нарастает, то стихает, но не прекращается."""
        t = _mg_get("elapsed")
        nxt = _mg_get("knock_next")

        ## Первый удар — не сразу: даём кадру встать.
        if nxt < 0.0:
            _mg_set("knock_next", t + C1S1_MG_KNOCK_GAP[0])
            return
        if t < nxt:
            return

        wave = 0.5 - 0.5 * math.cos(2.0 * math.pi * t / max(1.0, C1S1_MG_KNOCK_WAVE_T))
        wave += renpy.random.uniform(-C1S1_MG_KNOCK_WAVE_NOISE, C1S1_MG_KNOCK_WAVE_NOISE)
        wave = max(0.0, min(1.0, wave))
        _mg_set("wave", wave)

        gap = _mg_lerp(C1S1_MG_KNOCK_GAP[0], C1S1_MG_KNOCK_GAP[1], wave)
        gap *= 1.0 + renpy.random.uniform(-C1S1_MG_KNOCK_GAP_NOISE, C1S1_MG_KNOCK_GAP_NOISE)
        _mg_set("knock_next", t + max(0.15, gap))

        ## TODO(звук): удар в дверь (добавим позже).
        flash_fx(high=_mg_lerp(C1S1_MG_KNOCK_FLASH[0], C1S1_MG_KNOCK_FLASH[1], wave),
                 fall=_mg_lerp(C1S1_MG_KNOCK_FALL[0], C1S1_MG_KNOCK_FALL[1], wave))
        _mg_set("shake_a", _mg_lerp(C1S1_MG_KNOCK_SHAKE[0], C1S1_MG_KNOCK_SHAKE[1], wave))
        _mg_set("shake_t", 0.0)

    def c1s1_mg_driver_f(trans, st, at):
        """Единый тик мини-игры: время, стук, ход текущего замка. dt считаем
        сами — st переживает пересборку трансформа, но при рестарте уходит в
        ноль, поэтому отрицательные и слишком большие шаги отбрасываем."""
        dt = st - _mg_get("st", st)
        if dt < 0.0 or dt > 0.25:
            dt = 0.0
        _mg_set("st", st)
        _mg_set("shake_t", _mg_get("shake_t") + dt)

        if store.c1s1_mg_knocking:
            _mg_set("elapsed", _mg_get("elapsed") + dt)
            c1s1_mg_knock_step()

        if store.c1s1_mg_active:
            _mg_set("play_t", _mg_get("play_t") + dt)
            lock = c1s1_mg_lock()
            if lock == "latch":
                c1s1_latch_step(dt)
            elif lock == "big_lock":
                c1s1_big_step(dt)
            elif lock == "door_handle":
                c1s1_handle_step(dt)

        trans.alpha = 0.0
        return 0.0

    ## Камера ####################################################################

    def c1s1_mg_camera_f(strength, smooth, key, trans, st, at):
        """Кадр за оверлеем: параллакс за мышкой плюс вздрагивание от ударов.
        Дверь продолжает жить, пока игрок возится с замком. Вздрагивание
        кладём в те же ключи _fx_state, что и дрожь mouse_parallax_f, — его
        подхватывает follow_camera у кнопки «Открыть дверь»."""
        strength = _fx_num(strength, 10.0, 0.0)
        if not FX_MOUSE_PARALLAX_ON:
            strength = 0.0
        smooth = _fx_num(smooth, 0.06, 0.001, 1.0)

        mx, my = renpy.get_mouse_pos()
        tx = -(mx / float(config.screen_width) - 0.5) * 2.0 * strength
        ty = -(my / float(config.screen_height) - 0.5) * 2.0 * strength
        px = _fx_step(key + "_px", tx, smooth, start=0.0)
        py = _fx_step(key + "_py", ty, smooth, start=0.0)

        sy = c1s1_mg_shake_offset()
        _fx_state[key + "_jx"] = 0.0
        _fx_state[key + "_jy"] = sy

        trans.xoffset = px
        trans.yoffset = py + sy
        return 1.0 / 60.0

    ## Модель замка ##############################################################

    def c1s1_lock_pos(center_xy, off_xy, z):
        """Центр детали на экране. Смещение задано в пикселях ассета, поэтому
        масштабируется вместе с моделью. Только int: дробные значения в pos
        Ren'Py трактует как доли экрана и деталь молча улетает за кадр."""
        return (int(round(center_xy[0] + off_xy[0] * z)),
                int(round(center_xy[1] + off_xy[1] * z)))

    ## Щеколда ###################################################################

    def c1s1_latch_max_p():
        """Прогресс полностью открытой щеколды — по числу колен пути.
        Функция, а не константа: define'ы считаются на init 0, позже этого
        блока, и на этапе загрузки C1S1_LATCH_PATH ещё не существует."""
        return float(len(C1S1_LATCH_PATH))

    def c1s1_latch_offset(p):
        """Смещение ушка от запертого положения на прогрессе p (экранные px:
        путь задан в px ассета и масштабируется вместе с моделью)."""
        z = C1S1_LATCH_ZOOM
        ox = oy = 0.0
        for i, (vx, vy) in enumerate(C1S1_LATCH_PATH):
            if p >= i + 1:
                ox += vx * z
                oy += vy * z
            elif p > i:
                f = p - i
                ox += vx * z * f
                oy += vy * z * f
                break
            else:
                break
        return ox, oy

    def c1s1_latch_hit(mx, my):
        """Курсор на ушке? Хит-зона — C1S1_LATCH_GRAB_BOX вокруг ушка,
        едущая вместе с ним. Координаты экранные: модель нарисована поверх
        оверлея и с камерой не связана."""
        cx, cy, bw, bh = c1s1_latch_hit_rect()
        return abs(mx - cx) <= bw * 0.5 and abs(my - cy) <= bh * 0.5

    def c1s1_latch_hit_rect():
        """Хит-зона в экранных px: (центр x, центр y, ширина, высота).
        Отдельно от проверки — её же рисует отладочная обводка."""
        z = C1S1_LATCH_ZOOM
        dx, dy, bw, bh = C1S1_LATCH_GRAB_BOX
        ox, oy = c1s1_latch_offset(_mg_get("latch_p"))
        return (C1S1_MG_LOCK_CENTER[0] + (dx + C1S1_LATCH_KNOB_OFF[0]) * z + ox,
                C1S1_MG_LOCK_CENTER[1] + (dy + C1S1_LATCH_KNOB_OFF[1]) * z + oy,
                bw * z, bh * z)

    def c1s1_latch_hit_pos():
        """Левый-верхний угол хит-зоны, int — для отладочной рамки."""
        cx, cy, bw, bh = c1s1_latch_hit_rect()
        return (int(round(cx - bw * 0.5)), int(round(cy - bh * 0.5)))

    def c1s1_latch_hit_size():
        cx, cy, bw, bh = c1s1_latch_hit_rect()
        return (int(round(bw)), int(round(bh)))

    def c1s1_latch_grab():
        """Нажали мышь: если попали по ушку — взяли щеколду."""
        mx, my = renpy.get_mouse_pos()
        if not c1s1_latch_hit(mx, my):
            return
        _mg_set("latch_grab", 1.0)
        _mg_set("latch_last_mx", mx)
        _mg_set("latch_last_my", my)

    def c1s1_latch_step(dt):
        """Ход щеколды по коленам прорези. Пока держим — движение мыши
        проецируется на ось текущего колена: тянешь вверх — ушко выходит из
        нижней прорези, вправо — засов едет по каналу, снова вверх — ушко
        садится в верхнюю прорезь. Дошли до конца пути — щеколда открыта."""
        max_p = c1s1_latch_max_p()
        if store.c1s1_latch_open:
            _mg_set("latch_p", max_p)
            return

        p = _mg_get("latch_p")

        if _mg_get("latch_grab") > 0.5:
            mx, my = renpy.get_mouse_pos()
            dx = mx - _mg_get("latch_last_mx")
            dy = my - _mg_get("latch_last_my")
            _mg_set("latch_last_mx", mx)
            _mg_set("latch_last_my", my)

            ## Ось текущего колена. На стыке (p ровно целое) берём то колено,
            ## в которое движемся дальше, — иначе на границе ввод замирает.
            seg = int(min(p, max_p - 0.001))
            vx, vy = C1S1_LATCH_PATH[seg]
            span2 = (vx * vx + vy * vy) * C1S1_LATCH_ZOOM * C1S1_LATCH_ZOOM
            if span2 > 1.0:
                ## Проекция движения мыши на ось колена, в долях его длины.
                p += (dx * vx + dy * vy) * C1S1_LATCH_ZOOM / span2
            p = max(0.0, min(max_p, p))
            _mg_set("latch_p", p)

            if p >= max_p:
                ## TODO(звук): лязг отодвинутой щеколды (добавим позже).
                _mg_set("latch_grab", 0.0)
                store.c1s1_latch_open = True
            return

        ## Отпустили. Назад сползают только вертикальные колена — проворот и
        ## посадка ушка: их держит рука, а не корпус. В горизонтальном канале
        ## засов просто лежит там, где его бросили.
        seg = int(min(p, max_p - 0.001))
        if C1S1_LATCH_PATH[seg][1] == 0:
            return
        target = float(int(p))
        _mg_set("latch_p", max(target, p - dt / max(0.05, C1S1_LATCH_RETURN_T)))

    def c1s1_latch_rod_f(trans, st, at):
        """Шток: только вдоль своей оси. Вертикаль пути — это его проворот
        вокруг оси, сам шток при этом не поднимается."""
        ox, oy = c1s1_latch_offset(_mg_get("latch_p"))
        trans.xoffset = ox
        trans.yoffset = 0.0 if C1S1_LATCH_ROD_AXIS_ONLY else oy
        return 1.0 / 60.0

    def c1s1_latch_knob_f(trans, st, at):
        """Ушко идёт всем путём — по нему игрок и читает состояние замка."""
        ox, oy = c1s1_latch_offset(_mg_get("latch_p"))
        trans.xoffset = ox
        trans.yoffset = oy
        return 1.0 / 60.0

    ## Большой замок #############################################################

    def c1s1_big_spin_center():
        """Ось вертушки в экранных координатах. Файл обрезан по силуэту,
        поэтому ось — это просто центр детали."""
        z = C1S1_BIG_LOCK_ZOOM
        return (C1S1_MG_LOCK_CENTER[0] + C1S1_BIG_SPIN_OFF[0] * z,
                C1S1_MG_LOCK_CENTER[1] + C1S1_BIG_SPIN_OFF[1] * z)

    def c1s1_big_spin_angle(mx, my):
        cx, cy = c1s1_big_spin_center()
        return math.degrees(math.atan2(my - cy, mx - cx))

    def c1s1_big_latch_hit(mx, my):
        z = C1S1_BIG_LOCK_ZOOM
        dx, dy, bw, bh = C1S1_BIG_LATCH_GRAB_BOX
        shift = C1S1_BIG_LATCH_TRAVEL * z * min(1.0, _mg_get("big_p"))
        cx = C1S1_MG_LOCK_CENTER[0] + (dx + C1S1_BIG_LATCH_OFF[0]) * z + shift
        cy = C1S1_MG_LOCK_CENTER[1] + (dy + C1S1_BIG_LATCH_OFF[1]) * z
        return abs(mx - cx) <= bw * z * 0.5 and abs(my - cy) <= bh * z * 0.5

    def c1s1_big_spin_hit(mx, my):
        """Круглая зона — у вертушки круглый силуэт, прямоугольник ловил бы
        углы, где её нет."""
        cx, cy = c1s1_big_spin_center()
        r = C1S1_BIG_SPIN_RADIUS * C1S1_BIG_LOCK_ZOOM
        return (mx - cx) ** 2 + (my - cy) ** 2 <= r * r

    def c1s1_big_grab():
        """Пока щеколда не отодвинута, вертушка не отзывается — порядок
        действий задан жёстко."""
        mx, my = renpy.get_mouse_pos()
        if _mg_get("big_p") < 1.0:
            if c1s1_big_latch_hit(mx, my):
                _mg_set("big_grab", 1.0)
                _mg_set("big_last_mx", mx)
            return
        if c1s1_big_spin_hit(mx, my):
            _mg_set("big_grab", 2.0)
            _mg_set("big_last_a", c1s1_big_spin_angle(mx, my))

    def c1s1_big_step(dt):
        """Два этапа. Щеколда: движение мыши вдоль её оси. Вертушка: угол,
        накопленный вокруг оси, — крутить надо против часовой. Назад ничего
        не сползает, обе детали держатся сами."""
        if store.c1s1_big_lock_open:
            _mg_set("big_p", 2.0)
            return
        if _mg_get("big_grab") < 0.5:
            return

        p = _mg_get("big_p")
        mx, my = renpy.get_mouse_pos()

        if _mg_get("big_grab") < 1.5:
            dx = mx - _mg_get("big_last_mx")
            _mg_set("big_last_mx", mx)
            p += dx / max(1.0, C1S1_BIG_LATCH_TRAVEL * C1S1_BIG_LOCK_ZOOM)
            p = max(0.0, min(1.0, p))
        else:
            ## На экране ось y смотрит вниз, поэтому atan2 растёт ПО часовой —
            ## против часовой это его убывание, отсюда минус.
            a = c1s1_big_spin_angle(mx, my)
            da = a - _mg_get("big_last_a")
            while da > 180.0:
                da -= 360.0
            while da < -180.0:
                da += 360.0
            _mg_set("big_last_a", a)
            p += -da / max(1.0, C1S1_BIG_SPIN_TURN)
            p = max(1.0, min(2.0, p))

        _mg_set("big_p", p)
        if p >= 2.0:
            ## TODO(звук): щелчок ригеля большого замка (добавим позже).
            _mg_set("big_grab", 0.0)
            store.c1s1_big_lock_open = True

    def c1s1_big_turn():
        """Доля пройденного оборота 0..1 — по ней идут и вертушка, и шток."""
        return max(0.0, min(1.0, _mg_get("big_p") - 1.0))

    def c1s1_big_latch_f(trans, st, at):
        trans.xoffset = C1S1_BIG_LATCH_TRAVEL * C1S1_BIG_LOCK_ZOOM * min(1.0, _mg_get("big_p"))
        return 1.0 / 60.0

    def c1s1_big_stroke_f(trans, st, at):
        trans.xoffset = C1S1_BIG_STROKE_TRAVEL * C1S1_BIG_LOCK_ZOOM * c1s1_big_turn()
        return 1.0 / 60.0

    def c1s1_big_spin_f(trans, st, at):
        ## Против часовой — отрицательный rotate: положительный в Ren'Py
        ## крутит по часовой.
        trans.rotate = -C1S1_BIG_SPIN_TURN * c1s1_big_turn()
        return 1.0 / 60.0

    ## Дверная ручка #############################################################

    def c1s1_handle_anchor():
        """Якорь рычага — его ось в долях холста. Ось задана в px от центра
        холста, размер холста — константой рядом: у обеих деталей ручки он
        общий и меняется только вместе с переэкспортом."""
        w, h = C1S1_HANDLE_CANVAS
        return (0.5 + C1S1_HANDLE_PIVOT[0] / float(max(1, w)),
                0.5 + C1S1_HANDLE_PIVOT[1] / float(max(1, h)))

    def c1s1_handle_pivot_screen():
        z = C1S1_HANDLE_ZOOM
        return (C1S1_MG_LOCK_CENTER[0] + (C1S1_HANDLE_OFF[0] + C1S1_HANDLE_PIVOT[0]) * z,
                C1S1_MG_LOCK_CENTER[1] + (C1S1_HANDLE_OFF[1] + C1S1_HANDLE_PIVOT[1]) * z)

    def c1s1_handle_angle(mx, my):
        cx, cy = c1s1_handle_pivot_screen()
        return math.degrees(math.atan2(my - cy, mx - cx))

    def c1s1_handle_hit(mx, my):
        """Курсор на рычаге? Точку переводим в систему самого рычага — крутим
        назад на его текущий угол — и проверяем прямоугольником. Так зона
        едет и поворачивается вместе с ним, и держать можно за любое место."""
        z = C1S1_HANDLE_ZOOM
        cx, cy = c1s1_handle_pivot_screen()
        a = math.radians(C1S1_HANDLE_TURN * _mg_get("handle_p"))
        dx, dy = mx - cx, my - cy
        lx = dx * math.cos(a) + dy * math.sin(a)
        ly = -dx * math.sin(a) + dy * math.cos(a)
        bx, by, bw, bh = C1S1_HANDLE_GRAB_BOX
        return abs(lx - bx * z) <= bw * z * 0.5 and abs(ly - by * z) <= bh * z * 0.5

    def c1s1_handle_grab():
        mx, my = renpy.get_mouse_pos()
        if not c1s1_handle_hit(mx, my):
            return
        _mg_set("handle_grab", 1.0)
        _mg_set("handle_last_a", c1s1_handle_angle(mx, my))

    def c1s1_handle_step(dt):
        """Рычаг идёт за курсором по углу вокруг оси: тянешь вниз — угол
        растёт (на экране y вниз, поэтому вниз это рост atan2). Отпустил, не
        дотянув, — рычаг возвращается вверх сам."""
        if store.c1s1_door_handle_open:
            _mg_set("handle_p", 1.0)
            return

        p = _mg_get("handle_p")

        if _mg_get("handle_grab") > 0.5:
            mx, my = renpy.get_mouse_pos()
            a = c1s1_handle_angle(mx, my)
            da = a - _mg_get("handle_last_a")
            while da > 180.0:
                da -= 360.0
            while da < -180.0:
                da += 360.0
            _mg_set("handle_last_a", a)
            p = max(0.0, min(1.0, p + da / max(1.0, C1S1_HANDLE_TURN)))
            _mg_set("handle_p", p)
            if p >= 1.0:
                ## TODO(звук): щелчок дверной ручки (добавим позже).
                _mg_set("handle_grab", 0.0)
                store.c1s1_door_handle_open = True
            return

        _mg_set("handle_p", max(0.0, p - dt / max(0.05, C1S1_HANDLE_RETURN_T)))

    def c1s1_handle_f(trans, st, at):
        trans.rotate = C1S1_HANDLE_TURN * _mg_get("handle_p")
        return 1.0 / 60.0

    ## Ввод ######################################################################

    def c1s1_mg_grab():
        """Нажатие мыши уходит текущему замку — у каждого свой захват."""
        if not store.c1s1_mg_active or c1s1_mg_lock_open():
            return
        lock = c1s1_mg_lock()
        if lock == "latch":
            c1s1_latch_grab()
        elif lock == "big_lock":
            c1s1_big_grab()
        elif lock == "door_handle":
            c1s1_handle_grab()

    def c1s1_mg_release():
        _mg_set("latch_grab", 0.0)
        _mg_set("big_grab", 0.0)
        _mg_set("handle_grab", 0.0)

    def c1s1_mg_open_all():
        """Все замки разом — для пропуска сцены."""
        for flag in C1S1_MG_LOCK_FLAGS.values():
            setattr(store, flag, True)

    ## Сумка #####################################################################

    def c1s1_mg_bag_f(trans, st, at):
        """Дрожь сумки следует за ударами: в тишине едва заметная, на ударе
        рывок. Накопители — как у object_jitter_f, своим ключом."""
        amp = _mg_lerp(C1S1_MG_BAG_TREMBLE[0], C1S1_MG_BAG_TREMBLE[1],
                       c1s1_mg_shake_env())
        trans.xoffset = _fx_step("c1s1_mg_bag_jx", renpy.random.uniform(-amp, amp), 0.5, start=0.0)
        trans.yoffset = _fx_step("c1s1_mg_bag_jy", renpy.random.uniform(-amp, amp), 0.5, start=0.0)
        return 1.0 / 60.0

## Трансформы ###################################################################

## Драйвер: невидим, тикает каждый кадр.
transform c1s1_mg_driver():
    subpixel True
    alpha 0.0
    pos (0, 0)
    function c1s1_mg_driver_f

## Камера за оверлеем. Начальный zoom НЕ задаётся намеренно: состояние камеры
## переживает смену `camera at`, поэтому наезд предыдущего кадра плавно
## доводится до C1S1_MG_ZOOM, без скачка. rotate сбрасываем явно — по той же
## причине (см. комментарий у mouse_parallax).
transform c1s1_mg_camera(z1=C1S1_MG_ZOOM, t=C1S1_MG_SETTLE_T, strength=8.0, smooth=0.06, key="cam"):
    subpixel True
    align (0.5, 0.5)
    rotate 0.0
    parallel:
        ease t zoom z1
    parallel:
        function renpy.curry(c1s1_mg_camera_f)(strength, smooth, key)

## Оверлей: наплывает и держится всю мини-игру.
transform c1s1_mg_overlay_in(a=C1S1_MG_OVERLAY_ALPHA, t=C1S1_MG_OVERLAY_T):
    align (0.5, 0.5)
    alpha 0.0
    ease t alpha a

transform c1s1_mg_overlay_out(a=C1S1_MG_OVERLAY_ALPHA, t=C1S1_MG_OVERLAY_T):
    align (0.5, 0.5)
    alpha a
    ease t alpha 0.0

## Неподвижная деталь модели.
transform c1s1_lock_part(off_xy, center_xy, z):
    subpixel True
    anchor (0.5, 0.5)
    zoom z
    pos c1s1_lock_pos(center_xy, off_xy, z)

## Шток щеколды: едет вправо по каналу.
transform c1s1_latch_rod(off_xy, center_xy, z):
    subpixel True
    anchor (0.5, 0.5)
    zoom z
    pos c1s1_lock_pos(center_xy, off_xy, z)
    xoffset 0.0 yoffset 0.0
    function c1s1_latch_rod_f

## Ушко штока: идёт всем путём по прорези корпуса.
transform c1s1_latch_knob(off_xy, center_xy, z):
    subpixel True
    anchor (0.5, 0.5)
    zoom z
    pos c1s1_lock_pos(center_xy, off_xy, z)
    xoffset 0.0 yoffset 0.0
    function c1s1_latch_knob_f

## Щеколда большого замка и её тень: едут вправо вместе.
transform c1s1_big_latch_slide(off_xy, center_xy, z):
    subpixel True
    anchor (0.5, 0.5)
    zoom z
    pos c1s1_lock_pos(center_xy, off_xy, z)
    xoffset 0.0
    function c1s1_big_latch_f

## Шток большого замка: уезжает вправо, в корпус, пока крутится вертушка.
transform c1s1_big_stroke_slide(off_xy, center_xy, z):
    subpixel True
    anchor (0.5, 0.5)
    zoom z
    pos c1s1_lock_pos(center_xy, off_xy, z)
    xoffset 0.0
    function c1s1_big_stroke_f

## Вертушка: крутится вокруг своего центра — файл обрезан по силуэту, поэтому
## центр детали и есть её ось. transform_anchor обязателен (правило
## .claude/rules/rotate-transform-anchor.md): без него активный rotate расширил
## бы холст спрайта до квадрата и якорь считался бы уже от него.
transform c1s1_big_spinner(off_xy, center_xy, z):
    subpixel True
    transform_anchor True
    anchor (0.5, 0.5)
    zoom z
    pos c1s1_lock_pos(center_xy, off_xy, z)
    rotate 0.0
    function c1s1_big_spin_f

## Рычаг дверной ручки: вращается вокруг своего основания. Якорь переносится
## в ось, позиция компенсирует перенос тем же сдвигом. transform_anchor
## обязателен (правило .claude/rules/rotate-transform-anchor.md).
transform c1s1_handle_lever(off_xy, center_xy, z):
    subpixel True
    transform_anchor True
    anchor c1s1_handle_anchor()
    zoom z
    pos c1s1_lock_pos(center_xy, (off_xy[0] + C1S1_HANDLE_PIVOT[0], off_xy[1] + C1S1_HANDLE_PIVOT[1]), z)
    rotate 0.0
    function c1s1_handle_f

## Сумка у стены на время мини-игры: дрожь привязана к ударам.
transform c1s1_mg_bag(pos_xy, anchor_xy):
    subpixel True
    anchor anchor_xy
    pos pos_xy
    xoffset 0.0 yoffset 0.0
    function c1s1_mg_bag_f

## Экраны #######################################################################

## Кнопка «Открыть дверь». Живёт в мире (follow_camera с зумом кадра
## мини-игры) — держится за дверь, пока камера дышит параллаксом и вздрагивает
## от ударов.
screen c1s1_locks_open_door():
    modal True
    fixed:
        at follow_camera(zoom_pad=C1S1_MG_ZOOM)
        xysize (config.screen_width, config.screen_height)
        use glow_button(
            _("Открыть дверь"),
            Return("done"),
            bg="dark",
            pulse="alarm",
            pos=C1S1_LOCKS_BTN_POS,
            size=C1S1_LOCKS_BTN_SIZE)

## Мини-игра. Экран ничего не рисует: модель замка живёт спрайтами на слое
## lockgame, дверь и оверлей — на master. Здесь только мышь и модальность.
screen c1s1_locks_minigame():
    modal True

    key "mousedown_1" action Function(c1s1_mg_grab)
    key "mouseup_1" action Function(c1s1_mg_release)

    timer C1S1_MG_POLL_T action Function(c1s1_mg_check_done) repeat True

    ## Отладка: где именно ловится захват. Рамка обновляется на таймере опроса,
    ## поэтому за ушком тянется с шагом C1S1_MG_POLL_T — этого хватает, чтобы
    ## понять, попадает зона по ушку или мимо.
    if C1S1_MG_DEBUG_HIT and c1s1_mg_lock() == "latch":
        add Solid("#00ff0040"):
            pos c1s1_latch_hit_pos()
            xysize c1s1_latch_hit_size()

## Сцена ########################################################################

label chapter_1_scene_1_minigame_locks:

    ## Камера доводит наезд до кадра мини-игры и встаёт: дальше она только
    ## дышит параллаксом и вздрагивает от ударов, поэтому кнопка в мировых
    ## координатах не разъезжается с дверью.
    camera at c1s1_mg_camera()

    ## Драйвер стука включается до кнопки — удары не прерываются ни на кадр.
    $ c1s1_mg_reset()
    show chapter_1_mg_driver zorder C1S1_Z_MG_DRIVER at c1s1_mg_driver()
    show chapter_1_hall_door_bag zorder C1S1_Z_DOOR_BAG at c1s1_mg_bag(C1S1_DOOR_BAG_POS, C1S1_DOOR_BAG_ANCHOR)
    $ c1s1_mg_knocking = True

    $ pause(C1S1_MG_SETTLE_T)

    ## Развилок и влияния на состояние игры пока нет — при пропуске сцена
    ## проходится насквозь (правило .claude/rules/skippable-scenes.md).
    ## TODO: убрать guard, когда появятся развилки по времени.
    if not renpy.is_skipping():
        call screen c1s1_locks_open_door

    ## Сцена уходит в темноту под оверлеем, зерно поднимается. Дверь за ним
    ## продолжает вздрагивать от ударов — но игрок теперь не с ней.
    show chapter_1_mg_overlay zorder C1S1_Z_MG_OVERLAY at c1s1_mg_overlay_in()
    $ fx_noise_strength = C1S1_MG_NOISE
    $ pause(C1S1_MG_OVERLAY_T)

    ## Замки по одному, в порядке C1S1_MG_LOCK_ORDER. Время идёт, стук не
    ## прекращается.
    $ c1s1_mg_lock_i = 0
    if renpy.is_skipping():
        $ c1s1_mg_open_all()
    else:
        while c1s1_mg_lock() is not None:
            call .play_lock from _call_c1s1_mg_play_lock

    ## Итог: время прохождения. Развилки по нему появятся, когда будут все три
    ## замка — пока только замеряем.
    $ c1s1_locks_time = c1s1_mg_elapsed()

    ## Мир возвращается: стук стихает, зерно и оверлей отпускают.
    $ c1s1_mg_knocking = False
    $ fx_noise_strength = FX_NOISE_DEFAULT
    show chapter_1_mg_overlay zorder C1S1_Z_MG_OVERLAY at c1s1_mg_overlay_out()
    $ pause(C1S1_MG_OVERLAY_T)
    hide chapter_1_mg_overlay

    ## Драйвер снимаем последним, погасив вздрагивание (см. c1s1_mg_stop).
    $ c1s1_mg_stop()
    hide chapter_1_mg_driver

    return

## Один замок: модель проявляется на своём слое, игрок с ней возится, открытый
## замок уходит и освобождает место следующему. Переходы — только на слое
## lockgame (renpy.transition с layer), чтобы дверь и оверлей не мигали.
label .play_lock:

    $ renpy.transition(Dissolve(C1S1_MG_LOCK_FADE_T), layer="lockgame")
    if c1s1_mg_lock() == "latch":
        call .show_latch from _call_c1s1_mg_show_latch
    elif c1s1_mg_lock() == "big_lock":
        call .show_big_lock from _call_c1s1_mg_show_big_lock
    elif c1s1_mg_lock() == "door_handle":
        call .show_door_handle from _call_c1s1_mg_show_door_handle
    $ pause(C1S1_MG_LOCK_FADE_T)

    $ c1s1_mg_active = True
    call screen c1s1_locks_minigame
    $ c1s1_mg_active = False

    $ renpy.transition(Dissolve(C1S1_MG_LOCK_FADE_T), layer="lockgame")
    scene onlayer lockgame
    $ pause(C1S1_MG_LOCK_FADE_T)

    $ c1s1_mg_lock_i += 1
    return

## Модель щеколды: шесть деталей вокруг общего центра. Позиции задаются
## центрами (anchor 0.5), поэтому детали с общего холста PSD совпадают сами,
## без знания их размеров.
##
## Порядок show и есть композиция — «бутерброд» вокруг штока (внутри слоя
## спрайты с одним zorder ложатся в порядке показа):
##
##   тень → основа корпуса → ШТОК → накладка корпуса → накладка скобы → ушко
##
## Шток лежит под накладками, поэтому виден только в их сквозных прорезях:
## уезжая вправо, он уходит под планку и выходит из ответной скобы. Ушко —
## поверх всего: по нему игрок держит щеколду и читает её состояние.
label .show_latch:

    show chapter_1_latch_shadow onlayer lockgame at c1s1_lock_part(C1S1_LATCH_SHADOW_OFF, C1S1_MG_LOCK_CENTER, C1S1_LATCH_ZOOM)
    show chapter_1_latch_body onlayer lockgame at c1s1_lock_part(C1S1_LATCH_BODY_OFF, C1S1_MG_LOCK_CENTER, C1S1_LATCH_ZOOM)
    show chapter_1_latch_stroke onlayer lockgame at c1s1_latch_rod(C1S1_LATCH_STROKE_OFF, C1S1_MG_LOCK_CENTER, C1S1_LATCH_ZOOM)
    show chapter_1_latch_overlay_body onlayer lockgame at c1s1_lock_part(C1S1_LATCH_OVERLAY_BODY_OFF, C1S1_MG_LOCK_CENTER, C1S1_LATCH_ZOOM)
    show chapter_1_latch_overlay_keeper onlayer lockgame at c1s1_lock_part(C1S1_LATCH_OVERLAY_KEEPER_OFF, C1S1_MG_LOCK_CENTER, C1S1_LATCH_ZOOM)
    show chapter_1_latch_knob onlayer lockgame at c1s1_latch_knob(C1S1_LATCH_KNOB_OFF, C1S1_MG_LOCK_CENTER, C1S1_LATCH_ZOOM)

    return

## Модель большого замка. Порядок показа — композиция:
##
##   ЯЗЫЧОК → корпус → тень щеколды → ЩЕКОЛДА → тень вертушки → ВЕРТУШКА
##
## Язычок идёт первым, ПОД корпусом: корпус цельный — и коробка, и ответная
## планка с прорезью, — и непрозрачные его места работают маской. Снаружи
## язычок виден только в этой прорези и в зазоре между планкой и коробкой;
## уезжая вправо, он выходит из планки, и оба места пустеют.
## Щеколда со своей тенью едут вместе; тень вертушки неподвижна — вертушка
## круглая, её тень от поворота не меняется.
label .show_big_lock:

    show chapter_1_big_lock_stroke onlayer lockgame at c1s1_big_stroke_slide(C1S1_BIG_STROKE_OFF, C1S1_MG_LOCK_CENTER, C1S1_BIG_LOCK_ZOOM)
    show chapter_1_big_lock_body onlayer lockgame at c1s1_lock_part(C1S1_BIG_BODY_OFF, C1S1_MG_LOCK_CENTER, C1S1_BIG_LOCK_ZOOM)
    show chapter_1_big_lock_latch_shadow onlayer lockgame at c1s1_big_latch_slide(C1S1_BIG_LATCH_SHADOW_OFF, C1S1_MG_LOCK_CENTER, C1S1_BIG_LOCK_ZOOM)
    show chapter_1_big_lock_latch onlayer lockgame at c1s1_big_latch_slide(C1S1_BIG_LATCH_OFF, C1S1_MG_LOCK_CENTER, C1S1_BIG_LOCK_ZOOM)
    show chapter_1_big_lock_spin_shadow onlayer lockgame at c1s1_lock_part(C1S1_BIG_SPIN_SHADOW_OFF, C1S1_MG_LOCK_CENTER, C1S1_BIG_LOCK_ZOOM)
    show chapter_1_big_lock_spin onlayer lockgame at c1s1_big_spinner(C1S1_BIG_SPIN_OFF, C1S1_MG_LOCK_CENTER, C1S1_BIG_LOCK_ZOOM)

    return

## Модель дверной ручки: планка и рычаг поверх неё. Последний замок — просто
## потянуть рычаг вниз до упора.
label .show_door_handle:

    show chapter_1_handle_body onlayer lockgame at c1s1_lock_part(C1S1_HANDLE_BODY_OFF, C1S1_MG_LOCK_CENTER, C1S1_HANDLE_ZOOM)
    show chapter_1_handle_lever onlayer lockgame at c1s1_handle_lever(C1S1_HANDLE_OFF, C1S1_MG_LOCK_CENTER, C1S1_HANDLE_ZOOM)

    return
