## Настоящие call screen без ожидания предшествующих анимаций и реплик.
label sm_test_skip_note_start:
    call screen prologue_note_start
    jump sm_test_skip_complete

label sm_test_skip_lamp:
    call screen c1s1_lamp_switch
    jump sm_test_skip_complete

label sm_test_skip_metronome:
    call screen c1s1_metronome_start
    jump sm_test_skip_complete

label sm_test_skip_open_door:
    $ c1s1_mg_reset()
    $ c1s1_mg_active = True
    call screen c1s1_locks_open_door
    jump sm_test_skip_complete

label sm_test_skip_locks:
    $ c1s1_mg_reset()
    $ c1s1_mg_active = True
    call screen c1s1_locks_minigame
    jump sm_test_skip_complete

label sm_test_skip_complete:
    $ skip_stop()
    call screen sm_test_skip_finished
    return

screen sm_test_skip_finished():
    modal True
    null

screen sm_test_skip_modal():
    modal True
    zorder 200
    null

testcase nonbranching_prompt_late_skip:
    parameter (prompt_label, prompt_screen) = [
        ("sm_test_skip_note_start", "prologue_note_start"),
        ("sm_test_skip_lamp", "c1s1_lamp_switch"),
        ("sm_test_skip_metronome", "c1s1_metronome_start")]
    parameter skip_mode = ["fast", "normal", "ctrl"]

    run Function(dev_scene_nav_start, prompt_label)
    assert screen prompt_screen timeout 3.0
    pause 0.1
    assert screen prompt_screen
    assert eval (not renpy.is_skipping())
    if eval (skip_mode == "fast"):
        skip fast
    elif eval (skip_mode == "normal"):
        skip
    else:
        ## То же keymap-событие, которое движок получает при нажатии Ctrl.
        keysym "skip"
    assert screen "sm_test_skip_finished" timeout 1.0
    assert not screen prompt_screen
    run MainMenu(confirm=False)

testcase nonbranching_prompt_skip_modal:
    run Function(dev_scene_nav_start, "sm_test_skip_lamp")
    assert screen "c1s1_lamp_switch" timeout 3.0
    run Show("sm_test_skip_modal")
    skip fast
    pause 0.1
    assert screen "c1s1_lamp_switch"
    assert not screen "sm_test_skip_finished"
    run Hide("sm_test_skip_modal")
    assert screen "sm_test_skip_finished" timeout 1.0
    run MainMenu(confirm=False)

testcase locks_do_not_skip:
    parameter (prompt_label, prompt_screen) = [
        ("sm_test_skip_open_door", "c1s1_locks_open_door"),
        ("sm_test_skip_locks", "c1s1_locks_minigame")]

    run Function(dev_scene_nav_start, prompt_label)
    assert screen prompt_screen timeout 3.0
    skip fast
    pause 0.2
    assert screen prompt_screen
    assert not screen "sm_test_skip_finished"
    assert eval (not c1s1_latch_open and not c1s1_big_lock_open and not c1s1_door_handle_open)
    $ skip_stop()
    run MainMenu(confirm=False)

testcase story_choice_does_not_skip:
    run Function(dev_scene_nav_start, "chapter_1_scene_3")
    advance until screen "choice" timeout 10.0
    skip fast
    pause 0.2
    assert screen "choice"
    assert eval (c1s3_teaparty_choice is None and c1s3_neighbor_choice is None)
    $ skip_stop()
    run MainMenu(confirm=False)
