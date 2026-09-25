## Удержание: метку сносит «дрожь», игрок удерживает её в зоне. Поражения нет: итог — доля
## времени в зоне (0.0–1.0) или "skipped". Попытка живёт в объекте CDD из default экрана:
## каждый call screen начинает её заново.

define HOLD_ZONE_ZORDER = 110
define HOLD_ZONE_SIZE = (960, 160)
define HOLD_ZONE_W = 200
define HOLD_ZONE_MARK_W = 18
define HOLD_ZONE_FILL_H = 8
define HOLD_ZONE_HINT_Y = 330
define HOLD_ZONE_DURATION = 8.0
define HOLD_ZONE_PUSH = 520.0           # px/с от ввода игрока
define HOLD_ZONE_DRIFT = 300.0          # px/с максимальный снос
define HOLD_ZONE_DRIFT_EVERY = (0.4, 1.1)
## «Простые мини-игры»: снос слабее, зона та же.
define HOLD_ZONE_SIMPLE_DRIFT = 0.35
## Потолок шага: время меню и подвисания не превращается в рывок метки.
define HOLD_ZONE_MAX_DT = 0.05
define HOLD_ZONE_POINTER_DEADZONE = 8

define HOLD_ZONE_LEFT = ["K_LEFT", "pad_dpleft_press", "pad_leftx_neg"]
define HOLD_ZONE_RIGHT = ["K_RIGHT", "pad_dpright_press", "pad_leftx_pos"]
## У геймпада нет keyup: отпускание — отдельные события *_release и возврат оси в ноль.
define HOLD_ZONE_LEFT_UP = ["keyup_K_LEFT", "pad_dpleft_release", "pad_leftx_zero"]
define HOLD_ZONE_RIGHT_UP = ["keyup_K_RIGHT", "pad_dpright_release", "pad_leftx_zero"]

default hold_zone_seed = 0

