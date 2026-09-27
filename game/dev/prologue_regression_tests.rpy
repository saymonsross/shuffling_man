testcase prologue_note_start_pickup_restore:
    ## Вход из сцены с камерой проверяет совпадение кнопки с карандашом после перехода.
    run Function(dev_scene_nav_start, "chapter_1_scene_1")
    assert screen "c1s1_lamp_switch" timeout 8.0
    keysym "game_menu"
    click "Сцены"
    click id "prologue_scene.letter"
    advance until screen "prologue_note_start" timeout 10.0
    assert "Взять ручку"
    assert eval (sprite_showed('prologue_note_pencil'))
    assert eval (sprite_showed('prologue_hand_right'))
    assert eval (not sprite_showed('prologue_hand_right_move'))
    assert eval (not sprite_showed('prologue_hand_right_write'))
    python hide:
        x, y, w, h = get_sprite_bounds("prologue_note_pencil")
        assert abs(x + w / 2.0 - 1264) < 2.0
        assert abs(y + h / 2.0 - 431) < 2.0

    move pos (100, 100)
    assert eval (not note_hover_pencil) timeout 1.0
    click pos (100, 100)
    assert screen "prologue_note_start"
    move pos (1264, 431)
    assert eval (note_hover_pencil) timeout 1.0
    run Function(sm_test_cleanup_memory_save)

    click pos (1264, 431)
    assert not screen "prologue_note_start" timeout 1.0
    assert eval (not note_hover_pencil)
    assert eval (sprite_showed('prologue_hand_right_write')) timeout 5.0
    assert eval (not sprite_showed('prologue_note_pencil'))
    assert eval (not sprite_showed('prologue_hand_right_move'))
    assert eval (not can_dismiss)
    assert "Я не осмелюсь вернуться к карандашу и бумаге позже." timeout 8.0
    assert eval (sprite_showed('prologue_pencil_close') and can_dismiss)

    run Rollback()
    assert screen "prologue_note_start" timeout 2.0
    assert eval (sprite_showed('prologue_note_pencil'))
    assert eval (not sprite_showed('prologue_hand_right_write'))
    click "Взять ручку"
    assert "Я не осмелюсь вернуться к карандашу и бумаге позже." timeout 10.0
    assert eval (not note_hover_pencil and can_dismiss)

    run Function(sm_test_cleanup_memory_load)
    assert screen "prologue_note_start" timeout 2.0
    assert eval (sprite_showed('prologue_note_pencil'))
    assert eval (not sprite_showed('prologue_hand_right_write'))
    assert eval ('_sm_cleanup_saved_game' not in renpy.session)
    move pos (100, 100)
    assert eval (not note_hover_pencil) timeout 1.0
    click "Взять ручку"
    assert "Я не осмелюсь вернуться к карандашу и бумаге позже." timeout 10.0
    assert eval (not note_hover_pencil and can_dismiss)
    run MainMenu(confirm=False)


testcase prologue_head_returns_after_fade:
    ## Голова и её фон гаснут через alpha и остаются на экране; .letter обязан вернуть их видимыми.
    if not screen "main_menu":
        run MainMenu(confirm=False)
    click "Начать"
    advance until "...должно помочь мне пережить произошедшее." timeout 20.0
    advance until "Долго я не находила в себе сил" timeout 5.0
    assert eval (renpy.showing('prologue') and renpy.showing('prologue_head_bg'))
    assert eval (pt_scene_state('prologue')['alpha'] > 0.99) timeout 3.0
    assert eval (pt_scene_state('prologue_head_bg')['alpha'] > 0.99) timeout 3.0

    advance until screen "prologue_note_start" timeout 8.0
    assert eval (sprite_showed('prologue_note_pencil') and not renpy.showing('prologue'))
    click "Взять ручку"
    assert "Я не осмелюсь вернуться к карандашу и бумаге позже." timeout 10.0
    assert eval (not note_hover_pencil and can_dismiss)
    run MainMenu(confirm=False)
