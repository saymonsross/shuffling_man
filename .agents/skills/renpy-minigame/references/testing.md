# Тестирование мини-игры

Каждая мини-игра приходит с testsuite в `game/dev/<имя>_regression_tests.rpy`, и этот testsuite **запущен**. В отчёте
— числа из итога прогона (тест-кейсы и assert-ы). Если пользователь запретил открывать окно игры — прямо напиши, что
тесты не запускались; «проверил скриптом вне движка» тест не заменяет: скрипт не видит экран, ввод, откат, сейв и
пропуск.

## Запуск

Полная проверка и ручной lint — README, раздел «Проверка и запуск». Сверх этого:

- Один testsuite или testcase: `<sdk>/lib/py3-windows-x86_64/python.exe <sdk>/renpy.py <проект> test <имя> --report-detailed`.
- Путь к SDK зависит от машины: если `tools/check_project.ps1` не находит SDK по умолчанию, передай `-SdkPath`.
- Прогон открывает окно игры на секунды — это штатно. Частота кадров в тестах разблокирована (`_test.maximum_framerate`).
- Сравнивай lint с состоянием до правки. На SDK 8.5.0 строгий lint записывает каждый `testcase` в «Unreachable
  Statements» — новые строки этого класса для твоего файла тестов там ожидаемы.
- Тест, падавший до твоей правки, запиши как существующий, а не чини попутно.
- MCP `run_test` — только точечно (правило `renpy_mcp`).

## Структура

```renpy
label sm_test_qte hide:
    call minigame_qte(("left", "right"), 30.0) from _call_sm_test_qte
    $ sm_test_qte_result = _return
    call screen sm_test_qte_finished     # «сторожевой» экран: мини-игра вернула управление
    return

screen sm_test_qte_finished():
    modal True
    null

testsuite minigame_qte_regression:
    testcase happy_path:
        run Function(dev_scene_nav_start, "sm_test_qte")   # full_restart: чистые default
        assert screen "minigame_qte_screen" timeout 3.0
        keysym "K_LEFT"
        assert eval (qte_state["verdicts"] == ("hit",)) timeout 1.0
        assert screen "sm_test_qte_finished" timeout 3.0
        run MainMenu(confirm=False)
```

- Экран мини-игры в тесте показывай через вход-лейбл и `dev_scene_nav_start`; `run Show(...)` поверх главного меню
  тест не завершает.
- Хуки `testsuite global` (`game/dev/testcases.rpy`) сохраняют и возвращают флаги доступности и
  `renpy.get_mouse_pos`; в режимах test/lint запись сейвов и persistent выключена.
- Результат для проверки клади в `default`-переменную; `assert eval (…) timeout N` надёжнее `pause`.
- Условие `assert eval` вычисляется многократно — без побочных эффектов (`get`, а не `pop`).
- Значение, которое сравниваешь до и после отката, храни в `renpy.session`: откат вернёт и store-переменную теста.
- Прокрутку вперёд проверяй `keysym "rollforward"`, а не `run RollForward()`.
- В `game/dev/` не пиши `_()` и реплики: `renpy translate` унесёт их в `game/tl/`, а сборка исключает только `game/dev/`.
- Каждый проверяемый элемент экрана — с `id`; `renpy.get_displayable(screen, id)` даёт доступ к виджету.
- Имена входов, экранов и хелперов тестов — `sm_test_<имя>_…`, как в остальных тестах проекта.

## Обязательный набор

