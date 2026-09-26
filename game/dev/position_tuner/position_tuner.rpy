## POSITION TUNER · ядро (dev-only)
## Читает живые трансформы и меняет свою модель; результат копируется в буфер
## или записывается в код (position_tuner_write.rpy).
## Папка переносима и исключена из prod-сборки. Документация — README.*.

define -30 PT_UNDO_LIMIT = 1000

## Быстрые однотипные правки склеиваются в один шаг undo.
define -30 PT_COALESCE_T = 0.35

define -30 PT_STEP = 1
define -30 PT_STEP_BIG = 10
define -30 PT_STEP_ANGLE = 1.0
define -30 PT_STEP_ANGLE_BIG = 15.0

define -30 PT_ANCHORS = [
    (0.0, 0.0), (0.5, 0.5), (0.5, 1.0), (1.0, 1.0),
    (0.0, 1.0), (1.0, 0.0), (0.5, 0.0), (0.0, 0.5), (1.0, 0.5),
]

define -30 PT_GHOST_ALPHA = 0.55
define -30 PT_COLOR_BOX = "#00ff88"
define -30 PT_COLOR_DIM = "#00ff8855"
define -30 PT_COLOR_GUIDE = "#00ff8840"
define -30 PT_COLOR_MARK = "#ff3860"

define -30 PT_CALL_TEMPLATE = "at placed({pos}, {anchor}, {angle})"

define -30 PT_HOTKEY = "K_F9"


init -20 python:

    import re as _pt_re
    import time as _pt_time
    import collections as _pt_collections
    import pygame_sdl2 as _pt_pygame

    ## Сканируем все scene-слои, кроме служебных экранных и transient.
    PT_SKIP_LAYERS = ("transient", "screens", "overlay", "top")

    ## tag → layer; карта опирается на проектную уникальность image-тегов.
    _pt_tag_layer = python_dict()

    def _pt_layers():
        try:
            return [l for l in config.layers if l not in PT_SKIP_LAYERS]
        except Exception:
            return ["master"]

    def pt_layer_of(tag):
        return _pt_tag_layer.get(tag.split(" ")[0], "master")

    def pt_showing(layer=None):
        out = python_list()
        for lay in ([layer] if layer else _pt_layers()):
            try:
                tags = sorted(renpy.get_showing_tags(lay, False))
            except Exception:
                continue
            for tag in tags:
                try:
                    attrs = renpy.get_attributes(tag, lay) or ()
                except Exception:
                    attrs = ()
                _pt_tag_layer[tag] = lay
                out.append(" ".join((tag,) + tuple(attrs)))
        return out

    def pt_bounds(tag, layer=None):
        """Экранные (x, y, w, h) с учётом zoom и rotate."""
        try:
            b = renpy.get_image_bounds(tag.split(" ")[0], layer=(layer or pt_layer_of(tag)))
        except Exception:
            b = None
        if not b:
            return None
        return tuple(int(round(float(v))) for v in b)

    def _pt_live(tag, layer=None):
        """Реальные свойства живут в scene_lists, не в шаблоне get_at_list."""
        tag = tag.split(" ")[0]
        layer = layer or pt_layer_of(tag)
        try:
            sl = renpy.scene_lists()
        except Exception:
            return None
        for sle in sl.layers.get(layer, []):
            if sle.tag == tag:
                return sle.displayable
        return None

    def _pt_px(v, total):
        """int/absolute — пиксели, float — доля; absolute проверять первым."""
        if v is None:
            return None
        if isinstance(v, absolute):
            return float(v)
        if isinstance(v, float):
            return v * total
        return float(v)

    def _pt_anchor(v, size):
        """float — доля стороны, int/absolute — пиксели от края."""
        if v is None:
            return None
        if isinstance(v, absolute):
            return (float(v) / size) if size else 0.0
        if isinstance(v, float):
            return v
        return (float(v) / size) if size else 0.0

    def pt_scene_state(name):
        """Нормализует позицию в px, якорь — в доли."""
        b = pt_bounds(name)
        d = _pt_live(name)

        st = python_dict()
        st["bounds"] = b
        st["natural"] = None
        st["zoom"] = 1.0
        st["alpha"] = 1.0
        st["rotate"] = None
        st["from_scene"] = d is not None

        w = h = 0
        if d is not None:
            ch = getattr(d, "child", None)
            if ch is not None:
                try:
                    surf = renpy.render(ch, config.screen_width, config.screen_height, 0, 0)
                    w, h = surf.get_size()
                except Exception:
                    w = h = 0
            for prop, key in (("rotate", "rotate"), ("zoom", "zoom"), ("alpha", "alpha")):
                try:
                    st[key] = getattr(d, prop)
                except Exception:
                    pass
            px = _pt_px(getattr(d, "xpos", None), config.screen_width)
            py = _pt_px(getattr(d, "ypos", None), config.screen_height)
            ax = _pt_anchor(getattr(d, "xanchor", None), w)
            ay = _pt_anchor(getattr(d, "yanchor", None), h)
        else:
            px = py = ax = ay = None

        if not w and b:
            w, h = b[2], b[3]
        st["natural"] = (int(w), int(h))

        ## Fallback для displayable без явного transform.
        if px is None or py is None:
            if b:
                px, py, ax, ay = b[0], b[1], 0.0, 0.0
            else:
                px = py = 0.0
                ax = ay = 0.0
        st["pos"] = (int(round(px)), int(round(py)))
        st["anchor"] = (round(ax if ax is not None else 0.0, 4),
                        round(ay if ay is not None else 0.0, 4))
        return st


