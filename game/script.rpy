# Точка входа. Сценарий глав лежит в папках 0_prologue ... 4_endings.

label start:

    call prologue_scene_1 from _call_prologue_scene_1

label .prologue_scene_2 hide:
    call prologue_scene_2 from _call_prologue_scene_2

    ## Сохраняет исходную границу между прологом и первой главой.
    scene black
    with Dissolve(2.0)
    $ pause(1.2)

label .chapter_1_scene_1 hide:
    call chapter_1_scene_1 from _call_chapter_1_scene_1

label .chapter_1_scene_2 hide:
    call chapter_1_scene_2 from _call_chapter_1_scene_2

label .chapter_1_scene_3 hide:
    call chapter_1_scene_3 from _call_chapter_1_scene_3

    return

## Входы каталога в фрагменты основной игры продолжают общий маршрут главы.
label .chapter_1_tv hide:
    call chapter_1_scene_1.tv from _call_start_chapter_1_tv
    jump start.chapter_1_scene_2

label .chapter_1_cleanup hide:
    call chapter_1_scene_1.cleanup from _call_start_chapter_1_cleanup
    jump start.chapter_1_scene_2

label .chapter_1_sandwiches hide:
    camera
    call chapter_1_scene_2.sandwiches from _call_start_chapter_1_sandwiches
    jump start.chapter_1_scene_3
