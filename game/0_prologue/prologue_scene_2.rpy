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
            _("Начать"),
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
        scene prologue_head at uneasy_sway(12.0, 0.6)
        with prologue_dissolve

    "Долго я не находила в себе сил, чтобы записать случившееся. Ушло много попыток."
    "Не было сил вспоминать: меня трясло, рвало, руки непроизвольно тянулись закрыть лицо."

    scene prologue_note_bg
    show prologue_note_paper at placed((990, 455), (0.5, 0.5))
    show prologue_note_pencil at placed((1264, 431), (0.5, 0.5))
    show prologue_hand_left at placed((310, 391))
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
        ease 0.9 pos (1237, 211)
    hide prologue_hand_right
    with Dissolve(0.1)
    $ pause(1.0)

    ## Позы на разных холстах совмещены по кончику карандаша.
    show prologue_hand_right_write:
        subpixel True
        anchor (0.0, 0.0)
        pos (1237, 211)
        pause 1.1
        linear 1.1 pos (767, 158)
    hide prologue_hand_right_move
    hide prologue_note_pencil
    with Dissolve(0.4)
    $ pause(1.8)
    $ dismiss_on()

    camera at camera_rest(shake_amp=1.5)
    scene prologue_pencil_close
    with prologue_dissolve

    "Я не осмелюсь вернуться к карандашу и бумаге позже."
    "Это будет моя последняя попытка. Спринтерский забег."
    "Я Расскажу всё на одном дыхании. Здесь и сейчас."

    return
