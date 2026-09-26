## Автоматические smoke-тесты Ren'Py. Каталог game/dev исключён из сборки.

init -999 python:
    if renpy.game.args.command in ("test", "compile", "lint"):
        ## В том числе запрещает запись при возврате теста в главное меню.
        config.save = False
        config.save_persistent = False

default sm_test_pointer_leaked = False
default sm_test_tick_sample = 0.0
default sm_test_arrow_rotation = 0.0

## Проба click-through под modal-мини-игрой.
screen sm_test_pointer_leak_target():
    zorder 100

    textbutton "LEAK PROBE":
        id "leak_probe"
        action SetVariable("sm_test_pointer_leaked", True)
        xalign 0.5
        yalign 1.0

testsuite global:
    before testcase:
        $ renpy.session["_sm_test_preferences"] = (persistent.sm_reduce_motion, persistent.sm_simplified_locks, persistent.sm_disable_flashes)
        $ renpy.session["_sm_test_get_mouse_pos"] = renpy.get_mouse_pos
        ## Реестр FX живёт вне rollback: упавший тест не должен оставить эффект включённым.
        $ renpy.session["_sm_test_fx"] = sm_test_fx_snapshot()

    after testcase:
        $ persistent.sm_reduce_motion, persistent.sm_simplified_locks, persistent.sm_disable_flashes = renpy.session.pop("_sm_test_preferences")
        $ renpy.get_mouse_pos = renpy.session.pop("_sm_test_get_mouse_pos")
        $ sm_test_fx_restore(renpy.session.pop("_sm_test_fx"))

    teardown:
        exit

testcase c1s1_metronome_motion:
    parameter reduce_motion = [False, True]

    $ persistent.sm_reduce_motion = reduce_motion
    run Function(dev_scene_nav_start, "chapter_1_scene_1")
    assert screen "c1s1_lamp_switch" timeout 8.0
    click "Зажечь свет"
    assert screen "c1s1_metronome_start" timeout 15.0
    click "Завести метроном"
    pause 1.5
    assert eval (sprite_showed("chapter_1_metronome_arrow"))
    $ sm_test_arrow_rotation = pt_scene_state("chapter_1_metronome_arrow")["rotate"]
    pause 0.45
    if eval (reduce_motion):
        assert eval (abs(sm_test_arrow_rotation) < 0.001)
        assert eval (abs(pt_scene_state("chapter_1_metronome_arrow")["rotate"]) < 0.001)
    else:
        assert eval (abs(sm_test_arrow_rotation) > 3.0)
        assert eval (abs(pt_scene_state("chapter_1_metronome_arrow")["rotate"] - sm_test_arrow_rotation) > 3.0)
    run MainMenu(confirm=False)
    assert eval ("_sm_test_preferences" in renpy.session)

testcase c1s1_minigame_model:
    $ c1s1_mg_reset()
    assert eval (isinstance(c1s1_mg_state, renpy.revertable.RevertableDict))
    assert eval (c1s1_mg_state.get('latch_p') == 0.0)
    assert eval (not c1s1_latch_open and not c1s1_big_lock_open and not c1s1_door_handle_open)

    $ c1s1_mg_active = True
    $ c1s1_mg_lock_i = 0
    $ c1s1_mg_simplified_step()
    $ c1s1_mg_simplified_tick(1.0)
    assert eval (c1s1_mg_state.get('latch_p') == 1.0 and not c1s1_latch_open)
    $ c1s1_mg_simplified_step()
    $ c1s1_mg_simplified_tick(1.0)
    assert eval (c1s1_mg_state.get('latch_p') == 2.0 and not c1s1_latch_open)
    $ c1s1_mg_simplified_step()
    $ c1s1_mg_simplified_tick(1.0)
    assert eval (c1s1_latch_open)
    assert eval (c1s1_mg_simplified_label() == 'Замок открыт')

    $ c1s1_mg_lock_i = 1
    $ c1s1_mg_simplified_step()
    $ c1s1_mg_simplified_tick(1.0)
    $ c1s1_mg_simplified_step()
    $ c1s1_mg_simplified_tick(1.0)
    assert eval (c1s1_big_lock_open and c1s1_mg_state.get('big_p') == 2.0)

    $ c1s1_mg_lock_i = 2
    $ c1s1_mg_simplified_step()
    $ c1s1_mg_simplified_tick(1.0)
    assert eval (c1s1_door_handle_open and c1s1_mg_state.get('handle_p') == 1.0)

    $ c1s1_mg_reset()
    assert eval (not c1s1_latch_open and not c1s1_big_lock_open and not c1s1_door_handle_open)
    $ c1s1_mg_active = True
    $ c1s1_mg_knocking = True
    $ _c1s1_clock_state.context_level = renpy.context_nesting_level() + 1
    $ _c1s1_clock_state.tick_clock = sm_time.monotonic() - 10.0
    $ c1s1_mg_tick()
    assert eval (sm_time.monotonic() - _c1s1_clock_state.tick_clock < 0.1)
    assert eval (c1s1_mg_state.get('play_t') < 0.1)
    assert eval (c1s1_mg_state.get('decision_t') < 0.1)
    assert eval (c1s1_mg_state.get('elapsed') < 0.1)
    $ _mg_set("play_t", 0.0)
    $ _mg_set("decision_t", 0.0)
    $ _c1s1_clock_state.tick_clock = sm_time.monotonic() - 1.0
    $ c1s1_mg_tick()
    assert eval (0.24 <= c1s1_mg_state.get('play_t') <= 0.25)
    assert eval (0.24 <= c1s1_mg_state.get('decision_t') <= 0.25)
    $ sm_test_tick_sample = _mg_get("play_t")
    $ c1s1_mg_tick()
    assert eval (0.0 <= c1s1_mg_state.get('play_t') - sm_test_tick_sample < 0.05)
    $ c1s1_mg_open_all()
    assert eval (c1s1_mg_lock_i == len(C1S1_MG_LOCK_ORDER))
    assert eval (c1s1_latch_open and c1s1_big_lock_open and c1s1_door_handle_open)

