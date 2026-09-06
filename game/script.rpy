# Точка входа. Сценарий глав лежит в папках 0_prologue ... 4_endings.

label start:

    call prologue_scene_1 from _call_prologue_scene_1
    call prologue_scene_2 from _call_prologue_scene_2

    ## Сохраняет исходную границу между прологом и первой главой.
    scene black
    with Dissolve(2.0)
    $ pause(1.2)

    call chapter_1_scene_1 from _call_chapter_1_scene_1
    call chapter_1_scene_2 from _call_chapter_1_scene_2
    call chapter_1_scene_3 from _call_chapter_1_scene_3

    return
