

## Основное


define config.name = _("Шаркающий человек")

## В dev шахматная подложка выявляет прозрачные области; в релизе она отключена.


define gui.show_name = True


define config.version = "0.1.2-demo"


define gui.about = _p("""
""")


define build.name = "shuffling_man"


## Звуки и музыка


define config.has_sound = True
define config.has_music = True
define config.has_voice = True

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

## Ren'Py по умолчанию не передаёт show/hide внутрь fixed/vbox: трансформы с on show /
## on hide (show_hide) у кнопок и рамок внутри контейнеров экранов иначе не играют.
define config.containers_pass_transform_events = {"hover", "idle", "insensitive", "selected_hover", "selected_idle", "show", "hide"}


## Стандартные настройки


default preferences.text_cps = 45


default preferences.afm_time = 15


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
