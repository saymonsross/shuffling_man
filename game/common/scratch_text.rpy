## «Процарапанный» штрих текста и картинок: дрожание контура по шуму, волокна-разрывы
## и до трёх нервных обводок. Каждое место применения — своя группа параметров
## (scratch_params), тюнер группы открывается из Dev Hub. Координаты шейдера — пиксели
## текстуры до zoom.

init -11 python:

    def scratch_params(group, title, amp, fiber_cut, spread, copy_alpha):
        fx_param(group + ".enabled", True, doc="включить процарапанный штрих")
        fx_param(group + ".mix", 1.0, 0.0, 1.0, step=0.01, doc="сила штриха: 0 — исходник, 1 — полный")
        fx_param(group + ".amp", amp, 0.0, 10.0, step=0.1, doc="дрожание контура, px; при наведении +50%")
        fx_param(group + ".jitter_x", 0.02, 0.0, 2.0, step=0.005, doc="частота шума дрожания по X, 1/px")
        fx_param(group + ".jitter_y", 0.6, 0.0, 2.0, step=0.005, doc="частота шума дрожания по Y, 1/px")
        fx_param(group + ".fiber_x", 1.0, 0.0, 2.0, step=0.005, doc="частота шума волокон по X, 1/px")
        fx_param(group + ".fiber_y", 0.05, 0.0, 2.0, step=0.005, doc="частота шума волокон по Y, 1/px")
        fx_param(group + ".fiber_cut", fiber_cut, 0.0, 1.0, step=0.01, doc="порог волокон: выше — больше разрывов")
        fx_param(group + ".copies", 3, 1, 3, doc="обводок: основная + копии")
        fx_param(group + ".spread", spread, 0.0, 5.0, step=0.1, doc="множитель смещения копий")
        fx_param(group + ".copy_alpha", copy_alpha, 0.0, 1.0, step=0.01, doc="альфа копий")
        fx_param(group + ".animate", True, doc="перерисовывать штрих ступеньками")
        fx_param(group + ".step", 0.15, 0.05, 0.5, step=0.01, doc="шаг перерисовки, с")
        fx_group(group, title)

    ## u_scratch_tint: 1 — штрих заливается цветом idle/hover, 0 — остаётся цвет исходника
    ## (обводка текста, фактура картинки).
    renpy.register_shader("sm.scratch",
        variables="""
        uniform sampler2D tex0;
        uniform vec2 u_model_size;
        uniform float u_scratch_on;
        uniform float u_scratch_amp;
        uniform vec2 u_scratch_jitter_freq;
        uniform vec2 u_scratch_fiber_freq;
        uniform float u_scratch_fiber_cut;
        uniform float u_scratch_copies;
        uniform float u_scratch_spread;
        uniform float u_scratch_copy_alpha;
        uniform float u_scratch_seed;
        uniform float u_scratch_hover;
        uniform float u_scratch_tint;
        uniform float u_scratch_mix;
        uniform float u_scratch_group_mix;
        uniform vec4 u_scratch_idle_color;
        uniform vec4 u_scratch_hover_color;
        attribute vec2 a_tex_coord;
        varying vec2 v_tex_coord;
        """,
        fragment_functions="""
        float sm_scr_hash(vec2 p) {
            return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453);
        }

        float sm_scr_noise(vec2 p) {
            vec2 i = floor(p);
            vec2 f = fract(p);
            vec2 u = f * f * (3.0 - 2.0 * f);
            return mix(mix(sm_scr_hash(i), sm_scr_hash(i + vec2(1.0, 0.0)), u.x),
                mix(sm_scr_hash(i + vec2(0.0, 1.0)), sm_scr_hash(i + vec2(1.0, 1.0)), u.x), u.y);
        }

        // Одна обводка (premultiplied): копия сдвинута на offset и повёрнута на angle вокруг центра.
        vec4 sm_scr_layer(sampler2D tex, vec2 size, vec2 p, vec2 offset, float angle, float seed,
                float amp, vec2 jitter_freq, vec2 fiber_freq, float fiber_cut) {
            vec2 c = size * 0.5;
            vec2 q = p - offset - c;
            float s = sin(angle);
            float co = cos(angle);
            q = vec2(co * q.x + s * q.y, co * q.y - s * q.x) + c;
            vec2 jp = q * jitter_freq + seed * 17.0;
            q += (vec2(sm_scr_noise(jp), sm_scr_noise(jp + 41.3)) * 2.0 - 1.0) * amp;
            float fiber = sm_scr_noise(q * fiber_freq + seed * 29.0 + 7.1);
            return texture2D(tex, q / size) * smoothstep(fiber_cut - 0.04, fiber_cut + 0.04, fiber);
        }
        """,
        vertex_300="""
        v_tex_coord = a_tex_coord;
        """,
        fragment_300="""
        vec4 src;
        vec4 plain = texture2D(tex0, v_tex_coord);
        if (u_scratch_on < 0.5) {
            src = plain;
        } else {
            vec2 p = v_tex_coord * u_model_size;
            float amp = u_scratch_amp * (1.0 + 0.5 * u_scratch_hover);
            src = sm_scr_layer(tex0, u_model_size, p, vec2(0.0), 0.0, u_scratch_seed,
                amp, u_scratch_jitter_freq, u_scratch_fiber_freq, u_scratch_fiber_cut);
            // Основная обводка поверх копий.
            if (u_scratch_copies >= 2.0) {
                src += (1.0 - src.a) * u_scratch_copy_alpha * sm_scr_layer(tex0, u_model_size, p,
                    vec2(1.5, -1.0) * u_scratch_spread, radians(-1.5), u_scratch_seed + 11.0,
                    amp, u_scratch_jitter_freq, u_scratch_fiber_freq, u_scratch_fiber_cut);
            }
            if (u_scratch_copies >= 3.0) {
                src += (1.0 - src.a) * u_scratch_copy_alpha * sm_scr_layer(tex0, u_model_size, p,
                    vec2(-1.0, 1.5) * u_scratch_spread, radians(1.0), u_scratch_seed + 23.0,
                    amp, u_scratch_jitter_freq, u_scratch_fiber_freq, u_scratch_fiber_cut);
            }
            // mix < 1 — штрих слабее: смесь с исходником.
            src = mix(plain, src, u_scratch_mix * u_scratch_group_mix);
        }
        vec4 col = mix(u_scratch_idle_color, u_scratch_hover_color, u_scratch_hover);
        gl_FragColor = mix(src, vec4(col.rgb, 1.0) * col.a * src.a, u_scratch_tint);
        """)

    ## mix_f — функция без аргументов, множитель силы штриха в рантайме (например, курсор гасит штрих).
    def scratch_f(group, mix_f, trans, st, at):
        trans.u_scratch_on = 1.0 if fx_cfg(group + ".enabled") and not fx_cfg_bypassed() else 0.0
        trans.u_scratch_group_mix = float(fx_cfg(group + ".mix")) * (mix_f() if mix_f else 1.0)
        trans.u_scratch_amp = float(fx_cfg(group + ".amp"))
        trans.u_scratch_jitter_freq = (float(fx_cfg(group + ".jitter_x")), float(fx_cfg(group + ".jitter_y")))
        trans.u_scratch_fiber_freq = (float(fx_cfg(group + ".fiber_x")), float(fx_cfg(group + ".fiber_y")))
        trans.u_scratch_fiber_cut = float(fx_cfg(group + ".fiber_cut"))
        trans.u_scratch_copies = float(fx_cfg(group + ".copies"))
        trans.u_scratch_spread = float(fx_cfg(group + ".spread"))
        trans.u_scratch_copy_alpha = float(fx_cfg(group + ".copy_alpha"))
        ## Seed меняется ступенькой, как в покадровой анимации; без анимации штрих застывает.
        step = fx_cfg(group + ".step")
        if fx_cfg(group + ".animate") and not sm_reduced_motion():
            trans.u_scratch_seed = float(int(st / step))
            return step - (st % step)
        trans.u_scratch_seed = 0.0
        ## Редкая перерисовка подхватывает правки тюнера.
        return 0.1