testcase c1s1_minigame_timed_outcomes:
    assert eval (c1s1_mg_outcome_for_time(C1S1_MG_FAST_T - 0.01) == 'fast')
    assert eval (c1s1_mg_outcome_for_time(C1S1_MG_FAST_T) == 'normal')
    assert eval (c1s1_mg_outcome_for_time(C1S1_MG_FAST_T + 0.01) == 'normal')
    ## Прежний порог проигрыша больше не создаёт отдельный исход.
    assert eval (c1s1_mg_outcome_for_time(39.99) == 'normal')
    assert eval (c1s1_mg_outcome_for_time(40.0) == 'normal')
    assert eval (c1s1_mg_outcome_for_time(3600.0) == 'normal')
    assert eval (c1s1_mg_vitya_line(0.0) == 'Это я, открывай!')
    assert eval (c1s1_mg_vitya_line(C1S1_MG_VITYA_INTERVAL_T) == 'Опять заперлась? Я ж на минуту выскочил!')
    assert eval (c1s1_mg_vitya_line(C1S1_MG_VITYA_INTERVAL_T * 2.0) == 'Боже, что ты там возишься?')
    assert eval (c1s1_mg_vitya_line(C1S1_MG_VITYA_INTERVAL_T * 3.0) == 'Марина, ну ёбана! Замок сломался?')
    assert eval (c1s1_mg_vitya_line(40.0) == 'Марина, ну ёбана! Замок сломался?')
    assert eval (c1s1_mg_vitya_line(3600.0) == 'Марина, ну ёбана! Замок сломался?')

    ## Время выбора не включает короткую выдержку уже открытого замка.
    $ c1s1_mg_reset()
    $ c1s1_mg_active = True
    $ c1s1_latch_open = True
    $ _c1s1_clock_state.tick_clock = sm_time.monotonic() - 0.2
    $ c1s1_mg_tick()
    assert eval (c1s1_mg_state.get('decision_t') == 0.0)
    assert eval (0.18 <= c1s1_mg_state.get('play_t') <= 0.25)

    ## Игровое меню переякоривает live clock и не начисляет время паузы.
    $ c1s1_mg_reset()
    $ c1s1_mg_active = True
    $ _mg_set("decision_t", 12.0)
    $ _c1s1_clock_state.tick_clock = sm_time.monotonic() - 10.0
    $ c1s1_mg_anchor_clock()
    $ c1s1_mg_tick()
    assert eval (12.0 <= c1s1_mg_state.get('decision_t') < 12.05)

    ## Неинициализированный и будущий anchor не дают отрицательный dt.
    $ _mg_set("decision_t", 0.0)
    $ _c1s1_clock_state.tick_clock = None
    $ c1s1_mg_tick()
    assert eval (c1s1_mg_state.get('decision_t') == 0.0)
    $ _c1s1_clock_state.tick_clock = sm_time.monotonic() + 1.0
    $ c1s1_mg_tick()
    assert eval (c1s1_mg_state.get('decision_t') == 0.0)

    $ c1s1_mg_reset()

