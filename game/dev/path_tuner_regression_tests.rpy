## Сплайны Path Tuner: экспортные knot-списки обязаны совпадать с интерполяцией движка.

## Беспараметрический трансформ компилируется на старте: если rotate перестанет
## принимать knot (spline требует position-типы), упадёт запуск, не инструмент.
transform _path_probe_rotate_knots:
    rotate 0.0
    linear 1.0 rotate 90.0 knot -10.0 knot 40.0

testcase path_tuner_spline_math:
    python hide:
        snap = (list(path_model.points), path_model.h_out, path_model.h_in,
                path_model.rot_mode, path_model.rot_offset, path_model.sprite,
                path_model.anchor)
        try:
            ## Catmull-Rom: кривая проходит через опорные точки в t = i/(N-1).
            path_model.points = python_list([(100, 100), (500, 300), (900, 200), (1300, 600)])
            path_model.h_out = None
            path_model.h_in = None
            spline = path_spline()
            assert len(spline) == 6, spline
            for i, p in enumerate([(100, 100), (500, 300), (900, 200), (1300, 600)]):
                v = path_pos_at(i / 3.0)
                assert abs(v[0] - p[0]) <= 1.0 and abs(v[1] - p[1]) <= 1.0, (i, v, p)

            ## Авто-ручки дают классические зеркальные фантомы 2*P0-P1 и 2*Pn-Pn-1.
            assert spline[1] == (2 * 100 - 500, 2 * 100 - 300), spline[1]
            assert spline[-2] == (2 * 1300 - 900, 2 * 600 - 200), spline[-2]

            ## Ручка задаёт направление старта и не меняет смысл при N=2 и N>=3.
            path_model.points = python_list([(0, 0), (1000, 0)])
            path_model.h_out = (100, -300)
            path_model.h_in = (900, 300)
            assert path_knots() == [(100, -300), (900, 300)], path_knots()
            eps = 1e-3
            v = path_pos_at(eps)
            assert v[1] < 0 and abs(v[1] / v[0] + 3.0) < 0.1, v      # dy/dx = -300/100
            path_model.points = python_list([(0, 0), (1000, 0), (2000, 500)])
            v = path_pos_at(eps)
            assert v[1] < 0 and abs(v[1] / v[0] + 3.0) < 0.1, v

            ## Режим tangent: сплайн угла зеркалит структуру pos-сплайна,
            ## а угол в опорной точке совпадает с касательной кривой.
            path_model.rot_mode = "tangent"
            path_model.rot_offset = 0.0
            rs = path_rot_spline()
            assert len(rs) == len(path_spline()), (len(rs), len(path_spline()))
            t_mid = 0.5      # опорная точка 1 из трёх
            a = path_pos_at(t_mid - eps)
            b = path_pos_at(t_mid + eps)
            want = _path_math.degrees(_path_math.atan2(b[1] - a[1], b[0] - a[0]))
            got = path_rot_at(t_mid)
            assert abs((got - want + 180.0) % 360.0 - 180.0) < 1.0, (got, want)

            ## Прямая без ручек экспортируется без knot.
            path_model.points = python_list([(0, 0), (1000, 0)])
            path_model.h_out = None
            path_model.h_in = None
            path_model.rot_mode = "none"
            assert path_knots() == []

            ## Экспортный текст: setup + интерполяция, rotate тянет transform_anchor True.
            path_model.points = python_list([(100, 100), (500, 300), (900, 200)])
            path_model.rot_mode = "tangent"
            path_model.sprite = "test_sprite"
            path_model.anchor = (0.5, 1.0)
            lines = path_atl_lines()
            assert len(lines) == 2, lines
            assert lines[0].startswith("anchor (0.5, 1.0) pos (100, 100)"), lines[0]
            assert "transform_anchor True rotate" in lines[0], lines[0]
            assert lines[1].count("knot") == 6, lines[1]     # 3 pos-knot + 3 rotate-knot
            assert path_show_text().startswith("show test_sprite:\n    anchor"), path_show_text()
        finally:
            (path_model.points, path_model.h_out, path_model.h_in,
             path_model.rot_mode, path_model.rot_offset, path_model.sprite,
             path_model.anchor) = (python_list(snap[0]),) + snap[1:]

## Экран: хоткей, клик добавляет точку, undo убирает, Esc закрывает.
testcase path_tuner_ui_smoke:
    if not screen "main_menu":
        run MainMenu(confirm=False)
    $ path_model.points = python_list()
    $ path_model.h_out = None
    $ path_model.h_in = None
    $ path_model.sel = None

    keysym "K_F6"
    assert screen "path_tuner" timeout 1.0
    assert "Копировать ATL"

    click pos (500, 500)
    assert eval (len(path_model.points) == 1)
    click pos (800, 700)
    assert eval (len(path_model.points) == 2)

    keysym "ctrl_K_z"
    assert eval (len(path_model.points) == 1)

    keysym "K_ESCAPE"
    assert not screen "path_tuner" timeout 1.0
    $ path_model.points = python_list()
