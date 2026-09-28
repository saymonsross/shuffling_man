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
## pause, with и реплики; промотка (Ctrl, «ПРОПУСК») работает. Меню не блокируются:
## у них свой контекст, а экран проверяет, что игра не в меню.
default click_skip_block = False

screen sm_click_skip_block():
    zorder 1000
    if click_skip_block and not main_menu and not renpy.context()._menu:
        ## Вспышку отказа курсора даёт нажатие кнопки мыши (cursor.rpy), а не этот ключ:
        ## dismiss срабатывает на отпускании.
        key "dismiss" action NullAction()

init python:
    config.overlay_screens.append("sm_click_skip_block")

    ## with и pause слушают клик сами, без экранов: их держит встроенный _dismiss_pause.
    def _sm_click_skip_block_sync():
        store._dismiss_pause = not store.click_skip_block

    config.interact_callbacks.append(_sm_click_skip_block_sync)
