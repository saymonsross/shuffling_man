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

    def _fx_frame_time():
        ## SDK 8.5.3 фиксирует это время на весь render; st сбрасывается при смене ATL.
        return renpy.game.interface.frame_time

    def _fx_step(key, target, relax, start):
        """relax задан для 60 Hz; callable-цель вычисляется только на новом кадре."""
        cur = _fx_state.get(key, start)
        if renpy.predicting():
            return cur

        now = _fx_frame_time()
        clock_key = (key, "time")
        previous = _fx_state.get(clock_key)
        dt = 1.0 / 60.0 if previous is None else now - previous
        if dt <= 0.0:
            ## Смена часов не сбрасывает позицию и не замораживает эффект до старой даты.
            if dt < 0.0:
                _fx_state[clock_key] = now
            return cur

        value = target() if callable(target) else target
        ## После скрытого окна не отыгрываем весь простой одним скачком.
        blend = 1.0 - (1.0 - relax) ** (min(dt, 0.25) * 60.0)
        cur += (value - cur) * blend
        _fx_state[clock_key] = now
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

    def camera_shake_f(shake_amp, relax, tension_var, key, trans, st, at):
        """Дрожь камеры от tension_var; key уникален для каждого
        одновременного эффекта."""
        if renpy.predicting():
            return 1.0 / 60.0
        if sm_reduced_motion():
            _fx_state[key + "_jx"] = 0.0
            _fx_state[key + "_jy"] = 0.0
            trans.xoffset = 0.0
            trans.yoffset = 0.0
            _fx_publish_camera(key, trans)
            return 1.0 / 60.0
        shake_amp = _fx_num(shake_amp, 0.0, 0.0)
        relax = _fx_num(relax, 0.04, 0.001, 1.0)

        t = _fx_tension(tension_var, relax, key + "_tension")
        amp = shake_amp * t
        jx = _fx_step(key + "_jx", lambda: _fx_visual_jitter(amp), 0.5, start=0.0)
        jy = _fx_step(key + "_jy", lambda: _fx_visual_jitter(amp), 0.5, start=0.0)

        trans.xoffset = jx
        trans.yoffset = jy
        _fx_publish_camera(key, trans)
        return 1.0 / 60.0

    def _focus_offset(focus_align, screen_align, z):
        """Совмещает focus_align изображения со screen_align экрана пиксельным
        offset: дробные anchor/pos камеры артефактят на Windows/ANGLE."""
        fx, fy = focus_align
        sx, sy = (screen_align or focus_align)
        ox = config.screen_width * (sx - 0.5 - (fx - 0.5) * z)
        oy = config.screen_height * (sy - 0.5 - (fy - 0.5) * z)
        return ox, oy

    def focus_camera_f(focus_align, screen_align, key, trans, st, at):
        """Держит focus_align в screen_align при текущем trans.zoom."""
        if renpy.predicting():
            return 1.0 / 60.0
        trans.xoffset, trans.yoffset = _focus_offset(focus_align, screen_align, trans.zoom or 1.0)
        _fx_publish_camera(key, trans)
        return 1.0 / 60.0

    def _fx_publish_camera(key, trans):
        ## master рендерится перед screens; UI получает итоговый transform этого кадра.
        _fx_state[(key, "camera")] = (
            trans.zoom, trans.rotate, trans.xoffset, trans.yoffset)

    def follow_camera_f(key, zoom_pad, trans, st, at):
        """Копирует камеру целиком и добавляет параллакс слоя master."""
        snapshot = _fx_state.get((key, "camera")) or (zoom_pad, 0.0, 0.0, 0.0)
        trans.zoom, trans.rotate, trans.xoffset, trans.yoffset = sm_parallax_compose(*snapshot)
        _fx_state["ui_follow"] = (trans.zoom, trans.rotate, trans.xoffset, trans.yoffset)
        ## ATL-зум камеры меняется каждый кадр даже при статичном содержимом кнопки.
        return 0.0

    def mouse_follow_f(rx, ry, smooth, key, trans, st, at):
        if renpy.predicting():
            return 1.0 / 60.0
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

    def object_jitter_f(amp, relax, key, trans, st, at):
        """Аддитивный jitter поверх ATL; key должен быть уникален для объекта."""
        if renpy.predicting():
            return 1.0 / 60.0
        amp = _fx_num(amp, 3.0, 0.0)
        relax = _fx_num(relax, 0.5, 0.001, 1.0)

        if sm_reduced_motion():
            _fx_state[key + "_jx"] = 0.0
            _fx_state[key + "_jy"] = 0.0
            trans.xoffset = 0.0
            trans.yoffset = 0.0
            return 1.0 / 60.0

        jx = _fx_step(key + "_jx", lambda: _fx_visual_jitter(amp), relax, start=0.0)
        jy = _fx_step(key + "_jy", lambda: _fx_visual_jitter(amp), relax, start=0.0)
        trans.xoffset = jx
        trans.yoffset = jy
        return 1.0 / 60.0

