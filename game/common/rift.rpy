## «Разлом» под сценовыми кнопками: пространство за кнопкой плывёт рябью, рвётся
## строками и расслаивается по цветам. Шейдер не видит, что лежит под кнопкой, поэтому
## искажается сам слой сцены (fx_layer, camera_fx.rpy) в экранной точке кнопки.
## Кнопка отмечается маяком rift_beacon каждый кадр; пропал маяк — пятно гаснет.
## Вид — fx_config.yaml (F10, группа rift).

init -10 python:

    import math

    fx_param("rift.enabled", True, doc="включить разлом под сценовыми кнопками")
    fx_param("rift.idle", 0.55, 0.0, 1.0, step=0.01, doc="сила без наведения")
    fx_param("rift.hover", 1.0, 0.0, 1.0, step=0.01, doc="сила при наведении")
    fx_param("rift.scale", 1.15, 0.3, 3.0, step=0.01, doc="размер пятна относительно кнопки")
    fx_param("rift.soft", 0.6, 0.05, 1.0, step=0.01, doc="мягкость края пятна")
    fx_param("rift.amp", 9.0, 0.0, 40.0, step=0.5, doc="размах ряби, px")
    fx_param("rift.freq", 9.0, 1.0, 40.0, step=0.5, doc="частота ряби по пятну")
    fx_param("rift.speed", 1.0, 0.0, 5.0, step=0.05, doc="скорость ряби")
    fx_param("rift.rgb", 5.0, 0.0, 30.0, step=0.5, doc="расслоение каналов к краю пятна, px")
    fx_param("rift.tear", 14.0, 0.0, 60.0, step=0.5, doc="сдвиг рваных строк, px")
    fx_param("rift.tear_rate", 0.12, 0.0, 1.0, step=0.01, doc="доля рваных строк")
    fx_param("rift.glow", 0.0, 0.0, 1.0, step=0.01, doc="свечение под текстом: сила, 0 — нет")
    fx_param("rift.glow_size", 1.0, 0.3, 3.0, step=0.01, doc="свечение: размер овала относительно кнопки")
    fx_param("rift.glow_soft", 0.7, 0.05, 1.0, step=0.01, doc="свечение: мягкость края")
    fx_param("rift.glow_core", 1.2, 0.1, 5.0, step=0.05, doc="свечение: плотность ядра, больше — уже")
    fx_param("rift.glow_color", "#f5f0e3", doc="свечение: цвет")
    fx_param("rift.glow_breath_t", 0.8, 0.1, 5.0, step=0.05, doc="свечение: моргание, половина цикла, с")
    fx_param("rift.glow_grow", 1.06, 1.0, 1.5, step=0.01, doc="свечение: раздувание на вдохе; 1 — без")
    fx_param("rift.glow_low", 0.65, 0.0, 1.0, step=0.01, doc="свечение: яркость на выдохе; 1 — не моргает")
    fx_param("rift.blink", 0.12, 0.0, 1.0, step=0.01, doc="белое мерцание за кнопкой: сила на пике, 0 — нет")
    fx_param("rift.blink_size", 0.43, 0.3, 3.0, step=0.01, doc="белое мерцание: размер овала относительно кнопки")
    fx_param("rift.blink_wide", 1.8, 0.5, 3.0, step=0.05, doc="белое мерцание: растяжение по ширине")
    fx_param("rift.blink_t", 1.4, 0.2, 5.0, step=0.05, doc="белое мерцание: разгорание и угасание, половина цикла, с")
    fx_param("rift.fade", 0.3, 0.0, 2.0, step=0.05, doc="появление, исчезание и смена силы при наведении, с")
    fx_group("rift", "Разлом (сценовые кнопки)")

    ## Четыре пятна: больше сценовых кнопок одновременно не бывает.
    ## Приоритет 265 — после пикселизации и аберрации (они заново читают tex0),
    ## до bloom, ретуши и постеризации: те ложатся уже на разлом.
    renpy.register_shader("sm.rift",
        variables="""
        uniform sampler2D tex0;
        uniform vec2 u_model_size;
        uniform vec4 u_rift_spot0;
        uniform vec4 u_rift_spot1;
        uniform vec4 u_rift_spot2;
        uniform vec4 u_rift_spot3;
        uniform vec4 u_rift_k;
        uniform float u_rift_time;
        uniform float u_rift_soft;
        uniform float u_rift_amp;
        uniform float u_rift_freq;
        uniform float u_rift_rgb;
        uniform float u_rift_tear;
        uniform float u_rift_tear_rate;
        attribute vec2 a_tex_coord;
        varying vec2 v_tex_coord;
        """,
        fragment_functions="""
        // fragment_functions идут до объявления uniform: параметры — аргументами.
        // w: x — время, y — мягкость края, z — частота ряби, w — размах ряби;
        // tear: x — сдвиг рваных строк, y — их доля.
        void sm_rift_spot(vec4 spot, float k, vec2 p, vec4 w, vec2 tear,
                inout vec2 disp, inout vec2 dir, inout float m) {
            if (k <= 0.0) return;
            vec2 q = (p - spot.xy) / max(spot.zw, vec2(1.0));
            float d = length(q);
            float f = (1.0 - smoothstep(1.0 - w.y, 1.0, d)) * k;
            if (f <= 0.0) return;
            float t = w.x;
            float fr = w.z;
            float w1 = sin(q.y * fr + t * 2.3 + sin(q.x * fr * 0.7 - t * 1.7));
            float w2 = cos(q.x * fr * 1.3 - t * 1.9 + sin(q.y * fr * 0.5 + t));
            disp += vec2(w1, w2) * w.w * f;
            // Рваные строки: полосы по 6 px, набор меняется рывками 9 раз в секунду.
            float band = floor((p.y - spot.y) / 6.0);
            float n = fract(sin(band * 12.9898 + floor(t * 9.0) * 78.233 + spot.x) * 43758.5453);
            float cut = 1.0 - tear.y;
            if (n > cut) {
                disp.x += (n - cut) / max(tear.y, 0.001) * tear.x * f * (fract(n * 7.0) > 0.5 ? 1.0 : -1.0);
            }
            dir += q * f;
            m = max(m, f);
        }
        """,
        vertex_300="""
        v_tex_coord = a_tex_coord;
        """,
        fragment_265="""
        {
            vec2 p = v_tex_coord * u_model_size;
            vec2 disp = vec2(0.0);
            vec2 dir = vec2(0.0);
            float m = 0.0;
            vec4 w = vec4(u_rift_time, u_rift_soft, u_rift_freq, u_rift_amp);
            vec2 tear = vec2(u_rift_tear, u_rift_tear_rate);
            sm_rift_spot(u_rift_spot0, u_rift_k.x, p, w, tear, disp, dir, m);
            sm_rift_spot(u_rift_spot1, u_rift_k.y, p, w, tear, disp, dir, m);
            sm_rift_spot(u_rift_spot2, u_rift_k.z, p, w, tear, disp, dir, m);
            sm_rift_spot(u_rift_spot3, u_rift_k.w, p, w, tear, disp, dir, m);
            if (m > 0.0005) {
                vec2 uv = (p + disp) / u_model_size;
                vec2 s = dir * u_rift_rgb / u_model_size;
                vec4 c = texture2D(tex0, uv);
                vec4 rift = vec4(texture2D(tex0, uv + s).r, c.g, texture2D(tex0, uv - s).b, c.a);
                gl_FragColor = mix(gl_FragColor, rift, clamp(m, 0.0, 1.0));
            }
        }
        """)

    def sm_rift_beacon_f(key, rect, follow, trans, st, at):
        spots = _fx_state.setdefault("rift_spots", {})
        spot = spots.setdefault(key, {"hover": False})
        spot["rect"] = rect
        spot["follow"] = follow
        spot["seen"] = _fx_frame_time()
        return 0.0

    def sm_rift_rect(pos, anchor, size):
        """Прямоугольник кнопки; float в pos — доля экрана, как у Ren'Py."""
        w, h = size
        x = pos[0] * config.screen_width if isinstance(pos[0], float) else pos[0]
        y = pos[1] * config.screen_height if isinstance(pos[1], float) else pos[1]
        return (x - anchor[0] * w, y - anchor[1] * h, w, h)

    def sm_rift_glow():
        """Овал свечения сценовой кнопки с живыми параметрами группы rift; цвет один для любого bg."""
        return Transform(Solid("#ffffff", xysize=GLOW_BASE_SIZE),
            mesh=True, shader="sm.oval_glow",
            u_glow_color=fx_cfg_rgba("rift.glow_color"),
            u_glow_soft=fx_cfg("rift.glow_soft"), u_glow_core=fx_cfg("rift.glow_core"))

    def _sm_rift_level(key, target, fade):
        """Линейно к target за fade секунд на полный размах 0..1; один шаг на кадр."""
        now = _fx_frame_time()
        state = _fx_state.get(("rift", key))
        if state is None:
            state = _fx_state[("rift", key)] = [0.0, now]
        level, last = state
        if now > last:
            step = (now - last) / fade if fade > 0.0 else 1.0
            level = min(target, level + step) if target > level else max(target, level - step)
            state[0], state[1] = level, now
        return level

    def sm_rift_hover(key, value):
        spot = _fx_state.setdefault("rift_spots", {}).get(key)
        if spot is not None:
            spot["hover"] = value

    def _sm_rift_to_screen(x, y, follow):
        ## Та же раскладка, что у follow_camera: зум и поворот вокруг центра экрана, затем сдвиг.
        zoom, rotate, xoffset, yoffset = follow
        cx, cy = config.screen_width / 2.0, config.screen_height / 2.0
        a = math.radians(rotate or 0.0)
        dx, dy = (x - cx) * zoom, (y - cy) * zoom
        return (cx + dx * math.cos(a) - dy * math.sin(a) + xoffset,
                cy + dx * math.sin(a) + dy * math.cos(a) + yoffset)

    def sm_rift_layer(trans):
        """Ставит uniforms разлома на слой; False — пятен нет."""
        spots = _fx_state.get("rift_spots")
        if not spots:
            return False
        now = _fx_frame_time()
        enabled = fx_cfg("rift.enabled")
        follow = _fx_state.get("ui_follow") or (1.0, 0.0, 0.0, 0.0)
        active = []
        for key, spot in list(spots.items()):
            alive = enabled and now - spot.get("seen", -1.0) < 0.05
            target = (fx_cfg("rift.hover") if spot["hover"] else fx_cfg("rift.idle")) if alive else 0.0
            k = _sm_rift_level(key, target, fx_cfg("rift.fade"))
            if not alive and k < 0.001:
                del spots[key]
                _fx_state.pop(("rift", key), None)
                continue
            if k < 0.001:
                continue
            x, y, w, h = spot["rect"]
            zoom = 1.0
            cx, cy = x + w / 2.0, y + h / 2.0
            if spot["follow"]:
                zoom = follow[0] or 1.0
                cx, cy = _sm_rift_to_screen(cx, cy, follow)
            scale = fx_cfg("rift.scale") * zoom / 2.0
            active.append(((cx, cy, w * scale, h * scale), k))
        if not active:
            return False
        active = active[:4] + [((0.0, 0.0, 1.0, 1.0), 0.0)] * (4 - min(len(active), 4))
        trans.u_rift_spot0, trans.u_rift_spot1, trans.u_rift_spot2, trans.u_rift_spot3 = [s for s, _ in active]
        trans.u_rift_k = tuple(k for _, k in active)
        trans.u_rift_time = 0.0 if sm_reduced_motion() else (now * fx_cfg("rift.speed")) % 600.0
        trans.u_rift_soft = fx_cfg("rift.soft")
        trans.u_rift_amp = fx_cfg("rift.amp")
        trans.u_rift_freq = fx_cfg("rift.freq")
        trans.u_rift_rgb = fx_cfg("rift.rgb")
        trans.u_rift_tear = fx_cfg("rift.tear")
        trans.u_rift_tear_rate = fx_cfg("rift.tear_rate")
        return True

## rect — (x, y, w, h) кнопки в координатах её контейнера; follow — контейнер едет за камерой.
## on hide: маяк замолкает вместе с уходом экрана, разлом гаснет за rift.fade, не дожидаясь
## конца анимации кнопки.
transform rift_beacon(key, rect, follow):
    on show, replace:
        function renpy.curry(sm_rift_beacon_f)(key, rect, follow)
    on hide:
        pass
