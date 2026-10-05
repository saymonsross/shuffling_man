init python:
    def sm_crt_projection(corners, size):
        ## Обратная гомография: локальные координаты стекла → UV изображения.
        (x0, y0), (x1, y1), (x2, y2), (x3, y3) = [
            (x / float(size[0]), y / float(size[1])) for x, y in corners]
        dx1, dx2 = x1 - x2, x3 - x2
        dy1, dy2 = y1 - y2, y3 - y2
        sx, sy = x0 - x1 + x2 - x3, y0 - y1 + y2 - y3
        divisor = dx1 * dy2 - dx2 * dy1
        if abs(divisor) < 1e-9:
            raise ValueError("Degenerate CRT screen corners")
        g = (sx * dy2 - dx2 * sy) / divisor
        h = (dx1 * sy - sx * dy1) / divisor
        a, b, c = x1 - x0 + g * x1, x3 - x0 + h * x3, x0
        d, e, f = y1 - y0 + g * y1, y3 - y0 + h * y3, y0
        determinant = a * (e - f * h) - b * (d - f * g) + c * (d * h - e * g)
        if abs(determinant) < 1e-9:
            raise ValueError("Degenerate CRT screen projection")
        return tuple(tuple(value / determinant for value in row) for row in (
            (e - f * h, c * h - b, b * f - c * e),
            (f * g - d, a - c * g, c * d - a * f),
            (d * h - e * g, b * g - a * h, a * e - b * d)))

    renpy.register_shader("sm.crt_glass",
        variables="""
        uniform sampler2D tex0;
        uniform vec2 u_model_size;
        uniform vec3 u_crt_row0;
        uniform vec3 u_crt_row1;
        uniform vec3 u_crt_row2;
        uniform float u_crt_curvature;
        uniform float u_crt_corner_radius;
        uniform float u_crt_vignette;
        uniform float u_crt_turn;
        uniform float u_crt_tall;
        attribute vec4 a_position;
        varying vec2 v_crt_position;
        """,
        vertex_300="""
        v_crt_position = a_position.xy / u_model_size;
        """,
        fragment_300="""
        vec3 dest = vec3(v_crt_position, 1.0);
        float denominator = dot(u_crt_row2, dest);
        vec2 uv = vec2(dot(u_crt_row0, dest), dot(u_crt_row1, dest)) / denominator;
        vec2 edge_px = min(uv, 1.0 - uv) * u_model_size;
        float coverage = smoothstep(0.0, 1.25, min(edge_px.x, edge_px.y));

        vec2 p = uv * 2.0 - 1.0;
        vec2 bowed = p * (1.0 + 0.3 * u_crt_curvature * p.yx * p.yx);
        vec2 radius = vec2(u_crt_corner_radius);
        vec2 corner = abs(bowed * u_model_size * 0.5) - (u_model_size * 0.5 - radius - 1.5);
        float distance_to_glass = length(max(corner, 0.0)) + min(max(corner.x, corner.y), 0.0) - u_crt_corner_radius;
        float aperture = 1.0 - smoothstep(-0.8, 1.0, distance_to_glass);

        // Overscan supplies pixels beyond the warped rim; no clamped stripe.
        vec2 warped = p * (1.0 + u_crt_curvature * dot(p, p));
        vec2 sample_uv = 0.5 + 0.5 * warped / (1.0 + 2.0 * u_crt_curvature);
        // Content turns with the set: compressed toward the far (right) side, near side taller.
        sample_uv.x /= 1.0 + u_crt_turn * (1.0 - sample_uv.x);
        sample_uv.y = 0.5 + (sample_uv.y - 0.5) * (1.0 - u_crt_tall * (1.0 - sample_uv.x));
        vec4 pixel = texture2D(tex0, sample_uv);
        float falloff = 1.0 - u_crt_vignette * smoothstep(0.15, 1.75, dot(p, p));
        float rim = 1.0 - 0.48 * exp(-max(-distance_to_glass, 0.0) / 10.0);
        float reflection = exp(-dot((p - vec2(-0.32, -0.48)) * vec2(1.15, 2.4),
                                     (p - vec2(-0.32, -0.48)) * vec2(1.15, 2.4))) * 0.035;
        vec3 glass = pixel.rgb * falloff * rim + vec3(1.0, 0.94, 0.80) * reflection;
        // Opaque backing covers the baked white placeholder even at rounded corners.
        vec3 color = mix(vec3(0.022, 0.024, 0.023), glass, aperture);
        gl_FragColor = vec4(color * coverage, coverage);
        """)