## Зум покоя камеры: кадры сцен скомпонованы с этим запасом по краям.
define FX_CAMERA_ZOOM_PAD = 1.02

## Неподвижная камера с необязательной дрожью.
## Явный rotate 0.0 сбрасывает наклон, унаследованный от предыдущего camera at.
transform camera_rest(zoom_pad=FX_CAMERA_ZOOM_PAD, shake_amp=0.0, relax=0.04, tension_var=None, key="cam"):
    subpixel True
    align (0.5, 0.5) zoom zoom_pad
    rotate 0.0
    xoffset 0.0 yoffset 0.0
    function renpy.curry(camera_shake_f)(shake_amp, relax, tension_var, key)

## World-space UI: размер контейнера и key совпадают с камерой.
## zoom_pad задаёт только начальное значение до первого кадра камеры.
transform follow_camera(key="cam", zoom_pad=FX_CAMERA_ZOOM_PAD):
    subpixel True
    align (0.5, 0.5) zoom zoom_pad
    xoffset 0.0 yoffset 0.0
    function renpy.curry(follow_camera_f)(key, zoom_pad)

## focus_align удерживается в screen_align во время зума. Пиксельные offsets
## обязательны: дробные anchor/pos камеры дают артефакты на части render paths.
## Зум-трек идёт первым, поскольку function читает trans.zoom текущего кадра.
transform camera_push(focus_align, z0, z1, t, key="cam", screen_align=None):
    subpixel True
    align (0.5, 0.5)
    zoom (z1 if sm_reduced_motion() else z0)
    parallel:
        ease sm_motion_time(t) zoom z1
    parallel:
        function renpy.curry(focus_camera_f)(focus_align, screen_align, key)

transform camera_settle(focus_align, z0, z1, t, key="cam", screen_align=None):
    subpixel True
    align (0.5, 0.5)
    zoom (z1 if sm_reduced_motion() else z0)
    parallel:
        easein sm_motion_time(t) zoom z1
    parallel:
        function renpy.curry(focus_camera_f)(focus_align, screen_align, key)

transform mouse_follow(rx, ry, smooth=0.12, key="follow"):
    subpixel True
    xoffset 0.0 yoffset 0.0
    function renpy.curry(mouse_follow_f)(rx, ry, smooth, key)

## Зерно — один экран на всю игру постоянной силы: вид задаёт fx_config.yaml (F10),
## сцены его не меняют. Слой top лежит поверх всех слоёв и меню и не участвует в
## переходах, camera и постеризации. Он очищается в каждом новом контексте (меню, H),
## а always_shown сразу показывает экран снова — копия всегда ровно одна.
init -10 python:

    fx_param("noise.enabled", True, doc="включить зерно")
    fx_param("noise.strength", 0.10, 0.0, 1.0, step=0.01, doc="сила зерна поверх всей игры")
    fx_param("noise.steps", 0, 0, 32, doc="ступеней серого в зерне; 0 — без постеризации, от 2 — ступени")
    fx_group("noise", "Зерно")

    def noise_overlay_f(trans, st, at):
        on = fx_cfg("noise.enabled") and not fx_cfg_bypassed() and not sm_reduced_motion()
        trans.u_strength = fx_cfg("noise.strength") if on else 0.0
        steps = fx_cfg("noise.steps")
        trans.u_noise_steps = float(steps) if steps >= 2 else 0.0
        ## Кадр нужен каждый раз: u_random шейдера меняется только при перерисовке.
        return 1.0 / 60.0

image fx_noise = Solid("#FFF")

transform noise_overlay():
    mesh True
    shader "sm.noise"
    u_strength 0.0
    u_noise_steps 0.0
    function noise_overlay_f

screen fx_noise_screen():
    layer "top"
    add "fx_noise" at noise_overlay

init python:
    config.always_shown_screens.append("fx_noise_screen")

## Постеризация: вид задаёт fx_config.yaml (F10), интенсивность по сюжету —
## fx_posterize_strength (0..1); после сцены вернуть к FX_POSTERIZE_DEFAULT.
define FX_POSTERIZE_DEFAULT = 1.0
default fx_posterize_strength = FX_POSTERIZE_DEFAULT

