## Дышащая виньетка. Вид — fx_config.yaml (F10, группа vignette); включение по сюжету —
## $ fx_vignette = True / False, проявление и угасание за vignette.fade секунд.
## Экран на слое screens под окном диалога и меню: UI не затемняется.

default fx_vignette = False

init -10 python:

    fx_param("vignette.enabled", True, doc="разрешить виньетку; включает сцена через fx_vignette")
    fx_param("vignette.strength", 0.7, 0.0, 1.0, step=0.01, doc="плотность затемнения у краёв")
    fx_param("vignette.radius", 0.45, 0.0, 1.5, step=0.01, doc="радиус чистого центра, доля полудиагонали")
    fx_param("vignette.softness", 0.55, 0.01, 1.5, step=0.01, doc="ширина перехода к краю")
    fx_param("vignette.breath_amp", 0.06, 0.0, 0.5, step=0.005, doc="дыхание: размах радиуса")
    fx_param("vignette.breath_period", 6.0, 0.5, 20.0, step=0.1, doc="период дыхания, с")
    fx_param("vignette.fade", 1.0, 0.0, 5.0, step=0.05, doc="проявление и угасание при смене fx_vignette, с")
    fx_group("vignette", "Виньетка")

    ## Дизеринг в полшага: без него плавный чёрный градиент идёт видимыми ступенями.
    renpy.register_shader("sm.vignette",
        variables="""
        uniform float u_vig_strength;
        uniform float u_vig_radius;
        uniform float u_vig_softness;
        uniform float u_vig_aspect;
        attribute vec2 a_tex_coord;
        varying vec2 v_tex_coord;
        """,
        vertex_300="""
        v_tex_coord = a_tex_coord;
        """,
        fragment_300="""
        vec2 k = vec2(u_vig_aspect, 1.0);
        float d = length((v_tex_coord - 0.5) * k) / length(0.5 * k);
        float a = smoothstep(u_vig_radius, u_vig_radius + u_vig_softness, d) * u_vig_strength;
        float n = fract(sin(dot(gl_FragCoord.xy, vec2(12.9898, 78.233))) * 43758.5453) - 0.5;
        a = clamp(a + n / 255.0, 0.0, 1.0);
        gl_FragColor = vec4(0.0, 0.0, 0.0, a);
        """)

    def vignette_f(trans, st, at):
        on = store.fx_vignette and fx_cfg("vignette.enabled") and not fx_cfg_bypassed()
        target = 1.0 if on else 0.0
        level = _fx_state.get("vignette_level", 0.0)
        now = _fx_frame_time()
        if not renpy.predicting():
            ## Шаг по реальному времени: fade секунд на полный переход в любую сторону.
            dt = max(0.0, min(now - _fx_state.get("vignette_time", now), 0.1))
            fade = fx_cfg("vignette.fade")
            if fade <= 0.0:
                level = target
            elif level < target:
                level = min(target, level + dt / fade)
            else:
                level = max(target, level - dt / fade)
            _fx_state["vignette_level"] = level
            _fx_state["vignette_time"] = now

        ## Доля кадра (fx_frame) — плавно: на конце растворения кадра она меняется разом.
        share = fx_frame_value("vignette")
        share = 1.0 if share is None else share
        share = _fx_step("vignette_frame", share, 0.05, start=share)

        period = fx_cfg("vignette.breath_period")
        breath = math.sin(2.0 * math.pi * (now % period) / period)
        trans.u_vig_strength = fx_cfg("vignette.strength") * level * share
        trans.u_vig_radius = fx_cfg("vignette.radius") + fx_cfg("vignette.breath_amp") * breath * sm_motion_scale()
        trans.u_vig_softness = fx_cfg("vignette.softness")
        trans.u_vig_aspect = config.screen_width / float(config.screen_height)
        ## Погашенная виньетка не перерисовывается каждый кадр.
        if level > 0.0 or target > 0.0:
            return fx_tick()
        return fx_tick(12)

image fx_vignette = Solid("#000")

transform vignette_overlay():
    mesh True
    shader "sm.vignette"
    u_vig_strength 0.0
    u_vig_radius 0.45
    u_vig_softness 0.55
    u_vig_aspect 1.7777
    function vignette_f

## zorder ниже окна диалога (0) и быстрого меню (100).
screen fx_vignette_screen():
    zorder -100
    add "fx_vignette" at vignette_overlay

init python:
    config.always_shown_screens.append("fx_vignette_screen")
