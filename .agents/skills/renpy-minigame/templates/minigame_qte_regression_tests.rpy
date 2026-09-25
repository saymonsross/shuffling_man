## Регрессия minigame_qte.rpy. Вход — hide-лейбл со «сторожевым» экраном: по нему тест видит,
## что мини-игра вернула управление.

default sm_test_qte_result = None

init python:

    ## В python-блоке тест-кейса замыкания не видят его локальные имена, поэтому подмены — здесь.
    def sm_test_qte_model():
        calls = []
        original = store.sm_sfx
        store.sm_sfx = lambda name, **kwargs: calls.append(name)
        try:
            persistent.sm_simplified_locks = False
            qte_start(("left", "up"), 1.0)
            assert qte_tick() is None and qte_state["phase"] == "intro"
            ## Перемотка часов вместо ожидания: dt настоящий, но с потолком QTE_MAX_DT.
            for _ in range(20):
                qte_clock.last = qte_time.perf_counter() - 0.05
                qte_tick()
            assert qte_state["phase"] == "run"
            qte_press("up")
            assert qte_state["verdicts"] == ("miss",)
            assert calls == [QTE_MISS_SOUND]
            qte_press("up")
            assert qte_state["verdicts"] == ("miss", "hit")
            assert qte_state["phase"] == "outro"
            qte_press("up")
            assert qte_state["verdicts"] == ("miss", "hit")
            qte_clock.last = qte_time.perf_counter() - 60.0
            assert qte_tick() is None
            assert qte_state["t"] <= QTE_MAX_DT + 0.001
            result = None
            for _ in range(40):
                qte_clock.last = qte_time.perf_counter() - 0.05
                result = qte_tick()
                if result is not None:
                    break
            assert result == 1, result
        finally:
            store.sm_sfx = original

    def sm_test_qte_simplified():
        original = store.sm_sfx
        store.sm_sfx = lambda name, **kwargs: None
        try:
            persistent.sm_simplified_locks = True
            qte_start(("left",), 0.2)
            store.qte_state["phase"] = "run"
            for _ in range(30):
                qte_clock.last = qte_time.perf_counter() - 0.05
                qte_tick()
            assert qte_state["verdicts"] == ()
            qte_press("right")
            assert qte_state["verdicts"] == ()
            qte_press("left")
            assert qte_state["verdicts"] == ("hit",)
        finally:
            store.sm_sfx = original

label sm_test_qte(sm_test_keys=("left", "right"), sm_test_per_key=30.0, sm_test_skippable=False) hide:
    $ sm_test_qte_result = None
    call minigame_qte(sm_test_keys, sm_test_per_key, sm_test_skippable) from _call_sm_test_qte
    $ sm_test_qte_result = _return
    call screen sm_test_qte_finished
    return

## Жёсткая контрольная точка до мини-игры: без неё откату некуда уйти, и проверка блокировки пуста.
label sm_test_qte_after_ready hide:
    call screen sm_test_qte_ready
    call sm_test_qte from _call_sm_test_qte_after_ready
    return

screen sm_test_qte_ready():
    modal True
    button:
        id "sm_test_qte_go"
        xysize (200, 200)
        action Return(True)

label sm_test_qte_timeout hide:
    call sm_test_qte(("up", "down"), 0.3) from _call_sm_test_qte_timeout
    return

label sm_test_qte_skippable hide:
    call sm_test_qte(("up", "down", "left"), 30.0, True) from _call_sm_test_qte_skippable
    return

screen sm_test_qte_finished():
    modal True
    null

testsuite minigame_qte_regression:

    testcase model:
        $ sm_test_qte_model()

    testcase simplified_mode_never_misses:
        $ sm_test_qte_simplified()

    testcase keyboard_gamepad_and_mouse:
        parameter device = ["keyboard", "gamepad", "mouse"]

        run Function(dev_scene_nav_start, "sm_test_qte")
        assert screen "minigame_qte_screen" timeout 3.0
        assert eval (qte_state["phase"] == "run") timeout 3.0
        if eval (device == "keyboard"):
            keysym "K_LEFT"
        elif eval (device == "gamepad"):
            run Function(renpy.queue_event, "pad_dpleft_press")
        else:
            click id "qte_pad_left"
        assert eval (qte_state["verdicts"] == ("hit",)) timeout 1.0
        keysym "K_UP"
        assert eval (qte_state["verdicts"] == ("hit", "miss")) timeout 1.0
        assert screen "sm_test_qte_finished" timeout 3.0
        assert not screen "minigame_qte_screen"
        assert eval (sm_test_qte_result == 1)
        run MainMenu(confirm=False)

    testcase timeout_is_a_miss_not_a_loss:
        run Function(dev_scene_nav_start, "sm_test_qte_timeout")
        assert screen "minigame_qte_screen" timeout 3.0
        assert screen "sm_test_qte_finished" timeout 5.0
        assert eval (sm_test_qte_result == 0)
        run MainMenu(confirm=False)

    testcase rollback_key_does_not_restart:
        run Function(dev_scene_nav_start, "sm_test_qte_after_ready")
        assert screen "sm_test_qte_ready" timeout 3.0
        click id "sm_test_qte_go"
        assert eval (qte_state.get("phase") == "run") timeout 3.0
        keysym "K_LEFT"
        assert eval (qte_state["verdicts"] == ("hit",)) timeout 1.0
        keysym "rollback"
        pause 0.3
        assert not screen "sm_test_qte_ready"
        assert screen "minigame_qte_screen"
        assert eval (qte_state["verdicts"] == ("hit",))
        run MainMenu(confirm=False)

    testcase load_restarts_series_and_keeps_rollback_blocked:
        run Function(dev_scene_nav_start, "sm_test_qte_after_ready")
        assert screen "sm_test_qte_ready" timeout 3.0
        click id "sm_test_qte_go"
        assert eval (qte_state.get("phase") == "run") timeout 3.0
        run Function(sm_test_cleanup_memory_save)
        keysym "K_LEFT"
        assert eval (qte_state["verdicts"] == ("hit",)) timeout 1.0
        run Function(sm_test_cleanup_memory_load)
        assert screen "minigame_qte_screen" timeout 2.0
        assert eval (qte_state["verdicts"] == ()) timeout 1.0
        keysym "rollback"
        pause 0.3
        assert not screen "sm_test_qte_ready"
        assert screen "minigame_qte_screen"
        run MainMenu(confirm=False)

    testcase rollback_into_finished_series_then_forward:
        run Function(dev_scene_nav_start, "sm_test_qte")
        assert eval (qte_state["phase"] == "run") timeout 3.0
        keysym "K_LEFT"
        keysym "K_RIGHT"
        assert screen "sm_test_qte_finished" timeout 3.0
        assert eval (sm_test_qte_result == 2)
        run Rollback()
        assert screen "minigame_qte_screen" timeout 2.0
        keysym "rollforward"
        assert screen "sm_test_qte_finished" timeout 2.0
        assert eval (sm_test_qte_result == 2)
        run MainMenu(confirm=False)

    testcase late_skip_only_when_skippable:
        parameter skippable = [True, False]

        if eval (skippable):
            run Function(dev_scene_nav_start, "sm_test_qte_skippable")
        else:
            run Function(dev_scene_nav_start, "sm_test_qte")
        assert eval (qte_state["phase"] == "run") timeout 3.0
        skip fast
        if eval (skippable):
            assert screen "sm_test_qte_finished" timeout 2.0
            assert eval (sm_test_qte_result == "skipped")
        else:
            pause 0.5
            assert screen "minigame_qte_screen"
        run MainMenu(confirm=False)
