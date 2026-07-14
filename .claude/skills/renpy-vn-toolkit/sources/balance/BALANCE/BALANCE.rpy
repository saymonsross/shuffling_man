## КАК ПОЛЬЗОВАТЬСЯ:

# просто вызвать метку игры
# call balance

# на входе могут быть параметры, которые обеспечат требуемую сложность
# call balance(time=2, target_width=80, target_xalign=.5, frame_xysize=(600, 80), frame_align=(.5, .5), frame_xpadding=23)

# time - время движения маятника в одну сторону
# target_width - ширина целевой зоны, куда нужно попасть маятником
# target_xalign - положение целевой зоны внутри рамки
# frame_xysize - размеры рамки
# frame_align - положение рамки на экране
# frame_xpadding - горизонтальные отступы внутри рамки

# ширина маятника определяется размерами картинки BALANCE/thumb.png

init:
    # картинка маятника, которая будет двигаться
    image balance_thumb = Image("BALANCE/frame/thumb.png")

init -2 python:
    balance_countdown = "BALANCE/audio/countdown.ogg"

# появление/исчезание
transform balance_show_hide(t=.5):
    alpha 0

    on show:
        linear t alpha 1

    on hide:
        linear t alpha 0

# стиль цифр для последнего отсчёта
style balance_count is text:
    size 222
    bold True
    color "#fff"
    outlines [ (6, "#0234", 0, 0), (4, "#0234", 0, 0), (2, "#0234", 0, 0) ]
    align (.5, .5)

## ДАЛЕЕ ЛУЧШЕ НИЧЕГО НЕ МЕНЯТЬ

init python:
    # аналог with fade, который нельзя прокликать
    # запускается так: $ hard_fade()
    # можно указать цвет и длительность вспышки
    def hard_fade(color="#fff", t=1, hard=True):
        temp = config.dismiss_blocking_transitions
        config.dismiss_blocking_transitions = not hard
        renpy.transition(Fade(t/4, t/2, t/4, color=color))
        renpy.restart_interaction()
        renpy.pause(t, hard=hard)
        config.dismiss_blocking_transitions = temp

# последний отсчёт
label balance_ready:
    # последний отсчёт
    if balance_countdown:
        play sound balance_countdown

    $ i = 3
    while i > 0:
        show expression Text(str(i), style="balance_count") as txt onlayer screens zorder 44:
            truecenter
            zoom 0 rotate 0
            ease .25 zoom 1 rotate 360
            .5
            ease .25 zoom 0 rotate 720
        $ renpy.pause(1, hard=True)
        $ i -= 1
    hide txt onlayer screens

    return

# движение маятника
transform balance_at(x1, x2, t):
    subpixel True
    xpos x1
    ease t xpos x2
    ease t xpos x1
    repeat

# экран с картинкой маятника
screen balance(target_width=50, target_xalign=.5, frame_xysize=(600, 80), frame_align=(.5, .5), frame_xpadding=23):
    zorder 11

    frame:
        style "empty"
        xysize frame_xysize
        align frame_align
        xpadding frame_xpadding

        # рамка
        foreground Frame("BALANCE/frame/foreground.png", 40, 40)

        at balance_show_hide

        # фон
        add Frame("BALANCE/frame/left.png", 40, 40, xysize=(frame_xysize[0], frame_xysize[1])) align(.5, .5)

        # целевая зона
        add Frame("BALANCE/frame/right.png", 40, 40, xysize=(frame_xysize[0], frame_xysize[1])):
            yalign .5
            xpos target_xpos

            at transform:
                crop(frame_xpadding + target_xpos, 0, target_width, 1.)

# вызов игры с параметрами, чтобы задать длительность и сложность
label balance(time=2, target_width=80, target_xalign=.5, frame_xysize=(600, 80), frame_align=(.5, .5), frame_xpadding=23):
    # положение целевой зоны внутри рамки
    $ target_xpos = int((frame_xysize[0] - frame_xpadding * 2 - target_width) * target_xalign)

    # положение фона маятника
    $ left_xpos = int((config.screen_width - frame_xysize[0]) * frame_align[0]) + frame_xpadding

    # положение целевой зоны на экране
    $ xpos = left_xpos + target_xpos

    # показать рамку
    show screen balance(target_width, target_xalign, frame_xysize, frame_align, frame_xpadding)

    # узнать ширину маятника
    $ w, h = renpy.render(renpy.displayable("balance_thumb"), config.screen_width, config.screen_height, 0, 0).get_size()
    $ w = int(w)

    # показать маятник
    show balance_thumb onlayer screens zorder 22 at balance_at(left_xpos, left_xpos + frame_xysize[0] - frame_xpadding * 2 - w, time):
        yalign frame_align[1]

    # последний отсчёт
    call balance_ready

    # начать/закончить игру
    pause

    # остановка маятника
    $ x, y, w, h = renpy.get_image_bounds("balance_thumb", layer="screens")
    $ x = int(x)
    hide balance_thumb onlayer screens zorder 22
    show balance_thumb onlayer screens zorder 22:
        xpos x
        yalign frame_align[1]
    with None

    # проверяем победу
    $ balance_win = x >= xpos and x + w < xpos + target_width

    # чтобы не видно было, как резко сбрасывается время,
    # а заодно понятно было, победа или поражение, показываем вспышки
    if balance_win:
        $ hard_fade()

    else:
        $ hard_fade("#b34")

    $ renpy.pause(1, hard=True)

    hide balance_thumb onlayer screens
    hide screen balance onlayer screens

    $ renpy.pause(.5, hard=True)

    return