testcase c1s1_minigame_accessibility:
    ## UI и drag должны читать один виртуальный курсор; hook восстановит export даже при падении.
    $ renpy.get_mouse_pos = lambda: renpy.test.testmouse.get_mouse_pos(0, 0)
    $ persistent.sm_simplified_locks = True
    $ persistent.sm_reduce_motion = True
    assert eval (abs(
        sm_motion_transition(c1s1_knock_punch)(old_widget=Null(), new_widget=Null()).delay
        - c1s1_knock_punch(old_widget=Null(), new_widget=Null()).delay) < 0.0001)
    assert eval (isinstance(
        sm_motion_transition(c1s1_knock_punch)(old_widget=Null(), new_widget=Null()),
        renpy.display.transition.NoTransition))
    $ persistent.sm_reduce_motion = False
    assert eval (sm_motion_transition(c1s1_knock_punch) is c1s1_knock_punch)
    $ c1s1_mg_reset()
    $ c1s1_mg_active = True

    run Show("c1s1_locks_minigame")
    assert not "Упростить управление"
    assert not "Вернуть перетаскивание"
    assert "Поднять щеколду"
    click "Поднять щеколду"
    assert "Сдвинуть щеколду вправо" timeout 1.0

    run Hide("c1s1_locks_minigame")
    $ c1s1_mg_active = False

testcase c1s1_minigame_pointer_capture:
    ## Проверяем настоящий drag после accessibility-сценария.
    if screen "main_menu":
        click "Начать" raw
        assert "Чтобы заговорить о чём-то тяжёлом" raw timeout 8.0
    $ persistent.sm_simplified_locks = False
    $ quick_menu = True
    $ c1s1_mg_reset()
    $ c1s1_mg_lock_i = 2
    $ c1s1_mg_active = True
    $ sm_test_pointer_leaked = False

    run Show("quick_menu")
    run Show("c1s1_mg_runtime")
    run Show("sm_test_pointer_leak_target")
    run Show("c1s1_locks_minigame")
    assert id "leak_probe"
    assert not "Упростить управление"
    assert not "Вернуть перетаскивание"

    ## Mouseup над нижним контролом не должен пройти сквозь мини-игру.
    $ sm_test_handle_pos = (int(c1s1_handle_pivot_screen()[0] + C1S1_HANDLE_GRAB_BOX[0] * C1S1_HANDLE_ZOOM), int(c1s1_handle_pivot_screen()[1] + C1S1_HANDLE_GRAB_BOX[1] * C1S1_HANDLE_ZOOM))
    drag pos sm_test_handle_pos to id "leak_probe" pos (0.5, 0.5) steps 8
    pause 0.2
    assert eval (not sm_test_pointer_leaked)
    assert eval (not c1s1_mg_pointer_down())
    assert eval (_mg_get('handle_grab') == 0.0)

    ## Завершение ждёт физического release.
    $ c1s1_door_handle_open = True
    $ _mg_set("done", 0.0)
    $ _mg_set("play_t", C1S1_MG_DONE_HOLD_T + 1.0)
    $ _c1s1_clock_state.pointer_down = True
    $ c1s1_mg_check_done()
    assert eval (c1s1_mg_pointer_down() and _mg_get('done') == 0.0)

    ## Потерянный SDL mouseup не должен навсегда оставить экран modal.
    $ _c1s1_clock_state.pointer_up_since = sm_time.monotonic() - C1S1_MG_POINTER_LOST_T - 0.01
    $ c1s1_mg_recover_lost_pointer(sm_time.monotonic())
    assert eval (not c1s1_mg_pointer_down())

    $ c1s1_mg_release()
    run Hide("c1s1_locks_minigame")
    run Hide("sm_test_pointer_leak_target")

    ## Quick menu скрыто до завершения runtime.
    assert not "История" raw
    assert not "Меню" raw
    run Hide("c1s1_mg_runtime")
    assert ("История" raw or "Меню" raw) timeout 1.0
    $ c1s1_mg_active = False
    $ c1s1_mg_reset()

testcase c1s1_story_fast_outcome:
    $ c1s1_locks_outcome = "fast"
    $ dismiss_on()
    run Jump("chapter_1_scene_1.after_locks")
    assert "Привет." timeout 10.0
    advance
    advance until "Ничего серьёзного:" timeout 10.0
    assert eval (sprite_showed('chapter_1 scene_1_hall_mess'))
    advance until "Наконец-то..." timeout 10.0
    assert eval (c1s1_locks_outcome == 'fast')

