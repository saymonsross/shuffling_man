## Dev-старт: блок «DEV-СТАРТ С:» в Dev Hub (F12) из главного меню запускает игру с выбранной
## сцены кнопкой ▶; «НОВАЯ ИГРА» всегда начинает с начала. Выбор сцены живёт в persistent.
## game/dev/** не входит в дистрибутив; script.rpy дополнительно проверяет config.developer.

default persistent.sm_dev_start_label = "chapter_1_scene_2"

init python:

    def dev_start_entries():
        """(лейбл, подпись) в сюжетном порядке: карточки навигатора и вход в пианино."""
        rv = []
        for entry in DEV_SCENE_NAV_ENTRIES:
            rv.append((entry["label"], entry["section"] + " · " + entry["title"]))
            if entry["label"] == "chapter_1_scene_1":
                rv.append(("chapter_1_scene_1.piano", "ГЛАВА 1 · Пианино"))
        return rv

    def dev_start_title(label):
        return next((title for key, title in dev_start_entries() if key == label), label or "—")


## Используется внутри dev_hub; сам экран не показывается.
screen dev_start_panel():

    default dev_start_open = False

    vbox:
        spacing 6

        hbox:
            spacing 10

            text "DEV-СТАРТ С:":
                style "dev_hub_key"
                min_width 0
                yalign 0.5
                substitute False

            button:
                style "dev_hub_item"
                action ToggleScreenVariable("dev_start_open")
                text (dev_start_title(persistent.sm_dev_start_label) + "  ▾"):
                    style "dev_hub_name"
                    substitute False

        button:
            style "dev_hub_item"
            action [Hide("dev_hub"), SetField(persistent, "sm_dev_start_once", True), Start()]
            text "▶ ИГРАТЬ С ВЫБРАННОЙ СЦЕНЫ" style "dev_hub_name" substitute False

        if dev_start_open:
            for key, title in dev_start_entries():
                button:
                    style "dev_hub_item"
                    selected (key == persistent.sm_dev_start_label)
                    selected_background "#9fffcf33"
                    action [SetField(persistent, "sm_dev_start_label", key),
                        SetScreenVariable("dev_start_open", False), Function(renpy.save_persistent)]
                    text title style "dev_hub_name" substitute False
