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

transform sm_crt_glass(projection, curvature=0.16, corner_radius=26.0, vignette=0.28):
    mesh True
    shader "sm.crt_glass"
    u_crt_row0 projection[0]
    u_crt_row1 projection[1]
    u_crt_row2 projection[2]
    u_crt_curvature curvature
    u_crt_corner_radius corner_radius
    u_crt_vignette vignette
