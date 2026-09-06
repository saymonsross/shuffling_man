default sm_test_camera_zoom = 1.0

init python:
    def sm_test_camera_matches_ui(screen_name, widget_id):
        camera_transform = renpy.scene_lists().camera_transform.get("master")
        widget = renpy.get_displayable(screen_name, widget_id)
        if camera_transform is None or widget is None:
            return False
        transforms = []
        def find_parent(displayable):
            if isinstance(displayable, renpy.display.motion.Transform) and displayable.child is widget:
                transforms.append(displayable)
        renpy.get_screen(screen_name).visit_all(find_parent)
        if len(transforms) != 1:
            return False
        widget = transforms[0]
        return all(abs((getattr(camera_transform, prop) or 0.0)
            - (getattr(widget, prop) or 0.0)) < 0.00001
            for prop in ("zoom", "rotate", "xoffset", "yoffset"))

testcase fx_smoothing_frame_time:
    python hide:
        original_clock = _fx_frame_time
        original_predicting = renpy.predicting
        original_state = dict(_fx_state)
        original_rng = sm_visual_rng.getstate()
        clock = [0.0]
        try:
            store._fx_frame_time = lambda value=clock: value[0]
            for fps in (15, 30, 60, 120):
                key = "sm_test_fps_" + str(fps)
                clock[0] = 0.0
                _fx_step(key, 0.0, 0.06, 0.0)
                for frame in range(1, fps + 1):
                    clock[0] = frame / float(fps)
                    actual = _fx_step(key, -10.0, 0.06, 0.0)
                expected = -10.0 * (1.0 - 0.94 ** 60)
                assert abs(actual - expected) < 0.000001, (fps, actual, expected)

            clock[0] = 2.0
            value = _fx_step("sm_test_repeat", lambda: _fx_visual_jitter(4.0), 0.5, 0.0)
            rng = sm_visual_rng.getstate()
            state = dict(_fx_state)
            assert _fx_step("sm_test_repeat", lambda: _fx_visual_jitter(4.0), 0.5, 0.0) == value
            assert _fx_state == state and sm_visual_rng.getstate() == rng

            ## Новый transform с тем же ключом продолжает позицию, а не стартует с нуля.
            clock[0] += 1.0 / 60.0
            expected = value + (10.0 - value) * 0.5
            actual = _fx_step("sm_test_repeat", 10.0, 0.5, 0.0)
            assert abs(actual - expected) < 0.000001
            clock[0] -= 10.0
            assert _fx_step("sm_test_repeat", 10.0, 0.5, 0.0) == actual
            clock[0] += 1.0 / 60.0
            assert _fx_step("sm_test_repeat", 10.0, 0.5, 0.0) > actual

            state = dict(_fx_state)
            rng = sm_visual_rng.getstate()
            renpy.predicting = lambda: True
            _fx_step("sm_test_prediction", lambda: _fx_visual_jitter(4.0), 0.5, 0.0)
            mouse_parallax_f(10.0, 0.06, 4.0, 0.04, None, "sm_test_prediction", Transform(), 0.0, 0.0)
            focus_parallax_f((0.44, 0.44), None, 10.0, 0.06, "sm_test_prediction", Transform(zoom=1.14), 0.0, 0.0)
            c1s1_mg_camera_f(10.0, 0.06, "sm_test_prediction", Transform(), 0.0, 0.0)
            object_jitter_f(4.0, 0.5, "sm_test_prediction", Transform(), 0.0, 0.0)
            c1s1_mg_bag_f(Transform(), 0.0, 0.0)
            assert _fx_state == state and sm_visual_rng.getstate() == rng
        finally:
            store._fx_frame_time = original_clock
            renpy.predicting = original_predicting
            _fx_state.clear()
            _fx_state.update(original_state)
            sm_visual_rng.setstate(original_rng)

testcase fx_camera_snapshot:
    parameter reduce_motion = [False, True]

    $ persistent.sm_reduce_motion = reduce_motion
    python hide:
        original_state = dict(_fx_state)
        original_mouse_pos = renpy.get_mouse_pos
        try:
            renpy.get_mouse_pos = lambda: (config.screen_width // 2, config.screen_height // 2)
            key = "sm_test_snapshot"
            for zoom_value in (1.04, 1.09, 1.14):
                camera_transform = Transform(zoom=zoom_value, rotate=0.0)
                focus_parallax_f(C1S1_LAMP_FOCUS, None, 10.0, 0.06, key, camera_transform, 0.0, 0.0)
                widget = Transform(zoom=1.02)
                follow_camera_f(key, widget, 0.0, 0.0)
                bx, by = _focus_offset(C1S1_LAMP_FOCUS, None, zoom_value)
                assert widget.zoom == zoom_value
                assert abs(widget.xoffset - bx) < 0.000001
                assert abs(widget.yoffset - by) < 0.000001

            ## Новая камера двери не должна наследовать zoom/focus из снимка лампы.
            camera_transform = Transform(zoom=C1S1_MG_ZOOM, rotate=0.0)
            c1s1_mg_camera_f(8.0, 0.06, key, camera_transform, 0.0, 0.0)
            follow_camera_f(key, widget, 0.0, 0.0)
            assert widget.zoom == C1S1_MG_ZOOM
            assert widget.xoffset == camera_transform.xoffset
            assert widget.yoffset == camera_transform.yoffset
        finally:
            renpy.get_mouse_pos = original_mouse_pos
            _fx_state.clear()
            _fx_state.update(original_state)

testcase c1s1_camera_ui_alignment:
    parameter reduce_motion = [False, True]
    parameter disable_flashes = [False, True]

    $ persistent.sm_reduce_motion = reduce_motion
    $ persistent.sm_disable_flashes = disable_flashes
    run Function(dev_scene_nav_start, "chapter_1_scene_1")
    assert screen "c1s1_lamp_switch" timeout 8.0
    pause 0.2
    assert eval (sm_test_camera_matches_ui("c1s1_lamp_switch", "lamp_world"))
    $ sm_test_camera_zoom = renpy.scene_lists().camera_transform["master"].zoom
    pause 0.8
    assert eval (sm_test_camera_matches_ui("c1s1_lamp_switch", "lamp_world"))
    pause 0.03
    assert eval (sm_test_camera_matches_ui("c1s1_lamp_switch", "lamp_world"))
    pause 0.03
    assert eval (sm_test_camera_matches_ui("c1s1_lamp_switch", "lamp_world"))
    pause 0.03
    assert eval (sm_test_camera_matches_ui("c1s1_lamp_switch", "lamp_world"))
    if eval (not reduce_motion):
        assert eval (renpy.scene_lists().camera_transform["master"].zoom > sm_test_camera_zoom)
    click "Зажечь свет"
    assert screen "c1s1_metronome_start" timeout 15.0
    pause 0.1
    assert eval (sm_test_camera_matches_ui("c1s1_metronome_start", "metronome_world"))
    click "Завести метроном"
    skip fast
    assert screen "c1s1_locks_open_door" timeout 15.0
    pause 0.1
    assert eval (sm_test_camera_matches_ui("c1s1_locks_open_door", "door_world"))
    run MainMenu(confirm=False)
