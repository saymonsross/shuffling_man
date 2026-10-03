init python:
    ## sm.outline рисует только альфа-контур поверх исходного объекта.
    renpy.register_shader("sm.outline",
        variables="""
        uniform sampler2D tex0;
        uniform vec2 u_model_size;
        uniform float u_line_width;
        uniform vec4 u_line_color;
        attribute vec2 a_tex_coord;
        varying vec2 v_tex_coord;
        """,
        vertex_300="""
        v_tex_coord = a_tex_coord;
        """,
        fragment_300="""
        vec4 c = texture2D(tex0, v_tex_coord);
        vec2 px = u_line_width / u_model_size;
        float m = 0.0;
        for (int i = 0; i < 16; i += 1) {
            float a = 6.2831853 * float(i) / 16.0;
            vec2 o = vec2(cos(a), sin(a));
            m = max(m, texture2D(tex0, v_tex_coord + o * px).a);
            m = max(m, texture2D(tex0, v_tex_coord + o * px * 0.5).a);
        }
        float edge = m * (1.0 - smoothstep(0.15, 0.4, c.a));
        gl_FragColor = u_line_color * edge;
        """)

init python:
    ## Кадр зерна задаёт u_random: u_time растёт до 86400 во float32 и по мере
    ## роста теряет точность — рисунок зерна со временем беднел бы.
    renpy.register_shader("sm.noise",
        variables="""
        uniform vec4 u_random;
        uniform float u_strength;
        uniform float u_noise_steps;
        attribute vec2 a_tex_coord;
        varying vec2 v_tex_coord;
        """,
        vertex_300="""
        v_tex_coord = a_tex_coord;
        """,
        fragment_300="""
        vec2 uv = v_tex_coord + u_random.xy;
        float n = fract(sin(dot(uv, vec2(12.9898, 78.233))) * 43758.5453);
        // Постеризация зерна до расчёта альфы: ступени видны и в цвете, и в прозрачности.
        if (u_noise_steps >= 2.0) {
            n = min(floor(n * u_noise_steps) / (u_noise_steps - 1.0), 1.0);
        }
        float a = u_strength * n;
        gl_FragColor = vec4(vec3(n) * a, a);
        """)

init python:
    ## sm.oval_glow требует Solid с mesh True; размер displayable задаёт овал.
    renpy.register_shader("sm.oval_glow",
        variables="""
        uniform vec4 u_glow_color;
        uniform float u_glow_soft;
        uniform float u_glow_core;
        attribute vec2 a_tex_coord;
        varying vec2 v_tex_coord;
        """,
        vertex_300="""
        v_tex_coord = a_tex_coord;
        """,
        fragment_300="""
        vec2 p = (v_tex_coord - 0.5) * 2.0;
        float d = length(p);
        float a = 1.0 - smoothstep(1.0 - u_glow_soft, 1.0, d);
        a = pow(a, u_glow_core);
        gl_FragColor = u_glow_color * a;
        """)

init python:
    ## Формула Unity floor(c*s)/(s-1) + clamp: при c == 1 она даёт s/(s-1).
    ## Текстуры premultiplied: квантуется чистый цвет, альфа сохраняется.
    ## gamma > 1 отдаёт больше ступеней теням; при gamma == 1 pow обходится:
    ## его exp2/log2 сдвигал бы границы ступеней относительно Unity.
    renpy.register_shader("sm.posterize",
        variables="""
        uniform float u_posterize_steps;
        uniform float u_posterize_mix;
        uniform float u_posterize_gamma;
        """,
        fragment_400="""
        {
            vec4 c = gl_FragColor;
            if (c.a > 0.0) {
                vec3 rgb = clamp(c.rgb / c.a, 0.0, 1.0);
                float s = max(u_posterize_steps, 2.0);
                float g = max(u_posterize_gamma, 0.01);
                bool exact = abs(g - 1.0) < 0.0001;
                vec3 base = exact ? rgb : pow(rgb, vec3(1.0 / g));
                vec3 q = min(floor(base * s) / (s - 1.0), 1.0);
                q = exact ? q : pow(q, vec3(g));
                gl_FragColor = vec4(mix(rgb, q, clamp(u_posterize_mix, 0.0, 1.0)) * c.a, c.a);
            }
        }
        """)

