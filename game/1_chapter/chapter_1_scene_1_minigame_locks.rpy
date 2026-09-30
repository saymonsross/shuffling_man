## Мини-игра «Замки»: щеколда → большой замок → дверная ручка.
## master продолжает сцену и стук; lockgame изолирует модели от камеры и параллакса;
## screens захватывает ввод. Timer меняет default-backed модель, трансформы её читают.

## Слой мини-игры

init python:

    ## Отдельный слой изолирует модель замка от камеры master.
    if "lockgame" not in config.layers:
        renpy.add_layer("lockgame", below="screens")

## Изображения

## Детали щеколды экспортируются с общего холста; порядок show маскирует шток
## накладками. Опечатка `owerlay` сохранена в путях к исходным ассетам.
image chapter_1_latch_shadow = "images/1_chapter/lock_mini_game/latch/latch_shadow.png"
image chapter_1_latch_body = "images/1_chapter/lock_mini_game/latch/latch_body.png"
image chapter_1_latch_stroke = "images/1_chapter/lock_mini_game/latch/latch_stroke.png"
image chapter_1_latch_overlay_body = "images/1_chapter/lock_mini_game/latch/latch_body_owerlay_1.png"
image chapter_1_latch_overlay_keeper = "images/1_chapter/lock_mini_game/latch/latch_body_owerlay_2.png"
image chapter_1_latch_knob = hover_lit("images/1_chapter/lock_mini_game/latch/latch_knob.png", "c1s1_mg_part_lit('latch')", -0.08)

## У деталей большого замка разные холсты; расхождения заданы в C1S1_BIG_*_OFF.
image chapter_1_big_lock_body = "images/1_chapter/lock_mini_game/big_lock/big_lock_body.png"
image chapter_1_big_lock_stroke = "images/1_chapter/lock_mini_game/big_lock/big_lock_stroke.png"
image chapter_1_big_lock_latch_shadow = "images/1_chapter/lock_mini_game/big_lock/big_lock_latch_shadow.png"
image chapter_1_big_lock_latch = hover_lit("images/1_chapter/lock_mini_game/big_lock/big_lock_latch.png", "c1s1_mg_part_lit('big_latch')", -0.08)
image chapter_1_big_lock_spin_shadow = "images/1_chapter/lock_mini_game/big_lock/big_lock_knob_spinner_shadow.png"
## Центр обрезанной вертушки совпадает с осью вращения.
image chapter_1_big_lock_spin = hover_lit("images/1_chapter/lock_mini_game/big_lock/big_lock_knob_spinner_crop.png", "c1s1_mg_part_lit('big_spin')", -0.08)

## Рычаг ручки вращается вокруг C1S1_HANDLE_PIVOT, не центра холста.
image chapter_1_handle_body = "images/1_chapter/lock_mini_game/door_handle/door_handle_body.png"
image chapter_1_handle_lever = hover_lit("images/1_chapter/lock_mini_game/door_handle/door_handle.png", "c1s1_mg_part_lit('handle')", -0.08)

image c1s1_big_latch_arrow_img = "gui/arrow_right_128.png"

## Белые силуэты подвижных деталей под ними: рваный штрих выходит за край — обводка зацепа.
image chapter_1_latch_knob_outline = "images/1_chapter/lock_mini_game/latch/latch_knob.png"
image chapter_1_big_lock_latch_outline = "images/1_chapter/lock_mini_game/big_lock/big_lock_latch.png"
image chapter_1_big_lock_spin_outline = "images/1_chapter/lock_mini_game/big_lock/big_lock_knob_spinner_crop.png"
image chapter_1_handle_lever_outline = "images/1_chapter/lock_mini_game/door_handle/door_handle.png"

image chapter_1_mg_overlay = Solid("#0a0806")

## Игровое состояние

default c1s1_latch_open = False
default c1s1_big_lock_open = False
default c1s1_door_handle_open = False
## Чистое время управления закрытыми замками, сек.
default c1s1_locks_time = 0.0
default c1s1_locks_outcome = "fast"
default c1s1_mg_knocking = False
default c1s1_mg_active = False
default c1s1_mg_lock_i = 0
## Откатываемая модель прогресса.
default c1s1_mg_state = {}

## Новому замку нужны запись здесь, grab/step и лейбл .show_<замок>.
define C1S1_MG_LOCK_ORDER = ("latch", "big_lock", "door_handle")
define C1S1_MG_LOCK_FLAGS = {
    "latch": "c1s1_latch_open",
    "big_lock": "c1s1_big_lock_open",
    "door_handle": "c1s1_door_handle_open",
}

## Константы

## Кадр мини-игры и неподвижный фокус камеры. Камера продолжает наезд сцены (1.02 → 1.06 за
## 17 с, вход на 4-й секунде): доводит до C1S1_MG_ZOOM за оставшиеся C1S1_MG_CAMERA_T.
define C1S1_MG_ZOOM = 1.06
define C1S1_MG_CAMERA_T = 13.0
define C1S1_MG_SETTLE_T = 0.35

define C1S1_MG_OVERLAY_ALPHA = 0.72
define C1S1_MG_OVERLAY_T = 0.9

define C1S1_LOCKS_BTN_SIZE = (430, 190)
define C1S1_LOCKS_BTN_RATTLE = (18, 8)
define C1S1_LOCKS_BTN_TILT = 2.0

## Стук — серии из файла (C1S1_MG_KNOCKS), между сериями тишина; сила меняется медленной
## волной, пары значений — (тишина, пик). Толчки кадра — по ударам внутри файла.
define C1S1_MG_KNOCK_FIRST_T = 1.0          # сек до первой серии
define C1S1_MG_KNOCK_GAP = (2.4, 0.6)       # сек тишины между сериями
define C1S1_MG_KNOCK_SHAKE = (7.0, 22.0)    # px
define C1S1_MG_BAG_TREMBLE = (0.6, 4.4)     # px
define C1S1_MG_KNOCK_WAVE_T = 17.0          # сек
define C1S1_MG_KNOCK_WAVE_NOISE = 0.15      # доля
define C1S1_MG_KNOCK_GAP_NOISE = 0.35       # доля
define C1S1_MG_SHAKE_TAU = 0.16             # сек
define C1S1_MG_SHAKE_FREQ = 9.0             # Гц

define C1S1_MG_LOCK_CENTER = (960, 540)
define C1S1_MG_LOCK_FADE_T = 0.45

## Геометрия задаётся в px ассета и масштабируется вместе с моделью.
define C1S1_LATCH_ZOOM = 2.0

## Смещения нужны только слоям с обрезанным или отличающимся холстом.
define C1S1_LATCH_SHADOW_OFF = (0, 0)
define C1S1_LATCH_BODY_OFF = (0, 0)
define C1S1_LATCH_STROKE_OFF = (0, -15)
define C1S1_LATCH_OVERLAY_BODY_OFF = (0, 0)
define C1S1_LATCH_OVERLAY_KEEPER_OFF = (0, 0)
define C1S1_LATCH_KNOB_OFF = (-15, 25)

## Путь ушка: вверх → вправо → вверх. p ∈ [0, 3], целая часть — номер колена;
## векторы заданы в px ассета, отрицательный y направлен вверх.
define C1S1_LATCH_PATH = ((0, -40), (165, 0), (0, -38))

## Шток смещается только по горизонтали, ушко проходит весь путь.
define C1S1_LATCH_ROD_AXIS_ONLY = True

## Хит-зона (dx, dy, w, h) движется вместе с ушком.
define C1S1_LATCH_GRAB_BOX = (0, 0, 110, 90)

## Отладочная обводка хит-зоны.
define C1S1_MG_DEBUG_HIT = False

## Возврат к началу текущего вертикального колена, сек.
define C1S1_LATCH_RETURN_T = 0.45

## Большой замок

## big_p ∈ [0, 2]: щеколда вправо, затем вертушка против часовой.
define C1S1_BIG_LOCK_ZOOM = 1.4

## Смещения центров относительно корпуса, px ассета.
define C1S1_BIG_BODY_OFF = (0, 0)
define C1S1_BIG_STROKE_OFF = (159, 125)
define C1S1_BIG_LATCH_SHADOW_OFF = (0, 0)
define C1S1_BIG_LATCH_OFF = (0, 0)
define C1S1_BIG_SPIN_SHADOW_OFF = (0, 0)
## Смещение вертушки задаёт её ось на корпусе.
define C1S1_BIG_SPIN_OFF = (206, -15)

