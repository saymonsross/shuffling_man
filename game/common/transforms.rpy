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

    def _shake_grow_f(power, t, start, delay, trans, st, at):
        since = st if start is None else fx_flag_time("shake_grow", start)
        if since is not None:
            since -= delay
        k = 0.0 if since is None or since <= 0.0 else (1.0 if t <= 0.0 else min(1.0, since / t))
        return _shake_f(power * k, trans, st, at)

## Нарастающая дрожь: размах растёт от нуля до power px за t секунд и дальше держится.
## Отсчёт — с момента показа; start — имя store-флага: дрожи нет, пока сцена его не взвела.
## С флагом трансформ ставится в ATL кадра заранее отдельным parallel: новый show … с ATL
## посреди кадра оборвал бы его остальные анимации. delay — секунды покоя перед ростом.
transform shake_grow(power=1.5, t=10.0, start=None, delay=0.0):
    subpixel True
    xoffset 0.0 yoffset 0.0
    function renpy.curry(_shake_grow_f)(power, t, start, delay)

init -10 python:

    def _float_drift_axis(amp, side, wave):
        return amp * wave if not side else amp * side * (1.0 + wave) * 0.5

    def _float_drift_f(amp, speed, side, trans, st, at):
        import math
        t = _fx_frame_time() * speed
        k = sm_motion_scale()
        trans.xoffset = k * _float_drift_axis(amp[0], side[0], 0.6 * math.sin(t * 0.997) + 0.4 * math.sin(t * 1.698 + 1.1))
        trans.yoffset = k * _float_drift_axis(amp[1], side[1], 0.6 * math.sin(t * 1.232 + 0.7) + 0.4 * math.sin(t * 2.167 + 2.3))
        return 0

## Медленное плавание по кадру (рука с пультом и т. п.): amp — размах (x, y), px. Время —
## часы кадра, не st: при смене кадра с тем же трансформом плавание продолжается без рывка.
## side — у спрайта, срезанного краем кадра: -1/1 по оси держат сдвиг только в эту сторону
## (влево/вверх или вправо/вниз), чтобы у края не открывалась щель; 0 — в обе стороны.
transform float_drift(amp=(4.0, 3.0), speed=1.0, side=(0, 0)):
    subpixel True
    xoffset 0.0 yoffset 0.0
    function renpy.curry(_float_drift_f)(amp, speed, side)

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

init -10 python:

    def _fade_out_on_f(flag, t, faster, k, pulse, pulse_in, pulse_out, trans, st, at):
        import math
        since = fx_flag_time("fade_out_on", flag)
        if since is None:
            trans.alpha = 1.0
            return 1.0 / 30.0
        rush = fx_flag_time("fade_out_on", faster) if faster else None
        done = since if rush is None else since + (k - 1.0) * min(rush, since)
        alpha = max(0.0, 1.0 - done / t) if t > 0.0 else 0.0
        if rush is not None and rush < pulse_in + pulse_out:
            if rush < pulse_in:
                bump = math.sin(0.5 * math.pi * rush / max(pulse_in, 0.001))
            else:
                bump = math.cos(0.5 * math.pi * (rush - pulse_in) / max(pulse_out, 0.001))
            alpha *= 1.0 + pulse * sm_motion_scale() * bump
        trans.alpha = min(1.0, alpha)
        return 0 if alpha > 0.0 else 1.0 / 30.0

## Угасание по флагу: пока store-флаг flag снят — картинка видна; с момента, как сцена его
## взвела, линейно гаснет за t секунд. Всё с одним флагом гаснет синхронно. Ставится в ATL
## показа заранее: новый show … с ATL посреди кадра сбросил бы позицию и анимации.
## faster — второй флаг: с его взвода угасание идёт в k раз быстрее, а картинка один раз
## вспыхивает — ярче на долю pulse: за pulse_in секунд разгорается, за pulse_out спадает.
transform fade_out_on(flag, t=1.0, faster=None, k=2.0, pulse=0.0, pulse_in=0.2, pulse_out=0.2):
    function renpy.curry(_fade_out_on_f)(flag, t, faster, k, pulse, pulse_in, pulse_out)