testcase c1s1_story_normal_outcome:
    $ c1s1_locks_outcome = "normal"
    $ dismiss_on()
    run Jump("chapter_1_scene_1.after_locks")
    assert "Ну наконец-то, бля." timeout 10.0
    advance
    advance until "Ничего серьёзного:" timeout 10.0
    assert eval (sprite_showed('chapter_1 scene_1_hall_mess'))
    advance until "Наконец-то..." timeout 10.0
    assert eval (c1s1_locks_outcome == 'normal')

testcase c1s1_story_legacy_timeout_outcome:
    $ c1s1_locks_outcome = "timeout"
    $ dismiss_on()
    run Jump("chapter_1_scene_1.after_locks")
    assert "Ну наконец-то, бля." timeout 10.0
    advance
    advance until "Ничего серьёзного:" timeout 10.0
    assert eval (sprite_showed('chapter_1 scene_1_hall_mess'))
    advance until "Наконец-то..." timeout 10.0
    assert eval (c1s1_locks_outcome == 'normal')

testcase c1s3_apologize_branch:
    $ c1s3_teaparty_choice = None
    $ c1s3_neighbor_choice = None
    $ dismiss_on()
    run Jump("chapter_1_scene_3")
    advance until screen "choice" timeout 10.0
    assert "Очаровашка!"
    assert "Зануда!"
    assert "Странный!"
    assert "А где Полли?"
    click "Очаровашка!"
    advance until screen "choice" timeout 10.0
    assert "Простите..."
    assert "Заткнитесь!"
    assert eval (sprite_showed('chapter_1 scene_3_entrance_neighbors'))
    click "Простите..."
    advance until "Я знала. Просто не понимала, как. Мы пытались разобраться..." timeout 10.0
    assert eval (c1s3_teaparty_choice == 'charming')
    assert eval (c1s3_neighbor_choice == 'apologize')
    advance until "Конечно, мы ходили с дочкой к психологу." timeout 10.0
    assert eval (sprite_showed('chapter_1 scene_3_sofa_marina'))
    advance until "Он приходит, когда дома тихо" timeout 10.0
    assert eval (sprite_showed('chapter_1 scene_3_sofa_daughter'))
    advance until "Шаркающий человек." timeout 10.0

testcase c1s3_confront_branch:
    $ c1s3_teaparty_choice = None
    $ c1s3_neighbor_choice = None
    $ dismiss_on()
    run Jump("chapter_1_scene_3")
    advance until screen "choice" timeout 10.0
    click "А где Полли?"
    advance until screen "choice" timeout 10.0
    click "Заткнитесь!"
    advance until "Они не имели права нравоучать нас." timeout 10.0
    advance until "Пусть лучше приглядывают за своими детьми, болтающимися без дела по двору, как оборванцы." timeout 5.0
    assert eval (c1s3_teaparty_choice == 'where_is_polly')
    assert eval (c1s3_neighbor_choice == 'confront')
    advance until "Шаркающий человек." timeout 10.0

testcase c1s3_strange_branch:
    $ dismiss_on()
    run Jump("chapter_1_scene_3")
    advance until screen "choice" timeout 10.0
    click "Странный!"
    assert "Кажется, он помешан на еловых шишках..." timeout 10.0
    assert eval (c1s3_teaparty_choice == 'strange')
    advance until "В лесу нет конфеток! Вот и приходится шишами чай закусывать..." timeout 10.0

