## transform_anchor не даёт rotate_pad сдвинуть якорь при повороте.
transform placed(pos_xy, anchor_xy=(0.0, 0.0), angle=None):
    transform_anchor True
    anchor anchor_xy
    pos pos_xy
    rotate angle

transform slide_in(from_xy, to_xy, t=0.9, jitter_amp=0.0, jitter_key="slide_in"):
    subpixel True
    anchor (0.0, 0.0)
    pos from_xy
    alpha 0.0
    xoffset 0.0 yoffset 0.0
    parallel:
        ease t alpha 1.0 pos to_xy
    parallel:
        function renpy.curry(object_jitter_f)(jitter_amp, 0.5, jitter_key)

## Одинаковый jitter_key бесшовно продолжает дрожь между трансформами.
transform placed_jitter(pos_xy, anchor_xy=(0.0, 0.0), jitter_amp=3.0, jitter_key="placed_jitter"):
    subpixel True
    anchor anchor_xy
    pos pos_xy
    xoffset 0.0 yoffset 0.0
    function renpy.curry(object_jitter_f)(jitter_amp, 0.5, jitter_key)

init -10 python:

    def _shake_f(power, trans, st, at):
        ## Накопитель привязан к картинке спрайта: она живёт, пока спрайт показан,
        ## а обёртка-трансформ пересоздаётся.
        return object_jitter_f(power, 0.5, "shake_%d" % id(trans.child or trans), trans, st, at)

## Дрожь спрайта поверх его позиции: `at placed(...), shake(1.5)`; power — размах, px.
transform shake(power=1.5):
    subpixel True
    xoffset 0.0 yoffset 0.0
    function renpy.curry(_shake_f)(power)

init -10 python:

    def _shake_grow_f(power, t, trans, st, at):
        return _shake_f(power * (1.0 if t <= 0.0 else min(1.0, st / t)), trans, st, at)

## Нарастающая дрожь: с момента показа размах растёт от нуля до power px за t секунд
## и дальше держится.
transform shake_grow(power=1.5, t=10.0):
    subpixel True
    xoffset 0.0 yoffset 0.0
    function renpy.curry(_shake_grow_f)(power, t)

## Дрожь по наведению для текста кнопки: hover/idle кнопка передаёт вложенным трансформам.
transform hover_shake(power=1.0):
    subpixel True
    on idle, selected_idle, insensitive:
        xoffset 0.0 yoffset 0.0
    on hover, selected_hover:
        function renpy.curry(_shake_f)(power * sm_motion_scale())

transform move_between(from_xy, to_xy, t=0.8, jitter_amp=0.0, jitter_key="move_between"):
    subpixel True
    anchor (0.0, 0.0)
    pos from_xy
    xoffset 0.0 yoffset 0.0
    parallel:
        ease t pos to_xy
    parallel:
        function renpy.curry(object_jitter_f)(jitter_amp, 0.5, jitter_key)

init -10 python:

    def _flag_alpha_f(flags, visible_when, relax, trans, st, at):
        """Хранит alpha в _fx_state между пересборками transform; ключ разделён
        по flags и ветви кроссфейда."""
        active = any(getattr(store, f, False) for f in flags)
        target = 1.0 if active == visible_when else 0.0
        key = "flagfade_" + "|".join(flags) + ("_on" if visible_when else "_off")
        trans.alpha = _fx_step(key, target, relax, start=target)
        return 1.0 / 60.0

transform flag_fade(pos_xy, flags, visible_when=True, relax=0.15):
    anchor (0.0, 0.0)
    pos pos_xy
    function renpy.curry(_flag_alpha_f)(flags, visible_when, relax)

