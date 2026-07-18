################################################################################
## Интерактив «наведи и кликни»: невидимые кнопки с попиксельной хит-зоной.
################################################################################

init -5 python:

    ## Образ с подсветкой при наведении: пока store[flag] истинен — светлее
    ## (7dots brightness). Использовать в image-статементах сцен.
    def hover_lit(img, flag, amount=0.35):
        return ConditionSwitch(
            flag, At(img, brightness(amount)),
            True, img,
            predict_all=True)

## items — список (image, transform, flag, return_value). Кнопка полностью
## прозрачна и только ловит курсор: хит-зона — по альфе image (focus_mask),
## наведение пишет флаг (подсветку рисует сам спрайт на master, см. hover_lit),
## клик возвращает return_value. После закрытия экрана флаги гасить вручную —
## unhovered уже не сработает.
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
