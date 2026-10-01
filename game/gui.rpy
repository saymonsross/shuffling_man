## Инициализация

init offset = -2

init python:
    gui.init(1920, 1080)

define config.check_conflicting_properties = True


## Конфигурируемые Переменные GUI


## Цвета

define gui.accent_color = '#cc0000'

## Заголовки экранов и разделов — приглушённый красный: чистый accent слишком яркий.
define gui.header_color = '#8e1414'

## Фирменный красный для текста на тёмном фоне.
define gui.dark_background_accent = '#b01e1e'

define gui.idle_color = '#888888'

define gui.idle_small_color = '#aaaaaa'

## Наведение — тёмно-красный, а не розовый.
define gui.hover_color = '#b01e1e'

define gui.selected_color = '#ffffff'

define gui.insensitive_color = '#8888887f'

define gui.muted_color = '#510000'
define gui.hover_muted_color = '#7a0000'

define gui.text_color = '#ffffff'
define gui.interface_text_color = '#ffffff'


## Шрифты и их размеры

## В Martian Mono нет ∞, стрелок кроме ←↑→↓ (↺) и геометрических фигур (●, ▸) —
## их рисует DejaVuSans, иначе вместо них пустые квадраты. Диапазоны не должны
## задевать собственные ←↑→↓ U+2190–2193.
define gui.text_font = (
    FontGroup()
    .add("fonts/martian_mono_regular.ttf", None, None)
    .add("DejaVuSans.ttf", 0x2194, 0x21FF)
    .add("DejaVuSans.ttf", 0x221E, 0x221E)
    .add("DejaVuSans.ttf", 0x25A0, 0x25FF)
    )

## {b} берёт настоящее жирное начертание; курсива у шрифта нет, {i} — наклон движка.
init python:
    config.font_replacement_map["fonts/martian_mono_regular.ttf", True, False] = ("fonts/martian_mono_bold.ttf", False, False)
    config.font_replacement_map["fonts/martian_mono_regular.ttf", True, True] = ("fonts/martian_mono_bold.ttf", False, True)

## Реплики (say и NVL) — Fira Sans Condensed Light, {b}/{i} берут настоящие начертания;
## быстрое меню — Regular того же семейства.
define gui.dialogue_text_font = "fonts/fira_sans_condensed_light.ttf"
define gui.quick_button_text_font = "fonts/fira_sans_condensed_regular.ttf"

init python:
    config.font_replacement_map["fonts/fira_sans_condensed_light.ttf", True, False] = ("fonts/fira_sans_condensed_bold.ttf", False, False)
    config.font_replacement_map["fonts/fira_sans_condensed_light.ttf", False, True] = ("fonts/fira_sans_condensed_light_italic.ttf", False, False)
    config.font_replacement_map["fonts/fira_sans_condensed_light.ttf", True, True] = ("fonts/fira_sans_condensed_bold_italic.ttf", False, False)

## Имя говорящего — шрифтом быстрого меню.
define gui.name_text_font = gui.quick_button_text_font

## Интерфейс (меню игры, настройки, сохранения, история) — Fira Sans Condensed Regular,
## как быстрое меню. Стрелок кроме ←↑→↓ ⇦–⇪ и фигур (●, ▸) в нём нет — их рисует
## DejaVuSans; диапазоны обходят собственные глифы Fira (▯ U+25AF, ◊ U+25CA).
define gui.interface_text_font = (
    FontGroup()
    .add("fonts/fira_sans_condensed_regular.ttf", None, None)
    .add("DejaVuSans.ttf", 0x2194, 0x21E5)
    .add("DejaVuSans.ttf", 0x21EB, 0x21FF)
    .add("DejaVuSans.ttf", 0x25A0, 0x25AE)
    .add("DejaVuSans.ttf", 0x25B0, 0x25C9)
    .add("DejaVuSans.ttf", 0x25CB, 0x25FF)
    )

## Заголовки экранов и разделов настроек — тем же шрифтом интерфейса.
define gui.label_text_font = gui.interface_text_font

define gui.text_size = 32

## Реплики (say и NVL) мельче text_size; выборы остаются на text_size.
define gui.dialogue_text_size = 31

## Реплики чуть приглушённее чисто белого интерфейса.
define gui.dialogue_text_color = "#e8e6e1"

define gui.name_text_size = 34

define gui.interface_text_size = 36

define gui.label_text_size = 36

define gui.notify_text_size = 18

define gui.title_text_size = 54


