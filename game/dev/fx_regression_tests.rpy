## Регрессия FX-конфига, постеризации и FX Tuner. Каталог game/dev исключён из сборки.
## Состояние реестра восстанавливают хуки testsuite global (testcases.rpy).

## Однотонные плашки: центры не зависят от масштабирования кадра, поэтому
## ожидаемый байт считается по формуле шейдера точно. Цвета не лежат на
## границах ступеней для steps 4/5 и gamma 1/2.
define SM_TEST_SWATCHES = (
    (0.30, 0.55, 0.90), (0.10, 0.45, 0.70), (0.99, 0.22, 0.62),
    (1.0, 1.0, 1.0), (0.0, 0.0, 0.0), (0.26, 0.74, 0.51),
)

## Ряды живого кадра: master, lockgame и экран UI на слое screens.
define SM_TEST_ROW_MASTER = 220
define SM_TEST_ROW_LOCK = 520
define SM_TEST_ROW_UI = 820

init python:

    import io as _sm_test_io
    import math as _sm_test_math
    import os as _sm_test_os
    import pygame_sdl2 as _sm_test_pygame
    import shutil as _sm_test_shutil
    import tempfile as _sm_test_tempfile

    def sm_test_fx_snapshot():
        """Снимок реестра и накопителей: rollback и MainMenu их не возвращают."""
        return (python_dict(_fxc_values), python_dict(_fxc_saved), python_dict(_fxc_file),
                python_list(fx_cfg_warnings), python_dict(fx_cfg_runtime),
                _fx_state.get("posterize_level"), _fx_state.get("noise_tension"),
                getattr(store, "fx_posterize_strength", None), fxt_model.status)

    def sm_test_fx_restore(snap):
        values, saved, file_, warnings, runtime, level, noise, strength, status = snap
        pairs = ((_fxc_values, values), (_fxc_saved, saved), (_fxc_file, file_), (fx_cfg_runtime, runtime))
        for target, source in pairs:
            target.clear()
            target.update(source)
        fx_cfg_warnings[:] = warnings
        for key, value in (("posterize_level", level), ("noise_tension", noise)):
            if value is None:
                _fx_state.pop(key, None)
            else:
                _fx_state[key] = value
        if strength is not None:
            store.fx_posterize_strength = strength
        fxt_model.status = status

    def sm_test_expect_error(text):
        try:
            fx_cfg_parse(text)
        except FxConfigError:
            return True
        raise AssertionError("parser accepted: %r" % text)

    def sm_test_swatch_centers(y=300):
        return [(160 + 320 * i, y) for i in range(len(SM_TEST_SWATCHES))]

    def sm_test_swatches(alpha=1.0, y=300):
        return Fixed(*[
            Transform(Solid(Color(rgb=rgb, alpha=alpha)), xysize=(280, 280), anchor=(0.5, 0.5), pos=pos)
            for rgb, pos in zip(SM_TEST_SWATCHES, sm_test_swatch_centers(y))
        ], xysize=(1920, 1080))

    def sm_test_render(d):
        return renpy.render_to_surface(d, width=1920, height=1080, st=0.03, resize=True)

    def sm_test_poster_byte(value, steps, mix=1.0, gamma=1.0):
        c = value / 255.0
        q = min(_sm_test_math.floor(c ** (1.0 / gamma) * steps) / (steps - 1.0), 1.0) ** gamma
        return (c + (q - c) * mix) * 255.0

    def sm_test_swatch_errors(raw, post, steps=None, mix=1.0, gamma=1.0, alpha=1.0, y=300):
        """Расхождения в центрах плашек; steps=None — ждём кадр без изменений.
        Альфа-канал render_to_surface искажён (0.5 → 63), поэтому доля берётся
        из фикстуры, а straight/premultiplied определяется по исходнику."""
        scale = raw.get_width() / 1920.0
        errors = python_list()
        for rgb, (x, cy) in zip(SM_TEST_SWATCHES, sm_test_swatch_centers(y)):
            point = (int(x * scale), int(cy * scale))
            r, o = raw.get_at(point), post.get_at(point)
            premult = alpha < 0.99 and abs(r[0] - rgb[0] * alpha * 255) < abs(r[0] - rgb[0] * 255)
            want = python_list()
            for channel in r[:3]:
                if steps is None:
                    want.append(channel)
                elif premult:
                    want.append(sm_test_poster_byte(channel / alpha, steps, mix, gamma) * alpha)
                else:
                    want.append(sm_test_poster_byte(channel, steps, mix, gamma))
            if abs(o[3] - r[3]) > 1 or any(abs(g - w) > 2 for g, w in zip(o[:3], want)):
                errors.append((point, tuple(r), tuple(o), tuple(int(round(w)) for w in want)))
        return errors

    def sm_test_screen_surface():
        data = renpy.screenshot_to_bytes(None)
        return _sm_test_pygame.image.load(_sm_test_io.BytesIO(data), "shot.png")

    def sm_test_assert_live(raw, scope):
        """Мир квантуется в любом охвате, UI — только в охвате screen."""
        post = sm_test_screen_surface()
        errors = sm_test_swatch_errors(raw, post, 4, y=SM_TEST_ROW_MASTER)
        errors += sm_test_swatch_errors(raw, post, 4, y=SM_TEST_ROW_LOCK)
        errors += sm_test_swatch_errors(raw, post, 4 if scope == "screen" else None, y=SM_TEST_ROW_UI)
        assert not errors, (scope, errors)

