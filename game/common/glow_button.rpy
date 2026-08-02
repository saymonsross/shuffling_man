################################################################################
## Кнопка-подсветка: мягкое овальное пятно под надписью. Ни одного ассета —
## овал рисует шейдер sm.oval_glow (common/shaders.rpy). Переиспользуемый
## компонент, вызывать через `use glow_button`.
################################################################################

## Форма ########################################################################

## Базовый холст пятна. Дисплеябль объявляется один раз и растягивается зумом
## под конкретную кнопку: шейдер работает в нормированных координатах, так что
## растяжение не мылит край и не ломает овал.
define GLOW_BASE_SIZE = (400, 200)

## 0.70 — растушёвка в две трети радиуса: остаётся читаемое ядро под текстом и
## длинный мягкий спад, у пятна нет чёткой границы, но форма овала видна.
define GLOW_SOFT = 0.70
define GLOW_CORE = 1.2

## Два варианта ##################################################################

## Пятно одного цвета не работает везде: светлое на бумаге не видно, тёмное в
## тёмной комнате не видно. Поэтому вариант выбирается по фону сцены, под
## которой стоит кнопка, — параметр bg при вызове.
##
##   bg="dark"  — тёмная сцена: пятно светлое, работает как источник света;
##   bg="light" — светлая сцена (бумага, окно): пятно тёмное, работает как
##                мягкая тень под словом.
##
## Цвета нейтральные, чуть тёплые: на выцветшей оливково-коричневой палитре
## игры чистый серый выглядит инородным, а насыщенный даёт цветное пятно.
define GLOW_ON_DARK_COLOR = (0.96, 0.94, 0.89, 1.0)
define GLOW_ON_LIGHT_COLOR = (0.09, 0.08, 0.07, 1.0)

## Потолок плотности: покой и наведение. У светлого пятна выше 0.62 середина
## выбивается в белое и съедает надпись, у тёмного выше 0.85 получается клякса.
## На наведении пятно не «светлеет» буквально, а становится плотнее — для
## тёмного варианта осветление означало бы, наоборот, исчезновение.
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

## Дыхание ######################################################################

## Полупериод: вдох и выдох по столько же, полный цикл — вдвое больше.
define GLOW_BREATH_T = 0.8
## Прирост размера на вдохе. Больше 1.06 читается уже как пульс, а не дыхание.
define GLOW_GROW = 1.06
## Насколько пятно опадает на выдохе — доля от плотности текущего состояния.
define GLOW_BREATH_LOW = 0.65
## Переход между покоем и наведением: короткий, но не мгновенный, чтобы вход
## курсора не сбивал дыхание рывком.
define GLOW_FADE_T = 0.18

## Цикл дыхания вынесен в отдельный трансформ БЕЗ обработчиков on: событие idle
## Ren'Py шлёт кнопке на каждой новой интеракции, и блок с repeat внутри on idle
## перезапускался бы с нуля — пятно застывало на одной фазе. Здесь событий нет,
## а состояние ATL переносится между обновлениями экрана, так что цикл идёт
## непрерывно, сколько бы реплик ни сменилось.
transform glow_breath():
    subpixel True
    alpha 1.0
    zoom 1.0
    block:
        easeout GLOW_BREATH_T alpha 1.0 zoom GLOW_GROW
        easein GLOW_BREATH_T alpha GLOW_BREATH_LOW zoom 1.0
        repeat

## Внешний слой: базовый зум под размер кнопки (xz/yz считаются при вызове) и
## потолок плотности. Альфа перемножается с дыханием, поэтому наведение не гасит
## цикл, а поднимает обе его границы. on idle здесь безобиден — повторный
## linear в ту же цель ничего не двигает.
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

## Надпись ######################################################################

## Светлая с обводкой — единственный вариант, читаемый в обоих режимах: на
## тёмном пятне держит сам цвет, на светлом — обводка.
define GLOW_TEXT_SIZE = 33
define GLOW_TEXT_COLOR = "#f2ece0"
define GLOW_TEXT_HOVER_COLOR = "#ffffff"
define GLOW_TEXT_OUTLINES = [(2, "#1a1712d9", 0, 0)]

style glow_button_text is default:
    font gui.interface_text_font
    size GLOW_TEXT_SIZE
    color GLOW_TEXT_COLOR
    hover_color GLOW_TEXT_HOVER_COLOR
    outlines GLOW_TEXT_OUTLINES
    textalign 0.5

## Компонент ####################################################################

## label     — подпись; action — что делать по клику.
## bg        — какой под кнопкой фон: "light" или "dark" (см. «Два варианта»).
## pos/anchor— положение внутри родительского контейнера (px или доли экрана).
## size      — габариты пятна в пикселях; None — GLOW_BASE_SIZE.
## hovered/unhovered — доп. действия сцены (подсветка предметов и т.п.).
##
## Хит-зона — прямоугольник по size: у мягкого пятна нет видимого края, и
## попиксельная маска по нему ощущалась бы как случайная.
screen glow_button(label, action, bg="dark", pos=(0.5, 0.5), anchor=(0.5, 0.5), size=None, text_size=None, hovered=None, unhovered=None, sensitive=True):

    $ _g_w, _g_h = size or GLOW_BASE_SIZE
    $ _g_xz = _g_w / float(GLOW_BASE_SIZE[0])
    $ _g_yz = _g_h / float(GLOW_BASE_SIZE[1])
    $ _g_on_light = (bg == "light")
    $ _g_img = "glow_oval_on_light" if _g_on_light else "glow_oval_on_dark"
    $ _g_idle = GLOW_ON_LIGHT_IDLE if _g_on_light else GLOW_ON_DARK_IDLE
    $ _g_hover = GLOW_ON_LIGHT_HOVER if _g_on_light else GLOW_ON_DARK_HOVER

    button:
        xysize (_g_w, _g_h)
        xpos pos[0]
        ypos pos[1]
        xanchor anchor[0]
        yanchor anchor[1]

        background None
        sensitive sensitive
        action action
        hovered (hovered or NullAction())
        unhovered (unhovered or NullAction())

        fixed:
            xysize (_g_w, _g_h)
            ## Пятно живёт внутри кнопки — так ATL получает события idle/hover,
            ## но зум дыхания не задевает надпись: масштабировать текст нельзя,
            ## он от передискретизации мылится.
            add _g_img at glow_breath, glow_state(_g_xz, _g_yz, _g_idle, _g_hover)
            text label:
                style "glow_button_text"
                align (0.5, 0.5)
                size (text_size or GLOW_TEXT_SIZE)
