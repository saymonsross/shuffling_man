## Регрессионные тесты RMB Editor: контекст клика, запрос, жест, пауза, перетаскивание.
## Настоящая ссылка не открывается: открыватель, корень запросов и Shift подменены.

default sm_test_rmb_passed = False
default sm_test_rmb_timer_fired = False
default sm_test_rmb_alt = False

## modal-экран, как у мини-игр; alternate — проба штатной ПКМ.
screen sm_test_rmb_idle():
    modal True
    textbutton "RMB PROBE":
        pos (200, 800)
        action NullAction()
        alternate SetVariable("sm_test_rmb_alt", True)

screen sm_test_rmb_timer():
    timer 1.5 action SetVariable("sm_test_rmb_timer_fired", True)

transform sm_test_rmb_shift:
    xoffset 900

label sm_test_rmb_scene:
    scene
    show prologue_hand_right at placed((1358, 468))
    call screen sm_test_rmb_idle
    return

## Две реплики подряд: откат со второй на первую виден по номеру строки сценария.
label sm_test_rmb_say:
    scene black
    "RMB Editor probe line one."
    "RMB Editor probe line two."
    $ sm_test_rmb_passed = True
    call screen sm_test_rmb_idle
    return

## Камера сдвигает слой: нарисованный прямоугольник спрайта расходится с базовым.
label sm_test_rmb_camera:
    scene black
    show expression Solid("#f00", xysize=(100, 100)) as sm_test_rmb_box at placed((100, 100))
    camera at sm_test_rmb_shift
    call screen sm_test_rmb_idle
    return

label sm_test_rmb_pause:
    scene black
    show screen sm_test_rmb_timer
    pause 1.5
    $ sm_test_rmb_passed = True
    call screen sm_test_rmb_idle
    return


