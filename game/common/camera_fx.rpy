################################################################################
## Общие эффекты камеры и экрана: параллакс, покачивание, зерно-помехи, дрожь.
## Перед добавлением новых — проверить, нет ли готового в libs/7dots.rpy.
################################################################################

init -10 python:

    def _fx_num(v, default, lo=None, hi=None):
        """Число с проверкой: не число → default, вне диапазона → к границе."""
        if not isinstance(v, (int, float)) or isinstance(v, bool):
            v = default
        if lo is not None:
            v = max(v, lo)
        if hi is not None:
            v = min(v, hi)
        return float(v)

    ## Накопители сглаживания function-трансформов. Module-level, НЕ атрибуты
    ## трансформа: camera-слой и always_shown-экраны пересобирают обёртку
    ## трансформа при каждом restart_interaction (любой клик/наведение), и
    ## python-атрибуты вроде trans.fx_px при этом теряются — видимый рывок.
    _fx_state = {}

    def _fx_step(key, target, relax, st, start):
        """Шаг сглаживания _fx_state[key] к target. st около 0 — новый старт
        эффекта (начинаем с start), иначе — продолжаем накопленное."""
        cur = start if st < 0.001 else _fx_state.get(key, start)
        cur += (target - cur) * relax
        _fx_state[key] = cur
        return cur

    def _fx_tension(tension_var, relax, st, key):
        """Сглаженное значение store[tension_var] (0..1); нет переменной —
        полная сила. key — свой накопитель на каждый вызывающий эффект."""
        if isinstance(tension_var, str) and tension_var:
            target = _fx_num(getattr(store, tension_var, 0.0), 0.0, 0.0, 1.0)
        else:
            target = 1.0
        return _fx_step(key, target, relax, st, start=target)

    def mouse_parallax_f(strength, smooth, shake_amp, relax, tension_var, trans, st, at):
        """Камера сдвигается против движения мыши (до strength px), поверх —
        дрожь shake_amp × напряжение store[tension_var]."""
        strength = _fx_num(strength, 10.0, 0.0)
        smooth = _fx_num(smooth, 0.06, 0.001, 1.0)
        shake_amp = _fx_num(shake_amp, 0.0, 0.0)
        relax = _fx_num(relax, 0.04, 0.001, 1.0)

        mx, my = renpy.get_mouse_pos()
        tx = -(mx / float(config.screen_width) - 0.5) * 2.0 * strength
        ty = -(my / float(config.screen_height) - 0.5) * 2.0 * strength
        px = _fx_step("cam_px", tx, smooth, st, start=0.0)
        py = _fx_step("cam_py", ty, smooth, st, start=0.0)

        t = _fx_tension(tension_var, relax, st, "cam_tension")
        amp = shake_amp * t
        jx = _fx_step("cam_jx", renpy.random.uniform(-amp, amp), 0.5, st, start=0.0)
        jy = _fx_step("cam_jy", renpy.random.uniform(-amp, amp), 0.5, st, start=0.0)

        trans.xoffset = px + jx
        trans.yoffset = py + jy
        return 1.0 / 60.0

    def mouse_follow_f(rx, ry, smooth, trans, st, at):
        """Слой смещается так, чтобы опорная точка изображения (rx, ry, px)
        плавно следовала за курсором."""
        rx = _fx_num(rx, 0.0)
        ry = _fx_num(ry, 0.0)
        smooth = _fx_num(smooth, 0.12, 0.001, 1.0)

        mx, my = renpy.get_mouse_pos()
        fx = getattr(trans, "fx_fx", 0.0)
        fy = getattr(trans, "fx_fy", 0.0)
        fx += ((mx - rx) - fx) * smooth
        fy += ((my - ry) - fy) * smooth
        trans.fx_fx = fx
        trans.fx_fy = fy

        trans.xoffset = fx
        trans.yoffset = fy
        return 1.0 / 60.0

    def noise_overlay_f(strength, relax, tension_var, trans, st, at):
        """Сила зерна = strength × напряжение (0..1)."""
        strength = _fx_num(strength, 0.1, 0.0, 1.0)
        relax = _fx_num(relax, 0.04, 0.001, 1.0)
        trans.u_strength = strength * _fx_tension(tension_var, relax, st, "noise_tension")
        return 1.0 / 60.0

    def object_jitter_f(amp, relax, key, trans, st, at):
        """Дрожь объекта добавочным offset — parallel-трек поверх pos/alpha,
        складывается с движением аддитивно. key уникален на объект."""
        amp = _fx_num(amp, 3.0, 0.0)
        relax = _fx_num(relax, 0.5, 0.001, 1.0)

        jx = _fx_step(key + "_jx", renpy.random.uniform(-amp, amp), relax, st, start=0.0)
        jy = _fx_step(key + "_jy", renpy.random.uniform(-amp, amp), relax, st, start=0.0)
        trans.xoffset = jx
        trans.yoffset = jy
        return 1.0 / 60.0

## Параллакс за мышкой + опциональная дрожь. Применять через `camera`.
## zoom_pad — запас по краям, чтобы при сдвигах не проступал фон.
transform mouse_parallax(strength=10.0, smooth=0.06, shake_amp=0.0, relax=0.04, tension_var=None, zoom_pad=1.02):
    subpixel True
    align (0.5, 0.5) zoom zoom_pad
    xoffset 0.0 yoffset 0.0
    function renpy.curry(mouse_parallax_f)(strength, smooth, shake_amp, relax, tension_var)

## Слой следует за курсором опорной точкой (rx, ry).
transform mouse_follow(rx, ry, smooth=0.12):
    subpixel True
    xoffset 0.0 yoffset 0.0
    function renpy.curry(mouse_follow_f)(rx, ry, smooth)

## Полноэкранное зерно. Глобально включено через fx_noise_screen ниже —
## руками показывать не нужно, сцены только меняют fx_noise_strength.
image fx_noise = Solid("#FFF")

transform noise_overlay(strength=0.1, relax=0.04, tension_var=None):
    mesh True
    shader "sm.noise"
    u_strength 0.0
    function renpy.curry(noise_overlay_f)(strength, relax, tension_var)

## Фоновая сила зерна (0..1). Сцены временно меняют fx_noise_strength и
## возвращают FX_NOISE_DEFAULT; переход плавный (relax в noise_overlay_f).
define FX_NOISE_DEFAULT = 0.10
default fx_noise_strength = FX_NOISE_DEFAULT

## always_shown: виден всегда, `scene` его не сбрасывает (чистит только master).
screen fx_noise_screen():
    add "fx_noise" at noise_overlay(1.0, tension_var="fx_noise_strength")

init python:
    config.always_shown_screens.append("fx_noise_screen")

## Тревожное покачивание камеры: дрейф (drift, px) + наклон (tilt, градусы).
## Периоды осей некратны — движение не выглядит зацикленным.
transform uneasy_sway(drift=12.0, tilt=0.6, speed=1.0, zoom_pad=1.06):
    subpixel True
    align (0.5, 0.5)
    zoom zoom_pad
    parallel:
        ease 3.4 / max(speed, 0.05) xoffset drift
        ease 4.1 / max(speed, 0.05) xoffset -drift * 0.85
        repeat
    parallel:
        ease 2.9 / max(speed, 0.05) yoffset -drift * 0.7
        ease 3.7 / max(speed, 0.05) yoffset drift * 0.75
        repeat
    parallel:
        ease 5.3 / max(speed, 0.05) rotate tilt
        ease 4.7 / max(speed, 0.05) rotate -tilt * 0.85
        repeat
