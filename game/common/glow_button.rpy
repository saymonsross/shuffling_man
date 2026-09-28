define GLOW_BASE_SIZE = (400, 200)

define GLOW_SOFT = 0.70
define GLOW_CORE = 1.2

define GLOW_ON_DARK_COLOR = (0.96, 0.94, 0.89, 1.0)
define GLOW_ON_LIGHT_COLOR = (0.09, 0.08, 0.07, 1.0)

define GLOW_ON_DARK_IDLE = 0.45
define GLOW_ON_DARK_HOVER = 0.62
define GLOW_ON_LIGHT_IDLE = 0.62
define GLOW_ON_LIGHT_HOVER = 0.82

image glow_oval_on_dark = Transform(
    Solid("#ffffff", xysize=GLOW_BASE_SIZE),
    mesh=True, shader="sm.oval_glow",
    u_glow_color=GLOW_ON_DARK_COLOR, u_glow_soft=GLOW_SOFT, u_glow_core=GLOW_CORE)

image glow_oval_on_light = Transform(
    Solid("#ffffff", xysize=GLOW_BASE_SIZE),
    mesh=True, shader="sm.oval_glow",
    u_glow_color=GLOW_ON_LIGHT_COLOR, u_glow_soft=GLOW_SOFT, u_glow_core=GLOW_CORE)

define GLOW_BREATH_T = 0.8
define GLOW_GROW = 1.06
define GLOW_BREATH_LOW = 0.65
define GLOW_FADE_T = 0.18

## Не переносить repeat в on idle: новая интеракция перезапустит цикл.
transform glow_breath():
    subpixel True
    alpha 1.0
    zoom 1.0
    block:
        easeout GLOW_BREATH_T alpha 1.0 zoom GLOW_GROW
        easein GLOW_BREATH_T alpha GLOW_BREATH_LOW zoom 1.0
        repeat

define GLOW_ALARM_GROW = 1.10
define GLOW_ALARM_LOW = 0.28
define GLOW_ALARM_PAUSE = 0.62

transform glow_alarm():
    subpixel True
    alpha 1.0
    zoom 1.0
    block:
        easeout 0.10 alpha 1.0 zoom GLOW_ALARM_GROW
        easein 0.16 alpha GLOW_ALARM_LOW zoom 1.0
        pause 0.09
        easeout 0.08 alpha 0.95 zoom GLOW_ALARM_GROW
        easein 0.20 alpha GLOW_ALARM_LOW zoom 1.0
        pause GLOW_ALARM_PAUSE
        repeat

## Состояние hover меняет плотность, не перезапуская внутренний цикл.
transform glow_state(xz, yz, idle_a, hover_a):
    subpixel True
    align (0.5, 0.5)
    xzoom xz
    yzoom yz
    alpha idle_a

    on idle:
        linear GLOW_FADE_T alpha idle_a
    on hover:
        linear GLOW_FADE_T alpha hover_a

define GLOW_TEXT_SIZE = 33
define GLOW_TEXT_COLOR = "#f2ece0"
define GLOW_TEXT_HOVER_COLOR = "#ffffff"
define GLOW_TEXT_OUTLINES = [(2, "#1a1712d9", 0, 0)]

## Процарапанный штрих подписи (common/scratch_text.rpy); тюнер — Choice Tuner в Dev Hub.
init -10 python:
    scratch_params("scene_choice_text", "Текст кнопок в сценах", 2.0, 0.3, 1.0, 0.55)

style glow_button_text is default:
    font gui.main_menu_font
    size GLOW_TEXT_SIZE
    color GLOW_TEXT_COLOR
    hover_color GLOW_TEXT_HOVER_COLOR
    outlines GLOW_TEXT_OUTLINES
    textalign 0.5

screen glow_button(label, action, bg="dark", pos=(0.5, 0.5), anchor=(0.5, 0.5), size=None, text_size=None, hovered=None, unhovered=None, sensitive=True, pulse="breath", visual_at=None):

    $ _g_w, _g_h = size or GLOW_BASE_SIZE
    $ _g_xz = _g_w / float(GLOW_BASE_SIZE[0])
    $ _g_yz = _g_h / float(GLOW_BASE_SIZE[1])
    $ _g_on_light = (bg == "light")
    $ _g_img = "glow_oval_on_light" if _g_on_light else "glow_oval_on_dark"
    $ _g_idle = GLOW_ON_LIGHT_IDLE if _g_on_light else GLOW_ON_DARK_IDLE
    $ _g_hover = GLOW_ON_LIGHT_HOVER if _g_on_light else GLOW_ON_DARK_HOVER

    button:
        at show_hide(.25)
        xysize (_g_w, _g_h)
        xpos pos[0]
        ypos pos[1]
        xanchor anchor[0]
        yanchor anchor[1]

        background None
        sensitive sensitive
        action [SPlay("click"), action]
        hovered [SPlay("hover"), (hovered or NullAction())]
        unhovered (unhovered or NullAction())

        fixed:
            at (visual_at if visual_at is not None else [])
            xysize (_g_w, _g_h)
            ## Отдельный add сохраняет ATL-состояние и не масштабирует текст.
            if sm_reduced_motion() or sm_flashes_disabled():
                add _g_img at glow_state(_g_xz, _g_yz, _g_idle, _g_hover)
            elif pulse == "alarm":
                add _g_img at glow_alarm, glow_state(_g_xz, _g_yz, _g_idle, _g_hover)
            else:
                add _g_img at glow_breath, glow_state(_g_xz, _g_yz, _g_idle, _g_hover)
            ## tint 0: обводка и hover-цвет стиля остаются, шейдер только рвёт штрих.
            text label:
                style "glow_button_text"
                align (0.5, 0.5)
                size (text_size or GLOW_TEXT_SIZE)
                at scratch("scene_choice_text", tint=0.0), hover_shake(0.51)
