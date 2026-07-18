################################################################################
## Общие шейдеры и трансформы подсветки. Параметры сцен — аргументами на месте.
################################################################################

init python:
    ## sm.outline: обводка по альфа-каналу, сам объект не рисует — накладывать
    ## поверх уже показанного (hover-подсветка).
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
    ## sm.noise: телевизионное зерно на fullscreen-дисплеябле. Сила — u_strength
    ## (0.0 — невидимо), анимация — от встроенного u_time.
    renpy.register_shader("sm.noise",
        variables="""
        uniform float u_time;
        uniform float u_strength;
        attribute vec2 a_tex_coord;
        varying vec2 v_tex_coord;
        """,
        vertex_300="""
        v_tex_coord = a_tex_coord;
        """,
        fragment_300="""
        vec2 uv = v_tex_coord + fract(u_time * 61.7);
        float n = fract(sin(dot(uv, vec2(12.9898, 78.233))) * 43758.5453);
        float a = u_strength * n;
        gl_FragColor = vec4(vec3(n) * a, a);
        """)

## Контур по краю объекта. width — px, color — RGBA-кортеж 0.0–1.0.
transform outline_hover(width=5.0, color=(1.0, 0.97, 0.85, 1.0)):
    mesh True
    shader "sm.outline"
    u_line_width width
    u_line_color color

## Пульсация прозрачности; half — половина периода, сек.
transform hover_pulse(low=0.45, high=1.0, half=0.7):
    block:
        easein half alpha low
        easeout half alpha high
        repeat
