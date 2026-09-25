## QTE: серия направлений, на каждое — окно времени. Поражения нет: промах засчитывается,
## серия доигрывается; итог — число попаданий или "skipped".

## Без стика: вращение даёт все направления за оборот, диагональ — обе оси сразу.
define QTE_BINDINGS = {
    "up": ["K_UP", "pad_dpup_press"],
    "down": ["K_DOWN", "pad_dpdown_press"],
    "left": ["K_LEFT", "pad_dpleft_press"],
    "right": ["K_RIGHT", "pad_dpright_press"],
}
define QTE_PAD_ORDER = ("left", "up", "down", "right")
define QTE_GLYPHS = {"up": "↑", "down": "↓", "left": "←", "right": "→"}
define QTE_ALT = {"up": _("Вверх"), "down": _("Вниз"), "left": _("Влево"), "right": _("Вправо")}

define QTE_TICK_T = 1.0 / 30.0
## Потолок шага часов: игровое меню, H и подвисание съедают не больше этого.
define QTE_MAX_DT = 0.1
## Ряд виден без отсчёта, чтобы игрок прочитал задание.
define QTE_INTRO_T = 0.8
define QTE_OUTRO_T = 0.9

## Выше quick_menu (zorder 100).
define QTE_ZORDER = 110
define QTE_CENTER = (960, 470)
define QTE_STEP = 190
define QTE_CAP = 150
define QTE_BAR_H = 12
define QTE_BAR_GAP = 14
define QTE_HINT_Y = 250
define QTE_PAD_Y = 830
define QTE_COLORS = {
    "pending": "#17131ccc",
    "current": "#3b2f45f0",
    "hit": "#2f5a3af0",
    "miss": "#7a2b2bf0",
}

define QTE_HIT_SOUND = "070_equip_10"
define QTE_MISS_SOUND = "033_denied_03"

default qte_state = {}