transform posterize(steps=5, mix=1.0, gamma=1.0):
    mesh True
    shader "sm.posterize"
    u_posterize_steps float(steps)
    u_posterize_mix float(mix)
    u_posterize_gamma float(gamma)

init python:
    ## Порт Pixelate.shader из nubick/unity-utils (MIT, © nubick):
    ## uv / cell → round → * cell. Ячейка задаётся в пикселях модели, а не в долях
    ## uv, чтобы на 16:9 она оставалась квадратной; round — floor(x + 0.5), его
    ## нет в GLSL ES 1.0. Приоритет 250: после renpy.texture и до постеризации.
    renpy.register_shader("sm.pixelate",
        variables="""
        uniform sampler2D tex0;
        uniform vec2 u_model_size;
        uniform float u_pixelate_size;
        attribute vec2 a_tex_coord;
        varying vec2 v_tex_coord;
        """,
        vertex_300="""
        v_tex_coord = a_tex_coord;
        """,
        fragment_250="""
        {
            vec2 cell = max(u_pixelate_size, 1.0) / u_model_size;
            vec2 stepped = floor(v_tex_coord / cell + 0.5) * cell;
            gl_FragColor = texture2D(tex0, stepped);
        }
        """)

init python:
    ## Тела фрагментов в { }: части шейдеров слоя склеиваются в один main(),
    ## одноимённые локальные переменные иначе конфликтуют.
    ## Базовая ретушь: яркость → контраст вокруг 0.5 → насыщенность (яркость по Rec.709).
    ## Считается по чистому цвету; приоритет 300 — после пикселизации, до постеризации.
    renpy.register_shader("sm.grade",
        variables="""
        uniform float u_grade_brightness;
        uniform float u_grade_contrast;
        uniform float u_grade_saturation;
        """,
        fragment_300="""
        {
            vec4 c = gl_FragColor;
            if (c.a > 0.0) {
                vec3 rgb = c.rgb / c.a + u_grade_brightness;
                rgb = (rgb - 0.5) * u_grade_contrast + 0.5;
                float lum = dot(rgb, vec3(0.2126, 0.7152, 0.0722));
                rgb = clamp(mix(vec3(lum), rgb, u_grade_saturation), 0.0, 1.0);
                gl_FragColor = vec4(rgb * c.a, c.a);
            }
        }
        """)

init python:
    ## Хроматическая аберрация по статье lettier «3D Game Shaders For Beginners»:
    ## три выборки кадра, каждая со своим смещением от центра экрана по радиусу.
    ## Альфа берётся вместе с синим, как в статье. u_chroma_cell > 1 — выборки
    ## снапятся к сетке пикселизации, иначе аберрация смазала бы её ячейки.
    renpy.register_shader("sm.chroma",
        variables="""
        uniform sampler2D tex0;
        uniform vec2 u_model_size;
        uniform vec3 u_chroma_offsets;
        uniform float u_chroma_cell;
        attribute vec2 a_tex_coord;
        varying vec2 v_tex_coord;
        """,
        vertex_300="""
        v_tex_coord = a_tex_coord;
        """,
        fragment_260="""
        {
            vec2 cell = max(u_chroma_cell, 1.0) / u_model_size;
            bool snap = u_chroma_cell > 1.0;
            vec2 base = snap ? floor(v_tex_coord / cell + 0.5) * cell : v_tex_coord;
            vec2 dir = base - vec2(0.5);
            vec2 ur = base + dir * u_chroma_offsets.r;
            vec2 ug = base + dir * u_chroma_offsets.g;
            vec2 ub = base + dir * u_chroma_offsets.b;
            if (snap) {
                ur = floor(ur / cell + 0.5) * cell;
                ug = floor(ug / cell + 0.5) * cell;
                ub = floor(ub / cell + 0.5) * cell;
            }
            gl_FragColor = vec4(texture2D(tex0, ur).r, texture2D(tex0, ug).g, texture2D(tex0, ub).ba);
        }
        """)

transform chroma(red=0.009, green=0.006, blue=-0.006):
    mesh True
    shader "sm.chroma"
    u_chroma_offsets (float(red), float(green), float(blue))
    u_chroma_cell 0.0