## Ход и зона хвата щеколды, px ассета.
define C1S1_BIG_LATCH_TRAVEL = 70
define C1S1_BIG_LATCH_GRAB_BOX = (261, 205, 300, 150)
## Стрелка-подсказка под нижней щеколдой, пока её держат: мигает, едет вместе с щеколдой.
## Смещение — px ассета от центра замка (как GRAB_BOX), zoom — доля от 128 px.
define C1S1_BIG_LATCH_ARROW_OFF = (261, 262)
define C1S1_BIG_LATCH_ARROW_ZOOM = 0.6
define C1S1_BIG_LATCH_ARROW_ALPHA = (0.25, 0.65)
define C1S1_BIG_LATCH_ARROW_BLINK_T = 0.8

define C1S1_BIG_SPIN_RADIUS = 135
define C1S1_BIG_SPIN_TURN = 540.0   # градусы: полтора оборота

## Ход язычка в корпус за полный оборот, px ассета.
define C1S1_BIG_STROKE_TRAVEL = 120

## Дверная ручка

## Рычаг тянут вниз; незавершённый ход возвращается сам.
define C1S1_HANDLE_ZOOM = 1.0

define C1S1_HANDLE_BODY_OFF = (0, 0)
define C1S1_HANDLE_OFF = (0, 0)

## Ось в px от центра холста пересчитывается в anchor по размеру холста.
define C1S1_HANDLE_CANVAS = (640, 940)
define C1S1_HANDLE_PIVOT = (-178, -105)

## Положительный rotate опускает свободный конец рычага.
define C1S1_HANDLE_TURN = 45.0

## Зона хвата задана от оси в локальных координатах рычага.
define C1S1_HANDLE_GRAB_BOX = (240, 0, 520, 180)

define C1S1_HANDLE_RETURN_T = 0.35
define C1S1_MG_DONE_HOLD_T = 0.7
define C1S1_MG_POLL_T = 0.15
define C1S1_MG_TICK_T = 1.0 / 30.0  # 30 обновлений/с
define C1S1_MG_POINTER_LOST_T = 0.25  # release вне окна: защита от вечного drag

define C1S1_MG_HOVER_SOUND = "hover"
## Белая рваная обводка подвижной детали (белый силуэт под деталью со штрихом группы
## lock_parts, Locks Tuner): слабая C1S1_MG_IDLE_OUTLINE_ALPHA, пока замок ждёт — деталь
## читается как интерактивная; полная C1S1_MG_GRAB_OUTLINE_ALPHA, пока держишь. Зацеп — щелчок.
define C1S1_MG_GRAB_SOUND = "click"
define C1S1_MG_GRAB_VOL = 0.5
define C1S1_MG_IDLE_OUTLINE_ALPHA = 0.3
define C1S1_MG_GRAB_OUTLINE_ALPHA = 1.0
define C1S1_MG_GRAB_OUTLINE_RELAX = 0.3
define C1S1_MG_BLOCKED_SOUND = "c1s1/2_lock_declaine"

## Звук мини-игры; файлы в game/audio/sfx/c1s1/.
## Серия стука: (файл, длительность, ((секунда удара, сила 0..1), ...)) — удары измерены по
## огибающей файла; серия выбирается случайно.
define C1S1_MG_KNOCKS = (
    ("c1s1/knock_door_1", 1.5, ((0.055, 0.8), (0.315, 1.0), (0.595, 0.94), (0.865, 0.89), (1.11, 0.86), (1.365, 0.71))),
    ("c1s1/knock_door_2", 1.4, ((0.095, 0.6), (0.25, 1.0), (0.455, 0.72), (0.73, 0.77), (0.985, 0.86), (1.235, 0.72))),
)
define C1S1_MG_KNOCK_VOL = (0.70, 1.0)   # тихая и громкая серия волны
define C1S1_LATCH_OPEN_SOUND = "c1s1/latch_open"
## Звук хода, пока деталь тащат: петля, громкость по скорости (доли пути детали в секунду до
## полной), гаснет через C1S1_SLIDE_HOLD_T без движения или при отпускании. Один звук на
## каждую подвижную деталь; нет файла — деталь ходит молча.
define C1S1_LATCH_SLIDE_SOUND = "c1s1/shekolda_slide"
define C1S1_LATCH_SLIDE_FULL_SPEED = 2.0
define C1S1_BIG_LATCH_SLIDE_SOUND = "c1s1/shekolda_slide"
define C1S1_BIG_LATCH_SLIDE_FULL_SPEED = 1.5
define C1S1_BIG_SPIN_SLIDE_SOUND = "c1s1/shekolda_slide"
define C1S1_BIG_SPIN_SLIDE_FULL_SPEED = 1.0
## Ручка скрипит, только пока её тянут вниз; обратный ход молчит.
define C1S1_HANDLE_SLIDE_SOUND = "c1s1/handle_squeak"
define C1S1_HANDLE_SLIDE_FULL_SPEED = 1.5
define C1S1_SLIDE_VOL = (0.25, 1.0)
define C1S1_SLIDE_HOLD_T = 0.12
define C1S1_SLIDE_FADE_T = 0.15
define C1S1_BIG_LOCK_SOUND = "c1s1/big_lock_open"
## Нижняя щеколда большого замка дошла до упора: вертушка свободна.
define C1S1_BIG_LATCH_OPEN_SOUND = "c1s1/big_lock_latch_open"
define C1S1_HANDLE_SOUND = "c1s1/handle_open"
define C1S1_MG_LOCK_VOL = 1.0
define C1S1_MG_HOVER_GAP_T = 0.15
define C1S1_MG_BLOCKED_GAP_T = 0.35
define C1S1_MG_BLOCKED_T = 1.25
define C1S1_MG_BLOCKED_SHAKE_T = 0.3
## Отказ вертушки: обводка нижней щеколды один раз вспыхивает тёмно-красным и гаснет за
## C1S1_MG_BLOCKED_BLINK_T.
define C1S1_MG_BLOCKED_BLINK_T = 0.5
define C1S1_MG_BLOCKED_BLINK_COLOR = "#8a1414"
## Щеколда при отказе еле заметно дёргается на месте: механизм упирается.
define C1S1_MG_BLOCKED_JOLT = 2.0

define C1S1_MG_FAST_T = 10.0

## Оверлей на master; модель замка живёт на отдельном lockgame.
define C1S1_Z_MG_OVERLAY = 50

init -10 python:
    scratch_params("lock_parts", "Обводка зацепленной детали замков", 3.0, 0.3, 3.0, 0.9)

## Логика