## Текст, показанный в сценах через show (титры и т. п.): своя группа, тюнер — Text Tuner.
init -10 python:
    scratch_params("show_text", "Текст на экране (show text)", 2.0, 0.3, 1.0, 0.55)

## group — группа параметров scratch_params. Цвета — аргументы: у FX Tuner нет цветовых
## параметров. pad — запас под дрожание и копии, иначе штрих обрезается по краю текстуры.
## Внутри кнопки трансформ получает hover/idle: дрожание +50%, цвет idle → hover при tint 1.
## mix — сила штриха у этого места (1 — полный, 0 — исходник); умножается на mix группы из тюнера.
transform scratch(group, tint=1.0, idle_color="#8A8784", hover_color="#F2EFE9", pad=16, mix=1.0, mix_f=None):
    mesh True
    mesh_pad (pad, pad, pad, pad)
    shader "sm.scratch"
    u_scratch_tint float(tint)
    u_scratch_mix float(mix)
    u_scratch_group_mix 1.0
    u_scratch_idle_color Color(idle_color).rgba
    u_scratch_hover_color Color(hover_color).rgba
    u_scratch_hover 0.0
    parallel:
        function renpy.curry(scratch_f)(group, mix_f)
    parallel:
        on idle, selected_idle, insensitive:
            linear 0.12 u_scratch_hover 0.0
        on hover, selected_hover:
            linear 0.12 u_scratch_hover 1.0