transform sm_crt_glass(projection, curvature=0.16, corner_radius=26.0, vignette=0.28, turn=(0.0, 0.0)):
    mesh True
    shader "sm.crt_glass"
    u_crt_row0 projection[0]
    u_crt_row1 projection[1]
    u_crt_row2 projection[2]
    u_crt_curvature curvature
    u_crt_corner_radius corner_radius
    u_crt_vignette vignette
    u_crt_turn turn[0]
    u_crt_tall turn[1]

## Сигнал на экране телевизора: строки развёртки, медленная бегущая полоса и лёгкое
## мерцание. Время — по часам кадра; при «меньше движения» полоса и мерцание стоят.
init python:
    renpy.register_shader("sm.tv_signal",
        variables="""
        uniform sampler2D tex0;
        uniform vec2 u_model_size;
        uniform float u_tv_time;
        uniform float u_tv_motion;
        attribute vec2 a_tex_coord;
        varying vec2 v_tex_coord;
        """,
        vertex_300="""
        v_tex_coord = a_tex_coord;
        """,
        fragment_300="""
        vec4 c = texture2D(tex0, v_tex_coord);
        float line = 0.86 + 0.14 * sin(v_tex_coord.y * u_model_size.y * 2.0943951);
        float band = 0.06 * u_tv_motion * smoothstep(0.85, 1.0, sin((v_tex_coord.y - u_tv_time * 0.12) * 6.2831853));
        float flick = 0.025 * u_tv_motion * sin(u_tv_time * 43.0);
        gl_FragColor = vec4(c.rgb * line * (1.0 + band + flick), c.a);
        """)

    def _tv_glow_breath_f(lo, hi, t, trans, st, at):
        trans.alpha = fx_track(st, lo, (("ease", t, hi), ("ease", t, lo)))
        return fx_tick()

    def sm_tv_signal_f(trans, st, at):
        trans.u_tv_time = _fx_frame_time() % 1000.0
        trans.u_tv_motion = sm_motion_scale()
        return fx_tick()

transform sm_tv_signal():
    mesh True
    shader "sm.tv_signal"
    u_tv_time 0.0
    u_tv_motion 1.0
    function sm_tv_signal_f

## Свет экрана: размытая копия картинки, чуть крупнее экрана, ложится на корпус и комнату
## сложением цвета; сила дышит lo → hi → lo, по t секунд. center — центр экрана в кадре, px.
## mesh_pad — запас под размытие: без него свет обрывается краем картинки прямоугольником.
transform sm_tv_glow(center, zoom=1.3, blur=36.0, lo=0.18, hi=0.34, t=2.8):
    subpixel True
    transform_anchor True
    anchor (0.5, 0.5)
    pos center
    zoom zoom
    mesh True
    mesh_pad (int(blur * 3), int(blur * 3), int(blur * 3), int(blur * 3))
    blur blur
    blend "add"
    alpha lo
    function renpy.curry(_tv_glow_breath_f)(lo, hi, t)

