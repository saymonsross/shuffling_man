## PATH TUNER · ядро (dev-only)
## Рисование spline-траектории мышью поверх сцены и генерация ATL с knot.
## Превью считает та же функция движка, что исполняет ATL
## (renpy.atl.interpolate_spline), поэтому призрак и код совпадают точно.
## Использует helpers Position Tuner (pt_showing, _pt_num...) — папка
## position_tuner/ обязана лежать рядом. Документация — README.*.

define -30 PATH_HOTKEY = "K_F6"

define -30 PATH_UNDO_LIMIT = 1000
define -30 PATH_COALESCE_T = 0.35
define -30 PATH_STEP = 1
define -30 PATH_STEP_BIG = 10
define -30 PATH_HIT_R = 14
define -30 PATH_LOOP_HOLD = 0.6
define -30 PATH_SAMPLES_PER_SEG = 24
define -30 PATH_GHOST_ALPHA = 0.6

define -30 PATH_COLOR_CURVE = "#4db8ff"
define -30 PATH_COLOR_POINT = "#ffd166"
define -30 PATH_COLOR_SEL = "#ff3860"
define -30 PATH_COLOR_HANDLE = "#9fffcf"
define -30 PATH_COLOR_HANDLE_LINE = "#9fffcf55"

## Порядок перебора кнопкой.
define -30 PATH_WARPER_ORDER = (
    "linear", "ease", "easein", "easeout",
    "ease_quad", "easein_quad", "easeout_quad",
    "ease_cubic", "easein_cubic", "easeout_cubic",
    "ease_expo", "easein_expo", "easeout_expo",
    "ease_back", "easein_back", "easeout_back",
    "ease_elastic", "ease_bounce",
)

define -30 PATH_ROT_MODES = ("none", "fixed", "tangent")
define -30 PATH_ROT_TITLES = {"none": "нет", "fixed": "фикс. значения", "tangent": "по касательной"}


init -20 python:

    import math as _path_math
    import time as _path_clock
    import collections as _path_collections
    import pygame_sdl2 as _path_pygame

    def _path_pos_typ():
        return renpy.atl.PROPERTIES["pos"]

    def _path_warper(name):
        return renpy.atl.warpers.get(name, lambda t: t)

    def path_warper_list():
        return [w for w in PATH_WARPER_ORDER if w in renpy.atl.warpers]

    def _path_int(p):
        return (int(round(p[0])), int(round(p[1])))


    class PathModel(python_object):
        """python_object — состояние инструмента вне rollback и сейвов."""

        def __init__(self):
            self.points = python_list()
            self.h_out = None                # ручки касательных старта/конца; None = авто
            self.h_in = None
            self.sel = None                  # ("p", i) | ("h", "out") | ("h", "in")
            self.duration = 2.0
            self.warper = "easein"
            self.rot_mode = "none"
            self.rot_from = 0.0
            self.rot_to = 0.0
            self.rot_offset = 0.0
            self.sprite = None
            self.anchor = (0.5, 0.5)
            self.playing = True
            self.play_t0 = _path_clock.time()
            self.scrub = 0.0
            self.side = "right"
            self.collapsed = False
            self.panel_rect = (0, 0, 0, 0)
            self.status = ""
            self.dragging = False
            self.drag_from = None
            self._len_key = None
            self._len_val = 0.0
            self.undo = _path_collections.deque(maxlen=PATH_UNDO_LIMIT)
            self.redo = _path_collections.deque(maxlen=PATH_UNDO_LIMIT)
            self._last_key = None
            self._last_t = 0.0


    def path_snapshot():
        m = path_model
        return (tuple(m.points), m.h_out, m.h_in)

    def path_restore(snap):
        m = path_model
        m.points = python_list(snap[0])
        m.h_out, m.h_in = snap[1], snap[2]
        if m.sel and m.sel[0] == "p" and m.sel[1] >= len(m.points):
            m.sel = None
        ## Ручки существуют только при двух и более точках.
        if m.sel and m.sel[0] == "h" and len(m.points) < 2:
            m.sel = None

    def path_push(label, key=None, snap=None):
        """key склеивает только серию однотипных правок (nudge) в один шаг undo."""
        m = path_model
        now = _path_clock.time()
        if key is not None and key == m._last_key and (now - m._last_t) < PATH_COALESCE_T and m.undo:
            m._last_t = now
            return
        m.undo.append((label, snap if snap is not None else path_snapshot()))
        m.redo.clear()
        m._last_key = key
        m._last_t = now

    def path_undo():
        m = path_model
        if not m.undo:
            m.status = "отменять нечего"
            return
        label, snap = m.undo.pop()
        m.redo.append((label, path_snapshot()))
        path_restore(snap)
        m._last_key = None
        m.status = "отменено: " + label

    def path_redo():
        m = path_model
        if not m.redo:
            m.status = "повторять нечего"
            return
        label, snap = m.redo.pop()
        m.undo.append((label, path_snapshot()))
        path_restore(snap)
        m._last_key = None
        m.status = "возвращено: " + label


