## Пролог, сцена 2.

screen prologue_note_start():
    modal True
    use sm_skippable_interaction
    ## Камера здесь сброшена; координаты совпадают с положением карандаша,
    ## а контейнер повторяет параллакс слоя master.
    fixed:
        at parallax_follow()
        xysize (config.screen_width, config.screen_height)
        use glow_button(
            _("Взять ручку"),
            Return("done"),
            bg="light",
            pos=(1264, 431),
            size=(260, 140),
            hovered=[SetVariable("note_hover_pencil", True), SPlay("click")],
            unhovered=SetVariable("note_hover_pencil", False))

label prologue_scene_2:

    $ note_hover_pencil = False
    ## При продолжении сохраняем тот же кадр и фазу покачивания; каталог входит отдельно.
    if not sprite_showed("prologue_head"):
        camera
        
        show prologue_head_bg:
            zoom 1.0
            truecenter
            subpixel True
            linear 40.5 zoom 1.2
        show prologue head
        with Dissolve(2.0)

    "Долго я не находила в себе сил, чтобы записать случившееся. Ушло много попыток."

    show prologue head_blink

    "Не было сил вспоминать: меня трясло, рвало, руки непроизвольно тянулись закрыть лицо."

    scene prologue_note_bg
    show prologue_note_paper at placed((990, 455), (0.5, 0.5))
    show prologue_note_pencil at placed((1264, 431), (0.5, 0.5))
    show prologue_hand_left at placed((271, 417))
    show prologue_hand_right at placed((1358, 468))
    with prologue_dissolve

    "Обо всём случившемся невыносимо думать."
    "Но я должна излить наружу то, что пожирает меня изнутри."

    window hide

    if not renpy.is_skipping():
        call screen prologue_note_start

    ## После закрытия экрана unhovered не вызывается.
    $ note_hover_pencil = False
    window auto

    $ dismiss_off()

    show prologue_hand_right_move:
        subpixel True
        anchor (0.0, 0.0)
        pos (1358, 468)
        linear 0.4 pos (1217, 211)
    hide prologue_hand_right
    with Dissolve(0.1)
    $ pause(0.2)

    ## Позы на разных холстах совмещены по кончику карандаша.
    show prologue_hand_right_write:
        subpixel True
        anchor (0.0, 0.0)
        pos (1217, 211)
        linear 0.4 pos (1100, 198)
    hide prologue_hand_right_move
    hide prologue_note_pencil
    with Dissolve(0.2)
    $ pause(0.1)
    $ dismiss_on()

    # camera at camera_rest(shake_amp=1.5)

    scene black with Dissolve(1.0)

    show prologue_pencil_close 
    show prologue_pensil_close_hand at shake(1.5)
    with Dissolve(1.3)

    "Я не осмелюсь вернуться к карандашу и бумаге позже."
    "Это будет моя последняя попытка. Так сказать, спринтерский забег."
    "Я Расскажу всё на одном дыхании. Здесь и сейчас."

    ## Граница между прологом и первой главой.
    scene black
    with Dissolve(2.0)
    $ pause(1.2)

    jump chapter_1_scene_1
