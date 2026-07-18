################################################################################
## Общие эффекты камеры и экрана
##
## Переиспользуемые трансформы: покачивание камеры, параллакс за мышкой с
## дрожью напряжения, полноэкранные зерно-помехи (шейдер sm.noise —
## common/shaders.rpy), дрожь произвольного объекта (object_jitter_f). Все
## параметры имеют дефолты, числовые аргументы проверяются и приводятся к
## безопасным диапазонам.
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

    ## Накопители сглаживания для function-трансформов ниже (offset, дрожь,
    ## напряжение) — хранятся здесь, в module-level словаре, а НЕ на объекте
    ## трансформа (как раньше — trans.fx_px = ...).
    ##
    ## Причина: "camera"-слой (см. transform_layer в движке) и постоянные
    ## оверлей-экраны (config.always_shown_screens, см. fx_noise_screen ниже)
    ## пересобирают обёртку трансформа заново при каждом restart_interaction —
    ## а это ЛЮБОЙ клик и ЛЮБОЕ наведение на кнопку/хотспот, не только смена
    ## сцены. Ren'Py при пересборке переносит в новый объект только
    ## официальные ATL-свойства (xoffset, zoom, alpha, u_-юниформы шейдеров) —
    ## обычные python-атрибуты вроде trans.fx_px копированию не подлежат и
    ## обнуляются, отчего сглаженное значение резко прыгает к 0 и заново
    ## подъезжает к цели: видимый рывок камеры на каждом клике/наведении.
    _fx_state = {}

    def _fx_step(key, target, relax, st, start):
        """Один шаг сглаживания _fx_state[key] к target на relax за кадр.

        st (shown time трансформа) отличает настоящий новый старт эффекта
        (st около 0 — старое значение неактуально, начинаем с start) от
        пересборки обёртки после клика/наведения (st продолжает расти —
        подхватываем накопленное в _fx_state значение).
        """
        cur = start if st < 0.001 else _fx_state.get(key, start)
        cur += (target - cur) * relax
        _fx_state[key] = cur
        return cur

    def _fx_tension(tension_var, relax, st, key):
        """Сглаженное значение переменной напряжения store[tension_var] (0..1).

        tension_var не задана или не строка → эффект на полную силу (1.0).
        key — идентификатор вызывающего эффекта (у разных эффектов свои
        независимые накопители, даже если tension_var совпадает).
        """
        if isinstance(tension_var, str) and tension_var:
            target = _fx_num(getattr(store, tension_var, 0.0), 0.0, 0.0, 1.0)
        else:
            target = 1.0
        return _fx_step(key, target, relax, st, start=target)

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
        px = _fx_step("cam_px", tx, smooth, st, start=0.0)
        py = _fx_step("cam_py", ty, smooth, st, start=0.0)

        ## Мелкая дрожь: не тряска, а зуд-раздражение. Короткий диапазон,
        ## лёгкое сглаживание рывков между кадрами.
        t = _fx_tension(tension_var, relax, st, "cam_tension")
        amp = shake_amp * t
        jx = _fx_step("cam_jx", renpy.random.uniform(-amp, amp), 0.5, st, start=0.0)
        jy = _fx_step("cam_jy", renpy.random.uniform(-amp, amp), 0.5, st, start=0.0)

        trans.xoffset = px + jx
        trans.yoffset = py + jy
        return 1.0 / 60.0

    def mouse_follow_f(rx, ry, smooth, trans, st, at):
        """function-трансформ: слой смещается так, чтобы его опорная точка
        (rx, ry в координатах изображения) плавно следовала за курсором.

        rx, ry — опорная точка изображения (px);
        smooth — доля пути к цели за кадр (0..1).
        """
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
        """function-трансформ зерна: сила = strength × напряжение (0..1)."""
        strength = _fx_num(strength, 0.1, 0.0, 1.0)
        relax = _fx_num(relax, 0.04, 0.001, 1.0)
        trans.u_strength = strength * _fx_tension(tension_var, relax, st, "noise_tension")
        return 1.0 / 60.0

    def object_jitter_f(amp, relax, key, trans, st, at):
        """function-трансформ: лёгкая дрожь объекта — добавочный xoffset/
        yoffset поверх уже заданной pos/anchor. Годится для сцен напряжения
        (дрожащие руки и т.п.); использовать как ещё один parallel-трек внутри
        трансформа сцены, рядом с ease по pos/alpha — тогда дрожь складывается
        с движением аддитивно, не заменяя его.

        amp   — амплитуда дрожи, px;
        relax — сглаживание рывков между кадрами (0..1), выше — резче;
        key   — идентификатор состояния в _fx_state; разным одновременно
                дрожащим объектам нужны разные key, иначе делят один накопитель.
        """
        amp = _fx_num(amp, 3.0, 0.0)
        relax = _fx_num(relax, 0.5, 0.001, 1.0)

        jx = _fx_step(key + "_jx", renpy.random.uniform(-amp, amp), relax, st, start=0.0)
        jy = _fx_step(key + "_jy", renpy.random.uniform(-amp, amp), relax, st, start=0.0)
        trans.xoffset = jx
        trans.yoffset = jy
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

## Слой следует за курсором: опорная точка изображения (rx, ry) плавно
## тянется к позиции мыши. Начальное смещение нулевое — слой «поднимается»
## со своего исходного места и догоняет курсор.
transform mouse_follow(rx, ry, smooth=0.12):
    subpixel True
    xoffset 0.0 yoffset 0.0
    function renpy.curry(mouse_follow_f)(rx, ry, smooth)

## Полноэкранные зерно-помехи. Показываются всегда поверх всей игры (см.
## fx_noise_screen ниже) — руками через `show fx_noise at noise_overlay(...)`
## включать не нужно, эффект уже глобальный.
##     show fx_noise at noise_overlay(strength, relax, "имя_переменной")
## Без tension_var сила постоянна и равна strength.
image fx_noise = Solid("#FFF")

transform noise_overlay(strength=0.1, relax=0.04, tension_var=None):
    mesh True
    shader "sm.noise"
    u_strength 0.0
    function renpy.curry(noise_overlay_f)(strength, relax, tension_var)

## Сила фонового зерна-помех (0..1) — общая на всю игру. Сцены могут временно
## поднимать/опускать значение через `$ fx_noise_strength = ...`; переход
## плавный (см. relax в noise_overlay_f выше).
default fx_noise_strength = 0.10

## Постоянный оверлей зерна: зарегистрирован в config.always_shown_screens,
## поэтому виден всегда — от главного меню до любой сцены — и не пропадает при
## `scene` (тот очищает только слой master, не слой screens).
screen fx_noise_screen():
    add "fx_noise" at noise_overlay(1.0, tension_var="fx_noise_strength")

init python:
    config.always_shown_screens.append("fx_noise_screen")

## Тревожное покачивание камеры: непрерывный дрейф позиции и лёгкий наклон.
##
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
