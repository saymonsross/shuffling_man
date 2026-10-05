

## Основное


define config.name = _("Шаркающий человек")

## В dev шахматная подложка выявляет прозрачные области; в релизе она отключена.


define gui.show_name = True


define config.version = "0.1.5-demo"


define gui.about = _p("""
""")


define build.name = "shuffling_man"

define config.default_fullscreen = True

## Интервал vsync под 60 кадров: на 165 Гц — 82, на 120/240 — 60. Внутренняя сетка эффектов —
## fx_tick (common/camera_fx.rpy), это предел только для кадров от мыши и ввода.
default preferences.gl_framerate = 60

## Движок после каждой перерисовки рисует ещё столько кадров без ожидания событий; при 12
## они перекрывают такт сетки fx_tick, и цикл отрисовки не отпускает CPU между тактами.
define config.fast_redraw_frames = 0


## Звуки и музыка


define config.has_sound = True
define config.has_music = True
## Озвучка выключена на демо: строки voice в сценах и файлы остаются, True — включить.
define config.has_voice = False
## voice "prologue/work/prologue_01" → game/audio/voice/prologue/work/prologue_01.ogg, как у vplay.
define config.voice_filename_format = "audio/voice/{filename}.ogg"

define config.default_music_volume = 0.85
define config.default_sfx_volume = 0.85
define config.default_voice_volume = 0.85

## Трек главного меню запускает label main_menu (main_menu.rpy), а не config.main_menu_music:
## тот заново включается при каждом full_restart, в том числе при входе в сцену из навигатора.


## Переходы


## Смена экранов интерфейса (вход в меню, переходы между ними, выход) — одна длительность.
define config.enter_transition = Dissolve(0.3)
define config.exit_transition = Dissolve(0.3)


define config.intra_transition = Dissolve(0.3)


define config.after_load_transition = None


define config.end_game_transition = None


## Управление окнами

define config.window = "auto"


define config.window_show_transition = Dissolve(0.3)
define config.window_hide_transition = Dissolve(0.3)

## Окно диалога само прячется на pause, with, scene, hide, call, menu и показе экранов
## (7dots auto_hide). Включается при запуске игры, а не в сцене: иначе вход не с пролога
## (загрузка сейва, dev-старт) оставлял бы окно висеть на паузах.
init python:
    auto_hide()

## Ren'Py по умолчанию не передаёт show/hide внутрь fixed/vbox: трансформы с on show /
## on hide (show_hide) у кнопок и рамок внутри контейнеров экранов иначе не играют.
define config.containers_pass_transform_events = {"hover", "idle", "insensitive", "selected_hover", "selected_idle", "show", "hide"}

## Клавиша F не переключает полноэкранный режим: остаются Alt+Enter и F11.
## Озвучка интерфейса (self voicing) снята с клавиш (V и её варианты): включить её можно
## только осознанно, через меню специальных возможностей Shift+A.
init python:
    config.keymap["toggle_fullscreen"].remove("noshift_K_f")
    config.keymap["self_voicing"] = []
    config.keymap["clipboard_voicing"] = []
    config.keymap["debug_voicing"] = []


## Стандартные настройки


default preferences.text_cps = 45


default preferences.afm_time = 15


## Откат — только в разработке (тесты, dev-инструменты); в дистрибутиве config.developer
## выключен, и колесо/«Назад» не возвращают игрока по сцене.
init 999 python:
    config.rollback_enabled = bool(config.developer)


## Директория сохранений

define config.save_directory = "shuffling_man-1783360448"


## Иконка

define config.window_icon = "gui/window_icon.png"


## Настройка дистрибутива

init python:


    build.classify('**~', None)
    build.classify('**.bak', None)
    build.classify('**/.**', None)
    build.classify('**/#**', None)
    build.classify('**/thumbs.db', None)

    ## Рабочие материалы, диагностика и docs со спойлерами не попадают в релиз.
    build.classify('.agents/**', None)
    build.classify('CLAUDE.md', None)
    build.classify('AGENTS.md', None)
    build.classify('README.md', None)
    build.classify('docs/**', None)
    build.classify('errors.txt', None)
    build.classify('files.txt', None)
    build.classify('image_cache.txt', None)
    build.classify('lint.txt', None)
    build.classify('log.txt', None)
    build.classify('memory.txt', None)
    build.classify('profile_screen.txt', None)
    build.classify('save_dump.txt', None)
    build.classify('text_overflow.txt', None)
    build.classify('trace.txt', None)
    build.classify('traceback.txt', None)

    ## Локальные данные исключаются независимо от .gitignore.
    build.classify('game/cache/**', None)
    build.classify('game/saves/**', None)
    build.classify('tools/**', None)

    ## Dev-инструменты (позиционирование спрайтов и т.п.) — не в дистрибутив.
    build.classify('game/dev/**', None)

    build.documentation('*.html')
    build.documentation('*.txt')
