################################################################################
## Психологическое состояние ГГ (PSY_HP). Глобально на всю игру, попадает в
## сохранения (default). Меняется выборами игрока через psy_hp_change();
## учитывается при выборе концовки.
################################################################################

define PSY_HP_MIN = 0
define PSY_HP_MAX = 100
define PSY_HP_START = 100   # стартовое значение, подгонять по балансу

default PSY_HP = PSY_HP_START

init python:

    def psy_hp_change(delta):
        """Сдвиг PSY_HP на delta (может быть отрицательным) с границами в
        [PSY_HP_MIN, PSY_HP_MAX]. Использовать в сценах: $ psy_hp_change(-10)"""
        store.PSY_HP = max(PSY_HP_MIN, min(PSY_HP_MAX, store.PSY_HP + delta))
