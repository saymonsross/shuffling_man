################################################################################
## Вспышка: резкий подъём яркости экрана и спад обратно. Визуализация громкого
## звука (стук в дверь и т.п.) — без спрайтов, только свет. Вызов: $ flash_fx().
## Не блокирует сценарий: ставится в один такт с транзишеном тряски (`with ...`).
################################################################################

## Диапазон яркости — доли белого (0.0 — экран как есть, 1.0 — полностью
## засвечен). low — уровень покоя, к которому вспышка спадает и на котором
## остаётся до следующей; high — пик.
define FX_FLASH_LOW = 0.0
define FX_FLASH_HIGH = 0.30

## Времена, сек: rise — нарастание, hold — удержание пика, fall — спад.
define FX_FLASH_RISE_T = 0.03
define FX_FLASH_HOLD_T = 0.02
define FX_FLASH_FALL_T = 0.26

## Кривая спада: 1.0 — линейно, больше — резкий обрыв и длинный тихий хвост.
define FX_FLASH_FALL_POW = 2.2

## Цвет вспышки. Белый — чистая яркость; другой цвет тонирует засветку.
define FX_FLASH_COLOR = "#ffffff"

## Смешивание: 0.0 — обычное наложение (весь кадр равномерно уходит в цвет
## вспышки), 1.0 — аддитивное (чистая прибавка к яркости, светлые места
## выбиваются в белый, тёмные остаются тёмными). Аддитив рисуется не на всех
## рендер-путях (оверлей поверх слоёв) — если вспышка пропала, вернуть 0.0.
define FX_FLASH_ADDITIVE = 0.0

init -10 python:

    import time

    ## Заявка на вспышку (её ставит flash_fx) и текущая проигрываемая вспышка.
    ## Служебное состояние, не игровое: префикс "_" исключает из сейвов и
    ## rollback. Держим здесь, а не в атрибутах trans — по общему правилу
    ## function-трансформов (см. _fx_state в camera_fx.rpy): always_shown-экран
    ## пересобирает обёртку трансформа на каждом restart_interaction, и
    ## python-атрибуты trans теряются. По той же причине время считаем не от
    ## st (он обнуляется вместе с обёрткой), а от независимых часов time.time().
    _flash_req = None
    _flash_cur = None

    def flash_fx(high=None, low=None, rise=None, hold=None, fall=None,
                 fall_pow=None, color=None, additive=None):
        """Одна вспышка: яркость экрана резко идёт от low к high и спадает
        обратно к low.

        Все параметры необязательны — без них берутся константы FX_FLASH_*.
        low/high — доли белого (0.0…1.0), rise/hold/fall — секунды,
        fall_pow — кривая спада. Новая вспышка перебивает недоигравшую.

            $ flash_fx()                          # штатная вспышка
            $ flash_fx(high=0.55, fall=0.4)       # ярче и гаснет дольше
            $ flash_fx(high=0.2, color="#ffdcc0") # тёплая и слабая
        """
        global _flash_req
        _flash_req = {
            "low": _fx_num(low, FX_FLASH_LOW, 0.0, 1.0),
            "high": _fx_num(high, FX_FLASH_HIGH, 0.0, 1.0),
            "rise": _fx_num(rise, FX_FLASH_RISE_T, 0.0),
            "hold": _fx_num(hold, FX_FLASH_HOLD_T, 0.0),
            "fall": _fx_num(fall, FX_FLASH_FALL_T, 0.0),
            "pow": _fx_num(fall_pow, FX_FLASH_FALL_POW, 0.05),
            "additive": _fx_num(additive, FX_FLASH_ADDITIVE, 0.0, 1.0),
            "color": color or FX_FLASH_COLOR,
            "t0": time.time(),
        }

    def flash_off():
        """Гасит вспышку немедленно: экран возвращается к обычной яркости в
        обход спада. Нужно, если уровень покоя low был поднят выше нуля."""
        global _flash_req, _flash_cur
        _flash_req = None
        _flash_cur = None

    def flash_fx_f(trans, st, at):
        """Отрисовка вспышки по фазам rise → hold → fall. После спада вспышка
        не снимается, а остаётся на уровне low: он и есть яркость покоя."""
        global _flash_req, _flash_cur

        if _flash_req is not None:
            _flash_cur = _flash_req
            _flash_req = None

        s = _flash_cur
        if s is None:
            trans.alpha = 0.0
            return 1.0 / 60.0

        e = max(time.time() - s["t0"], 0.0)
        rise, hold, fall = s["rise"], s["hold"], s["fall"]
        if e < rise:
            k = e / rise if rise > 0.0 else 1.0
        elif e < rise + hold:
            k = 1.0
        elif e < rise + hold + fall:
            k = (1.0 - (e - rise - hold) / fall) ** s["pow"]
        else:
            k = 0.0

        trans.alpha = s["low"] + (s["high"] - s["low"]) * k
        trans.additive = s["additive"]
        trans.matrixcolor = TintMatrix(s["color"])
        return 1.0 / 60.0

## Белая заливка во весь экран; цвет вспышки доводится тинтом в flash_fx_f.
image fx_flash = Solid("#ffffff")

transform flash_overlay():
    alpha 0.0
    function flash_fx_f

## always_shown: виден всегда и поверх всего, `scene` его не сбрасывает
## (чистит только master) — вспышка переживает смену кадра и не зависит от
## камерных трансформов сцены.
screen fx_flash_screen():
    zorder 100
    add "fx_flash" at flash_overlay

init python:
    config.always_shown_screens.append("fx_flash_screen")
