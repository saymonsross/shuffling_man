## Инициализация

init offset = -1


## Стили

style default:
    properties gui.text_properties()
    language gui.language

style input:
    properties gui.text_properties("input", accent=True)
    adjust_spacing False

style hyperlink_text:
    properties gui.text_properties("hyperlink", accent=True)
    hover_underline True

style gui_text:
    properties gui.text_properties("interface")


style button:
    properties gui.button_properties("button")

style button_text is gui_text:
    properties gui.text_properties("button")
    yalign 0.5

## Звуки интерфейса. Кнопки сцен и мини-игр звучат через SPlay: у них своя логика hover.
style gui_button:
    hover_sound "audio/sfx/hover.ogg"
    activate_sound "audio/sfx/click.ogg"


style label_text is gui_text:
    properties gui.text_properties("label", accent=True)

style prompt_text is gui_text:
    properties gui.text_properties("prompt")


style bar:
    ysize gui.bar_size
    left_bar Frame("gui/bar/left.png", gui.bar_borders, tile=gui.bar_tile)
    right_bar Frame("gui/bar/right.png", gui.bar_borders, tile=gui.bar_tile)

style vbar:
    xsize gui.bar_size
    top_bar Frame("gui/bar/top.png", gui.vbar_borders, tile=gui.bar_tile)
    bottom_bar Frame("gui/bar/bottom.png", gui.vbar_borders, tile=gui.bar_tile)

