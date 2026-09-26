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

    def sm_test_door_prompt_parts():
        prompt = renpy.get_displayable("c1s1_locks_open_door", "door_prompt")
        buttons, rattles = [], []
        def collect(displayable):
            if isinstance(displayable, renpy.display.behavior.Button):
                buttons.append(displayable)
            if getattr(displayable, "atl", None) is c1s1_mg_button_rattle.atl:
                rattles.append(displayable)
            assert getattr(displayable, "atl", None) is not follow_camera.atl
        prompt.visit_all(collect)
        assert len(buttons) == len(rattles) == 1
        return buttons[0], rattles[0]

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
            camera_shake_f(4.0, 0.04, None, "sm_test_prediction", Transform(), 0.0, 0.0)
            focus_camera_f((0.44, 0.44), None, "sm_test_prediction", Transform(zoom=1.14), 0.0, 0.0)
            c1s1_mg_camera_f("sm_test_prediction", Transform(), 0.0, 0.0)
            parallax_bg_f(Transform(), 0.0, 0.0)
            parallax_near_f(Transform(), 0.0, 0.0)
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
                focus_camera_f(C1S1_LAMP_FOCUS, None, key, camera_transform, 0.0, 0.0)
                widget = Transform(zoom=1.02)
                follow_camera_f(key, 1.02, widget, 0.0, 0.0)
                bx, by = _focus_offset(C1S1_LAMP_FOCUS, None, zoom_value)
                assert widget.zoom == zoom_value
                assert abs(widget.xoffset - bx) < 0.000001
                assert abs(widget.yoffset - by) < 0.000001

            ## Новая камера двери не должна наследовать zoom/focus из снимка лампы.
            camera_transform = Transform(zoom=C1S1_MG_ZOOM, rotate=0.0)
            c1s1_mg_camera_f(key, camera_transform, 0.0, 0.0)
            follow_camera_f(key, 1.02, widget, 0.0, 0.0)
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
    python hide:
        button, rattle = sm_test_door_prompt_parts()
        assert button.get_placement()[:4] == (
            config.screen_width // 2, config.screen_height // 2, 0.5, 0.5)
        assert button.window_size == C1S1_LOCKS_BTN_SIZE
        assert rattle.transform_anchor

    ## Настоящий удар двигает только внутренний визуал; хит-зона остаётся в центре.
    assert eval (_mg_get("shake_a") > 0.0) timeout 3.0
    if eval (reduce_motion):
        assert eval (all(abs(getattr(sm_test_door_prompt_parts()[1], prop) or 0.0) < 0.00001
            for prop in ("xoffset", "yoffset", "rotate")))
    else:
        assert eval (abs(sm_test_door_prompt_parts()[1].xoffset or 0.0) >= 1.0) timeout 3.0
    move pos (960, 540)
    pause 0.15
    python hide:
        button, rattle = sm_test_door_prompt_parts()
        assert button.get_placement()[:4] == (
            config.screen_width // 2, config.screen_height // 2, 0.5, 0.5)
        assert button.window_size == C1S1_LOCKS_BTN_SIZE
    click pos (960, 540)
    assert screen "c1s1_locks_minigame" timeout 10.0
    assert eval (c1s1_mg_active and c1s1_mg_knocking)
    run MainMenu(confirm=False)

## Под test параллакс выключен ради эталонных кадров, поэтому здесь он включается подменой.
testcase parallax_layer_follow:
    parameter reduce_motion = [False, True]

    $ persistent.sm_reduce_motion = reduce_motion
    python hide:
        original_clock = _fx_frame_time
        original_active = sm_parallax_active
        original_mouse_pos = renpy.get_mouse_pos
        original_state = dict(_fx_state)
        clock = [0.0]
        w, h = config.screen_width, config.screen_height
        try:
            store._fx_frame_time = lambda value=clock: value[0]
            store.sm_parallax_active = lambda: True
            renpy.get_mouse_pos = lambda: (0, 0)
            for state_key in list(_fx_state):
                name = state_key[0] if isinstance(state_key, tuple) else state_key
                if name in ("parallax_level", "parallax_mx", "parallax_my"):
                    del _fx_state[state_key]

            layer = Transform()
            for frame in range(120):
                clock[0] += 1.0 / 60.0
                parallax_bg_f(layer, 0.0, 0.0)
                assert w * (layer.zoom - 1.0) / 2.0 >= abs(layer.xoffset) - 0.000001
                assert h * (layer.zoom - 1.0) / 2.0 >= abs(layer.yoffset) - 0.000001
            near = Transform()
            parallax_near_f(near, 0.0, 0.0)
            if sm_reduced_motion():
                assert layer.zoom == 1.0 and layer.xoffset == 0.0 and layer.yoffset == 0.0
                assert near.xoffset == 0.0 and near.yoffset == 0.0
            else:
                ## Мышь в левом верхнем углу: слой уходит вправо-вниз, ближний план — дальше.
                assert layer.zoom > 1.0 and layer.xoffset > 10.0 and layer.yoffset > 5.0
                assert near.xoffset > 1.0 and near.yoffset > 0.5

            ## World-space UI попадает туда же, куда камера и слой переносят точку мира.
            key = "sm_test_parallax_cam"
            camera_transform = Transform(zoom=1.1, rotate=0.0)
            focus_camera_f(C1S1_LAMP_FOCUS, None, key, camera_transform, 0.0, 0.0)
            widget = Transform()
            follow_camera_f(key, 1.02, widget, 0.0, 0.0)
            for qx, qy in ((300.0, 200.0), (1700.0, 950.0)):
                sx = w / 2.0 + camera_transform.zoom * (qx - w / 2.0) + camera_transform.xoffset
                sy = h / 2.0 + camera_transform.zoom * (qy - h / 2.0) + camera_transform.yoffset
                sx = w / 2.0 + layer.zoom * (sx - w / 2.0) + layer.xoffset
                sy = h / 2.0 + layer.zoom * (sy - h / 2.0) + layer.yoffset
                ux = w / 2.0 + widget.zoom * (qx - w / 2.0) + widget.xoffset
                uy = h / 2.0 + widget.zoom * (qy - h / 2.0) + widget.yoffset
                assert abs(sx - ux) < 0.001 and abs(sy - uy) < 0.001, (sx, ux, sy, uy)

            ## Выключение гасит сдвиг и зум вместе: край кадра не открывается.
            store.sm_parallax_active = lambda: False
            for frame in range(600):
                clock[0] += 1.0 / 60.0
                parallax_bg_f(layer, 0.0, 0.0)
                assert w * (layer.zoom - 1.0) / 2.0 >= abs(layer.xoffset) - 0.000001
                assert h * (layer.zoom - 1.0) / 2.0 >= abs(layer.yoffset) - 0.000001
            assert abs(layer.zoom - 1.0) < 0.0001 and abs(layer.xoffset) < 0.01
        finally:
            store._fx_frame_time = original_clock
            store.sm_parallax_active = original_active
            renpy.get_mouse_pos = original_mouse_pos
            _fx_state.clear()
            _fx_state.update(original_state)
