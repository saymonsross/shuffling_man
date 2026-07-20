################################################################################
## Общие трансформы размещения и движения объектов (пиксельные координаты).
## Перед добавлением новых — проверить, нет ли готового в libs/7dots.rpy.
################################################################################

## Статичное размещение: якорь anchor_xy в точке pos_xy, опциональный поворот.
transform placed(pos_xy, anchor_xy=(0.0, 0.0), angle=None):
    anchor anchor_xy
    pos pos_xy
    rotate angle

## Въезд объекта: движение from_xy → to_xy за t с проявлением и опциональной
## дрожью (object_jitter_f, common/camera_fx.rpy). jitter_key уникален на объект.
transform slide_in(from_xy, to_xy, t=0.9, jitter_amp=0.0, jitter_key="slide_in"):
    anchor (0.0, 0.0)
    pos from_xy
    alpha 0.0
    xoffset 0.0 yoffset 0.0
    parallel:
        ease t alpha 1.0
    parallel:
        ease t pos to_xy
    parallel:
        function renpy.curry(object_jitter_f)(jitter_amp, 0.5, jitter_key)

## Статичное размещение с дрожью (object_jitter_f). jitter_key уникален на
## объект; тем же ключом дрожь бесшовно продолжается между трансформами.
transform placed_jitter(pos_xy, anchor_xy=(0.0, 0.0), jitter_amp=3.0, jitter_key="placed_jitter"):
    anchor anchor_xy
    pos pos_xy
    xoffset 0.0 yoffset 0.0
    function renpy.curry(object_jitter_f)(jitter_amp, 0.5, jitter_key)

## Перемещение уже видимого объекта from_xy → to_xy за t с опциональной дрожью.
transform move_between(from_xy, to_xy, t=0.8, jitter_amp=0.0, jitter_key="move_between"):
    anchor (0.0, 0.0)
    pos from_xy
    xoffset 0.0 yoffset 0.0
    parallel:
        ease t pos to_xy
    parallel:
        function renpy.curry(object_jitter_f)(jitter_amp, 0.5, jitter_key)

init -10 python:

    def _flag_alpha_f(flags, visible_when, relax, trans, st, at):
        active = any(getattr(store, f, False) for f in flags)
        target = 1.0 if active == visible_when else 0.0
        a = getattr(trans, "fx_a", target)
        a += (target - a) * relax
        trans.fx_a = a
        trans.alpha = a
        return 1.0 / 60.0

## Альфа объекта плавно следует за флагами: при visible_when=True объект виден,
## пока поднят хотя бы один из flags (кортеж имён переменных). Пара таких
## трансформов с противоположным visible_when на двух спрайтах даёт кроссфейд поз.
transform flag_fade(pos_xy, flags, visible_when=True, relax=0.15):
    anchor (0.0, 0.0)
    pos pos_xy
    function renpy.curry(_flag_alpha_f)(flags, visible_when, relax)
