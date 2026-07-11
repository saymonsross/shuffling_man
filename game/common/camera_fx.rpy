################################################################################
## Общие эффекты камеры и экрана
##
## Переиспользуемые трансформы: покачивание камеры, параллакс за мышкой с
## дрожью напряжения, полноэкранные зерно-помехи (шейдер sm.noise —
## common/shaders.rpy). Все параметры имеют дефолты, числовые аргументы
## проверяются и приводятся к безопасным диапазонам.
##
## Правило проекта: перед добавлением сюда новых эффектов — проверить,
## нет ли готового решения в libs/7dots.rpy.
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

    def _fx_tension(trans, tension_var, relax):
        """Сглаженное значение переменной напряжения store[tension_var] (0..1).

        Состояние хранится на объекте трансформа (fx_t), поэтому после смены
        переменной значение тянется к цели плавно, со скоростью relax за кадр.
        tension_var не задана или не строка → эффект на полную силу (1.0).
        """
        if isinstance(tension_var, str) and tension_var:
            target = _fx_num(getattr(store, tension_var, 0.0), 0.0, 0.0, 1.0)
        else:
            target = 1.0
        t = getattr(trans, "fx_t", None)
        t = target if t is None else t + (target - t) * relax
        trans.fx_t = t
        return t

    def mouse_parallax_f(strength, smooth, shake_amp, relax, tension_var, trans, st, at):
        """function-трансформ (по образцу xy_at_f из 7dots): камера чуть
        сдвигается против движения мыши, поверх — мелкая дрожь напряжения.

        strength   — максимальный сдвиг параллакса в пикселях;
        smooth     — доля пути к цели за кадр (0..1);
        shake_amp  — амплитуда дрожи в пикселях при полном напряжении;
        relax      — скорость спадания напряжения за кадр (0..1);
        tension_var — имя переменной напряжения 0..1 (None — дрожь постоянна).
        """
        strength = _fx_num(strength, 10.0, 0.0)
        smooth = _fx_num(smooth, 0.06, 0.001, 1.0)
        shake_amp = _fx_num(shake_amp, 0.0, 0.0)
        relax = _fx_num(relax, 0.04, 0.001, 1.0)

        ## Параллакс: цель — против движения мыши, со сглаживанием.
        mx, my = renpy.get_mouse_pos()
        tx = -(mx / float(config.screen_width) - 0.5) * 2.0 * strength
        ty = -(my / float(config.screen_height) - 0.5) * 2.0 * strength
        px = getattr(trans, "fx_px", 0.0)
        py = getattr(trans, "fx_py", 0.0)
        px += (tx - px) * smooth
        py += (ty - py) * smooth
        trans.fx_px = px
        trans.fx_py = py

        ## Мелкая дрожь: не тряска, а зуд-раздражение. Короткий диапазон,
        ## лёгкое сглаживание рывков между кадрами.
        t = _fx_tension(trans, tension_var, relax)
        amp = shake_amp * t
        jx = getattr(trans, "fx_jx", 0.0)
        jy = getattr(trans, "fx_jy", 0.0)
        jx += (renpy.random.uniform(-amp, amp) - jx) * 0.5
        jy += (renpy.random.uniform(-amp, amp) - jy) * 0.5
        trans.fx_jx = jx
        trans.fx_jy = jy

        trans.xoffset = px + jx
        trans.yoffset = py + jy
        return 1.0 / 60.0

    def noise_overlay_f(strength, relax, tension_var, trans, st, at):
        """function-трансформ зерна: сила = strength × напряжение (0..1)."""
        strength = _fx_num(strength, 0.1, 0.0, 1.0)
        relax = _fx_num(relax, 0.04, 0.001, 1.0)
        trans.u_strength = strength * _fx_tension(trans, tension_var, relax)
        return 1.0 / 60.0

## Камера следует за мышкой (сдвиг против движения, до strength px), сверху —
## опциональная дрожь shake_amp, спадающая вместе со store[tension_var].
## zoom_pad — запас по краям, чтобы при сдвигах не проступал фон.
## Применять через `camera`, чтобы двигался весь слой master.
transform mouse_parallax(strength=10.0, smooth=0.06, shake_amp=0.0, relax=0.04, tension_var=None, zoom_pad=1.02):
    subpixel True
    align (0.5, 0.5) zoom zoom_pad
    xoffset 0.0 yoffset 0.0
    function renpy.curry(mouse_parallax_f)(strength, smooth, shake_amp, relax, tension_var)

## Полноэкранные зерно-помехи поверх сцены:
##     show fx_noise at noise_overlay(strength, relax, "имя_переменной")
## Без tension_var сила постоянна и равна strength.
image fx_noise = Solid("#FFF")

transform noise_overlay(strength=0.1, relax=0.04, tension_var=None):
    mesh True
    shader "sm.noise"
    u_strength 0.0
    function renpy.curry(noise_overlay_f)(strength, relax, tension_var)

## Тревожное покачивание камеры: непрерывный дрейф позиции и лёгкий наклон.
## drift — амплитуда сдвига (px), tilt — наклон (градусы), speed — множитель
## скорости (>0), zoom_pad — запас по краям. Периоды осей некратны друг
## другу — движение не выглядит зацикленным.
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