init -5 python:

    import math
    import time as sm_time

    class _C1S1ClockState(NoRollback):
        """NoRollback-состояние часов и физического pointer capture."""
        def __init__(self):
            self.context_level = None
            self.rollback_active = False
            self.tick_clock = None
            self.pointer_down = False
            self.pointer_up_since = None
            self.slide_handle = None
            self.slide_sound = None
            self.slide_idle_t = 0.0

    _c1s1_clock_state = _C1S1ClockState()

    ## Звук хода живёт вне rollback: откат и выход просто глушат его.
    def c1s1_slide(sound, full_speed, moved_p, dt):
        state = _c1s1_clock_state
        if dt <= 0.0:
            return
        if state.slide_sound != sound:
            c1s1_slide_stop()
            state.slide_sound = sound
        speed = abs(moved_p) / dt
        if speed > 0.02:
            state.slide_idle_t = 0.0
            vol = _mg_lerp(C1S1_SLIDE_VOL[0], C1S1_SLIDE_VOL[1], speed / max(0.01, full_speed))
            if state.slide_handle is None:
                if renpy.loadable("audio/sfx/" + sound + ".ogg"):
                    state.slide_handle = sfxplay(sound, loop=True, fadein=C1S1_SLIDE_FADE_T,
                        fadeout=0, tag="c1s1_slide", overlap=True, volume=vol)
            else:
                sm_audio_set_volume(state.slide_handle, vol, delay=0.05)
            return
        state.slide_idle_t += dt
        if state.slide_idle_t >= C1S1_SLIDE_HOLD_T:
            c1s1_slide_stop()

    def c1s1_slide_stop():
        state = _c1s1_clock_state
        if state.slide_handle is not None:
            sm_audio_stop(handle=state.slide_handle, fadeout=C1S1_SLIDE_FADE_T)
            state.slide_handle = None
        state.slide_sound = None
        state.slide_idle_t = 0.0

    ## В отличие от _fx_state, эта модель участвует в rollback.
    def _mg_get(name, default=0.0):
        return store.c1s1_mg_state.get(name, default)

    def _mg_set(name, value):
        store.c1s1_mg_state[name] = value
        return value

    def c1s1_mg_pointer_down():
        """True для drag и post-context release-барьера."""
        return bool(getattr(_c1s1_clock_state, "pointer_down", False))

    def c1s1_mg_physical_primary_down():
        buttons = renpy.pygame.mouse.get_pressed()
        return bool(buttons and buttons[0])

    def c1s1_mg_pointer_held():
        return c1s1_mg_pointer_down() or c1s1_mg_physical_primary_down()

    def c1s1_mg_cancel_pointer():
        c1s1_slide_stop()
        _c1s1_clock_state.pointer_down = False
        _c1s1_clock_state.pointer_up_since = None
        _mg_set("latch_grab", 0.0)
        _mg_set("big_grab", 0.0)
        _mg_set("handle_grab", 0.0)

    def c1s1_mg_anchor_clock():
        """Исключает паузы игрового меню из игрового времени."""
        _c1s1_clock_state.tick_clock = sm_time.monotonic()

    def c1s1_mg_sync_pointer_after_context():
        """Сбрасывает drag, сохраняя release-барьер при смене контекста с hold."""
        held = c1s1_mg_physical_primary_down()
        c1s1_mg_cancel_pointer()
        _c1s1_clock_state.pointer_down = held

    def c1s1_mg_recover_lost_pointer(now):
        """Снимает потерянный при focus loss capture после короткого debounce."""
        if not c1s1_mg_pointer_down() or c1s1_mg_physical_primary_down():
            _c1s1_clock_state.pointer_up_since = None
            return
        since = getattr(_c1s1_clock_state, "pointer_up_since", None)
        if since is None:
            _c1s1_clock_state.pointer_up_since = now
        elif now - since >= C1S1_MG_POINTER_LOST_T:
            c1s1_mg_cancel_pointer()

    def _mg_lerp(a, b, t):
        return a + (b - a) * max(0.0, min(1.0, t))

    def c1s1_mg_init_state():
        """Создаёт чистое состояние новой попытки."""
        store.c1s1_mg_state.clear()
        store.c1s1_mg_state.update({
            "elapsed": 0.0,
            "play_t": 0.0,
            "decision_t": 0.0,
            "hover_part": None,
            "hover_next": -1.0,
            "blocked_at": -10.0,
            "blocked_active": False,
            "wave": 0.0,
            "shake_a": 0.0,
            "shake_t": 0.0,
            "latch_p": 0.0,
            "latch_grab": 0.0,
            "latch_last_mx": 0.0,
            "latch_last_my": 0.0,
            "big_p": 0.0,
            "big_grab": 0.0,
            "big_last_mx": 0.0,
            "big_last_a": 0.0,
            "handle_p": 0.0,
            "handle_grab": 0.0,
            "handle_last_a": 0.0,
            "knock_next": -1.0,
            "knock_hits": (),
            "done": -1.0,
            "simple_target": -1.0,
        })

    def c1s1_mg_reset():
        c1s1_mg_init_state()
        for flag in C1S1_MG_LOCK_FLAGS.values():
            setattr(store, flag, False)
        store.c1s1_mg_lock_i = 0
        store.c1s1_locks_time = 0.0
        store.c1s1_locks_outcome = "fast"
        store.c1s1_mg_knocking = False
        store.c1s1_mg_active = False
        c1s1_mg_cancel_pointer()
        c1s1_mg_anchor_clock()

    def c1s1_mg_stop():
        """Обнуляет shake до остановки драйвера, чтобы кадр не застыл смещённым."""
        c1s1_slide_stop()
        _mg_set("shake_a", 0.0)
        _mg_set("shake_t", 0.0)
        c1s1_mg_clear_feedback()

    def c1s1_mg_elapsed():
        """Время реального управления ещё закрытыми замками."""
        return _mg_get("decision_t")

    def c1s1_mg_outcome_for_time(elapsed):
        if elapsed < C1S1_MG_FAST_T:
            return "fast"
        return "normal"

    def c1s1_mg_reanchor_clock():
        """Исключает menu/rollback из времени, не сбрасывая clock при restart."""
        level = renpy.context_nesting_level()
        context_changed = _c1s1_clock_state.context_level != level
        rollback_active = renpy.in_rollback()
        rollback_started = rollback_active and not _c1s1_clock_state.rollback_active
        _c1s1_clock_state.context_level = level
        _c1s1_clock_state.rollback_active = rollback_active
        ## Через смену контекста переносится только барьер до физического release.
        if ((context_changed or rollback_started)
                and (c1s1_mg_pointer_down()
                     or getattr(store, "c1s1_mg_active", False))):
            c1s1_mg_sync_pointer_after_context()
        if (getattr(store, "c1s1_mg_knocking", False)
                and (context_changed or rollback_started)):
            c1s1_mg_anchor_clock()

    if c1s1_mg_reanchor_clock not in config.interact_callbacks:
        config.interact_callbacks.append(c1s1_mg_reanchor_clock)

    ## Последовательность замков

    def c1s1_mg_lock():
        i = store.c1s1_mg_lock_i
        if 0 <= i < len(C1S1_MG_LOCK_ORDER):
            return C1S1_MG_LOCK_ORDER[i]
        return None

    def c1s1_mg_lock_open(lock=None):
        lock = lock or c1s1_mg_lock()
        if lock is None:
            return True
        return getattr(store, C1S1_MG_LOCK_FLAGS[lock], False)

    def c1s1_mg_check_done():
        if not store.c1s1_mg_active or not c1s1_mg_lock_open():
            return

        t = _mg_get("play_t")
        if _mg_get("done") < 0.0:
            _mg_set("done", t)
            return
        ## Modal-экран держится до release, исключая click-through.
        if c1s1_mg_pointer_held():
            return
        if t - _mg_get("done") >= C1S1_MG_DONE_HOLD_T:
            _mg_set("done", -1.0)
            renpy.end_interaction("done")

    ## Вздрагивание кадра

    def c1s1_mg_shake_env():
        amp = _mg_get("shake_a")
        if amp <= 0.01:
            return 0.0
        decay = math.exp(-_mg_get("shake_t") / max(0.01, C1S1_MG_SHAKE_TAU))
        return min(1.0, amp * decay / max(1.0, C1S1_MG_KNOCK_SHAKE[1]))

    def c1s1_mg_shake_offset():
        amp = _mg_get("shake_a")
        if amp <= 0.01:
            return 0.0
        t = _mg_get("shake_t")
        decay = math.exp(-t / max(0.01, C1S1_MG_SHAKE_TAU))
        return amp * decay * math.sin(2.0 * math.pi * C1S1_MG_SHAKE_FREQ * t)

    def c1s1_mg_button_rattle_f(trans, st, at):
        ## Читаем импульс двери: hover и пересборка экрана не перезапускают дребезг.
        shake = 0.0 if sm_reduced_motion() else (
            c1s1_mg_shake_offset() / max(1.0, C1S1_MG_KNOCK_SHAKE[1]))
        trans.xoffset = int(round(C1S1_LOCKS_BTN_RATTLE[0] * shake))
        trans.yoffset = int(round(-C1S1_LOCKS_BTN_RATTLE[1] * shake))
        trans.rotate = C1S1_LOCKS_BTN_TILT * shake
        return 1.0 / 60.0

    ## Драйвер

    def c1s1_mg_knock_step():
        """Косинусная волна с шумом задаёт паузу и силу следующей серии; толчки кадра идут
        по ударам внутри файла (knock_hits — очередь (секунда, сила))."""
        t = _mg_get("elapsed")
        hits = _mg_get("knock_hits", ())
        while hits and hits[0][0] <= t:
            _mg_set("shake_a", hits[0][1])
            _mg_set("shake_t", 0.0)
            hits = hits[1:]
            _mg_set("knock_hits", hits)

        nxt = _mg_get("knock_next")
        if nxt < 0.0:
            _mg_set("knock_next", t + C1S1_MG_KNOCK_FIRST_T)
            return
        if t < nxt:
            return

        wave = 0.5 - 0.5 * math.cos(2.0 * math.pi * t / max(1.0, C1S1_MG_KNOCK_WAVE_T))
        wave += renpy.random.uniform(-C1S1_MG_KNOCK_WAVE_NOISE, C1S1_MG_KNOCK_WAVE_NOISE)
        wave = max(0.0, min(1.0, wave))
        _mg_set("wave", wave)

        name, length, onsets = renpy.random.choice(C1S1_MG_KNOCKS)
        gap = _mg_lerp(C1S1_MG_KNOCK_GAP[0], C1S1_MG_KNOCK_GAP[1], wave)
        gap *= 1.0 + renpy.random.uniform(-C1S1_MG_KNOCK_GAP_NOISE, C1S1_MG_KNOCK_GAP_NOISE)
        _mg_set("knock_next", t + length + max(0.15, gap))

        c1s1_knock(name, "door", _mg_lerp(C1S1_MG_KNOCK_VOL[0], C1S1_MG_KNOCK_VOL[1], wave))
        amp = _mg_lerp(C1S1_MG_KNOCK_SHAKE[0], C1S1_MG_KNOCK_SHAKE[1], wave)
        _mg_set("knock_hits", tuple((t + at, amp * rel) for at, rel in onsets))

    def c1s1_mg_tick():
        """Timer-драйвер модели: сайд-эффекты только в interaction, dt ограничен."""
        ## После game menu parent-interaction продолжается без нового callback.
        c1s1_mg_reanchor_clock()
        now = sm_time.monotonic()
        c1s1_mg_recover_lost_pointer(now)
        previous = getattr(_c1s1_clock_state, "tick_clock", None)
        dt = 0.0 if previous is None else now - previous
        if dt < 0.0:
            dt = 0.0
        else:
            dt = min(dt, 0.25)
        _c1s1_clock_state.tick_clock = now
        _mg_set("shake_t", _mg_get("shake_t") + dt)

        if store.c1s1_mg_knocking:
            _mg_set("elapsed", _mg_get("elapsed") + dt)
            c1s1_mg_knock_step()

        if store.c1s1_mg_active:
            _mg_set("play_t", _mg_get("play_t") + dt)
            if not c1s1_mg_lock_open():
                _mg_set("decision_t", _mg_get("decision_t") + dt)
            if not c1s1_mg_simplified_tick(dt):
                lock = c1s1_mg_lock()
                if lock == "latch":
                    c1s1_latch_step(dt)
                elif lock == "big_lock":
                    c1s1_big_step(dt)
                elif lock == "door_handle":
                    c1s1_handle_step(dt)
            c1s1_mg_update_hover()

    ## Камера

    def c1s1_mg_camera_f(key, trans, st, at):
        """Держит фокус на замках и сводит shake в общие _fx_state-ключи камеры двери."""
        if renpy.predicting():
            return 1.0 / 60.0
        bx, by = _focus_offset(C1S1_LOCKS_FOCUS, None, trans.zoom or 1.0)
        if sm_reduced_motion():
            for suffix in ("_jx", "_jy"):
                _fx_state[key + suffix] = 0.0
            trans.xoffset = bx
            trans.yoffset = by
            _fx_publish_camera(key, trans)
            return 1.0 / 60.0

        sy = c1s1_mg_shake_offset()
        _fx_state[key + "_jx"] = 0.0
        _fx_state[key + "_jy"] = sy

        trans.xoffset = bx
        trans.yoffset = by + sy
        _fx_publish_camera(key, trans)
        return 1.0 / 60.0

    ## Модель замка

    def c1s1_lock_pos(center_xy, off_xy, z):
        """Экранный центр: offset масштабируется; pos должен быть int, не долей."""
        return (int(round(center_xy[0] + off_xy[0] * z)),
                int(round(center_xy[1] + off_xy[1] * z)))

    ## Щеколда

    def c1s1_latch_max_p():
        """Вычисляется поздно: C1S1_LATCH_PATH ещё не задан при init блока."""
        return float(len(C1S1_LATCH_PATH))

    def c1s1_latch_offset(p):
        """Интерполирует путь в asset-px и масштабирует в экранные px."""
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
        """Движущаяся hit-зона ушка в экранных координатах, вне камеры."""
        cx, cy, bw, bh = c1s1_latch_hit_rect()
        return abs(mx - cx) <= bw * 0.5 and abs(my - cy) <= bh * 0.5

    def c1s1_latch_hit_rect():
        """Общая hit-зона для ввода и debug overlay: экранные cx, cy, w, h."""
        z = C1S1_LATCH_ZOOM
        dx, dy, bw, bh = C1S1_LATCH_GRAB_BOX
        ox, oy = c1s1_latch_offset(_mg_get("latch_p"))
        return (C1S1_MG_LOCK_CENTER[0] + (dx + C1S1_LATCH_KNOB_OFF[0]) * z + ox,
                C1S1_MG_LOCK_CENTER[1] + (dy + C1S1_LATCH_KNOB_OFF[1]) * z + oy,
                bw * z, bh * z)

    def c1s1_latch_hit_pos():
        cx, cy, bw, bh = c1s1_latch_hit_rect()
        return (int(round(cx - bw * 0.5)), int(round(cy - bh * 0.5)))

    def c1s1_latch_hit_size():
        cx, cy, bw, bh = c1s1_latch_hit_rect()
        return (int(round(bw)), int(round(bh)))

    def c1s1_latch_grab():
        mx, my = renpy.get_mouse_pos()
        if not c1s1_latch_hit(mx, my):
            return
        _mg_set("latch_grab", 1.0)
        _mg_set("latch_last_mx", mx)
        _mg_set("latch_last_my", my)

    def c1s1_latch_step(dt):
        """Проецирует drag на текущее колено; незавершённая вертикаль откатывается."""
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

            seg = int(min(p, max_p - 0.001))
            vx, vy = C1S1_LATCH_PATH[seg]
            ## На повороте можно продолжить вперёд или вернуться по прежнему колену.
            if p == float(seg) and seg > 0 and dx * vx + dy * vy <= 0.0:
                prev_vx, prev_vy = C1S1_LATCH_PATH[seg - 1]
                if dx * prev_vx + dy * prev_vy < 0.0:
                    seg -= 1
                    vx, vy = prev_vx, prev_vy
            span2 = (vx * vx + vy * vy) * C1S1_LATCH_ZOOM * C1S1_LATCH_ZOOM
            if span2 > 1.0:
                ## Проекция движения мыши на ось колена.
                p += (dx * vx + dy * vy) * C1S1_LATCH_ZOOM / span2
            ## Избыток одного движения не переносится через поворот траектории.
            p = max(float(seg), min(float(seg + 1), p))
            c1s1_slide(C1S1_LATCH_SLIDE_SOUND, C1S1_LATCH_SLIDE_FULL_SPEED, p - _mg_get("latch_p"), dt)
            _mg_set("latch_p", p)

            if p >= max_p:
                c1s1_slide_stop()
                sm_sfx(C1S1_LATCH_OPEN_SOUND, volume=C1S1_MG_LOCK_VOL)
                _mg_set("latch_grab", 0.0)
                store.c1s1_latch_open = True
            return

        ## Вертикальные колена возвращаются; горизонтальный канал держит засов.
        seg = int(min(p, max_p - 0.001))
        if C1S1_LATCH_PATH[seg][1] == 0:
            return
        target = float(int(p))
        _mg_set("latch_p", max(target, p - dt / max(0.05, C1S1_LATCH_RETURN_T)))

    def c1s1_latch_rod_f(trans, st, at):
        """Шток следует оси x; вертикаль пути визуализирует поворот ушка."""
        ox, oy = c1s1_latch_offset(_mg_get("latch_p"))
        trans.xoffset = ox
        trans.yoffset = 0.0 if C1S1_LATCH_ROD_AXIS_ONLY else oy
        return 1.0 / 60.0

    def c1s1_latch_knob_f(trans, st, at):
        ox, oy = c1s1_latch_offset(_mg_get("latch_p"))
        trans.xoffset = ox
        trans.yoffset = oy
        return 1.0 / 60.0

    ## Большой замок

    def c1s1_big_spin_center():
        """Ось вертушки — центр обрезанного по силуэту ассета в экранных px."""
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
        cx, cy = c1s1_big_spin_center()
        r = C1S1_BIG_SPIN_RADIUS * C1S1_BIG_LOCK_ZOOM
        return (mx - cx) ** 2 + (my - cy) ** 2 <= r * r

    def c1s1_big_grab():
        """Вертушка захватывается только после полного сдвига щеколды."""
        mx, my = renpy.get_mouse_pos()
        if _mg_get("big_p") < 1.0:
            if c1s1_big_latch_hit(mx, my):
                _mg_set("big_grab", 1.0)
                _mg_set("big_last_mx", mx)
            elif c1s1_big_spin_hit(mx, my):
                c1s1_mg_blocked_feedback()
            return
        if c1s1_big_spin_hit(mx, my):
            _mg_set("big_grab", 2.0)
            _mg_set("big_last_a", c1s1_big_spin_angle(mx, my))

    def c1s1_big_step(dt):
        """Линейный drag, затем угол против часовой; прогресс не откатывается."""
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
            if p >= 1.0 and _mg_get("big_p") < 1.0:
                c1s1_slide_stop()
                sm_sfx(C1S1_BIG_LATCH_OPEN_SOUND, volume=C1S1_MG_LOCK_VOL)
        else:
            ## При экранной оси y вниз против часовой соответствует убыванию atan2.
            a = c1s1_big_spin_angle(mx, my)
            da = a - _mg_get("big_last_a")
            while da > 180.0:
                da -= 360.0
            while da < -180.0:
                da += 360.0
            _mg_set("big_last_a", a)
            p += -da / max(1.0, C1S1_BIG_SPIN_TURN)
            p = max(1.0, min(2.0, p))

        if _mg_get("big_grab") < 1.5:
            c1s1_slide(C1S1_BIG_LATCH_SLIDE_SOUND, C1S1_BIG_LATCH_SLIDE_FULL_SPEED, p - _mg_get("big_p"), dt)
        else:
            c1s1_slide(C1S1_BIG_SPIN_SLIDE_SOUND, C1S1_BIG_SPIN_SLIDE_FULL_SPEED, p - _mg_get("big_p"), dt)
        _mg_set("big_p", p)
        if p >= 2.0:
            c1s1_slide_stop()
            sm_sfx(C1S1_BIG_LOCK_SOUND, volume=C1S1_MG_LOCK_VOL)
            _mg_set("big_grab", 0.0)
            store.c1s1_big_lock_open = True

    def c1s1_big_turn():
        return max(0.0, min(1.0, _mg_get("big_p") - 1.0))

    def c1s1_big_latch_x():
        """Сдвиг нижней щеколды по ходу плюс дрожь отказа."""
        x = C1S1_BIG_LATCH_TRAVEL * C1S1_BIG_LOCK_ZOOM * min(1.0, _mg_get("big_p"))
        if not sm_reduced_motion():
            age = _mg_get("play_t") - _mg_get("blocked_at", -10.0)
            if _mg_get("big_p") < 1.0 and 0.0 <= age < C1S1_MG_BLOCKED_BLINK_T:
                fade = 1.0 - age / C1S1_MG_BLOCKED_BLINK_T
                x += C1S1_MG_BLOCKED_JOLT * fade * math.sin(age * math.pi * 24.0)
        return x

    def c1s1_big_latch_f(trans, st, at):
        trans.xoffset = c1s1_big_latch_x()
        return 1.0 / 60.0

    def c1s1_big_latch_arrow_f(trans, st, at):
        trans.xoffset = c1s1_big_latch_x()
        lo, hi = C1S1_BIG_LATCH_ARROW_ALPHA
        if not c1s1_mg_part_grabbed("big_latch") or _mg_get("big_p") >= 1.0:
            level = 0.0
        elif sm_reduced_motion():
            level = (lo + hi) / 2.0
        else:
            phase = _fx_frame_time() / max(0.05, C1S1_BIG_LATCH_ARROW_BLINK_T)
            level = lo + (hi - lo) * (0.5 + 0.5 * math.sin(2.0 * math.pi * phase))
        trans.alpha = _fx_step("c1s1_big_latch_arrow", level, 0.35, 0.0)
        return 1.0 / 60.0

    def c1s1_big_stroke_f(trans, st, at):
        trans.xoffset = C1S1_BIG_STROKE_TRAVEL * C1S1_BIG_LOCK_ZOOM * c1s1_big_turn()
        return 1.0 / 60.0

    def c1s1_big_spin_f(trans, st, at):
        trans.rotate = -C1S1_BIG_SPIN_TURN * c1s1_big_turn()
        age = _mg_get("play_t") - _mg_get("blocked_at", -10.0)
        if c1s1_mg_blocked_visible() and not sm_reduced_motion() and age < C1S1_MG_BLOCKED_SHAKE_T:
            fade = 1.0 - age / C1S1_MG_BLOCKED_SHAKE_T
            trans.rotate += 3.0 * math.sin(age * math.pi * 20.0) * fade
        return 1.0 / 60.0

    ## Дверная ручка

    def c1s1_handle_anchor():
        """Переводит pivot из px от центра общего холста в долю anchor."""
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
        """Проверяет рычаг локально, компенсируя его текущий поворот."""
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
        """Накапливает угол drag вокруг pivot; незавершённый рычаг возвращается."""
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
            c1s1_slide(C1S1_HANDLE_SLIDE_SOUND, C1S1_HANDLE_SLIDE_FULL_SPEED, max(0.0, p - _mg_get("handle_p")), dt)
            _mg_set("handle_p", p)
            if p >= 1.0:
                c1s1_slide_stop()
                sm_sfx(C1S1_HANDLE_SOUND, volume=C1S1_MG_LOCK_VOL)
                _mg_set("handle_grab", 0.0)
                store.c1s1_door_handle_open = True
            return

        _mg_set("handle_p", max(0.0, p - dt / max(0.05, C1S1_HANDLE_RETURN_T)))

    def c1s1_handle_f(trans, st, at):
        trans.rotate = C1S1_HANDLE_TURN * _mg_get("handle_p")
        return 1.0 / 60.0

    ## Ввод

    def c1s1_mg_hover_target(mx, my):
        """Hover и grab используют одну геометрию, включая движущиеся детали."""
        if not store.c1s1_mg_active or c1s1_mg_lock_open():
            return None
        lock = c1s1_mg_lock()
        if lock == "latch" and c1s1_latch_hit(mx, my):
            return "latch"
        if lock == "big_lock":
            if _mg_get("big_p") < 1.0 and c1s1_big_latch_hit(mx, my):
                return "big_latch"
            if c1s1_big_spin_hit(mx, my):
                return "big_spin"
        if lock == "door_handle" and c1s1_handle_hit(mx, my):
            return "handle"
        return None

    def c1s1_mg_blocked_visible():
        age = _mg_get("play_t") - _mg_get("blocked_at", -10.0)
        return (store.c1s1_mg_active and c1s1_mg_lock() == "big_lock"
                and _mg_get("big_p") < 1.0 and 0.0 <= age < C1S1_MG_BLOCKED_T)

    def c1s1_mg_part_lit(part):
        return (store.c1s1_mg_active
                and (_mg_get("hover_part", None) == part
                     or (part == "big_latch" and c1s1_mg_blocked_visible())))

    def c1s1_mg_update_hover():
        target = (c1s1_mg_hover_target(*renpy.get_mouse_pos())
                  if renpy.game.interface.mouse_focused else None)
        changed = target != _mg_get("hover_part", None)
        if changed:
            _mg_set("hover_part", target)
            now = _mg_get("play_t")
            if target is not None and now >= _mg_get("hover_next", -1.0) and not c1s1_mg_pointer_down():
                _mg_set("hover_next", now + C1S1_MG_HOVER_GAP_T)
                splay(C1S1_MG_HOVER_SOUND, ext="ogg")
        blocked = c1s1_mg_blocked_visible()
        changed = changed or blocked != _mg_get("blocked_active", False)
        _mg_set("blocked_active", blocked)
        if changed:
            ## ConditionSwitch и подсказка обновляются только на границах состояния.
            renpy.restart_interaction()

    def c1s1_mg_blocked_feedback():
        now = _mg_get("play_t")
        if now - _mg_get("blocked_at", -10.0) < C1S1_MG_BLOCKED_GAP_T:
            return
        _mg_set("blocked_at", now)
        _mg_set("blocked_active", True)
        splay(C1S1_MG_BLOCKED_SOUND, ext="ogg")
        renpy.restart_interaction()

    def c1s1_mg_clear_feedback():
        _mg_set("hover_part", None)
        _mg_set("blocked_at", -10.0)
        _mg_set("blocked_active", False)

    def c1s1_mg_grab():
        c1s1_mg_cancel_pointer()
        if not store.c1s1_mg_active or c1s1_mg_lock_open():
            return
        lock = c1s1_mg_lock()
        if lock == "latch":
            c1s1_latch_grab()
        elif lock == "big_lock":
            c1s1_big_grab()
        elif lock == "door_handle":
            c1s1_handle_grab()

        ## Release захватывается только после grab детали, не клика по UI.
        _c1s1_clock_state.pointer_down = (
            _mg_get("latch_grab") > 0.5
            or _mg_get("big_grab") > 0.5
            or _mg_get("handle_grab") > 0.5)
        if _c1s1_clock_state.pointer_down:
            sm_sfx(C1S1_MG_GRAB_SOUND, volume=C1S1_MG_GRAB_VOL)

    def c1s1_mg_part_grabbed(part):
        if part == "latch":
            return _mg_get("latch_grab") > 0.5
        if part == "big_latch":
            return abs(_mg_get("big_grab") - 1.0) < 0.01
        if part == "big_spin":
            return abs(_mg_get("big_grab") - 2.0) < 0.01
        return _mg_get("handle_grab") > 0.5

    def c1s1_mg_part_actionable(part):
        """Деталь, которую сейчас можно двигать: у большого замка сначала щеколда, потом вертушка."""
        if part == "big_latch":
            return _mg_get("big_p") < 1.0
        if part == "big_spin":
            return _mg_get("big_p") >= 1.0
        return True

    def c1s1_mg_blocked_blink():
        """Доля красного в обводке нижней щеколды после отказа вертушки: мигает и гаснет."""
        age = _mg_get("play_t") - _mg_get("blocked_at", -10.0)
        if not (c1s1_mg_lock() == "big_lock" and _mg_get("big_p") < 1.0 and 0.0 <= age < C1S1_MG_BLOCKED_BLINK_T):
            return 0.0
        return 1.0 - age / C1S1_MG_BLOCKED_BLINK_T

    def c1s1_mg_grab_outline_f(part, trans, st, at):
        blink = c1s1_mg_blocked_blink() if part == "big_latch" else 0.0
        if c1s1_mg_part_grabbed(part):
            target = C1S1_MG_GRAB_OUTLINE_ALPHA
        elif store.c1s1_mg_active and not c1s1_mg_lock_open() and c1s1_mg_part_actionable(part):
            target = C1S1_MG_IDLE_OUTLINE_ALPHA
        else:
            target = 0.0
        alpha = _fx_step("c1s1_mg_outline_" + part, target, C1S1_MG_GRAB_OUTLINE_RELAX, 0.0)
        trans.alpha = max(alpha, blink)
        trans.u_scratch_hover = blink
        return 1.0 / 60.0

    def c1s1_mg_release():
        ## Щелчок только когда деталь действительно отпускают, не на клик по пустому месту;
        ## если этим движением замок открылся, звучит только его звук открытия.
        if c1s1_mg_pointer_down() and not c1s1_mg_lock_open():
            sm_sfx(C1S1_MG_GRAB_SOUND, volume=C1S1_MG_GRAB_VOL)
        c1s1_mg_cancel_pointer()

    def c1s1_mg_capture_release():
        """Поглощает mouseup только после drag, предотвращая click-through."""
        if not c1s1_mg_pointer_down():
            return
        c1s1_mg_release()
        raise renpy.display.core.IgnoreEvent()

    def c1s1_mg_simplified_label():
        """Self-voicing-подпись следующего шага без drag."""
        if c1s1_mg_lock_open():
            return _("Замок открыт")
        if _mg_get("simple_target", -1.0) >= 0.0:
            return _("Выполняется…")
        lock = c1s1_mg_lock()
        if lock == "latch":
            p = _mg_get("latch_p")
            if p < 1.0:
                return _("Поднять щеколду")
            if p < 2.0:
                return _("Сдвинуть щеколду вправо")
            return _("Поднять щеколду ещё раз")
        if lock == "big_lock":
            if _mg_get("big_p") < 1.0:
                return _("Сдвинуть засов вправо")
            return _("Повернуть вертушку против часовой")
        if lock == "door_handle":
            return _("Опустить ручку")
        return _("Замок открыт")

    def c1s1_mg_simplified_step():
        """Запускает focusable-шаг; при reduced motion завершает синхронно."""
        if (not store.c1s1_mg_active
                or c1s1_mg_lock_open()
                or _mg_get("simple_target", -1.0) >= 0.0):
            return
        c1s1_mg_release()
        lock = c1s1_mg_lock()
        if lock == "latch":
            p = _mg_get("latch_p")
            target = 1.0 if p < 1.0 else (2.0 if p < 2.0 else c1s1_latch_max_p())
        elif lock == "big_lock":
            target = 1.0 if _mg_get("big_p") < 1.0 else 2.0
        elif lock == "door_handle":
            target = 1.0
        else:
            return
        _mg_set("simple_target", target)
        if sm_reduced_motion():
            c1s1_mg_simplified_tick(1.0)

    def c1s1_mg_simplified_tick(dt):
        target = _mg_get("simple_target", -1.0)
        if target < 0.0:
            return False

        lock = c1s1_mg_lock()
        if lock == "latch":
            key, limit, speed, sound = "latch_p", c1s1_latch_max_p(), 3.5, C1S1_LATCH_OPEN_SOUND
        elif lock == "big_lock":
            key, limit, speed, sound = "big_p", 2.0, 2.5, C1S1_BIG_LOCK_SOUND
        elif lock == "door_handle":
            key, limit, speed, sound = "handle_p", 1.0, 2.5, C1S1_HANDLE_SOUND
        else:
            _mg_set("simple_target", -1.0)
            return False

        p = min(target, _mg_get(key) + dt * speed)
        _mg_set(key, p)
        if p + 0.0001 < target:
            return True

        _mg_set("simple_target", -1.0)
        ## Упрощённый режим открывает замок тем же звуком, что и drag.
        if p + 0.0001 >= limit:
            sm_sfx(sound, volume=C1S1_MG_LOCK_VOL)
            setattr(store, C1S1_MG_LOCK_FLAGS[lock], True)
        elif lock == "big_lock" and p + 0.0001 >= 1.0:
            sm_sfx(C1S1_BIG_LATCH_OPEN_SOUND, volume=C1S1_MG_LOCK_VOL)
        return True

    def c1s1_mg_open_all():
        c1s1_mg_release()
        _mg_set("latch_p", c1s1_latch_max_p())
        _mg_set("big_p", 2.0)
        _mg_set("handle_p", 1.0)
        _mg_set("simple_target", -1.0)
        for flag in C1S1_MG_LOCK_FLAGS.values():
            setattr(store, flag, True)
        store.c1s1_mg_lock_i = len(C1S1_MG_LOCK_ORDER)

    ## Сумка

    def c1s1_mg_bag_f(trans, st, at):
        if renpy.predicting():
            return 1.0 / 60.0
        if sm_reduced_motion():
            _fx_state["c1s1_mg_bag_jx"] = 0.0
            _fx_state["c1s1_mg_bag_jy"] = 0.0
            trans.xoffset = 0.0
            trans.yoffset = 0.0
            return 1.0 / 60.0

        amp = _mg_lerp(C1S1_MG_BAG_TREMBLE[0], C1S1_MG_BAG_TREMBLE[1],
                       c1s1_mg_shake_env())
        trans.xoffset = _fx_step("c1s1_mg_bag_jx", lambda: _fx_visual_jitter(amp), 0.5, start=0.0)
        trans.yoffset = _fx_step("c1s1_mg_bag_jy", lambda: _fx_visual_jitter(amp), 0.5, start=0.0)
        return 1.0 / 60.0

