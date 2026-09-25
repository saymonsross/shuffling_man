# Постеризация, сквозной FX-конфиг и девкит — план

**Цель:** шейдер постеризации в игре, его параметры правятся вживую (F10) и сохраняются в проектный YAML; Dev Hub (F12) собирает все dev-инструменты.

**Стек:** Ren'Py 8.5 (локально SDK 8.5.0), GLSL shader parts, `config.layer_transforms`, screen language.

## Проблема

Автор принёс Unity-шейдер постеризации (`floor(c*s)/(s-1)`, параметр `_steps = 5`). Нужно встроить его в игру так, чтобы вид эффекта подбирался во время игры и сохранялся для всего проекта, а сцены могли управлять интенсивностью по сюжету («распад реальности»). Dev-инструменты разрознены: F9 — Position Tuner, «Сцены» — в меню, песочницы — через консоль.

## Требования

- R1. `sm.posterize` даёт ровно `steps` уровней на канал при `gamma = 1` (формула Unity + clamp), сохраняет альфу и корректен для premultiplied-текстур; `mix = 0` — кадр идентичен исходнику.
- R2. Глобальный эффект: охват `scene` — все слои мира (`config.layers` без UI-слоёв; сейчас `master` и `lockgame`), UI чистый; охват `screen` — весь экран с UI. Охват, вкл/выкл и параметры меняются на лету без перезапуска.
- R3. Выключенный/неактивный эффект не добавляет проход рендера (`mesh` снят).
- R4. `default fx_posterize_strength` (0..1) — множитель от сцены, переход сглажен через `_fx_step` (правило function-transform-state).
- R5. Значения эффектов живут в `game/fx_config.yaml`; читаются при старте и в релизе; не попадают в сейвы/rollback; мусорные значения → дефолт/clamp; запись файла — только при `config.developer`.
- R6. F10 — FX Tuner: правка всех зарегистрированных параметров, маркер несохранённого, сохранить (F5)/перечитать/откатить, A/B (bypass), превью (игнорировать переменную сцены). UI строится из реестра — новый параметр появляется без правки UI. Ошибки чтения/записи — строка статуса, не падение.
- R7. F12 — Dev Hub: запуск инструментов проекта и встроенных Ren'Py с реальными хоткеями из `config.keymap`, статус (файл:строка, лейбл, игровые переменные эффектов, несохранённые правки).
- R8. Всё dev-only живёт в `game/dev/**` (вырезано из сборки) и не активно без `config.developer`.

## Решения

| # | Решение | Почему | Отклонено |
|---|---|---|---|
| D1 | Глобальный эффект через `config.layer_transforms` (слои + `None`) | Применяется поверх camera-transform, не конфликтует с `camera at` сцен | `camera at` — затирается каждой сценой; always-shown экран-оверлей — не может читать пиксели под собой |
| D2 | Function-transform ставит `mesh`/`shader`/uniforms каждый кадр; неактивный — `mesh False`, `shader None` | Охват и вкл/выкл на лету без мутации `config` после init; без лишнего FBO | Статичный `mesh True` — FBO всегда; смена `config.layer_transforms` в рантайме — нарушает конвенцию |
| D3 | Реестр `fx_param` + собственный парсер/эмиттер подмножества YAML | PyYAML в SDK нет; эмиттер пишет диапазоны и описания в комментарии | Вендорить PyYAML — лишний объём; JSON — пользователь просил YAML |
| D4 | Значения — module-level `python_dict` | Проектная настройка, не игровое состояние: вне rollback и сейвов | `default`/`persistent` — привязали бы вид к сейву/машине |
| D5 | Панели на слое `top`, не modal; мышь над FX Tuner гасит `modal True` у frame (он проверяет только события мыши), Dev Hub — затемнением на весь экран | Охват `screen` не постеризует панели; встроенный keymap (Shift+R, консоль) работает; под FX Tuner игра идёт дальше | modal-экран на `top` — глушит underlay-keymap целиком |
| D6 | `gamma` и `mix` сверх Unity | `mix` — плавные переходы сцен; `gamma > 1` — ступени в тенях для тёмных сцен; `gamma = 1` обходит `pow` и совпадает с Unity | Точный порт без параметров — нет плавности, тёмные сцены схлопываются |
| D7 | Слои охвата `scene` — исключением UI-слоёв (`FX_POSTERIZE_UI_LAYERS`), регистрация на init 999 | Новый слой мира (мини-игры) получает эффект без правки `common/` | Белый список слоёв — общий код знал бы о каждой мини-игре |
| D8 | Сохранение — F5 | Ctrl — клавиша пропуска, движок ловит её раньше экранов: Ctrl+S проматывал бы диалог | Ctrl+S |

## Контекст

