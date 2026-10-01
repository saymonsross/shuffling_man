## Параллакс за мышью на весь проект — по образцу plenka.
## Сцены его не объявляют: слой master целиком едет через config.layer_transforms,
## снаружи camera, поэтому зумы, наезды и дрожь сцен работают поверх как раньше.
## lockgame и UI не двигаются: хит-зоны мини-игр остаются под курсором.
## World-space кнопки повторяют сдвиг через follow_camera или parallax_follow,
## ближний план добавляет своё смещение трансформом parallax_near.
## Многослойный кадр с глубиной — depth_scene(): планы от дальнего к ближнему, каждый едет
## за мышью сильнее предыдущего и слегка увеличен, чтобы сдвиг не открывал края.

## Сцена гасит параллакс локально: $ sm_parallax_off = True … False.
default sm_parallax_off = False

init -10 python:

    fx_param("parallax.amp", 22, 0, 60, doc="сдвиг слоя master при мыши у края экрана, px")
    fx_param("parallax.near", 6, 0, 60, doc="добавка ближнего плана к сдвигу слоя, px")
    fx_param("parallax.smooth", 0.1, 0.005, 1.0, step=0.005, doc="доля пути за кадр 60 Гц; меньше — плавнее")
    fx_param("parallax.plane", 10, 0, 60, doc="шаг глубины между планами depth_scene, px на план")
    fx_group("parallax", "Параллакс")

    def sm_parallax_active():
        if not persistent.sm_parallax or store.sm_parallax_off or store.main_menu or sm_reduced_motion() or fx_cfg_bypassed():
            return False
        ## Автотесты сравнивают кадры с эталонами, Position Tuner рисует в координатах экрана.
        if renpy.game.args.command == "test":
            return False
        return renpy.get_screen("position_tuner") is None

    def _sm_parallax_state():
        """(level, mx, my): level плавно включает сдвиг и запас зума вместе,
        поэтому зум покрывает сдвиг и во время включения/выключения."""
        if renpy.predicting():
            return (_fx_state.get("parallax_level", 0.0),
                _fx_state.get("parallax_mx", 0.0), _fx_state.get("parallax_my", 0.0))
        ## Главное меню и его подменю неподвижны сразу, без затухания после выхода из игры.
        if sm_reduced_motion() or store.main_menu:
            for name in ("parallax_level", "parallax_mx", "parallax_my"):
                _fx_state[name] = 0.0
            return 0.0, 0.0, 0.0

        active = sm_parallax_active()
        smooth = fx_cfg("parallax.smooth")
        level = _fx_step("parallax_level", 1.0 if active else 0.0, smooth, start=1.0 if active else 0.0)
        x, y = renpy.get_mouse_pos()
        tx = max(-1.0, min(1.0, (x / float(config.screen_width) - 0.5) * 2.0))
        ty = max(-1.0, min(1.0, (y / float(config.screen_height) - 0.5) * 2.0))
        mx = _fx_step("parallax_mx", tx, smooth, start=0.0)
        my = _fx_step("parallax_my", ty, smooth, start=0.0)
        return level, mx, my

    def _sm_parallax_shift(amp, level, mx, my):
        ## По вертикали амплитуда в пропорции кадра: один запас зума покрывает обе оси.
        amp *= level
        return -mx * amp, -my * amp * config.screen_height / float(config.screen_width)

    def sm_parallax_frame():
        """(zoom, xoffset, yoffset) слоя master в этом кадре."""
        level, mx, my = _sm_parallax_state()
        amp = fx_cfg("parallax.amp")
        px, py = _sm_parallax_shift(amp, level, mx, my)
        ## +1 px запаса против субпиксельной кромки.
        zoom = 1.0 + 2.0 * (amp + 1.0) / config.screen_width * level if amp > 0 else 1.0
        return zoom, px, py

    def sm_parallax_compose(zoom, rotate, xoffset, yoffset):
        """Камера сцены, пересчитанная через трансформ слоя: слой масштабирует её
        вокруг центра экрана и сдвигает, поворот с равномерным зумом коммутирует."""
        lz, px, py = sm_parallax_frame()
        return zoom * lz, rotate, xoffset * lz + px, yoffset * lz + py

    ## Трансформ слоя попадает в сейвы вместе со SceneLists: после релиза не
    ## переименовывать parallax_bg и parallax_bg_f.
    def parallax_bg_f(trans, st, at):
        trans.zoom, trans.xoffset, trans.yoffset = sm_parallax_frame()
        ## Выключенный параллакс не перерисовывает слой каждый кадр; включение перезапускает интеракцию.
        if sm_parallax_active() or _fx_state.get("parallax_level", 0.0) > 0.0001:
            return 1.0 / 60.0
        return 0.1

    def parallax_near_f(trans, st, at):
        """Добавка ближнего плана: спрайт уже едет вместе со слоем."""
        level, mx, my = _sm_parallax_state()
        trans.xoffset, trans.yoffset = _sm_parallax_shift(fx_cfg("parallax.near"), level, mx, my)
        return 1.0 / 60.0

    def parallax_plane_f(depth, trans, st, at):
        """План глубины depth: сдвиг depth·parallax.plane px и запас зума под него,
        как у слоя master. depth 0 — задник, едет только вместе со слоем."""
        level, mx, my = _sm_parallax_state()
        amp = fx_cfg("parallax.plane") * depth
        trans.xoffset, trans.yoffset = _sm_parallax_shift(amp, level, mx, my)
        trans.zoom = 1.0 + 2.0 * (amp + 1.0) / config.screen_width * level if amp > 0 else 1.0
        return 1.0 / 60.0

    def depth_scene(*planes, **kwargs):
        """Кадр из планов глубины, от дальнего к ближнему: план — образ или кортеж
        образов на одной глубине, все холсты 1920×1080. step — множитель шага глубины.
        Применяется как обычный кадр: scene … с breath_brightness и Dissolve."""
        step = kwargs.pop("step", 1.0)
        assert not kwargs, kwargs
        items = []
        for depth, plane in enumerate(planes):
            for img in (plane if isinstance(plane, (tuple, list)) else (plane,)):
                items.append(At(img, parallax_plane(depth * step)))
        return Fixed(*items, xysize=(config.screen_width, config.screen_height))

    def parallax_follow_f(trans, st, at):
        trans.zoom, trans.rotate, trans.xoffset, trans.yoffset = sm_parallax_compose(1.0, 0.0, 0.0, 0.0)
        _fx_state["ui_follow"] = (trans.zoom, trans.rotate, trans.xoffset, trans.yoffset)
        return 0.0

transform parallax_bg():
    subpixel True
    align (0.5, 0.5)
    function parallax_bg_f

transform parallax_near():
    subpixel True
    function parallax_near_f

transform parallax_plane(depth=1.0):
    subpixel True
    align (0.5, 0.5)
    function renpy.curry(parallax_plane_f)(depth)

## World-space UI без camera сцены: полноэкранный контейнер повторяет слой master.
transform parallax_follow():
    subpixel True
    align (0.5, 0.5)
    function parallax_follow_f

## Раньше постеризации (init 999): эффект ложится на уже сдвинутый слой.
init 2 python hide:
    config.layer_transforms.setdefault("master", []).append(parallax_bg())
