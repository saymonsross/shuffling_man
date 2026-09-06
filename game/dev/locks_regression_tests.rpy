init python:
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

testcase c1s1_latch_drag_segments:
    parameter trajectory = ["regular", "large", "reverse"]
    $ sm_test_latch_drag_segments(trajectory)

testcase c1s1_latch_drag_release:
    parameter stop_at = [0.5, 1.0, 1.5, 2.0, 2.5]
    $ sm_test_latch_drag_release(stop_at)