init -20 python:

    class PTTarget(python_object):
        def __init__(self, name, state):
            self.name = name
            self.scene = state
            self.pos = state["pos"]
            self.anchor = state["anchor"]
            self.rotate = state["rotate"]

        def resync(self, state):
            self.scene = state
            self.pos = state["pos"]
            self.anchor = state["anchor"]
            self.rotate = state["rotate"]

        @property
        def natural(self):
            return self.scene["natural"] or (0, 0)

        @property
        def dirty(self):
            s = self.scene
            return (self.pos != s["pos"] or self.anchor != s["anchor"]
                    or self.rotate != s["rotate"])

        def values(self):
            return (self.pos, self.anchor, self.rotate)

        def restore(self, v):
            self.pos, self.anchor, self.rotate = v


    class PTModel(python_object):
        """Наследуется от python_object — состояние инструмента не попадает
        ни в rollback, ни в сейвы игрока."""

        def __init__(self):
            self.targets = python_dict()
            self.name = None
            self.undo = _pt_collections.deque(maxlen=PT_UNDO_LIMIT)
            self.redo = _pt_collections.deque(maxlen=PT_UNDO_LIMIT)
            self.dragging = False
            self.drag_from = None
            self.side = "left"
            self.collapsed = False
            self.panel_rect = (0, 0, 0, 0)
            self.status = ""
            self._last_key = None
            self._last_t = 0.0

        def target(self):
            return self.targets.get(self.name)

        def topleft(self):
            t = self.target()
            if t is None:
                return (0, 0)
            w, h = t.natural
            ax, ay = t.anchor
            return (int(round(t.pos[0] - ax * w)), int(round(t.pos[1] - ay * h)))

        def pos_from_topleft(self, x, y):
            t = self.target()
            w, h = t.natural
            ax, ay = t.anchor
            return (int(round(x + ax * w)), int(round(y + ay * h)))

        def cycle_anchor(self, step=1):
            t = self.target()
            if t is None:
                return
            cur = PT_ANCHORS.index(t.anchor) if t.anchor in PT_ANCHORS else -1
            pt_set(t, anchor=PT_ANCHORS[(cur + step) % len(PT_ANCHORS)],
                   key="anchor:" + t.name)


