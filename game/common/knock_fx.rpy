################################################################################
## Эффект «стук»: расходящиеся звуковые кольца в точке удара — визуализация
## слышимого героем звука (стук в дверь и т.п.).
## Кадры: images/common/knock/knock1.png … knock5.png (600×600, прозрачные,
## центр волны — центр кадра). Вызов: $ knock_at((x, y)).
################################################################################

define KNOCK_FRAMES = 5
define KNOCK_FRAME_T = 0.06                       # длительность кадра
define KNOCK_LIFE = KNOCK_FRAMES * KNOCK_FRAME_T  # полный проигрыш ≈ 0.3 с
define KNOCK_TAGS = 3   # ротация тегов: столько ударов может жить одновременно

## Покадровая анимация без цикла (7dots Ani). effect=None — резкая смена
## кадров без дизолва (рваная анимация). На последнем кадре Ani
## останавливается — остаток гасится альфой в knock_placed.
image knock_fx = Ani("images/common/knock/knock", KNOCK_FRAMES,
    delay=KNOCK_FRAME_T, loop=False, effect=None, ext="png")

## Размещение удара: pos_xy — точка удара (px, центр колец), zoom — масштаб
## эффекта. После проигрыша спрайт гасится и остаётся невидимым до
## переиспользования тега или knock_clear().
transform knock_placed(pos_xy, zoom_k=1.0):
    subpixel True
    anchor (0.5, 0.5)
    pos pos_xy
    zoom zoom_k
    alpha 1.0
    pause KNOCK_LIFE
    alpha 0.0

init python:

    ## Счётчик ротации тегов — служебный, не игровое состояние (префикс "_"
    ## исключает его из сейвов и rollback).
    _knock_seq = 0

    def knock_at(pos_xy, zoom=1.0, zorder=100, layer="master"):
        """Показывает очередной удар стука с центром колец в pos_xy (px, int).

        Удары можно вызывать в темпе стука — они перекрываются: под каждый
        новый удар берётся следующий из KNOCK_TAGS тегов, самый старый
        (уже отыгравший) переиспользуется. Пример:

            $ knock_at((960, 340))
            $ pause(0.4)
            $ knock_at((960, 340), zoom=1.2)
        """
        global _knock_seq
        tag = "knock_fx_{}".format(_knock_seq % KNOCK_TAGS)
        _knock_seq += 1
        renpy.hide(tag, layer=layer)  # сброс ATL при переиспользовании тега
        renpy.show("knock_fx", at_list=[ knock_placed(tuple(pos_xy), zoom) ],
            tag=tag, layer=layer, zorder=zorder)

    def knock_clear(layer="master"):
        """Прячет все спрайты стука; вызывать при уходе со сцены."""
        for i in range(KNOCK_TAGS):
            renpy.hide("knock_fx_{}".format(i), layer=layer)
