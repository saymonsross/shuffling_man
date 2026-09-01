## КАК ПОЛЬЗОВАТЬСЯ

# чтобы переключить на следующее доступное разрешение, в quick_menu добавить
# textbutton resolution_aliace() action ToggleResolution()

# чтобы выбрать из списка доступных разрешений, в preferences добавить:
# textbutton res_dropbox.text xsize config.screen_width // 6 action DropBoxDrop(res_dropbox)

# но для начала заполнить resolution_dpi ниже доступными разрешениями
# и создать нужные папки в game/ gui_2K, gui_4K и т.д.
# а так же версии спрайтов и прочей графики нужных разрешений
# и с соответствующими суффиксами img 2K.png, img 4K.png и т.д. (через пробел)

# в файле gui.rpy заменить все параметры на те же, но через функцию K()
# init python:
    # gui.init(K(1920), K(1080))

# define gui.quick_button_borders = Borders(K(15), K(6), K(15), K(0))
# define gui.quick_button_text_size = K(21)
# и т.д.

# в файле screens.rpy то же с делать ещё и с картинками
# style window:
    # background Image(K("gui") + "/textbox.png", xalign=0.5, yalign=1.0)

## НАСТРОЙКИ

init -11 python:
    # список доступных разрешений %K: dpi (высота)
    # "1K": 1080
    # "2K": 1440
    # "4K": 2160
    # "8K": 4320
    # и т.д.
    # в примере есть графика для трёх вариантов
    resolution_dpi = {
        "1K": 1080,
        "2K": 1440,
        "4K": 2160
    }

    # словарь суффиксов, которые нужно переименовать для выпадающего списка
    resolution_aliaces = {
        "1K": "FullHD"
    }

## ДАЛЕЕ ЛУЧШЕ НИЧЕГО НЕ МЕНЯТЬ

    # подмена на псевдоним
    def resolution_aliace(key=None):
        if key is None: key = persistent.resolution_k

        if key in resolution_aliaces.keys():
            return resolution_aliaces[key]

        return key

    # отсортированные разрешения
    resolution_keys = list(resolution_dpi.keys())

    # список с заменой названий для разрешений
    resolution_keys_aliased = [ resolution_aliace(i) for i in resolution_keys ]

    # по умолчанию самое низкое разрешение (FullHD)
    default_resolution_k = resolution_keys[0]
    if persistent.resolution_k is None: persistent.resolution_k = default_resolution_k

    # модуль помогает настроить игру для любых разрешений (1920x1080, 3840x2160 и т.д.)
    # если у вас есть соответствующие наборы графики, включая интерфейс

    # с помощью функции K() нужно переписать файлы qui.rpy и screens.rpy
    # везде, где есть целочисленные координаты и размеры
    # define gui.quick_button_borders = Borders(K(15), K(6), K(15), K(0))
    # define gui.quick_button_text_size = K(21)

    # как менять графику gui (пример, но нужно поменять всё):
    # left_bar Frame(K("gui") + "/bar/left.png", gui.bar_borders, tile=gui.bar_tile)

    # при этом нужно добавить в проект папку gui_2K с соответствующей графикой

    # как объявлять спрайты и фоны:
    # image bg room = IK("bg room")
    # в папке images должны быть картинки "bg room 1K", "bg room 2K" и "bg room 4K"

    # автоматическое объявление спрайтов,
    # чтобы собирать из них переключаемые спрайты
    config.automatic_images_minimum_components = 1
    config.automatic_images = [ ' ', '_', '/' ]
    config.automatic_images_strip = [ 'images' ]

    # узнать следующее по списку разрешение
    def get_next_resolution(k=None, alias=True):
        if k is None:
            index = resolution_keys.index(persistent.resolution_k) + 1
            if index >= len(resolution_keys): index = 0
            k = resolution_keys[index]

        new_k = k

        if alias:
            return resolution_aliace(new_k)

        return new_k

    # сменить разрешение
    def change_resolution(k=None, confirm=True):
        new_k = get_next_resolution(k, False)
        new_dpi = resolution_dpi[new_k]

        if confirm:
            layout.yesno_screen(message=_("Сменить разрешение на %s (%sp)?" % (resolution_aliace(new_k), new_dpi)), yes=[ SetField(persistent, "resolution_k", new_k), Function(renpy.exports.reload_script) ])

        else:
            persistent.resolution_k = new_k
            renpy.exports.reload_script()

    ChangeResolution = renpy.curry(change_resolution)

    # класс для переключения разрешения, пример:
    # textbutton "2K" action ToggleResolution()
    class ToggleResolution(Action):
        def __init__(self, confirm=True):
            self.confirm = confirm

            if persistent.resolution_k is None:
                persistent.resolution_k = default_resolution_k

        # переключение на одно из возможных разрешений [ 1, 2, 4... ]
        # или при i=None - на следующее после текущего (сортируются оп возрастанию)
        def __call__(self, i=None, confirm=True):
            self.confirm = confirm

            change_resolution(i, self.confirm)

        def get_selected(self):
            return persistent.resolution_k != default_resolution_k

    ## ДЛЯ GUI
    # пересчёт переменной в зависимости от режима
    # к строковым переменным добавляется суффикс " %K",
    # где % - индекс разрешения, отличное от разрешения по умолчанию (2, 4...)
    # если разрешение стандартное (равно default_resolution_k), то без суффикса
    def K(x, gui=True, delimiter=" "):
        if gui is True and persistent.resolution_k == default_resolution_k:
            return x

        if isinstance(x, (str, unicode)):
            suffix = delimiter + persistent.resolution_k
            if suffix == delimiter: suffix = ""

            return str(x) + suffix

        if persistent.resolution_k == default_resolution_k:
            return x

        return int(x / (resolution_dpi[default_resolution_k] * 1. / resolution_dpi[persistent.resolution_k]))

    # создание изображений, разрешение которых зависит от текущего разрешения
    # image bg room = IK("bg room")
    # должны быть картинки "bg room 1K", "bg room 2K", "bg room 4K" и т.д.
    # смотря сколько режимов доступно и в наличии графика
    # режим по умолчанию тоже должен иметь свой индекс и папку!
    def IK(img):
        return K(img, False)

