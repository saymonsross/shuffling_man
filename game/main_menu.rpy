## Главное меню как сцена (по образцу TVARUK_HD): задник и логотип ставятся обычными
## scene/show с ATL, экран main_menu (screens.rpy) несёт только кнопки.
## Ren'Py сам вызывает label main_menu вместо штатного меню, в контексте меню.

image main_menu_bg = gui.main_menu_background

## Процарапанный штрих (common/scratch_text.rpy): текст кнопок заливается цветом idle/hover,
## логотип сохраняет свой цвет и фактуру. Тюнеры групп — Font / Logo Tuner в Dev Hub.
init -10 python:

    scratch_params("main_menu_text", "Текст главного меню", 3.0, 0.3, 1.0, 0.55)
    scratch_params("main_menu_logo", "Логотип главного меню", 2.0, 0.15, 1.5, 0.4)

image main_menu_logo = At(gui.main_menu_logo, scratch("main_menu_logo", tint=0.0, pad=24))

label main_menu:
    $ quick_menu = False
    $ sm_parallax_off = True

    ## Штатный канал music вне пула 7dots; label start гасит его при старте игры.
    $ renpy.music.play("audio/main_menu.ogg", channel="music", if_changed=True, fadein=2.0, relative_volume=0.8)

    ## Возврат из подменю через _return снова входит сюда: постановку не повторяем.
    if not renpy.showing("prologue_head_bg"):
        scene prologue_head_bg:
            zoom 1.0
            rotate 0.0
            truecenter
            subpixel True
            # matrixcolor BrightnessMatrix(-0.1)
            parallel:
                breath_brightness(-0.11, -0.08, 16.0)
            parallel:
                linear 60.5 zoom 1.15
            parallel:
                linear 90.5 rotate 5.0
            
        show main_menu_logo:
            align (0.5, 0.115)
            zoom 0.8
        show screen main_menu
        with Dissolve(0.3)

label .loop:

    ## Return() из подменю завершает паузу; экран кнопок заменяет подменю по тегу menu.
    show screen main_menu
    $ renpy.pause(hard=True)
    jump .loop
