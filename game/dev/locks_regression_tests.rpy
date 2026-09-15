init python:
    def sm_test_lock_hover_feedback():
        original_mouse_pos = renpy.get_mouse_pos
        original_mouse_focused = renpy.game.interface.mouse_focused
        original_splay = store.splay
        original_restart = renpy.restart_interaction
        mouse = [0, 0]
        sounds = []
        try:
            renpy.game.interface.mouse_focused = True
            renpy.get_mouse_pos = lambda: tuple(mouse)
            store.splay = lambda name, **kwargs: sounds.append((name, kwargs.get("ext")))
            renpy.restart_interaction = lambda: None
            for part, lock_i in (("latch", 0), ("big_latch", 1), ("big_spin", 1), ("handle", 2)):
                c1s1_mg_reset()
                store.c1s1_mg_active = True
                store.c1s1_mg_lock_i = lock_i
                if part == "latch":
                    point = c1s1_latch_hit_rect()[:2]
                elif part == "big_latch":
                    point = c1s1_lock_pos(C1S1_MG_LOCK_CENTER,
                        (C1S1_BIG_LATCH_OFF[0] + C1S1_BIG_LATCH_GRAB_BOX[0],
                         C1S1_BIG_LATCH_OFF[1] + C1S1_BIG_LATCH_GRAB_BOX[1]),
                        C1S1_BIG_LOCK_ZOOM)
                elif part == "big_spin":
                    point = c1s1_big_spin_center()
                else:
                    cx, cy = c1s1_handle_pivot_screen()
                    point = (cx + C1S1_HANDLE_GRAB_BOX[0] * C1S1_HANDLE_ZOOM,
                             cy + C1S1_HANDLE_GRAB_BOX[1] * C1S1_HANDLE_ZOOM)
                mouse[:] = point
                sounds[:] = []
                assert c1s1_mg_hover_target(*point) == part
                c1s1_mg_update_hover()
                c1s1_mg_update_hover()
                assert _mg_get("hover_part", None) == part
                assert c1s1_mg_part_lit(part)
                assert sounds == [(C1S1_MG_HOVER_SOUND, "ogg")]

                mouse[:] = (-10000, -10000)
                c1s1_mg_update_hover()
                assert _mg_get("hover_part", None) is None
                assert not c1s1_mg_part_lit(part)
                assert len(sounds) == 1
                _mg_set("play_t", C1S1_MG_HOVER_GAP_T + 0.01)
                mouse[:] = point
                c1s1_mg_update_hover()
                assert sounds == [(C1S1_MG_HOVER_SOUND, "ogg")] * 2

                ## Потеря фокуса окна оставляет координаты SDL внутри прежней детали.
                renpy.game.interface.mouse_focused = False
                c1s1_mg_update_hover()
                assert _mg_get("hover_part", None) is None
                assert not c1s1_mg_part_lit(part)
                assert len(sounds) == 2
                renpy.game.interface.mouse_focused = True

                setattr(store, C1S1_MG_LOCK_FLAGS[C1S1_MG_LOCK_ORDER[lock_i]], True)
                c1s1_mg_update_hover()
                assert c1s1_mg_hover_target(*point) is None
                assert not c1s1_mg_part_lit(part)
                store.c1s1_mg_active = False
                assert c1s1_mg_hover_target(*point) is None
                c1s1_mg_clear_feedback()
                assert _mg_get("hover_part", None) is None
                assert not c1s1_mg_blocked_visible()
        finally:
            renpy.game.interface.mouse_focused = original_mouse_focused
            renpy.get_mouse_pos = original_mouse_pos
            store.splay = original_splay
            renpy.restart_interaction = original_restart
            c1s1_mg_reset()

    def sm_test_big_lock_blocked_feedback():
        c1s1_mg_reset()
        store.c1s1_mg_active = True
        store.c1s1_mg_lock_i = 1
        original_mouse_pos = renpy.get_mouse_pos
        original_splay = store.splay
        original_restart = renpy.restart_interaction
        mouse = list(c1s1_big_spin_center())
        sounds = []
        try:
            renpy.get_mouse_pos = lambda: tuple(mouse)
            store.splay = lambda name, **kwargs: sounds.append((name, kwargs.get("ext")))
            renpy.restart_interaction = lambda: None
            c1s1_mg_grab()
            assert _mg_get("big_p") == 0.0 and _mg_get("big_grab") == 0.0
            assert not c1s1_mg_pointer_down()
            assert c1s1_mg_blocked_visible()
            assert c1s1_mg_part_lit("big_latch")
            assert sounds == [(C1S1_MG_BLOCKED_SOUND, "ogg")]
            c1s1_mg_grab()
            assert sounds == [(C1S1_MG_BLOCKED_SOUND, "ogg")]

            _mg_set("play_t", _mg_get("blocked_at") + C1S1_MG_BLOCKED_T + 0.01)
            assert not c1s1_mg_blocked_visible()
            assert not c1s1_mg_part_lit("big_latch")
            c1s1_mg_grab()
            assert c1s1_mg_blocked_visible()
            assert sounds == [(C1S1_MG_BLOCKED_SOUND, "ogg")] * 2

            ## После отказа нижний засов и вертушка остаются доступны настоящему drag.
            mouse[:] = c1s1_lock_pos(C1S1_MG_LOCK_CENTER,
                (C1S1_BIG_LATCH_OFF[0] + C1S1_BIG_LATCH_GRAB_BOX[0],
                 C1S1_BIG_LATCH_OFF[1] + C1S1_BIG_LATCH_GRAB_BOX[1]),
                C1S1_BIG_LOCK_ZOOM)
            c1s1_mg_grab()
            assert _mg_get("big_grab") == 1.0 and c1s1_mg_pointer_down()
            mouse[0] += C1S1_BIG_LATCH_TRAVEL * C1S1_BIG_LOCK_ZOOM
            c1s1_big_step(C1S1_MG_TICK_T)
            c1s1_mg_release()
            assert _mg_get("big_p") == 1.0
            assert not c1s1_mg_blocked_visible()

            cx, cy = c1s1_big_spin_center()
            radius = C1S1_BIG_SPIN_RADIUS * C1S1_BIG_LOCK_ZOOM * 0.5
            mouse[:] = (cx + radius, cy)
            c1s1_mg_grab()
            assert _mg_get("big_grab") == 2.0 and c1s1_mg_pointer_down()
            for step in range(1, int(math.ceil(C1S1_BIG_SPIN_TURN / 90.0)) + 2):
                angle = math.radians(-min(C1S1_BIG_SPIN_TURN + 1.0, step * 90.0))
                mouse[:] = (cx + radius * math.cos(angle), cy + radius * math.sin(angle))
                c1s1_big_step(C1S1_MG_TICK_T)
            assert store.c1s1_big_lock_open and _mg_get("big_p") == 2.0
            c1s1_mg_release()
            c1s1_mg_clear_feedback()
            assert _mg_get("hover_part", None) is None
            assert not c1s1_mg_blocked_visible()
        finally:
            renpy.get_mouse_pos = original_mouse_pos
            store.splay = original_splay
            renpy.restart_interaction = original_restart
            c1s1_mg_reset()

    def sm_test_lock_idle_and_resume(lock_i):
        c1s1_mg_reset()
        store.c1s1_mg_active = True
        store.c1s1_mg_lock_i = lock_i
        for lock in C1S1_MG_LOCK_ORDER[:lock_i]:
            setattr(store, C1S1_MG_LOCK_FLAGS[lock], True)
        original_end_interaction = renpy.end_interaction
        results = []
        try:
            ## Модель и проверка завершения настоящие; ожидание ускоряет только clock.
            renpy.end_interaction = lambda result: results.append(result)
            for _ in range(480):
                _c1s1_clock_state.tick_clock = sm_time.monotonic() - 0.25
                c1s1_mg_tick()
                c1s1_mg_check_done()
            assert c1s1_mg_elapsed() >= 119.9
            assert store.c1s1_mg_lock_i == lock_i
            assert not c1s1_mg_lock_open()
            assert not store.c1s1_door_handle_open
            assert _mg_get("done") < 0.0 and not results
            assert (_mg_get("latch_p"), _mg_get("big_p"), _mg_get("handle_p")) == (0.0, 0.0, 0.0)

            for _ in range((3, 2, 1)[lock_i]):
                c1s1_mg_simplified_step()
                c1s1_mg_simplified_tick(1.0)
            assert c1s1_mg_lock_open()
            assert c1s1_mg_outcome_for_time(c1s1_mg_elapsed()) == "normal"
            c1s1_mg_check_done()
            assert not results
            _mg_set("play_t", _mg_get("play_t") + C1S1_MG_DONE_HOLD_T + 0.01)
            c1s1_mg_check_done()
            assert results == ["done"]
        finally:
            renpy.end_interaction = original_end_interaction
            c1s1_mg_reset()

    ## Подмена только координат: захват, модель движения и release настоящие.
    def sm_test_latch_drag_segments(trajectory):
        c1s1_mg_reset()
        store.c1s1_mg_active = True
        original_mouse_pos = renpy.get_mouse_pos
        mouse = list(c1s1_latch_hit_rect()[:2])
        paths = {
            "regular": ((0, -40, 0.5), (0, -40, 1.0),
                        (165, 0, 1.5), (165, 0, 2.0),
                        (0, -38, 2.5), (0, -38, 3.0)),
            "large": ((0, -240, 1.0), (0, -240, 1.0),
                      (0, 0, 1.0), (990, 0, 2.0),
                      (990, 0, 2.0), (0, -228, 3.0)),
            "reverse": ((0, -80, 1.0), (0, 40, 0.5),
                        (0, 240, 0.0), (0, -80, 1.0),
                        (330, 0, 2.0), (-165, 0, 1.5),
                        (-990, 0, 1.0), (-990, 0, 1.0),
                        (0, 240, 0.0), (0, -80, 1.0),
                        (330, 0, 2.0), (0, -38, 2.5),
                        (0, 228, 2.0), (0, 228, 2.0),
                        (0, -76, 3.0)),
        }
        try:
            renpy.get_mouse_pos = lambda position=mouse: tuple(position)
            c1s1_mg_grab()
            assert c1s1_mg_pointer_down() and _mg_get("latch_grab") == 1.0
            for dx, dy, expected in paths[trajectory]:
                mouse[0] += dx
                mouse[1] += dy
                c1s1_latch_step(C1S1_MG_TICK_T)
                assert abs(_mg_get("latch_p") - expected) < 0.000001, (trajectory, dx, dy, expected, _mg_get("latch_p"))
                assert store.c1s1_latch_open == (expected == 3.0)
                assert _mg_get("latch_grab") == (0.0 if expected == 3.0 else 1.0)
            assert c1s1_mg_pointer_down()
            c1s1_mg_release()
            assert not c1s1_mg_pointer_down()
        finally:
            renpy.get_mouse_pos = original_mouse_pos
            c1s1_mg_reset()

    def sm_test_latch_drag_release(stop_at):
        c1s1_mg_reset()
        store.c1s1_mg_active = True
        original_mouse_pos = renpy.get_mouse_pos
        mouse = list(c1s1_latch_hit_rect()[:2])
        try:
            renpy.get_mouse_pos = lambda position=mouse: tuple(position)
            c1s1_mg_grab()
            for segment, (vx, vy) in enumerate(C1S1_LATCH_PATH):
                fraction = max(0.0, min(1.0, stop_at - segment))
                if fraction == 0.0:
                    break
                mouse[0] += vx * C1S1_LATCH_ZOOM * fraction
                mouse[1] += vy * C1S1_LATCH_ZOOM * fraction
                c1s1_latch_step(C1S1_MG_TICK_T)
            assert abs(_mg_get("latch_p") - stop_at) < 0.000001
            c1s1_mg_release()
            assert not c1s1_mg_pointer_down() and _mg_get("latch_grab") == 0.0
            c1s1_latch_step(C1S1_LATCH_RETURN_T)
            expected = stop_at if 1.0 <= stop_at <= 2.0 else float(int(stop_at))
            assert abs(_mg_get("latch_p") - expected) < 0.000001
            assert not store.c1s1_latch_open
            ## После отпускания повторный захват движущейся детали остаётся рабочим.
            mouse[:] = c1s1_latch_hit_rect()[:2]
            c1s1_mg_grab()
            assert c1s1_mg_pointer_down() and _mg_get("latch_grab") == 1.0
        finally:
            renpy.get_mouse_pos = original_mouse_pos
            c1s1_mg_reset()

