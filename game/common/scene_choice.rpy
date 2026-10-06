## Сценовые действия: menu(screen="scene_choice"). Каждый пункт — glow_button,
## аргументы пункта меню уходят в него (pos, size, bg, hovered...).
## Под кнопками — разлом сцены (common/rift.rpy).
## follow — трансформ мирового контейнера; skippable — поздний пропуск выбирает
## первый пункт, только для меню без развилки.
## drift — для выборов в разговоре (не для действий над предметами): кнопки висят ближе
## кадра и сильнее едут за мышью, а наведённая отталкивает остальные от себя — каждую по
## направлению от своего центра к её; при уходе курсора они плавно возвращаются.

init -5 python:
    ## Позиции, перетащенные Choice Placer (dev/choice_placer.rpy) в этой сессии:
    ## (файл и строка menu, подпись) → pos. В релизе словарь пуст.
    _sm_choice_moved = {}

    fx_param("choice_drift.depth", 7, 0, 60, doc="добавка параллакса кнопок выбора к сдвигу кадра, px")
    fx_param("choice_drift.push", 12, 0, 200, doc="отталкивание от наведённой кнопки, px")
    fx_param("choice_drift.smooth", 0.03, 0.01, 1.0, step=0.01, doc="доля пути за кадр 60 Гц; меньше — плавнее")
    fx_group("choice_drift", "Выборы в разговоре: движение")

    def sm_choice_center(kwargs):
        x, y, w, h = sm_rift_rect(kwargs.get("pos", (0.5, 0.5)), kwargs.get("anchor", (0.5, 0.5)),
            kwargs.get("size") or GLOW_BASE_SIZE)
        return (x + w / 2.0, y + h / 2.0)

    def sm_choice_drift_f(key, center, trans, st, at):
        import math
        _fx_state[("choice_center", key)] = center
        level, mx, my = _sm_parallax_state()
        px, py = _sm_parallax_shift(fx_cfg("choice_drift.depth"), level, mx, my)
        tx = ty = 0.0
        hovered = _fx_state.get("choice_hover")
        other = _fx_state.get(("choice_center", hovered)) if hovered and hovered != key else None
        if other is not None and not sm_reduced_motion():
            vx, vy = center[0] - other[0], center[1] - other[1]
            d = math.hypot(vx, vy) or 1.0
            push = fx_cfg("choice_drift.push")
            tx, ty = vx / d * push, vy / d * push
        smooth = fx_cfg("choice_drift.smooth")
        dx = _fx_step(("choice_dx", key), tx, smooth, start=0.0)
        dy = _fx_step(("choice_dy", key), ty, smooth, start=0.0)
        trans.xoffset = px + dx
        trans.yoffset = py + dy
        _fx_state[("choice_shift", key)] = (px + dx, py + dy)
        return fx_tick()

    def sm_choice_kwargs(where, item):
        pos = _sm_choice_moved.get((where, item.caption))
        if pos is None:
            return item.kwargs
        kwargs = dict(item.kwargs)
        kwargs["pos"] = pos
        return kwargs

transform choice_drift(key, center):
    subpixel True
    function renpy.curry(sm_choice_drift_f)(key, center)

screen scene_choice(items, follow=None, skippable=False, drift=False):
    modal True
    $ _sc_where = renpy.get_filename_line()
    $ _sc_placing = config.developer and renpy.get_screen("dev_choice_placer") is not None

    ## SkipOnce здесь нельзя: menu примет его True за индекс пункта 1.
    if skippable and renpy.is_skipping():
        timer 0.01 action items[0].action modal True

    ## Плавное появление и уход всего экрана — внешним трансформом корня; follow остаётся
    ## ближайшим к контейнеру, как ждёт камера.
    fixed:
        id "world"
        at (([follow] if follow is not None else []) + [show_hide(0.5)])
        xysize (config.screen_width, config.screen_height)
        for i in items:
            if _sc_placing:
                use dev_choice_drag(i, _sc_where)
            elif drift:
                $ _sc_kw = sm_choice_kwargs(_sc_where, i)
                fixed:
                    xysize (config.screen_width, config.screen_height)
                    at choice_drift("%s@%s" % (i.caption, _sc_kw.get("pos", (0.5, 0.5))), sm_choice_center(_sc_kw))
                    use glow_button(i.caption, i.action, rift=("follow" if follow is not None else "screen"), **_sc_kw)
            else:
                use glow_button(i.caption, i.action, rift=("follow" if follow is not None else "screen"), **sm_choice_kwargs(_sc_where, i))