## Трансформы

## Белый силуэт под деталью: штрих (tint 1 — белый) рвёт край наружу, alpha растёт, пока держат.
## hover-цвет штриха занят под мигание отказа: u_scratch_hover ведёт c1s1_mg_grab_outline_f.
transform c1s1_mg_grab_outline(part):
    alpha 0.0
    parallel:
        scratch("lock_parts", tint=1.0, idle_color="#ffffff", hover_color=C1S1_MG_BLOCKED_BLINK_COLOR, pad=24)
    parallel:
        function renpy.curry(c1s1_mg_grab_outline_f)(part)

transform c1s1_mg_button_rattle():
    subpixel True
    transform_anchor True
    align (0.5, 0.5)
    function c1s1_mg_button_rattle_f

## Начальный zoom наследуется для плавной склейки; rotate сбрасывается явно.
transform c1s1_mg_camera(z1=C1S1_MG_ZOOM, t=C1S1_MG_CAMERA_T, key="cam"):
    subpixel True
    align (0.5, 0.5)
    rotate 0.0
    parallel:
        ease sm_motion_time(t) zoom z1
    parallel:
        function renpy.curry(c1s1_mg_camera_f)(key)

transform c1s1_mg_overlay_in(a=C1S1_MG_OVERLAY_ALPHA, t=C1S1_MG_OVERLAY_T):
    align (0.5, 0.5)
    alpha 0.0
    ease t alpha a

