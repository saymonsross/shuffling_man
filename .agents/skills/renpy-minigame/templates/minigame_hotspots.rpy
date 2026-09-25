## Цели на экране: клик по зоне = одно действие = одна контрольная точка.
## hotspots_ordered=False — собрать все зоны в любом порядке; True — сыграть target по порядку
## (повторы разрешены: фраза, код). Промах не наказывает: прогресс сохраняется.
## spots — кортеж (ключ, displayable, (x, y) int, alt); ключ "done" зарезервирован.
## В режиме сбора target — уникальные ключи: повтор нельзя собрать дважды.

define HOTSPOTS_ZORDER = 110
define HOTSPOTS_DISSOLVE = Dissolve(0.22)
define HOTSPOTS_HOVER_SOUND = "click"
define HOTSPOTS_HIT_SOUND = "070_equip_10"
define HOTSPOTS_MISS_SOUND = "033_denied_03"
define HOTSPOTS_MISS_T = 1.25
define HOTSPOTS_HOVER_LIGHT = 0.18
define HOTSPOTS_HINT_LIGHT = 0.3
define HOTSPOTS_PANEL_Y = 28
define HOTSPOTS_PANEL_W = 760
define HOTSPOTS_DONE_W = 660
define HOTSPOTS_MISS_Y = 980

default hotspots_done = ()
default hotspots_misses = 0
default hotspots_missed = False
default hotspots_outcome = None

init python:

    def hotspots_reset():
        store.hotspots_done = ()
        store.hotspots_misses = 0
        store.hotspots_missed = False
        store.hotspots_outcome = None

    def hotspots_expected(target, ordered):
        """Ключ, который ждёт фраза; None — порядок не важен или всё сыграно."""
        if not ordered or len(store.hotspots_done) >= len(target):
            return None
        return target[len(store.hotspots_done)]

    def hotspots_visible(key, ordered):
        return ordered or key not in store.hotspots_done

    def hotspots_complete(target):
        return len(store.hotspots_done) >= len(target)

    def hotspots_click(target, ordered, key):
        """Засчитывает клик; звук здесь, а не в экране: экран только возвращает ключ."""
        store.hotspots_missed = False
        if store.hotspots_outcome is not None or hotspots_complete(target):
            return None
        if ordered:
            hit = key == hotspots_expected(target, ordered)
        else:
            hit = key in target and key not in store.hotspots_done
        if hit:
            ## Новое значение tuple сохраняется и откатывается вместе с call screen.
            store.hotspots_done += (key,)
            sm_sfx(HOTSPOTS_HIT_SOUND)
            return "hit"
        store.hotspots_misses += 1
        store.hotspots_missed = True
        sm_sfx(HOTSPOTS_MISS_SOUND)
        return "miss"

    def hotspots_finish(target, skipped=False):
        if skipped:
            store.hotspots_done = tuple(target)
            store.hotspots_outcome = "skipped"
        elif hotspots_complete(target):
            store.hotspots_outcome = "done"

style hotspots_text is gui_text:
    color "#f1e9db"
    size 28
    textalign 0.5

screen minigame_hotspots_screen(spots, target, ordered=False, guide=False, skippable=True):
    zorder HOTSPOTS_ZORDER
    modal True
    roll_forward True
    if skippable:
        use sm_skippable_interaction

    $ expected = hotspots_expected(target, ordered)
    ## Нужная зона подсвечивается в режиме guide и на время объяснения промаха.
    $ show_hint = guide or hotspots_missed

    for key, spot, spot_pos, spot_alt in spots:
        if hotspots_visible(key, ordered):
            imagebutton:
                id "hotspots_" + key
                idle (At(spot, brightness(HOTSPOTS_HINT_LIGHT)) if show_hint and key == expected else spot)
                hover At(spot, brightness(HOTSPOTS_HOVER_LIGHT))
                focus_mask spot
                pos spot_pos
                alt spot_alt
                sensitive not hotspots_complete(target)
                hovered SPlay(HOTSPOTS_HOVER_SOUND)
                action Return(key)

    if hotspots_missed:
        timer HOTSPOTS_MISS_T action SetVariable("hotspots_missed", False)
        text _("Не то. Попробуйте ещё раз."):
            id "hotspots_miss_hint"
            style "hotspots_text"
            xalign 0.5
            ypos HOTSPOTS_MISS_Y

    $ done_count = len(hotspots_done)
    $ total_count = len(target)

    frame:
        xalign 0.5
        ypos HOTSPOTS_PANEL_Y
        xsize HOTSPOTS_PANEL_W
        padding (28, 16)
        background Solid("#17131ce6")

        vbox:
            spacing 10

            text _("Прогресс: [done_count] / [total_count]"):
                style "hotspots_text"
                xalign 0.5

            bar:
                id "hotspots_progress"
                value StaticValue(done_count, total_count)
                xfill True
                ysize 14
                left_bar Solid("#e2cea4")
                right_bar Solid("#4c444b")
                thumb None

    ## Игрок видит итог и уходит дальше сам.
    if hotspots_complete(target):
        frame:
            id "hotspots_complete"
            align (0.5, 0.5)
            xsize HOTSPOTS_DONE_W
            padding (36, 28)
            background Solid("#17131cee")
            at show_hide(0.22)

            textbutton _("Продолжить"):
                id "hotspots_continue"
                xalign 0.5
                hovered SPlay(HOTSPOTS_HOVER_SOUND)
                action Return("done")

## Вызов: call minigame_hotspots(SPOTS) — собрать всё; call minigame_hotspots(SPOTS, ("e", "e", "g"), True)
## — фраза по порядку. Возвращает "done" или "skipped".
## По умолчанию пропускается: сбор и фраза обычно без развилки. Если исход меняет состояние игры —
## hotspots_skippable=False.
## Откат: контрольная точка на каждое действие — колесо отменяет одно нажатие.
label minigame_hotspots(hotspots_def, hotspots_target=None, hotspots_ordered=False, hotspots_guide=False, hotspots_skippable=True) hide:
    $ hotspots_target = tuple(hotspots_target or (spot[0] for spot in hotspots_def))
    $ hotspots_reset()
    if not hotspots_skippable:
        $ skip_stop()

    if not (hotspots_skippable and renpy.is_skipping()):
        show screen minigame_hotspots_screen(hotspots_def, hotspots_target, hotspots_ordered, hotspots_guide, hotspots_skippable)
        with HOTSPOTS_DISSOLVE

    while hotspots_outcome is None:
        if hotspots_skippable and renpy.is_skipping():
            $ hotspots_finish(hotspots_target, skipped=True)
        else:
            ## _with_none=False сохраняет кадр для dissolve исчезающей зоны.
            call screen minigame_hotspots_screen(hotspots_def, hotspots_target, hotspots_ordered, hotspots_guide, hotspots_skippable, _with_none=False)
            if _return == "done":
                $ hotspots_finish(hotspots_target)
            elif _return is True:
                $ hotspots_finish(hotspots_target, skipped=True)
            elif hotspots_click(hotspots_target, hotspots_ordered, _return) == "hit" and not hotspots_ordered:
                ## Растворение блокирует ввод: только когда зона действительно исчезает.
                show screen minigame_hotspots_screen(hotspots_def, hotspots_target, hotspots_ordered, hotspots_guide, hotspots_skippable)
                with HOTSPOTS_DISSOLVE

    hide screen minigame_hotspots_screen
    return hotspots_outcome
