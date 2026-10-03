## Курсор рисует игра, а не система: только так на него ложится процарапанный штрих.
## Своя группа параметров, тюнер — Cursor Tuner в Dev Hub. (1, 1) — остриё треугольника.
## Порог волокон 0: волокна рвали бы заливку треугольника, и курсор просвечивал.
init -10 python:
    scratch_params("cursor", "Курсор", 1.5, 0.0, 1.0, 0.55)
    ## Над интерактивом курсор «оживает»: штрих нервнее, треугольник чуть сужается в
    ## перспективе и клонится к цели — остриё на месте. Дёрг — только на отказе клика,
    ## чтобы тряска значила «нельзя» и не путалась с «можно».
    fx_param("cursor.hover_t", 0.12, 0.0, 0.5, step=0.01, doc="наведение: время перехода, с")
    fx_param("cursor.hover_mix", 1.15, 1.0, 5.0, step=0.1, doc="наведение: множитель силы штриха")
    fx_param("cursor.hover_squeeze", 0.06, 0.0, 0.5, step=0.01, doc="наведение: сужание по ширине, доля")
    fx_param("cursor.hover_tilt", -3.0, -20.0, 20.0, step=0.5, doc="наведение: наклон, °")
    fx_param("cursor.deny_shake", 3.0, 0.0, 10.0, step=0.5, doc="отказ клика: размах дёрга, px")
    fx_param("cursor.deny_shake_t", 0.25, 0.05, 1.0, step=0.01, doc="отказ клика: длина дёрга, с")

    ## Серый «заблокированный» курсор: клик сейчас ничего не сделает
    ## (click_skip_block или dismiss_off из 7dots). В меню клик работает — курсор обычный.
    CURSOR_BLOCKED_FADE = 0.25

    ## Мимо кнопок фокус держит SayBehavior реплики — его не считаем.
    def _cursor_over_focus():
        f = renpy.display.focus.get_focused()
        return isinstance(f, (renpy.display.behavior.Button, renpy.display.behavior.Bar))

    def _cursor_blocked():
        if main_menu or renpy.context()._menu or renpy.get_screen("confirm"):
            return False
        ## Над кнопкой (быстрое меню и т. п.) клик работает — курсор обычный.
        if _cursor_over_focus():
            return False
        return sm_click_blocked() or not getattr(store, "can_dismiss", True)

    ## Клик по заблокированному (мимо кнопок) — тёмно-красная вспышка: нарастает за IN, гаснет за OUT.
    CURSOR_DENY_IN = 0.0
    CURSOR_DENY_OUT = 0.4
    CURSOR_DENY_COLOR = "#8b1a1a"

    def _cursor_deny_level(now):
        t = now - _fx_state.get("cursor_deny_at", -10.0)
        if t < CURSOR_DENY_IN:
            return t / CURSOR_DENY_IN
        return max(0.0, 1.0 - (t - CURSOR_DENY_IN) / CURSOR_DENY_OUT)

    def _cursor_approach(level, target, step):
        return min(target, level + step) if level < target else max(target, level - step)

    def cursor_block_f(trans, st, at):
        import math
        import pygame_sdl2
        level = _fx_state.get("cursor_block", 0.0)
        hover = _fx_state.get("cursor_hover", 0.0)
        blocked = _cursor_blocked()
        target = 1.0 if blocked else 0.0
        hover_target = 1.0 if not blocked and _cursor_over_focus() else 0.0
        deny = 0.0
        shake = 0.0
        if not renpy.predicting():
            now = _fx_frame_time()
            dt = max(0.0, min(now - _fx_state.get("cursor_block_time", now), 0.1))
            level = _cursor_approach(level, target, dt / CURSOR_BLOCKED_FADE)
            hover_t = fx_cfg("cursor.hover_t")
            hover = _cursor_approach(hover, hover_target, dt / hover_t if hover_t > 0.0 else 1.0)
            _fx_state["cursor_block"] = level
            _fx_state["cursor_hover"] = hover
            _fx_state["cursor_block_time"] = now
            ## Клик ловится по нажатию кнопки мыши: pause и with под блоком не видят событий экранов.
            pressed = bool(pygame_sdl2.mouse.get_pressed()[0])
            if pressed and not _fx_state.get("cursor_pressed") and blocked \
                    and not _cursor_over_focus():
                _fx_state["cursor_deny_at"] = now
            _fx_state["cursor_pressed"] = pressed
            deny = _cursor_deny_level(now)
            shake_t = fx_cfg("cursor.deny_shake_t")
            since = now - _fx_state.get("cursor_deny_at", -10.0)
            if since < shake_t:
                shake = fx_cfg("cursor.deny_shake") * math.sin(since * 113.0) * (1.0 - since / shake_t)
        ## Контраст к серому: чёрная заливка светлеет, белая обводка тускнеет — курсор блёклый.
        m = SaturationMatrix(1.0 - level) * ContrastMatrix(1.0 - 0.45 * level)
        if deny > 0.0:
            red = Color(CURSOR_DENY_COLOR).interpolate(Color("#ffffff"), 1.0 - deny)
            m = TintMatrix(red) * m
        trans.matrixcolor = m
        trans.alpha = 1.0 - 0.35 * level * (1.0 - deny)
        ## Сужание — масштабом по x: поворот вокруг вертикали без перспективы выносит
        ## треугольник из плоскости, и он отсекается. Якорь (0, 0) держит остриё (1, 1)
        ## на месте горячей точки.
        motion = sm_motion_scale()
        trans.matrixanchor = (0.0, 0.0)
        trans.matrixtransform = (Matrix.rotate(0.0, 0.0, fx_cfg("cursor.hover_tilt") * hover * motion)
            * Matrix.scale(1.0 - fx_cfg("cursor.hover_squeeze") * hover * motion, 1.0, 1.0))
        trans.xoffset = shake * motion
        ## Под блоком, в переходах и дёрге — каждый кадр: иначе короткий клик можно пропустить.
        busy = level != target or hover != hover_target or blocked or deny > 0.0 or shake != 0.0
        return 1.0 / 60.0 if busy else 1.0 / 30.0

    ## Заблокированный курсор без штриха: сила штриха гаснет вместе с серым. Над
    ## интерактивом сильнее, но не выше полной: шейдер за 1.0 экстраполирует.
    def cursor_scratch_mix():
        hover = _fx_state.get("cursor_hover", 0.0)
        boost = min(1.0 + (fx_cfg("cursor.hover_mix") - 1.0) * hover, 1.0 / max(fx_cfg("cursor.mix"), 0.01))
        return (1.0 - _fx_state.get("cursor_block", 0.0)) * boost

    def cursor_scratch_hover():
        return _fx_state.get("cursor_hover", 0.0)

transform cursor_block():
    function cursor_block_f

define 1 config.mouse_displayable = MouseDisplayable(
    At("gui/tri_bone_hover.png", scratch("cursor", tint=0.0, pad=8, mix_f=cursor_scratch_mix, hover_f=cursor_scratch_hover), cursor_block), 1, 1)
