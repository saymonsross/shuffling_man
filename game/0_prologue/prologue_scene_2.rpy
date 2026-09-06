## Пролог, сцена 2.

label prologue_scene_2:

    camera
    scene prologue_head at uneasy_sway(PROLOGUE_SWAY_DRIFT, PROLOGUE_SWAY_TILT)
    with prologue_dissolve

    "Долго я не находила в себе сил, чтобы записать случившееся. Ушло много попыток."
    "Не было сил вспоминать: меня трясло, рвало, руки непроизвольно тянулись закрыть лицо."

    scene prologue_note_bg
    show prologue_note_paper at placed(NOTE_PAPER_NEAT_POS, (0.5, 0.5))
    show prologue_note_pencil at placed(NOTE_PENCIL_NEAT_POS, (0.5, 0.5))
    show prologue_hand_left at placed(NOTE_HAND_LEFT_POS)
    show prologue_hand_right at flag_fade(NOTE_HAND_RIGHT_POS, NOTE_HOVER_FLAGS, visible_when=False)
    with prologue_dissolve

    "Обо всём случившемся невыносимо думать."
    "Но я должна излить наружу то, что пожирает меня изнутри."

    window hide

    ## Общий jitter_key сохраняет непрерывность дрожи между позами.
    $ dismiss_off()
    $ fx_noise_strength = NOTE_WRITE_TENSION_NOISE
    $ pause(0.5)
    hide prologue_hand_right
    show prologue_hand_right_move at slide_in(NOTE_HAND_RIGHT_POS, NOTE_HAND_AT_PENCIL_POS, t=NOTE_HAND_REACH_T, jitter_amp=NOTE_HAND_JITTER_AMP, jitter_key="note_hand")
    $ pause(NOTE_HAND_REACH_T)
    $ pause(NOTE_HAND_HOVER_T)

    show prologue_hand_right_write at placed_jitter(NOTE_HAND_WRITE_GRIP_POS, jitter_amp=NOTE_HAND_JITTER_AMP, jitter_key="note_hand")
    hide prologue_hand_right_move
    hide prologue_note_pencil
    with Dissolve(0.4)
    $ pause(0.7)

    show prologue_hand_right_write at move_between(NOTE_HAND_WRITE_GRIP_POS, NOTE_HAND_LINE_START_POS, t=NOTE_HAND_TO_LINE_T, jitter_amp=NOTE_HAND_JITTER_AMP, jitter_key="note_hand")
    $ pause(NOTE_HAND_TO_LINE_T)
    $ dismiss_on()

    camera at mouse_parallax(NOTE_PARALLAX, NOTE_PARALLAX_SMOOTH, shake_amp=PENCIL_CLOSE_SHAKE_AMP)
    scene prologue_pencil_close
    with prologue_dissolve

    "Я не осмелюсь вернуться к карандашу и бумаге позже. Это будет моя последняя попытка. Спринтерский забег."
    "Я Расскажу всё на одном дыхании. Здесь и сейчас."

    $ fx_noise_strength = FX_NOISE_DEFAULT

    return