init python:

    import time as qte_time

    class QTEClock(NoRollback):
        """Откат и загрузка не должны возвращать чужую метку времени."""

        def __init__(self):
            self.last = None

    qte_clock = QTEClock()

    def qte_start(keys, per_key):
        keys = tuple(keys)
        if not keys or any(k not in QTE_BINDINGS for k in keys):
            raise ValueError("minigame_qte: unknown key ids {!r}".format(keys))
        store.qte_state = {"keys": keys, "per_key": float(per_key), "index": 0,
            "verdicts": (), "phase": "intro", "t": 0.0}
        qte_clock.last = None

    def qte_dt():
        ## monotonic() в Python 3.12 под Windows идёт шагами по 15,6 мс; perf_counter() тоже монотонный.
        now = qte_time.perf_counter()
        last, qte_clock.last = qte_clock.last, now
        if last is None:
            return 0.0
        return min(max(now - last, 0.0), QTE_MAX_DT)

    def qte_hits():
        return store.qte_state.get("verdicts", ()).count("hit")

    def qte_judge(verdict):
        s = store.qte_state
        s["verdicts"] = s["verdicts"] + (verdict,)
        s["index"] += 1
        s["t"] = 0.0
        if s["index"] >= len(s["keys"]):
            s["phase"] = "outro"
        sm_sfx(QTE_HIT_SOUND if verdict == "hit" else QTE_MISS_SOUND)
        renpy.restart_interaction()

    def qte_press(key_id):
        """Action ввода: всегда None, чтобы key поглотил событие и не завершил экран."""
        s = store.qte_state
        if s.get("phase") != "run":
            return None
        expected = s["keys"][s["index"]]
        ## «Простые мини-игры»: чужое направление не засчитывается промахом.
        if key_id != expected and persistent.sm_simplified_locks:
            return None
        qte_judge("hit" if key_id == expected else "miss")
        return None

    def qte_tick():
        """Драйвер модели; не-None завершает call screen числом попаданий."""
        s = store.qte_state
        s["t"] += qte_dt()
        phase = s.get("phase")
        if phase == "intro" and s["t"] >= QTE_INTRO_T:
            s["phase"] = "run"
            s["t"] = 0.0
            renpy.restart_interaction()
        elif phase == "run" and s["t"] >= s["per_key"] and not persistent.sm_simplified_locks:
            qte_judge("miss")
        elif phase == "outro" and s["t"] >= QTE_OUTRO_T:
            return qte_hits()
        return None

    def qte_look(i):
        s = store.qte_state
        verdicts = s.get("verdicts", ())
        if i < len(verdicts):
            return verdicts[i]
        if i == s.get("index") and s.get("phase") == "run":
            return "current"
        return "pending"

    def qte_pos(i, count):
        x = QTE_CENTER[0] + (i - (count - 1) / 2.0) * QTE_STEP
        return (int(round(x)), QTE_CENTER[1])

    def qte_bar_pos(i, count):
        x, y = qte_pos(i, count)
        return (x - QTE_CAP // 2, y + QTE_CAP // 2 + QTE_BAR_GAP)

    def qte_bar_f(trans, st, at):
        s = store.qte_state
        if s.get("phase") == "run" and not persistent.sm_simplified_locks:
            trans.xzoom = max(0.0, 1.0 - s["t"] / s["per_key"])
        else:
            trans.xzoom = 1.0
        return 0

transform qte_bar(pos_xy):
    transform_anchor True
    anchor (0.0, 0.0)
    pos pos_xy
    function qte_bar_f

style qte_glyph is default:
    size 72
    color "#f2ece0"
    align (0.5, 0.5)

style qte_hint is gui_text:
    size 30
    color "#f1e9db"
    xalign 0.5
    textalign 0.5

style qte_pad_button is button:
    xysize (120, 96)
    background Solid("#17131ccc")
    hover_background Solid("#3b2f45f0")

style qte_pad_button_text is button_text:
    size 52
    align (0.5, 0.5)
    color "#f2ece0"
    hover_color "#ffffff"

screen minigame_qte_screen(skippable=False):
    zorder QTE_ZORDER
    modal True
    roll_forward True

    ## Колесо и PgUp посреди свежей серии перезапустили бы её. В пройденной серии (есть данные
    ## прокрутки вперёд) не блокируем: игрок листает назад или вперёд к прежнему итогу.
    ## renpy.in_rollback() не годится: после загрузки оно истинно при первом показе экрана.
    if renpy.roll_forward_info() is None:
        key "rollback" action NullAction()
    for key_id, keysyms in QTE_BINDINGS.items():
        key keysyms action Function(qte_press, key_id)

    if skippable:
        use sm_skippable_interaction

    timer QTE_TICK_T repeat True modal True action Function(qte_tick, _update_screens=False)

    add Solid("#000000aa")

    $ row_keys = qte_state.get("keys", ())
    $ row_phase = qte_state.get("phase")

    if row_phase == "outro":
        $ row_hits = qte_hits()
        $ row_total = len(row_keys)
        text _("Попаданий: [row_hits] из [row_total]") style "qte_hint" ypos QTE_HINT_Y
    elif persistent.sm_simplified_locks and row_phase == "run":
        ## Озвучка и игрок без таймера узнают нужное направление из текста, а не перебором.
        $ row_expected = QTE_ALT[row_keys[qte_state["index"]]]
        text _("Нажмите: [row_expected!t]") style "qte_hint" ypos QTE_HINT_Y
    elif persistent.sm_simplified_locks:
        text _("Стрелки, D-pad или кнопки внизу — в любом темпе") style "qte_hint" ypos QTE_HINT_Y
    else:
        text _("Стрелки, D-pad или кнопки внизу — пока не опустела полоска") style "qte_hint" ypos QTE_HINT_Y

    for i, key_id in enumerate(row_keys):
        $ look = qte_look(i)
        frame:
            id "qte_cap_" + str(i)
            anchor (0.5, 0.5)
            pos qte_pos(i, len(row_keys))
            xysize (QTE_CAP, QTE_CAP)
            background Solid(QTE_COLORS[look])
            text QTE_GLYPHS[key_id] style "qte_glyph" alt QTE_ALT[key_id]
        if look == "current":
            add Solid("#e2cea4", xysize=(QTE_CAP, QTE_BAR_H)) at qte_bar(qte_bar_pos(i, len(row_keys)))

    ## Мышь и тач: та же механика, что у клавиш, а не упрощение.
    hbox:
        xalign 0.5
        ypos QTE_PAD_Y
        spacing 24
        for key_id in QTE_PAD_ORDER:
            textbutton QTE_GLYPHS[key_id]:
                id "qte_pad_" + key_id
                style "qte_pad_button"
                text_style "qte_pad_button_text"
                alt QTE_ALT[key_id]
                action Function(qte_press, key_id)

## Вызов: call minigame_qte(("left", "up", "right"), 1.2) → _return = число попаданий или "skipped".
## Исход идёт в сюжет → пропуск останавливается; без влияния на сюжет — qte_skippable=True.
## Откат: свежую серию колесо не перезапускает; откатившись в пройденную серию, можно листать дальше
## назад или вперёд к прежнему итогу (roll_forward) — как у выбора в меню.
label minigame_qte(qte_keys=("left", "up", "right", "down"), qte_per_key=1.5, qte_skippable=False) hide:
    if qte_skippable and renpy.is_skipping():
        return "skipped"
    if not qte_skippable:
        $ skip_stop()
    $ qte_start(qte_keys, qte_per_key)
    call screen minigame_qte_screen(qte_skippable)
    ## SkipOnce позднего пропуска завершает экран значением True, а не числом.
    if _return is True:
        return "skipped"
    return _return