## Включение кинескопа: от показа картинки в центре вспыхивает узкая искра-звезда,
## растягивается в ромб с вогнутыми сторонами, тот округляется и раскрывается на весь
## экран — всё за t секунд. Картинка внутри пятна сжата по его высоте и разворачивается
## вместе с ним, добела раскалена и остывает; вокруг пятна — ореол. Ставится на саму
## картинку, до sm_tv_set: свет экрана повторяет вспышку. При выключенных вспышках
## добела не раскаляется и ореола нет.
init python:
    renpy.register_shader("sm.tv_power",
        variables="""
        uniform sampler2D tex0;
        uniform float u_tvpw_level;
        uniform float u_tvpw_flash;
        attribute vec2 a_tex_coord;
        varying vec2 v_tvpw_coord;
        """,
        vertex_300="""
        v_tvpw_coord = a_tex_coord;
        """,
        fragment_300="""
        vec2 tvpw_q = v_tvpw_coord - 0.5;
        float tvpw_l = u_tvpw_level;
        float tvpw_w = 1.0 - pow(1.0 - clamp(tvpw_l / 0.3, 0.0, 1.0), 3.0);
        float tvpw_h = smoothstep(0.22, 0.9, tvpw_l);
        // Spot half-axes (0.5 is the screen edge) and superellipse exponent: below 1 the
        // sides are concave, 1 is a rhombus, 2 an ellipse, larger tends to a rectangle.
        vec2 tvpw_ab = vec2(max(mix(0.56, 0.8, tvpw_h) * tvpw_w, 0.0001), mix(0.012, 0.8, tvpw_h * tvpw_h));
        float tvpw_p = mix(0.7, 5.0, tvpw_h * tvpw_h * tvpw_h * tvpw_h);
        vec2 tvpw_n = max(abs(tvpw_q) / tvpw_ab, 0.00001);
        float tvpw_r = pow(pow(tvpw_n.x, tvpw_p) + pow(tvpw_n.y, tvpw_p), 1.0 / tvpw_p);
        float tvpw_lit = (1.0 - smoothstep(0.8, 1.0, tvpw_r)) * step(0.001, tvpw_l);
        vec2 tvpw_n2 = max(abs(tvpw_q) / (tvpw_ab + vec2(0.06, 0.04)), 0.00001);
        float tvpw_r2 = pow(pow(tvpw_n2.x, tvpw_p) + pow(tvpw_n2.y, tvpw_p), 1.0 / tvpw_p);
        float tvpw_heat = u_tvpw_flash * (1.0 - smoothstep(0.35, 0.95, tvpw_l));
        float tvpw_halo = tvpw_heat * 0.55 * (1.0 - smoothstep(0.35, 1.0, tvpw_r2)) * step(0.001, tvpw_l);

        vec2 tvpw_s = clamp(tvpw_ab / 0.5, 0.02, 1.0);
        vec4 tvpw_pic = texture2D(tex0, 0.5 + tvpw_q / tvpw_s)
            * step(abs(tvpw_q.x), 0.5 * tvpw_s.x) * step(abs(tvpw_q.y), 0.5 * tvpw_s.y);
        float tvpw_gain = 1.0 + 0.25 * u_tvpw_flash * (1.0 - smoothstep(0.6, 1.0, tvpw_l));
        float tvpw_white = tvpw_heat * mix(1.0, 0.7, clamp(tvpw_r, 0.0, 1.0));
        vec3 tvpw_rgb = mix(tvpw_pic.rgb * tvpw_gain, vec3(0.86, 0.93, 1.0), tvpw_white) * tvpw_lit
            + vec3(0.55, 0.72, 1.0) * tvpw_halo * (1.0 - tvpw_lit);
        gl_FragColor = vec4(tvpw_rgb, 1.0) * gl_FragColor.a;
        """)

transform sm_tv_power(t=0.9):
    mesh True
    shader "sm.tv_power"
    u_tvpw_flash (0.0 if sm_flashes_disabled() else 1.0)
    u_tvpw_level 0.0
    linear t u_tvpw_level 1.0

