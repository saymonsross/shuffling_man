## Мини-игра «Замки»: щеколда → большой замок → дверная ручка.
## master продолжает сцену и стук; lockgame изолирует модели от камеры;
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
image chapter_1_latch_knob = "images/1_chapter/lock_mini_game/latch/latch_knob.png"

## У деталей большого замка разные холсты; расхождения заданы в C1S1_BIG_*_OFF.
image chapter_1_big_lock_body = "images/1_chapter/lock_mini_game/big_lock/big_lock_body.png"
image chapter_1_big_lock_stroke = "images/1_chapter/lock_mini_game/big_lock/big_lock_stroke.png"
image chapter_1_big_lock_latch_shadow = "images/1_chapter/lock_mini_game/big_lock/big_lock_latch_shadow.png"
image chapter_1_big_lock_latch = "images/1_chapter/lock_mini_game/big_lock/big_lock_latch.png"
image chapter_1_big_lock_spin_shadow = "images/1_chapter/lock_mini_game/big_lock/big_lock_knob_spinner_shadow.png"
## Центр обрезанной вертушки совпадает с осью вращения.
image chapter_1_big_lock_spin = "images/1_chapter/lock_mini_game/big_lock/big_lock_knob_spinner_crop.png"

## Рычаг ручки вращается вокруг C1S1_HANDLE_PIVOT, не центра холста.
image chapter_1_handle_body = "images/1_chapter/lock_mini_game/door_handle/door_handle_body.png"
image chapter_1_handle_lever = "images/1_chapter/lock_mini_game/door_handle/door_handle.png"

image chapter_1_mg_overlay = Solid("#0a0806")

## Игровое состояние

default c1s1_latch_open = False
default c1s1_big_lock_open = False
default c1s1_door_handle_open = False
## Чистое время управления закрытыми замками, сек.
default c1s1_locks_time = 0.0
default c1s1_locks_outcome = "fast"
default c1s1_locks_forced = False
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

## Кадр мини-игры и неподвижный фокус камеры.
define C1S1_MG_ZOOM = 1.06
define C1S1_MG_SETTLE_T = 1.4

define C1S1_MG_OVERLAY_ALPHA = 0.72
define C1S1_MG_OVERLAY_T = 0.9
define C1S1_MG_NOISE = 0.34     # выше FX_NOISE_DEFAULT

define C1S1_LOCKS_BTN_POS = (960, 800)
define C1S1_LOCKS_BTN_SIZE = (430, 190)

## Стук меняется медленной волной; пары значений — (тишина, пик).
define C1S1_MG_KNOCK_GAP = (1.35, 0.40)     # сек
define C1S1_MG_KNOCK_FLASH = (0.13, 0.42)   # доля белого
define C1S1_MG_KNOCK_FALL = (0.30, 0.14)    # сек
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

define C1S1_BIG_SPIN_RADIUS = 135
define C1S1_BIG_SPIN_TURN = 360.0   # градусы

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

define C1S1_MG_VITYA_INTERVAL_T = 10.0
define C1S1_MG_FAST_T = C1S1_MG_VITYA_INTERVAL_T
define C1S1_MG_TIMEOUT_T = C1S1_MG_VITYA_INTERVAL_T * 4.0
define C1S1_MG_TIMEOUT_HOLD_T = 1.8
define C1S1_MG_VITYA_LINES = (
    _("Это я, открывай!"),
    _("Опять заперлась? Я ж на минуту выскочил!"),
    _("Боже, что ты там возишься?"),
    _("Марина, ну ёбана! Замок сломался?"),
)
define C1S1_MG_VITYA_TIMEOUT_LINE = _("Всё, отходи!")