## Пикселизация — так же: вид в fx_config.yaml, сила по сюжету — fx_pixelate_strength
## (0..1, множитель к размеру ячейки); после сцены вернуть к FX_PIXELATE_DEFAULT.
define FX_PIXELATE_DEFAULT = 1.0
default fx_pixelate_strength = FX_PIXELATE_DEFAULT

## Аберрация — так же: сила по сюжету fx_chroma_strength (0..1, множитель к смещениям).
define FX_CHROMA_DEFAULT = 1.0
default fx_chroma_strength = FX_CHROMA_DEFAULT

## Bloom — так же: сила по сюжету fx_bloom_strength (0..FX_BLOOM_MAX, множитель к
## bloom.intensity), меняется плавно в обе стороны (bloom.relax). Мгновенно — через
## fx_bloom_snap(сила): например, свет щёлкнул выключателем.
define FX_BLOOM_DEFAULT = 1.0
define FX_BLOOM_MAX = 3.0
default fx_bloom_strength = FX_BLOOM_DEFAULT

## Охват scene — все слои config.layers, кроме UI: новый слой мира (как lockgame
## у мини-игры замков) получает эффекты сам, если добавлен в init.
## forever — экраны 7dots show_forever, которые не прячутся по H.
define FX_LAYER_UI_LAYERS = ("transient", "screens", "overlay", "forever")