## Живая картинка на экране, едва заметно: поле колышется плавным шумом — мелкие фигурки
## перетаптываются и смещаются на доли пикселя (amp, px картинки); выше top (доля высоты:
## трибуны, щиты) картинка стоит. Разметку отличить от игроков нельзя — она «дышит» вместе
## с ними, поэтому amp держать маленьким. pan — камера трансляции: вся картинка медленно
## плывёт по горизонтали на ±pan px с периодом pan_t секунд. Сдвиг — точкой выборки, не
## геометрией: щели у края не бывает, а края прячет выпуклость стекла sm_crt_glass.
init python:
    renpy.register_shader("sm.tv_players",
        variables="""
        uniform sampler2D tex0;
        uniform vec2 u_model_size;
        uniform float u_tv_time;
        uniform float u_tv_motion;
        uniform float u_tvp_amp;
        uniform float u_tvp_top;
        uniform float u_tvp_speed;
        uniform float u_tvp_pan;
        uniform float u_tvp_pan_t;
        attribute vec2 a_tex_coord;
        varying vec2 v_tex_coord;
        """,
        vertex_300="""
        v_tex_coord = a_tex_coord;
        """,
        fragment_functions="""
        float sm_tvp_hash(vec2 p) {
            return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453);
        }
        float sm_tvp_noise(vec2 p) {
            vec2 i = floor(p);
            vec2 f = fract(p);
            vec2 u = f * f * (3.0 - 2.0 * f);
            return mix(mix(sm_tvp_hash(i), sm_tvp_hash(i + vec2(1.0, 0.0)), u.x),
                mix(sm_tvp_hash(i + vec2(0.0, 1.0)), sm_tvp_hash(i + vec2(1.0, 1.0)), u.x), u.y);
        }
        """,
        fragment_300="""
        vec2 px = v_tex_coord * u_model_size;
        float t = u_tv_time * u_tvp_speed;
        vec2 q = px * 0.035;
        vec2 n = vec2(sm_tvp_noise(q + vec2(t, 0.0)), sm_tvp_noise(q + vec2(13.1, t))) * 2.0 - 1.0;
        float field = smoothstep(u_tvp_top, u_tvp_top + 0.04, v_tex_coord.y);
        float w = 6.2831853 / max(u_tvp_pan_t, 0.1);
        float pan = u_tvp_pan * u_tv_motion * (0.7 * sin(u_tv_time * w) + 0.3 * sin(u_tv_time * w * 2.3 + 1.7));
        gl_FragColor = texture2D(tex0, (px + vec2(pan, 0.0) + n * u_tvp_amp * u_tv_motion * field) / u_model_size);
        """)

transform sm_tv_players(top=0.36, amp=1.5, speed=0.35, pan=10.0, pan_t=26.0):
    mesh True
    shader "sm.tv_players"
    u_tvp_top float(top)
    u_tvp_amp float(amp)
    u_tvp_speed float(speed)
    u_tvp_pan float(pan)
    u_tvp_pan_t float(pan_t)
    u_tv_time 0.0
    u_tv_motion 1.0
    function sm_tv_signal_f


## Свет телевизора на слое (рука перед экраном, комната): прибавка цвета tint, сильнее всего
## у прямоугольника экрана rect (x0, y0, x1, y1 — px слоя) и тающая за radius px. Мерцает,
## как живой экран (sm_tv_flicker): мелкая неровная рябь и смена уровня раз в пару секунд —
## будто сменился план. При «меньше движения» или выключенных вспышках свет ровный. Правит
## готовый цвет слоя, поэтому складывается с другими шейдерами того же трансформа.
init python:
    def sm_tv_flicker():
        """Яркость света экрана сейчас, около 0.7..1.1: уровень «плана» держится 1.9 с и
        меняется за 0.15 с, поверх — рябь. Один источник для всего, что светится от
        телевизора в кадре: слой (sm_tv_light) и контур (sm_tv_rim) мерцают синхронно."""
        import math
        if sm_reduced_motion() or sm_flashes_disabled():
            return 0.9
        t = _fx_frame_time() % 1000.0
        shot = t / 1.9
        k = math.floor(shot)
        level_from = math.sin((k - 1.0) * 12.9898) * 43758.5453 % 1.0
        level_to = math.sin(k * 12.9898) * 43758.5453 % 1.0
        blend = min(1.0, (shot - k) / 0.08)
        blend = blend * blend * (3.0 - 2.0 * blend)
        level = level_from + (level_to - level_from) * blend
        return 0.72 + 0.28 * level + 0.08 * math.sin(t * 7.3) + 0.05 * math.sin(t * 13.7 + 1.3)

    renpy.register_shader("sm.tv_light",
        variables="""
        uniform vec2 u_model_size;
        uniform vec4 u_tvl_rect;
        uniform vec3 u_tvl_tint;
        uniform float u_tvl_radius;
        uniform float u_tvl_strength;
        uniform float u_tvl_flick;
        attribute vec2 a_tex_coord;
        varying vec2 v_tvl_coord;
        """,
        vertex_300="""
        v_tvl_coord = a_tex_coord;
        """,
        fragment_300="""
        vec2 p = v_tvl_coord * u_model_size;
        vec2 outside = max(max(u_tvl_rect.xy - p, p - u_tvl_rect.zw), 0.0);
        float fall = exp(-length(outside) / u_tvl_radius);
        gl_FragColor.rgb += u_tvl_tint * (u_tvl_strength * fall * u_tvl_flick) * gl_FragColor.a;
        """)

    def sm_tv_light_f(trans, st, at):
        trans.u_tvl_flick = sm_tv_flicker()
        return fx_tick()

    def sm_tv_rim_f(strength, trans, st, at):
        trans.alpha = max(0.0, min(1.0, strength * sm_tv_flicker()))
        return fx_tick()