testcase c1s1_lock_hover_feedback:
    $ sm_test_lock_hover_feedback()

testcase c1s1_big_lock_blocked_feedback:
    parameter reduce_motion = [False, True]
    $ persistent.sm_reduce_motion = reduce_motion
    $ sm_test_big_lock_blocked_feedback()

testcase c1s1_blocked_hint_screen:
    $ c1s1_mg_reset()
    $ c1s1_mg_lock_i = 1
    $ c1s1_mg_active = True
    run Show("c1s1_locks_minigame")
    assert not id "c1s1_mg_blocked_hint"
    run Function(c1s1_mg_blocked_feedback)
    assert id "c1s1_mg_blocked_hint" timeout 0.5
    pause 1.4
    assert not id "c1s1_mg_blocked_hint"
    run Hide("c1s1_locks_minigame")
    $ c1s1_mg_reset()

testcase c1s1_lock_idle_and_resume:
    parameter lock_i = [0, 1, 2]
    $ sm_test_lock_idle_and_resume(lock_i)

testcase c1s1_latch_drag_segments:
    parameter trajectory = ["regular", "large", "reverse"]
    $ sm_test_latch_drag_segments(trajectory)

testcase c1s1_latch_drag_release:
    parameter stop_at = [0.5, 1.0, 1.5, 2.0, 2.5]
    $ sm_test_latch_drag_release(stop_at)
