init python:

    ## Подмена позиции канала: {handle: pos}; отсутствующий — None, как молчащий канал.
    ## Возвращает прежнюю функцию — вернуть её в finally.
    def sm_test_piano_fake_pos(table):
        original = store.piano_channel_pos
        store.sm_test_piano_pos_table = table
        store.piano_channel_pos = lambda handle: store.sm_test_piano_pos_table.get(handle)
        return original

    ## Короткая партия для модели: шаги по две ноты (мелодия + бас) на долях 0, 1 и 3;
    ## в последнем обе ноты на одних клавишах (C6+C4? нет: C6 и A3 — разные), плюс шаг с двумя F#.
    SM_TEST_PIANO_PART = (
        (0, (("b", 5, 4), ("e", 4, 4))),
        (4, (("a", 5, 4), ("c", 4, 4))),
        (12, (("c", 6, 4), ("a", 3, 4))),
    )
    SM_TEST_PIANO_SAME_KEY = ((0, (("fs", 4, 4), ("fs", 3, 4))),)

    def sm_test_piano_count_play(filename):
        store.sm_test_piano_played += 1

    def sm_test_piano_begin():
        """Игра на синтетическом такте (t0 = 0, 90 BPM) без звука; возвращает синтетическое now."""
        piano_metro.bind(None, 2.0 / 3.0, 0.5)
        piano_metro.t0 = 0.0
        piano_start((SM_TEST_PIANO_PART, SM_TEST_PIANO_PART))
        return 100.0

    class SmTestPianoEvent(object):
        def __init__(self, **kw):
            self.__dict__.update(kw)

    def sm_test_piano_cdd_event(cdd, base, **kw):
        """Событие в CDD; поглощённое (IgnoreEvent) — "eaten"."""
        try:
            return cdd.event(SmTestPianoEvent(**dict(base, **kw)), 0, 0, 0)
        except renpy.IgnoreEvent:
            return "eaten"

    def sm_test_piano_key_xy(key):
        """Точка клика по клавише (имя, up) — низ клавиши, где нет чёрных."""
        for name, up, label, kx, ky, kw, kh, black in piano_key_geometry():
            if (name, up) == key:
                return (kx + kw // 2, ky + kh - 20)

    def sm_test_piano_next_xy():
        return sm_test_piano_key_xy(sorted(piano_pending())[0])

    def sm_test_piano_wrong_xy():
        pending = piano_pending()
        for name, up, label, kx, ky, kw, kh, black in piano_key_geometry():
            if (name, up) not in pending:
                return (kx + kw // 2, ky + kh - 20)


label sm_test_piano hide:
    $ piano_metro.t0 = None
    $ piano_metro.handle = None
    call chapter_1_scene_1_minigame_piano from _call_sm_test_piano
    if piano_state.get("phase") == "collapse":
        show screen minigame_piano_screen
        pause PIANO_COLLAPSE_T
        hide screen minigame_piano_screen
    $ piano_collapse_end()
    $ skip_stop()
    call screen sm_test_piano_finished
    return

screen sm_test_piano_finished():
    modal True
    null


testcase c1s1_piano_midi_parts:
    ## Эталон читается: шаги по возрастанию от нуля, ноты — имя, октава, длительность ≥ 1.
    python:
        store.sm_test_piano_midi_ok = True
        for path in C1S1_PIANO_PARTS:
            part = piano_part_steps(path)
            if not part or part[0][0] != 0:
                store.sm_test_piano_midi_ok = False
            if [p for p, notes in part] != sorted(set(p for p, notes in part)):
                store.sm_test_piano_midi_ok = False
            for pos, notes in part:
                if not notes or len(set(notes)) != len(notes):
                    store.sm_test_piano_midi_ok = False
                for name, octave, dur in notes:
                    if name not in PIANO_NOTE_NAMES or not (0 <= octave <= 8) or dur < 1:
                        store.sm_test_piano_midi_ok = False
    assert eval (sm_test_piano_midi_ok)

testcase c1s1_piano_key_samples:
    ## У каждой ноты эталона есть сэмпл клавиши; холостой щелчок — на месте.
    python:
        store.sm_test_piano_missing = []
        for path in C1S1_PIANO_PARTS:
            for pos, notes in piano_part_steps(path):
                for name, octave, dur in notes:
                    if not renpy.loadable(piano_key_file(name, octave)):
                        store.sm_test_piano_missing.append(piano_key_file(name, octave))
        if not renpy.loadable(PIANO_DEAD_SOUND):
            store.sm_test_piano_missing.append(PIANO_DEAD_SOUND)
        store.sm_test_piano_missing = sorted(set(store.sm_test_piano_missing))
    assert eval (sm_test_piano_missing == [])

testcase c1s1_piano_steps:
    $ persistent.sm_simplified_locks = False
    python:
        original = sm_test_piano_fake_pos({})
        try:
            now = sm_test_piano_begin()
            store.sm_test_piano_v = []
            ## Первый шаг ждёт у клавиш (due нет); шаг собирается, только когда зажаты обе клавиши.
            store.sm_test_piano_first_due = piano_due()
            store.sm_test_piano_pending0 = sorted(piano_pending())
            store.sm_test_piano_v.append(piano_key_down(("e", 0), now=now + 3.0))
            store.sm_test_piano_v.append(piano_key_down(("f", 0), now=now + 3.1))
            ## Отпустил e, зажал b — шаг не собран: e уже не держат.
            piano_key_up(("e", 0))
            store.sm_test_piano_v.append(piano_key_down(("b", 0), now=now + 3.2))
            store.sm_test_piano_v.append(piano_key_down(("e", 0), now=now + 3.3))
            piano_complete_step(now=now + 3.3)
            store.sm_test_piano_held_after = set(piano_clock.held)
            ## Следующий шаг подступает через свой промежуток от доли нажатия.
            store.sm_test_piano_gap = piano_clock.due - piano_grid_after(now + 3.3 - PIANO_WINDOW)
            ## Клик мышью «залипает»: a кликом, c с клавиатуры — шаг собран.
            store.sm_test_piano_v.append(piano_latch(("a", 0), now=piano_clock.due))
            store.sm_test_piano_v.append(piano_key_down(("c", 0), now=piano_clock.due))
            piano_complete_step(now=piano_clock.due)
            ## C6 и A3 — те же клавиши z и n, октава берётся из эталона.
            store.sm_test_piano_pending2 = sorted(piano_pending())
            store.sm_test_piano_v.append(piano_key_down(("c", 0), now=piano_clock.due + 9.0))
            store.sm_test_piano_v.append(piano_key_down(("a", 0), now=piano_clock.due + 9.5))
            piano_complete_step(now=piano_clock.due + 9.5)
            store.sm_test_piano_after = (piano_state["part"], piano_state["pos"], piano_state["results"], piano_state["stumbles"])
            store.sm_test_piano_outcome = piano_outcome()
        finally:
            store.piano_channel_pos = original
            piano_clock.held.clear()
    assert eval (sm_test_piano_first_due is None)
    assert eval (sm_test_piano_pending0 == [("b", 0), ("e", 0)])
    assert eval (sm_test_piano_v == [None, "miss", None, "step", None, "step", None, "step"])
    assert eval (sm_test_piano_held_after == set())
    assert eval (abs(sm_test_piano_gap - 4 * piano_step_t()) < 1e-6)
    assert eval (sm_test_piano_pending2 == [("a", 0), ("c", 0)])
    assert eval (sm_test_piano_after == (1, 0, ("played",), 1))
    assert eval (sm_test_piano_outcome == "flawed")

testcase c1s1_piano_same_key_step:
    ## Две ноты одного имени в шаге — одна клавиша, шаг собирается одним нажатием.
    python:
        original = sm_test_piano_fake_pos({})
        try:
            piano_metro.bind(None, 2.0 / 3.0, 0.5)
            piano_metro.t0 = 0.0
            piano_start((SM_TEST_PIANO_SAME_KEY,))
            store.sm_test_piano_keys = sorted(piano_step_keys())
            store.sm_test_piano_v = piano_key_down(("fs", 0), now=100.0)
            piano_complete_step(now=100.0)
            store.sm_test_piano_done = piano_state["phase"]
        finally:
            store.piano_channel_pos = original
            piano_clock.held.clear()
    assert eval (sm_test_piano_keys == [("fs", 0)])
    assert eval (sm_test_piano_v == "step" and sm_test_piano_done == "done")

testcase c1s1_piano_collapse:
    ## break_before_end=1: сбор предпоследнего шага не звучит, ломает последний — осколки,
    ## фаза collapse, конец.
    python:
        original = sm_test_piano_fake_pos({})
        original_play = store.piano_play_file
        store.piano_play_file = sm_test_piano_count_play
        store.sm_test_piano_played_steps = ()
        try:
            piano_metro.bind(None, 2.0 / 3.0, 0.5)
            piano_metro.t0 = 0.0
            piano_start((SM_TEST_PIANO_PART,), break_before_end=1)
            now = 100.0
            for step in range(2):
                store.sm_test_piano_played = 0
                for key in sorted(piano_pending()):
                    piano_key_down(key, now=now)
                piano_complete_step(now=now)
                store.sm_test_piano_played_steps += (store.sm_test_piano_played,)
                now += 1.0
            store.sm_test_piano_phase = piano_state["phase"]
            store.sm_test_piano_shards = len(piano_clock.shards)
            store.sm_test_piano_thin = sum(1 for sh in piano_clock.shards if sh[4] < PIANO_BAR_MIN_H)
            store.sm_test_piano_key_shards = len(piano_clock.key_shards)
            store.sm_test_piano_pend = piano_pending()
            piano_collapse_done()
            store.sm_test_piano_results = piano_state["results"]
        finally:
            store.piano_channel_pos = original
            store.piano_play_file = original_play
            piano_clock.held.clear()
    assert eval (sm_test_piano_phase == "collapse")
    ## Первый шаг звучит (2 ноты), ломающий — молчит.
    assert eval (sm_test_piano_played_steps == (2, 0))
    ## Осколки: по 2 бруска у предпоследнего и последнего шагов, каждый брусок — PIANO_SHARDS
    ## кусков не тоньше минимума.
    assert eval (sm_test_piano_shards == 4 * PIANO_SHARDS and sm_test_piano_thin == 0)
    ## Клавиатура ломается целиком: каждая клавиша — PIANO_KEY_SHARDS кусков.
    assert eval (sm_test_piano_key_shards == len(PIANO_KEYS) * PIANO_KEY_SHARDS)
    assert eval (sm_test_piano_pend == {})
    assert eval (sm_test_piano_results == ("broken",) and piano_state["phase"] == "done")

testcase c1s1_piano_screen_collapse:
    ## Эталон c1s1 ломается на предпоследнем шаге; обрушение — не контрольная точка: откат
    ## возвращает к предпоследнему шагу, повтор доводит до конца с чистым исходом.
    $ persistent.sm_simplified_locks = False
    run Start("sm_test_piano")
    assert screen "minigame_piano_screen" timeout 3.0
    click pos sm_test_piano_next_xy()
    assert eval (piano_state["pos"] == 1) timeout 2.0
    click pos sm_test_piano_next_xy()
    assert eval (piano_state["pos"] == 2) timeout 2.0
    click pos sm_test_piano_next_xy()
    assert eval (piano_state["pos"] == 3) timeout 2.0
    click pos sm_test_piano_next_xy()
    assert eval (piano_state["pos"] == 4) timeout 2.0
    click pos sm_test_piano_next_xy()
    assert eval (len(piano_state["pressed"]) == 1) timeout 2.0
    click pos sm_test_piano_next_xy()
    assert eval (piano_state["pos"] == 5) timeout 2.0
    click pos sm_test_piano_next_xy()
    assert eval (len(piano_state["pressed"]) == 1) timeout 2.0
    click pos sm_test_piano_next_xy()
    assert eval (piano_state["pos"] == 6) timeout 2.0
    click pos sm_test_piano_next_xy()
    assert eval (len(piano_state["pressed"]) == 1) timeout 2.0
    click pos sm_test_piano_next_xy()
    assert eval (piano_state.get("phase") == "collapse" and len(piano_clock.shards) > 0) timeout 2.0
    assert screen "minigame_piano_screen"
    keysym "rollback"
    assert eval (piano_state.get("phase") == "play" and piano_state["pos"] == 6) timeout 2.0
    click pos sm_test_piano_next_xy()
    assert eval (piano_state.get("phase") == "collapse") timeout 2.0
    assert screen "sm_test_piano_finished" timeout 5.0
    assert eval (c1s1_piano_outcome == "clean" and piano_state == {})
    $ skip_stop()

testcase c1s1_piano_clean_when_late:
    ## Опоздание не наказывается: все шаги собраны с большим опозданием — исход чистый.
    python:
        original = sm_test_piano_fake_pos({})
        try:
            now = sm_test_piano_begin()
            while piano_state["phase"] == "play":
                now += 7.0
                for key in sorted(piano_pending()):
                    piano_key_down(key, now=now)
                piano_complete_step(now=now)
            store.sm_test_piano_outcome = piano_outcome()
            store.sm_test_piano_results = piano_state["results"]
        finally:
            store.piano_channel_pos = original
    assert eval (sm_test_piano_results == ("played", "played"))
    assert eval (sm_test_piano_outcome == "clean")

testcase c1s1_piano_key_input:
    ## CDD ввода: скан-код важнее символа, автоповтор и Alt/Ctrl не играют, чужие клавиши проходят;
    ## шаг b+e собирается только когда зажаты обе.
    python:
        import pygame_sdl2 as pg
        original = sm_test_piano_fake_pos({})
        try:
            sm_test_piano_begin()
            cdd = PianoKeyInput()
            base = {"type": pg.KEYDOWN, "key": 0, "scancode": 0, "mod": 0, "repeat": False}
            ## Клавиша шага, не собравшая его, поглощается (IgnoreEvent) — не доходит до хоткеев.
            store.sm_test_piano_ev = (
                sm_test_piano_cdd_event(cdd, base, scancode=29, key=pg.K_a),
                sm_test_piano_cdd_event(cdd, base, scancode=6, repeat=True),
                sm_test_piano_cdd_event(cdd, base, scancode=6, mod=pg.KMOD_LALT),
                sm_test_piano_cdd_event(cdd, base, scancode=20, key=pg.K_q),
                sm_test_piano_cdd_event(cdd, base, scancode=6),
                sm_test_piano_cdd_event(cdd, base, type=pg.KEYUP, scancode=6),
                sm_test_piano_cdd_event(cdd, base, key=pg.K_m),
                sm_test_piano_cdd_event(cdd, base, scancode=6, key=pg.K_a),
            )
            store.sm_test_piano_held = set(piano_clock.held)
        finally:
            store.piano_channel_pos = original
            piano_clock.held.clear()
    assert eval (sm_test_piano_ev == (("miss", ("c", 0)), None, None, None, "eaten", "eaten", "eaten", ("step", ("e", 0))))
    assert eval (sm_test_piano_held == {("b", 0), ("e", 0)})

testcase c1s1_piano_metronome_sync:
    ## Такт подтягивается к позиции loop-канала метронома; молчание его не меняет, вторая доля loop — та же фаза.
    python:
        original = sm_test_piano_fake_pos({("sm_test_metro", 1): 0.2})
        try:
            piano_metro.bind(("sm_test_metro", 1), 2.0 / 3.0, 0.5)
            piano_metro.t0 = 10.0
            ## Звук идёт от 19.8: позиция растёт вместе со временем.
            now = 20.0
            for _ in range(200):
                now += 0.05
                store.sm_test_piano_pos_table = {("sm_test_metro", 1): (now - 19.8) % piano_metro.beat}
                piano_metro.sync(now)
            err = (19.8 - piano_metro.t0) % piano_metro.beat
            store.sm_test_piano_sync_err = min(err, piano_metro.beat - err)
            store.sm_test_piano_pos_table = {}
            t0 = piano_metro.t0
            piano_metro.sync(now + 1.0)
            store.sm_test_piano_sync_hold = (piano_metro.t0 == t0)
            ## Loop на два такта: позиция во второй доле — та же фаза.
            store.sm_test_piano_pos_table = {("sm_test_metro", 1): ((now + 1.0 - 19.8) % piano_metro.beat) + piano_metro.beat}
            piano_metro.sync(now + 1.0)
            err = (19.8 - piano_metro.t0) % piano_metro.beat
            store.sm_test_piano_sync_hold = store.sm_test_piano_sync_hold and min(err, piano_metro.beat - err) < 0.001
            ## Свежая связка без t0 берёт такт прямо из позиции.
            piano_metro.bind(("sm_test_metro", 2), 2.0 / 3.0, 0.5)
            store.sm_test_piano_pos_table = {("sm_test_metro", 2): 0.1}
            piano_metro.sync(30.0)
            store.sm_test_piano_fresh = abs(piano_metro.t0 - 29.9) < 1e-6
        finally:
            store.piano_channel_pos = original
            piano_metro.bind(None, 2.0 / 3.0, 0.5)
    assert eval (sm_test_piano_sync_err < 0.001)
    assert eval (sm_test_piano_sync_hold and sm_test_piano_fresh)

testcase c1s1_piano_screen_keys_and_skip:
    ## Клик по клавише — контрольная точка; откат возвращает клавишу; поздний пропуск завершает игру.
    $ persistent.sm_simplified_locks = False
    run Start("sm_test_piano")
    assert screen "minigame_piano_screen" timeout 3.0
    assert eval (piano_state["part"] == 0 and piano_state["pos"] == 0 and piano_state["pressed"] == ())
    click pos sm_test_piano_next_xy()
    assert eval (piano_state["pressed"] != () or piano_state["pos"] == 1) timeout 2.0
    ## Колесо отменяет одно нажатие.
    keysym "rollback"
    assert eval (piano_state["pos"] == 0 and piano_state["pressed"] == ()) timeout 2.0
    assert screen "minigame_piano_screen"
    ## Не та клавиша — запинка, шаг на месте.
    click pos sm_test_piano_wrong_xy()
    assert eval (piano_state["stumbles"] == 1 and piano_state["pos"] == 0 and piano_state["pressed"] == ()) timeout 2.0
    ## Буквы клавиатуры — ноты, а не хоткеи движка (h — спрятать окна, s — скриншот): экран на месте,
    ## каждое нажатие — нота или запинка.
    keysym "K_h"
    keysym "K_s"
    pause 0.3
    assert screen "minigame_piano_screen"
    assert eval (piano_state["stumbles"] + len(piano_state["pressed"]) + 4 * piano_state["pos"] == 3)
    skip fast
    assert screen "sm_test_piano_finished" timeout 5.0
    assert eval (c1s1_piano_outcome == "skipped")
    assert eval (piano_state == {})
    $ skip_stop()

testcase c1s1_piano_early_skip:
    $ persistent.sm_simplified_locks = False
    run Function(dev_scene_nav_start, "chapter_1_scene_1.piano")
    assert "start" timeout 15.0
    ## Непрочитанная реплика останавливает пропуск: в тестовом savedir всё непрочитано.
    $ _preferences.skip_unseen = True
    skip fast
    assert eval (c1s1_piano_outcome == "skipped") timeout 15.0
    $ skip_stop()
    $ _preferences.skip_unseen = False
    run MainMenu(confirm=False)

testcase c1s1_piano_load_rebinds_metronome:
    ## Загрузка возвращает к последнему нажатию; такт (NoRollback) связывается заново из состояния.
    $ persistent.sm_simplified_locks = False
    run Function(dev_scene_nav_start, "chapter_1_scene_1.piano")
    advance until screen "minigame_piano_screen" timeout 15.0
    assert eval (piano_state["metronome"] is not None and piano_state["metronome"] == c1s1_metronome_audio)
    assert eval (piano_metro.handle == c1s1_metronome_audio)
    run Function(sm_test_cleanup_memory_save)
    $ piano_metro.handle = None
    $ piano_metro.t0 = None
    run Function(sm_test_cleanup_memory_load)
    assert screen "minigame_piano_screen" timeout 3.0
    assert eval (piano_state["pos"] == 0 and piano_state["metronome"] == c1s1_metronome_audio)
    assert eval (piano_metro.handle == c1s1_metronome_audio) timeout 2.0
    click pos sm_test_piano_next_xy()
    assert eval (piano_state["pressed"] != () or piano_state["pos"] == 1) timeout 2.0
    skip fast
    $ skip_stop()
    run MainMenu(confirm=False)