| Проверка | Как |
|---|---|
| Модель: переходы фаз, пороги, исходы | `$ sm_test_<имя>_model()` — функция из `init python` с `assert` |
| Основной путь до конца | DSL до «сторожевого» экрана |
| Промах и таймаут — не поражение | исход есть, игра доиграна |
| Каждое устройство | `parameter device = [...]`: `keysym "K_LEFT"`, `run Function(renpy.queue_event, "pad_dpleft_press")`, `click id "…"`, `drag id "…" to id "…"`; `keysym "pad_…"` теряется, если у окна теста нет фокуса клавиатуры |
| Пропуск | без развилки: `skip fast`, `skip`, `keysym "skip"` и поздний пропуск доводят до `"skipped"`; с исходом — экран остаётся |
| Откат | `run Rollback()` отменяет одно действие; заблокированный `keysym "rollback"` не перезапускает свежий раунд ни сразу, ни после загрузки посреди раунда; из пройденной игры `run Rollback()` + `keysym "rollforward"` возвращают прежний итог. Вход теста ставит жёсткую контрольную точку до игры (сторожевой `call screen`, как `sm_test_qte_ready` в каркасе), иначе откату некуда уйти и проверка блокировки пуста |
| Сейв и загрузка | `run Function(sm_test_cleanup_memory_save)` / `…_load` из `game/dev/cleanup_regression_tests.rpy`: прогресс совпадает с контрольной точкой |
| Click-through (drag) | кнопка-проба под модальным экраном (`sm_test_pointer_leak_target` в `game/dev/testcases.rpy`); `drag … to id "leak_probe" … steps 8`; проба не нажата, захват снят |
| Доступность | `parameter` по `sm_reduce_motion`, `sm_disable_flashes`, `sm_simplified_locks` |
| Долгие ожидания | перемотка часов вместо реального ожидания |

## Приёмы

**Подмены окружения — функцией в `init python`.** В `python`-блоке тест-кейса код исполняется через `exec` с
раздельными globals/locals: lambda и вложенные функции не видят его локальных имён (`NameError`). Подмена — всегда в
`try/finally`:

```python
init python:
    def sm_test_qte_model():
        calls = []
        original = store.sm_sfx
        store.sm_sfx = lambda name, **kwargs: calls.append(name)
        try:
            qte_start(("left",), 1.0)
            ...
            assert calls == [QTE_MISS_SOUND]
        finally:
            store.sm_sfx = original
```

Типичные подмены: `store.splay`/`store.sm_sfx` (запись звуков), `renpy.restart_interaction` (no-op),
`renpy.end_interaction` (сбор результатов), `renpy.get_mouse_pos` (изменяемый список координат),
`renpy.game.interface.mouse_focused` (потеря фокуса окна).

**Перемотка часов.** Настоящий `dt` с потолком, без ожидания:

```python
for _ in range(480):
    qte_clock.last = qte_time.perf_counter() - 0.25
    qte_tick()
```

**Курсор DSL не двигает `renpy.get_mouse_pos()`** — тот читает рендерер. Если UI-клики и hit-test модели должны
видеть один курсор: `renpy.get_mouse_pos = lambda: renpy.test.testmouse.get_mouse_pos(0, 0)` (восстанавливает
глобальный хук).

**Синтетические события для CDD:**

```python
pg = renpy.pygame
down = pg.event.Event(pg.KEYDOWN, key=pg.K_LEFT, mod=0, scancode=0, unicode="", repeat=False)
pad = pg.event.Event(renpy.display.core.EVENTNAME, eventnames=["pad_dpright_press"], controller="test", up=False)
lost = pg.event.Event(pg.ACTIVEEVENT, gain=0, state=3)
try:
    zone.event(down, -1, -1, 0.0)
except renpy.IgnoreEvent:
    pass                                     # событие съедено — значит, обработано
```

**Визуальные инварианты:** `renpy.render_to_surface(...)` и выборка пикселей; непрерывность кадра — сравнение
`renpy.scene_lists().layers["master"]`; звук — `sm_audio_snapshot()`.

## Что остаётся ручной приёмке

Темп, звук на слух, положение на экране, тач на устройстве, реальная раскладка клавиатуры, реальный геймпад
(`keysym "pad_…"` лишь посылает событие). **[проект]** Приёмку делает владелец; в отчёте её отделяют от технических
проверок (`docs/02_owner_review_2026_09_11.md`).
