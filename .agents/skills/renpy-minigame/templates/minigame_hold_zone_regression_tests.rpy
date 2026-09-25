## Регрессия minigame_hold_zone.rpy: модель и ввод — синтетическими событиями,
## возврат итога из event() и поздний пропуск — живым прогоном экрана.

default sm_test_hold_zone_result = None

init python:

    def sm_test_hold_zone_feed(zone, ev):
        """event() съедает своё через IgnoreEvent; для теста это «обработано»."""
        try:
            return zone.event(ev, -1, -1, 0.0)
        except renpy.IgnoreEvent:
            return "eaten"

    def sm_test_hold_zone_run(zone, dt=0.05, pointer=None):
        zone.pointer = pointer
        while zone.result is None:
            zone.step(dt)
        return zone.result

    def sm_test_hold_zone_model():
        first = sm_test_hold_zone_run(HoldZone(3.0, 11))
        second = sm_test_hold_zone_run(HoldZone(3.0, 11))
        assert first == second
        assert 0.0 <= first <= 1.0
        ## Указатель в центре сильнее сноса: метка почти всё время в зоне.
        steered = sm_test_hold_zone_run(HoldZone(3.0, 11), pointer=HOLD_ZONE_SIZE[0] / 2.0)
        assert steered >= 0.9, steered
        ## Крупный последний шаг не выводит долю за 1.0.
        calm = HoldZone(1.0, 3)
        calm.drift_scale = 0.0
        assert sm_test_hold_zone_run(calm, dt=0.3) == 1.0

    def sm_test_hold_zone_input():
        pg = renpy.pygame
        zone = HoldZone(3.0, 5)
        down = pg.event.Event(pg.KEYDOWN, key=pg.K_LEFT, mod=0, scancode=0, unicode="", repeat=False)
        up = pg.event.Event(pg.KEYUP, key=pg.K_LEFT, mod=0, scancode=0, unicode="", repeat=False)
        assert sm_test_hold_zone_feed(zone, down) == "eaten" and zone.left
        assert sm_test_hold_zone_feed(zone, up) == "eaten" and not zone.left

        pad = renpy.display.core.EVENTNAME
        press = pg.event.Event(pad, eventnames=["pad_dpright_press"], controller="test", up=False)
        release = pg.event.Event(pad, eventnames=["pad_dpright_release"], controller="test", up=False)
        assert sm_test_hold_zone_feed(zone, press) == "eaten" and zone.right
        assert sm_test_hold_zone_feed(zone, release) == "eaten" and not zone.right

        zone.right = True
        zone.pointer = 100.0
        lost = pg.event.Event(pg.ACTIVEEVENT, gain=0, state=3)
        assert sm_test_hold_zone_feed(zone, lost) is None
        assert not zone.right and zone.pointer is None

        ## Чужие клавиши не съедаются.
        other = pg.event.Event(pg.KEYDOWN, key=pg.K_ESCAPE, mod=0, scancode=0, unicode="", repeat=False)
        assert sm_test_hold_zone_feed(zone, other) is None

label sm_test_hold_zone(sm_test_skippable=False) hide:
    $ sm_test_hold_zone_result = None
    call minigame_hold_zone(1.0, sm_test_skippable) from _call_sm_test_hold_zone
    $ sm_test_hold_zone_result = _return
    call screen sm_test_hold_zone_finished
    return

## Жёсткая контрольная точка до мини-игры: без неё откату некуда уйти, и проверка блокировки пуста.
label sm_test_hold_zone_after_ready hide:
    call screen sm_test_hold_zone_ready
    call sm_test_hold_zone from _call_sm_test_hold_zone_after_ready
    return

screen sm_test_hold_zone_ready():
    modal True
    button:
        id "sm_test_hold_zone_go"
        xysize (200, 200)
        action Return(True)

label sm_test_hold_zone_skippable hide:
    call sm_test_hold_zone(True) from _call_sm_test_hold_zone_skippable
    return

screen sm_test_hold_zone_finished():
    modal True
    null

testsuite minigame_hold_zone_regression:

    testcase model_is_deterministic_and_bounded:
        $ sm_test_hold_zone_model()

    testcase keyboard_gamepad_and_focus_loss:
        $ sm_test_hold_zone_input()

    testcase result_returns_from_call_screen:
        run Function(dev_scene_nav_start, "sm_test_hold_zone")
        assert screen "minigame_hold_zone_screen" timeout 3.0
        assert screen "sm_test_hold_zone_finished" timeout 4.0
        assert eval (isinstance(sm_test_hold_zone_result, float) and 0.0 <= sm_test_hold_zone_result <= 1.0)
        run MainMenu(confirm=False)

    testcase rollback_key_does_not_restart:
        run Function(dev_scene_nav_start, "sm_test_hold_zone_after_ready")
        assert screen "sm_test_hold_zone_ready" timeout 3.0
        click id "sm_test_hold_zone_go"
        assert screen "minigame_hold_zone_screen" timeout 3.0
        keysym "rollback"
        pause 0.2
        assert not screen "sm_test_hold_zone_ready"
        assert screen "minigame_hold_zone_screen"
        assert screen "sm_test_hold_zone_finished" timeout 4.0
        run MainMenu(confirm=False)

    testcase load_keeps_rollback_blocked:
        run Function(dev_scene_nav_start, "sm_test_hold_zone_after_ready")
        assert screen "sm_test_hold_zone_ready" timeout 3.0
        click id "sm_test_hold_zone_go"
        assert screen "minigame_hold_zone_screen" timeout 3.0
        run Function(sm_test_cleanup_memory_save)
        run Function(sm_test_cleanup_memory_load)
        assert screen "minigame_hold_zone_screen" timeout 2.0
        keysym "rollback"
        pause 0.2
        assert not screen "sm_test_hold_zone_ready"
        assert screen "minigame_hold_zone_screen"
        run MainMenu(confirm=False)

    testcase rollback_into_finished_attempt_then_forward:
        run Function(dev_scene_nav_start, "sm_test_hold_zone")
        assert screen "sm_test_hold_zone_finished" timeout 4.0
        ## Откат вернул бы и store-переменную; session живёт вне отката.
        $ renpy.session["sm_test_hold_zone_first"] = sm_test_hold_zone_result
        run Rollback()
        assert screen "minigame_hold_zone_screen" timeout 2.0
        keysym "rollforward"
        assert screen "sm_test_hold_zone_finished" timeout 2.0
        assert eval (sm_test_hold_zone_result == renpy.session.get("sm_test_hold_zone_first"))
        $ renpy.session.pop("sm_test_hold_zone_first", None)
        run MainMenu(confirm=False)

    testcase late_skip_when_skippable:
        run Function(dev_scene_nav_start, "sm_test_hold_zone_skippable")
        assert screen "minigame_hold_zone_screen" timeout 3.0
        skip fast
        assert screen "sm_test_hold_zone_finished" timeout 2.0
        assert eval (sm_test_hold_zone_result == "skipped")
        run MainMenu(confirm=False)