init -20 python:

    def pt_push(records, label=""):
        if not records:
            return
        pt_model.undo.append((label, python_list(records)))
        pt_model.redo.clear()
        pt_model._last_key = None

    def pt_set(t, pos=None, anchor=None, rotate=None, key=None, commit=True):
        """key склеивает серию однотипных правок в один undo."""
        if t is None:
            return
        new = (pos if pos is not None else t.pos,
               anchor if anchor is not None else t.anchor,
               rotate if rotate is not None else t.rotate)
        if new == t.values():
            return

        if commit:
            now = _pt_time.time()
            merge = (
                key is not None
                and key == pt_model._last_key
                and (now - pt_model._last_t) < PT_COALESCE_T
                and len(pt_model.undo) > 0
            )
            if not merge:
                pt_push([(t.name, t.values())], key or t.name)
            pt_model._last_key = key
            pt_model._last_t = now

        t.restore(new)

    def pt_nudge(dx, dy, big=False):
        t = pt_model.target()
        if t is None:
            return
        s = PT_STEP_BIG if big else PT_STEP
        pt_set(t, pos=(t.pos[0] + dx * s, t.pos[1] + dy * s), key="move:" + t.name)

    def pt_turn(sign, big=False):
        t = pt_model.target()
        if t is None:
            return
        s = PT_STEP_ANGLE_BIG if big else PT_STEP_ANGLE
        cur = t.rotate if t.rotate is not None else 0.0
        pt_set(t, rotate=round((cur + sign * s) % 360.0, 2), key="turn:" + t.name)

    def _pt_swap(records):
        back = python_list()
        for name, values in records:
            t = pt_model.targets.get(name)
            if t is None:
                continue
            back.append((name, t.values()))
            t.restore(values)
            pt_model.name = name
        return back

    def pt_undo():
        if not pt_model.undo:
            pt_model.status = "отменять нечего"
            return
        label, records = pt_model.undo.pop()
        pt_model.redo.append((label, _pt_swap(records)))
        pt_model._last_key = None
        pt_model.status = "отменено: " + label

    def pt_redo():
        if not pt_model.redo:
            pt_model.status = "повторять нечего"
            return
        label, records = pt_model.redo.pop()
        pt_model.undo.append((label, _pt_swap(records)))
        pt_model._last_key = None
        pt_model.status = "возвращено: " + label

    def pt_reset():
        t = pt_model.target()
        if t is None:
            return
        if t.dirty:
            pt_push([(t.name, t.values())], "сброс " + t.name)
        t.resync(pt_scene_state(t.name))
        pt_model.status = "значения снова из сцены"

    def pt_sync(keep_edits=True):
        shown = pt_showing()
        for name in shown:
            t = pt_model.targets.get(name)
            state = pt_scene_state(name)
            if t is None:
                pt_model.targets[name] = PTTarget(name, state)
            elif keep_edits and t.dirty:
                t.scene = state          # сцена могла поехать, правки бережём
            else:
                t.resync(state)
        for gone in [n for n in pt_model.targets if n not in shown]:
            del pt_model.targets[gone]
        if pt_model.name not in pt_model.targets:
            pt_model.name = shown[-1] if shown else None

    def pt_pick(name):
        pt_model.name = name
        if name not in pt_model.targets:
            pt_model.targets[name] = PTTarget(name, pt_scene_state(name))

    def pt_open():
        if not config.developer:
            return
        pt_model.status = ""
        pt_sync()


