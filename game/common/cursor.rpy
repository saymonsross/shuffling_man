## Курсор рисует игра, а не система: только так на него ложится процарапанный штрих.
## Своя группа параметров, тюнер — Cursor Tuner в Dev Hub. (1, 1) — остриё треугольника.
## Порог волокон 0: волокна рвали бы заливку треугольника, и курсор просвечивал.
init -10 python:
    scratch_params("cursor", "Курсор", 1.5, 0.0, 1.0, 0.55)

define 1 config.mouse_displayable = MouseDisplayable(
    At("gui/tri_bone_hover.png", scratch("cursor", tint=0.0, pad=8)), 1, 1)