image sm_test_poster_world = sm_test_swatches(y=SM_TEST_ROW_MASTER)
image sm_test_poster_lock = sm_test_swatches(y=SM_TEST_ROW_LOCK)

screen sm_test_poster_ui_probe():
    add sm_test_swatches(y=SM_TEST_ROW_UI)

## Детерминированный кадр без камеры: пиксели плашек зависят только от эффекта.
label sm_test_posterize_scene:
    scene black
    show sm_test_poster_world
    show sm_test_poster_lock onlayer lockgame
    show screen sm_test_poster_ui_probe
    while True:
        pause


testcase fx_config_yaml_parser:
    python hide:
        text = (
            "# заголовок\n"
            "top_key: 7\n"
            "\n"
            "posterize:  # группа\n"
            "  enabled: true   # вкл\n"
            "  steps: 12\n"
            "  mix: 0.35\n"
            "  name: \"a # b \\\" c\"\n"
            "  quote: 'it''s'\n"
            "  scope: screen\n"
            "  list: [1, 2.5, x, \"y, z\"]\n"
            "  empty: ~\n"
            "legacy:\n"
            "  deep:\n"
            "    value: -3\n"
        )
        parsed = fx_cfg_parse(text)
        assert parsed == {
            "top_key": 7,
            "posterize.enabled": True,
            "posterize.steps": 12,
            "posterize.mix": 0.35,
            "posterize.name": 'a # b " c',
            "posterize.quote": "it's",
            "posterize.scope": "screen",
            "posterize.list": [1, 2.5, "x", "y, z"],
            "posterize.empty": None,
            "legacy.deep.value": -3,
        }, parsed
        assert fx_cfg_parse(chr(0xFEFF) + "a:\n  b: 1\n") == {"a.b": 1}
        assert fx_cfg_parse("a: " + "9" * 5000 + "\n")["a"] == "9" * 5000

        sm_test_expect_error("a:\n\tb: 1\n")
        sm_test_expect_error("a:\n  - 1\n")
        sm_test_expect_error("just text\n")
        sm_test_expect_error("a: \"open\n")
        sm_test_expect_error("a: [1, 2\n")
        sm_test_expect_error("a: 1\n  b: 2\n")
        sm_test_expect_error("a:\n  b: 1\n c: 2\n")

testcase fx_config_coercion:
    python hide:
        steps = FxParam("t.steps", 5, 2, 32, None, None, "")
        assert steps.kind == "int" and steps.coerce(40) == 32 and steps.coerce(1) == 2
        assert steps.coerce(6.6) == 7
        for bad in ("banana", True, None, float("nan")):
            try:
                steps.coerce(bad)
            except ValueError:
                pass
            else:
                raise AssertionError("int accepted %r" % (bad,))

        mix = FxParam("t.mix", 1.0, 0.0, 1.0, None, None, "")
        assert mix.kind == "float" and mix.coerce(0.1 + 0.2) == 0.3 and mix.coerce(3) == 1.0
        assert mix.step == 0.01
        ## Целые границы у float-параметра не превращают значение в int.
        wide = FxParam("t.wide", 1.0, 0, 4, None, None, "")
        assert isinstance(wide.coerce(-5), float) and isinstance(wide.coerce(9), float)
        count = FxParam("t.count", 3, 1.0, 8.0, None, None, "")
        assert isinstance(count.coerce(0), int) and isinstance(count.coerce(20), int)

        flag = FxParam("t.flag", False, None, None, None, None, "")
        assert flag.coerce(True) is True
        try:
            flag.coerce(1)
        except ValueError:
            pass
        else:
            raise AssertionError("bool accepted 1")

        scope = FxParam("t.scope", "scene", None, None, None, ("scene", "screen"), "")
        assert scope.kind == "choice" and scope.coerce("screen") == "screen"
        try:
            scope.coerce("everything")
        except ValueError:
            pass
        else:
            raise AssertionError("choice accepted unknown value")

    python hide:
        _fxc_file["posterize.steps"] = "banana"
        _fxc_file["posterize.mix"] = 7
        _fxc_file["posterize.stpes"] = 3
        del fx_cfg_warnings[:]
        assert _fxc_resolve(fx_cfg_param("posterize.steps")) == 5
        assert _fxc_resolve(fx_cfg_param("posterize.mix")) == 1.0
        assert len(fx_cfg_warnings) == 1 and "posterize.steps" in fx_cfg_warnings[0]
        assert any("posterize.stpes" in issue for issue in fx_cfg_issues())

