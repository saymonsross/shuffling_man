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