transform sm_tv_light(rect, tint=(1.0, 1.0, 1.0), radius=180.0, strength=0.16):
    mesh True
    shader "sm.tv_light"
    u_tvl_rect (float(rect[0]), float(rect[1]), float(rect[2]), float(rect[3]))
    u_tvl_tint (float(tint[0]), float(tint[1]), float(tint[2]))
    u_tvl_radius float(radius)
    u_tvl_strength float(strength)
    u_tvl_flick 0.9
    function sm_tv_light_f

## Контур, подсвеченный телевизором: отдельный слой с нарисованным бликом (на прозрачном,
## яркость — как в самый светлый момент) мерцает синхронно со светом экрана. strength —
## множитель, на мерцании альфа ходит около 0.7..1.0 от него.
transform sm_tv_rim(strength=1.0):
    alpha 0.9
    function renpy.curry(sm_tv_rim_f)(strength)

## Бегущая строка новостей внутри картинки телевизора (до ЭЛТ-шейдера): закрашивает
## запечённую размытую строку цветом полосы и прокручивает настоящий текст по кругу.
define SM_TV_TICKER_SPEED = 50.0
define SM_TV_TICKER_GAP = 44
define SM_TV_TICKER_FILL = "#cac8c6"
define SM_TV_TICKER_MARK = 6
define SM_TV_TICKER_INK = "#3c4438"

style sm_tv_ticker_text is default:
    font "fonts/roboto_condensed_bold.ttf"
    size 26
    color SM_TV_TICKER_INK
    outlines []
    layout "nobreak"

init python:
    class SmTvTicker(renpy.Displayable):
        """rect — полоса в px картинки. Лента начинается так, что сводка first въезжает
        с правого края через lead секунд после показа: кадр может держаться всего пару
        секунд, а нужная сводка не должна прятаться в середине круга."""

        def __init__(self, items, rect, first=0, lead=1.5, speed=SM_TV_TICKER_SPEED, **properties):
            super(SmTvTicker, self).__init__(**properties)
            self.texts = [Text(item, style="sm_tv_ticker_text") for item in items]
            self.rect = rect
            self.first = first
            self.lead = lead
            self.speed = speed

        def render(self, width, height, st, at):
            w, h = self.rect[2], self.rect[3]
            rv = renpy.Render(w, h)
            rv.blit(renpy.render(Solid(SM_TV_TICKER_FILL), w, h, st, at), (0, 0))
            renders = [renpy.render(text, 100000, h, st, at) for text in self.texts]
            steps = [r.width + SM_TV_TICKER_GAP for r in renders]
            total = sum(steps)
            start = sum(steps[:self.first]) - w
            x = -((start + (st - self.lead) * self.speed) % total)
            mark = renpy.render(Solid(SM_TV_TICKER_INK), SM_TV_TICKER_MARK, SM_TV_TICKER_MARK, st, at)
            i = 0
            while x < w:
                r = renders[i % len(renders)]
                rv.blit(r, (int(x), int((h - r.height) // 2)))
                x += r.width
                rv.blit(mark, (int(x + (SM_TV_TICKER_GAP - SM_TV_TICKER_MARK) // 2), (h - SM_TV_TICKER_MARK) // 2))
                x += SM_TV_TICKER_GAP
                i += 1
            renpy.redraw(self, 0)
            return rv

        def visit(self):
            return self.texts

    def sm_tv_ticker(items, rect, **kwargs):
        return Transform(SmTvTicker(items, rect, **kwargs), pos=(rect[0], rect[1]))