init -20 python:

    def path_handle_out():
        pts = path_model.points
        if len(pts) < 2:
            return None
        if path_model.h_out is not None:
            return path_model.h_out
        (x0, y0), (x1, y1) = pts[0], pts[1]
        return (x0 + (x1 - x0) / 3.0, y0 + (y1 - y0) / 3.0)

    def path_handle_in():
        pts = path_model.points
        if len(pts) < 2:
            return None
        if path_model.h_in is not None:
            return path_model.h_in
        (x0, y0), (x1, y1) = pts[-1], pts[-2]
        return (x0 + (x1 - x0) / 3.0, y0 + (y1 - y0) / 3.0)

    def path_knots():
        """N==2 — кубическая Безье, ручки и есть контрольные точки.
        N>=3 — Catmull-Rom: крайние knot — фантомы вне кривой. A = P1 - 6*T0
        даёт скорость 3*T0 внутри крайнего сегмента — ручка работает как
        безье-касательная своего сегмента и не зависит от числа точек;
        авто-ручка (треть сегмента) сводится к классическому зеркальному
        фантому 2*P0 - P1."""
        pts = path_model.points
        n = len(pts)
        if n < 2:
            return python_list()
        ho, hi = path_handle_out(), path_handle_in()
        if n == 2:
            if path_model.h_out is None and path_model.h_in is None:
                return python_list()
            return python_list([_path_int(ho), _path_int(hi)])
        t0 = (ho[0] - pts[0][0], ho[1] - pts[0][1])
        t1 = (pts[-1][0] - hi[0], pts[-1][1] - hi[1])
        a = (pts[1][0] - 6.0 * t0[0], pts[1][1] - 6.0 * t0[1])
        b = (pts[-2][0] + 6.0 * t1[0], pts[-2][1] + 6.0 * t1[1])
        return python_list([_path_int(a)] + [_path_int(p) for p in pts[1:-1]] + [_path_int(b)])

    def path_spline():
        pts = path_model.points
        if len(pts) < 2:
            return python_list()
        return python_list([_path_int(pts[0])] + list(path_knots()) + [_path_int(pts[-1])])

    def _path_scalar_px(v, total):
        """Движок возвращает position(absolute, relative), не float."""
        a = getattr(v, "absolute", None)
        if a is not None:
            return float(a) + float(getattr(v, "relative", 0.0) or 0.0) * total
        return float(v)

    def path_pos_at(u):
        """Позиция при завершённости u (уже после warper) — движковой функцией."""
        pts = path_model.points
        if not pts:
            return (0.0, 0.0)
        spline = path_spline()
        if not spline:
            return (float(pts[0][0]), float(pts[0][1]))
        v = renpy.atl.interpolate_spline(u, spline, _path_pos_typ())
        return (_path_scalar_px(v[0], config.screen_width),
                _path_scalar_px(v[1], config.screen_height))

    def _path_tangent_deg(t):
        """Угол касательной в параметре сплайна t (без warper); экранный y вниз."""
        eps = 1e-3
        a = path_pos_at(max(0.0, t - eps))
        b = path_pos_at(min(1.0, t + eps))
        dx, dy = b[0] - a[0], b[1] - a[1]
        if abs(dx) < 1e-9 and abs(dy) < 1e-9:
            return 0.0
        return _path_math.degrees(_path_math.atan2(dy, dx))

    def path_point_angles():
        """Углы касательной в опорных точках, развёрнутые в непрерывный ряд."""
        n = len(path_model.points)
        if n < 2:
            return python_list()
        out = python_list()
        for i in range(n):
            a = _path_tangent_deg(i / float(n - 1))
            if out:
                while a - out[-1] > 180.0:
                    a -= 360.0
                while a - out[-1] < -180.0:
                    a += 360.0
            out.append(a)
        return out

    def path_rot_spline():
        """Сплайн угла для режима tangent, зеркалит структуру pos-сплайна:
        те же количества knot — сектора Catmull-Rom совпадают по времени."""
        m = path_model
        angles = path_point_angles()
        if len(angles) < 2:
            return python_list()
        off = m.rot_offset
        angles = [a + off for a in angles]
        if len(angles) == 2:
            return python_list(angles)
        aa = 2.0 * angles[0] - angles[1]
        ab = 2.0 * angles[-1] - angles[-2]
        return python_list([angles[0], aa] + angles[1:-1] + [ab, angles[-1]])

    def path_rot_at(u):
        m = path_model
        if m.rot_mode == "none" or len(m.points) < 2:
            return None
        if m.rot_mode == "fixed":
            spline = [m.rot_from, m.rot_to]
        else:
            spline = path_rot_spline()
            if not spline:
                return None
        return float(renpy.atl.interpolate_spline(u, spline, float))

    def path_length():
        m = path_model
        if len(m.points) < 2:
            return 0.0
        key = path_snapshot()
        if key == m._len_key:
            return m._len_val
        n = PATH_SAMPLES_PER_SEG * (len(m.points) - 1)
        total = 0.0
        prev = path_pos_at(0.0)
        for i in range(1, n + 1):
            cur = path_pos_at(i / float(n))
            total += _path_math.hypot(cur[0] - prev[0], cur[1] - prev[1])
            prev = cur
        m._len_key = key
        m._len_val = total
        return total