init python:

    import os as _sm_rmb_os
    import shutil as _sm_rmb_shutil
    import tempfile as _sm_rmb_tempfile
    import urllib.parse as _sm_rmb_urlparse

    _sm_test_rmb = python_dict(urls=python_list(), root=None, fail=False, dir=None, line=0, changed=None)

    def _sm_test_rmb_opener(url):
        if _sm_test_rmb["fail"]:
            raise Exception("test opener failure")
        _sm_test_rmb["urls"].append(url)

    def sm_test_rmb_begin(shift=True):
        _sm_test_rmb.update(
            urls=python_list(), fail=False, dir=None, line=0,
            changed=set(renpy.python.store_dicts["store"].ever_been_changed))
        if _sm_test_rmb["root"] is None:
            _sm_test_rmb["root"] = _sm_rmb_tempfile.mkdtemp(prefix="rmb_test_")
        _rmb_override.update(opener=_sm_test_rmb_opener, root=_sm_test_rmb["root"], shift=shift)

    def sm_test_rmb_reset():
        _rmb_override.update(opener=None, root=None, shift=None)
        _rmb_run["pending"] = False
        if renpy.session.get("_reload_slot") == "sm_test_rmb_no_such_slot":
            del renpy.session["_reload_slot"]
        rmb_data().update(open=False, text="", files=python_list(), ctx=None, dir=None, error="")
        if _sm_test_rmb["root"] is not None:
            _sm_rmb_shutil.rmtree(_sm_test_rmb["root"], ignore_errors=True)
            _sm_test_rmb["root"] = None

    def _sm_test_rmb_prompt(url):
        assert url.startswith(RMB_URL), url
        return _sm_rmb_urlparse.unquote(url[len(RMB_URL):])

    def _sm_test_rmb_names(ctx):
        return [s["name"].split(" ")[0] for s in ctx["sprites"]]

    def sm_test_rmb_url():
        root = _sm_test_rmb["root"]
        text = "ТЕСТ\nстрока 2 + плюс & амперсанд 100%"
        d = python_dict(
            open=True, text=text, files=python_list(), ctx=rmb_context(), error="",
            dir=_sm_rmb_os.path.join(root, "req_20260930_120000_000"))

        url = rmb_url(d)
        assert "+" not in url[len(RMB_URL):] and "%2B" in url, url
        prompt = _sm_test_rmb_prompt(url)
        assert prompt.startswith(text + "\n\n"), prompt
        assert prompt.endswith("req_20260930_120000_000/request.md"), prompt
        assert "\\" not in prompt.splitlines()[-1], prompt

        d["files"] = python_list(("D:\\a b\\x.wav",))
        assert "- D:\\a b\\x.wav" in _sm_test_rmb_prompt(rmb_url(d))

        ## Бюджет превышен текстом: в ссылке только указатель, всё остальное — в файле.
        d["text"] = "длинный текст " * 300
        url = rmb_url(d)
        prompt = _sm_test_rmb_prompt(url)
        assert len(url) <= RMB_URL_MAX, len(url)
        assert "длинный" not in prompt and "x.wav" not in prompt and "request.md" in prompt, prompt
        request = rmb_request_text(d)
        assert d["text"] in request and "x.wav" in request

        ## Бюджет превышен одними вложениями.
        d["text"] = ""
        d["files"] = python_list("D:\\dir\\file_%03d_длинное_имя.wav" % i for i in range(60))
        prompt = _sm_test_rmb_prompt(rmb_url(d))
        assert "file_000" not in prompt and "request.md" in prompt, prompt
        assert "file_059" in rmb_request_text(d)

        d["files"] = python_list()
        assert _sm_test_rmb_prompt(rmb_url(d)).startswith("Поймано в игре:")
        return True

    def sm_test_rmb_rules():
        lines = ["label _service:", "    pass", "label real_one:", "    pass", "    label .local:", "    pass"]
        assert _rmb_label_at(lines, 2) is None
        assert _rmb_label_at(lines, 6) == "real_one"
        assert _rmb_label_at(lines, 0) is None

        def sprite(lines, more=0):
            return python_dict(name="hero", layer="master", size=(10, 10), lines=lines, lines_more=more)

        def line(path, n, current):
            return python_dict(file=path, line=n, text="show hero", current=current)

        def summary(sprites, at=50):
            return rmb_summary(python_dict(
                sprites=sprites, widgets=python_list(), main_menu=False,
                script=python_dict(file="game/a.rpy", line=at, label="a")))

        ## Строка названа, только если однозначна: ближайшая выше позиции в текущем файле или единственная.
        here = [line("game/a.rpy", 10, True), line("game/a.rpy", 40, True), line("game/a.rpy", 90, True)]
        assert summary([sprite(here)]) == "hero · game/a.rpy:40"
        assert summary([sprite(here)], at=5) == "hero · game/a.rpy:10"
        assert summary([sprite([line("game/b.rpy", 7, False)])]) == "hero · game/b.rpy:7"
        assert summary([sprite([line("game/b.rpy", 7, False), line("game/c.rpy", 9, False)])]) == "hero · слой master"
        assert summary([sprite([line("game/b.rpy", 7, False)], more=3)]) == "hero · слой master"
        assert summary([]) == "game/a.rpy:50"
        return True

    def sm_test_rmb_error_exit():
        """Ошибка внутри контекста поля снимает оба признака: поле не открывается заново."""
        def boom(layers):
            raise RuntimeError("field failure")
        real = store._rmb_field_interact
        rmb_begin(10, 10)
        store._rmb_field_interact = boom
        try:
            try:
                _rmb_enter()
            except RuntimeError:
                pass
            else:
                raise AssertionError("no exception")
        finally:
            store._rmb_field_interact = real
        assert not rmb_data()["open"] and not _rmb_run["active"] and not rmb_deferred_due()
        assert _sm_rmb_os.path.isdir(rmb_data()["dir"])
        return True

    def sm_test_rmb_prune():
        root = _sm_test_rmb["root"]
        keep = _sm_rmb_os.path.join(root, "keep_me")
        _sm_rmb_os.makedirs(keep)
        with _rmb_io.open(_sm_rmb_os.path.join(root, "note.txt"), "w", encoding="utf-8") as f:
            f.write("x")
        made = [_rmb_new_dir() for _i in range(RMB_KEEP + 1)]
        left = sorted(n for n in _sm_rmb_os.listdir(root) if _RMB_REQ_RE.match(n))
        assert len(left) == RMB_KEEP, left
        assert not _sm_rmb_os.path.exists(made[0]) and _sm_rmb_os.path.isdir(made[-1])
        assert _sm_rmb_os.path.isdir(keep) and _sm_rmb_os.path.exists(_sm_rmb_os.path.join(root, "note.txt"))
        _rmb_remove_dir(keep)
        assert _sm_rmb_os.path.isdir(keep)
        return True

    def sm_test_rmb_startfile():
        seen = python_list()
        real = getattr(_rmb_os, "startfile", None)
        saved = _rmb_os.environ.get("ELECTRON_RUN_AS_NODE")
        _rmb_os.environ["ELECTRON_RUN_AS_NODE"] = "1"
        _rmb_os.startfile = lambda url: seen.append((url, "ELECTRON_RUN_AS_NODE" in _rmb_os.environ))
        try:
            _rmb_startfile("vscode://test")
            assert seen == [("vscode://test", False)], seen
            assert _rmb_os.environ.get("ELECTRON_RUN_AS_NODE") == "1"
            ## Под тестами открыватель по умолчанию ничего не запускает.
            _rmb_open_url("vscode://never")
            assert len(seen) == 1
        finally:
            if real is None:
                del _rmb_os.startfile
            else:
                _rmb_os.startfile = real
            if saved is None:
                del _rmb_os.environ["ELECTRON_RUN_AS_NODE"]
            else:
                _rmb_os.environ["ELECTRON_RUN_AS_NODE"] = saved
        return True

    def sm_test_rmb_ctx_scene():
        b = pt_bounds("prologue_hand_right")
        ctx = rmb_context(b[0] + b[2] // 2, b[1] + b[3] // 2)
        assert _sm_test_rmb_names(ctx) == ["prologue_hand_right"], ctx["sprites"]
        s = ctx["sprites"][0]
        assert s["pos"] == (1358, 468) and s["layer"] == "master", s
        hits = [l for l in s["lines"] if l["file"] == "game/0_prologue/prologue_scene.rpy"
                and l["text"].startswith("show prologue_hand_right at placed(")]
        assert hits, s["lines"]
        assert all("\\" not in l["file"] and not l["file"].startswith("game/dev/") for l in s["lines"])
        assert ctx["script"]["file"] == "game/dev/rmb_editor_regression_tests.rpy", ctx["script"]
        assert ctx["script"]["label"] == "sm_test_rmb_scene", ctx["script"]
        assert not ctx["menu"] and not ctx["widgets"], ctx["widgets"]
        ## Строка show не из текущего файла и не единственная — в сводке только слой.
        expect = "prologue_hand_right · слой master"
        if len(s["lines"]) + s["lines_more"] == 1:
            expect = "prologue_hand_right · %s:%d" % (s["lines"][0]["file"], s["lines"][0]["line"])
        assert rmb_summary(ctx) == expect, rmb_summary(ctx)

        empty = rmb_context(5, 5)
        assert empty["sprites"] == [] and empty["point"] == (5, 5), empty
        assert rmb_summary(empty).startswith("game/dev/rmb_editor_regression_tests.rpy:")

        free = rmb_context()
        assert free["point"] is None and free["sprites"] == [] and free["widgets"] == [] and free["script"]
        return True

    def sm_test_rmb_ctx_camera():
        ## Базовый прямоугольник спрайта — 100..200, нарисованный под камерой — 1000..1100.
        drawn = rmb_context(1050, 150)
        base = rmb_context(150, 150)
        assert "sm_test_rmb_box" in _sm_test_rmb_names(drawn), drawn["sprites"]
        assert "sm_test_rmb_box" not in _sm_test_rmb_names(base), base["sprites"]
        bg = rmb_context(1500, 700)
        black = [s for s in bg["sprites"] if s["name"] == "black"]
        assert black and "sm_test_rmb_box" not in _sm_test_rmb_names(bg), bg["sprites"]
        assert any(l["text"].startswith("scene black") for l in black[0]["lines"]), black[0]["lines"]
        return True

    def sm_test_rmb_ctx_menu():
        found = python_list()
        for gx in range(24):
            for gy in range(14):
                ctx = rmb_context(40 + gx * 80, 40 + gy * 75)
                assert ctx["script"] is None and ctx["sprites"] == [], ctx
                found.extend(ctx["widgets"])
        assert found
        assert any(w["file"] in ("game/screens.rpy", "game/main_menu.rpy") and w["line"] > 0 for w in found), found[:5]
        assert all(not w["file"].startswith(("renpy/", "game/dev/")) for w in found)
        assert all(w["screen"] not in RMB_SKIP_SCREENS for w in found)
        return True

    def sm_test_rmb_sent(text):
        assert len(_sm_test_rmb["urls"]) == 1, _sm_test_rmb["urls"]
        prompt = _sm_test_rmb_prompt(_sm_test_rmb["urls"][0])
        assert prompt.startswith(text + "\n\n"), prompt
        d = rmb_data()
        assert d["dir"].startswith(_sm_test_rmb["root"]), d["dir"]
        with _rmb_io.open(_sm_rmb_os.path.join(d["dir"], "request.md"), encoding="utf-8") as f:
            request = f.read()
        assert text in request and "shot.png" in request, request
        shot = d["ctx"]["shot"]
        assert shot and shot["size"] == _rmb_png_size(_sm_rmb_os.path.join(d["dir"], "shot.png")), shot
        assert shot["point"] and ("(%d, %d)" % shot["point"]) in request, request
        assert ("%d×%d" % shot["size"]) in request, request
        return True

    def sm_test_rmb_store_clean():
        """Инструмент не завёл переменных store и не держит состояние в типах, которые откатывает rollback."""
        new = set(renpy.python.store_dicts["store"].ever_been_changed) - _sm_test_rmb["changed"]
        mine = [n for n in new if n.lstrip("_").startswith("rmb")]
        assert not mine, mine
        d = rmb_data()
        ctx = d["ctx"]
        assert type(d) is python_dict and type(d["files"]) is python_list and type(ctx) is python_dict, d
        for key in ("sprites", "widgets", "screens"):
            assert type(ctx[key]) is python_list, (key, type(ctx[key]))
        for item in python_list(ctx["sprites"]) + python_list(ctx["widgets"]):
            assert type(item) is python_dict, type(item)
        for s in ctx["sprites"]:
            assert type(s["lines"]) is python_list and all(type(l) is python_dict for l in s["lines"]), s
        assert type(ctx["script"]) is python_dict and type(ctx["shot"]) is python_dict
        return True


testcase rmb_request:
    $ sm_test_rmb_begin()
    assert eval (config.developer and "rmb_editor_catcher" in config.always_shown_screens)
    assert eval (_rmb_pygame.DROPFILE in config.pygame_events)
    $ sm_test_rmb_url()
    $ sm_test_rmb_rules()
    $ sm_test_rmb_prune()
    $ sm_test_rmb_startfile()

testcase rmb_context_scene:
    $ sm_test_rmb_begin()
    run Function(dev_scene_nav_start, "sm_test_rmb_scene")
    assert screen "sm_test_rmb_idle" timeout 5.0
    pause 0.2
    $ sm_test_rmb_ctx_scene()
    run Function(dev_scene_nav_start, "sm_test_rmb_camera")
    assert screen "sm_test_rmb_idle" timeout 5.0
    pause 0.2
    $ sm_test_rmb_ctx_camera()
    run MainMenu(confirm=False)
    assert screen "main_menu" timeout 5.0
    pause 0.5
    $ sm_test_rmb_ctx_menu()

## Жест в сцене под modal-экраном: поле, отправка, возврат в игру.
testcase rmb_gesture_send:
    $ sm_test_rmb_begin()
    run Function(dev_scene_nav_start, "sm_test_rmb_scene")
    assert screen "sm_test_rmb_idle" timeout 5.0
    pause 0.2
    click "RMB PROBE" button 3
    assert screen "rmb_editor_field" timeout 2.0
    assert eval (_rmb_run["active"] and renpy.context_nesting_level() == 1)
    assert eval (not sm_test_rmb_alt)
    assert eval (rmb_data()["ctx"]["point"] is not None and rmb_data()["ctx"]["script"]["label"] == "sm_test_rmb_scene")

    ## Повторный жест второе поле не открывает.
    click button 3 pos (1400, 500)
    pause 0.2
    assert eval (renpy.context_nesting_level() == 1)

    type "move left"
    assert eval (rmb_data()["text"] == "move left")
    keysym "shift_K_RETURN"
    assert eval (rmb_data()["text"] == "move left\n")
    ## type набирает только US-раскладку: кириллица задаётся через состояние.
    $ rmb_data()["text"] = "ТЕСТ\nстрока 2 + плюс"
    keysym "K_RETURN"
    assert not screen "rmb_editor_field" timeout 2.0
    $ sm_test_rmb_sent("ТЕСТ\nстрока 2 + плюс")
    assert screen "notify" timeout 1.0
    assert eval (renpy.context_nesting_level() == 0 and not renpy.context()._menu and not rmb_data()["open"])
    assert screen "sm_test_rmb_idle"
    $ sm_test_rmb_store_clean()
    run MainMenu(confirm=False)

## После закрытия поля сам жест и Enter отправки не пролистывают реплику под полем.
testcase rmb_gesture_say:
    $ sm_test_rmb_begin()
    run Function(dev_scene_nav_start, "sm_test_rmb_say")
    assert screen "say" timeout 5.0
    pause 0.3
    $ _sm_test_rmb["line"] = renpy.get_filename_line()[1]
    click button 3 pos (960, 300)
    assert screen "rmb_editor_field" timeout 2.0
    keysym "K_RETURN"
    assert not screen "rmb_editor_field" timeout 2.0
    pause 0.5
    assert screen "say"
    assert eval (renpy.get_filename_line()[1] == _sm_test_rmb["line"] and len(_sm_test_rmb["urls"]) == 1)
    $ sm_test_rmb_error_exit()
    pause 0.3
    assert not screen "rmb_editor_field"
    assert eval (renpy.get_filename_line()[1] == _sm_test_rmb["line"])
    run MainMenu(confirm=False)

## Без Shift правая кнопка остаётся штатной: alternate и игровое меню.
testcase rmb_plain_right_click:
    $ sm_test_rmb_begin(False)
    run Function(dev_scene_nav_start, "sm_test_rmb_scene")
    assert screen "sm_test_rmb_idle" timeout 5.0
    pause 0.2
    click "RMB PROBE" button 3
    assert eval (sm_test_rmb_alt) timeout 1.0
    click button 3 pos (1400, 300)
    assert eval (renpy.context()._menu) timeout 2.0
    assert not screen "rmb_editor_field"
    assert eval (not rmb_data()["open"] and not _sm_test_rmb["urls"])
    run MainMenu(confirm=False)

testcase rmb_gesture_menus:
    $ sm_test_rmb_begin()
    if not screen "main_menu":
        run MainMenu(confirm=False)
    assert screen "main_menu" timeout 5.0
    pause 0.5
    click button 3 pos (960, 540)
    assert screen "rmb_editor_field" timeout 2.0
    assert eval (rmb_data()["ctx"]["script"] is None and rmb_data()["ctx"]["sprites"] == [])
    $ _sm_test_rmb["dir"] = rmb_data()["dir"]
    assert eval (_sm_rmb_os.path.isdir(_sm_test_rmb["dir"]))
    $ rmb_data()["text"] = "left over"
    $ rmb_add_file("D:/sounds/left_over.wav")
    keysym "K_ESCAPE"
    assert not screen "rmb_editor_field" timeout 2.0
    assert screen "main_menu"
    ## Esc не оставляет папки запроса и не зовёт открыватель.
    assert eval (not _sm_rmb_os.path.exists(_sm_test_rmb["dir"]) and not _sm_test_rmb["urls"])

    run Function(dev_scene_nav_start, "sm_test_rmb_scene")
    assert screen "sm_test_rmb_idle" timeout 5.0
    keysym "game_menu"
    assert eval (renpy.context()._menu) timeout 2.0
    pause 0.5
    click button 3 pos (960, 540)
    assert screen "rmb_editor_field" timeout 2.0
    assert eval (rmb_data()["ctx"]["menu"] and rmb_data()["ctx"]["sprites"] == [])
    assert eval (rmb_data()["ctx"]["script"]["label"] == "sm_test_rmb_scene")
    ## Следующее открытие — с пустым текстом и без вложений.
    assert eval (rmb_data()["text"] == "" and rmb_data()["files"] == [])
    keysym "K_ESCAPE"
    assert not screen "rmb_editor_field" timeout 2.0
    assert eval (renpy.context()._menu and renpy.context_nesting_level() == 1)
    run MainMenu(confirm=False)

## Пауза как под игровым меню: пока поле открыто, pause и timer базового контекста не срабатывают.
testcase rmb_pause:
    $ sm_test_rmb_begin()
    run Function(dev_scene_nav_start, "sm_test_rmb_pause")
    assert screen "sm_test_rmb_timer" timeout 5.0
    click button 3 pos (960, 540)
    assert screen "rmb_editor_field" timeout 1.0
    pause 2.5
    assert eval (not sm_test_rmb_passed and not sm_test_rmb_timer_fired)
    ## В контексте поля слои сцены очищены: под фоном ничего не исполняется.
    assert eval (not renpy.get_showing_tags("master") and not renpy.get_screen("sm_test_rmb_timer"))
    keysym "K_ESCAPE"
    ## После возврата истёкшие ожидания завершаются сразу — время паузы считается прошедшим.
    assert eval (sm_test_rmb_passed and sm_test_rmb_timer_fired) timeout 2.0
    run MainMenu(confirm=False)

## В контексте поля camera слоя сброшена — её function-трансформы не исполняются; в игре она на месте.
testcase rmb_camera_pause:
    $ sm_test_rmb_begin()
    run Function(dev_scene_nav_start, "sm_test_rmb_camera")
    assert screen "sm_test_rmb_idle" timeout 5.0
    pause 0.2
    assert eval (len(renpy.game.context().scene_lists.camera_list["master"][1]) == 1)
    click button 3 pos (1500, 700)
    assert screen "rmb_editor_field" timeout 2.0
    assert eval (renpy.context_nesting_level() == 1)
    assert eval (all(not v[1] for v in renpy.game.context().scene_lists.camera_list.values()))
    assert eval (all(not v[1] for v in renpy.game.context().scene_lists.layer_at_list.values()))
    keysym "K_ESCAPE"
    assert not screen "rmb_editor_field" timeout 2.0
    assert eval (len(renpy.game.context().scene_lists.camera_list["master"][1]) == 1)
    $ sm_test_rmb_ctx_camera()
    run MainMenu(confirm=False)

## Клавиши и клики не доходят ни до keymap, ни до dev-инструментов.
testcase rmb_no_leak:
    $ sm_test_rmb_begin()
    run Function(dev_scene_nav_start, "sm_test_rmb_say")
    assert screen "say" timeout 5.0
    pause 0.3
    $ _sm_test_rmb["line"] = renpy.get_filename_line()[1]
    advance
    assert eval (renpy.get_filename_line()[1] == _sm_test_rmb["line"] + 1) timeout 3.0
    ## Откат в этой сцене заметен: со второй реплики он возвращает на первую.
    keysym "K_PAGEUP"
    assert eval (renpy.get_filename_line()[1] == _sm_test_rmb["line"]) timeout 3.0
    advance
    assert eval (renpy.get_filename_line()[1] == _sm_test_rmb["line"] + 1) timeout 3.0
    pause 0.3
    click button 3 pos (1400, 300)
    assert screen "rmb_editor_field" timeout 2.0
    keysym "K_TAB"
    keysym "K_PAGEUP"
    keysym "K_F9"
    keysym "K_F12"
    keysym "alt_K_r"
    keysym "skip"
    scroll amount 3 pos (960, 100)
    click pos (30, 30)
    pause 0.3
    assert screen "rmb_editor_field"
    assert not screen "position_tuner"
    assert not screen "dev_hub"
    assert eval (not renpy.is_skipping() and renpy.context_nesting_level() == 1)

    ## Ошибка открывателя: поле остаётся с текстом ошибки и набранным текстом.
    $ _sm_test_rmb["fail"] = True
    $ rmb_data()["text"] = "keep me"
    keysym "K_RETURN"
    pause 0.2
    assert screen "rmb_editor_field"
    $ assert rmb_data()["text"] == "keep me" and "test opener failure" in rmb_data()["error"], repr((rmb_data()["text"], rmb_data()["error"]))
    $ _sm_test_rmb["fail"] = False
    keysym "K_RETURN"
    assert not screen "rmb_editor_field" timeout 2.0
    assert eval (len(_sm_test_rmb["urls"]) == 1 and rmb_data()["error"] == "")
    ## Просочившийся запрос отката движок исполнил бы после возврата.
    pause 0.5
    assert screen "say"
    assert eval (renpy.get_filename_line()[1] == _sm_test_rmb["line"] + 1)
    assert eval (not renpy.context()._menu and not sm_test_rmb_passed)
    run MainMenu(confirm=False)

## Обработчик броска и разблокировка типа события; доставку из Проводника тест не проверяет.
testcase rmb_drop_file:
    $ sm_test_rmb_begin(False)
    run Function(dev_scene_nav_start, "sm_test_rmb_scene")
    assert screen "sm_test_rmb_idle" timeout 5.0
    pause 0.2
    $ _rmb_pygame.event.post(_rmb_pygame.event.Event(_rmb_pygame.DROPFILE, file="D:\\sounds\\one.wav"))
    assert screen "rmb_editor_field" timeout 2.0
    assert eval (rmb_data()["files"] == ["D:\\sounds\\one.wav"])
    assert eval (rmb_data()["ctx"]["point"] is None and rmb_data()["ctx"]["script"]["label"] == "sm_test_rmb_scene")
    $ _rmb_pygame.event.post(_rmb_pygame.event.Event(_rmb_pygame.DROPFILE, file="D:\\sounds\\two.wav"))
    assert eval (rmb_data()["files"] == ["D:\\sounds\\one.wav", "D:\\sounds\\two.wav"]) timeout 2.0
    assert eval (renpy.context_nesting_level() == 1)
    click "×"
    assert eval (rmb_data()["files"] == ["D:\\sounds\\two.wav"]) timeout 1.0
    keysym "K_RETURN"
    assert not screen "rmb_editor_field" timeout 2.0
    assert eval (len(_sm_test_rmb["urls"]) == 1 and "two.wav" in _sm_test_rmb_prompt(_sm_test_rmb["urls"][0]))
    assert eval ("one.wav" not in _sm_test_rmb_prompt(_sm_test_rmb["urls"][0]))
    run MainMenu(confirm=False)

## Состояние после перезагрузки скриптов: признак «открыто» в сессии есть, контекста поля нет.
## Поле возвращается с черновиком, но не во время кадра «Reloading game...».
testcase rmb_reentry:
    $ sm_test_rmb_begin(False)
    run Function(dev_scene_nav_start, "sm_test_rmb_scene")
    assert screen "sm_test_rmb_idle" timeout 5.0
    pause 0.2
    $ renpy.session["_reload_slot"] = "sm_test_rmb_no_such_slot"
    $ rmb_begin(1400, 300, ("D:/sounds/one.wav",))
    $ rmb_data()["text"] = "draft survives"
    $ renpy.restart_interaction()
    pause 0.5
    assert not screen "rmb_editor_field"
    assert eval (rmb_data()["open"] and not _rmb_run["active"])
    $ del renpy.session["_reload_slot"]
    $ renpy.restart_interaction()
    assert screen "rmb_editor_field" timeout 2.0
    assert eval (rmb_data()["text"] == "draft survives" and rmb_data()["files"] == ["D:/sounds/one.wav"])
    assert eval (rmb_data()["ctx"]["point"] == (1400, 300) and renpy.context_nesting_level() == 1)
    keysym "K_ESCAPE"
    assert not screen "rmb_editor_field" timeout 2.0
    pause 0.3
    assert not screen "rmb_editor_field"
    assert eval (not rmb_data()["open"])
    run MainMenu(confirm=False)

testcase rmb_dev_hub:
    $ sm_test_rmb_begin(False)
    run Function(dev_scene_nav_start, "sm_test_rmb_scene")
    assert screen "sm_test_rmb_idle" timeout 5.0
    keysym "K_F12"
    assert screen "dev_hub" timeout 1.0
    click "RMB Editor"
    assert screen "rmb_editor_field" timeout 2.0
    assert not screen "dev_hub"
    assert eval (rmb_data()["ctx"]["point"] is None and not _rmb_run["pending"])
    keysym "K_ESCAPE"
    assert not screen "rmb_editor_field" timeout 2.0
    run MainMenu(confirm=False)