transform c1s1_mg_overlay_out(a=C1S1_MG_OVERLAY_ALPHA, t=C1S1_MG_OVERLAY_T):
    align (0.5, 0.5)
    alpha a
    ease t alpha 0.0

transform c1s1_lock_part(off_xy, center_xy, z):
    subpixel True
    anchor (0.5, 0.5)
    zoom z
    pos c1s1_lock_pos(center_xy, off_xy, z)

transform c1s1_latch_rod(off_xy, center_xy, z):
    subpixel True
    anchor (0.5, 0.5)
    zoom z
    pos c1s1_lock_pos(center_xy, off_xy, z)
    xoffset 0.0 yoffset 0.0
    function c1s1_latch_rod_f

transform c1s1_latch_knob(off_xy, center_xy, z):
    subpixel True
    anchor (0.5, 0.5)
    zoom z
    pos c1s1_lock_pos(center_xy, off_xy, z)
    xoffset 0.0 yoffset 0.0
    function c1s1_latch_knob_f

transform c1s1_big_latch_arrow(off_xy, center_xy, z):
    subpixel True
    anchor (0.5, 0.0)
    zoom C1S1_BIG_LATCH_ARROW_ZOOM
    pos c1s1_lock_pos(center_xy, off_xy, z)
    xoffset 0.0
    alpha 0.0
    function c1s1_big_latch_arrow_f