init python:
    ## Bloom — своя реализация: код Unity PostProcessing под Unity Companion License
    ## (только для Unity-проектов) переносить нельзя. Идея та же: яркое выше порога
    ## с мягким коленом → размытие → добавка к кадру. Вместо пирамиды проходов —
    ## один проход: 17 выборок по двум кольцам из mipmap-копии слоя (gl_mipmap).
    ## Приоритет 270: после пикселизации/аберрации, до ретуши и постеризации.
    renpy.register_shader("sm.bloom",
        variables="""
        uniform sampler2D tex0;
        uniform vec2 u_model_size;
        uniform float u_bloom_threshold;
        uniform float u_bloom_knee;
        uniform float u_bloom_intensity;
        uniform float u_bloom_radius;
        attribute vec2 a_tex_coord;
        varying vec2 v_tex_coord;
        """,
        fragment_functions="""
        vec3 sm_bloom_prefilter(vec3 c, float threshold, float knee) {
            float br = max(max(c.r, c.g), c.b);
            float k = max(knee, 0.0001);
            float soft = clamp(br - threshold + k, 0.0, 2.0 * k);
            soft = soft * soft / (4.0 * k);
            return c * max(soft, br - threshold) / max(br, 0.0001);
        }
        """,
        vertex_300="""
        v_tex_coord = a_tex_coord;
        """,
        fragment_270="""
        {
            vec2 px = 1.0 / u_model_size;
            float lod = max(log2(u_bloom_radius / 8.0), 0.0);
            vec3 acc = sm_bloom_prefilter(texture2D(tex0, v_tex_coord, lod).rgb, u_bloom_threshold, u_bloom_knee);
            float total = 1.0;
            for (int ring = 1; ring <= 2; ring += 1) {
                float r = u_bloom_radius * float(ring) * 0.5;
                float w = ring == 1 ? 0.8 : 0.45;
                for (int i = 0; i < 8; i += 1) {
                    float a = 6.2831853 * (float(i) + 0.5 * float(ring - 1)) / 8.0;
                    vec2 uv = v_tex_coord + vec2(cos(a), sin(a)) * r * px;
                    acc += sm_bloom_prefilter(texture2D(tex0, uv, lod).rgb, u_bloom_threshold, u_bloom_knee) * w;
                    total += w;
                }
            }
            gl_FragColor.rgb += acc / total * u_bloom_intensity;
        }
        """)

transform pixelate(size=8):
    mesh True
    shader "sm.pixelate"
    u_pixelate_size float(size)

## show … at снова наследует mesh/shader прошлого трансформа — снимать явно.
## Снимает любой шейдер трансформа: и posterize, и pixelate.
transform posterize_off:
    mesh False
    shader None

transform pixelate_off:
    mesh False
    shader None

transform outline_hover(width=5.0, color_=(1.0, 0.97, 0.85, 1.0)):
    mesh True
    shader "sm.outline"
    u_line_width width
    u_line_color color_

transform hover_pulse(low=0.45, high=1.0, half=0.7):
    block:
        easein half alpha low
        easeout half alpha high
        repeat

init python:
    ## Медленная смена яркости: 8 бит на канал дают шаг 1/255 сразу на весь кадр, на тёмных
    ## фонах он виден. Статичный дизеринг в полшага разносит переход по пикселям.
    ## Правит готовый gl_FragColor (после renpy.texture / renpy.blur на 200), а не читает
    ## tex0 заново — иначе blur того же трансформа терялся бы.
    renpy.register_shader("sm.breath",
        variables="""
        uniform float u_breath_brightness;
        """,
        fragment_300="""
        float d = fract(sin(dot(gl_FragCoord.xy, vec2(12.9898, 78.233))) * 43758.5453) - 0.5;
        gl_FragColor.rgb += (u_breath_brightness + d / 255.0) * gl_FragColor.a;
        """)