init -20 python:

    def _pt_num(v):
        if v is None:
            return "—"
        if isinstance(v, int):
            return str(v)
        s = "%.4f" % float(v)
        s = s.rstrip("0")
        if s.endswith("."):
            s += "0"
        return s

    def _pt_pair(v):
        return "(%s, %s)" % (_pt_num(v[0]), _pt_num(v[1]))

    def pt_dirty_count():
        return sum(1 for t in pt_model.targets.values() if t.dirty)

    def pt_atl_text():
        t = pt_model.target()
        if t is None:
            return ""
        lines = ["anchor %s" % _pt_pair(t.anchor), "pos %s" % _pt_pair(t.pos)]
        if t.rotate is not None:
            lines.append("rotate %s" % _pt_num(t.rotate))
        return "\n".join(lines)

    def pt_call_text():
        t = pt_model.target()
        if t is None:
            return ""
        return PT_CALL_TEMPLATE.format(
            pos=_pt_pair(t.pos),
            anchor=_pt_pair(t.anchor),
            angle=_pt_num(t.rotate) if t.rotate is not None else "None",
        )

    def pt_info_text():
        """DynamicDisplayable обновляет значения прямо во время drag."""
        t = pt_model.target()
        if t is None:
            return "{color=#f66}на сцене нет спрайтов{/color}"

        s = t.scene
        w, h = t.natural
        b = s["bounds"]
        mark = "{color=#ffd166}●{/color} " if t.dirty else ""

        lines = python_list()
        lines.append("%s{b}%s{/b}" % (mark, t.name))
        lines.append("{color=#9f9}{size=30}pos %s{/size}{/color}" % _pt_pair(t.pos))
        lines.append("{color=#aaa}anchor{/color} %s   {color=#aaa}rotate{/color} %s°   "
                     "{color=#aaa}zoom{/color} %s"
                     % (_pt_pair(t.anchor), _pt_num(t.rotate), _pt_num(s["zoom"])))
        lines.append("{color=#aaa}картинка{/color} %d×%d   {color=#aaa}на экране{/color} %s"
                     % (w, h, ("%s %d×%d" % (_pt_pair((b[0], b[1])), b[2], b[3])) if b else "—"))
        if t.dirty:
            lines.append("{color=#888}в сцене: pos %s  anchor %s  rotate %s{/color}"
                         % (_pt_pair(s["pos"]), _pt_pair(s["anchor"]), _pt_num(s["rotate"])))
        elif not s["from_scene"]:
            lines.append("{color=#888}трансформа нет — значения из габаритов на экране{/color}")
        return "\n".join(lines)

    def pt_info_dd(st, at):
        return Text(pt_info_text(), style="pt_info"), (0.0 if pt_model.dragging else 0.15)

    def pt_head_text():
        bits = python_list()
        n = pt_dirty_count()
        bits.append("{color=#ffd166}● подобрано: %d{/color}" % n if n
                    else "{color=#6c6}значения как в сцене{/color}")
        bits.append("{color=#888}undo %d / redo %d{/color}" % (len(pt_model.undo), len(pt_model.redo)))
        if pt_model.status:
            bits.append("{color=#7bd}%s{/color}" % pt_model.status)
        return "   ".join(bits)