transform c1s1_big_latch_slide(off_xy, center_xy, z):
    subpixel True
    anchor (0.5, 0.5)
    zoom z
    pos c1s1_lock_pos(center_xy, off_xy, z)
    xoffset 0.0
    function c1s1_big_latch_f

transform c1s1_big_stroke_slide(off_xy, center_xy, z):
    subpixel True
    anchor (0.5, 0.5)
    zoom z
    pos c1s1_lock_pos(center_xy, off_xy, z)
    xoffset 0.0
    function c1s1_big_stroke_f

## transform_anchor удерживает ось обрезанной вертушки при rotate_pad.
transform c1s1_big_spinner(off_xy, center_xy, z):
    subpixel True
    transform_anchor True
    anchor (0.5, 0.5)
    zoom z
    pos c1s1_lock_pos(center_xy, off_xy, z)
    rotate 0.0
    function c1s1_big_spin_f

## Якорь рычага переносится в ось, а позиция компенсирует тот же сдвиг.
transform c1s1_handle_lever(off_xy, center_xy, z):
    subpixel True
    transform_anchor True
    anchor c1s1_handle_anchor()
    zoom z
    pos c1s1_lock_pos(center_xy, (off_xy[0] + C1S1_HANDLE_PIVOT[0], off_xy[1] + C1S1_HANDLE_PIVOT[1]), z)
    rotate 0.0
    function c1s1_handle_f

