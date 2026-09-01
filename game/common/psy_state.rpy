## PSY_HP сохраняется и влияет на выбор концовки.

define PSY_HP_MIN = 0
define PSY_HP_MAX = 100
define PSY_HP_START = 100   # стартовое значение, подгонять по балансу

default PSY_HP = PSY_HP_START

init python:

    def psy_hp_change(delta):
        store.PSY_HP = max(PSY_HP_MIN, min(PSY_HP_MAX, store.PSY_HP + delta))
