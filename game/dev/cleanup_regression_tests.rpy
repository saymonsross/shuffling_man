init python:

    ## Тот же roots/log, что у save/load, но без слотов и записи persistent.
    def sm_test_cleanup_memory_save():
        from renpy.compat.pickle import dumps
        roots = renpy.game.log.freeze()
        try:
            renpy.session["_sm_cleanup_saved_game"] = dumps((roots, renpy.game.log))
        finally:
            renpy.game.log.discard_freeze()

    def sm_test_cleanup_memory_load():
        from renpy.compat.pickle import loads
        roots, log = loads(renpy.session.pop("_sm_cleanup_saved_game"))
        log.unfreeze(roots, label="_after_load")


label sm_test_cleanup hide:
    call chapter_1_scene_1_minigame_cleanup from _call_sm_test_cleanup
    $ skip_stop()
    call screen sm_test_cleanup_finished
    return

screen sm_test_cleanup_finished():
    modal True
    null


testcase c1s1_cleanup_model:
    $ c1s1_cleanup_reset()
    assert eval (c1s1_cleanup_collected == () and c1s1_cleanup_outcome is None)
    assert eval (len(C1S1_CLEANUP_KEYS) == 11 and len(set(C1S1_CLEANUP_KEYS)) == 11)
    assert eval (not c1s1_cleanup_collect("unknown"))
    assert eval (not c1s1_cleanup_complete())
    $ c1s1_cleanup_finish()
    assert eval (c1s1_cleanup_outcome is None)
    python hide:
        for count, key in enumerate(C1S1_CLEANUP_KEYS, start=1):
            assert c1s1_cleanup_collect(key)
            assert len(store.c1s1_cleanup_collected) == count
            assert not c1s1_cleanup_collect(key)
            assert len(store.c1s1_cleanup_collected) == count
            assert c1s1_cleanup_complete() == (count == 11)
    $ c1s1_cleanup_finish()
    assert eval (c1s1_cleanup_outcome == "done")
    $ c1s1_cleanup_reset()
    assert eval (c1s1_cleanup_collected == () and c1s1_cleanup_outcome is None)
    $ c1s1_cleanup_finish(skipped=True)
    assert eval (c1s1_cleanup_complete() and c1s1_cleanup_outcome == "skipped")
    assert eval (not c1s1_cleanup_collect("blanket"))
    $ c1s1_cleanup_reset()


testcase c1s1_cleanup_pixel_clicks_and_completion:
    run Function(dev_scene_nav_start, "sm_test_cleanup")
    assert screen "c1s1_cleanup_minigame" timeout 3.0
    assert eval (c1s1_cleanup_collected == ())
    assert eval (renpy.get_displayable('c1s1_cleanup_minigame', 'cleanup_background').name == ('chapter_1_cleanup_room',))
    assert eval (renpy.get_displayable('c1s1_cleanup_minigame', 'cleanup_progress').adjustment.value == 0)
    assert not id "cleanup_complete"

    ## Прозрачный угол PNG мяча и стена не являются кнопками.
    click pos (110, 720)
    click pos (1100, 200)
    assert eval (c1s1_cleanup_collected == ())

    move pos (1490, 846)
    assert eval (renpy.get_displayable('c1s1_cleanup_minigame', 'cleanup_blanket').is_focused()) timeout 1.0
    click pos (1490, 846)
    assert eval (c1s1_cleanup_collected == ("blanket",)) timeout 1.0
    assert not id "cleanup_blanket"
    assert eval (renpy.get_displayable('c1s1_cleanup_minigame', 'cleanup_progress').adjustment.value == 1)
    click pos (1490, 846)
    assert eval (c1s1_cleanup_collected == ("blanket",))

    click pos (1455, 676)
    assert eval (len(c1s1_cleanup_collected) == 2) timeout 1.0
    click pos (220, 790)
    assert eval (len(c1s1_cleanup_collected) == 3) timeout 1.0
    click pos (584, 635)
    assert eval (len(c1s1_cleanup_collected) == 4) timeout 1.0
    click pos (1740, 1003)
    assert eval (len(c1s1_cleanup_collected) == 5) timeout 1.0
    click pos (1035, 609)
    assert eval (len(c1s1_cleanup_collected) == 6) timeout 1.0
    click pos (940, 391)
    assert eval (len(c1s1_cleanup_collected) == 7) timeout 1.0
    click pos (856, 416)
    assert eval (len(c1s1_cleanup_collected) == 8) timeout 1.0
    click pos (362, 400)
    assert eval (len(c1s1_cleanup_collected) == 9) timeout 1.0
    click pos (619, 426)
    assert eval (len(c1s1_cleanup_collected) == 10) timeout 1.0
    click pos (1430, 424)
    assert id "cleanup_complete" timeout 1.0
    assert eval (c1s1_cleanup_complete() and c1s1_cleanup_outcome is None)
    assert id "cleanup_progress"
    assert eval (renpy.get_displayable('c1s1_cleanup_minigame', 'cleanup_progress').adjustment.value == 11)
    click id "cleanup_continue"
    assert screen "sm_test_cleanup_finished" timeout 1.0
    assert not screen "c1s1_cleanup_minigame"
    assert eval (c1s1_cleanup_outcome == "done")
    run MainMenu(confirm=False)