transform c1s1_mg_bag(pos_xy, anchor_xy):
    subpixel True
    anchor anchor_xy
    pos pos_xy
    xoffset 0.0 yoffset 0.0
    parallel:
        function c1s1_mg_bag_f
    parallel:
        brightness_to(-0.04, 3.0)
        block:
            ease 6.0 u_breath_brightness -0.08
            ease 6.0 u_breath_brightness -0.04
            repeat

## Экраны

## Timer меняет модель на всём протяжении эпизода.
screen c1s1_mg_runtime():
    ## Под modal-меню таймер останавливается.
    timer C1S1_MG_TICK_T action Function(c1s1_mg_tick, _update_screens=False) repeat True modal True

## Кнопка в стиле сценовых (glow_button с разломом); центр и хит-зона неподвижны, от стука
## дребезжит только текст со свечением.
screen c1s1_locks_open_door():
    ## Выше quick_menu: интерактив остаётся modal.
    zorder 110
    modal True
    timer C1S1_MG_TICK_T action Function(c1s1_mg_tick, _update_screens=False) repeat True modal True
    fixed:
        id "door_prompt"
        at show_hide(0.5)
        xysize (config.screen_width, config.screen_height)
        use glow_button(
            _("МАРИНА, ОТКРЫВАЙ ДВЕРЬ!"),
            Return("done"),
            bg="dark",
            pos=(960, 540),
            size=C1S1_LOCKS_BTN_SIZE,
            visual_at=c1s1_mg_button_rattle(),
            rift="screen")

## Drag для мыши и focusable-альтернатива для клавиатуры, touch и self-voicing.
screen c1s1_locks_minigame():
    zorder 110
    modal True

    on "hide" action [Function(c1s1_mg_release, _update_screens=False), Function(c1s1_mg_clear_feedback, _update_screens=False)]

    timer C1S1_MG_TICK_T action Function(c1s1_mg_tick, _update_screens=False) repeat True modal True
    timer C1S1_MG_POLL_T action Function(c1s1_mg_check_done) repeat True modal True

    ## Реплики Вити за дверью: по одной на замок, в порядке C1S1_MG_LOCK_ORDER.
    use c1s1_vitya_bark((_("Марина, открывай!"), _("Опять заперлась? Я ж на минуту выскочил!"), _("Боже, что ты там возишься?"), _("Марина, ну давай быстрее! Замок сломался?")), side="up", pos=(1444, 13), index=(lambda: c1s1_mg_lock_i))

    if c1s1_mg_blocked_visible():
        frame:
            xalign 0.5
            yalign 0.985
            padding (28, 14)
            at show_hide(0.3)
            text _("Сначала сдвиньте нижнюю щеколду вправо."):
                id "c1s1_mg_blocked_hint"
                style "c1s1_mg_step_button_text"
                color "#dad4ca"
                at scratch("show_text", tint=0.0, mix=0.09)

    if persistent.sm_simplified_locks:
        textbutton c1s1_mg_simplified_label():
            style "c1s1_mg_step_button"
            action [SPlay("click"), Function(c1s1_mg_simplified_step)]
            hovered SPlay(C1S1_MG_HOVER_SOUND, ext="ogg")
            default_focus True
            xalign 0.5
            yalign 0.90

    if C1S1_MG_DEBUG_HIT and c1s1_mg_lock() == "latch":
        add Solid("#00ff0040"):
            pos c1s1_latch_hit_pos()
            xysize c1s1_latch_hit_size()

    ## MultiBox обходит события с конца: key перехватывают drag-release раньше UI.
    ## capture False пропускает обычные клики.
    key "mousedown_1" action Function(c1s1_mg_grab, _update_screens=False) capture False
    key "mouseup_1" action Function(c1s1_mg_capture_release, _update_screens=False) capture False