init -20 python:

    def path_time01():
        m = path_model
        if not m.playing:
            return m.scrub
        cycle = (_path_clock.time() - m.play_t0) % (m.duration + PATH_LOOP_HOLD)
        t = min(cycle / m.duration, 1.0)
        m.scrub = t     # пауза продолжит с текущего t
        return t

    def path_toggle_play():
        m = path_model
        if m.playing:
            m.playing = False
        else:
            m.play_t0 = _path_clock.time() - m.scrub * m.duration
            m.playing = True

    def path_set_duration(delta):
        m = path_model
        m.duration = max(0.1, round(m.duration + delta, 2))

    def path_cycle_warper(step=1):
        m = path_model
        names = path_warper_list()
        if not names:
            return
        i = names.index(m.warper) if m.warper in names else 0
        m.warper = names[(i + step) % len(names)]

    def path_cycle_rot_mode():
        m = path_model
        i = PATH_ROT_MODES.index(m.rot_mode)
        m.rot_mode = PATH_ROT_MODES[(i + 1) % len(PATH_ROT_MODES)]

    def path_adjust(field, delta):
        setattr(path_model, field, round(getattr(path_model, field) + delta, 1))

    def path_cycle_anchor(step=1):
        m = path_model
        cur = PT_ANCHORS.index(m.anchor) if m.anchor in PT_ANCHORS else -1
        m.anchor = PT_ANCHORS[(cur + step) % len(PT_ANCHORS)]

    def path_pick_sprite(name):
        path_model.sprite = name

    def path_sel_title():
        sel = path_model.sel
        if sel is None:
            return ""
        if sel[0] == "p":
            return "точка %d" % sel[1]
        return "ручка старта" if sel[1] == "out" else "ручка конца"

    def path_nudge(dx, dy, big=False):
        m = path_model
        if m.sel is None:
            return
        s = PATH_STEP_BIG if big else PATH_STEP
        path_push("сдвиг: " + path_sel_title(), key="nudge:" + str(m.sel))
        _path_move_sel(dx * s, dy * s)

    def _path_drag_handles(i, dx, dy):
        """Ручка закреплена за своей крайней точкой и едет вместе с ней."""
        m = path_model
        if i == 0 and m.h_out is not None:
            m.h_out = (m.h_out[0] + dx, m.h_out[1] + dy)
        if i == len(m.points) - 1 and m.h_in is not None:
            m.h_in = (m.h_in[0] + dx, m.h_in[1] + dy)

    def _path_move_sel(dx, dy):
        m = path_model
        if m.sel is None:
            return
        kind, which = m.sel
        if kind == "p":
            x, y = m.points[which]
            m.points[which] = (int(round(x + dx)), int(round(y + dy)))
            _path_drag_handles(which, int(round(dx)), int(round(dy)))
        elif which == "out":
            ho = path_handle_out()
            if ho is not None:
                m.h_out = (int(round(ho[0] + dx)), int(round(ho[1] + dy)))
        else:
            hi = path_handle_in()
            if hi is not None:
                m.h_in = (int(round(hi[0] + dx)), int(round(hi[1] + dy)))

    def _path_set_sel_pos(x, y):
        m = path_model
        if m.sel is None:
            return
        kind, which = m.sel
        p = (int(round(x)), int(round(y)))
        if kind == "p":
            old = m.points[which]
            m.points[which] = p
            _path_drag_handles(which, p[0] - old[0], p[1] - old[1])
        elif which == "out":
            m.h_out = p
        else:
            m.h_in = p

    def path_delete_sel():
        m = path_model
        if m.sel is None or m.sel[0] != "p":
            m.status = "выберите опорную точку"
            return
        path_push("удаление: " + path_sel_title())
        i = m.sel[1]
        ## Ручка закреплена за своей крайней точкой — уходит вместе с ней.
        if i == 0:
            m.h_out = None
        if i == len(m.points) - 1:
            m.h_in = None
        del m.points[i]
        m.sel = None
        if len(m.points) < 2:
            m.h_out = None
            m.h_in = None
        m.status = "точка удалена"

    def path_clear():
        m = path_model
        if not m.points and m.h_out is None and m.h_in is None:
            return
        path_push("очистка пути")
        m.points = python_list()
        m.h_out = None
        m.h_in = None
        m.sel = None
        m.status = "путь очищен"

    def path_reset_handles():
        m = path_model
        if m.h_out is None and m.h_in is None:
            return
        path_push("сброс ручек")
        m.h_out = None
        m.h_in = None
        m.status = "ручки снова авто"

    def path_open():
        m = path_model
        m.status = ""
        ## Закрытие с зажатой кнопкой не должно оставить вечный drag.
        path_grab._grab = None
        m.dragging = False
        m.drag_from = None
        ## Два тюнера с mouse-захватом одновременно глушат друг друга.
        if renpy.has_screen("position_tuner") and renpy.get_screen("position_tuner"):
            renpy.hide_screen("position_tuner")
        shown = pt_showing()
        if m.sprite not in shown:
            m.sprite = shown[-1] if shown else None
        if m.playing:
            m.play_t0 = _path_clock.time()


