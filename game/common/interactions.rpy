## Интерактив «наведи и кликни»: невидимые кнопки с попиксельной хит-зоной.

init -5 python:

    ## Подсветка image-стейтмента по store-флагу.
    def hover_lit(img, flag, amount=0.35):
        return ConditionSwitch(
            flag, At(img, brightness(amount)),
            True, img,
            predict_all=True)

## Только для интерактивов без выбора: пропуск может включиться уже после call screen.
screen sm_skippable_interaction():
    if renpy.is_skipping():
        timer 0.01 action SkipOnce() modal True

## items: (image, transform, flag, return_value). После Hide флаги гасить вручную:
## unhovered закрытого экрана не вызывается.
screen hover_click(items):
    modal True

    for img, tr, flag, val in items:
        imagebutton:
            at tr
            idle Transform(img, alpha=0.0)
            focus_mask img
            hovered SetVariable(flag, True)
            unhovered SetVariable(flag, False)
            action Return(val)

## Блокировщик клика: $ click_skip_block = True — клик, Enter и пробел не проматывают
## pause, with и реплики; промотка (Ctrl, «ПРОПУСК») работает. Это ритм постановки, и
## настройка «Темп сцен» (persistent.sm_author_pacing) даёт игроку его снять.
## $ click_skip_block = "hard" — блок держится при любой настройке: там клик сломал бы
## постановку (рука не доехала, переход позы длиной в паузу, цепочка под звук).
## Игровые меню не блокируются: у них свой контекст. Сценовые кнопки тоже: блокировщик
## выше их и съел бы клик. Окно подтверждения (выход по Alt+F4 и т. п.) открывается в
## контексте игры — его кнопки тоже не блокируются.
default click_skip_block = False
default persistent.sm_author_pacing = True

init -20 python:

    def sm_click_blocked():
        ## statement_callbacks бегут и на init-операторах, до default.
        block = getattr(store, "click_skip_block", False)
        return block == "hard" or bool(block and persistent.sm_author_pacing)

screen sm_click_skip_block():
    zorder 1000
    if sm_click_blocked() and not main_menu and not renpy.context()._menu and not renpy.get_screen("scene_choice") and not renpy.get_screen("confirm"):
        ## Вспышку отказа курсора даёт нажатие кнопки мыши (cursor.rpy), а не этот ключ:
        ## dismiss срабатывает на отпускании.
        key "dismiss" action NullAction()

init python:
    config.overlay_screens.append("sm_click_skip_block")

    ## with и pause слушают клик сами, без экранов: их держит встроенный _dismiss_pause.
    def _sm_click_skip_block_sync():
        store._dismiss_pause = not sm_click_blocked()

    config.interact_callbacks.append(_sm_click_skip_block_sync)
    ## pause читает _dismiss_pause до начала интеракции, а interact_callbacks бегут уже внутри
    ## неё: без синхронизации перед оператором голый pause после заблокированной паузы стал бы
    ## hard-паузой без таймера — клик его не снимает. Поэтому флаг обновляется и перед каждым
    ## оператором.
    config.statement_callbacks.append(lambda statement: _sm_click_skip_block_sync())

    ## auto_hide() из 7dots прячет окно на "call", а вход в меню Ren'Py сам делает
    ## call _enter_game_menu: первое открытие меню растворяло окно диалога отдельно.
    ## Служебные операторы Ren'Py окно не трогают.
    def _sm_window_auto_callback(statement):
        if renpy.get_filename_line()[0].replace("\\", "/").startswith("renpy/common/"):
            return
        _window_auto_callback(statement)

    config.statement_callbacks = [
        _sm_window_auto_callback if cb is _window_auto_callback else cb
        for cb in config.statement_callbacks]
