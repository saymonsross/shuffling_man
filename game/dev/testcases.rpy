## Автоматические smoke-тесты Ren'Py. Каталог game/dev исключён из сборки.

default sm_test_original_simplified = None
default sm_test_original_reduce_motion = None
default sm_test_pointer_leaked = False

## Проба click-through под modal-мини-игрой.
screen sm_test_pointer_leak_target():
    zorder 100

    textbutton "LEAK PROBE":
        id "leak_probe"
        action SetVariable("sm_test_pointer_leaked", True)
        xalign 0.5
        yalign 1.0

testsuite global:
    teardown:
        if eval "sm_test_original_simplified is not None":
            $ persistent.sm_simplified_locks = sm_test_original_simplified
            $ sm_test_original_simplified = None
        if eval "sm_test_original_reduce_motion is not None":
            $ persistent.sm_reduce_motion = sm_test_original_reduce_motion
            $ sm_test_original_reduce_motion = None
        exit

testcase c1s1_minigame_model:
    $ c1s1_mg_reset()
    assert eval "isinstance(c1s1_mg_state, renpy.revertable.RevertableDict)"
    assert eval "c1s1_mg_state.get('latch_p') == 0.0"
    assert eval "not c1s1_latch_open and not c1s1_big_lock_open and not c1s1_door_handle_open"

    $ c1s1_mg_active = True
    $ c1s1_mg_lock_i = 0
    $ c1s1_mg_simplified_step()
    $ c1s1_mg_simplified_tick(1.0)
    assert eval "c1s1_mg_state.get('latch_p') == 1.0 and not c1s1_latch_open"
    $ c1s1_mg_simplified_step()
    $ c1s1_mg_simplified_tick(1.0)
    assert eval "c1s1_mg_state.get('latch_p') == 2.0 and not c1s1_latch_open"
    $ c1s1_mg_simplified_step()
    $ c1s1_mg_simplified_tick(1.0)
    assert eval "c1s1_latch_open"
    assert eval "c1s1_mg_simplified_label() == 'Замок открыт'"

    $ c1s1_mg_lock_i = 1
    $ c1s1_mg_simplified_step()
    $ c1s1_mg_simplified_tick(1.0)
    $ c1s1_mg_simplified_step()
    $ c1s1_mg_simplified_tick(1.0)
    assert eval "c1s1_big_lock_open and c1s1_mg_state.get('big_p') == 2.0"

    $ c1s1_mg_lock_i = 2
    $ c1s1_mg_simplified_step()
    $ c1s1_mg_simplified_tick(1.0)
    assert eval "c1s1_door_handle_open and c1s1_mg_state.get('handle_p') == 1.0"

    $ c1s1_mg_reset()
    assert eval "not c1s1_latch_open and not c1s1_big_lock_open and not c1s1_door_handle_open"
    $ c1s1_mg_active = True
    $ c1s1_mg_knocking = True
    $ _c1s1_clock_state.context_level = renpy.context_nesting_level() + 1
    $ _mg_set("clock", sm_time.monotonic() - 10.0)
    $ c1s1_mg_tick()
    assert eval "sm_time.monotonic() - c1s1_mg_state.get('clock') < 0.1"
    assert eval "c1s1_mg_state.get('play_t') < 0.1"
    $ _mg_set("play_t", 0.0)
    $ _mg_set("clock", sm_time.monotonic() - 1.0)
    $ c1s1_mg_tick()
    assert eval "0.24 <= c1s1_mg_state.get('play_t') <= 0.25"
    $ c1s1_mg_open_all()
    assert eval "c1s1_mg_lock_i == len(C1S1_MG_LOCK_ORDER)"
    assert eval "c1s1_latch_open and c1s1_big_lock_open and c1s1_door_handle_open"

testcase c1s1_minigame_accessibility:
    $ sm_test_original_simplified = persistent.sm_simplified_locks
    $ sm_test_original_reduce_motion = persistent.sm_reduce_motion
    $ persistent.sm_simplified_locks = False
    $ persistent.sm_reduce_motion = True
    assert eval "abs(sm_motion_transition(c1s1_knock_punch).delay - c1s1_knock_punch.delay) < 0.0001"
    $ persistent.sm_reduce_motion = False
    $ c1s1_mg_reset()
    $ c1s1_mg_active = True

    run Show("c1s1_locks_minigame")
    assert "Упростить управление"
    click "Упростить управление"
    assert "Поднять щеколду"
    click "Поднять щеколду"
    assert "Сдвинуть щеколду вправо" timeout 1.0

    run Hide("c1s1_locks_minigame")
    $ c1s1_mg_active = False

testcase c1s1_minigame_pointer_capture:
    ## Проверяем настоящий drag после accessibility-сценария.
    if screen "main_menu":
        click "Начать" raw
        assert "Чтобы заговорить о чём-то тяжёлом" raw timeout 8.0
    $ persistent.sm_simplified_locks = False
    $ quick_menu = True
    $ c1s1_mg_reset()
    $ c1s1_mg_lock_i = 2
    $ c1s1_mg_active = True
    $ sm_test_pointer_leaked = False

    run Show("quick_menu")
    run Show("c1s1_mg_runtime")
    run Show("sm_test_pointer_leak_target")
    run Show("c1s1_locks_minigame")
    assert id "leak_probe"

    ## Mouseup над нижним контролом не должен пройти сквозь мини-игру.
    $ sm_test_handle_pos = (int(c1s1_handle_pivot_screen()[0] + C1S1_HANDLE_GRAB_BOX[0] * C1S1_HANDLE_ZOOM), int(c1s1_handle_pivot_screen()[1] + C1S1_HANDLE_GRAB_BOX[1] * C1S1_HANDLE_ZOOM))
    drag pos sm_test_handle_pos to id "leak_probe" pos (0.5, 0.5) steps 8
    pause 0.2
    assert eval "not sm_test_pointer_leaked"
    assert eval "not c1s1_mg_pointer_down()"
    assert eval "_mg_get('handle_grab') == 0.0"

    ## Release не должен стать кликом по кнопке самого modal-screen.
    $ c1s1_door_handle_open = False
    $ _mg_set("handle_p", 0.0)
    $ _mg_set("done", -1.0)
    drag pos sm_test_handle_pos to "Упростить управление" raw pos (0.5, 0.5) steps 8
    pause 0.2
    assert eval "not persistent.sm_simplified_locks"
    assert eval "not c1s1_mg_pointer_down()"

    ## Завершение ждёт физического release.
    $ c1s1_door_handle_open = True
    $ _mg_set("done", 0.0)
    $ _mg_set("play_t", C1S1_MG_DONE_HOLD_T + 1.0)
    $ _c1s1_clock_state.pointer_down = True
    $ c1s1_mg_check_done()
    assert eval "c1s1_mg_pointer_down() and _mg_get('done') == 0.0"

    ## Потерянный SDL mouseup не должен навсегда оставить экран modal.
    $ _c1s1_clock_state.pointer_up_since = sm_time.monotonic() - C1S1_MG_POINTER_LOST_T - 0.01
    $ c1s1_mg_recover_lost_pointer(sm_time.monotonic())
    assert eval "not c1s1_mg_pointer_down()"

    $ c1s1_mg_release()
    run Hide("c1s1_locks_minigame")
    run Hide("sm_test_pointer_leak_target")

    ## Quick menu скрыто до завершения runtime.
    assert not "История" raw
    assert not "Меню" raw
    run Hide("c1s1_mg_runtime")
    assert ("История" raw or "Меню" raw) timeout 1.0
    $ c1s1_mg_active = False
    $ c1s1_mg_reset()