init -10 python:

    fx_param("posterize.enabled", False, doc="включить постеризацию")
    fx_param("posterize.scope", "scene", choices=("scene", "screen"),
        doc="scene — сцена без UI, screen — весь экран с UI")
    fx_param("posterize.steps", 5, 2, 32, doc="уровней на канал")
    fx_param("posterize.mix", 1.0, 0.0, 1.0, doc="сила: смешивание с оригиналом")
    fx_param("posterize.gamma", 1.0, 0.25, 4.0, step=0.05,
        doc="больше 1 — больше ступеней в тенях; 1 — как в Unity")
    fx_param("posterize.relax", 0.04, 0.005, 1.0, step=0.005,
        doc="плавность смены fx_posterize_strength")

    fx_param("pixelate.enabled", False, doc="включить пикселизацию")
    fx_param("pixelate.scope", "scene", choices=("scene", "screen"),
        doc="scene — сцена без UI, screen — весь экран с UI")
    fx_param("pixelate.size", 8, 2, 64, doc="размер пикселя в точках экрана 1920×1080")
    fx_param("pixelate.relax", 0.04, 0.005, 1.0, step=0.005,
        doc="плавность смены fx_pixelate_strength")

    fx_param("grade.enabled", False, doc="включить ретушь")
    fx_param("grade.scope", "scene", choices=("scene", "screen"),
        doc="scene — сцена без UI, screen — весь экран с UI")
    fx_param("grade.brightness", 0.0, -0.5, 0.5, step=0.01, doc="яркость: сдвиг, 0 — без изменений")
    fx_param("grade.contrast", 1.0, 0.0, 2.0, step=0.01, doc="контраст: 1 — без изменений")
    fx_param("grade.saturation", 1.0, 0.0, 2.0, step=0.01, doc="насыщенность: 0 — ч/б, 1 — без изменений")

    fx_param("chroma.enabled", False, doc="включить хроматическую аберрацию")
    fx_param("chroma.scope", "scene", choices=("scene", "screen"),
        doc="scene — сцена без UI, screen — весь экран с UI")
    fx_param("chroma.red", 0.009, -0.05, 0.05, step=0.001, doc="смещение красного от центра; 0 — на месте")
    fx_param("chroma.green", 0.006, -0.05, 0.05, step=0.001, doc="смещение зелёного от центра")
    fx_param("chroma.blue", -0.006, -0.05, 0.05, step=0.001, doc="смещение синего от центра")
    fx_param("chroma.relax", 0.04, 0.005, 1.0, step=0.005,
        doc="плавность смены fx_chroma_strength")

    fx_param("bloom.enabled", False, doc="включить свечение ярких мест")
    fx_param("bloom.scope", "scene", choices=("scene", "screen"),
        doc="scene — сцена без UI, screen — весь экран с UI")
    fx_param("bloom.threshold", 0.7, 0.0, 1.0, step=0.01, doc="порог яркости, выше которого светится")
    fx_param("bloom.knee", 0.5, 0.0, 1.0, step=0.01, doc="мягкость порога: 0 — резкая граница")
    fx_param("bloom.intensity", 0.6, 0.0, 3.0, step=0.05, doc="сила свечения")
    fx_param("bloom.radius", 24, 4, 128, doc="радиус свечения в точках экрана 1920×1080")
    fx_param("bloom.relax", 0.03, 0.005, 1.0, step=0.005,
        doc="плавность спада fx_bloom_strength")

    def _fx_grade_identity():
        return (fx_cfg("grade.brightness") == 0.0 and fx_cfg("grade.contrast") == 1.0
            and fx_cfg("grade.saturation") == 1.0)

    def _fx_story_level(key, var, default, relax, hi=1.0, snap_up=False, frame=None):
        """(сглаженная сила от сцены, цель); превью тюнера подменяет цель полной.
        frame — доля от fx_frame показанного кадра (None — кадр её не задал)."""
        if fx_cfg_runtime["preview"]:
            target = 1.0
        else:
            target = _fx_num(getattr(store, var, default), default, 0.0, hi)
            if frame is not None:
                target = min(hi, target * frame)
        ## _fx_step после подстановки всё равно нужен: он ведёт часы накопителя.
        if snap_up and target > _fx_state.get(key, target):
            _fx_state[key] = target
        ## Один накопитель эффекта на все слои намеренно: цель у них общая, а _fx_step
        ## делает не больше одного шага за кадр, поэтому слои не тянут его друг у друга.
        return _fx_step(key, target, relax, start=target), target

    def _fx_posterize_level():
        return _fx_story_level("posterize_level", "fx_posterize_strength",
            FX_POSTERIZE_DEFAULT, fx_cfg("posterize.relax"))

    def _fx_pixelate_level():
        return _fx_story_level("pixelate_level", "fx_pixelate_strength",
            FX_PIXELATE_DEFAULT, fx_cfg("pixelate.relax"))

    def _fx_chroma_level():
        return _fx_story_level("chroma_level", "fx_chroma_strength",
            FX_CHROMA_DEFAULT, fx_cfg("chroma.relax"))

    def _fx_bloom_level():
        return _fx_story_level("bloom_level", "fx_bloom_strength",
            FX_BLOOM_DEFAULT, fx_cfg("bloom.relax"), hi=FX_BLOOM_MAX, frame=fx_frame_value("bloom"))

    ## Эффекты кадра: fx_frame в ATL кадра при каждой отрисовке отмечает свои доли, эффекты
    ## берут отметку не старше FX_FRAME_TTL секунд. Кадр ушёл — отметка устарела, и эффекты
    ## сами плавно возвращаются к сюжетным: возвращать руками нечего, в сейвы не попадает.
    ## Слой эффектов рисуется раньше кадра внутри него и видит отметку прошлой отрисовки.
    FX_FRAME_TTL = 0.25

    def fx_frame_f(bloom, vignette, trans, st, at):
        if not renpy.predicting():
            now = _fx_frame_time()
            if bloom is not None:
                _fx_state[("fx_frame", "bloom")] = (float(bloom), now)
            if vignette is not None:
                _fx_state[("fx_frame", "vignette")] = (float(vignette), now)
        return 0

    def fx_frame_value(name):
        mark = _fx_state.get(("fx_frame", name))
        if mark is None or _fx_frame_time() - mark[1] > FX_FRAME_TTL:
            return None
        return mark[0]

    def fx_bloom_snap(strength):
        """Сила bloom сразу, без сглаживания. Накопитель визуальный: после отката или
        загрузки сила придёт к той же цели плавно."""
        store.fx_bloom_strength = strength
        _fx_state["bloom_level"] = _fx_num(strength, FX_BLOOM_DEFAULT, 0.0, FX_BLOOM_MAX)

    ## Трансформ слоя попадает в сейвы вместе со SceneLists: после релиза не
    ## переименовывать fx_layer и fx_layer_f.
    def fx_layer_f(scope, trans, st, at):
        """Все эффекты слоя — один проход в текстуру: пикселизация, аберрация, bloom, ретушь, постеризация."""
        if renpy.predicting():
            return 1.0 / 60.0
        p_level, p_target = _fx_posterize_level()
        x_level, x_target = _fx_pixelate_level()
        c_level, c_target = _fx_chroma_level()
        b_level, b_target = _fx_bloom_level()
        shaders = python_list()
        bloom = False
        if not fx_cfg_bypassed():
            size = fx_cfg("pixelate.size") * x_level
            ## Ячейка меньше полутора точек неотличима от исходника.
            pixel = fx_cfg("pixelate.enabled") and fx_cfg("pixelate.scope") == scope and size >= 1.5
            offsets = tuple(fx_cfg("chroma." + ch) * c_level for ch in ("red", "green", "blue"))
            chroma = (fx_cfg("chroma.enabled") and fx_cfg("chroma.scope") == scope
                and max(abs(o) for o in offsets) > 0.0001)
            ## Аберрация сама снапит выборки к сетке пикселизации — отдельный проход не нужен.
            if chroma:
                shaders.append("sm.chroma")
                trans.u_chroma_offsets = offsets
                trans.u_chroma_cell = float(size) if pixel else 0.0
            elif pixel:
                shaders.append("sm.pixelate")
                trans.u_pixelate_size = float(size)
            if scope == "scene" and sm_rift_layer(trans):
                shaders.append("sm.rift")
            intensity = fx_cfg("bloom.intensity") * b_level
            bloom = (fx_cfg("bloom.enabled") and fx_cfg("bloom.scope") == scope
                and intensity > 0.001)
            if bloom:
                shaders.append("sm.bloom")
                trans.u_bloom_threshold = fx_cfg("bloom.threshold")
                trans.u_bloom_knee = fx_cfg("bloom.knee")
                trans.u_bloom_intensity = intensity
                trans.u_bloom_radius = float(fx_cfg("bloom.radius"))
            if fx_cfg("grade.enabled") and fx_cfg("grade.scope") == scope and not _fx_grade_identity():
                shaders.append("sm.grade")
                trans.u_grade_brightness = fx_cfg("grade.brightness")
                trans.u_grade_contrast = fx_cfg("grade.contrast")
                trans.u_grade_saturation = fx_cfg("grade.saturation")
            mix = fx_cfg("posterize.mix") * p_level
            if fx_cfg("posterize.enabled") and fx_cfg("posterize.scope") == scope and mix > 0.001:
                shaders.append("sm.posterize")
                trans.u_posterize_steps = float(fx_cfg("posterize.steps"))
                trans.u_posterize_mix = mix
                trans.u_posterize_gamma = fx_cfg("posterize.gamma")
        ## Без эффектов mesh снимается: иначе слой каждый кадр рендерится в лишнюю текстуру.
        if shaders:
            trans.mesh = True
            trans.shader = shaders
            ## Mipmap-копию слоя читает только bloom; без него её не строим.
            trans.gl_mipmap = bloom
            return 1.0 / 60.0
        trans.mesh = False
        trans.shader = None
        ## Правки тюнера и сцены перезапускают интеракцию сами; кадры нужны только затуханию.
        settling = any(abs(l - t) > 0.001 for l, t in
            ((p_level, p_target), (x_level, x_target), (c_level, c_target), (b_level, b_target)))
        return 1.0 / 60.0 if settling else 0.1

    def _fx_story_status(var, key, value):
        strength = getattr(store, var, None)
        level = _fx_state.get(key)
        text = "%s = %s" % (var, "—" if strength is None else "%.2f" % strength)
        if level is not None:
            text += " · итог %s" % value(level)
        return text

    def fx_posterize_status():
        return _fx_story_status("fx_posterize_strength", "posterize_level",
            lambda level: "%.2f" % (fx_cfg("posterize.mix") * level))

    def fx_pixelate_status():
        return _fx_story_status("fx_pixelate_strength", "pixelate_level",
            lambda level: "%.1f px" % (fx_cfg("pixelate.size") * level))

    fx_group("posterize", "Постеризация", fx_posterize_status)
    fx_group("pixelate", "Пикселизация", fx_pixelate_status)
    fx_group("grade", "Ретушь")

    def fx_bloom_status():
        return _fx_story_status("fx_bloom_strength", "bloom_level",
            lambda level: "%.2f" % (fx_cfg("bloom.intensity") * level))

    fx_group("bloom", "Bloom", fx_bloom_status)

    def fx_chroma_status():
        return _fx_story_status("fx_chroma_strength", "chroma_level", lambda level: "%.2f" % level)

    fx_group("chroma", "Хроматическая аберрация", fx_chroma_status)

transform fx_layer(scope="scene"):
    function renpy.curry(fx_layer_f)(scope)

## Доли эффектов, пока кадр на экране: bloom=0.0 — без свечения, vignette=0.6 — виньетка на
## 40% слабее. В ATL кадра — отдельной веткой parallel: функция не завершается.
transform fx_frame(bloom=None, vignette=None):
    function renpy.curry(fx_frame_f)(bloom, vignette)

## init 999 — после всех add_layer. layer_transforms работают снаружи camera,
## поэтому эффекты не спорят с camera at сцен.
init 999 python hide:
    for name in config.layers:
        if name not in FX_LAYER_UI_LAYERS:
            config.layer_transforms.setdefault(name, []).append(fx_layer("scene"))
    config.layer_transforms.setdefault(None, []).append(fx_layer("screen"))

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