## Речь персонажа: Character(..., callback=talk_callback("ключ")) отмечает начало каждой
## его реплики, и всё, что слушает этот ключ (TalkFrames, mouth_talk(who=...)), двигает рот
## само, без строк в сценарии. Рот двигается столько, сколько длилась бы фраза вслух
## (mouth.chars знаков в секунду, не меньше 0.8 с). На знаках препинания внутри реплики
## рот ненадолго закрывается: фразы не сливаются.
## Движения рта идут по слогам самой реплики: слог — одна гласная, его время — по позиции
## в тексте; рот открывается в начале слога (или группы из mouth.per_move слогов) и
## закрывается к концу. «При-вет» — два движения. Реплику пролистнули — начатое движение
## доигрывает до закрытия, новых нет.
## Своя подача одной реплики — аргументом say: vit "…" (callback=talk_callback("vit",
## moves=2, hold=0.3)) — рот открывается moves раз, равномерно по длине фразы, каждый раз
## на hold секунд, без слогов и пауз на знаках; step — секунды между началами открытий
## вместо равномерного шага. drop — сколько последних движений обычной слоговой реплики
## убрать: рот на них остаётся закрытым. fade — растворение кадров TalkFrames на
## эту реплику вместо их собственного: при hold = fade кадр проявляется и сразу гаснет.
init -10 python:

    _TALK_VOWELS = u"аеёиоуыэюяaeiouy"
    _TALK_BREAKS = u".!?…,;:—–"

    def _talk_syllables(text, cps):
        """Слоги реплики: (начало, конец, после знака препинания) в секундах. Граница
        слогов — посередине между соседними гласными; слог перед знаком препинания
        кончается на знаке, не залезая в паузу после него."""
        vowels = [i for i, c in enumerate(text) if c.lower() in _TALK_VOWELS]
        if not vowels:
            return ((0.0, max(1.0, len(text)) / cps, False),)
        rv = []
        for k, v in enumerate(vowels):
            start = (vowels[k - 1] + v) / 2.0 if k else max(0.0, v - 1.0)
            end = (v + vowels[k + 1]) / 2.0 if k + 1 < len(vowels) else v + 1.5
            stop = next((i for i in range(v + 1, int(end) + 1) if i < len(text) and text[i] in _TALK_BREAKS), None)
            if stop is not None:
                end = min(end, float(stop))
            gap = text[vowels[k - 1]:v] if k else u""
            rv.append((start / cps, end / cps, any(c in _TALK_BREAKS for c in gap)))
        return tuple(rv)

    def _talk_pauses(text, cps):
        """Окна молчания (от, до) в секундах от начала реплики: конец предложения — 0.3 с,
        запятая и тире — 0.15 с. Знаки в самом конце реплики окна не дают."""
        rv = []
        last = len(text.rstrip(" .!?…,;:—–-"))
        for i, c in enumerate(text[:last]):
            if i + 1 < len(text) and text[i + 1] in ".!?…,;:":
                continue
            if c in ".!?…":
                rv.append((i / cps, i / cps + 0.3))
            elif c in ",;:—–":
                rv.append((i / cps, i / cps + 0.15))
        return tuple(rv)

    def _talk_moves(length, moves, hold, step=None):
        """moves отдельных движений равномерно по length секундам; открытая часть движения —
        доля mouth.open_share, поэтому движение длиннее hold на обратную долю."""
        span = hold / max(float(fx_cfg("mouth.open_share")), 0.05)
        step = length / moves if step is None else step
        return tuple((k * step, k * step + span, True) for k in range(moves))

    def _talk_event(who, event, what=None, moves=None, hold=0.3, fade=None, step=None, drop=0, **kwargs):
        if event == "show" and what:
            now = _fx_frame_time()
            _fx_state[("talk_line_fade", who)] = fade
            _fx_state[("talk_line_drop", who)] = int(drop)
            ## Тире перед репликой (what_prefix) не произносится.
            text = renpy.filter_text_tags(what, allow=()).lstrip("—– ")
            cps = float(fx_cfg("mouth.chars"))
            if moves:
                syllables = _talk_moves(max(0.8, len(text) / cps), int(moves), float(hold), step)
                pauses = ()
            else:
                syllables = _talk_syllables(text, cps)
                pauses = _talk_pauses(text, cps)
            ## Последний слог дотягивает до конца: иначе рот обрывался бы на нём.
            length = max(0.8, len(text) / cps, syllables[-1][1])
            _fx_state[("talk", who)] = (now, now + length, pauses, syllables, None)
        elif event == "end":
            ## Пролистнули — отметка обрыва: начатое движение доигрывает (talk_open).
            state = _fx_state.get(("talk", who))
            if state is not None and state[4] is None:
                _fx_state[("talk", who)] = state[:4] + (_fx_frame_time() - state[0],)

    def talk_callback(who, moves=None, hold=0.3, fade=None, step=None, drop=0):
        return renpy.partial(_talk_event, who, moves=moves, hold=hold, fade=fade, step=step, drop=drop)

    def talk_time(who):
        """Секунды с начала текущей реплики персонажа who; None — молчит (реплики нет,
        фраза договорена или пауза на знаке препинания)."""
        state = _fx_state.get(("talk", who))
        if state is None or renpy.predicting():
            return None
        now = _fx_frame_time()
        if now >= state[1]:
            return None
        t = max(0.0, now - state[0])
        for t0, t1 in state[2]:
            if t0 <= t < t1:
                return None
        return t

    def talk_open(who, rate=1.0, share=None, gap=0.0, trim=0.0):
        """Раскрытие рта персонажа who сейчас, 0..1: дуга внутри открытой части движения,
        0 — между движениями; None — молчит. rate меньше 1 — движения реже: одно на
        несколько слогов. share — доля движения, пока рот открыт (по умолчанию
        mouth.open_share); gap — не меньше стольких секунд рот закрыт перед следующим
        движением, даже если share держал бы его открытым дольше; trim — столько секунд
        срезается с конца каждого открытия. Знак препинания
        начинает новое движение. После обрыва реплики доигрывает только движение,
        начатое до него."""
        import math
        t = talk_time(who)
        if t is None:
            return None
        state = _fx_state[("talk", who)]
        cut = state[4]
        per = max(1.0, float(fx_cfg("mouth.per_move"))) / max(rate, 0.05)
        share = float(fx_cfg("mouth.open_share")) if share is None else float(share)
        ## Движения: (начало, конец, начало следующего слога или None).
        moves = []
        group = None
        acc = 0.0
        for start, end, after_break in state[3] + ((None, None, True),):
            if group is not None and (after_break or acc >= per - 1e-6):
                moves.append((group[0], group[1], start))
                acc = 0.0 if after_break else acc - per
                group = None
            if start is None:
                break
            group = (start, end) if group is None else (group[0], end)
            acc += 1.0
        drop = _fx_state.get(("talk_line_drop", who)) or 0
        if drop:
            moves = moves[:max(0, len(moves) - drop)]
        for g0, g1, after in moves:
            if cut is not None and g0 >= cut:
                return None
            if t < g0:
                return 0.0
            g_open = g0 + share * (g1 - g0)
            if after is not None and gap > 0.0:
                g_open = min(g_open, after - gap)
            g_open = max(g0 + 0.05, g_open - trim)
            if t < g_open:
                return math.sin(math.pi * (t - g0) / max(g_open - g0, 1e-3))
        return 0.0 if cut is None else None

    class TalkFrames(renpy.Displayable):
        """Покадровая речь: пока персонаж who говорит, кадры closed и opened меняются по
        слогам реплики (talk_open); молчит — стоит closed. Оба кадра — одна поза, различие
        только во рту. rate меньше 1 — рот двигается реже. share — доля движения, пока
        рот открыт (по умолчанию mouth.open_share); threshold (0..1) — с какого раскрытия
        показывать opened: выше — рот открыт короче. fade — секунды растворения между
        кадрами в обе стороны (0 — смена встык); шейдер перехода Dissolve, поэтому
        полупрозрачные края не мигают. gap — минимум секунд закрытого рта между
        движениями; trim — секунды, срезаемые с конца каждого открытия. При «меньше
        движения» рот не мелькает."""

        def __init__(self, closed, opened, who, rate=1.0, share=None, threshold=0.0, fade=0.0, gap=0.0, trim=0.0, **properties):
            super(TalkFrames, self).__init__(**properties)
            self.closed = renpy.displayable(closed)
            self.opened = renpy.displayable(opened)
            self.who = who
            self.rate = rate
            self.share = share
            self.gap = gap
            self.trim = trim
            self.threshold = threshold
            self.fade = fade

        def visit(self):
            return [self.closed, self.opened]

        def _full(self, d, width, height, st, at):
            ## place учитывает offset кадра; шейдеру оба кадра нужны одного размера.
            rv = renpy.Render(width, height)
            rv.place(d, 0, 0, width, height, st=st, at=at)
            return rv

        def render(self, width, height, st, at):
            opened = None if sm_reduced_motion() else talk_open(self.who, self.rate, self.share, self.gap, self.trim)
            target = 1.0 if opened is not None and opened > self.threshold else 0.0
            fade = _fx_state.get(("talk_line_fade", self.who))
            fade = self.fade if fade is None else fade
            if fade <= 0.0 or renpy.predicting():
                k = target
            else:
                ## Доля открытого кадра идёт к цели по часам кадра, ключ — сам объект.
                key = ("talk_fade", self.who, id(self))
                level, seen = _fx_state.get(key, (target, None))
                now = _fx_frame_time()
                dt = 0.0 if seen is None else max(0.0, min(now - seen, 0.1))
                step = dt / fade
                k = min(target, level + step) if level < target else max(target, level - step)
                _fx_state[key] = (k, now)
            renpy.redraw(self, 0 if opened is not None or k != target else 1.0 / 30.0)
            if k <= 0.0:
                return self._full(self.closed, width, height, st, at)
            if k >= 1.0:
                return self._full(self.opened, width, height, st, at)
            rv = renpy.Render(width, height)
            rv.mesh = True
            rv.add_shader("renpy.dissolve")
            ## Растворение — по плавной кривой: кадр трогается и садится мягко.
            rv.add_uniform("u_renpy_dissolve", k * k * (3.0 - 2.0 * k))
            rv.blit(self._full(self.closed, width, height, st, at), (0, 0))
            rv.blit(self._full(self.opened, width, height, st, at), (0, 0))
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
            ## Плавная кривая: поза трогается и садится мягко.
            rv.add_uniform("u_renpy_dissolve", k * k * (3.0 - 2.0 * k))
            rv.blit(self._full(self.old, width, height, st, at), (0, 0))
            rv.blit(self._full(self.new, width, height, st, at), (0, 0))
            return rv

    class StageDissolve(renpy.Displayable):
        """Цепочка кадров по счётчику прямо во время реплики: frames — кадры по порядку,
        counter — store-счётчик (сцена поднимает его: $ counter += 1), delay — имя
        store-переменной с задержкой в секундах. Через delay секунд после подъёма счётчика
        до n кадр n-1 растворяется в кадр n за fade секунд (шейдер перехода Dissolve).
        Счётчик 0 — первый кадр. Откат счётчика возвращает прежний кадр."""

        def __init__(self, frames, counter, delay, fade=0.3, **properties):
            super(StageDissolve, self).__init__(**properties)
            self.frames = [renpy.displayable(f) for f in frames]
            self.counter = counter
            self.delay = delay
            self.fade = fade

        def visit(self):
            return self.frames

        def _full(self, d, width, height, st, at):
            rv = renpy.Render(width, height)
            rv.place(d, 0, 0, width, height, st=st, at=at)
            return rv

        def render(self, width, height, st, at):
            n = max(0, min(len(self.frames) - 1, int(getattr(store, self.counter, 0) or 0)))
            if n == 0:
                renpy.redraw(self, 1.0 / 30.0)
                return self._full(self.frames[0], width, height, st, at)
            since = fx_flag_time("stage", self.counter)
            delay = float(getattr(store, self.delay, 0.0) or 0.0)
            k = 0.0 if since is None else (since - delay) / max(self.fade, 0.001)
            if sm_reduced_motion() and since is not None:
                k = 0.0 if k < 0.0 else 1.0
            renpy.redraw(self, 0 if 0.0 < k < 1.0 else 1.0 / 30.0)
            if k <= 0.0:
                return self._full(self.frames[n - 1], width, height, st, at)
            if k >= 1.0:
                return self._full(self.frames[n], width, height, st, at)
            rv = renpy.Render(width, height)
            rv.mesh = True
            rv.add_shader("renpy.dissolve")
            rv.add_uniform("u_renpy_dissolve", k)
            rv.blit(self._full(self.frames[n - 1], width, height, st, at), (0, 0))
            rv.blit(self._full(self.frames[n], width, height, st, at), (0, 0))
            return rv
