## Smoke-тесты Dev Hub.

testcase dev_hub_hotkey:
    if not screen "main_menu":
        run MainMenu(confirm=False)
    assert eval (dev_hub_key_label("shift_K_o") == "Shift+O")
    assert eval (dev_hub_key_label("noshift_K_d") == "D")
    assert eval (dev_hub_key_label("mouseup_2") is None)
    assert eval (dev_hub_keys("console").startswith("Shift+O"))

    keysym "K_F12"
    assert screen "dev_hub" timeout 1.0
    ## Текстовый assert видит только фокусируемые элементы — проверяем кнопки.
    assert "Position Tuner"
    assert "Консоль"
    ## Лейблы недоступны из главного меню — пункт серый.
    assert eval (not dev_hub_tool_ok(next(e for e in DEV_HUB_TOOLS if e["title"] == "Заморозить кадр")))
    click "FX Tuner"
    assert not screen "dev_hub" timeout 1.0
    assert screen "fx_tuner" timeout 1.0
    keysym "K_ESCAPE"
    assert not screen "fx_tuner" timeout 1.0