init 1 python:
    # обработчик клика по строке выпадающего списка
    def res_db_click(db):
        change_resolution(resolution_keys[db.index], False)

    # экземпляр класса выпадающего списка специально для выбора разрешений
    res_dropbox = DropBox(resolution_keys_aliased, res_db_click)

    # в настройках будет:
    # textbutton res_dropbox.text xsize config.screen_width // 6 action DropBoxDrop(res_dropbox)



## КЛАСС DropBox

# стиль составных частей выпадающего списка
init:
    style dropbox_vbox is vbox:
        spacing 0

    style dropbox_button is button:
        background gui.text_color
        hover_background gui.hover_color

    style dropbox_button_text is button_text:
        color gui.idle_color
        hover_color gui.text_color

# строки списка всегда той же ширины, что и родительский виджет, которым вызвали список

# пример создания выпадающего списка (4 и callback_sample - необязательные параметры):
# $ db1 = DropBox( [ _("Строка 1"), _("Строка 2"), _("Строка 3"), _("Строка 4"), _("Строка 5") ], 4, callback_sample )

# пример вызова выпадающего списка:
# textbutton db1.text xsize 480 action DropBoxDrop(db1)

# пример обработчика выбора строки в выпадающем списке (необязательно),
# на входе всегда экземпляр класса DropBox, в котором произошёл выбор:
# def callback_sample(db):
    # renpy.notify("%s: %s" % (db.id, db.text))

init python:
    # для уникальности id каждого списка, чтобы на экране их могло быть сколько угодно
    dropbox_current_id = 0

    # класс для выпадающего списка
    class DropBox():
        def __init__(self, lines, callback=None, index=0, id=None):
            global dropbox_current_id

            # уникальный идентификатор
            if id is None:
                self.id = "dropbox" + str(dropbox_current_id)
                dropbox_current_id += 1

            else:
                self.id = id

            # список строк для выбора вариантов
            self.lines = lines
            # текст выбранной строки
            self.text = ""

            # индекс выбранной строки
            if index >= len(self.lines): index = len(self.lines) - 1
            if index < 0: index = 0
            self.index = index

            if self.lines:
                self.text = self.lines[self.index]

            # параметры родительского для выпадающего списка виджета
            self.x, self.y, self.w, self.h = 0, 0, 0, 0
            # текущая видимость
            self.shown = False
            # обработчик выбора
            self.callback = callback

    # показать скрыть выпадающий список
    def dropbox_drop(db):
        tag = ("dropbox_"+str(db.id)).strip().replace(" ", "_")

        if db.shown:
            db.shown = False

            renpy.hide_screen(tag)
            renpy.restart_interaction()

        else:
            db.x, db.y, db.w, db.h = renpy.focus_coordinates()
            db.x, db.y, db.w, db.h = int(db.x), int(db.y), int(db.w), int(db.h)
            db.shown = True

            renpy.show_screen("db_screen", db, _tag=tag, _transient=True)
            renpy.restart_interaction()

    DropBoxDrop = renpy.curry(dropbox_drop)

    # обработка клика по строке выпадающего списка - выбрать новую строку
    def dropbox_click(db, index):
        db.index = index
        db.text = db.lines[db.index]
        db.shown = False

        tag = ("dropbox_"+str(db.id)).strip().replace(" ", "_")
        renpy.hide_screen(tag)
        renpy.restart_interaction()

        if db.callback:
            db.callback(db)

    DropBoxClick = renpy.curry(dropbox_click)

# экран с выпадающим списком
screen db_screen(db):
    style_prefix "dropbox"

    vbox:
        pos (db.x, db.y + db.h)

        for i in range(len(db.lines)):
            # строки списка всегда той же ширины, что и родительский виджет, которым вызвали список
            textbutton db.lines[i] xsize db.w action DropBoxClick(db, i)

# готовые примеры выпадающих списков
init python:
    # обработчик выбора режима экрана
    # на входе всегда экземпляр класса DropBox, в котором произошёл выбор, даже если он не нужен
    def set_display(db):
        if db.index:
            Preference("display", "fullscreen")()
        else:
            Preference("display", "window")()

    # стартовое состояние
    i = 1 if preferences.fullscreen else 0

    # класс выпадающего списка для управления режимом экрана
    db_display = DropBox([ _("Оконный"), _("Полный") ], set_display, i)

    # пример использования на экране настроек
    # vbox:
        # label _("Режим экрана") style "radio_label"
        # textbutton db_display.text xsize config.screen_width // 6 action DropBoxDrop(db_display)
