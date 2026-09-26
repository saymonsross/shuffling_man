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
