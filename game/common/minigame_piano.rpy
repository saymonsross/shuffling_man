## Мини-игра пианино: одна октава клавиш на экране, над ней ноты MIDI-эталона опускаются к
## клавишам в темпе метронома сцены. Шаг — все ноты одной позиции (бас + мелодия): его ноты
## звучат только в момент, когда все клавиши шага оказались зажаты одновременно (клавиатура —
## реальное удержание, клик мышью «залипает» до сбора шага); до этого не звучит ничего. Потом
## следующие ноты подступают в темпе. Опоздание не наказывается — ноты стоят у клавиш;
## неправильная клавиша — холостой «деревянный» щелчок. Поражения нет: исход "clean" /
## "flawed" (были неправильные клавиши) / "skipped".
##
## Партия — путь к .mid (одна дорожка, темп не важен) или кортеж шагов
## ((позиция в шестнадцатых, ((имя, октава, длительность в шестнадцатых), ...)), ...).
## Ноты одного имени в шаге (F#3 + F#4) — одна клавиша, но звучат обе.
## break_before_end > 0: столько последних шагов не доигрывается — сбор шага перед ними
## не звучит, игра возвращается в момент обрушения, а падение осколков сцена показывает сама:
## show screen minigame_piano_screen → свои show/camera/pause → hide screen + piano_collapse_end().
## Сэмплы клавиш — PIANO_KEYS_DIR/<нота><октава>.ogg: c4, c#4, d4 …; щелчок — PIANO_DEAD_SOUND.

define PIANO_ZORDER = 110
define PIANO_SUBDIV = 4
define PIANO_KEYS_DIR = "audio/keys/"
define PIANO_KEYS_EXT = ".ogg"
define PIANO_DEAD_SOUND = "audio/keys/key_dead.ogg"
## Громкость сэмплов клавиш; промашки и обрушение — на своей.
define PIANO_KEY_VOLUME = 0.9
## Под холостым щелчком — тихий короткий призвук нажатой клавиши: PIANO_SOFT_DIR/<нота>.ogg
## (громкость и затухание запечены в файл, tools/cut_piano_keys.py).
define PIANO_SOFT_DIR = "audio/keys/soft/"
## Первый шаг партии ждёт у клавиш сразу; после нажатия следующий подступает по сетке от доли
## нажатия, не раньше чем через PIANO_WINDOW.
define PIANO_WINDOW = 0.18
## Время подтяжки такта к позиции звука метронома, с: позиция обновляется рывками.
define PIANO_SYNC_TAU = 0.25
define PIANO_SYNC_T = 0.05
## Раскладка клавиатурного пианино: нижний ряд — белые C…B, ряд над ним — чёрные.
## Скан-коды SDL (физические клавиши): работают при любой раскладке. Второе поле — запас
## под верхнюю октаву (сейчас всегда 0).
define PIANO_NOTE_NAMES = ("c", "cs", "d", "ds", "e", "f", "fs", "g", "gs", "a", "as", "b")
define PIANO_KEYS = (
    ("c", 0, "z", 29), ("cs", 0, "s", 22), ("d", 0, "x", 27), ("ds", 0, "d", 7), ("e", 0, "c", 6),
    ("f", 0, "v", 25), ("fs", 0, "g", 10), ("g", 0, "b", 5), ("gs", 0, "h", 11), ("a", 0, "n", 17),
    ("as", 0, "j", 13), ("b", 0, "m", 16),
)
## Стыки белых клавиш, над которыми стоят чёрные: C-D, D-E, F-G, G-A, A-B.
define PIANO_BLACK_SLOTS = (0, 1, 3, 4, 5)

## Клавиатура на кадре: белые клавиши слева направо, чёрные — над стыками.
define PIANO_KB_X = 612
define PIANO_KB_Y = 812
define PIANO_WHITE_W = 96
define PIANO_WHITE_H = 190
define PIANO_WHITE_GAP = 4
define PIANO_BLACK_W = 58
define PIANO_BLACK_H = 116
define PIANO_FLASH_T = 0.15
## Пульс подсветки: вспышка на щелчке гаснет до нижнего уровня за PIANO_PULSE_T.
define PIANO_PULSE_LOW = 0.45
define PIANO_PULSE_T = 0.22
## Дорожка падающих нот: линия — верх клавиш, доля — PIANO_PX_PER_BEAT px вверх.
## Брусок белой клавиши — штриховка в контуре, чёрной — контур с затемнением; края рвёт
## скратч-шейдер (группа piano_notes, тюнер — Piano Tuner в Dev Hub).
define PIANO_FALL_TOP = 3
define PIANO_PX_PER_BEAT = 90
define PIANO_BAR_INSET = 8
define PIANO_BAR_MIN_H = 18
define PIANO_BAR_BORDER = 3
## Чёрный контур вокруг бруска ноты белой клавиши, px: светлая штриховка не теряется на светлом.
define PIANO_BAR_OUTLINE = 3
define PIANO_BAR_PAD = 12
define PIANO_KEY_PAD = 6
define PIANO_HATCH_PERIOD = 11.0
define PIANO_HATCH_THICK = 3.0
define PIANO_BAR_LABEL_SIZE = 30
## Сыгранный шаг уходит вниз за клавиши в темпе и растворяется за PIANO_BAR_FADE_T.
define PIANO_BAR_FADE_T = 1.0
## Подсказка держится первые PIANO_HINT_STEPS шагов и растворяется за PIANO_HINT_FADE_T.
define PIANO_HINT_STEPS = 4
define PIANO_HINT_FADE_T = 1.0
## Мини-игра проявляется за PIANO_FADE_IN_T от старта (по часам игры: каждое нажатие — новая интеракция).
define PIANO_FADE_IN_T = 0.8
## Раннее нажатие подтягивает мелодию к игроку: бруски доезжают до новых мест за PIANO_SNAP_T,
## а не прыгают.
define PIANO_SNAP_T = 0.12
## Обрушение: осколки бруска (PIANO_SHARDS на ноту) разлетаются и падают с гравитацией,
## экран держится PIANO_COLLAPSE_T и последние PIANO_COLLAPSE_FADE_T гаснет целиком.
define PIANO_COLLAPSE_T = 1.8
define PIANO_COLLAPSE_FADE_T = 0.4
define PIANO_SHARDS = 3
define PIANO_GRAVITY = 2400.0
define PIANO_SHARD_VX = (40.0, 160.0)
define PIANO_SHARD_VY = (-220.0, -40.0)
define PIANO_SHARD_SPIN = (60.0, 200.0)
## Клавиши ломаются пополам и тяжелее нот: срываются с задержкой, летят ниже и медленнее.
define PIANO_KEY_SHARDS = 2
define PIANO_KEY_SHARD_DELAY = (0.05, 0.35)
define PIANO_KEY_SHARD_VX = (15.0, 80.0)
define PIANO_KEY_SHARD_VY = (-170.0, -40.0)
define PIANO_KEY_SHARD_SPIN = (25.0, 110.0)
define PIANO_KEY_LABEL_SIZE = 32
define PIANO_COLORS = {
    "white": "#e9e2d6", "white_hover": "#f6f1e8", "white_down": "#b9b0a1", "white_label": "#141210",
    "black": "#241f1c", "black_hover": "#3a332e", "black_down": "#0f0d0b", "black_label": "#efe9df",
    "white_next": "#9c1f1f", "black_next": "#6e1010",
    "bar_outline": "#050403", "bar_edge": "#f2ece0", "bar_hatch": "#f2ece0c0", "bar_dark": "#050403f2", "bar_done": "#7e8f6a80",
    "bar_label_white": "#141210", "bar_label_black": "#efe9df",
    "line": "#f2ece080",
}