testcase fx_config_save_roundtrip:
    python hide:
        folder = _sm_test_tempfile.mkdtemp(prefix="sm_fx_")
        try:
            assert fx_cfg_dirty_keys() == []
            fx_cfg_set("posterize.steps", 7)
            fx_cfg_set("posterize.mix", 0.35)
            fx_cfg_set("posterize.scope", "screen")
            fx_cfg_set("posterize.enabled", True)
            _fxc_file["legacy.old_value"] = 3
            _fxc_file["version"] = 2
            assert set(fx_cfg_dirty_keys()) == {"posterize.steps", "posterize.mix",
                                                "posterize.scope", "posterize.enabled"}

            path = fx_cfg_save(_sm_test_os.path.join(folder, "fx_config.yaml"))
            ## Сохранение во временный файл не сдвигает базу основного файла.
            assert len(fx_cfg_dirty_keys()) == 4
            assert not _sm_test_os.path.exists(path + ".tmp")

            with open(path, encoding="utf-8") as f:
                written = f.read()
            parsed = fx_cfg_parse(written)
            for p in fx_cfg_params():
                assert parsed[p.key] == fx_cfg(p.key), p.key
            assert parsed["legacy.old_value"] == 3 and parsed["version"] == 2
            assert "# уровней на канал · 2..32" in written
            assert "не используется кодом" in written
            assert "\r" not in written
        finally:
            _sm_test_shutil.rmtree(folder, ignore_errors=True)

    ## Файл репозитория парсится, и в нём нет ключей, неизвестных коду.
    ## Новый fx_param может отсутствовать в файле до первого «Сохранить».
    python hide:
        with renpy.open_file(FX_CONFIG_FILE) as f:
            shipped = fx_cfg_parse(f.read().decode("utf-8-sig"))
        known = set(p.key for p in fx_cfg_params())
        assert set(shipped) <= known, sorted(set(shipped) - known)
        for key, value in shipped.items():
            assert fx_cfg_param(key).coerce(value) == value, key

testcase fx_posterize_shader_levels:
    python hide:
        for alpha in (1.0, 0.5):
            fixture = sm_test_swatches(alpha)
            raw = sm_test_render(fixture)
            for steps, mix, gamma in ((5, 1.0, 1.0), (4, 1.0, 1.0), (5, 1.0, 2.0), (5, 0.5, 1.0)):
                post = sm_test_render(At(fixture, posterize(steps, mix=mix, gamma=gamma)))
                errors = sm_test_swatch_errors(raw, post, steps, mix, gamma, alpha)
                assert not errors, (alpha, steps, mix, gamma, errors)
            same = sm_test_render(At(fixture, posterize(5, mix=0.0)))
            assert not sm_test_swatch_errors(raw, same), alpha
            ## show … at наследует состояние прошлого трансформа — как take_state.
            first = posterize(5)(child=fixture)
            sm_test_render(first)
            off = posterize_off(child=fixture)
            off.take_state(first)
            assert not sm_test_swatch_errors(raw, sm_test_render(off)), alpha

testcase fx_posterize_layer_modes:
    python hide:
        fixture = sm_test_swatches()
        raw = sm_test_render(fixture)
        _fx_state["posterize_level"] = 1.0
        fx_cfg_set("posterize.steps", 4)
        fx_cfg_set("posterize.mix", 1.0)
        fx_cfg_set("posterize.gamma", 1.0)
        fx_cfg_set("posterize.scope", "scene")

        ## python hide исполняется через exec: вложенным функциям локали передаются явно.
        def errors(scope, steps=None, fixture=fixture, raw=raw):
            post = sm_test_render(At(fixture, posterize_layer(scope)))
            return sm_test_swatch_errors(raw, post, steps)

        fx_cfg_set("posterize.enabled", False)
        assert not errors("scene"), "disabled effect changed the frame"

        fx_cfg_set("posterize.enabled", True)
        assert not errors("scene", 4), errors("scene", 4)
        assert not errors("screen"), "inactive scope changed the frame"

        fx_cfg_runtime["bypass"] = True
        assert not errors("scene"), "A/B bypass kept the effect"
        fx_cfg_runtime["bypass"] = False

        ## Цель 0 при накопителе 0: сглаживание не сдвигает силу между кадрами.
        store.fx_posterize_strength = 0.0
        _fx_state["posterize_level"] = 0.0
        assert not errors("scene"), "scene strength 0 kept the effect"
        fx_cfg_runtime["preview"] = True
        _fx_state["posterize_level"] = 1.0
        assert not errors("scene", 4), "preview ignored"

    python hide:
        world = [name for name in config.layers if name not in FX_POSTERIZE_UI_LAYERS]
        assert "master" in world and "lockgame" in world, world
        for name in world:
            assert config.layer_transforms.get(name), name
        for name in FX_POSTERIZE_UI_LAYERS:
            assert not config.layer_transforms.get(name), name
        assert config.layer_transforms.get(None)

