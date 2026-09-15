testcase c1s2_sandwiches_clicks_and_rollback:
    run Function(dev_scene_nav_start, "chapter_1_scene_2.sandwiches")
    assert "Для него, для Настеньки. Для себя." timeout 3.0
    assert eval (sprite_showed("chapter_1 scene_2_sandwiches"))

    advance until "Трещины можно спрятать. Сделать вид, что их нет." timeout 3.0
    assert "Трещины можно спрятать. Сделать вид, что их нет." timeout 1.0
    assert eval (sprite_showed("chapter_1 scene_2_sandwiches_1"))

    advance until "Представить, что процесс разрушения остановлен." timeout 3.0
    assert "Представить, что процесс разрушения остановлен." timeout 1.0
    assert eval (sprite_showed("chapter_1 scene_2_sandwiches_2"))

    advance until "Все люди притворяются. Почему мы не могли?.." timeout 3.0
    assert "Все люди притворяются. Почему мы не могли?.." timeout 1.0
    assert eval (sprite_showed("chapter_1 scene_2_sandwiches_3"))

    run Rollback()
    assert "Представить, что процесс разрушения остановлен." timeout 1.0
    assert eval (sprite_showed("chapter_1 scene_2_sandwiches_2"))

    advance until "Все люди притворяются. Почему мы не могли?.." timeout 3.0
    assert "Все люди притворяются. Почему мы не могли?.." timeout 1.0
    assert eval (sprite_showed("chapter_1 scene_2_sandwiches_3"))
    advance until screen "main_menu" timeout 3.0
    assert screen "main_menu" timeout 3.0