testcase c1s1_cleanup_late_skip:
    parameter skip_mode = ["fast", "normal", "ctrl"]

    run Function(dev_scene_nav_start, "sm_test_cleanup")
    assert screen "c1s1_cleanup_minigame" timeout 3.0
    click pos (1490, 846)
    assert eval (c1s1_cleanup_collected == ("blanket",)) timeout 1.0
    assert eval (not renpy.is_skipping())

    if eval (skip_mode == "fast"):
        skip fast
    elif eval (skip_mode == "normal"):
        skip
    else:
        keysym "skip"
    assert screen "sm_test_cleanup_finished" timeout 1.0
    assert not screen "c1s1_cleanup_minigame"
    assert eval (c1s1_cleanup_complete() and c1s1_cleanup_outcome == "skipped")
    run MainMenu(confirm=False)


testcase c1s1_cleanup_rollback:
    run Function(dev_scene_nav_start, "sm_test_cleanup")
    assert screen "c1s1_cleanup_minigame" timeout 3.0
    click pos (1490, 846)
    assert eval (c1s1_cleanup_collected == ("blanket",)) timeout 1.0
    click pos (1455, 676)
    assert eval (c1s1_cleanup_collected == ("blanket", "pizza")) timeout 1.0
    run Rollback()
    assert screen "c1s1_cleanup_minigame" timeout 1.0
    assert eval (c1s1_cleanup_collected == ("blanket",)) timeout 1.0
    assert id "cleanup_pizza"
    assert not id "cleanup_blanket"
    click pos (1455, 676)
    assert eval (c1s1_cleanup_collected == ("blanket", "pizza")) timeout 1.0
    run MainMenu(confirm=False)


testcase c1s1_cleanup_save_restore:
    run Function(dev_scene_nav_start, "sm_test_cleanup")
    assert screen "c1s1_cleanup_minigame" timeout 3.0
    click pos (1490, 846)
    assert eval (c1s1_cleanup_collected == ("blanket",)) timeout 1.0
    run Function(sm_test_cleanup_memory_save)
    click pos (1455, 676)
    assert eval (c1s1_cleanup_collected == ("blanket", "pizza")) timeout 1.0
    run Function(sm_test_cleanup_memory_load)
    assert screen "c1s1_cleanup_minigame" timeout 2.0
    assert eval (c1s1_cleanup_collected == ("blanket",)) timeout 1.0
    assert id "cleanup_pizza"
    assert not id "cleanup_blanket"
    assert eval (c1s1_cleanup_outcome is None)
    click pos (1455, 676)
    assert eval (c1s1_cleanup_collected == ("blanket", "pizza")) timeout 1.0
    assert eval ("_sm_cleanup_saved_game" not in renpy.session)
    run MainMenu(confirm=False)
