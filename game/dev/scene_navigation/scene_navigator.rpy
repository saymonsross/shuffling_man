## Навигатор сцен для локальной developer-сборки.
## game/dev/** исключён из дистрибутива; меню также проверяет config.developer.

define DEV_SCENE_NAV_CARDS_PER_ROW = 3

## label — ключ карточки и точка входа: сцены продолжают маршрут цепочкой jump.
define DEV_SCENE_NAV_ENTRIES = (
    {
        "section": _("ПРОЛОГ"),
        "title": _("Сцена 1 · Записка"),
        "label": "prologue_scene",
        "preview": "dev/scene_navigation/previews/prologue_scene_1.jpg",
    },
    {
        "section": _("ПРОЛОГ"),
        "title": _("Сцена 2 · Начало письма"),
        "label": "prologue_scene.letter",
        "preview": "images/0_prologue/prologue pencil_close.jpg",
    },
    {
        "section": _("ГЛАВА 1"),
        "title": _("Сцена 1 · Стук в дверь"),
        "label": "chapter_1_scene_1",
        "preview": "dev/scene_navigation/previews/chapter_1_scene_1.jpg",
    },
    {
        "section": _("ГЛАВА 1"),
        "title": _("Телевизор"),
        "label": "chapter_1_scene_1.tv",
        "preview": "images/1_chapter/chapter_1 scene_1_tv_close.jpg",
    },
    {
        "section": _("ГЛАВА 1"),
        "title": _("Уборка"),
        "label": "chapter_1_scene_1.cleanup",
        "preview": "images/1_chapter/cleanup/chapter_1_cleanup_mess.png",
    },
    {
        "section": _("ГЛАВА 1"),
        "title": _("Сцена 2 · Ссора"),
        "label": "chapter_1_scene_2",
        "preview": "images/1_chapter/chapter_1 scene_2_parents_room_door.jpg",
    },
    {
        "section": _("ГЛАВА 1"),
        "title": _("Бутерброды"),
        "label": "chapter_1_scene_2.sandwiches",
        "preview": "images/1_chapter/chapter_1 scene_2_sandwiches.jpg",
    },
    {
        "section": _("ГЛАВА 1"),
        "title": _("Сцена 3 · Воображаемый друг"),
        "label": "chapter_1_scene_3",
        "preview": "images/1_chapter/chapter_1 scene_3_children_room_girl_neutral.jpg",
    },
)


init python:

    def dev_scene_nav_start(label):
        if not config.developer:
            return

        if not renpy.has_label(label):
            renpy.notify(_("Сцена недоступна."))
            return

        ## full_restart не переносит состояние предыдущей сцены.
        renpy.full_restart(None, label=label)


screen dev_scene_navigator():

    tag menu

    ## ShowMenu сохраняет старый фокус; переносим его на первую карточку.
    on ("show", "replace") action Function(
        renpy.set_focus,
        "dev_scene_navigator",
        DEV_SCENE_NAV_ENTRIES[0]["label"])

    use game_menu(_("Сцены"), scroll="viewport", spacing=24):

        for row_start in range(0, len(DEV_SCENE_NAV_ENTRIES), DEV_SCENE_NAV_CARDS_PER_ROW):

            hbox:
                xalign 0.5
                spacing 24

                for entry_index in range(row_start, min(row_start + DEV_SCENE_NAV_CARDS_PER_ROW, len(DEV_SCENE_NAV_ENTRIES))):

                    use dev_scene_nav_card(
                        DEV_SCENE_NAV_ENTRIES[entry_index],
                        autofocus=(entry_index == 0))


screen dev_scene_nav_card(entry, autofocus=False):

    button:
        id entry["label"]
        style "dev_scene_nav_card"
        action Function(dev_scene_nav_start, entry["label"])
        default_focus autofocus

        vbox:
            xfill True
            spacing 3

            fixed:
                xysize (384, 216)
                xalign 0.5

                if renpy.loadable(entry["preview"]):
                    add entry["preview"]:
                        xysize (384, 216)
                else:
                    add Solid("#241c1c")

            text entry["section"]:
                style "dev_scene_nav_section"

            text entry["title"]:
                style "dev_scene_nav_title"

style dev_scene_nav_card is slot_button:
    xsize 414
    ysize 316
    padding (15, 15)

## Карточки — шрифтом движка, как остальные dev-инструменты; рамка меню — игровая.
style dev_scene_nav_section is gui_text:
    font "DejaVuSans.ttf"
    color gui.dark_background_accent
    hover_color "#ffffff"
    size 18
    xalign 0.5

style dev_scene_nav_title is gui_text:
    font "DejaVuSans.ttf"
    color gui.interface_text_color
    hover_color "#ffffff"
    size 26
    xalign 0.5
    textalign 0.5