testcase story_full_route:
    parameter reduce_motion = [False, True]

    if not screen "main_menu":
        run MainMenu(confirm=False)
    click "Начать"
    $ persistent.sm_reduce_motion = reduce_motion
    advance until "Я здесь после нервного срыва" timeout 10.0
    assert eval (sprite_showed('prologue_head'))
    assert eval (not sprite_showed('prologue_note_bg'))
    advance until "Долго я не находила в себе сил" timeout 10.0
    assert eval (sprite_showed('prologue_head'))
    advance until screen "prologue_note_start" timeout 10.0
    click "Взять ручку"
    assert "Я не осмелюсь вернуться к карандашу и бумаге позже." timeout 10.0
    assert eval (not note_hover_pencil and can_dismiss)
    advance until "Я Расскажу всё на одном дыхании. Здесь и сейчас." timeout 20.0
    assert eval (sprite_showed('prologue_pencil_close'))
    advance until screen "c1s1_lamp_switch" timeout 15.0
    click "Зажечь свет"
    advance until screen "c1s1_metronome_start" timeout 15.0
    click "Завести метроном"
    skip fast
    assert screen "c1s1_locks_open_door" timeout 15.0
    click "Открыть дверь"
    assert screen "c1s1_locks_minigame" timeout 10.0
    assert eval (c1s1_mg_active and c1s1_mg_knocking)
    assert eval (c1s1_mg_vitya_line() == 'Это я, открывай!')

    ## Механику замков проверяют отдельные тесты; здесь важен возврат из мини-игры в сцену.
    $ c1s1_mg_open_all()
    assert "Привет." timeout 10.0
    assert eval (c1s1_locks_outcome == 'fast')
    advance until "Разбросанные носки, не опускающийся стульчак, как типично!" timeout 10.0
    assert eval (sprite_showed('chapter_1 scene_1_living_room_mess'))
    advance until screen "c1s1_cleanup_minigame" timeout 3.0
    assert eval (c1s1_cleanup_collected == ())
    ## Сбор каждого предмета проверен отдельно; здесь продолжаем настоящий маршрут.
    python hide:
        for key in C1S1_CLEANUP_KEYS:
            c1s1_cleanup_collect(key)
        renpy.restart_interaction()
    assert id "cleanup_continue" timeout 1.0
    click id "cleanup_continue"
    assert eval (c1s1_cleanup_outcome == 'done')
    assert "Ты в магазин зашёл?" timeout 3.0
    advance until "Я потеряла способность закрывать на эти мелочи глаза." timeout 15.0
    assert eval (sprite_showed('chapter_1 scene_2_parents_room_door'))
    advance until "Ладно, пойдём поедим. Я состряпаю чего-нибудь." timeout 15.0
    assert eval (sprite_showed('chapter_1 scene_2_parents_room_door_marina'))
    advance until "Моя дочь как раз проходила через сложный период" timeout 15.0
    assert eval (sprite_showed('chapter_1 scene_3_children_room_floor'))
    advance until "То есть вела себя как обычно" timeout 10.0
    assert eval (sprite_showed('chapter_1 scene_3_fridge'))
    advance until "Последней её потрясающей выдумкой" timeout 10.0
    assert eval (sprite_showed('chapter_1 scene_3_fridge_new_drawing'))
    advance until "Спасибо, что побыла на нашем чаепитии!" timeout 10.0
    assert eval (sprite_showed('chapter_1 scene_3_children_room_girl_neutral'))
    advance until screen "choice" timeout 10.0
    assert eval (sprite_showed('chapter_1 scene_3_toys'))
    click "Зануда!"
    assert "Его лекция о мёдоведении была совершенно ни к месту!" timeout 10.0
    assert eval (c1s3_teaparty_choice == 'boring')
    advance until "Он очень гордится своей научной... Штукой!" timeout 10.0
    advance until "Я пойду встречу папу с работы. Посиди, пока..." timeout 10.0
    assert eval (sprite_showed('chapter_1 scene_3_children_room_girl_sad'))
    advance until "НЕТ!" timeout 10.0
    assert eval (sprite_showed('chapter_1 scene_3_children_room_girl_crying'))
    advance until "Стоило нам с Витей обоим ненадолго отлучиться" timeout 10.0
    assert eval (sprite_showed('chapter_1 scene_3_sofa_tv_1'))
    advance until "Мы пыталась с ней по-хорошему поговорить" timeout 10.0
    assert eval (sprite_showed('chapter_1 scene_3_entrance'))
    advance until "Это ни в какие рамки." timeout 10.0
    assert eval (sprite_showed('chapter_1 scene_3_daughter_top'))
    advance until "Вот она: охрипшая от крика" timeout 10.0
    assert eval (sprite_showed('chapter_1 scene_3_daughter_top_close'))
    advance until "Ну наконец-то явились! И что за дела?" timeout 10.0
    assert eval (sprite_showed('chapter_1 scene_3_entrance_neighbor'))
    advance until screen "choice" timeout 10.0
    assert eval (sprite_showed('chapter_1 scene_3_entrance_neighbors'))
    click "Простите..."
    advance until "Шаркающий человек." timeout 10.0
    advance until screen "main_menu" timeout 10.0
    assert eval ("_sm_test_preferences" in renpy.session)
    assert eval (not config.save and not config.save_persistent)