## Вода на отдельном слое (слеза, капля, струйка): волна бежит вниз по картинке и чуть
## качает её по горизонтали, вместе с ней скользит блик. Слой — обычная картинка с альфой;
## параметры общие, группа «Вода» в FX Tuner. При «меньше движения» вода стоит.
## water(flow=(y0, y1)) — струйка ещё и стекает, один раз за показ: участок слоя между y0
## и y1 (px картинки) проявляется сверху вниз за бегущей каплей, держится, потом тускнеет
## до water.fade_to и такой остаётся. Пока тускнеет, может вытянуться вниз на water.stretch px.
## Всё выше y0 и ниже конца струйки видно всегда. start — имя store-флага: пока он False,
## струйки нет; через delay секунд после того, как сцена его взвела, она начинает стекать.
## run, hold, fade, fade_to — свои тайминги стекания для этого места вместо общих water.*.
init -10 python:

    fx_param("water.amp", 1.5, 0.0, 8.0, step=0.1, doc="качание слоя по горизонтали, px")
    fx_param("water.wave", 90, 10, 400, doc="длина волны по вертикали, px")
    fx_param("water.speed", 40, 0, 300, doc="скорость стекания волны вниз, px/с")
    fx_param("water.glint", 0.3, 0.0, 3.0, step=0.05, doc="яркость бегущего блика: 0 — без блика")
    fx_param("water.run", 5.0, 0.5, 30.0, step=0.5, doc="за сколько секунд капля стекает по струйке")
    fx_param("water.hold", 3.0, 0.0, 30.0, step=0.5, doc="сколько секунд струйка держится целиком")
    fx_param("water.fade", 1.5, 0.1, 10.0, step=0.1, doc="за сколько секунд струйка тускнеет")
    fx_param("water.fade_to", 0.5, 0.0, 1.0, step=0.05, doc="какой остаётся струйка после стекания: 1 — как была, 0 — исчезает")
    fx_param("water.bead", 0.75, 0.0, 5.0, step=0.1, doc="яркость капли на конце струйки")
    fx_param("water.stretch", 0, 0, 200, doc="на сколько px струйка вытягивается вниз, пока тускнеет")
    fx_group("water", "Вода")

    renpy.register_shader("sm.water",
        variables="""
        uniform sampler2D tex0;
        uniform vec2 u_model_size;
        uniform float u_water_t;
        uniform float u_water_amp;
        uniform float u_water_wave;
        uniform float u_water_speed;
        uniform float u_water_glint;
        uniform vec2 u_water_span;
        uniform float u_water_front;
        uniform float u_water_fade;
        uniform float u_water_bead;
        uniform float u_water_stretch;
        attribute vec2 a_tex_coord;
        varying vec2 v_tex_coord;
        """,
        vertex_300="""
        v_tex_coord = a_tex_coord;
        """,
        fragment_250="""
        {
            vec2 px = v_tex_coord * u_model_size;
            float flow = px.y - u_water_t * u_water_speed;
            float k = 6.2831853 / max(u_water_wave, 1.0);
            float w = sin(flow * k) * 0.65 + sin(flow * k * 2.3 + px.x * 0.05) * 0.35;
            vec2 uv = v_tex_coord + vec2(w * u_water_amp / u_model_size.x, 0.0);
            bool flowing = u_water_span.y > u_water_span.x;
            float end = u_water_span.y + u_water_stretch;
            float inside = flowing ? step(u_water_span.x, px.y) * step(px.y, end) : 0.0;
            if (inside > 0.5) {
                // Участок растянут до end: выборка — из исходной, нерастянутой струйки.
                float src = u_water_span.x + (px.y - u_water_span.x) * (u_water_span.y - u_water_span.x) / (end - u_water_span.x);
                uv.y = src / u_model_size.y;
            }
            vec4 c = texture2D(tex0, uv);
            float glint = pow(max(0.0, sin(flow * k * 0.5)), 8.0);
            c.rgb = min(c.rgb * (1.0 + glint * u_water_glint), vec3(1.0));
            if (flowing) {
                float shown = 1.0 - smoothstep(u_water_front - 10.0, u_water_front, px.y);
                float d = (px.y - (u_water_front - 8.0)) / 9.0;
                float bead = exp(-d * d) * u_water_bead;
                c.rgb = min(c.rgb * (1.0 + bead * inside), vec3(1.0));
                c *= mix(1.0, shown * u_water_fade, inside);
            }
            gl_FragColor = c;
        }
        """)

    def fx_flag_time(owner, flag):
        """Секунды с момента, когда store-флаг flag впервые увиден взведённым; None — флаг
        снят. Отсчёт — по часам кадра: st эффекта не годится, кадр показан раньше.
        Флаг-счётчик перезапускает отсчёт каждым новым значением ($ flag += 1)."""
        if renpy.predicting():
            return None
        value = getattr(store, flag, False)
        if not value:
            _fx_state.pop((owner, flag), None)
            return None
        now = _fx_frame_time()
        seen = _fx_state.get((owner, flag))
        if seen is None or seen[0] != value:
            seen = _fx_state[(owner, flag)] = (value, now)
        return now - seen[1]

    def water_f(flow, start, delay, own, trans, st, at):
        import math
        trans.u_water_amp = float(fx_cfg("water.amp")) * sm_motion_scale()
        trans.u_water_wave = float(fx_cfg("water.wave"))
        trans.u_water_speed = float(fx_cfg("water.speed"))
        trans.u_water_glint = float(fx_cfg("water.glint")) * sm_motion_scale()
        ## Фаза — от времени показа: копить её между пересборками не нужно.
        trans.u_water_t = 0.0 if sm_reduced_motion() else st % 3600.0
        y0, y1 = flow or (0.0, 0.0)
        trans.u_water_span = (float(y0), float(y1))
        run, hold, fade, fade_to = [fx_cfg("water." + name) if value is None else value
            for name, value in zip(("run", "hold", "fade", "fade_to"), own)]
        if start is None:
            t = st
        else:
            since = fx_flag_time("water", start)
            t = -1.0 if since is None else since - delay
        gone = t - run - hold
        k = 0.0 if sm_reduced_motion() or gone <= 0.0 else min(1.0, gone / max(fade, 0.001))
        trans.u_water_stretch = float(fx_cfg("water.stretch")) * (1.0 - (1.0 - k) * (1.0 - k))
        if sm_reduced_motion() or t >= run:
            ## Запас: кромка проявления уходит за нижний край участка.
            trans.u_water_front = float(y1) + trans.u_water_stretch + 20.0
            trans.u_water_bead = 0.0
        else:
            ## Капля идёт неровно: замирает и срывается, но всегда вниз.
            p = max(0.0, t) / run
            p += 0.04 * math.sin(p * 6.2831853 * 3.0)
            trans.u_water_front = y0 + (y1 - y0 + 20.0) * p
            trans.u_water_bead = float(fx_cfg("water.bead")) if t >= 0.0 else 0.0
            trans.u_water_stretch = 0.0
        trans.u_water_fade = 1.0 - k * (1.0 - float(fade_to))
        return 1.0 / 30.0

