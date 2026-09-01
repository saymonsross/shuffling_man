define FX_MOUSE_PARALLAX_ON = True

init -10 python:

    import random as sm_python_random

    ## Визуальный RNG изолирован: renpy.random засоряет rollback-log на 60 fps.
    sm_visual_rng = sm_python_random.Random()

    def _fx_num(v, default, lo=None, hi=None):
        if not isinstance(v, (int, float)) or isinstance(v, bool):
            v = default
        if lo is not None:
            v = max(v, lo)
        if hi is not None:
            v = min(v, hi)
        return float(v)

    ## Состояние function-трансформов хранится здесь под уникальным key:
    ## restart_interaction пересоздаёт trans, а повторный ATL сбрасывает st.
    ## Поэтому накопители нельзя сбрасывать при st≈0 между сценами.
    _fx_state = {}

    def _fx_step(key, target, relax, start):
        """Сглаживает _fx_state[key]; start действует только при первом вызове
        для key, а накопитель переживает пересборку transform."""
        cur = _fx_state.get(key, start)
        cur += (target - cur) * relax
        _fx_state[key] = cur
        return cur

    def _fx_visual_jitter(amp):
        """Случайный визуальный offset без загрязнения игрового RNG/rollback."""
        if amp <= 0.0 or sm_reduced_motion():
            return 0.0
        return sm_visual_rng.uniform(-amp, amp)

    def _fx_tension(tension_var, relax, key):
        """Пустой tension_var означает полную силу; key задаёт накопитель."""
        if isinstance(tension_var, str) and tension_var:
            target = _fx_num(getattr(store, tension_var, 0.0), 0.0, 0.0, 1.0)
        else:
            target = 1.0
        return _fx_step(key, target, relax, start=target)

    def mouse_parallax_f(strength, smooth, shake_amp, relax, tension_var, key, trans, st, at):
        """Параллакс с дрожью от tension_var; key уникален для каждого
        одновременного эффекта."""
        strength = _fx_num(strength, 10.0, 0.0)
        ## Глобальный флаг плавно гасит параллакс; reduced motion сразу гасит и дрожь.
        if sm_reduced_motion():
            for suffix in ("_px", "_py", "_jx", "_jy"):
                _fx_state[key + suffix] = 0.0
            trans.xoffset = 0.0
            trans.yoffset = 0.0
            return 1.0 / 60.0
        if not FX_MOUSE_PARALLAX_ON:
            strength = 0.0
        smooth = _fx_num(smooth, 0.06, 0.001, 1.0)
        shake_amp = _fx_num(shake_amp, 0.0, 0.0)
        relax = _fx_num(relax, 0.04, 0.001, 1.0)

        mx, my = renpy.get_mouse_pos()
        tx = -(mx / float(config.screen_width) - 0.5) * 2.0 * strength
        ty = -(my / float(config.screen_height) - 0.5) * 2.0 * strength
        px = _fx_step(key + "_px", tx, smooth, start=0.0)
        py = _fx_step(key + "_py", ty, smooth, start=0.0)

        t = _fx_tension(tension_var, relax, key + "_tension")
        amp = shake_amp * t
        jx = _fx_step(key + "_jx", _fx_visual_jitter(amp), 0.5, start=0.0)
        jy = _fx_step(key + "_jy", _fx_visual_jitter(amp), 0.5, start=0.0)

        trans.xoffset = px + jx
        trans.yoffset = py + jy
        return 1.0 / 60.0

    def _focus_offset(focus_align, screen_align, z):
        """Совмещает focus_align изображения со screen_align экрана пиксельным
        offset: дробные anchor/pos камеры артефактят на Windows/ANGLE."""
        fx, fy = focus_align
        sx, sy = (screen_align or focus_align)
        ox = config.screen_width * (sx - 0.5 - (fx - 0.5) * z)
        oy = config.screen_height * (sy - 0.5 - (fy - 0.5) * z)
        return ox, oy

    def focus_parallax_f(focus_align, screen_align, strength, smooth, key, trans, st, at):
        """Считает базовый кадр по текущему trans.zoom и добавляет параллакс."""
        bx, by = _focus_offset(focus_align, screen_align, trans.zoom or 1.0)

        strength = _fx_num(strength, 10.0, 0.0)
        if sm_reduced_motion():
            _fx_state[key + "_px"] = 0.0
            _fx_state[key + "_py"] = 0.0
            trans.xoffset = bx
            trans.yoffset = by
            return 1.0 / 60.0
        if not FX_MOUSE_PARALLAX_ON:
            strength = 0.0
        smooth = _fx_num(smooth, 0.06, 0.001, 1.0)
        mx, my = renpy.get_mouse_pos()
        tx = -(mx / float(config.screen_width) - 0.5) * 2.0 * strength
        ty = -(my / float(config.screen_height) - 0.5) * 2.0 * strength
        px = _fx_step(key + "_px", tx, smooth, start=0.0)
        py = _fx_step(key + "_py", ty, smooth, start=0.0)

        trans.xoffset = bx + px
        trans.yoffset = by + py
        return 1.0 / 60.0

    def follow_camera_f(key, trans, st, at):
        """Читает готовые offsets камеры из _fx_state, чтобы не создавать
        второй накопитель и не давать экранному элементу дрейфовать."""
        px = _fx_state.get(key + "_px", 0.0)
        py = _fx_state.get(key + "_py", 0.0)
        jx = _fx_state.get(key + "_jx", 0.0)
        jy = _fx_state.get(key + "_jy", 0.0)

        trans.xoffset = px + jx
        trans.yoffset = py + jy
        return 1.0 / 60.0

    def mouse_follow_f(rx, ry, smooth, key, trans, st, at):
        rx = _fx_num(rx, 0.0)
        ry = _fx_num(ry, 0.0)
        smooth = _fx_num(smooth, 0.12, 0.001, 1.0)

        if sm_reduced_motion():
            _fx_state[key + "_fx"] = 0.0
            _fx_state[key + "_fy"] = 0.0
            trans.xoffset = 0.0
            trans.yoffset = 0.0
            return 1.0 / 60.0

        mx, my = renpy.get_mouse_pos()
        fx = _fx_step(key + "_fx", mx - rx, smooth, start=0.0)
        fy = _fx_step(key + "_fy", my - ry, smooth, start=0.0)

        trans.xoffset = fx
        trans.yoffset = fy
        return 1.0 / 60.0

    def noise_overlay_f(strength, relax, tension_var, trans, st, at):
        strength = _fx_num(strength, 0.1, 0.0, 1.0)
        if sm_reduced_motion():
            strength = 0.0
        relax = _fx_num(relax, 0.04, 0.001, 1.0)
        trans.u_strength = strength * _fx_tension(tension_var, relax, "noise_tension")
        return 1.0 / 60.0

    def object_jitter_f(amp, relax, key, trans, st, at):
        """Аддитивный jitter поверх ATL; key должен быть уникален для объекта."""
        amp = _fx_num(amp, 3.0, 0.0)
        relax = _fx_num(relax, 0.5, 0.001, 1.0)

        if sm_reduced_motion():
            _fx_state[key + "_jx"] = 0.0
            _fx_state[key + "_jy"] = 0.0
            trans.xoffset = 0.0
            trans.yoffset = 0.0
            return 1.0 / 60.0

        jx = _fx_step(key + "_jx", _fx_visual_jitter(amp), relax, start=0.0)
        jy = _fx_step(key + "_jy", _fx_visual_jitter(amp), relax, start=0.0)
        trans.xoffset = jx
        trans.yoffset = jy
        return 1.0 / 60.0