init -20 python:

    class PTSurface(renpy.Displayable):
        """draw рисует снизу; grab стоит последним и первым получает события."""

        def __init__(self, mode="draw", **kwargs):
            super(PTSurface, self).__init__(**kwargs)
            self.mode = mode
            self._img = None
            self._img_key = None
            self._frames = python_dict()
            self._solids = python_dict()
            self._grab = None

        def _solid(self, color):
            d = self._solids.get(color)
            if d is None:
                d = Solid(color)
                self._solids[color] = d
            return d

        def _frame(self, w, h, color, th):
            """Обводка повторяет rotate спрайта, а не его axis-aligned bbox."""
            key = (w, h, color, th)
            d = self._frames.get(key)
            if d is None:
                c = self._solid(color)
                d = Fixed(
                    Transform(c, xysize=(w, th), pos=(0, 0)),
                    Transform(c, xysize=(w, th), pos=(0, h - th)),
                    Transform(c, xysize=(th, h), pos=(0, 0)),
                    Transform(c, xysize=(th, h), pos=(w - th, 0)),
                    xysize=(w, h),
                )
                self._frames[key] = d
            return d

        def _ghost(self, name):
            if name != self._img_key:
                self._img_key = name
                try:
                    self._img = renpy.displayable(name) if name else None
                except Exception:
                    self._img = None
            return self._img

        def _bar(self, rv, color, x, y, w, h, st, at):
            w, h = int(w), int(h)
            if w <= 0 or h <= 0:
                return
            rv.blit(renpy.render(self._solid(color), w, h, st, at), (int(x), int(y)))

        def render(self, width, height, st, at):
            rv = renpy.Render(width, height)
            if self.mode != "draw":
                return rv

            ## Модель меняется вне screen tree, поэтому render надо инвалидировать.
            renpy.redraw(self, 0 if pt_model.dragging else 1.0 / 30.0)

            sel = pt_model.target()

            for name, t in pt_model.targets.items():
                if sel is not None and name == sel.name:
                    continue
                b = t.scene["bounds"]
                if not b:
                    continue
                x, y, w, h = b
                self._bar(rv, PT_COLOR_DIM, x, y, w, 1, st, at)
                self._bar(rv, PT_COLOR_DIM, x, y + h - 1, w, 1, st, at)
                self._bar(rv, PT_COLOR_DIM, x, y, 1, h, st, at)
                self._bar(rv, PT_COLOR_DIM, x + w - 1, y, 1, h, st, at)

            if sel is None:
                return rv

            w, h = sel.natural
            if w <= 0 or h <= 0:
                return rv

            layers = python_list()

            if sel.dirty:
                child = self._ghost(sel.name)
                if child is not None:
                    layers.append(Transform(
                        child, pos=sel.pos, anchor=sel.anchor, rotate=sel.rotate,
                        transform_anchor=True, alpha=PT_GHOST_ALPHA,
                    ))

            layers.append(Transform(
                self._frame(w, h, PT_COLOR_BOX, 2),
                pos=sel.pos, anchor=sel.anchor, rotate=sel.rotate,
                transform_anchor=True,
            ))

            rv.blit(renpy.render(Fixed(*layers, xysize=(width, height)),
                                 width, height, st, at), (0, 0))

            ## transform_anchor=True совмещает pos с направляющими.
            mx, my = sel.pos
            self._bar(rv, PT_COLOR_GUIDE, 0, my, width, 1, st, at)
            self._bar(rv, PT_COLOR_GUIDE, mx, 0, 1, height, st, at)
            self._bar(rv, PT_COLOR_MARK, mx - 9, my - 1, 19, 3, st, at)
            self._bar(rv, PT_COLOR_MARK, mx - 1, my - 9, 3, 19, st, at)
            return rv

        def event(self, ev, x, y, st):
            if self.mode != "grab":
                return None

            t = pt_model.target()
            if t is None:
                return None

            if self._grab is None:
                if ev.type == _pt_pygame.MOUSEBUTTONDOWN and ev.button == 1:
                    px, py, pw, ph = pt_model.panel_rect
                    if px <= x < px + pw and py <= y < py + ph:
                        return None      # клик по панели — это кнопки

                    ## Выбранный спрайт имеет приоритет при пересечении.
                    hit = t if self._inside(t, x, y) else self._pick_at(x, y)
                    if hit is None:
                        return None
                    if hit is not t:
                        pt_model.name = hit.name
                        t = hit
                    bx, by = pt_model.topleft()
                    self._grab = (x - bx, y - by)
                    pt_model.dragging = True
                    pt_model.drag_from = t.values()
                    renpy.restart_interaction()
                    raise renpy.IgnoreEvent()
                return None

            ## Захваченный спрайт продолжаем вести и под панелью.
            if ev.type == _pt_pygame.MOUSEMOTION:
                pt_set(t, pos=pt_model.pos_from_topleft(x - self._grab[0], y - self._grab[1]),
                       commit=False)
                renpy.redraw(pt_ghost, 0)
                raise renpy.IgnoreEvent()

            if ev.type == _pt_pygame.MOUSEBUTTONUP and ev.button == 1:
                self._grab = None
                pt_model.dragging = False
                if pt_model.drag_from is not None and pt_model.drag_from != t.values():
                    pt_push([(t.name, pt_model.drag_from)], "мышь: " + t.name)
                    pt_model.status = "перетащено: " + t.name
                pt_model.drag_from = None
                renpy.restart_interaction()
                raise renpy.IgnoreEvent()

            return None

        def _inside(self, t, x, y):
            b = t.scene["bounds"] if not t.dirty else None
            if b is None:
                w, h = t.natural
                ax, ay = t.anchor
                bx = int(round(t.pos[0] - ax * w))
                by = int(round(t.pos[1] - ay * h))
                b = (bx, by, w, h)
            return b[0] <= x < b[0] + b[2] and b[1] <= y < b[1] + b[3]

        def _pick_at(self, x, y):
            """При пересечении выбирает самый мелкий спрайт."""
            best = None
            for t in pt_model.targets.values():
                if not self._inside(t, x, y):
                    continue
                w, h = t.natural
                if best is None or w * h < best[0]:
                    best = (w * h, t)
            return best[1] if best else None

        def visit(self):
            if self.mode != "draw":
                return []
            sel = pt_model.target()
            c = self._ghost(sel.name) if sel is not None else None
            return [c] if c is not None else []


init -10 python:
    pt_model = PTModel()
    pt_ghost = PTSurface("draw")
    pt_grab = PTSurface("grab")