transform water(flow=None, start=None, delay=0.0, run=None, hold=None, fade=None, fade_to=None):
    mesh True
    shader "sm.water"
    function renpy.curry(water_f)(flow, start, delay, (run, hold, fade, fade_to))

## Говорящий рот «пластикой»: нарисованный открытый рот сжимается по вертикали к своей
## середине и разжимается обратно в ритме речи. Сжатие — только внутри эллипса вокруг рта
## (center и radius в px картинки): край эллипса неподвижен, нос и подбородок не тянутся.
## time — сколько секунд говорить; None — без ограничения. start — имя store-флага:
## рот двигается с момента, когда сцена его взвела (без start — с момента показа);
## флаг-счётчик ($ flag += 1) запускает рот заново на каждой реплике. who — ключ
## talk_callback персонажа: рот двигается на каждой его реплике сам, time и start не нужны.
## rate — множитель темпа mouth.rate, когда рот идёт не по репликам (без who).
## strength — множитель силы; отрицательный — для закрытого рта: губы не сжимаются,
## а нижняя чуть отходит вниз.
## При «меньше движения» рот стоит, как нарисован.
init -10 python:

    fx_param("mouth.close", 0.16, 0.0, 1.0, step=0.01, doc="насколько рот закрывается между слогами: 0 — не двигается")
    fx_param("mouth.rate", 5.5, 0.5, 15.0, step=0.5, doc="слогов в секунду, когда рот идёт по флагу, а не по реплике")
    fx_param("mouth.per_move", 1, 1, 3, doc="слогов реплики на одно движение рта")
    fx_param("mouth.open_share", 0.6, 0.2, 0.9, step=0.05, doc="какую долю слога рот открыт")
    fx_param("mouth.chars", 16, 4, 60, doc="скорость речи, знаков в секунду: по длине реплики считается, сколько двигается рот")
    fx_group("mouth", "Говорящий рот")

    renpy.register_shader("sm.mouth",
        variables="""
        uniform sampler2D tex0;
        uniform vec2 u_model_size;
        uniform vec2 u_mouth_center;
        uniform vec2 u_mouth_radius;
        uniform float u_mouth_close;
        uniform float u_mouth_shade;
        attribute vec2 a_tex_coord;
        varying vec2 v_tex_coord;
        """,
        vertex_300="""
        v_tex_coord = a_tex_coord;
        """,
        fragment_250="""
        {
            vec2 px = v_tex_coord * u_model_size;
            vec2 uv = v_tex_coord;
            float qx = (px.x - u_mouth_center.x) / u_mouth_radius.x;
            float shade = 0.0;
            if (u_mouth_close != 0.0 && abs(qx) < 1.0) {
                // Полувысота эллипса на этой вертикали; внутри неё высота рта сжимается
                // степенной кривой, концы отрезка остаются на месте.
                float half_h = u_mouth_radius.y * sqrt(1.0 - qx * qx);
                float dy = px.y - u_mouth_center.y;
                // Отрицательная сила приоткрывает закрытый рот: растягивается только
                // нижняя половина, от линии губ вниз.
                if (half_h > 0.5 && abs(dy) < half_h && (u_mouth_close > 0.0 || dy > 0.0)) {
                    float t = pow(abs(dy) / half_h, 1.0 / (1.0 + 2.0 * u_mouth_close));
                    uv.y = (u_mouth_center.y + sign(dy) * half_h * t) / u_model_size.y;
                    // Тень в раскрытом рту: гуще у линии губ, к краям эллипса сходит на нет.
                    if (dy > 0.0) {
                        shade = u_mouth_shade * (1.0 - dy / half_h) * (1.0 - qx * qx);
                    }
                }
            }
            gl_FragColor = texture2D(tex0, uv);
            gl_FragColor.rgb *= 1.0 - shade;
        }
        """)

    def mouth_talk_f(time, start, strength, who, rate, trans, st, at):
        import math
        if who is not None:
            ## По слогам реплики: нарисованный закрытым (strength < 0) рот раскрывается на
            ## слоге, нарисованный открытым смыкается между слогами.
            opened = None if sm_reduced_motion() else talk_open(who)
            amount = 0.0 if opened is None else (opened if strength < 0 else 1.0 - opened)
            trans.u_mouth_close = float(fx_cfg("mouth.close")) * strength * amount
            return 1.0 / 60.0 if opened is not None else 1.0 / 20.0
        t = st if start is None else fx_flag_time("mouth", start)
        if sm_reduced_motion() or t is None or (time is not None and t >= time):
            trans.u_mouth_close = 0.0
            return 1.0 / 20.0
        beat = t * float(fx_cfg("mouth.rate")) * rate * 6.2831853
        ## Слоги неровные: вторая синусоида меняет силу соседних смыканий.
        wave = (0.5 - 0.5 * math.cos(beat)) * (0.65 + 0.35 * math.sin(beat * 0.37 + 1.3))
        trans.u_mouth_close = float(fx_cfg("mouth.close")) * strength * max(0.0, wave)
        return 1.0 / 60.0

