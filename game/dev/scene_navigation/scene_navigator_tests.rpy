## Smoke-тесты dev-навигатора сцен.

testcase dev_scene_navigator_menu:
    assert eval (all(renpy.has_label(entry['label']) for entry in DEV_SCENE_NAV_ENTRIES))
    assert eval (all(renpy.loadable(entry['preview']) for entry in DEV_SCENE_NAV_ENTRIES))
    assert eval (all(not entry['label'].startswith(('dev_', 'sm_test_')) for entry in DEV_SCENE_NAV_ENTRIES))
    assert eval (not renpy.has_label('dev_cleanup_preview') and not renpy.has_label('dev_tv_noise_preview'))

    if not screen "main_menu":
        run MainMenu(confirm=False)
    run ShowMenu("dev_scene_navigator")
    assert screen "dev_scene_navigator"
    assert "Сцена 1 · Записка"
    assert "Сцена 2 · Начало письма"
    assert "Сцена 1 · Стук в дверь"
    assert "Сцена 2 · Ссора"
    assert "Сцена 3 · Воображаемый друг"
    keysym "game_menu"

testcase dev_scene_navigator_starts_prologue:
    parameter entry_label = ["prologue_scene", "prologue_scene.letter"]

    if not screen "main_menu":
        run MainMenu(confirm=False)
    run ShowMenu("dev_scene_navigator")
    assert eval (renpy.get_displayable('dev_scene_navigator', 'prologue_scene') is not None)
    assert eval (renpy.get_displayable('dev_scene_navigator', 'prologue_scene').is_focused()) timeout 1.0
    if eval (entry_label == "prologue_scene"):
        keysym "button_select"
        advance until "Чтобы заговорить о чём-то тяжёлом" timeout 8.0
        advance until "Я здесь после нервного срыва" timeout 10.0
        assert eval (renpy.showing('prologue'))
        assert eval (not sprite_showed('prologue_note_bg'))
    else:
        click id entry_label

    advance until "Долго я не находила в себе сил" timeout 10.0
    assert eval (renpy.showing('prologue'))
    advance until "Взять ручку" timeout 10.0
    click "Взять ручку"
    assert "Я не осмелюсь вернуться к карандашу и бумаге позже." timeout 10.0
    assert eval (not note_hover_pencil and can_dismiss)
    advance until "Я Расскажу всё на одном дыхании. Здесь и сейчас." timeout 20.0
    assert eval (sprite_showed('prologue_pencil_close'))
    advance until "Зажечь свет" timeout 15.0
    assert not screen "main_menu"
    run MainMenu(confirm=False)

testcase dev_scene_navigator_starts_chapter_1:
    if not screen "main_menu":
        run MainMenu(confirm=False)
    click "НОВАЯ ИГРА"
    advance until "Чтобы заговорить о чём-то тяжёлом" timeout 8.0
    $ c1s3_neighbor_choice = "confront"
    keysym "game_menu"
    run ShowMenu("dev_scene_navigator")
    click id "chapter_1_scene_1"
    advance until "Зажечь свет" timeout 8.0
    assert eval (c1s3_neighbor_choice is None)

    ## Механику замков проверяют отдельно; здесь нужен настоящий возврат в маршрут.
    skip fast
    assert screen "c1s1_locks_open_door" timeout 15.0
    click "Открыть дверь"
    assert screen "c1s1_locks_minigame" timeout 10.0
    $ c1s1_mg_open_all()
    assert "Привет." timeout 10.0
    advance until "Наконец-то..." timeout 10.0
    assert eval (sm_test_tv_assert_shown('chapter_1 scene_1_tv_close'))
    advance until "Разбросанные носки, не опускающийся стульчак, как типично!" timeout 3.0
    assert eval (sprite_showed('chapter_1 scene_1_living_room_mess'))
    assert not screen "c1s1_cleanup_minigame"
    advance until screen "c1s1_cleanup_minigame" timeout 3.0
    assert eval (c1s1_cleanup_collected == ())
    assert eval (renpy.get_displayable('c1s1_cleanup_minigame', 'cleanup_background').name == ('chapter_1_cleanup_room',))
    python hide:
        for key in C1S1_CLEANUP_KEYS:
            c1s1_cleanup_collect(key)
        renpy.restart_interaction()
    assert "Ты в магазин зашёл?" timeout 6.0
    assert eval (sprite_showed('chapter_1 scene_1_kitchen_sink'))
    assert eval (c1s1_cleanup_outcome == 'done' and can_dismiss)
    advance until "Не-а." timeout 3.0
    assert eval (sm_test_tv_assert_shown('chapter_1 scene_1_sofa_tv_night', wide=True))
    advance until "Не, завтра не могу никак." timeout 3.0
    assert eval (sm_test_tv_assert_shown('chapter_1 scene_1_tv_close_night'))
    advance until "Я потеряла способность закрывать на эти мелочи глаза." timeout 15.0
    assert eval (sprite_showed('chapter_1 scene_2_parents_room_door'))
    assert not screen "main_menu"
    run MainMenu(confirm=False)