init -20 python:

    def _path_fmt_angle(a):
        return _pt_num(round(a, 1))

    def path_atl_lines():
        """Строки ATL для вставки в show-блок. transform_anchor True обязателен
        при rotate — правило rotate-transform-anchor."""
        m = path_model
        pts = m.points
        if len(pts) < 2:
            return python_list()
        p0, pend = _path_int(pts[0]), _path_int(pts[-1])
        rot0 = path_rot_at(0.0)

        setup = "anchor %s pos %s" % (_pt_pair(m.anchor), _pt_pair(p0))
        if rot0 is not None:
            setup += " transform_anchor True rotate %s" % _path_fmt_angle(rot0)

        interp = "%s %s pos %s" % (m.warper, _pt_num(m.duration), _pt_pair(pend))
        for kn in path_knots():
            interp += " knot %s" % _pt_pair(kn)

        if m.rot_mode == "fixed":
            interp += " rotate %s" % _path_fmt_angle(m.rot_to)
        elif m.rot_mode == "tangent":
            spline = path_rot_spline()
            interp += " rotate %s" % _path_fmt_angle(spline[-1])
            for a in spline[1:-1]:
                interp += " knot %s" % _path_fmt_angle(a)

        return python_list([setup, interp])

    def path_atl_text():
        return "\n".join(path_atl_lines())

    def path_show_text():
        lines = path_atl_lines()
        if not lines:
            return ""
        tag = path_model.sprite or "sprite"
        return "show %s:\n" % tag + "\n".join("    " + l for l in lines)

    def path_info_text():
        m = path_model
        n = len(m.points)
        lines = python_list()
        if n < 2:
            lines.append("{color=#f66}кликните по сцене — минимум две точки{/color}")
            if n == 1:
                lines.append("{color=#aaa}старт{/color} %s" % _pt_pair(_path_int(m.points[0])))
            return "\n".join(lines)
        mode = "кубическая Безье" if n == 2 else ("Catmull-Rom · %d точек" % n)
        length = path_length()
        t = m.scrub
        lines.append("{color=#9f9}{size=22}%s{/size}{/color}" % mode)
        lines.append("{color=#aaa}длительность{/color} %s с   {color=#aaa}warper{/color} %s"
                     % (_pt_num(m.duration), m.warper))
        lines.append("{color=#aaa}длина{/color} %d px   {color=#aaa}средняя скорость{/color} %d px/с"
                     % (int(length), int(length / m.duration)))
        lines.append("{color=#aaa}поворот{/color} %s   {color=#aaa}anchor{/color} %s"
                     % (PATH_ROT_TITLES[m.rot_mode], _pt_pair(m.anchor)))
        lines.append("{color=#aaa}t{/color} %.2f   {color=#aaa}спрайт{/color} %s"
                     % (t, m.sprite or "плейсхолдер"))
        if m.sel:
            lines.append("{color=#7bd}выбрано: %s{/color}"
                         % ("точка %d" % m.sel[1] if m.sel[0] == "p"
                            else ("ручка старта" if m.sel[1] == "out" else "ручка конца")))
        return "\n".join(lines)

    def path_info_dd(st, at):
        return Text(path_info_text(), style="path_info", substitute=False), \
            (0.0 if path_model.dragging else 0.15)

    def path_head_text():
        m = path_model
        bits = python_list()
        bits.append("{color=#888}undo %d / redo %d{/color}" % (len(m.undo), len(m.redo)))
        if m.status:
            bits.append("{color=#7bd}%s{/color}" % m.status)
        return "   ".join(bits)