testcase fx_posterize_live_frame:
    parameter scope = ["screen", "scene"]

    run Function(dev_scene_nav_start, "sm_test_posterize_scene")
    pause 0.5
    python hide:
        ## Зерно поверх сцены: для чистых пикселей гасим его накопитель.
        store.fx_noise_strength = 0.0
        _fx_state["noise_tension"] = 0.0
        _fx_state["posterize_level"] = 1.0
        fx_cfg_set("posterize.steps", 4)
        fx_cfg_set("posterize.mix", 1.0)
        fx_cfg_set("posterize.gamma", 1.0)
        fx_cfg_set("posterize.enabled", False)
    pause 0.3
    $ renpy.session["_sm_test_raw"] = sm_test_screen_surface()

    $ fx_cfg_set("posterize.scope", scope)
    $ fx_cfg_set("posterize.enabled", True)
    pause 0.3
    $ sm_test_assert_live(renpy.session["_sm_test_raw"], scope)

    $ fx_cfg_set("posterize.enabled", False)
    pause 0.3
    python hide:
        raw = renpy.session.pop("_sm_test_raw")
        errors = python_list()
        for y in (SM_TEST_ROW_MASTER, SM_TEST_ROW_LOCK, SM_TEST_ROW_UI):
            errors += sm_test_swatch_errors(raw, sm_test_screen_surface(), y=y)
        assert not errors, errors

    run MainMenu(confirm=False)

testcase fx_tuner_hotkey:
    if not screen "main_menu":
        run MainMenu(confirm=False)
    assert eval (config.developer and "fxt_hotkey_controller" in config.always_shown_screens)
    $ fx_cfg_set("posterize.steps", 5)

    keysym "K_F10"
    assert screen "fx_tuner" timeout 1.0
    ## Текстовый assert видит только фокусируемые элементы — проверяем кнопки.
    assert "Перечитать файл"
    assert "enabled"
    $ fxt_model.key = "posterize.steps"
    keysym "K_RIGHT"
    assert eval (fx_cfg("posterize.steps") == 6)
    keysym "shift_K_RIGHT"
    assert eval (fx_cfg("posterize.steps") == 16)
    keysym "K_r"
    assert eval (fx_cfg("posterize.steps") == 5)
    keysym "K_b"
    assert eval (fx_cfg_runtime["bypass"])
    keysym "K_b"
    assert eval (not fx_cfg_runtime["bypass"])
    keysym "K_ESCAPE"
    assert not screen "fx_tuner" timeout 1.0

## Ошибки чтения и записи попадают в статус панели и не роняют её отрисовку.
testcase fx_tuner_error_status:
    if not screen "main_menu":
        run MainMenu(confirm=False)
    keysym "K_F10"
    assert screen "fx_tuner" timeout 1.0
    python hide:
        read_file, config_path = store._fxc_read_file, store.fx_cfg_path
        before = fx_cfg("posterize.steps")

        def broken():
            raise FxConfigError("строка 3: блочные списки не поддерживаются, пишите [a, b] {b}")

        try:
            store._fxc_read_file = broken
            fxt_reload()
            assert fxt_model.status.startswith("файл не перечитан") and "[a, b]" in fxt_model.status
            assert fx_cfg("posterize.steps") == before

            ## Цель записи — существующая папка: .tmp пишется, os.replace падает.
            blocked = _sm_test_tempfile.mkdtemp(prefix="sm_fx_blocked_")
            store.fx_cfg_path = lambda blocked=blocked: blocked
            fxt_save()
            assert fxt_model.status.startswith("не сохранено"), fxt_model.status
            assert not _sm_test_os.path.exists(blocked + ".tmp")
            _sm_test_shutil.rmtree(blocked, ignore_errors=True)
            fxt_model.status += " [Errno 13] {i}"
        finally:
            store._fxc_read_file, store.fx_cfg_path = read_file, config_path
    pause 0.5
    assert screen "fx_tuner"
    keysym "K_F10"
    assert not screen "fx_tuner" timeout 1.0
