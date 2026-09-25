## Регрессия minigame_hotspots.rpy на зонах-заглушках Solid (маска = прямоугольник).
## Сохранение в память — общий хелпер из cleanup_regression_tests.rpy. Строки без _():
## renpy translate унёс бы их из game/dev в game/tl.

define SM_TEST_HOTSPOTS = (
    ("a", Solid("#884444", xysize=(200, 200)), (300, 400), "A"),
    ("b", Solid("#448844", xysize=(200, 200)), (860, 400), "B"),
    ("c", Solid("#444488", xysize=(200, 200)), (1420, 400), "C"),
)

default sm_test_hotspots_result = None

label sm_test_hotspots_phrase hide:
    call minigame_hotspots(SM_TEST_HOTSPOTS, ("b", "a", "b"), True) from _call_sm_test_hotspots_phrase
    $ sm_test_hotspots_result = _return
    call screen sm_test_hotspots_finished
    return

label sm_test_hotspots_collect hide:
    call minigame_hotspots(SM_TEST_HOTSPOTS) from _call_sm_test_hotspots_collect
    $ sm_test_hotspots_result = _return
    call screen sm_test_hotspots_finished
    return

screen sm_test_hotspots_finished():
    modal True
    null

testsuite minigame_hotspots_regression:

    testcase ordered_phrase_with_miss:
        run Function(dev_scene_nav_start, "sm_test_hotspots_phrase")
        assert screen "minigame_hotspots_screen" timeout 3.0
        click id "hotspots_a"
        assert eval (hotspots_misses == 1 and hotspots_done == ()) timeout 1.0
        assert id "hotspots_miss_hint" timeout 1.0
        assert not id "hotspots_miss_hint" timeout 3.0
        click id "hotspots_b"
        assert eval (hotspots_done == ("b",)) timeout 1.0
        click id "hotspots_a"
        assert eval (hotspots_done == ("b", "a")) timeout 1.0
        click id "hotspots_b"
        assert eval (hotspots_done == ("b", "a", "b")) timeout 1.0
        assert id "hotspots_complete" timeout 1.0
        click id "hotspots_continue"
        assert screen "sm_test_hotspots_finished" timeout 2.0
        assert not screen "minigame_hotspots_screen"
        assert eval (sm_test_hotspots_result == "done" and hotspots_misses == 1)
        run MainMenu(confirm=False)

    testcase collect_hides_taken_spots:
        run Function(dev_scene_nav_start, "sm_test_hotspots_collect")
        assert screen "minigame_hotspots_screen" timeout 3.0
        click id "hotspots_c"
        assert eval (hotspots_done == ("c",)) timeout 1.0
        assert not id "hotspots_c" timeout 1.0
        click id "hotspots_a"
        click id "hotspots_b"
        assert id "hotspots_complete" timeout 2.0
        assert eval (hotspots_misses == 0)
        run MainMenu(confirm=False)

    testcase rollback_undoes_one_action:
        run Function(dev_scene_nav_start, "sm_test_hotspots_collect")
        assert screen "minigame_hotspots_screen" timeout 3.0
        click id "hotspots_a"
        assert eval (hotspots_done == ("a",)) timeout 1.0
        click id "hotspots_b"
        assert eval (hotspots_done == ("a", "b")) timeout 1.0
        run Rollback()
        assert eval (hotspots_done == ("a",)) timeout 2.0
        assert id "hotspots_b" timeout 1.0
        run MainMenu(confirm=False)

    testcase save_load_keeps_progress:
        run Function(dev_scene_nav_start, "sm_test_hotspots_collect")
        assert screen "minigame_hotspots_screen" timeout 3.0
        click id "hotspots_a"
        assert eval (hotspots_done == ("a",)) timeout 1.0
        run Function(sm_test_cleanup_memory_save)
        click id "hotspots_b"
        assert eval (hotspots_done == ("a", "b")) timeout 1.0
        run Function(sm_test_cleanup_memory_load)
        assert screen "minigame_hotspots_screen" timeout 2.0
        assert eval (hotspots_done == ("a",)) timeout 1.0
        assert id "hotspots_b"
        run MainMenu(confirm=False)

    testcase late_skip:
        parameter skip_mode = ["fast", "ctrl"]

        run Function(dev_scene_nav_start, "sm_test_hotspots_collect")
        assert screen "minigame_hotspots_screen" timeout 3.0
        click id "hotspots_a"
        assert eval (hotspots_done == ("a",)) timeout 1.0
        if eval (skip_mode == "fast"):
            skip fast
        else:
            keysym "skip"
        assert screen "sm_test_hotspots_finished" timeout 2.0
        assert eval (sm_test_hotspots_result == "skipped" and hotspots_done == ("a", "b", "c"))
        run MainMenu(confirm=False)
