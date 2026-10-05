define FX_FLASH_LOW = 0.0
define FX_FLASH_HIGH = 0.30

define FX_FLASH_RISE_T = 0.03
define FX_FLASH_HOLD_T = 0.02
define FX_FLASH_FALL_T = 0.26

define FX_FLASH_FALL_POW = 2.2

define FX_FLASH_COLOR = "#ffffff"

## Аддитивный режим поддерживают не все render paths; безопасный fallback — 0.0.
define FX_FLASH_ADDITIVE = 0.0

init -10 python:

    import time

    ## Runtime-состояние не хранить в trans: restart_interaction пересоздаёт его.
    ## По той же причине фазы считаются от time.time(), а не от сбрасываемого st.
    _flash_req = None
    _flash_cur = None

    def flash_fx(high=None, low=None, rise=None, hold=None, fall=None,
                 fall_pow=None, color=None, additive=None):
        """None берёт FX_FLASH_*; новая вспышка прерывает текущую."""
        global _flash_req, _flash_cur
        if sm_flashes_disabled():
            _flash_req = None
            _flash_cur = None
            return
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
        global _flash_req, _flash_cur
        _flash_req = None
        _flash_cur = None

    def flash_fx_f(trans, st, at):
        """После фаз rise/hold/fall сохраняет alpha на уровне low."""
        global _flash_req, _flash_cur

        if sm_flashes_disabled():
            _flash_req = None
            _flash_cur = None
            trans.alpha = 0.0
            return 0.25

        if _flash_req is not None:
            _flash_cur = _flash_req
            _flash_req = None

        s = _flash_cur
        if s is None:
            trans.alpha = 0.0
            return fx_tick()

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
        return fx_tick()

image fx_flash = Solid("#ffffff")

transform flash_overlay():
    alpha 0.0
    function flash_fx_f

## always_shown сохраняет вспышку при смене master-сцены.
screen fx_flash_screen():
    zorder 100
    add "fx_flash" at flash_overlay

init python:
    config.always_shown_screens.append("fx_flash_screen")