- Ren'Py-текстуры premultiplied: un-premultiply → квантование → обратно; `blend normal = (ONE, ONE_MINUS_SRC_ALPHA)`.
- `mesh True` добавляет `renpy.texture` (цвет в `gl_FragColor` на priority 200); своя часть — `fragment_400`.
- `config.layer_transforms[layer]` применяется снаружи camera (`scenelists.transform_layer`), `[None]` — ко всему `layers_root` (без `top`). Трансформ клонируется `a(child=rv)` каждую интеракцию, состояние — через `transform_state`.
- Слой `lockgame` добавляется в `chapter_1_scene_1_minigame_locks.rpy` на init 0 → регистрация эффекта на init 999. Слои, добавленные во время игры (7dots `show_forever` → `forever`), эффект не получают; `forever` — UI.
- Уровни при `steps = 5`: {0, 64, 128, 191, 255} (±1).
- Свободные клавиши: F5, F6, F10, F12. Встроенные: F1 help, F2 progress, F3 performance, F4 image log, F7/F8 profile, F9 — Position Tuner.
- Встроенные действия: `_developer`, `_console.enter`, `_reload_game`, `_launch_editor`, `ToggleScreen("_performance")`, `director.Start()`.
- `config.label_callbacks` — список `f(label, abnormal)`; `renpy.get_filename_line()`.
- Тестовый `keysym "K_F10"` принимает и сырые keysym, и имена keymap.

## Ограничения

- Правила: `function-transform-state` (состояние только в `_fx_state`), `comments`, `rotate-transform-anchor` (не касается), config — только в init.
- Lint `--reserved-parameters`: не называть параметры `layer`, `at`, `st` и т.п.
- Dev-строки панелей не локализуются (прецедент Position Tuner).
- Проверка: `tools/check_project.ps1 -SdkPath D:\Dev\GameDev\RenPy\renpy-8.5.0-sdk`.

## Образцы

- `game/common/camera_fx.rpy` — `_fx_step`, `noise_overlay_f`, `fx_noise_strength` + always-shown экран.
- `game/common/crt_tv.rpy` — регистрация шейдера и ATL с uniforms.
- `game/dev/position_tuner/position_tuner_ui.rpy` — hotkey-controller (always_shown, zorder 1100), стили панели.
- `game/dev/tv_noise_regression_tests.rpy` — pixel-тесты через `renpy.render_to_surface`.

## Что меняется

- `game/common/shaders.rpy` — `sm.posterize`, ATL `posterize(steps, mix, gamma)`.
- `game/common/fx_config.rpy` — реестр и публичный API (`fx_param`, `fx_cfg`, `fx_cfg_*`), парсер, загрузка при init, autoreload-blacklist файла.
- `game/fx_config.yaml` — значения (эффект выключен по умолчанию).
- `game/common/camera_fx.rpy` — параметры постеризации, `fx_posterize_strength`, `posterize_layer`, регистрация в `config.layer_transforms`.
- `game/common/shaders.rpy` — также `posterize_off` для снятия точечного эффекта.
- `game/dev/fx_tuner/fx_tuner.rpy` — эмиттер и атомарная запись YAML, модель панели; `fx_tuner_ui.rpy` — экран F10.
- `game/dev/dev_hub/dev_hub.rpy` — панель F12, трекинг лейбла.
- `game/dev/fx_regression_tests.rpy` — парсер, coercion, round-trip записи, пиксели шейдера по плашкам, режимы слоя, живой кадр (мир/lockgame/UI), хоткеи и статус ошибок тюнера; `dev_hub/dev_hub_tests.rpy` — хаб; хуки `testsuite global` восстанавливают реестр.
- `README.md`, `AGENTS.md` — dev-инструменты, конвенция `fx_param`, эффект постеризации.

## Критерии готовности

- [x] Тесты R1–R3, R5 проходят (pixel-уровни, альфа, `mix = 0`, неактивный охват не меняет кадр, UI чист в охвате `scene`).
- [x] Сохранение → перечитывание даёт те же значения; битый YAML и ошибка записи в тюнере — статус-ошибка, не падение.
- [x] F10/F12 открывают и закрывают панели; хоткеи регистрируются только при `config.developer`.
- [ ] `check_project.ps1` на SDK 8.5.3 — SDK на машине нет. На 8.5.0: compile чистый; strict lint — только «Unreachable Statements» у testcase-блоков, как на HEAD; полный `test global` — 96/97, единственное падение `sm_audio_regression::menu_context_isolation` воспроизведено полным прогоном на чистом HEAD (86/87).
- [x] Ревью агентом `reviewer`.

## Документация

README «Для разработчика»: раздел dev-инструментов (F9/F10/F12, `fx_config.yaml`, добавление параметра), «Визуальные эффекты» — постеризация и `fx_posterize_strength`. AGENTS.md: дерево `dev/`, конвенция `fx_param`.
