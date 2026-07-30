################################################################################
## Dev-утилиты проекта (в prod-сборку не попадают: build.classify game/dev/**).
## Сам Position Tuner лежит в dev/position_tuner/ и от проекта не зависит.
################################################################################

## Удержание кадра: Shift+O → jump dev_hold.
label dev_hold:
    while True:
        pause


## Песочница тюнера: спрайт на чистом фоне, без камеры и параллакса — так
## призрак совпадает с реальным спрайтом пиксель в пиксель. Копировать под
## нужный спрайт. Запуск: Shift+O → jump dev_position_sandbox.
label dev_position_sandbox:

    scene black

    show prologue_hand_right

    show screen position_tuner

    while True:
        pause