transform mouth_talk(center, radius, time=None, start=None, strength=1.0, who=None, rate=1.0):
    mesh True
    shader "sm.mouth"
    u_mouth_center (float(center[0]), float(center[1]))
    u_mouth_radius (float(radius[0]), float(radius[1]))
    u_mouth_close 0.0
    u_mouth_shade 0.0
    function renpy.curry(mouth_talk_f)(time, start, strength, who, rate)

init -10 python:

    def mouth_loop_f(strength, period, hold, ease, dark, trans, st, at):
        if sm_reduced_motion():
            trans.u_mouth_close = 0.0
            trans.u_mouth_shade = 0.0
            return 1.0 / 20.0
        ph = st % period
        if ph < ease:
            k = ph / ease
        elif ph < ease + hold:
            k = 1.0
        elif ph < 2.0 * ease + hold:
            k = 1.0 - (ph - ease - hold) / ease
        else:
            k = 0.0
        opened = k * k * (3.0 - 2.0 * k)
        trans.u_mouth_close = float(fx_cfg("mouth.close")) * strength * opened
        trans.u_mouth_shade = dark * opened
        return 0

## Рот по кругу тем же шейдером: плавно приоткрывается за ease секунд, держится hold
## секунд, плавно смыкается и стоит до конца period; раскрытый рот темнеет на долю dark.
## При «меньше движения» рот стоит.
transform mouth_loop(center, radius, strength=-2.0, period=4.0, hold=2.0, ease=0.6, dark=0.0):
    mesh True
    shader "sm.mouth"
    u_mouth_center (float(center[0]), float(center[1]))
    u_mouth_radius (float(radius[0]), float(radius[1]))
    u_mouth_close 0.0
    u_mouth_shade 0.0
    function renpy.curry(mouth_loop_f)(strength, period, hold, ease, dark)