## Главное и игровое меню

define gui.main_menu_background = "#000000"
define gui.game_menu_background = "gui/game_menu.png"

## Логотип с надписью. Для другого языка кладётся game/tl/<язык>/gui/main_menu_logo.png —
## загрузчик Ren'Py сам подменит файл, код не меняется.
define gui.main_menu_logo = "gui/main_menu_logo.png"

define gui.main_menu_font = "fonts/oswald_extralight.ttf"


## Диалог

define gui.textbox_height = 278

define gui.textbox_yalign = 1.0

## Своя полоса быстрого меню под окном диалога; между ними серая линия-разделитель.
## Окно поднято на высоту полосы и толщину линии.
define gui.quick_menu_height = 40
define gui.quick_menu_gap = 2
define gui.quick_menu_line_color = "#2e2e2eb3"

## Контур всплывающих окон (подтверждение, уведомления, рамки) — плотнее, чем у окна
## диалога; штрих у них общий (Border Tuner).
define gui.frame_line_color = "#3d3d3dff"

## Контур окна диалога и полосы тем же цветом и толщиной, что разделитель.
## sides — какие стороны рисовать: t/b/l/r; углы не перекрываются; color — вместо цвета разделителя.
init python:
    def gui_outline(w, h, sides="tblr", color=None, **properties):
        t = gui.quick_menu_gap
        c = color or gui.quick_menu_line_color
        top = t if "t" in sides else 0
        bottom = t if "b" in sides else 0
        parts = []
        if top:
            parts.append(Solid(c, xsize=w, ysize=t))
        if bottom:
            parts.append(Solid(c, ypos=h - t, xsize=w, ysize=t))
        if "l" in sides:
            parts.append(Solid(c, ypos=top, xsize=t, ysize=h - top - bottom))
        if "r" in sides:
            parts.append(Solid(c, xpos=w - t, ypos=top, xsize=t, ysize=h - top - bottom))
        return Fixed(*parts, xsize=w, ysize=h, **properties)


define gui.name_xpos = 358
define gui.name_ypos = -28

define gui.name_xalign = 0.0

define gui.namebox_width = None
define gui.namebox_height = None

define gui.namebox_borders = Borders(18, 6, 18, 6)

define gui.namebox_tile = False


define gui.dialogue_xpos = 402
define gui.dialogue_ypos = 75

define gui.dialogue_width = 1116

define gui.dialogue_text_xalign = 0.0


## Кнопки

define gui.button_width = None
define gui.button_height = None

define gui.button_borders = Borders(6, 6, 6, 6)

define gui.button_tile = False

define gui.button_text_font = gui.interface_text_font

define gui.button_text_size = gui.interface_text_size

## Кнопки интерфейса выглядят как быстрое меню: тот же серый и тонкая тёмная обводка.
define gui.button_text_idle_color = gui.idle_small_color
define gui.button_text_outlines = [(1, "#000000cc", 0, 0)]
define gui.button_text_hover_color = gui.hover_color
define gui.button_text_selected_color = gui.selected_color
define gui.button_text_insensitive_color = gui.insensitive_color

define gui.button_text_xalign = 0.0


define gui.radio_button_borders = Borders(0, 6, 0, 6)

define gui.check_button_borders = Borders(0, 6, 0, 6)

define gui.confirm_button_text_xalign = 0.5

define gui.page_button_borders = Borders(15, 6, 15, 6)

define gui.quick_button_borders = Borders(15, 6, 15, 0)
define gui.quick_button_text_size = 18
define gui.quick_button_text_idle_color = gui.idle_small_color
define gui.quick_button_text_selected_color = gui.dark_background_accent


## Кнопки выбора

define gui.choice_button_width = 1185
define gui.choice_button_height = None
define gui.choice_button_tile = False
define gui.choice_button_borders = Borders(150, 8, 150, 8)
define gui.choice_button_text_font = gui.text_font
define gui.choice_button_text_size = gui.text_size
define gui.choice_button_text_xalign = 0.5
define gui.choice_button_text_idle_color = '#888888'
define gui.choice_button_text_hover_color = "#ffffff"
define gui.choice_button_text_insensitive_color = '#8888887f'


## Кнопки слотов

## Слот ровно под скриншот сохранения (config.thumbnail_*), без полей.
define gui.slot_button_width = 384
define gui.slot_button_height = 216
define gui.slot_button_borders = Borders(0, 0, 0, 0)
define gui.slot_button_text_size = 16
define gui.slot_button_text_xalign = 0.5
define gui.slot_button_text_idle_color = gui.idle_small_color
define gui.slot_button_text_selected_idle_color = gui.selected_color
define gui.slot_button_text_selected_hover_color = gui.hover_color