default piano_state = {}

init -10 python:
    scratch_params("piano_notes", "Ноты пианино", 2.0, 0.3, 1.0, 0.55)
    ## Клавиши — тот же штрих, но слабее: дрожание в полпикселя, без разрывов.
    scratch_params("piano_keys", "Клавиши пианино", 0.6, 0.05, 0.6, 0.35)

    ## Диагональная штриховка бруска белой клавиши.
    renpy.register_shader("sm.piano_hatch",
        variables="""
        uniform vec2 u_model_size;
        uniform float u_hatch_period;
        uniform float u_hatch_thick;
        uniform vec4 u_hatch_color;
        attribute vec2 a_tex_coord;
        varying vec2 v_tex_coord;
        """,
        vertex_300="""
        v_tex_coord = a_tex_coord;
        """,
        fragment_300="""
        vec2 p = v_tex_coord * u_model_size;
        float d = mod(p.x + p.y, u_hatch_period);
        float a = step(d, u_hatch_thick) * u_hatch_color.a;
        gl_FragColor = vec4(u_hatch_color.rgb * a, a);
        """)

init -5 python:

    def piano_read_midi(path):
        """Ноты .mid: (высота, начало в долях, длительность в долях); темп не нужен."""
        import struct
        f = renpy.file(path)
        try:
            data = f.read()
        finally:
            f.close()
        if data[:4] != b"MThd":
            raise ValueError("%s: не MIDI" % path)
        ppq = struct.unpack(">H", data[12:14])[0]
        if ppq & 0x8000:
            raise ValueError("%s: SMPTE-время не поддерживается" % path)
        pos = 8 + struct.unpack(">I", data[4:8])[0]
        notes = []
        while pos + 8 <= len(data):
            chunk, size = data[pos:pos + 4], struct.unpack(">I", data[pos + 4:pos + 8])[0]
            body, pos = data[pos + 8:pos + 8 + size], pos + 8 + size
            if chunk != b"MTrk":
                continue
            i, tick, status, open_notes = 0, 0, 0, {}
            while i < len(body):
                delta = 0
                while True:
                    b = body[i]; i += 1
                    delta = (delta << 7) | (b & 0x7F)
                    if not b & 0x80:
                        break
                tick += delta
                b = body[i]
                if b == 0xFF or b in (0xF0, 0xF7):
                    i += 2 if b == 0xFF else 1
                    length = 0
                    while True:
                        b = body[i]; i += 1
                        length = (length << 7) | (b & 0x7F)
                        if not b & 0x80:
                            break
                    i += length
                    continue
                if b & 0x80:
                    status = b; i += 1
                kind = status & 0xF0
                if kind in (0xC0, 0xD0):
                    i += 1
                    continue
                d1, d2 = body[i], body[i + 1]; i += 2
                key = (status & 0x0F, d1)
                if kind == 0x90 and d2 > 0:
                    open_notes[key] = tick
                elif kind in (0x80, 0x90) and key in open_notes:
                    start = open_notes.pop(key)
                    notes.append((d1, start / float(ppq), (tick - start) / float(ppq)))
        return notes

    def piano_steps_from_midi(path):
        """Шаги партии: (позиция в шестнадцатых от первой, ноты от верхней к нижней)."""
        by_pos = {}
        for pitch, start, dur in piano_read_midi(path):
            pos = int(round(start * PIANO_SUBDIV))
            by_pos.setdefault(pos, []).append((pitch, max(1, int(round(dur * PIANO_SUBDIV)))))
        if not by_pos:
            return ()
        first = min(by_pos)
        steps = []
        for pos in sorted(by_pos):
            notes = []
            for pitch, dur in sorted(set(by_pos[pos]), reverse=True):
                notes.append((PIANO_NOTE_NAMES[pitch % 12], pitch // 12 - 1, dur))
            steps.append((pos - first, tuple(notes)))
        return tuple(steps)

    piano_steps_cache = {}
    piano_missing_files = set()

    def piano_log_missing(filename):
        if filename not in piano_missing_files:
            piano_missing_files.add(filename)
            renpy.log("minigame_piano: нет файла {}".format(filename))

    def piano_part_steps(part):
        if isinstance(part, str):
            if part not in piano_steps_cache:
                if renpy.loadable(part):
                    piano_steps_cache[part] = piano_steps_from_midi(part)
                else:
                    piano_log_missing(part)
                    piano_steps_cache[part] = ()
            return piano_steps_cache[part]
        return tuple(part)

init python:

    import time as piano_time
    import math as piano_math
    import pygame_sdl2 as piano_pygame

    def piano_channel_pos(handle):
        """Позиция звука пула; None — handle устарел или молчит. Тесты подменяют."""
        if handle is None:
            return None
        return sm_audio_get_pos(handle)

    class PianoMetronome(NoRollback):
        """Такт: щелчки в t0 + beat * (phase + k). Сцена запускает loop метронома длиной в целое
        число долей (start); sync() держит t0 у позиции этого звука по модулю доли, поэтому
        задержка старта и меню такт не сбивают. Объект не сохраняется: после загрузки его
        связывают заново (bind)."""

        def __init__(self):
            self.t0 = None
            self.beat = 2.0 / 3.0
            self.phase = 0.5
            self.handle = None
            self.synced = None

        def start(self, handle, beat, phase, now):
            self.bind(handle, beat, phase)
            self.t0 = now

        def bind(self, handle, beat, phase):
            if handle != self.handle or beat != self.beat or phase != self.phase:
                self.t0 = None
            self.handle, self.beat, self.phase = handle, beat, phase
            self.synced = None

        def sync(self, now):
            pos = piano_channel_pos(self.handle)
            if pos is None:
                return
            pos %= self.beat
            gain = 1.0 if self.synced is None else 1.0 - piano_math.exp(-(now - self.synced) / PIANO_SYNC_TAU)
            self.synced = now
            if self.t0 is None:
                self.t0 = now - pos
                return
            err = (now - pos - self.t0) % self.beat
            if err > self.beat / 2.0:
                err -= self.beat
            self.t0 += err * gain

        def since_click(self, now):
            """Время от последнего щелчка, с; без такта — 0."""
            if self.t0 is None:
                return 0.0
            return (now - self.t0 - self.phase * self.beat) % self.beat

    class PianoClock(NoRollback):
        """Время игры и физически зажатые клавиши; откат их не возвращает — шаг после отката
        снова ждёт у клавиш."""

        def __init__(self):
            self.due = None
            self.due_for = None
            self.flash = None
            self.flash_t = None
            self.held = set()
            self.done = {}
            self.started = None
            self.shards = ()
            self.key_shards = ()
            self.collapse_t = None
            ## (момент, px до линии у собранного шага, px скачка остальных).
            self.snap = (-10.0, 0.0, 0.0)

    piano_metro = PianoMetronome()
    piano_clock = PianoClock()

    def piano_now():
        return piano_time.perf_counter()

    def piano_step_t():
        return piano_metro.beat / PIANO_SUBDIV

    def piano_sync_tick():
        piano_metro.sync(piano_now())

    def piano_grid_after(t):
        """Ближайшая шестнадцатая метронома не раньше t; без такта — t."""
        m = piano_metro
        if m.t0 is None:
            return t
        step = piano_step_t()
        k = piano_math.ceil((t - m.t0 - m.phase * m.beat) / step - 1e-6)
        return m.t0 + m.phase * m.beat + k * step

    def piano_start(parts, metronome=None, beat=2.0 / 3.0, phase=0.5, on_step=None, break_before_end=0):
        parts = tuple(piano_part_steps(p) for p in parts)
        ## Метроном лежит в сохраняемом состоянии: после загрузки ядро связывает его заново.
        ## on_step — имя функции store (сцена реагирует на собранный шаг); имя, а не функция:
        ## состояние сохраняется.
        store.piano_state = {"parts": parts, "part": 0, "pos": 0, "pressed": (), "phase": "play",
            "results": (), "stumbles": 0, "on_step": on_step,
            "break_before_end": break_before_end,
            "metronome": metronome, "beat": beat, "metro_phase": phase}
        piano_clock.shards = ()
        piano_clock.key_shards = ()
        piano_clock.collapse_t = None
        piano_clock.snap = (-10.0, 0.0, 0.0)
        piano_clock.due = piano_clock.due_for = None
        piano_clock.done = {}
        piano_clock.started = piano_now()
        piano_bind_metronome()
        piano_metro.sync(piano_now())
        piano_skip_empty()

    def piano_bind_metronome():
        s = store.piano_state
        if s.get("metronome") is not None:
            piano_metro.bind(s["metronome"], s["beat"], s["metro_phase"])

    def piano_after_load():
        phase = store.piano_state.get("phase")
        if phase == "play":
            piano_bind_metronome()
            piano_clock.due = piano_clock.due_for = None
        ## Сейв в окне обрушения: часы не сохраняются, без момента старта слой и осколки
        ## делили бы None. Обрушение считается уже завершённым.
        elif phase == "collapse" and piano_clock.collapse_t is None:
            piano_clock.collapse_t = piano_now() - PIANO_COLLAPSE_T

    config.after_load_callbacks.append(piano_after_load)

    def piano_skip_empty():
        """Пустые партии (нет файла, нет нот) пропускаются."""
        s = store.piano_state
        while s["phase"] == "play" and not s["parts"][s["part"]]:
            piano_advance_part("empty")

    def piano_current():
        """(позиция, ноты) текущего шага; None — всё сыграно."""
        s = store.piano_state
        if s.get("phase") != "play":
            return None
        return s["parts"][s["part"]][s["pos"]]

    def piano_key_for(note, part):
        """Клавиша ноты: одна октава на экране, октава файла — из эталона."""
        return note[0], 0

    def piano_step_keys():
        """Клавиши текущего шага: {(имя, up): верхняя нота клавиши}."""
        s = store.piano_state
        cur = piano_current()
        if cur is None:
            return {}
        part = s["parts"][s["part"]]
        keys = {}
        for n in cur[1]:
            keys.setdefault(piano_key_for(n, part), n)
        return keys

    def piano_pending():
        """Клавиши шага, которые ещё не зажаты и не «залипли» кликом."""
        active = piano_clock.held | set(store.piano_state["pressed"])
        return {k: n for k, n in piano_step_keys().items() if k not in active}

    def piano_active():
        """Клавиши шага, которые сейчас держат (клавиатура) или «залипли» (клик)."""
        return set(store.piano_state.get("pressed", ())) | (piano_clock.held & set(piano_step_keys()))

    def piano_due():
        """Момент, когда текущий шаг доходит до клавиш; None — шаг уже ждёт у клавиш."""
        c = piano_clock
        if c.due_for != (store.piano_state["part"], store.piano_state["pos"]):
            return None
        return c.due

    def piano_key_file(name, octave):
        return PIANO_KEYS_DIR + name.replace("s", "#") + str(octave) + PIANO_KEYS_EXT

    def piano_play_file(filename):
        if renpy.loadable(filename):
            sm_audio_play(filename, overlap=True, volume=PIANO_KEY_VOLUME)
        else:
            piano_log_missing(filename)

    ## Промашки звучат на своих каналах вне пула эффектов: в пуле пять каналов, длинные ноты
    ## занимают их все, и щелчок отбирал бы канал у звучащей ноты.
    PIANO_MISS_CHANNELS = ("sm_piano_wood", "sm_piano_soft")
    for _piano_channel in PIANO_MISS_CHANNELS:
        renpy.music.register_channel(_piano_channel, mixer="sfx", loop=False, tight=True,
            synchro_start=False, stop_on_mute=False)
        config.main_menu_stop_channels.append(_piano_channel)

    def piano_play_miss(filename, channel):
        if renpy.loadable(filename):
            fnplay(filename, channel=channel, loop=False, fadein=0, fadeout=0)
        else:
            piano_log_missing(filename)

    def piano_miss_sound(key):
        """Промашка: деревянный щелчок и под ним призвук самой клавиши."""
        piano_play_miss(PIANO_DEAD_SOUND, PIANO_MISS_CHANNELS[0])
        soft = PIANO_SOFT_DIR + key[0].replace("s", "#") + PIANO_KEYS_EXT
        if renpy.loadable(soft):
            piano_play_miss(soft, PIANO_MISS_CHANNELS[1])

    def piano_key_down(key, now=None):
        """Клавиша зажата: "miss" — не из шага (холостой щелчок), "step" — шаг собран, None — ждём остальные."""
        s = store.piano_state
        now = piano_now() if now is None else now
        if piano_current() is None:
            return None
        piano_clock.flash, piano_clock.flash_t = key, now
        if key not in piano_step_keys():
            s["stumbles"] += 1
            piano_miss_sound(key)
            return "miss"
        piano_clock.held.add(key)
        return "step" if not piano_pending() else None

    def piano_key_up(key):
        piano_clock.held.discard(key)

    def piano_latch(key, now=None):
        """Клик мышью «залипает» на клавише шага до его сбора; чужая клавиша — холостой щелчок."""
        s = store.piano_state
        now = piano_now() if now is None else now
        if piano_current() is None:
            return None
        piano_clock.flash, piano_clock.flash_t = key, now
        if key not in piano_step_keys():
            s["stumbles"] += 1
            piano_miss_sound(key)
            return "miss"
        if key not in s["pressed"]:
            s["pressed"] += (key,)
        return "step" if not piano_pending() else None

    def piano_complete_step(now=None):
        """Все клавиши шага зажаты: его ноты звучат вместе, следующий шаг подступает от доли нажатия."""
        s = store.piano_state
        now = piano_now() if now is None else now
        cur = piano_current()
        if cur is None:
            return
        piano_metro.sync(now)
        ## Сколько бруску оставалось до линии: нажали раньше, чем он доехал.
        due = piano_due()
        early_px = 0.0 if due is None else max(0.0, due - now) / piano_metro.beat * PIANO_PX_PER_BEAT
        part = s["parts"][s["part"]]
        breaking = piano_breaks_here(s, part, s["pos"] + 1)
        if not breaking:
            for name, octave, dur in cur[1]:
                piano_play_file(piano_key_file(name, octave))
        ## Собранный шаг отпускает клавиши: следующий шаг ждёт свежего нажатия.
        piano_clock.held.clear()
        s["pressed"] = ()
        piano_clock.done[(s["part"], s["pos"])] = now
        if s.get("on_step"):
            getattr(store, s["on_step"])(s["part"], s["pos"])
        if s["pos"] + 1 < len(part):
            gap = part[s["pos"] + 1][0] - cur[0]
            s["pos"] += 1
            piano_clock.due = piano_grid_after(now - PIANO_WINDOW) + gap * piano_step_t()
            piano_clock.due_for = (s["part"], s["pos"])
            ## Остальные бруски сдвинулись на разницу старого и нового места следующего шага.
            new_px = max(0.0, piano_clock.due - now) / piano_metro.beat * PIANO_PX_PER_BEAT
            piano_clock.snap = (now, early_px, gap * piano_px_step() + early_px - new_px)
            if breaking:
                piano_collapse(now)
        else:
            piano_advance_part("played")

    def piano_snap_offsets(now):
        """(px вверх для собранного шага, px вверх для остальных): скачок раннего нажатия тает."""
        t0, done_px, next_px = piano_clock.snap
        k = (now - t0) / PIANO_SNAP_T
        if k < 0.0 or k >= 1.0:
            return 0.0, 0.0
        f = (1.0 - k) * (1.0 - k)
        return done_px * f, next_px * f

    def piano_breaks_here(s, part, pos):
        """Последняя партия на шаге pos дошла до шагов, которые не доигрываются."""
        return s["part"] + 1 == len(s["parts"]) and pos + s["break_before_end"] >= len(part)

    def piano_px_step():
        return PIANO_PX_PER_BEAT / float(PIANO_SUBDIV)

    def piano_columns():
        return {(name, up): (kx, kw, black) for name, up, label, kx, ky, kw, kh, black in piano_key_geometry()}

    def piano_step_bars(part, notes):
        """[(клавиша, высота бруска)] шага; ноты одной клавиши — один брусок по самой длинной."""
        by_key = {}
        for note in notes:
            key = piano_key_for(note, part)
            if key not in by_key or note[2] > by_key[key][2]:
                by_key[key] = note
        return [(key, max(PIANO_BAR_MIN_H, int(note[2] * piano_px_step()) - 4)) for key, note in by_key.items()]

    def piano_step_bottom(pos, cur_pos, lead):
        """Низ бруска шага pos, когда текущий шаг cur_pos ждёт lead секунд до своей доли."""
        return PIANO_KB_Y - (pos - cur_pos) * piano_px_step() - lead / piano_metro.beat * PIANO_PX_PER_BEAT

    def piano_shard_heights(h):
        n = max(1, min(PIANO_SHARDS, h // PIANO_BAR_MIN_H))
        piece = h // n
        return [piece] * (n - 1) + [h - piece * (n - 1)]

    def piano_key_shards():
        """Клавиши трескаются поперёк на PIANO_KEY_SHARDS кусков; белые раньше — чёрные поверх."""
        out = []
        for name, up, label, kx, ky, kw, kh, black in piano_key_geometry():
            piece = kh // PIANO_KEY_SHARDS
            for i in range(PIANO_KEY_SHARDS):
                ph = piece if i + 1 < PIANO_KEY_SHARDS else kh - piece * i
                side = 1.0 if renpy.random.random() < 0.5 else -1.0
                out.append(("black" if black else "white", kx, ky + piece * i, kw, ph,
                    side * renpy.random.uniform(*PIANO_KEY_SHARD_VX), renpy.random.uniform(*PIANO_KEY_SHARD_VY),
                    side * renpy.random.uniform(*PIANO_KEY_SHARD_SPIN), renpy.random.uniform(*PIANO_KEY_SHARD_DELAY)))
        return tuple(out)

    def piano_collapse(now):
        """Только что нажатые и оставшиеся видимые ноты разлетаются осколками с их текущих мест."""
        s = store.piano_state
        part = s["parts"][s["part"]]
        columns = piano_columns()
        due = piano_due()
        lead = 0.0 if due is None else max(0.0, due - now)
        cur_pos = part[s["pos"]][0]
        shards = []
        for k in range(max(0, s["pos"] - 1), len(part)):
            pos, notes = part[k]
            bottom = int(PIANO_KB_Y if k < s["pos"] else piano_step_bottom(pos, cur_pos, lead))
            for key, h in piano_step_bars(part, notes):
                kx, kw, black = columns[key]
                top = max(PIANO_FALL_TOP, bottom - h)
                y = top
                for ph in piano_shard_heights(bottom - top) if top < bottom else ():
                    side = 1.0 if renpy.random.random() < 0.5 else -1.0
                    shards.append((black, kx + PIANO_BAR_INSET // 2, y, kw - PIANO_BAR_INSET, ph,
                        side * renpy.random.uniform(*PIANO_SHARD_VX), renpy.random.uniform(*PIANO_SHARD_VY),
                        side * renpy.random.uniform(*PIANO_SHARD_SPIN)))
                    y += ph
        piano_clock.shards = tuple(shards)
        piano_clock.key_shards = piano_key_shards()
        piano_clock.collapse_t = now
        s["phase"] = "collapse"
        s["results"] += ("broken",)

    def piano_advance_part(result):
        s = store.piano_state
        s["results"] += (result,)
        s["pos"] = 0
        s["pressed"] = ()
        if s["part"] + 1 >= len(s["parts"]):
            s["phase"] = "done"
        else:
            s["part"] += 1
        piano_clock.due = piano_clock.due_for = None

    def piano_outcome():
        return "clean" if store.piano_state["stumbles"] == 0 else "flawed"

    def piano_finish_skipped():
        s = store.piano_state
        while s["phase"] == "play":
            piano_advance_part("skipped")

    def piano_collapse_done():
        store.piano_state["phase"] = "done"

    def piano_collapse_end():
        """Сцена досмотрела обрушение: состояние игры больше не нужно."""
        store.piano_state = {}

    def piano_fade_in_f(trans, st, at):
        """Слой мини-игры проявляется при старте; при обрушении гаснет вместе с осколками."""
        if store.piano_state.get("phase") == "collapse":
            left = PIANO_COLLAPSE_T - (piano_now() - piano_clock.collapse_t)
            trans.alpha = min(1.0, max(0.0, left / PIANO_COLLAPSE_FADE_T))
            return 0
        if piano_clock.started is None:
            trans.alpha = 1.0
            return None
        k = (piano_now() - piano_clock.started) / PIANO_FADE_IN_T
        trans.alpha = min(1.0, k)
        return 0 if k < 1.0 else None

    def piano_hint_f(trans, st, at):
        """Подсказка гаснет от момента сбора последнего «учебного» шага; st не годится:
        каждое нажатие — новая интеракция."""
        s = store.piano_state
        done_t = piano_clock.done.get((s.get("part", 0), PIANO_HINT_STEPS - 1))
        if done_t is None:
            trans.alpha = 1.0
            return 0.1
        trans.alpha = max(0.0, 1.0 - (piano_now() - done_t) / PIANO_HINT_FADE_T)
        return 0

    def piano_pulse_f(trans, st, at):
        """Подсветка нужных клавиш вспыхивает на каждом щелчке метронома; без мигания — ровная."""
        if sm_flashes_disabled() or sm_reduced_motion():
            trans.alpha = 1.0
            return 0
        t = piano_metro.since_click(piano_now())
        trans.alpha = PIANO_PULSE_LOW + (1.0 - PIANO_PULSE_LOW) * max(0.0, 1.0 - t / PIANO_PULSE_T)
        return 0

    class PianoKeyInput(renpy.Displayable):
        """Физические клавиши: скан-код не зависит от раскладки; без него — по символу.
        Зажатие и отпускание ведут модель; call screen завершают только холостой щелчок и
        собранный шаг. Хоткеи движка на этих буквах (h, s, v) не доходят."""

        MODS = piano_pygame.KMOD_ALT | piano_pygame.KMOD_CTRL | piano_pygame.KMOD_GUI

        def __init__(self, **properties):
            super(PianoKeyInput, self).__init__(**properties)
            self.by_scancode = {sc: (name, up) for name, up, label, sc in PIANO_KEYS}
            self.by_key = {getattr(piano_pygame, "K_COMMA" if label == "," else "K_" + label): (name, up)
                for name, up, label, sc in PIANO_KEYS}

        def render(self, width, height, st, at):
            return renpy.Render(1, 1)

        def key_of(self, ev):
            hit = self.by_scancode.get(getattr(ev, "scancode", None))
            return hit if hit is not None else self.by_key.get(ev.key)

        def event(self, ev, x, y, st):
            if store.piano_state.get("phase") != "play":
                ## Обрушение: клавиши пианино молчат, но до хоткеев движка не доходят.
                if ev.type in (piano_pygame.KEYDOWN, piano_pygame.KEYUP) and self.key_of(ev) is not None:
                    raise renpy.IgnoreEvent()
                return None
            if ev.type == piano_pygame.KEYUP:
                key = self.key_of(ev)
                if key is not None:
                    piano_key_up(key)
                    renpy.restart_interaction()
                    raise renpy.IgnoreEvent()
                return None
            if ev.type != piano_pygame.KEYDOWN or getattr(ev, "repeat", False) or (getattr(ev, "mod", 0) & self.MODS):
                return None
            key = self.key_of(ev)
            if key is None:
                return None
            verdict = piano_key_down(key)
            if verdict is None:
                ## Клавиша зажата, шаг ещё не собран: экран перестраивается, ожидание продолжается.
                ## Событие поглощается — иначе s и h дошли бы до хоткеев движка (скриншот, спрятать окна).
                renpy.restart_interaction()
                raise renpy.IgnoreEvent()
            return (verdict, key)

    def piano_key_geometry():
        """[(имя, up, буква, x, y, w, h, чёрная)] — белые первыми, чёрные поверх."""
        white = [k for k in PIANO_KEYS if len(k[0]) == 1]
        black = [k for k in PIANO_KEYS if len(k[0]) == 2]
        out = []
        for i, (name, up, label, sc) in enumerate(white):
            out.append((name, up, label, PIANO_KB_X + i * (PIANO_WHITE_W + PIANO_WHITE_GAP), PIANO_KB_Y,
                PIANO_WHITE_W, PIANO_WHITE_H, False))
        for (name, up, label, sc), slot in zip(black, PIANO_BLACK_SLOTS):
            x = PIANO_KB_X + (slot + 1) * (PIANO_WHITE_W + PIANO_WHITE_GAP) - PIANO_WHITE_GAP // 2 - PIANO_BLACK_W // 2
            out.append((name, up, label, x, PIANO_KB_Y, PIANO_BLACK_W, PIANO_BLACK_H, True))
        return out

    def piano_bar(black, w, h, done):
        """Брусок ноты: контур с затемнением (чёрная клавиша) или штриховкой (белая); края
        рвёт скратч-шейдер. Размеры — целые px, набор небольшой — кэш по ключу."""
        key = (black, w, h, done)
        if key not in piano_bar_cache:
            b = PIANO_BAR_BORDER
            edge = PIANO_COLORS["bar_done" if done else "bar_edge"]
            inner = (w - 2 * b, h - 2 * b)
            if black or done:
                fill = Solid(PIANO_COLORS["bar_dark"], xysize=inner)
            else:
                fill = Transform(Solid("#ffffff", xysize=inner), mesh=True, shader="sm.piano_hatch",
                    u_hatch_period=PIANO_HATCH_PERIOD, u_hatch_thick=PIANO_HATCH_THICK,
                    u_hatch_color=Color(PIANO_COLORS["bar_hatch"]).rgba)
            ## Рамка — плашка цвета контура, внутри — прозрачный вырез, поверх него заливка.
            frame = Fixed(
                Solid(edge, xysize=(w, h)),
                Transform(Solid("#00000000", xysize=inner), xpos=b, ypos=b),
                Transform(fill, xpos=b, ypos=b),
                xysize=(w, h))
            ## Контур — четыре полосы: сплошная подложка закрасила бы просвет штриховки.
            if not black and not done:
                o = PIANO_BAR_OUTLINE
                c = PIANO_COLORS["bar_outline"]
                frame = Fixed(
                    Solid(c, xysize=(w + 2 * o, o)),
                    Solid(c, ypos=h + o, xysize=(w + 2 * o, o)),
                    Solid(c, ypos=o, xysize=(o, h)),
                    Solid(c, xpos=w + o, ypos=o, xysize=(o, h)),
                    Transform(frame, pos=(o, o)),
                    xysize=(w + 2 * o, h + 2 * o))
            piano_bar_cache[key] = At(frame, scratch("piano_notes", tint=0.0, pad=PIANO_BAR_PAD))
        return piano_bar_cache[key]

    piano_bar_cache = {}

    piano_key_cache = {}

    def piano_key_face(color, w, h):
        """Плашка клавиши с рваным краем (группа piano_keys); кэш по цвету и размеру."""
        key = (color, w, h)
        if key not in piano_key_cache:
            piano_key_cache[key] = At(Solid(PIANO_COLORS[color], xysize=(w, h)), scratch("piano_keys", tint=0.0, pad=PIANO_KEY_PAD))
        return piano_key_cache[key]

    class PianoFall(renpy.Displayable):
        """Ноты партии над клавиатурой: столбец — клавиша, низ бруска касается линии клавиш
        в момент своего шага, высота — длительность, подпись — буква клавиши. Текущий шаг стоит
        у линии, пока не собран. Только читает модель."""

        def __init__(self, **properties):
            super(PianoFall, self).__init__(**properties)
            self.columns = piano_columns()
            ## На бруске — буква клавиши, не нота: игроку важно, что нажать.
            self.labels = {(name, up): Text(label.upper(), size=PIANO_BAR_LABEL_SIZE,
                    color=PIANO_COLORS["bar_label_black" if black else "bar_label_white"], font="fonts/oswald_regular.ttf")
                for name, up, label, kx, ky, kw, kh, black in piano_key_geometry()}

        def render(self, width, height, st, at):
            rv = renpy.Render(config.screen_width, config.screen_height)
            s = store.piano_state
            now = piano_now()
            if s.get("phase") == "collapse":
                ## Сыгранные раньше предпоследнего шага бруски догорают как обычно.
                self._draw_done(rv, s, s["pos"] - 2, now, st, at, width, height)
                self._draw_shards(rv, now, st, at, width, height)
                renpy.redraw(self, 0)
                return rv
            cur = piano_current()
            if cur is None:
                return rv
            due = piano_due()
            ## Шаг у линии ждёт: время не идёт вперёд линии.
            lead = 0.0 if due is None else max(0.0, due - now)
            part = s["parts"][s["part"]]
            line = renpy.render(Solid(PIANO_COLORS["line"], xysize=((PIANO_WHITE_W + PIANO_WHITE_GAP) * 7 - PIANO_WHITE_GAP, 2)), width, height, st, at)
            rv.blit(line, (PIANO_KB_X, PIANO_KB_Y - 1))
            self._draw_done(rv, s, s["pos"] - 1, now, st, at, width, height)
            snap_next = piano_snap_offsets(now)[1]
            for k in range(s["pos"], len(part)):
                pos, notes = part[k]
                bottom = piano_step_bottom(pos, cur[0], lead) - snap_next
                if bottom < PIANO_FALL_TOP:
                    break
                self._draw_step(rv, part, notes, bottom, piano_active() if k == s["pos"] else set(), st, at, width, height, 1.0)
            renpy.redraw(self, 0)
            return rv

        def _draw_done(self, rv, s, last, now, st, at, width, height):
            """Сыгранные шаги (с last назад) продолжают ехать вниз за клавиши и гаснут."""
            part = s["parts"][s["part"]]
            for k in range(last, -1, -1):
                done_t = piano_clock.done.get((s["part"], k))
                if done_t is None or now - done_t > PIANO_BAR_FADE_T:
                    break
                age = now - done_t
                fade = 1.0 - age / PIANO_BAR_FADE_T
                bottom = PIANO_KB_Y + age / piano_metro.beat * PIANO_PX_PER_BEAT
                if k == last:
                    bottom -= piano_snap_offsets(now)[0]
                self._draw_step(rv, part, part[k][1], bottom, set(), st, at, width, height, fade)

        def _draw_shards(self, rv, now, st, at, width, height):
            ## Без движения осколки остаются на месте и гаснут вместе со слоем.
            t = (now - piano_clock.collapse_t) * sm_motion_scale()
            ## Клавиши под нотами: до своей задержки лежат на месте.
            for base, x0, y0, w, h, vx, vy, spin, delay in piano_clock.key_shards:
                k = max(0.0, t - delay)
                x = x0 + vx * k
                y = y0 + vy * k + 0.5 * PIANO_GRAVITY * k * k
                if y > config.screen_height:
                    continue
                r = renpy.render(Transform(piano_key_face(base, w, h), rotate=spin * k), width, height, st, at)
                rw, rh = r.get_size()
                rv.blit(r, (int(x + w / 2.0 - rw / 2.0), int(y + h / 2.0 - rh / 2.0)))
            for black, x0, y0, w, h, vx, vy, spin in piano_clock.shards:
                x = x0 + vx * t
                y = y0 + vy * t + 0.5 * PIANO_GRAVITY * t * t
                if y > config.screen_height:
                    continue
                d = Transform(piano_bar(black, w, h, False), rotate=spin * t)
                r = renpy.render(d, width, height, st, at)
                rw, rh = r.get_size()
                rv.blit(r, (int(x + w / 2.0 - rw / 2.0), int(y + h / 2.0 - rh / 2.0)))

        def _draw_step(self, rv, part, notes, bottom, active, st, at, width, height, fade):
            ## Бруски чёрных клавиш — поверх белых, как сами клавиши.
            for key, h in sorted(piano_step_bars(part, notes), key=lambda kb: self.columns[kb[0]][2]):
                kx, kw, black = self.columns[key]
                top = max(PIANO_FALL_TOP, int(bottom) - h)
                if top >= int(bottom):
                    continue
                done = key in active
                bw0, bh0 = kw - PIANO_BAR_INSET, int(bottom) - top
                d = piano_bar(black, bw0, bh0, done)
                if fade < 1.0:
                    d = Transform(d, alpha=fade)
                bar = renpy.render(d, width, height, st, at)
                ## Скратч расширяет текстуру на pad с каждой стороны.
                bw, bh = bar.get_size()
                rv.blit(bar, (kx + PIANO_BAR_INSET // 2 - (bw - bw0) // 2, top - (bh - bh0) // 2))
                if fade < 1.0:
                    continue
                label = renpy.render(self.labels[key], width, height, st, at)
                lw, lh = label.get_size()
                if lh + 4 <= bh0:
                    rv.blit(label, (kx + kw // 2 - lw // 2, int(bottom) - lh - 4))

transform piano_pulse():
    function piano_pulse_f

transform piano_hint_fade():
    function piano_hint_f

transform piano_fade_in():
    function piano_fade_in_f

## Нажатая клавиша темнеет и отпускается; новая интеракция после нажатия перезапускает st.
transform piano_key_flash():
    alpha 1.0
    linear PIANO_FLASH_T alpha 0.0

## Шрифт кнопок выбора в сценах (glow_button).
style piano_key_label is gui_text:
    font gui.main_menu_font
    size PIANO_KEY_LABEL_SIZE
    textalign 0.5

style piano_hint is gui_text:
    font gui.main_menu_font
    size 26
    color "#d9d3c8"
    outlines [(2, "#1a1712d9", 0, 0)]
    xalign 0.5
    textalign 0.5

## Контрольная точка на каждое нажатие: откат колесом отменяет одну клавишу, как у меню.
screen minigame_piano_screen(skippable=True):
    zorder PIANO_ZORDER
    ## При обрушении экран — только картинка: сцена ведёт время своими pause.
    modal (piano_state.get("phase") == "play")
    roll_forward True

    if skippable:
        use sm_skippable_interaction

    add PianoKeyInput()
    timer PIANO_SYNC_T repeat True modal True action Function(piano_sync_tick, _update_screens=False)

    ## После пропуска игры состояние пустое: экран обрушения ничего не рисует.
    $ playing = piano_state.get("phase") == "play"
    $ pending = piano_pending() if playing else {}
    $ active = piano_active() if playing else set()
    $ flash = piano_clock.flash if piano_clock.flash_t is not None and piano_now() - piano_clock.flash_t < PIANO_FLASH_T else None

    fixed:
        at piano_fade_in
        xysize (config.screen_width, config.screen_height)

        add PianoFall() alt _("Ноты опускаются к клавишам")

        ## При обрушении клавиши рисует PianoFall — кусками на тех же местах.
        for name, up, label, kx, ky, kw, kh, black in (piano_key_geometry() if playing else ()):
            $ base = "black" if black else "white"
            button:
                pos (kx, ky)
                xysize (kw, kh)
                background piano_key_face(base, kw, kh)
                hover_background piano_key_face(base + "_hover", kw, kh)
                ## alt читается озвучкой вне экрана: подстановка сразу, без [label].
                alt (renpy.substitute(_("[label] — нажать"), {"label": label.upper()}) if (name, up) in pending else label.upper())
                sensitive (piano_state.get("phase") == "play")
                action Return(("latch", (name, up)))
                if (name, up) in active:
                    add piano_key_face(base + "_down", kw, kh)
                elif flash == (name, up):
                    add piano_key_face(base + "_down", kw, kh) at piano_key_flash
                if (name, up) in pending:
                    add piano_key_face(base + "_next", kw, kh) at piano_pulse
                text label.upper() style "piano_key_label" color PIANO_COLORS[base + "_label"] align (0.5, 0.9)

        if playing and piano_state.get("part") == 0 and piano_state.get("pos", 0) <= PIANO_HINT_STEPS:
            text _("НАЖИМАЙ ПОДСВЕЧЕННЫЕ КЛАВИШИ") style "piano_hint" ypos ((PIANO_KB_Y + PIANO_WHITE_H + config.screen_height) // 2) yanchor 0.5 at piano_hint_fade

## Вызов: call minigame_piano(партии, metronome=handle loop-канала, beat=, phase=, on_step=имя
## функции store(part, pos) на собранный шаг, break_before_end=сколько последних шагов ломается)
## → _return = "clean" / "flawed" / "skipped". Исход в сюжет не идёт: мини-игра пропускается
## вместе со сценой. С break_before_end после возврата сцена показывает обрушение (см. шапку).
label minigame_piano(piano_parts, piano_metronome=None, piano_beat=2.0 / 3.0, piano_phase=0.5, piano_on_step=None, piano_break=0, piano_skippable=True) hide:
    if piano_skippable and renpy.is_skipping():
        return "skipped"
    $ piano_start(piano_parts, piano_metronome, piano_beat, piano_phase, piano_on_step, piano_break)
    $ piano_clock.held.clear()
    while piano_state["phase"] == "play":
        call screen minigame_piano_screen(piano_skippable)
        ## SkipOnce позднего пропуска завершает экран значением True.
        if _return is True:
            $ piano_finish_skipped()
            $ piano_state = {}
            return "skipped"
        ## ("latch", клавиша) — клик; ("step", клавиша) — клавиатура собрала шаг; "miss" уже озвучен.
        if _return[0] == "latch":
            $ piano_latch_result = piano_latch(_return[1])
        else:
            $ piano_latch_result = _return[0]
        if piano_latch_result == "step":
            $ piano_complete_step()
    $ piano_result = piano_outcome()
    ## Обрушение досматривает сцена: состояние нужно осколкам.
    if piano_state["phase"] != "collapse":
        $ piano_state = {}
    return piano_result