## Ветер в волосах (или ткани) на картинке: внутри эллипса center/radius (px картинки)
## пиксели колышутся бегущими волнами на amp px. У anchor (корень — макушка) смещения нет,
## к краю эллипса оно сходит на нет: лицо и всё вне эллипса стоят. speed — темп волн.
## При «меньше движения» стоит.
init -10 python:

    renpy.register_shader("sm.wind",
        variables="""
        uniform sampler2D tex0;
        uniform vec2 u_model_size;
        uniform vec2 u_wind_center;
        uniform vec2 u_wind_radius;
        uniform vec2 u_wind_anchor;
        uniform float u_wind_amp;
        uniform float u_wind_time;
        attribute vec2 a_tex_coord;
        varying vec2 v_tex_coord;
        """,
        vertex_300="""
        v_tex_coord = a_tex_coord;
        """,
        fragment_250="""
        {
            vec2 px = v_tex_coord * u_model_size;
            vec2 q = (px - u_wind_center) / u_wind_radius;
            float inside = 1.0 - smoothstep(0.55, 1.0, length(q));
            float reach = smoothstep(0.0, 1.0, length(px - u_wind_anchor) / max(u_wind_radius.x, u_wind_radius.y));
            float t = u_wind_time;
            vec2 wave = vec2(sin(px.y * 0.09 - t * 2.3) + 0.5 * sin(px.x * 0.05 - t * 1.4),
                0.6 * cos(px.x * 0.08 - t * 1.9));
            gl_FragColor = texture2D(tex0, (px + wave * u_wind_amp * inside * reach) / u_model_size);
        }
        """)

    def wind_warp_f(speed, amp, trans, st, at):
        trans.u_wind_time = (_fx_frame_time() * speed) % 1000.0
        trans.u_wind_amp = amp * sm_motion_scale()
        return 0

transform wind_warp(center, radius, anchor, amp=2.5, speed=1.0):
    mesh True
    shader "sm.wind"
    u_wind_center (float(center[0]), float(center[1]))
    u_wind_radius (float(radius[0]), float(radius[1]))
    u_wind_anchor (float(anchor[0]), float(anchor[1]))
    u_wind_amp 0.0
    u_wind_time 0.0
    function renpy.curry(wind_warp_f)(speed, amp)

