## Smoke-тесты dev-навигатора сцен.

testcase dev_scene_navigator_menu:
    assert eval "all(renpy.has_label(entry['label']) for entry in DEV_SCENE_NAV_ENTRIES)"
    assert eval "all(renpy.loadable(entry['preview']) for entry in DEV_SCENE_NAV_ENTRIES)"

    if not screen "main_menu":
        run MainMenu(confirm=False)
    click "Сцены · DEV"
    assert screen "dev_scene_navigator"
    assert "Сцена 1 · Записка"
    assert "Сцена 1 · Стук в дверь"
    keysym "game_menu"

testcase dev_scene_navigator_starts_prologue:
    if not screen "main_menu":
        run MainMenu(confirm=False)
    click "Сцены · DEV"
    assert eval "renpy.get_displayable('dev_scene_navigator', 'prologue_scene_1') is not None"
    assert eval "renpy.get_displayable('dev_scene_navigator', 'prologue_scene_1').is_focused()" timeout 1.0
    keysym "button_select"
    advance until "Чтобы заговорить о чём-то тяжёлом" timeout 8.0

testcase dev_scene_navigator_starts_chapter_1:
    if not screen "main_menu":
        run MainMenu(confirm=False)
    click "Начать"
    advance until "Чтобы заговорить о чём-то тяжёлом" timeout 8.0
    keysym "game_menu"
    click "Сцены · DEV"
    click "chapter_1_scene_1"
    advance until screen "c1s1_lamp_switch" timeout 8.0