style scrollbar:
    ysize gui.scrollbar_size
    base_bar Frame("gui/scrollbar/horizontal_[prefix_]bar.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/scrollbar/horizontal_[prefix_]thumb.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)

## Тонкая полоса цветом разделителей, бегунок — цветом заголовков.
style vscrollbar:
    xsize 4
    base_bar Solid(gui.quick_menu_line_color)
    thumb Solid(gui.header_color)

style slider:
    ysize gui.slider_size
    base_bar Frame("gui/slider/horizontal_[prefix_]bar.png", gui.slider_borders, tile=gui.slider_tile)
    thumb "gui/slider/horizontal_[prefix_]thumb.png"

style vslider:
    xsize gui.slider_size
    base_bar Frame("gui/slider/vertical_[prefix_]bar.png", gui.vslider_borders, tile=gui.slider_tile)
    thumb "gui/slider/vertical_[prefix_]thumb.png"


## Все игровые рамки — как окно диалога: заливка и контур со штрихом (ui_frame_border).
style frame:
    padding gui.frame_borders.padding
    background "ui_frame_bg"


## Внутриигровые экраны


## Разговор

screen say(who, what):

    window:
        id "window"

        if who is not None:

            window:
                id "namebox"
                style "namebox"
                text who id "who" at scratch("show_text", tint=0.0, mix=0.49)

        text what id "what"


    if not renpy.variant("small"):
        add SideImage() xalign 0.0 yalign 1.0


init python:
    config.character_id_prefixes.append('namebox')

style window is default
style say_label is default
style say_dialogue is default
style say_thought is say_dialogue

style namebox is default
style namebox_label is say_label


## Контур окна диалога, полосы быстрого меню и разделитель — с процарапанным штрихом
## (common/scratch_text.rpy), своя группа параметров; тюнер — Border Tuner в Dev Hub.
init -5 python:
    scratch_params("ui_border", "Контур окна диалога", 1.5, 0.3, 1.0, 0.55)
    ## Рамки всплывающих окон, слотов сохранения и подчёркивание «ДА/НЕТ» — Frame Tuner.
    scratch_params("ui_frame", "Рамки окон", 1.5, 0.3, 1.0, 0.55)
    scratch_params("quick_menu_text", "Текст быстрого меню", 3.0, 0.3, 1.0, 0.55)

image ui_textbox_border = At(gui_outline(1205, 225, "tlr"), scratch("ui_border", tint=0.0))
image ui_quick_border = At(gui_outline(1205, gui.quick_menu_height, "lrb"), scratch("ui_border", tint=0.0))
## Плашка имени: тот же контур и заливка, что у окна диалога. Frame растягивает контур
## под ширину имени.
image ui_namebox_bg = Fixed(Solid("#000000c7"),
    At(Frame(gui_outline(32, 32), 4, 4, 4, 4), scratch("ui_border", tint=0.0)))
## Контур любого размера: Frame растягивает рамку 32×32, штрих ложится поверх готового размера.
image ui_frame_border = At(Frame(gui_outline(32, 32, color=gui.frame_line_color), 4, 4, 4, 4),
    scratch("ui_frame", tint=0.0))
image ui_frame_bg = Fixed(Solid("#000000c7"), "ui_frame_border")
## Для окон поверх меню: плотная заливка, чтобы кнопки под окном не просвечивали.
image ui_frame_bg_solid = Fixed(Solid("#000000f5"), "ui_frame_border")
## Блёклый контур слотов сохранения — как линии таблицы настроек.
image ui_slot_border = At(Frame(gui_outline(32, 32), 4, 4, 4, 4), scratch("ui_frame", tint=0.0, mix=0.5))
## Наведение на слот — ярче контура всплывающих окон.
image ui_slot_border_hover = At(Frame(gui_outline(32, 32, color="#5c5c5cff"), 4, 4, 4, 4), scratch("ui_frame", tint=0.0))

## Линии таблицы настроек — штрих контура окна диалога вполсилы (mix 0.5); горизонтальные
## шире блока на 4 px с каждой стороны.
image ui_pref_hline = At(Solid(gui.quick_menu_line_color, xsize=1008, ysize=2), scratch("ui_border", tint=0.0, mix=0.5))
image ui_pref_vline = At(Solid(gui.quick_menu_line_color, xsize=2, ysize=56), scratch("ui_border", tint=0.0, mix=0.5))

## Подчёркивание кнопок подтверждения; картинка по имени — стиль вычисляется раньше scratch.
image ui_hover_underline = Transform(At(Solid("#F2EFE940", ysize=2), scratch("ui_frame", tint=0.0)), yalign=1.0)

image ui_quick_divider = At(Solid(gui.quick_menu_line_color, xsize=1205, ysize=gui.quick_menu_gap),
    scratch("ui_border", tint=0.0))

style window:
    xalign 0.5
    xfill True
    yalign gui.textbox_yalign
    yoffset -(gui.quick_menu_height + gui.quick_menu_gap)
    ysize gui.textbox_height

    ## Плашка 1205×225 от x 358, прижата к низу окна; заливка как у полосы быстрого меню,
    ## контур снизу — разделитель. Контур — картинка по имени: стиль вычисляется раньше,
    ## чем объявлен трансформ scratch.
    background Fixed(
        Solid("#000000c7", xpos=358, ypos=gui.textbox_height - 225, xsize=1205, ysize=225),
        Transform("ui_textbox_border", xpos=358, ypos=gui.textbox_height - 225),
        )

## Плашка имени — над окном диалога с зазором 5 px, вровень с его левым краем.
style namebox:
    xpos gui.name_xpos
    xanchor gui.name_xalign
    xsize gui.namebox_width
    ypos (gui.textbox_height - 225 - 5)
    yanchor 1.0
    ysize gui.namebox_height

    background "ui_namebox_bg"
    padding gui.namebox_borders.padding

style say_label:
    properties gui.text_properties("name", accent=True)
    color gui.dialogue_text_color
    xalign gui.name_xalign
    yalign 0.5

style say_dialogue:
    properties gui.text_properties("dialogue")

    xpos gui.dialogue_xpos
    xsize gui.dialogue_width
    ypos gui.dialogue_ypos

    adjust_spacing False

## Ввод

screen input(prompt):
    style_prefix "input"

    window:

        vbox:
            xanchor gui.dialogue_text_xalign
            xpos gui.dialogue_xpos
            xsize gui.dialogue_width
            ypos gui.dialogue_ypos

            text prompt style "input_prompt"
            input id "input"

style input_prompt is default

style input_prompt:
    xalign gui.dialogue_text_xalign
    properties gui.text_properties("input_prompt")

style input:
    xalign gui.dialogue_text_xalign
    xmaximum gui.dialogue_width


## Выбор

screen choice(items):
    style_prefix "choice"

    vbox:
        at show_hide(.25)
        for i in items:
            textbutton i.caption action i.action


style choice_vbox is vbox
style choice_button is button
style choice_button_text is button_text

style choice_vbox:
    xalign 0.5
    ypos 405
    yanchor 0.5

    spacing gui.choice_spacing

style choice_button is default:
    properties gui.button_properties("choice_button")
    hover_sound "audio/sfx/hover.ogg"
    activate_sound "audio/sfx/click.ogg"

style choice_button_text is default:
    properties gui.text_properties("choice_button")


## Выбор-реплика в окне диалога: menu(screen="textbox").

screen textbox(items):
    style_prefix "textbox_choice"

    window:
        style "window"
        ## Окно уже нарисовано, если вопрос остался на экране.
        if renpy.get_screen("say"):
            background None

        vbox:
            at show_hide(.25)
            for i in items:
                textbutton i.caption action i.action

style textbox_choice_vbox is vbox
style textbox_choice_button is choice_button
style textbox_choice_button_text is choice_button_text

## Центр непрозрачной части gui/textbox.png (y 53..278 внутри окна).
style textbox_choice_vbox:
    xpos gui.dialogue_xpos
    xsize gui.dialogue_width
    ypos 166
    yanchor 0.5
    spacing 5

style textbox_choice_button:
    xsize gui.dialogue_width
    padding (24, 4)
    background "#41000079"
    hover_background "#70000079"
    insensitive_background gui.insensitive_color

style textbox_choice_button_text:
    xalign 0.5
    size gui.dialogue_text_size


## Быстрое меню

## Полоса быстрого меню живёт вместе с окном диалога: видна, пока на экране реплика или
## выбор в окне, и уходит вместе с ним (пауза, сценовые кнопки, кино без реплик).
## quick_menu = False прячет её и при открытом окне; во время drag-мини-игры она скрыта
## во избежание click-through.
init python:

    def sm_quick_menu_shown():
        return bool(store.quick_menu and not renpy.get_screen("c1s1_mg_runtime")
            and (renpy.get_screen("say") or renpy.get_screen("textbox")))

screen quick_menu():

    zorder 100

    ## showif, а не if: только он шлёт детям show/hide для растворения.
    showif sm_quick_menu_shown():

        frame:
            at show_hide(.3)
            style "quick_menu_frame"

            hbox:
                style_prefix "quick"
                style "quick_menu"

                use quick_menu_button(_("ИСТОРИЯ"), ShowMenu('history'))
                use quick_menu_button(_("ПРОПУСК"), Skip(), alternate=Skip(fast=True, confirm=True))
                use quick_menu_button(_("АВТО"), Preference("auto-forward", "toggle"))
                use quick_menu_button(_("СОХРАНИТЬ"), ShowMenu('save'))
                use quick_menu_button(_("МЕНЮ"), ShowMenu())

            ## В fira_sans_condensed нет ✕ — только ×.
            button:
                style "quick_hide_button"
                alt _("Скрыть интерфейс")
                action HideInterface()
                text _("×"):
                    style "quick_hide_button_text"
                    at scratch("quick_menu_text"), hover_shake(0.77)

        ## Разделитель между окном диалога и полосой — общая сторона их контуров.
        add "ui_quick_divider":
            at show_hide(.3)
            xpos 358
            yalign 1.0
            yoffset -gui.quick_menu_height


init python:
    config.overlay_screens.append("quick_menu")
    config.overlay_screens.append("quick_menu_stub")

default quick_menu = True

## Пока полосы быстрого меню нет (окно диалога скрыто, quick_menu = False или мини-игра),
## в правом нижнем углу стоит значок — клик открывает игровое меню, как Esc. zorder выше
## модальных экранов мини-игр и блокировщика клика (1000): иначе значок был бы виден, но
## не нажимался.
screen quick_menu_stub():

    zorder 1001

    showif not sm_quick_menu_shown() and not main_menu and not renpy.get_screen("confirm"):

        button:
            at show_hide(.3)
            style "quick_stub_button"
            alt _("Пауза")
            action ShowMenu()
            add Transform("gui/menu_128.png", zoom=0.3):
                at scratch("quick_menu_text"), hover_shake(0.77)

style quick_stub_button is default:
    xalign 1.0
    yalign 1.0
    padding (20, 14)
    background None
    hover_sound "audio/sfx/hover.ogg"
    activate_sound "audio/sfx/click.ogg"

style quick_menu_frame is empty
style quick_menu is hbox
style quick_button is default
style quick_button_text is button_text

## Полоса под окном диалога: высота — gui.quick_menu_height, окно поднято на неё
## и на gui.quick_menu_gap. Ширина — видимая плашка gui/textbox.png (x 358–1563).
## Заливка как у textbox.png; контур — gui_outline.
style quick_menu_frame:
    background Fixed(
        Solid("#000000c7", xsize=1205, ysize=gui.quick_menu_height),
        "ui_quick_border",
        )
    ## Точный xpos, не xalign: 1205 по центру 1920 — это 357.5, и край уезжает на пиксель.
    xpos 358
    xsize 1205
    ysize gui.quick_menu_height
    yalign 1.0

style quick_menu:
    xalign 0.5
    yalign 0.5
    yoffset -2

## Кнопка быстрого меню: штрих и дрожь на тексте; включённый режим (АВТО, ПРОПУСК)
## горит цветом наведения и тёмно-красным контуром 2 px, пока включён.
## Контур — отдельная копия текста под основной: шейдер залил бы обводку цветом текста.
## Сдвиг основного текста (1, 1) центрирует его в контуре — подобран по скриншоту.
screen quick_menu_button(label, action, alternate=None):
    button:
        style "quick_button"
        action action
        alternate alternate
        fixed:
            xfit True
            yfit True
            at hover_shake(0.77), quick_insensitive_dim
            text label:
                style "quick_button_text"
                pos (0, 0) anchor (0, 0)
                color "#0000"
                outlines [(2, "#8e1414", 0, 0)]
                at quick_selected_outline
            text label:
                style "quick_button_text"
                pos (1, 1) anchor (0, 0)
                at scratch("quick_menu_text", selected_lit=True)

## Недоступная кнопка (ПРОПУСК на непрочитанном тексте) — полупрозрачная.
transform quick_insensitive_dim:
    alpha 1.0
    on insensitive:
        linear 0.12 alpha 0.35
    on idle, hover, selected_idle, selected_hover:
        linear 0.12 alpha 1.0

transform quick_selected_outline:
    alpha 0.0
    on idle, hover, insensitive:
        linear 0.12 alpha 0.0
    on selected_idle, selected_hover:
        linear 0.12 alpha 1.0

style quick_button:
    properties gui.button_properties("quick_button")
    hover_sound "audio/sfx/hover.ogg"
    activate_sound "audio/sfx/click.ogg"

## Без обводки: шейдер заливает текст одним цветом, обводка утолщила бы буквы.
style quick_button_text:
    properties gui.text_properties("quick_button")

## Во всю высоту полосы с симметричными отступами: у quick_button отступ только сверху.
style quick_hide_button is quick_button:
    xalign 1.0
    ysize gui.quick_menu_height
    padding (15, 0)

style quick_hide_button_text is quick_button_text:
    size 28
    yalign 0.5


## Главное и игровое меню

## Главное меню
## Кнопки по центру снизу, как в TVARUK_HD. Задник, логотип и трек ставит label main_menu
## (main_menu.rpy).

screen main_menu():

    tag menu

    ## Отрицательный spacing: зазор даёт поле кнопки, промежуток между ними — сверх него.
    vbox:
        align (0.5, 0.87)
        spacing -4

        use main_menu_button(_("НОВАЯ ИГРА"), Start())

        use main_menu_button(_("ЗАГРУЗИТЬ"), ShowMenu("load"))

        use main_menu_button(_("НАСТРОЙКИ"), ShowMenu("preferences"))

        use main_menu_button(_("СОЗДАТЕЛИ"), ShowMenu("about"))

        if renpy.variant("pc"):
            use main_menu_button(_("ВЫХОД"), Quit(confirm=True))

    ## Версия из options.rpy без суффикса «-demo»: слово DEMO стоит перед номером.
    $ main_menu_version = config.version.replace("-demo", "")
    text _("DEMO [main_menu_version]"):
        style "main_menu_version"
        at scratch("main_menu_text", tint=0.0, mix=0.6), alpha(0.81)

    use lang_dropdown


## Список языков для выпадашки главного меню и настроек: (код, самоназвание с ISO-кодом).
## Самоназвания и коды языков не переводятся — вне _().
define lang_dropdown_items = [
    (None, "Русский [[RU]"),
    ("english", "English [[EN]"),
]

transform lang_dd_unfold():
    on show:
        alpha 0.0 yoffset 20
        easeout 0.15 alpha 1.0 yoffset 0
    on hide:
        easein 0.15 alpha 0.0 yoffset 20

screen lang_dropdown():

    default lang_dd_open = False
    $ lang_dd_current = next((item for item in lang_dropdown_items if item[0] == _preferences.language), lang_dropdown_items[0])

    ## Клик мимо списка закрывает его.
    if lang_dd_open:
        button:
            background None
            xfill True
            yfill True
            action SetLocalVariable("lang_dd_open", False)

    frame:
        style "lang_dd_frame"
        background ("ui_frame_bg" if lang_dd_open else None)
        align (1.0, 1.0)
        offset (-6, -6)

        vbox:
            spacing 6

            showif lang_dd_open:
                vbox:
                    spacing 2
                    xalign 1.0
                    at lang_dd_unfold
                    for lang_dd_code, lang_dd_name in lang_dropdown_items:
                        button:
                            style "lang_dd_item"
                            action Language(lang_dd_code), SetLocalVariable("lang_dd_open", False)
                            ## tint 0: шейдер не перекрашивает текст, аутлайн выбранного языка остаётся.
                            text lang_dd_name:
                                style "lang_dd_item_text"
                                at scratch("main_menu_text", tint=0.0), hover_shake(0.77)

            button:
                style "lang_dd_header"
                action ToggleLocalVariable("lang_dd_open")
                hbox:
                    spacing 12
                    xalign 1.0
                    text ("▼" if lang_dd_open else "▲") style "lang_dd_arrow"
                    text lang_dd_current[1]:
                        style "lang_dd_header_text"
                        at scratch("main_menu_text", tint=0.0), hover_shake(0.77)

style lang_dd_frame is frame:
    padding (24, 14, 24, 14)


## Выбор языка при первом запуске (label splashscreen, script.rpy), как в TVARUK_HD.
screen language_choice_on_start():

    vbox:
        align (0.5, 0.5)
        spacing 8

        for lang_code, lang_name in lang_dropdown_items:
            use main_menu_button(lang_name, Return(lang_code))

style lang_dd_item is main_menu_button:
    xalign 1.0

style lang_dd_header is main_menu_button:
    xalign 1.0

style lang_dd_item_text is main_menu_button_text:
    size (gui.button_text_size - 6)
    xalign 1.0
    color "#8A8784"
    hover_color "#F2EFE9"
    selected_idle_color "#8A8784"
    selected_hover_color "#F2EFE9"
    selected_outlines [(2, "#5c0a0a", 0, 0)]

## Открытый список держит кнопку-заголовок в selected: вид не меняется.
style lang_dd_header_text is lang_dd_item_text:
    selected_outlines []

## Oswald без fallback: стрелку рисует интерфейсный шрифт.
style lang_dd_arrow is lang_dd_header_text:
    font gui.interface_text_font
    size 16
    yalign 0.5


## label приходит уже помеченным _(): Text переводит его при показе.
## Шейдер штриха (common/scratch_text.rpy) — только на тексте; hover/idle он получает от кнопки.
## underline — подчёркивание при наведении (окна подтверждения); button_style — свой стиль кнопки.
screen main_menu_button(label, action, underline=False, button_style=None):
    button:
        style (button_style or ("main_menu_button_underlined" if underline else "main_menu_button"))
        action action
        text label:
            style "main_menu_button_text"
            at scratch("main_menu_text"), hover_shake(0.77)

style main_menu_button is gui_button:
    xalign 0.5

## Страница сохранений: открытая подчёркнута красным, как выбранный вариант в настройках.
style main_menu_page_button is main_menu_button:
    selected_foreground Fixed(Solid(gui.accent_color, ysize=2, yalign=1.0))

## При наведении — подчёркивание цветом hover на 25% непрозрачности со штрихом контуров.
style main_menu_button_underlined is main_menu_button:
    hover_foreground Fixed("ui_hover_underline")

style main_menu_button_text is gui_button_text:
    font gui.main_menu_font
    size (gui.button_text_size + 7)
    ## Шейдер заливает текст одним цветом: обводка слилась бы с буквами.
    outlines []
    xalign 0.5

## Версия в левом нижнем углу, мелко и приглушённо; отступ как у выпадашки языков справа.
style main_menu_version is default:
    font gui.main_menu_font
    size 16
    color gui.idle_small_color
    align (0.0, 1.0)
    offset (12, -8)


## Меню паузы (Esc в игре), как в TVARUK_HD: затемнение и столбик кнопок в стиле
## главного меню. Подменю, открытые из паузы, возвращаются в неё; открытые из быстрого
## меню — сразу в игру. Признак живёт в контексте меню: каждый вход в меню — новый контекст.

init python:
    _game_menu_screen = "pause_menu"

    def _pause_menu_mark():
        renpy.context().sm_from_pause = True

    def pause_menu_back():
        if not main_menu and getattr(renpy.context(), "sm_from_pause", False):
            return ShowMenu("pause_menu")
        return Return()

screen pause_menu():

    tag menu

    on ("show", "replace") action Function(_pause_menu_mark)

    add Solid("#000000e6")

    vbox:
        align (0.5, 0.5)
        spacing 4

        use main_menu_button(_("ИСТОРИЯ"), ShowMenu("history"))
        use main_menu_button(_("СОХРАНИТЬ"), ShowMenu("save"))
        use main_menu_button(_("ЗАГРУЗИТЬ"), ShowMenu("load"))
        use main_menu_button(_("НАСТРОЙКИ"), ShowMenu("preferences"))
        if _in_replay:
            use main_menu_button(_("ЗАВЕРШИТЬ ПОВТОР"), EndReplay(confirm=True))
        else:
            use main_menu_button(_("ГЛАВНОЕ МЕНЮ"), MainMenu())

        if renpy.variant("pc") or (renpy.variant("web") and not renpy.variant("mobile")):
            use main_menu_button(_("ПОМОЩЬ"), ShowMenu("help"))

        if renpy.variant("pc"):
            use main_menu_button(_("ВЫХОД"), Quit(confirm=True))

        null height 60

        use main_menu_button(_("НАЗАД"), Return())


## Игровое меню

screen game_menu(title, scroll=None, yinitial=0.0, spacing=0):

    style_prefix "game_menu"

    ## В игре фоном служит затемнённая сцена, как у меню паузы.
    if main_menu:
        add gui.main_menu_background at parallax_bg()

    ## Без левой навигации, как в TVARUK_HD: содержимое по центру, «НАЗАД» снизу.
    frame:
        style "game_menu_outer_frame"

        hbox:

            frame:
                style "game_menu_content_frame"

                if scroll == "viewport":

                    viewport:
                        yinitial yinitial
                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        pagekeys True

                        side_yfill True

                        vbox:
                            spacing spacing

                            transclude

                elif scroll == "vpgrid":

                    vpgrid:
                        cols 1
                        yinitial yinitial

                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        pagekeys True

                        side_yfill True

                        spacing spacing

                        transclude

                else:

                    transclude

    vbox:
        align (0.5, 1.0)
        yoffset -30
        use main_menu_button(_("НАЗАД"), pause_menu_back())

    label title

    ## Заголовок экрана доступен Font Picker (F8, dev).
    add sm_font_preview_style("game_menu_label_text")

    if main_menu:
        key "game_menu" action ShowMenu("main_menu")
    else:
        key "game_menu" action pause_menu_back()


style game_menu_outer_frame is empty
style game_menu_content_frame is empty
style game_menu_viewport is gui_viewport
style game_menu_side is gui_side
style game_menu_scrollbar is gui_vscrollbar

style game_menu_label is gui_label
style game_menu_label_text is gui_label_text


style game_menu_outer_frame:
    bottom_padding 120
    top_padding 180

    ## Затемнение на весь экран, как у меню паузы.
    background Solid("#000000e6")
    xfill True
    yfill True

## xfill — содержимое может встать по центру экрана (xalign 0.5), как «НАЗАД» и заголовок.
style game_menu_content_frame:
    left_margin 255
    right_margin 255
    top_margin 15
    xfill True

style game_menu_viewport:
    xsize 1380

style game_menu_vscrollbar:
    unscrollable gui.unscrollable

style game_menu_side:
    spacing 15

style game_menu_label:
    xalign 0.5
    ysize 180

## Заголовок экрана: шрифт и цвет заголовков категорий настроек.
style game_menu_label_text:
    font "fonts/sofia_sans_condensed_regular.ttf"
    size 75
    color gui.header_color
    yalign 0.5


## Об игре

## Титры: (роль, имена). Имена в _(): для другого языка транслитерируются.
define about_credits = [
    (_("Разработчик"), [_("Hinterland Mood")]),
    (_("Автор рассказа"), [_("Роман «Chainsaw» Черный")]),
    (_("Художник"), [_("Надежда Певунова")]),
    (_("Сценарий"), [_("Данила Ромах")]),
    (_("Музыка и звук"), [_("REDCHINAWAVE")]),
    (_("Особая благодарность"), [_("Сергей Паршин")]),
]

screen about():

    tag menu

    use game_menu(_("СОЗДАТЕЛИ")):

        style_prefix "about"

        vbox:
            xfill True
            spacing 36

            for about_role, about_names in about_credits:
                vbox:
                    xfill True
                    spacing 6
                    text about_role style "about_role"
                    for about_name in about_names:
                        text about_name


style about_text is gui_text

## Как реплики в истории: шрифт и цвет окна диалога.
style about_text:
    font gui.dialogue_text_font
    size gui.dialogue_text_size
    color gui.dialogue_text_color
    xalign 0.5
    textalign 0.5

style about_role is about_text:
    size 26
    color gui.header_color


## Сохранение и загрузка

screen save():

    tag menu

    use file_slots(_("СОХРАНИТЬ"))


screen load():

    tag menu

    use file_slots(_("ЗАГРУЗИТЬ"))


screen file_slots(title):

    ## Подписи страницы нет: открытую страницу показывает подчёркивание в «1 2 3 4 АВТО».
    use game_menu(title):

        fixed:

            order_reverse True

            grid gui.file_slot_cols gui.file_slot_rows:
                style_prefix "slot"

                ## От заголовка, как первая категория в настройках: подписи страницы над слотами нет.
                xalign 0.5
                yalign 0.0
                yoffset 20

                spacing gui.slot_spacing

                for i in range(gui.file_slot_cols * gui.file_slot_rows):

                    $ slot = i + 1

                    ## Слот — кубик под скриншот; надпись по центру, у сохранения — на чёрной подложке.
                    button:
                        action FileAction(slot)

                        fixed:
                            add FileScreenshot(slot) align (0.5, 0.5)

                            if FileLoadable(slot):
                                frame:
                                    style "slot_plate"
                                    text FileTime(slot, format=_("{#file_time}%A, %d %B %Y, %H:%M")):
                                        style "slot_time_text"
                            else:
                                text _("ПУСТОЙ СЛОТ"):
                                    style "slot_time_text"
                                    align (0.5, 0.5)

                        key "save_delete" action FileDelete(slot)

            ## Сразу под сеткой слотов: отступ сетки 20 + её высота + 40.
            vbox:
                style_prefix "page"

                xalign 0.5
                ypos (20 + gui.file_slot_rows * gui.slot_button_height + (gui.file_slot_rows - 1) * gui.slot_spacing + 40)

                hbox:
                    xalign 0.5

                    spacing 24

                    ## Четыре страницы слотов и автосохранения; быстрых сохранений и Sync нет.
                    ## Как кнопки главного меню; открытая страница подчёркнута красным.
                    for page in range(1, 5):
                        use main_menu_button(str(page), FilePage(page), button_style="main_menu_page_button")

                    if config.has_autosave:
                        use main_menu_button(_("АВТО"), FilePage("auto"), button_style="main_menu_page_button")

                    key "save_page_prev" action FilePagePrevious(max=4, wrap=True, quick=False)
                    key "save_page_next" action FilePageNext(max=4, wrap=True, quick=False)


style page_label is gui_label
style page_label_text is gui_label_text
style page_button is gui_button
style page_button_text is gui_button_text

style slot_button is gui_button
style slot_button_text is gui_button_text
style slot_time_text is slot_button_text
style slot_name_text is slot_button_text

style page_label:
    xpadding 75
    ypadding 5
    xalign 0.5

style page_label_text:
    color gui.header_color
    textalign 0.5
    layout "subtitle"
    hover_color gui.hover_color

style page_button:
    properties gui.button_properties("page_button")

## Номера страниц — шрифтом кнопок главного меню.
style page_button_text:
    properties gui.text_properties("page_button")
    font gui.main_menu_font

## Чёрный кубик; обводка поверх скриншота: блёклая, как линии настроек, при наведении —
## яркая, как у окон подтверждения.
style slot_button:
    properties gui.button_properties("slot_button")
    background Solid("#000000c7")
    foreground "ui_slot_border"
    hover_foreground "ui_slot_border_hover"
    selected_hover_foreground "ui_slot_border_hover"

style slot_plate is empty:
    background Solid("#000000cc")
    padding (14, 6)
    align (0.5, 0.5)

style slot_button_text:
    properties gui.text_properties("slot_button")


## Настройки

screen preferences():

    tag menu

    ## Категории с заголовками; настройка — строка «название | варианты». Скорости текста
    ## и автопрочтения задаются в options.rpy, игроку не показываются.
    use game_menu(_("НАСТРОЙКИ")):

        vbox:
            xalign 0.5
            spacing 44

            if renpy.variant("pc") or renpy.variant("web"):
                use pref_section(_("ИЗОБРАЖЕНИЕ")):
                    use pref_row(_("РЕЖИМ ЭКРАНА")):
                        hbox:
                            style_prefix "radio"
                            spacing 40
                            yalign 0.5
                            textbutton _("ОКОННЫЙ") action Preference("display", "window")
                            textbutton _("ПОЛНЫЙ") action Preference("display", "fullscreen")

            use pref_section(_("ИГРА")):
                use pref_row(_("ЯЗЫК")):
                    hbox:
                        style_prefix "radio"
                        spacing 40
                        yalign 0.5
                        for lang_code, lang_name in lang_dropdown_items:
                            textbutton lang_name.upper() action Language(lang_code)
                use pref_row(_("ПРОПУСК")):
                    hbox:
                        style_prefix "radio"
                        spacing 40
                        yalign 0.5
                        textbutton _("ПРОЧИТАННЫЙ") action Preference("skip", "seen")
                        textbutton _("ВЕСЬ ТЕКСТ") action Preference("skip", "all")

            if config.has_music or config.has_sound or config.has_voice:
                use pref_section(_("ЗВУК")):
                    if config.has_music:
                        use pref_row(_("МУЗЫКА")):
                            bar style "slider_slider" value Preference("music volume")
                    if config.has_sound:
                        use pref_row(_("ЗВУКИ")):
                            bar style "slider_slider" value Preference("sound volume")
                    if config.has_voice:
                        use pref_row(_("ГОЛОС")):
                            bar style "slider_slider" value Preference("voice volume")
                    use pref_row(""):
                        textbutton _("БЕЗ ЗВУКА"):
                            action Preference("all mute", "toggle")
                            style "mute_all_button"
                            yalign 0.5


## Категория настроек: заголовок, линия цветом разделителя быстрого меню, строки.
screen pref_section(title):
    vbox:
        style "pref_section_vbox"
        text title style "pref_section_title"
        add "ui_pref_hline" xoffset -4
        ## Строки вплотную: вертикальная черта колонки идёт без разрывов.
        vbox:
            transclude
        add "ui_pref_hline" xoffset -4

## Строка настройки: название | черта цветом разделителя | варианты.
## Колонка названий 180 + черта 2 + отступ 18 = 200 — начало вариантов.
screen pref_row(label):
    hbox:
        style "pref_row"
        text label style "pref_row_label"
        add "ui_pref_vline"
        null width 18
        transclude

style pref_section_vbox is vbox:
    xsize 1000
    spacing 10

style pref_section_title is gui_text:
    size 30
    color gui.header_color

style pref_row is hbox:
    ysize 56

style pref_row_label is gui_text:
    min_width 180
    size 24
    color "#8a8784"
    yalign 0.5


style pref_label is gui_label
style pref_label_text is gui_label_text
style pref_vbox is vbox

style radio_label is pref_label
style radio_label_text is pref_label_text
style radio_button is gui_button
style radio_button_text is gui_button_text
style radio_vbox is pref_vbox

style check_label is pref_label
style check_label_text is pref_label_text
style check_button is gui_button
style check_button_text is gui_button_text
style check_vbox is pref_vbox

style slider_label is pref_label
style slider_label_text is pref_label_text
style slider_slider is gui_slider
style slider_button is gui_button
style slider_button_text is gui_button_text
style slider_pref_vbox is pref_vbox

style mute_all_button is check_button
style mute_all_button_text is check_button_text

style pref_label:
    top_margin gui.pref_spacing
    bottom_margin 3

## Настройки компактнее остального интерфейса: всё умещается на экране без прокрутки.
style pref_label_text:
    yalign 1.0
    size 24

style pref_vbox:
    xsize 340

style radio_vbox:
    spacing gui.pref_button_spacing

## Выбранный вариант подчёркнут красной линией вместо маркера слева.
style radio_button:
    properties gui.button_properties("radio_button")
    foreground None
    selected_foreground Fixed(Solid(gui.accent_color, ysize=2, yalign=1.0))

style radio_button_text:
    properties gui.text_properties("radio_button")
    size 26

style check_vbox:
    spacing gui.pref_button_spacing

style check_button:
    properties gui.button_properties("check_button")
    foreground None
    selected_foreground Fixed(Solid(gui.accent_color, ysize=2, yalign=1.0))

style check_button_text:
    properties gui.text_properties("check_button")
    size 26

## Высота — по картинке маркера; ширина — до края категории (1000 − колонка названий 200).
style slider_slider:
    xsize 800
    ysize gui.slider_size
    yalign 0.5

style slider_button:
    properties gui.button_properties("slider_button")
    yalign 0.5
    left_margin 15

style slider_button_text:
    properties gui.text_properties("slider_button")
    size 26

style slider_vbox:
    xsize 560


## История

screen history():

    tag menu

    ## История не предсказывается: _history_list может быть большим.
    predict False

    use game_menu(_("ИСТОРИЯ"), scroll=("vpgrid" if gui.history_height else "viewport"), yinitial=1.0, spacing=gui.history_spacing):

        style_prefix "history"

        for h in _history_list:

            window:

                has fixed:
                    yfit True

                if h.who:

                    label h.who:
                        style "history_name"
                        substitute False

                        if "color" in h.who_args:
                            text_color h.who_args["color"]

                $ what = renpy.filter_text_tags(h.what, allow=gui.history_allow_tags)
                text what:
                    substitute False

        if not _history_list:
            label _("ИСТОРИЯ ДИАЛОГОВ ПУСТА.")


## В истории разрешены только безопасные текстовые теги.

define gui.history_allow_tags = { "alt", "noalt", "rt", "rb", "art" }


style history_window is empty

style history_name is gui_label
style history_name_text is gui_label_text
style history_text is gui_text

style history_label is gui_label
style history_label_text is gui_label_text

style history_window:
    xfill True
    ysize gui.history_height

style history_name:
    xpos gui.history_name_xpos
    xanchor gui.history_name_xalign
    ypos gui.history_name_ypos
    xsize gui.history_name_width

style history_name_text:
    min_width gui.history_name_width
    textalign gui.history_name_xalign

## Реплики в истории — шрифтом и цветом окна диалога.
style history_text:
    font gui.dialogue_text_font
    size gui.dialogue_text_size
    color gui.dialogue_text_color
    xpos gui.history_text_xpos
    ypos gui.history_text_ypos
    xanchor gui.history_text_xalign
    xsize gui.history_text_width
    min_width gui.history_text_width
    textalign gui.history_text_xalign
    layout ("subtitle" if gui.history_text_xalign else "tex")

style history_label:
    xfill True

style history_label_text:
    xalign 0.5


## Помощь

screen help():

    tag menu

    default device = "keyboard"

    use game_menu(_("ПОМОЩЬ"), scroll="viewport"):

        style_prefix "help"

        vbox:
            spacing 23

            hbox:

                textbutton _("КЛАВИАТУРА") action SetScreenVariable("device", "keyboard")
                textbutton _("МЫШЬ") action SetScreenVariable("device", "mouse")

                if GamepadExists():
                    textbutton _("ГЕЙМПАД") action SetScreenVariable("device", "gamepad")

            if device == "keyboard":
                use keyboard_help
            elif device == "mouse":
                use mouse_help
            elif device == "gamepad":
                use gamepad_help


screen keyboard_help():

    hbox:
        label _("Enter")
        text _("Прохождение диалогов, активация интерфейса.")

    hbox:
        label _("Пробел")
        text _("Прохождение диалогов без возможности делать выбор.")

    hbox:
        label _("Стрелки")
        text _("Навигация по интерфейсу.")

    hbox:
        label _("Esc")
        text _("Вход в игровое меню.")

    hbox:
        label _("Ctrl")
        text _("Пропускает диалоги, пока зажат.")

    hbox:
        label _("Tab")
        text _("Включает режим пропуска.")

    hbox:
        label "H"
        text _("Скрывает интерфейс пользователя.")

    hbox:
        label "S"
        text _("Делает снимок экрана.")

    hbox:
        label "Shift+A"
        text _("Открывает меню специальных возможностей.")


screen mouse_help():

    hbox:
        label _("Левый клик")
        text _("Прохождение диалогов, активация интерфейса.")

    hbox:
        label _("Клик колёсиком")
        text _("Скрывает интерфейс пользователя.")

    hbox:
        label _("Правый клик")
        text _("Вход в игровое меню.")


screen gamepad_help():

    hbox:
        label _("Правый триггер\nA/Нижняя кнопка")
        text _("Прохождение диалогов, активация интерфейса.")

    hbox:
        label _("Крестовина, Стики")
        text _("Навигация по интерфейсу.")

    hbox:
        label _("Старт, Гид, B/Правая кнопка")
        text _("Вход в игровое меню.")

    hbox:
        label _("Y/Верхняя кнопка")
        text _("Скрывает интерфейс пользователя.")

    textbutton _("КАЛИБРОВКА") action GamepadCalibrate()


style help_button is gui_button
style help_button_text is gui_button_text
style help_label is gui_label
style help_label_text is gui_label_text
style help_text is gui_text

style help_button:
    properties gui.button_properties("help_button")
    xmargin 12

style help_button_text:
    properties gui.text_properties("help_button")

style help_label:
    xsize 375
    right_padding 30

style help_label_text:
    size gui.text_size
    xalign 1.0
    textalign 1.0


## Дополнительные экраны


## Подтверждение

screen confirm(message, yes_action, no_action):

    modal True

    zorder 200

    style_prefix "confirm"

    add "gui/overlay/confirm.png"

    frame:

        vbox:
            xalign .5
            yalign .5
            spacing 45

            label _(message):
                style "confirm_prompt"
                xalign 0.5

            hbox:
                xalign 0.5
                spacing 150

                use main_menu_button(_("ДА"), yes_action, underline=True)
                use main_menu_button(_("НЕТ"), no_action, underline=True)

    key "game_menu" action no_action


style confirm_frame is gui_frame
style confirm_prompt is gui_prompt
style confirm_prompt_text is gui_prompt_text
style confirm_button is gui_medium_button
style confirm_button_text is gui_medium_button_text

style confirm_frame:
    background "ui_frame_bg_solid"
    padding gui.confirm_frame_borders.padding
    xalign .5
    yalign .5

## Окна поверх игры — шрифтом кнопок главного меню.
style confirm_prompt_text:
    font gui.main_menu_font
    color "#dedbd7"
    textalign 0.5
    layout "subtitle"

style confirm_button:
    properties gui.button_properties("confirm_button")

style confirm_button_text:
    properties gui.text_properties("confirm_button")
    font gui.main_menu_font


## Индикатор пропуска

screen skip_indicator():

    zorder 100
    style_prefix "skip"

    frame:

        hbox:
            spacing 9

            text _("Пропускаю")

            text "▸" at delayed_blink(0.0, 1.0) style "skip_triangle"
            text "▸" at delayed_blink(0.2, 1.0) style "skip_triangle"
            text "▸" at delayed_blink(0.4, 1.0) style "skip_triangle"


transform delayed_blink(delay, cycle):
    alpha .5

    pause delay

    block:
        linear .2 alpha 1.0
        pause .2
        linear .2 alpha 0.5
        pause (cycle - .4)
        repeat


style skip_frame is empty
style skip_text is gui_text
style skip_triangle is skip_text

style skip_frame:
    ypos gui.skip_ypos
    background "ui_frame_bg"
    padding gui.skip_frame_borders.padding

style skip_text:
    size gui.notify_text_size
    font gui.main_menu_font

style skip_triangle:
    ## Шрифт должен содержать U+25B8.
    font "DejaVuSans.ttf"


## Уведомления

screen notify(message):

    zorder 100
    style_prefix "notify"

    frame at notify_appear:
        text "[message!tq]"

    timer 3.25 action Hide('notify')


transform notify_appear:
    on show:
        alpha 0
        linear .25 alpha 1.0
    on hide:
        linear .5 alpha 0.0


style notify_frame is empty
style notify_text is gui_text

style notify_frame:
    ypos gui.notify_ypos

    background "ui_frame_bg"
    padding gui.notify_frame_borders.padding

style notify_text:
    properties gui.text_properties("notify")
    font gui.main_menu_font


## NVL


screen nvl(dialogue, items=None):

    window:
        style "nvl_window"

        has vbox:
            spacing gui.nvl_spacing

        if gui.nvl_height:

            vpgrid:
                cols 1
                yinitial 1.0

                use nvl_dialogue(dialogue)

        else:

            use nvl_dialogue(dialogue)

        ## Меню NVL несовместимо с config.narrator_menu = True.
        for i in items:

            textbutton i.caption:
                action i.action
                style "nvl_button"

    add SideImage() xalign 0.0 yalign 1.0


screen nvl_dialogue(dialogue):

    for d in dialogue:

        window:
            id d.window_id

            fixed:
                yfit gui.nvl_height is None

                if d.who is not None:

                    text d.who:
                        id d.who_id

                text d.what:
                    id d.what_id


define config.nvl_list_length = gui.nvl_list_length

style nvl_window is default
style nvl_entry is default

style nvl_label is say_label
style nvl_dialogue is say_dialogue

style nvl_button is button
style nvl_button_text is button_text

style nvl_window:
    xfill True
    yfill True

    background "gui/nvl.png"
    padding gui.nvl_borders.padding

style nvl_entry:
    xfill True
    ysize gui.nvl_height

style nvl_label:
    xpos gui.nvl_name_xpos
    xanchor gui.nvl_name_xalign
    ypos gui.nvl_name_ypos
    yanchor 0.0
    xsize gui.nvl_name_width
    min_width gui.nvl_name_width
    textalign gui.nvl_name_xalign

style nvl_dialogue:
    xpos gui.nvl_text_xpos
    xanchor gui.nvl_text_xalign
    ypos gui.nvl_text_ypos
    xsize gui.nvl_text_width
    min_width gui.nvl_text_width
    textalign gui.nvl_text_xalign
    layout ("subtitle" if gui.nvl_text_xalign else "tex")

style nvl_thought:
    xpos gui.nvl_thought_xpos
    xanchor gui.nvl_thought_xalign
    ypos gui.nvl_thought_ypos
    xsize gui.nvl_thought_width
    min_width gui.nvl_thought_width
    textalign gui.nvl_thought_xalign
    layout ("subtitle" if gui.nvl_text_xalign else "tex")

style nvl_button:
    properties gui.button_properties("nvl_button")
    xpos gui.nvl_button_xpos
    xanchor gui.nvl_button_xalign

style nvl_button_text:
    properties gui.text_properties("nvl_button")


## Речевые пузыри

screen bubble(who, what):
    style_prefix "bubble"

    window:
        id "window"

        if who is not None:

            window:
                id "namebox"
                style "bubble_namebox"

                text who:
                    id "who"

        text what:
            id "what"

        default ctc = None
        showif ctc:
            add ctc

style bubble_window is empty
style bubble_namebox is empty
style bubble_who is default
style bubble_what is default

style bubble_window:
    xpadding 30
    top_padding 5
    bottom_padding 5

style bubble_namebox:
    xalign 0.5

style bubble_who:
    xalign 0.5
    textalign 0.5
    color "#000"

style bubble_what:
    align (0.5, 0.5)
    text_align 0.5
    layout "subtitle"
    color "#000"

define bubble.frame = Frame("gui/bubble.png", 55, 55, 55, 95)
define bubble.thoughtframe = Frame("gui/thoughtbubble.png", 55, 55, 55, 55)

define bubble.properties = {
    "bottom_left" : {
        "window_background" : Transform(bubble.frame, xzoom=1, yzoom=1),
        "window_bottom_padding" : 27,
    },

    "bottom_right" : {
        "window_background" : Transform(bubble.frame, xzoom=-1, yzoom=1),
        "window_bottom_padding" : 27,
    },

    "top_left" : {
        "window_background" : Transform(bubble.frame, xzoom=1, yzoom=-1),
        "window_top_padding" : 27,
    },

    "top_right" : {
        "window_background" : Transform(bubble.frame, xzoom=-1, yzoom=-1),
        "window_top_padding" : 27,
    },

    "thought" : {
        "window_background" : bubble.thoughtframe,
    }
}

define bubble.expand_area = {
    "bottom_left" : (0, 0, 0, 22),
    "bottom_right" : (0, 0, 0, 22),
    "top_left" : (0, 22, 0, 0),
    "top_right" : (0, 22, 0, 0),
    "thought" : (0, 0, 0, 0),
}


## Мобильные варианты

style pref_vbox:
    variant "medium"
    xsize 675

## На touch-устройствах кнопок меньше, а зоны касания крупнее.
screen quick_menu():
    variant "touch"

    zorder 100

    if quick_menu and not renpy.get_screen("c1s1_mg_runtime"):

        hbox:
            style "quick_menu"
            style_prefix "quick"

            textbutton _("НАЗАД") action Rollback()
            textbutton _("ПРОПУСК") action Skip() alternate Skip(fast=True, confirm=True)
            textbutton _("АВТО") action Preference("auto-forward", "toggle")
            textbutton _("МЕНЮ") action ShowMenu()


style window:
    variant "small"
    background "gui/phone/textbox.png"

style radio_button:
    variant "small"
    foreground "gui/phone/button/radio_[prefix_]foreground.png"

style check_button:
    variant "small"
    foreground "gui/phone/button/check_[prefix_]foreground.png"

style nvl_window:
    variant "small"
    background "gui/phone/nvl.png"

style game_menu_outer_frame:
    variant "small"
    background "gui/phone/overlay/game_menu.png"

style game_menu_content_frame:
    variant "small"
    top_margin 0

style game_menu_viewport:
    variant "small"
    xsize 1305

style pref_vbox:
    variant "small"
    xsize 600

style bar:
    variant "small"
    ysize gui.bar_size
    left_bar Frame("gui/phone/bar/left.png", gui.bar_borders, tile=gui.bar_tile)
    right_bar Frame("gui/phone/bar/right.png", gui.bar_borders, tile=gui.bar_tile)

style vbar:
    variant "small"
    xsize gui.bar_size
    top_bar Frame("gui/phone/bar/top.png", gui.vbar_borders, tile=gui.bar_tile)
    bottom_bar Frame("gui/phone/bar/bottom.png", gui.vbar_borders, tile=gui.bar_tile)

style scrollbar:
    variant "small"
    ysize gui.scrollbar_size
    base_bar Frame("gui/phone/scrollbar/horizontal_[prefix_]bar.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/phone/scrollbar/horizontal_[prefix_]thumb.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)

style vscrollbar:
    variant "small"
    xsize gui.scrollbar_size
    base_bar Frame("gui/phone/scrollbar/vertical_[prefix_]bar.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/phone/scrollbar/vertical_[prefix_]thumb.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)

style slider:
    variant "small"
    ysize gui.slider_size
    base_bar Frame("gui/phone/slider/horizontal_[prefix_]bar.png", gui.slider_borders, tile=gui.slider_tile)
    thumb "gui/phone/slider/horizontal_[prefix_]thumb.png"

style vslider:
    variant "small"
    xsize gui.slider_size
    base_bar Frame("gui/phone/slider/vertical_[prefix_]bar.png", gui.vslider_borders, tile=gui.slider_tile)
    thumb "gui/phone/slider/vertical_[prefix_]thumb.png"

style slider_vbox:
    variant "small"
    xsize None

style slider_slider:
    variant "small"
    xsize 900