init -20 python:

    class PathSurface(renpy.Displayable):
        """draw рисует под панелью; grab стоит последним ребёнком экрана
        и получает события первым."""

        def __init__(self, mode="draw", **kwargs):
            super(PathSurface, self).__init__(**kwargs)
            self.mode = mode
            self._solids = python_dict()
            self._texts = python_dict()
            self._img = None
            self._img_key = None
            self._grab = None
            self._grab_was_add = False

        def _solid(self, color):
            d = self._solids.get(color)
            if d is None:
                d = Solid(color)
                self._solids[color] = d
            return d

        def _label(self, txt):
            d = self._texts.get(txt)
            if d is None:
                d = Text(txt, size=14, color="#ffffffcc", outlines=[(1, "#000000aa", 0, 0)])
                self._texts[txt] = d
            return d

        def _ghost(self, name):
            if name != self._img_key:
                self._img_key = name
                try:
                    self._img = renpy.displayable(name) if name else None
                except Exception:
                    self._img = None
            if self._img is None:
                return Transform(self._solid("#8fd4ff66"), xysize=(110, 110))
            return self._img

        def _dot(self, rv, color, x, y, size, st, at):
            half = size // 2
            rv.blit(renpy.render(self._solid(color), size, size, st, at),
                    (int(x) - half, int(y) - half))

        def _dotline(self, rv, color, a, b, st, at):
            n = max(2, int(_path_math.hypot(b[0] - a[0], b[1] - a[1]) / 14.0))
            for i in range(n + 1):
                t = i / float(n)
                self._dot(rv, color, a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, 3, st, at)

        def render(self, width, height, st, at):
            rv = renpy.Render(width, height)
            if self.mode != "draw":
                return rv

            ## Модель меняется вне screen tree — перерисовку просим сами.
            m = path_model
            renpy.redraw(self, 0 if (m.playing or m.dragging) else 1.0 / 30.0)

            pts = m.points
            n = len(pts)

            if n >= 2:
                samples = PATH_SAMPLES_PER_SEG * (n - 1)
                for i in range(samples + 1):
                    x, y = path_pos_at(i / float(samples))
                    self._dot(rv, PATH_COLOR_CURVE, x, y, 3, st, at)

                for which, endp in (("out", pts[0]), ("in", pts[-1])):
                    h = path_handle_out() if which == "out" else path_handle_in()
                    self._dotline(rv, PATH_COLOR_HANDLE_LINE, endp, h, st, at)
                    sel = (m.sel == ("h", which))
                    self._dot(rv, PATH_COLOR_SEL if sel else PATH_COLOR_HANDLE,
                              h[0], h[1], 11 if sel else 9, st, at)

            for i, (x, y) in enumerate(pts):
                sel = (m.sel == ("p", i))
                self._dot(rv, PATH_COLOR_SEL if sel else PATH_COLOR_POINT,
                          x, y, 13 if sel else 11, st, at)
                rv.blit(renpy.render(self._label(str(i)), 40, 24, st, at), (int(x) + 10, int(y) - 24))

            if n >= 2:
                u = _path_warper(m.warper)(path_time01())
                gx, gy = path_pos_at(u)
                rot = path_rot_at(u)
                ghost = Transform(
                    self._ghost(m.sprite),
                    pos=(int(round(gx)), int(round(gy))), anchor=m.anchor,
                    rotate=rot, transform_anchor=True, alpha=PATH_GHOST_ALPHA,
                )
                rv.blit(renpy.render(Fixed(ghost, xysize=(width, height)),
                                     width, height, st, at), (0, 0))
            return rv

        def _hit(self, x, y):
            m = path_model
            if len(m.points) >= 2:
                for which, h in (("out", path_handle_out()), ("in", path_handle_in())):
                    if _path_math.hypot(x - h[0], y - h[1]) <= PATH_HIT_R:
                        return ("h", which)
            ## Поздние точки приоритетнее при наложении.
            for i in range(len(m.points) - 1, -1, -1):
                px, py = m.points[i]
                if _path_math.hypot(x - px, y - py) <= PATH_HIT_R:
                    return ("p", i)
            return None

        def event(self, ev, x, y, st):
            if self.mode != "grab":
                return None
            m = path_model

            if self._grab is None:
                if ev.type == _path_pygame.MOUSEBUTTONDOWN and ev.button == 1:
                    px, py, pw, ph = m.panel_rect
                    if px <= x < px + pw and py <= y < py + ph:
                        return None      # клики по панели — кнопкам
                    hit = self._hit(x, y)
                    if hit is None:
                        path_push("новая точка", snap=path_snapshot())
                        m.points.append((int(x), int(y)))
                        m.sel = ("p", len(m.points) - 1)
                        self._grab_was_add = True
                        self._grab = (0, 0)
                    else:
                        m.sel = hit
                        self._grab_was_add = False
                        self._grab = (0, 0)
                        m.drag_from = path_snapshot()
                    m.dragging = True
                    renpy.restart_interaction()
                    raise renpy.IgnoreEvent()
                return None

            if ev.type == _path_pygame.MOUSEMOTION:
                _path_set_sel_pos(x, y)
                renpy.redraw(path_draw, 0)
                raise renpy.IgnoreEvent()

            if ev.type == _path_pygame.MOUSEBUTTONUP and ev.button == 1:
                self._grab = None
                m.dragging = False
                if (not self._grab_was_add and m.drag_from is not None
                        and m.drag_from != path_snapshot()):
                    path_push("перетаскивание: " + path_sel_title(), snap=m.drag_from)
                m.drag_from = None
                renpy.restart_interaction()
                raise renpy.IgnoreEvent()

            return None

        def visit(self):
            if self.mode != "draw":
                return []
            c = self._ghost(path_model.sprite)
            return [c] if c is not None else []


init -10 python:
    path_model = PathModel()
    path_draw = PathSurface("draw")
    path_grab = PathSurface("grab")