define config.thumbnail_width = 384
define config.thumbnail_height = 216

define gui.file_slot_cols = 3
define gui.file_slot_rows = 2


## Позиционирование и интервалы

define gui.navigation_xpos = 60

define gui.skip_ypos = 15

define gui.notify_ypos = 68

define gui.choice_spacing = 33

define gui.navigation_spacing = 6

define gui.pref_spacing = 15

define gui.pref_button_spacing = 0

define gui.page_spacing = 0

define gui.slot_spacing = 40

define gui.main_menu_text_xalign = 1.0


## Рамки

define gui.frame_borders = Borders(6, 6, 6, 6)

define gui.confirm_frame_borders = Borders(60, 60, 60, 60)

define gui.skip_frame_borders = Borders(24, 8, 75, 8)

define gui.notify_frame_borders = Borders(24, 8, 60, 8)

define gui.frame_tile = False


## Панели, полосы прокрутки и ползунки

define gui.bar_size = 38
define gui.scrollbar_size = 18
define gui.slider_size = 38

define gui.bar_tile = False
define gui.scrollbar_tile = False
define gui.slider_tile = False

define gui.bar_borders = Borders(6, 6, 6, 6)
define gui.scrollbar_borders = Borders(6, 6, 6, 6)
define gui.slider_borders = Borders(6, 6, 6, 6)

define gui.vbar_borders = Borders(6, 6, 6, 6)
define gui.vscrollbar_borders = Borders(6, 6, 6, 6)
define gui.vslider_borders = Borders(6, 6, 6, 6)

define gui.unscrollable = "hide"


## История

define config.history_length = 250

## None — высота записи по тексту: фиксированная давала огромные пустоты между репликами.
define gui.history_height = None

define gui.history_spacing = 28

define gui.history_name_xpos = 233
define gui.history_name_ypos = 0
define gui.history_name_width = 233
define gui.history_name_xalign = 1.0

define gui.history_text_xpos = 255
define gui.history_text_ypos = 3
define gui.history_text_width = 1110
define gui.history_text_xalign = 0.0


## Режим NVL

define gui.nvl_borders = Borders(0, 15, 0, 30)

define gui.nvl_list_length = 6

define gui.nvl_height = 173

define gui.nvl_spacing = 15

define gui.nvl_name_xpos = 645
define gui.nvl_name_ypos = 0
define gui.nvl_name_width = 225
define gui.nvl_name_xalign = 1.0

define gui.nvl_text_xpos = 675
define gui.nvl_text_ypos = 12
define gui.nvl_text_width = 885
define gui.nvl_text_xalign = 0.0

define gui.nvl_thought_xpos = 360
define gui.nvl_thought_ypos = 0
define gui.nvl_thought_width = 1170
define gui.nvl_thought_xalign = 0.0

define gui.nvl_button_xpos = 675
define gui.nvl_button_xalign = 0.0


## Локализация


define gui.language = "unicode"


## Мобильные устройства

init python:

    @gui.variant
    def touch():

        gui.quick_button_borders = Borders(60, 21, 60, 0)

    @gui.variant
    def small():

        gui.text_size = 45
        gui.name_text_size = 54
        gui.notify_text_size = 38
        gui.interface_text_size = 45
        gui.button_text_size = 45
        gui.label_text_size = 51

        gui.textbox_height = 360
        gui.quick_menu_height = 70
        gui.name_xpos = 120
        gui.dialogue_xpos = 135
        gui.dialogue_width = 1650

        gui.slider_size = 54

        gui.choice_button_width = 1860
        gui.choice_button_text_size = 45

        gui.navigation_spacing = 30
        gui.pref_button_spacing = 15

        gui.history_height = None
        gui.history_text_width = 1035

        gui.quick_button_text_size = 30

        gui.file_slot_cols = 2
        gui.file_slot_rows = 2

        gui.nvl_height = 255

        gui.nvl_name_width = 458
        gui.nvl_name_xpos = 488

        gui.nvl_text_width = 1373
        gui.nvl_text_xpos = 518
        gui.nvl_text_ypos = 8

        gui.nvl_thought_width = 1860
        gui.nvl_thought_xpos = 30

        gui.nvl_button_width = 1860
        gui.nvl_button_xpos = 30
