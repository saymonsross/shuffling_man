# Точка входа. Сценарий глав лежит в папках 0_prologue ... 4_endings;
# сцены связаны цепочкой jump, последняя сцена делает return в главное меню.

default persistent.sm_language_chosen = False

## Первый запуск: выбор языка до главного меню; под test экран не показываем.
label splashscreen:
    ## Язык в persistent обязан быть кодом или None: иначе загрузчик tl-путей падает.
    if _preferences.language is not None and not isinstance(_preferences.language, str):
        $ renpy.change_language(None)

    if persistent.sm_language_chosen or renpy.game.args.command == "test":
        return

    $ sm_parallax_off = True
    scene black

    call screen language_choice_on_start

    ## Return(None) отдаёт True, а не None: русский приходит как True.
    $ renpy.change_language(_return if isinstance(_return, str) else None)
    $ persistent.sm_language_chosen = True

    return

label start:

    ## Трек главного меню идёт на штатном канале music вне пула 7dots — обёртки его не видят.
    $ renpy.music.stop(channel="music", fadeout=3.0)

    ## В меню параллакса нет; без этого он включился бы на растворении и дёрнул кадр меню.
    $ sm_parallax_off = True

    ## Главное меню растворяется в чёрный: переход берёт последний показанный кадр меню.
    scene black
    with Dissolve(0.6)

    ## Dev-старт (dev/scene_navigation/dev_start.rpy): кнопка ▶ плашки главного меню.
    ## В дистрибутиве config.developer выключен, persistent-полей нет.
    if config.developer and renpy.game.args.command != "test" and persistent.sm_dev_start_once:
        ## Флаг гасится до проверки лейбла: иначе он пережил бы сбой и увёл «Новую игру».
        $ persistent.sm_dev_start_once = None
        if renpy.has_label(persistent.sm_dev_start_label or ""):
            ## Параллакс выше гасится до пролога, а его включает пролог — здесь его не будет.
            $ sm_parallax_off = False
            ## Главное меню гасит quick_menu, а входы в середину сцены его не включают.
            $ quick_menu = True
            ## Флаг уже погашен, а persistent откат не возвращает: откат сюда увёл бы в пролог.
            $ renpy.block_rollback()
            jump expression persistent.sm_dev_start_label

    jump prologue_titles
