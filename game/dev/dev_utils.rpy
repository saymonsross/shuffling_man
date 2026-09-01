## Dev-утилиты проекта; game/dev/** исключён из prod-сборки.

## Удержание кадра: Shift+O → jump dev_hold.
label dev_hold:
    while True:
        pause


## Песочница без камеры: Shift+O → jump dev_position_sandbox.
label dev_position_sandbox:

    scene black

    show prologue_hand_right

    show screen position_tuner

    while True:
        pause