style c1s1_mg_access_button is button:
    background "ui_frame_bg"
    hover_background "ui_frame_bg_solid"
    insensitive_background "ui_frame_bg"
    padding (22, 12)

style c1s1_mg_access_button_text is button_text:
    font gui.main_menu_font
    color "#dad4ca"
    hover_color "#ffffff"
    insensitive_color "#8a8784"
    outlines [(2, "#1a1712d9", 0, 0)]
    size 25

style c1s1_mg_step_button is c1s1_mg_access_button:
    padding (30, 16)

style c1s1_mg_step_button_text is c1s1_mg_access_button_text:
    size 30

## Сцена

label chapter_1_scene_1_minigame_locks:

    ## Камера доводит наезд; кнопка остаётся в центре экрана.
    camera at c1s1_mg_camera()

    ## Runtime стартует до кнопки, чтобы стук не прерывался.
    $ c1s1_mg_reset()
    show screen c1s1_mg_runtime
    show chapter_1_hall_door_bag zorder C1S1_Z_DOOR_BAG at c1s1_mg_bag(C1S1_DOOR_BAG_POS, C1S1_DOOR_BAG_ANCHOR)
    $ c1s1_mg_knocking = True

    $ pause(C1S1_MG_SETTLE_T)

    ## Временной исход делает интерактив обязательным даже при пропуске текста.
    $ skip_stop()
    call screen c1s1_locks_open_door

    ## Оверлей отделяет сцену двери от моделей замков.
    show chapter_1_mg_overlay zorder C1S1_Z_MG_OVERLAY at c1s1_mg_overlay_in()
    $ pause(C1S1_MG_OVERLAY_T)

    ## Замки открываются по C1S1_MG_LOCK_ORDER без остановки часов и стука.
    $ c1s1_mg_lock_i = 0
    while c1s1_mg_lock() is not None:
        call .play_lock from _call_c1s1_mg_play_lock

    $ c1s1_locks_time = c1s1_mg_elapsed()
    $ c1s1_locks_outcome = c1s1_mg_outcome_for_time(c1s1_locks_time)

    ## Возврат к сцене.
    $ c1s1_mg_knocking = False
    show chapter_1_mg_overlay zorder C1S1_Z_MG_OVERLAY at c1s1_mg_overlay_out()
    $ pause(C1S1_MG_OVERLAY_T)
    hide chapter_1_mg_overlay

    ## Runtime снимается после сброса вздрагивания.
    $ c1s1_mg_stop()
    hide screen c1s1_mg_runtime

    return

## Переходы ограничены слоем lockgame, чтобы master не мигал.
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
    $ c1s1_mg_clear_feedback()

    $ renpy.transition(Dissolve(C1S1_MG_LOCK_FADE_T), layer="lockgame")
    scene onlayer lockgame
    $ pause(C1S1_MG_LOCK_FADE_T)

    $ c1s1_mg_lock_i = min(c1s1_mg_lock_i + 1, len(C1S1_MG_LOCK_ORDER))
    return

## Порядок show маскирует шток деталями с общего холста:
##   тень → основа корпуса → ШТОК → накладка корпуса → накладка скобы → ушко
label .show_latch:

    show chapter_1_latch_shadow onlayer lockgame at c1s1_lock_part(C1S1_LATCH_SHADOW_OFF, C1S1_MG_LOCK_CENTER, C1S1_LATCH_ZOOM)
    show chapter_1_latch_body onlayer lockgame at c1s1_lock_part(C1S1_LATCH_BODY_OFF, C1S1_MG_LOCK_CENTER, C1S1_LATCH_ZOOM)
    show chapter_1_latch_stroke onlayer lockgame at c1s1_latch_rod(C1S1_LATCH_STROKE_OFF, C1S1_MG_LOCK_CENTER, C1S1_LATCH_ZOOM)
    show chapter_1_latch_overlay_body onlayer lockgame at c1s1_lock_part(C1S1_LATCH_OVERLAY_BODY_OFF, C1S1_MG_LOCK_CENTER, C1S1_LATCH_ZOOM)
    show chapter_1_latch_overlay_keeper onlayer lockgame at c1s1_lock_part(C1S1_LATCH_OVERLAY_KEEPER_OFF, C1S1_MG_LOCK_CENTER, C1S1_LATCH_ZOOM)
    show chapter_1_latch_knob_outline onlayer lockgame at c1s1_latch_knob(C1S1_LATCH_KNOB_OFF, C1S1_MG_LOCK_CENTER, C1S1_LATCH_ZOOM), c1s1_mg_grab_outline("latch")
    show chapter_1_latch_knob onlayer lockgame at c1s1_latch_knob(C1S1_LATCH_KNOB_OFF, C1S1_MG_LOCK_CENTER, C1S1_LATCH_ZOOM)

    return

## Порядок show большого замка:
##   ЯЗЫЧОК → корпус → тень щеколды → ЩЕКОЛДА → тень вертушки → ВЕРТУШКА
## Корпус маскирует язычок; тень вертушки остаётся неподвижной.
label .show_big_lock:

    show chapter_1_big_lock_stroke onlayer lockgame at c1s1_big_stroke_slide(C1S1_BIG_STROKE_OFF, C1S1_MG_LOCK_CENTER, C1S1_BIG_LOCK_ZOOM)
    show chapter_1_big_lock_body onlayer lockgame at c1s1_lock_part(C1S1_BIG_BODY_OFF, C1S1_MG_LOCK_CENTER, C1S1_BIG_LOCK_ZOOM)
    show chapter_1_big_lock_latch_shadow onlayer lockgame at c1s1_big_latch_slide(C1S1_BIG_LATCH_SHADOW_OFF, C1S1_MG_LOCK_CENTER, C1S1_BIG_LOCK_ZOOM)
    show chapter_1_big_lock_latch_outline onlayer lockgame at c1s1_big_latch_slide(C1S1_BIG_LATCH_OFF, C1S1_MG_LOCK_CENTER, C1S1_BIG_LOCK_ZOOM), c1s1_mg_grab_outline("big_latch")
    show chapter_1_big_lock_latch onlayer lockgame at c1s1_big_latch_slide(C1S1_BIG_LATCH_OFF, C1S1_MG_LOCK_CENTER, C1S1_BIG_LOCK_ZOOM)
    show chapter_1_big_lock_spin_shadow onlayer lockgame at c1s1_lock_part(C1S1_BIG_SPIN_SHADOW_OFF, C1S1_MG_LOCK_CENTER, C1S1_BIG_LOCK_ZOOM)
    show c1s1_big_latch_arrow_img onlayer lockgame at c1s1_big_latch_arrow(C1S1_BIG_LATCH_ARROW_OFF, C1S1_MG_LOCK_CENTER, C1S1_BIG_LOCK_ZOOM)
    show chapter_1_big_lock_spin_outline onlayer lockgame at c1s1_big_spinner(C1S1_BIG_SPIN_OFF, C1S1_MG_LOCK_CENTER, C1S1_BIG_LOCK_ZOOM), c1s1_mg_grab_outline("big_spin")
    show chapter_1_big_lock_spin onlayer lockgame at c1s1_big_spinner(C1S1_BIG_SPIN_OFF, C1S1_MG_LOCK_CENTER, C1S1_BIG_LOCK_ZOOM)

    return

## Дверная ручка: планка, затем рычаг.
label .show_door_handle:

    show chapter_1_handle_body onlayer lockgame at c1s1_lock_part(C1S1_HANDLE_BODY_OFF, C1S1_MG_LOCK_CENTER, C1S1_HANDLE_ZOOM)
    show chapter_1_handle_lever_outline onlayer lockgame at c1s1_handle_lever(C1S1_HANDLE_OFF, C1S1_MG_LOCK_CENTER, C1S1_HANDLE_ZOOM), c1s1_mg_grab_outline("handle")
    show chapter_1_handle_lever onlayer lockgame at c1s1_handle_lever(C1S1_HANDLE_OFF, C1S1_MG_LOCK_CENTER, C1S1_HANDLE_ZOOM)

    return