## Речь персонажа: Character(..., callback=talk_callback("ключ")) отмечает начало каждой
## его реплики, и всё, что слушает этот ключ (TalkFrames, mouth_talk(who=...)), двигает рот
## само, без строк в сценарии. Рот двигается столько, сколько длилась бы фраза вслух
## (mouth.chars знаков в секунду, не меньше 0.8 с), и замирает, когда реплику пролистнули.
init -10 python:

    def _talk_event(who, event, what=None, **kwargs):
        if event == "show" and what:
            now = _fx_frame_time()
            spoken = len(renpy.filter_text_tags(what, allow=()))
            _fx_state[("talk", who)] = (now, now + max(0.8, spoken / float(fx_cfg("mouth.chars"))))
        elif event == "end":
            _fx_state.pop(("talk", who), None)

    def talk_callback(who):
        return renpy.partial(_talk_event, who)

    def talk_time(who):
        """Секунды с начала текущей реплики персонажа who; None — молчит."""
        state = _fx_state.get(("talk", who))
        if state is None or renpy.predicting():
            return None
        now = _fx_frame_time()
        return max(0.0, now - state[0]) if now < state[1] else None

    class TalkFrames(renpy.Displayable):
        """Покадровая речь: пока персонаж who говорит, кадры closed и opened меняются по
        слогам (mouth.rate в секунду, неровно); молчит — стоит closed. Оба кадра — одна
        поза, различие только во рту. rate — множитель темпа для этого места: меньше 1 —
        говорит медленнее. При «меньше движения» рот не мелькает."""

        def __init__(self, closed, opened, who, rate=1.0, **properties):
            super(TalkFrames, self).__init__(**properties)
            self.closed = renpy.displayable(closed)
            self.opened = renpy.displayable(opened)
            self.who = who
            self.rate = rate

        def visit(self):
            return [self.closed, self.opened]

        def render(self, width, height, st, at):
            t = None if sm_reduced_motion() else talk_time(self.who)
            renpy.redraw(self, 0 if t is not None else 1.0 / 30.0)
            frame = self.closed
            if t is not None:
                beat = t * float(fx_cfg("mouth.rate")) * self.rate
                ## Чётные слоги рот открыт дольше нечётных.
                if beat % 1.0 < (0.62 if int(beat) % 2 == 0 else 0.5):
                    frame = self.opened
            ## place учитывает offset кадра.
            rv = renpy.Render(width, height)
            rv.place(frame, 0, 0, width, height, st=st, at=at)
            return rv

init -5 python:

    class FlagDissolve(renpy.Displayable):
        """Смена картинки по времени прямо во время реплики: через after секунд после того,
        как сцена взвела store-флаг flag, old растворяется в new за fade секунд — тем же
        шейдером, что переход Dissolve, поэтому полупрозрачные края и тени не мигают.
        Пока флаг снят, показан old."""

        def __init__(self, old, new, flag, after, fade=0.2, **properties):
            super(FlagDissolve, self).__init__(**properties)
            self.old = renpy.displayable(old)
            self.new = renpy.displayable(new)
            self.flag = flag
            self.after = after
            self.fade = fade

        def visit(self):
            return [self.old, self.new]

        def _full(self, d, width, height, st, at):
            ## place учитывает offset/pos ребёнка: оба кадра нужны шейдеру одного размера.
            rv = renpy.Render(width, height)
            rv.place(d, 0, 0, width, height, st=st, at=at)
            return rv

        def render(self, width, height, st, at):
            since = fx_flag_time(("dissolve", self.after), self.flag)
            k = 0.0 if since is None else (since - self.after) / max(self.fade, 0.001)
            if sm_reduced_motion() and since is not None:
                k = 0.0 if k < 0.0 else 1.0
            ## Флаг ждём редким опросом, сам переход рисуем каждый кадр.
            renpy.redraw(self, 0 if 0.0 < k < 1.0 else 1.0 / 30.0)
            if k <= 0.0:
                return self._full(self.old, width, height, st, at)
            if k >= 1.0:
                return self._full(self.new, width, height, st, at)
            rv = renpy.Render(width, height)
            rv.mesh = True
            rv.add_shader("renpy.dissolve")
            rv.add_uniform("u_renpy_dissolve", k)
            rv.blit(self._full(self.old, width, height, st, at), (0, 0))
            rv.blit(self._full(self.new, width, height, st, at), (0, 0))
            return rv