## Общий zoom_pad камеры и world-space UI: значения обязаны совпадать.
define FX_CAMERA_ZOOM_PAD = 1.02

## Явный rotate 0.0 сбрасывает наклон, унаследованный от предыдущего camera at.
transform mouse_parallax(strength=10.0, smooth=0.06, shake_amp=0.0, relax=0.04, tension_var=None, zoom_pad=FX_CAMERA_ZOOM_PAD, key="cam"):
    subpixel True
    align (0.5, 0.5) zoom zoom_pad
    rotate 0.0
    xoffset 0.0 yoffset 0.0
    function renpy.curry(mouse_parallax_f)(strength, smooth, shake_amp, relax, tension_var, key)

## World-space UI: контейнер должен быть размером с экран, а key и zoom_pad —
## совпадать с камерой.
transform follow_camera(key="cam", zoom_pad=FX_CAMERA_ZOOM_PAD):
    subpixel True
    align (0.5, 0.5) zoom zoom_pad
    xoffset 0.0 yoffset 0.0
    function renpy.curry(follow_camera_f)(key)

## focus_align удерживается в screen_align во время зума. Пиксельные offsets
## обязательны: дробные anchor/pos камеры дают артефакты на части render paths.
## Зум-трек идёт первым, поскольку function читает trans.zoom текущего кадра.
transform parallax_push(focus_align, z0, z1, t, strength=10.0, smooth=0.06, key="cam", screen_align=None):
    subpixel True
    align (0.5, 0.5)
    zoom (z1 if sm_reduced_motion() else z0)
    parallel:
        ease sm_motion_time(t) zoom z1
    parallel:
        function renpy.curry(focus_parallax_f)(focus_align, screen_align, strength, smooth, key)