testcase dev_scene_navigator_continues_scene_2:
    parameter entry_label = ["chapter_1_scene_2", "chapter_1_scene_2.sandwiches"]

    if not screen "main_menu":
        run MainMenu(confirm=False)
    run ShowMenu("dev_scene_navigator")
    scroll "Bar" until id entry_label timeout 3.0
    click id entry_label

    if eval (entry_label == "chapter_1_scene_2"):
        assert "Я потеряла способность закрывать на эти мелочи глаза." timeout 8.0
    else:
        assert "Для него, для Настеньки. Для себя." timeout 3.0
        assert eval (sprite_showed('chapter_1 scene_2_sandwiches'))

    advance until "Все люди притворяются. Почему мы не могли?.." timeout 10.0
    assert eval (sprite_showed('chapter_1 scene_2_sandwiches_3'))
    run Function(sm_test_cleanup_memory_save)

    advance until "Моя дочь как раз проходила через сложный период" timeout 3.0
    assert eval (sprite_showed('chapter_1 scene_3_children_room_floor'))
    assert eval (not renpy.get_return_stack())
    run Rollback()
    assert "Все люди притворяются. Почему мы не могли?.." timeout 1.0
    assert eval (sprite_showed('chapter_1 scene_2_sandwiches_3'))

    advance until "Моя дочь как раз проходила через сложный период" timeout 3.0
    run Function(sm_test_cleanup_memory_load)
    assert "Все люди притворяются. Почему мы не могли?.." timeout 2.0
    assert eval (sprite_showed('chapter_1 scene_2_sandwiches_3'))
    assert eval ('_sm_cleanup_saved_game' not in renpy.session)
    advance until "Моя дочь как раз проходила через сложный период" timeout 3.0
    assert eval (sprite_showed('chapter_1 scene_3_children_room_floor'))
    assert eval (not renpy.get_return_stack())
    advance until screen "textbox" timeout 8.0
    click "Очаровашка!"
    advance until "Стоило нам с Витей обоим ненадолго отлучиться" timeout 10.0
    assert eval (sm_test_tv_assert_shown('chapter_1 scene_3_sofa_tv_1', wide=True))
    assert not screen "main_menu"
    run MainMenu(confirm=False)


testcase dev_scene_navigator_continues_household:
    parameter entry_label = ["chapter_1_scene_1.tv", "chapter_1_scene_1.cleanup"]

    if not screen "main_menu":
        run MainMenu(confirm=False)
    run ShowMenu("dev_scene_navigator")
    scroll "Bar" until id entry_label timeout 3.0
    click id entry_label

    if eval (entry_label == "chapter_1_scene_1.tv"):
        advance until "Наконец-то..." timeout 15.0
        assert eval (sm_test_tv_assert_shown('chapter_1 scene_1_tv_close'))
    else:
        assert "Разбросанные носки, не опускающийся стульчак, как типично!" timeout 3.0

    advance until "Разбросанные носки, не опускающийся стульчак, как типично!" timeout 3.0
    assert eval (sprite_showed('chapter_1 scene_1_living_room_mess'))
    assert not screen "c1s1_cleanup_minigame"
    advance until screen "c1s1_cleanup_minigame" timeout 3.0
    assert eval (c1s1_cleanup_collected == ())
    assert eval (renpy.get_displayable('c1s1_cleanup_minigame', 'cleanup_background').name == ('chapter_1_cleanup_room',))

    click pos (1490, 846)
    assert eval (len(c1s1_cleanup_collected) == 1) timeout 1.0
    click pos (1455, 676)
    assert eval (len(c1s1_cleanup_collected) == 2) timeout 1.0
    click pos (220, 790)
    assert eval (len(c1s1_cleanup_collected) == 3) timeout 1.0
    click pos (584, 635)
    assert eval (len(c1s1_cleanup_collected) == 4) timeout 1.0
    click pos (1740, 1003)
    assert eval (len(c1s1_cleanup_collected) == 5) timeout 1.0
    click pos (1035, 609)
    assert eval (len(c1s1_cleanup_collected) == 6) timeout 1.0
    click pos (940, 391)
    assert eval (len(c1s1_cleanup_collected) == 7) timeout 1.0
    click pos (856, 416)
    assert eval (len(c1s1_cleanup_collected) == 8) timeout 1.0
    click pos (362, 400)
    assert eval (len(c1s1_cleanup_collected) == 9) timeout 1.0
    click pos (619, 426)
    assert eval (len(c1s1_cleanup_collected) == 10) timeout 1.0
    click pos (1430, 424)

    assert "Ты в магазин зашёл?" timeout 6.0
    assert eval (sprite_showed('chapter_1 scene_1_kitchen_sink'))
    assert not screen "c1s1_cleanup_minigame"
    assert eval (c1s1_cleanup_outcome == 'done' and can_dismiss)
    advance until "Не-а." timeout 3.0
    assert eval (sm_test_tv_assert_shown('chapter_1 scene_1_sofa_tv_night', wide=True))
    advance until "Не, завтра не могу никак." timeout 3.0
    assert eval (sm_test_tv_assert_shown('chapter_1 scene_1_tv_close_night'))
    advance until "Я потеряла способность закрывать на эти мелочи глаза." timeout 10.0
    assert eval (sprite_showed('chapter_1 scene_2_parents_room_door'))
    assert not screen "main_menu"
    run MainMenu(confirm=False)
