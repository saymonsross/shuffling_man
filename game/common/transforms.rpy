## transform_anchor не даёт rotate_pad сдвинуть якорь при повороте.
transform placed(pos_xy, anchor_xy=(0.0, 0.0), angle=None):
    transform_anchor True
    anchor anchor_xy
    pos pos_xy
    rotate angle

transform slide_in(from_xy, to_xy, t=0.9, jitter_amp=0.0, jitter_key="slide_in"):
    subpixel True
    anchor (0.0, 0.0)
    pos from_xy
    alpha 0.0
    xoffset 0.0 yoffset 0.0
    parallel:
        ease t alpha 1.0 pos to_xy
    parallel:
        function renpy.curry(object_jitter_f)(jitter_amp, 0.5, jitter_key)

## Одинаковый jitter_key бесшовно продолжает дрожь между трансформами.
transform placed_jitter(pos_xy, anchor_xy=(0.0, 0.0), jitter_amp=3.0, jitter_key="placed_jitter"):
    subpixel True
    anchor anchor_xy
    pos pos_xy
    xoffset 0.0 yoffset 0.0
    function renpy.curry(object_jitter_f)(jitter_amp, 0.5, jitter_key)

init -10 python:

    def _shake_f(power, trans, st, at):
        ## Накопитель привязан к картинке спрайта: она живёт, пока спрайт показан,
        ## а обёртка-трансформ пересоздаётся.
        return object_jitter_f(power, 0.5, "shake_%d" % id(trans.child or trans), trans, st, at)

## Дрожь спрайта поверх его позиции: `at placed(...), shake(1.5)`; power — размах, px.
transform shake(power=1.5):
    subpixel True
    xoffset 0.0 yoffset 0.0
    function renpy.curry(_shake_f)(power)

## Дрожь по наведению для текста кнопки: hover/idle кнопка передаёт вложенным трансформам.
transform hover_shake(power=1.0):
    subpixel True
    on idle, selected_idle, insensitive:
        xoffset 0.0 yoffset 0.0
    on hover, selected_hover:
        function renpy.curry(_shake_f)(power * sm_motion_scale())

transform move_between(from_xy, to_xy, t=0.8, jitter_amp=0.0, jitter_key="move_between"):
    subpixel True
    anchor (0.0, 0.0)
    pos from_xy
    xoffset 0.0 yoffset 0.0
    parallel:
        ease t pos to_xy
    parallel:
        function renpy.curry(object_jitter_f)(jitter_amp, 0.5, jitter_key)

init -10 python:

    def _flag_alpha_f(flags, visible_when, relax, trans, st, at):
        """Хранит alpha в _fx_state между пересборками transform; ключ разделён
        по flags и ветви кроссфейда."""
        active = any(getattr(store, f, False) for f in flags)
        target = 1.0 if active == visible_when else 0.0
        key = "flagfade_" + "|".join(flags) + ("_on" if visible_when else "_off")
        trans.alpha = _fx_step(key, target, relax, start=target)
        return 1.0 / 60.0

transform flag_fade(pos_xy, flags, visible_when=True, relax=0.15):
    anchor (0.0, 0.0)
    pos pos_xy
    function renpy.curry(_flag_alpha_f)(flags, visible_when, relax)