init python:

    import random as hold_zone_random

    class HoldZone(renpy.Displayable):
        """Итог отдаёт event(): из render интеракцию не завершить."""

        def __init__(self, duration, seed, simple=False, **properties):
            super(HoldZone, self).__init__(**properties)
            self.duration = float(duration)
            ## Свой генератор: renpy.random в каждом кадре засорил бы лог отката.
            self.rng = hold_zone_random.Random(seed)
            self.drift_scale = HOLD_ZONE_SIMPLE_DRIFT if simple else 1.0
            self.x = HOLD_ZONE_SIZE[0] / 2.0
            self.drift = 0.0
            self.drift_left = 0.0
            self.left = False
            self.right = False
            self.pointer = None
            self.last_st = None
            self.t = 0.0
            self.inside_t = 0.0
            self.result = None
            self.track = Solid("#2a2430", xysize=HOLD_ZONE_SIZE)
            self.zone = Solid("#3c6b4a", xysize=(HOLD_ZONE_W, HOLD_ZONE_SIZE[1]))
            self.mark_in = Solid("#f2ece0", xysize=(HOLD_ZONE_MARK_W, HOLD_ZONE_SIZE[1]))
            self.mark_out = Solid("#e06666", xysize=(HOLD_ZONE_MARK_W, HOLD_ZONE_SIZE[1]))
            self.fill = Solid("#e2cea4")

        def inside(self):
            return abs(self.x - HOLD_ZONE_SIZE[0] / 2.0) <= HOLD_ZONE_W / 2.0

        def direction(self):
            if self.pointer is not None:
                gap = self.pointer - self.x
                if abs(gap) < HOLD_ZONE_POINTER_DEADZONE:
                    return 0.0
                return 1.0 if gap > 0 else -1.0
            return float(self.right) - float(self.left)

        def step(self, dt):
            ## Последний шаг не выходит за конец попытки: иначе доля в зоне превысит 1.0.
            dt = min(dt, self.duration - self.t)
            self.drift_left -= dt
            if self.drift_left <= 0.0:
                self.drift = self.rng.uniform(-HOLD_ZONE_DRIFT, HOLD_ZONE_DRIFT) * self.drift_scale
                self.drift_left = self.rng.uniform(*HOLD_ZONE_DRIFT_EVERY)
            speed = self.drift + self.direction() * HOLD_ZONE_PUSH
            self.x = min(max(self.x + speed * dt, 0.0), float(HOLD_ZONE_SIZE[0]))
            if self.inside():
                self.inside_t += dt
            self.t += dt
            if self.t >= self.duration:
                self.result = round(self.inside_t / self.duration, 3)

        def render(self, width, height, st, at):
            ## Шаг детерминирован по st: повторный рендер с тем же st ничего не меняет.
            dt = 0.0 if self.last_st is None else min(max(st - self.last_st, 0.0), HOLD_ZONE_MAX_DT)
            self.last_st = st
            if self.result is None:
                self.step(dt)

            w, h = HOLD_ZONE_SIZE
            rv = renpy.Render(w, h)
            rv.place(self.track)
            rv.place(self.zone, x=(w - HOLD_ZONE_W) // 2, y=0)
            rv.place(self.mark_in if self.inside() else self.mark_out,
                x=int(round(self.x - HOLD_ZONE_MARK_W / 2.0)), y=0)
            fill_w = int(round(w * min(self.t / self.duration, 1.0)))
            if fill_w > 0:
                rv.blit(renpy.render(self.fill, fill_w, HOLD_ZONE_FILL_H, st, at), (0, h - HOLD_ZONE_FILL_H))

            if self.result is None:
                renpy.redraw(self, 0)
            else:
                ## Без этого event() не позовут, и итог не вернётся из call screen.
                renpy.timeout(0)
            return rv

        def event(self, ev, x, y, st):
            if self.result is not None:
                return self.result

            ## Потерянный фокус окна: отпускание клавиш и мыши до нас уже не дойдёт.
            if ev.type == renpy.pygame.ACTIVEEVENT and not ev.gain:
                if ev.state & 1:
                    self.pointer = None
                if ev.state & 2:
                    self.left = self.right = False
                return None

            handled = False
            if renpy.map_event(ev, HOLD_ZONE_LEFT):
                self.left = handled = True
            if renpy.map_event(ev, HOLD_ZONE_RIGHT):
                self.right = handled = True
            if renpy.map_event(ev, HOLD_ZONE_LEFT_UP):
                self.left = False
                handled = True
            if renpy.map_event(ev, HOLD_ZONE_RIGHT_UP):
                self.right = False
                handled = True

            w, h = HOLD_ZONE_SIZE
            if self.pointer is None:
                if renpy.map_event(ev, "mousedown_1") and 0 <= x < w and 0 <= y < h:
                    self.pointer = float(x)
                    handled = True
            elif ev.type == renpy.pygame.MOUSEMOTION:
                if x >= 0:
                    self.pointer = float(min(max(x, 0), w))
                handled = True
            elif renpy.map_event(ev, "mouseup_1"):
                self.pointer = None
                handled = True

            ## Съедаем только своё: TIMEEVENT других экранов, Esc, F11, Shift+A живут дальше.
            if handled:
                raise renpy.IgnoreEvent()
            return None

        def visit(self):
            return [self.track, self.zone, self.mark_in, self.mark_out, self.fill]

style hold_zone_text is gui_text:
    color "#f1e9db"
    size 30
    xalign 0.5
    textalign 0.5

screen minigame_hold_zone_screen(duration=HOLD_ZONE_DURATION, seed=0, skippable=False):
    zorder HOLD_ZONE_ZORDER
    modal True
    roll_forward True

    ## Колесо и PgUp посреди свежей попытки перезапустили бы её. В пройденной попытке (есть данные
    ## прокрутки вперёд) не блокируем: игрок листает назад или вперёд к прежнему итогу.
    ## renpy.in_rollback() не годится: после загрузки оно истинно при первом показе экрана.
    if renpy.roll_forward_info() is None:
        key "rollback" action NullAction()

    if skippable:
        use sm_skippable_interaction

    default arena = HoldZone(duration, seed, persistent.sm_simplified_locks,
        alt=_("Удержание метки в зоне: стрелки влево и вправо или мышь"))

    add Solid("#000000aa")
    text _("Держите метку в зелёной зоне: ← → или мышью") style "hold_zone_text" ypos HOLD_ZONE_HINT_Y
    add arena:
        id "hold_zone_arena"
        align (0.5, 0.55)

## Вызов: call minigame_hold_zone(6.0) → _return = доля времени в зоне (0.0–1.0) или "skipped".
## Исход идёт в сюжет → пропуск останавливается; без влияния на сюжет — hold_zone_skippable=True.
## Откат: свежую попытку колесо не перезапускает; откатившись в пройденную, можно листать дальше
## назад или вперёд к прежнему итогу (roll_forward). Сид из renpy.random: откат повторяет рисунок сноса.
label minigame_hold_zone(hold_zone_duration=HOLD_ZONE_DURATION, hold_zone_skippable=False) hide:
    if hold_zone_skippable and renpy.is_skipping():
        return "skipped"
    if not hold_zone_skippable:
        $ skip_stop()
    $ hold_zone_seed = renpy.random.randint(0, 2 ** 30)
    call screen minigame_hold_zone_screen(hold_zone_duration, hold_zone_seed, hold_zone_skippable)
    ## SkipOnce позднего пропуска завершает экран значением True.
    if _return is True:
        return "skipped"
    return _return