transform parallax_settle(focus_align, z0, z1, t, strength=10.0, smooth=0.06, key="cam", screen_align=None):
    subpixel True
    align (0.5, 0.5)
    zoom (z1 if sm_reduced_motion() else z0)
    parallel:
        easein sm_motion_time(t) zoom z1
    parallel:
        function renpy.curry(focus_parallax_f)(focus_align, screen_align, strength, smooth, key)

transform mouse_follow(rx, ry, smooth=0.12, key="follow"):
    subpixel True
    xoffset 0.0 yoffset 0.0
    function renpy.curry(mouse_follow_f)(rx, ry, smooth, key)

## Зерно показано глобально; сцены меняют только fx_noise_strength.
image fx_noise = Solid("#FFF")

transform noise_overlay(strength=0.1, relax=0.04, tension_var=None):
    mesh True
    shader "sm.noise"
    u_strength 0.0
    function renpy.curry(noise_overlay_f)(strength, relax, tension_var)

## После сцены возвращать силу зерна к FX_NOISE_DEFAULT.
define FX_NOISE_DEFAULT = 0.10
default fx_noise_strength = FX_NOISE_DEFAULT

## always_shown переживает очистку master через scene.
screen fx_noise_screen():
    add "fx_noise" at noise_overlay(1.0, tension_var="fx_noise_strength")

init python:
    config.always_shown_screens.append("fx_noise_screen")

## Некратные периоды скрывают цикл покачивания. base/base_in_t задают входной
## наклон; zoom0 — плавный вход из другого camera-transform.
## Для угла θ: zoom_pad ≥ cos θ + (16/9)·sin θ.
transform uneasy_sway(drift=12.0, tilt=0.6, speed=1.0, zoom_pad=1.06, base=0.0, base_in_t=0.0, zoom0=None):
    subpixel True
    align (0.5, 0.5)
    zoom (zoom_pad if sm_reduced_motion() or zoom0 is None else zoom0)
    parallel:
        easein sm_motion_time(base_in_t) zoom zoom_pad
    parallel:
        ease sm_motion_time(3.4 / max(speed, 0.05)) xoffset (drift * sm_motion_scale())
        ease 4.1 / max(speed, 0.05) xoffset (-drift * 0.85 * sm_motion_scale())
        repeat
    parallel:
        easein sm_motion_time(base_in_t) rotate (base * sm_motion_scale())
        block:
            ease 5.3 / max(speed, 0.05) rotate ((base + tilt) * sm_motion_scale())
            ease 4.7 / max(speed, 0.05) rotate ((base - tilt * 0.85) * sm_motion_scale())
            repeat
    parallel:
        ease sm_motion_time(2.9 / max(speed, 0.05)) yoffset (-drift * 0.7 * sm_motion_scale())
        ease 3.7 / max(speed, 0.05) yoffset (drift * 0.75 * sm_motion_scale())
        repeat
