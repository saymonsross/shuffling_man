## Тег дрожащего текста {sc} (эффект как в TVARUK_HD / Kinetic Text Tags):
## {sc}Текст{/sc}, {sc=6} — размах, px (по умолчанию 4), {sc=1:6} — размах растёт от
## первой буквы к последней. При «меньше движения» буквы стоят на месте.
## Сделан текстовым шейдером, а не буквами-displayable: так строка переносится как обычно.

## Текстовые шейдеры Ren'Py работают только при шейдере текста по умолчанию; typewriter
## повторяет обычное посимвольное появление.
define config.default_textshader = "typewriter"

init python:

    ## Каждая буква своим случайным сдвигом, новым каждый кадр; u__amp — размах, px.
    renpy.register_textshader(
        "scshake",
        variables="""
        uniform float u__amp;
        uniform vec4 u_random;
        uniform float u_text_to_drawable;
        attribute float a_text_index;
        """,
        vertex_30="""
        float l__seed = floor(u_random.x * 997.0);
        vec2 l__r = vec2(fract(sin(a_text_index * 12.9898 + l__seed) * 43758.5453),
            fract(sin(a_text_index * 78.233 + l__seed * 1.7) * 43758.5453));
        gl_Position.xy += (l__r - 0.3) * u__amp * u_text_to_drawable;
        """,
        u__amp=4.0,
        redraw=0.0,
        )

    def scare_tag(tag, argument, contents):
        argument = str(argument or 4)
        start, _, end = argument.partition(":")
        scale = sm_motion_scale()
        start = float(start) * scale
        end = (float(end) if end else float(argument.partition(":")[0])) * scale
        total = max(1, sum(len(text) for kind, text in contents if kind == renpy.TEXT_TEXT) - 1)

        rv = []
        index = 0
        for kind, text in contents:
            if kind != renpy.TEXT_TEXT:
                rv.append((kind, text))
                continue
            for char in text:
                amp = start + (end - start) * index / float(total)
                index += 1
                ## Пробел без шейдера: ему нечего трясти.
                if char.isspace():
                    rv.append((renpy.TEXT_TEXT, char))
                    continue
                ## Размах округлён: одинаковые теги шейдера разбираются из кэша.
                rv.append((renpy.TEXT_TAG, "shader=scshake:u__amp=%.1f" % amp))
                rv.append((renpy.TEXT_TEXT, char))
                rv.append((renpy.TEXT_TAG, "/shader"))
        return rv

    config.custom_text_tags["sc"] = scare_tag