## Оверлей на master; модель замка живёт на отдельном lockgame.
define C1S1_Z_MG_OVERLAY = 50

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

    _c1s1_clock_state = _C1S1ClockState()

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
            "timeout_play_t": -1.0,
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
        store.c1s1_locks_forced = False
        store.c1s1_mg_knocking = False
        store.c1s1_mg_active = False
        c1s1_mg_cancel_pointer()
        c1s1_mg_anchor_clock()

    def c1s1_mg_stop():
        """Обнуляет shake до остановки драйвера, чтобы кадр не застыл смещённым."""
        _mg_set("shake_a", 0.0)
        _mg_set("shake_t", 0.0)

    def c1s1_mg_elapsed():
        """Время реального управления ещё закрытыми замками."""
        return _mg_get("decision_t")

    def c1s1_mg_outcome_for_time(elapsed):
        if elapsed < C1S1_MG_FAST_T:
            return "fast"
        if elapsed < C1S1_MG_TIMEOUT_T:
            return "normal"
        return "timeout"

    def c1s1_mg_vitya_line(elapsed=None):
        if elapsed is None:
            elapsed = c1s1_mg_elapsed()
        if elapsed >= C1S1_MG_TIMEOUT_T:
            return C1S1_MG_VITYA_TIMEOUT_LINE
        i = min(int(elapsed // C1S1_MG_VITYA_INTERVAL_T),
                len(C1S1_MG_VITYA_LINES) - 1)
        return C1S1_MG_VITYA_LINES[max(0, i)]

    def c1s1_mg_vitya_dd(st, at):
        return Text(c1s1_mg_vitya_line(), style="c1s1_mg_bark_text"), 0.1

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

    ## Драйвер

    def c1s1_mg_knock_step():
        """Косинусная волна с шумом задаёт интервал и силу следующего стука."""
        t = _mg_get("elapsed")
        nxt = _mg_get("knock_next")

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

        ## TODO(звук): удар в дверь.
        flash_fx(high=_mg_lerp(C1S1_MG_KNOCK_FLASH[0], C1S1_MG_KNOCK_FLASH[1], wave),
                 fall=_mg_lerp(C1S1_MG_KNOCK_FALL[0], C1S1_MG_KNOCK_FALL[1], wave))
        _mg_set("shake_a", _mg_lerp(C1S1_MG_KNOCK_SHAKE[0], C1S1_MG_KNOCK_SHAKE[1], wave))
        _mg_set("shake_t", 0.0)

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
            if not store.c1s1_locks_forced and not c1s1_mg_lock_open():
                _mg_set("decision_t", _mg_get("decision_t") + dt)
            c1s1_mg_timeout_step()
            if not c1s1_mg_simplified_tick(dt):
                lock = c1s1_mg_lock()
                if lock == "latch":
                    c1s1_latch_step(dt)
                elif lock == "big_lock":
                    c1s1_big_step(dt)
                elif lock == "door_handle":
                    c1s1_handle_step(dt)

    ## Камера

    def c1s1_mg_camera_f(strength, smooth, key, trans, st, at):
        """Сводит параллакс и shake в общие _fx_state-ключи камеры двери."""
        if renpy.predicting():
            return 1.0 / 60.0
        strength = _fx_num(strength, 10.0, 0.0)
        if sm_reduced_motion():
            for suffix in ("_px", "_py", "_jx", "_jy"):
                _fx_state[key + suffix] = 0.0
            trans.xoffset = 0.0
            trans.yoffset = 0.0
            _fx_publish_camera(key, trans)
            return 1.0 / 60.0
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
            _mg_set("latch_p", p)

            if p >= max_p:
                ## TODO(звук): лязг отодвинутой щеколды.
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

        _mg_set("big_p", p)
        if p >= 2.0:
            ## TODO(звук): щелчок ригеля большого замка.
            _mg_set("big_grab", 0.0)
            store.c1s1_big_lock_open = True

    def c1s1_big_turn():
        return max(0.0, min(1.0, _mg_get("big_p") - 1.0))

    def c1s1_big_latch_f(trans, st, at):
        trans.xoffset = C1S1_BIG_LATCH_TRAVEL * C1S1_BIG_LOCK_ZOOM * min(1.0, _mg_get("big_p"))
        return 1.0 / 60.0

    def c1s1_big_stroke_f(trans, st, at):
        trans.xoffset = C1S1_BIG_STROKE_TRAVEL * C1S1_BIG_LOCK_ZOOM * c1s1_big_turn()
        return 1.0 / 60.0

    def c1s1_big_spin_f(trans, st, at):
        trans.rotate = -C1S1_BIG_SPIN_TURN * c1s1_big_turn()
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
            _mg_set("handle_p", p)
            if p >= 1.0:
                ## TODO(звук): щелчок дверной ручки.
                _mg_set("handle_grab", 0.0)
                store.c1s1_door_handle_open = True
            return

        _mg_set("handle_p", max(0.0, p - dt / max(0.05, C1S1_HANDLE_RETURN_T)))

    def c1s1_handle_f(trans, st, at):
        trans.rotate = C1S1_HANDLE_TURN * _mg_get("handle_p")
        return 1.0 / 60.0

    ## Ввод

    def c1s1_mg_grab():
        c1s1_mg_cancel_pointer()
        if (not store.c1s1_mg_active or store.c1s1_locks_forced
                or c1s1_mg_lock_open()):
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

    def c1s1_mg_release():
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
        if (not store.c1s1_mg_active or store.c1s1_locks_forced
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
            key, limit, speed = "latch_p", c1s1_latch_max_p(), 3.5
        elif lock == "big_lock":
            key, limit, speed = "big_p", 2.0, 2.5
        elif lock == "door_handle":
            key, limit, speed = "handle_p", 1.0, 2.5
        else:
            _mg_set("simple_target", -1.0)
            return False

        p = min(target, _mg_get(key) + dt * speed)
        _mg_set(key, p)
        if p + 0.0001 < target:
            return True

        _mg_set("simple_target", -1.0)
        if p + 0.0001 >= limit:
            setattr(store, C1S1_MG_LOCK_FLAGS[lock], True)
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

    def c1s1_mg_timeout_step():
        if not store.c1s1_mg_active:
            return
        if not store.c1s1_locks_forced:
            if c1s1_mg_elapsed() < C1S1_MG_TIMEOUT_T:
                return
            store.c1s1_locks_forced = True
            _mg_set("timeout_play_t", _mg_get("play_t"))
            c1s1_mg_release()
        if (_mg_get("play_t") - _mg_get("timeout_play_t")
                >= C1S1_MG_TIMEOUT_HOLD_T):
            c1s1_mg_open_all()

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

## Начальный zoom наследуется для плавной склейки; rotate сбрасывается явно.
transform c1s1_mg_camera(z1=C1S1_MG_ZOOM, t=C1S1_MG_SETTLE_T, strength=8.0, smooth=0.06, key="cam"):
    subpixel True
    align (0.5, 0.5)
    rotate 0.0
    parallel:
        ease sm_motion_time(t) zoom z1
    parallel:
        function renpy.curry(c1s1_mg_camera_f)(strength, smooth, key)

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
    function c1s1_mg_bag_f

## Экраны

## Timer меняет модель на всём протяжении эпизода.
screen c1s1_mg_runtime():
    ## Под modal-меню таймер останавливается.
    timer C1S1_MG_TICK_T action Function(c1s1_mg_tick, _update_screens=False) repeat True modal True

## Кнопка «Открыть дверь» использует мировые координаты.
screen c1s1_locks_open_door():
    ## Выше quick_menu: интерактив остаётся modal.
    zorder 110
    modal True
    timer C1S1_MG_TICK_T action Function(c1s1_mg_tick, _update_screens=False) repeat True modal True
    fixed:
        id "door_world"
        at follow_camera(zoom_pad=C1S1_MG_ZOOM)
        xysize (config.screen_width, config.screen_height)
        use glow_button(
            _("Открыть дверь"),
            Return("done"),
            bg="dark",
            pulse="alarm",
            pos=C1S1_LOCKS_BTN_POS,
            size=C1S1_LOCKS_BTN_SIZE)

## Drag для мыши и focusable-альтернатива для клавиатуры, touch и self-voicing.
screen c1s1_locks_minigame():
    zorder 110
    modal True

    on "hide" action Function(c1s1_mg_release, _update_screens=False)

    timer C1S1_MG_TICK_T action Function(c1s1_mg_tick, _update_screens=False) repeat True modal True
    timer C1S1_MG_POLL_T action Function(c1s1_mg_check_done) repeat True modal True

    use c1s1_mg_vitya_bark

    if persistent.sm_simplified_locks:
        textbutton c1s1_mg_simplified_label():
            style "c1s1_mg_step_button"
            action Function(c1s1_mg_simplified_step)
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

screen c1s1_mg_vitya_bark():

    frame:
        style "c1s1_mg_bark_frame"

        vbox:
            spacing 4
            text _("Витя") style "c1s1_mg_bark_name"
            add DynamicDisplayable(c1s1_mg_vitya_dd)

style c1s1_mg_bark_frame is frame:
    xalign 0.5
    yalign 0.04
    xsize 1500
    padding (30, 18)
    background Solid("#0a0806e6")

style c1s1_mg_bark_name is default:
    properties gui.text_properties("name")
    color "#5c7c9e"

style c1s1_mg_bark_text is default:
    properties gui.text_properties("dialogue")
    xsize 1440

style c1s1_mg_access_button is button:
    background Solid("#17120ee6")
    hover_background Solid("#915454f2")
    insensitive_background Solid("#17120e99")
    padding (22, 12)

style c1s1_mg_access_button_text is button_text:
    color "#f2ece0"
    hover_color "#ffffff"
    insensitive_color "#aaa39a"
    outlines [(2, "#000000cc", 0, 0)]
    size 25

style c1s1_mg_step_button is c1s1_mg_access_button:
    padding (30, 16)

style c1s1_mg_step_button_text is c1s1_mg_access_button_text:
    size 30

## Сцена

label chapter_1_scene_1_minigame_locks:

    ## Камера доводит наезд и остаётся связана с мировой кнопкой.
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
    $ fx_noise_strength = C1S1_MG_NOISE
    $ pause(C1S1_MG_OVERLAY_T)

    ## Замки открываются по C1S1_MG_LOCK_ORDER без остановки часов и стука.
    $ c1s1_mg_lock_i = 0
    while c1s1_mg_lock() is not None:
        call .play_lock from _call_c1s1_mg_play_lock

    $ c1s1_locks_time = c1s1_mg_elapsed()
    $ c1s1_locks_outcome = c1s1_mg_outcome_for_time(c1s1_locks_time)

    ## Возврат к сцене.
    $ c1s1_mg_knocking = False
    $ fx_noise_strength = FX_NOISE_DEFAULT
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
    show chapter_1_latch_knob onlayer lockgame at c1s1_latch_knob(C1S1_LATCH_KNOB_OFF, C1S1_MG_LOCK_CENTER, C1S1_LATCH_ZOOM)

    return

## Порядок show большого замка:
##   ЯЗЫЧОК → корпус → тень щеколды → ЩЕКОЛДА → тень вертушки → ВЕРТУШКА
## Корпус маскирует язычок; тень вертушки остаётся неподвижной.
label .show_big_lock:

    show chapter_1_big_lock_stroke onlayer lockgame at c1s1_big_stroke_slide(C1S1_BIG_STROKE_OFF, C1S1_MG_LOCK_CENTER, C1S1_BIG_LOCK_ZOOM)
    show chapter_1_big_lock_body onlayer lockgame at c1s1_lock_part(C1S1_BIG_BODY_OFF, C1S1_MG_LOCK_CENTER, C1S1_BIG_LOCK_ZOOM)
    show chapter_1_big_lock_latch_shadow onlayer lockgame at c1s1_big_latch_slide(C1S1_BIG_LATCH_SHADOW_OFF, C1S1_MG_LOCK_CENTER, C1S1_BIG_LOCK_ZOOM)
    show chapter_1_big_lock_latch onlayer lockgame at c1s1_big_latch_slide(C1S1_BIG_LATCH_OFF, C1S1_MG_LOCK_CENTER, C1S1_BIG_LOCK_ZOOM)
    show chapter_1_big_lock_spin_shadow onlayer lockgame at c1s1_lock_part(C1S1_BIG_SPIN_SHADOW_OFF, C1S1_MG_LOCK_CENTER, C1S1_BIG_LOCK_ZOOM)
    show chapter_1_big_lock_spin onlayer lockgame at c1s1_big_spinner(C1S1_BIG_SPIN_OFF, C1S1_MG_LOCK_CENTER, C1S1_BIG_LOCK_ZOOM)

    return

## Дверная ручка: планка, затем рычаг.
label .show_door_handle:

    show chapter_1_handle_body onlayer lockgame at c1s1_lock_part(C1S1_HANDLE_BODY_OFF, C1S1_MG_LOCK_CENTER, C1S1_HANDLE_ZOOM)
    show chapter_1_handle_lever onlayer lockgame at c1s1_handle_lever(C1S1_HANDLE_OFF, C1S1_MG_LOCK_CENTER, C1S1_HANDLE_ZOOM)

    return
