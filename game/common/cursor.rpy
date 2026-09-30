## Курсор рисует игра, а не система: только так на него ложится процарапанный штрих.
## Своя группа параметров, тюнер — Cursor Tuner в Dev Hub. (1, 1) — остриё треугольника.
## Порог волокон 0: волокна рвали бы заливку треугольника, и курсор просвечивал.
init -10 python:
    scratch_params("cursor", "Курсор", 1.5, 0.0, 1.0, 0.55)

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
        return bool(getattr(store, "click_skip_block", False)) or not getattr(store, "can_dismiss", True)

    ## Клик по заблокированному (мимо кнопок) — тёмно-красная вспышка: нарастает за IN, гаснет за OUT.
    CURSOR_DENY_IN = 0.0
    CURSOR_DENY_OUT = 0.4
    CURSOR_DENY_COLOR = "#8b1a1a"

    def _cursor_deny_level(now):
        t = now - _fx_state.get("cursor_deny_at", -10.0)
        if t < CURSOR_DENY_IN:
            return t / CURSOR_DENY_IN
        return max(0.0, 1.0 - (t - CURSOR_DENY_IN) / CURSOR_DENY_OUT)

    def cursor_block_f(trans, st, at):
        import pygame_sdl2
        level = _fx_state.get("cursor_block", 0.0)
        blocked = _cursor_blocked()
        target = 1.0 if blocked else 0.0
        deny = 0.0
        if not renpy.predicting():
            now = _fx_frame_time()
            dt = max(0.0, min(now - _fx_state.get("cursor_block_time", now), 0.1))
            step = dt / CURSOR_BLOCKED_FADE
            level = min(target, level + step) if level < target else max(target, level - step)
            _fx_state["cursor_block"] = level
            _fx_state["cursor_block_time"] = now
            ## Клик ловится по нажатию кнопки мыши: pause и with под блоком не видят событий экранов.
            pressed = bool(pygame_sdl2.mouse.get_pressed()[0])
            if pressed and not _fx_state.get("cursor_pressed") and blocked \
                    and not _cursor_over_focus():
                _fx_state["cursor_deny_at"] = now
            _fx_state["cursor_pressed"] = pressed
            deny = _cursor_deny_level(now)
        ## Контраст к серому: чёрная заливка светлеет, белая обводка тускнеет — курсор блёклый.
        m = SaturationMatrix(1.0 - level) * ContrastMatrix(1.0 - 0.45 * level)
        if deny > 0.0:
            red = Color(CURSOR_DENY_COLOR).interpolate(Color("#ffffff"), 1.0 - deny)
            m = TintMatrix(red) * m
        trans.matrixcolor = m
        trans.alpha = 1.0 - 0.35 * level * (1.0 - deny)
        ## Под блоком — каждый кадр: иначе короткий клик можно пропустить.
        return 1.0 / 60.0 if (level != target or blocked or deny > 0.0) else 0.1

    ## Заблокированный курсор без штриха: сила штриха гаснет вместе с серым.
    def cursor_scratch_mix():
        return 1.0 - _fx_state.get("cursor_block", 0.0)

transform cursor_block():
    function cursor_block_f

define 1 config.mouse_displayable = MouseDisplayable(
    At("gui/tri_bone_hover.png", scratch("cursor", tint=0.0, pad=8, mix_f=cursor_scratch_mix), cursor_block), 1, 1)