## Пар над чашкой: в столбе над поверхностью напитка картинка плывёт бегущей вверх рябью
## на amp px, по ней ползут едва заметные светлые клубы силой glow. plumes — до двух
## столбов (x, y, полуширина у основания, высота) в px картинки: основание — поверхность
## напитка, к вершине столб расширяется в полтора раза и тает. speed — темп подъёма.
## При «меньше движения» рябь стоит.
init -10 python:

    renpy.register_shader("sm.steam",
        variables="""
        uniform sampler2D tex0;
        uniform vec2 u_model_size;
        uniform vec4 u_steam_a;
        uniform vec4 u_steam_b;
        uniform float u_steam_amp;
        uniform float u_steam_glow;
        uniform float u_steam_time;
        attribute vec2 a_tex_coord;
        varying vec2 v_tex_coord;
        """,
        fragment_functions="""
        float sm_steam_hash(vec2 p) {
            return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453);
        }
        float sm_steam_noise(vec2 p) {
            vec2 i = floor(p);
            vec2 f = fract(p);
            vec2 u = f * f * (3.0 - 2.0 * f);
            return mix(mix(sm_steam_hash(i), sm_steam_hash(i + vec2(1.0, 0.0)), u.x),
                mix(sm_steam_hash(i + vec2(0.0, 1.0)), sm_steam_hash(i + vec2(1.0, 1.0)), u.x), u.y);
        }
        // plume: x, y - base, z - half width at the base, w - column height.
        void sm_steam_plume(vec4 plume, vec2 px, float t, inout vec2 disp, inout float wisp) {
            float up = (plume.y - px.y) / plume.w;
            if (up < -0.15 || up > 1.0) return;
            float half_w = plume.z * (1.0 + 0.6 * max(up, 0.0));
            float lateral = (px.x - plume.x) / half_w;
            float f = (1.0 - smoothstep(0.5, 1.0, abs(lateral)))
                * smoothstep(-0.15, 0.1, up) * (1.0 - smoothstep(0.4, 1.0, up));
            if (f <= 0.0) return;
            vec2 q = px * 0.012 + vec2(0.0, t * 0.9);
            float n1 = sm_steam_noise(q);
            float n2 = sm_steam_noise(q * 1.9 + vec2(7.3, t * 0.4));
            disp += vec2(n1 - 0.5, (n2 - 0.5) * 0.5) * f;
            wisp += max(0.0, n1 * 0.6 + n2 * 0.4 - 0.55) * f;
        }
        """,
        vertex_300="""
        v_tex_coord = a_tex_coord;
        """,
        fragment_250="""
        {
            vec2 px = v_tex_coord * u_model_size;
            vec2 disp = vec2(0.0);
            float wisp = 0.0;
            sm_steam_plume(u_steam_a, px, u_steam_time, disp, wisp);
            sm_steam_plume(u_steam_b, px, u_steam_time, disp, wisp);
            vec4 c = texture2D(tex0, (px + disp * u_steam_amp) / u_model_size);
            gl_FragColor = c + vec4(vec3(1.0, 0.98, 0.94) * (wisp * u_steam_glow * c.a), 0.0);
        }
        """)

    def steam_f(speed, amp, glow, trans, st, at):
        trans.u_steam_time = (_fx_frame_time() * speed) % 1000.0
        trans.u_steam_amp = amp * sm_motion_scale()
        trans.u_steam_glow = glow
        return 0

    def _steam_plume(plumes, index):
        if index < len(plumes):
            return tuple(float(v) for v in plumes[index])
        return (0.0, -1.0e6, 1.0, 1.0)

transform steam(plumes, amp=3.0, glow=0.35, speed=1.0):
    mesh True
    shader "sm.steam"
    u_steam_a _steam_plume(plumes, 0)
    u_steam_b _steam_plume(plumes, 1)
    u_steam_amp 0.0
    u_steam_glow 0.0
    u_steam_time 0.0
    function renpy.curry(steam_f)(speed, amp, glow)

## «Дыхание» яркости lo → hi → lo, по t секунд в каждую сторону.
transform breath_brightness(lo=-0.01, hi=-0.04, t=6.0):
    mesh True
    shader "sm.breath"
    u_breath_brightness float(lo)
    block:
        ease t u_breath_brightness float(hi)
        ease t u_breath_brightness float(lo)
        repeat

init -10 python:

    def _breath_clock_f(lo, hi, t, trans, st, at):
        import math
        x = (_fx_frame_time() / t) % 2.0
        x = x if x < 1.0 else 2.0 - x
        trans.u_breath_brightness = lo + (hi - lo) * (0.5 - 0.5 * math.cos(math.pi * x))
        return 0

## То же дыхание, но фаза идёт от часов кадра, а не от показа: экран, который пересоздаётся
## на каждом действии (повторный show screen), дышит без скачков.
transform breath_brightness_clock(lo=-0.01, hi=-0.04, t=6.0):
    mesh True
    shader "sm.breath"
    function renpy.curry(_breath_clock_f)(lo, hi, t)

## Яркость в один конец: → end за t секунд, дальше держится. Старт — текущая яркость
## картинки (например, с breath_brightness в момент смены ATL): uniform наследуется.
transform brightness_to(end=-0.04, t=6.0):
    mesh True
    shader "sm.breath"
    ease t u_breath_brightness float(end)

## То же с явным стартом start.
transform fade_brightness(start=0.0, end=-0.04, t=6.0):
    mesh True
    shader "sm.breath"
    u_breath_brightness float(start)
    ease t u_breath_brightness float(end)
