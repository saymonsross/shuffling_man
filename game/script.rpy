# Точка входа. Сценарий глав лежит в папках 0_prologue ... 4_endings.

label start:

    call prologue_scene_1 from _call_prologue_scene_1

    ## TODO: сюда встанет пролог — сцена 2, когда будет готова.

    ## Акцент границы глав: пролог уходит в чёрный, короткая выдержка —
    ## глава 1 сама открывается дизолвом уже из черноты.
    scene black
    with Dissolve(2.0)
    $ pause(1.2)

    call chapter_1_scene_1 from _call_chapter_1_scene_1

    return
