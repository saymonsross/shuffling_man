## Уборка гостиной после реплики о разбросанных носках.

image chapter_1_cleanup_room = "images/1_chapter/cleanup/chapter_1_cleanup_room.png"

define C1S1_CLEANUP_ITEMS = (
    ("blanket", "images/1_chapter/cleanup/chapter_1_cleanup blanket.png", (1158, 640), _("Убрать плед")),
    ("pizza", "images/1_chapter/cleanup/chapter_1_cleanup pizza.png", (1306, 626), _("Убрать коробку пиццы")),
    ("ball", "images/1_chapter/cleanup/chapter_1_cleanup ball.png", (106, 714), _("Убрать мяч")),
    ("stool_clothes", "images/1_chapter/cleanup/chapter_1_cleanup stool_clothes.png", (471, 582), _("Убрать одежду с табурета")),
    ("floor_pillow", "images/1_chapter/cleanup/chapter_1_cleanup floor_pillow.png", (1542, 922), _("Убрать подушку с пола")),
    ("arm_clothes", "images/1_chapter/cleanup/chapter_1_cleanup arm_clothes.png", (883, 532), _("Убрать одежду с подлокотника")),
    ("mug", "images/1_chapter/cleanup/chapter_1_cleanup mug.png", (868, 356), _("Убрать кружку")),
    ("juice", "images/1_chapter/cleanup/chapter_1_cleanup juice.png", (777, 390), _("Убрать пакет сока")),
    ("wrapper", "images/1_chapter/cleanup/chapter_1_cleanup wrapper.png", (227, 349), _("Убрать упаковку")),
    ("album", "images/1_chapter/cleanup/chapter_1_cleanup album.png", (499, 397), _("Убрать альбом и карандаши")),
    ("back_clothes", "images/1_chapter/cleanup/chapter_1_cleanup back_clothes.png", (1334, 300), _("Убрать одежду со спинки дивана")),
)
define C1S1_CLEANUP_KEYS = tuple(item[0] for item in C1S1_CLEANUP_ITEMS)
define C1S1_CLEANUP_DISSOLVE = Dissolve(0.22)
define C1S1_CLEANUP_HOVER_SOUND = "hover"
define C1S1_CLEANUP_PICKUP_SOUND = "click"

default c1s1_cleanup_collected = ()
default c1s1_cleanup_outcome = None

init python:

    def c1s1_cleanup_reset():
        store.c1s1_cleanup_collected = ()
        store.c1s1_cleanup_outcome = None

    def c1s1_cleanup_collect(key):
        if (store.c1s1_cleanup_outcome is not None
                or key not in C1S1_CLEANUP_KEYS
                or key in store.c1s1_cleanup_collected):
            return False
        ## Новое значение tuple сохраняется и откатывается вместе с call screen.
        store.c1s1_cleanup_collected += (key,)
        return True

    def c1s1_cleanup_complete():
        return len(store.c1s1_cleanup_collected) == len(C1S1_CLEANUP_KEYS)

    def c1s1_cleanup_finish(skipped=False):
        if skipped:
            store.c1s1_cleanup_collected = C1S1_CLEANUP_KEYS
            store.c1s1_cleanup_outcome = "skipped"
        elif c1s1_cleanup_complete():
            store.c1s1_cleanup_outcome = "done"


## Все предметы и фон рисуются в одной системе координат без отдельной камеры UI.
## imagebutton/focus_mask повторяет принцип 7dots test_bg_inventory/game_items.
screen c1s1_cleanup_minigame():
    modal True
    roll_forward True
    use sm_skippable_interaction

    add "chapter_1_cleanup_room" id "cleanup_background"

    for key, item_image, item_pos, item_caption in C1S1_CLEANUP_ITEMS:
        if key not in c1s1_cleanup_collected:
            imagebutton:
                id "cleanup_" + key
                idle item_image
                hover At(item_image, brightness(0.18))
                focus_mask item_image
                pos item_pos
                alt item_caption
                hovered SPlay(C1S1_CLEANUP_HOVER_SOUND, ext="ogg")
                action Return(key)

    $ collected_count = len(c1s1_cleanup_collected)
    $ total_count = len(C1S1_CLEANUP_KEYS)
    $ cleanup_percent = int(100 * collected_count / total_count)

    frame:
        xalign 0.5
        ypos 28
        xsize 760
        padding (28, 16)
        background Solid("#17131ce6")

        vbox:
            spacing 10

            text _("Собрано предметов: [collected_count] / [total_count] · [cleanup_percent]%"):
                style "c1s1_cleanup_text"
                xalign 0.5

            bar:
                id "cleanup_progress"
                value StaticValue(collected_count, total_count)
                xfill True
                ysize 14
                left_bar Solid("#e2cea4")
                right_bar Solid("#4c444b")
                thumb None

    if c1s1_cleanup_complete():
        frame:
            id "cleanup_complete"
            align (0.5, 0.5)
            xsize 660
            padding (36, 28)
            background Solid("#17131cee")
            at show_hide(0.22)

            vbox:
                spacing 22
                xalign 0.5

                text _("Всё убрано"):
                    style "c1s1_cleanup_text"
                    xalign 0.5
                    size 38

                textbutton _("Продолжить"):
                    id "cleanup_continue"
                    xalign 0.5
                    hovered SPlay(C1S1_CLEANUP_HOVER_SOUND, ext="ogg")
                    action [SPlay(C1S1_CLEANUP_PICKUP_SOUND, ext="ogg"), Return("done")]


style c1s1_cleanup_text is gui_text:
    color "#f1e9db"
    size 28
    textalign 0.5


label chapter_1_scene_1_minigame_cleanup hide:
    $ c1s1_cleanup_reset()
    $ dismiss_off()
    window hide
    camera
    scene chapter_1_cleanup_room

    if not renpy.is_skipping():
        show screen c1s1_cleanup_minigame
        with C1S1_CLEANUP_DISSOLVE

    while c1s1_cleanup_outcome is None:
        if not renpy.is_skipping():
            ## Return создаёт отдельный checkpoint для каждого взятого предмета.
            ## _with_none=False сохраняет предыдущий кадр для dissolve одного слоя.
            call screen c1s1_cleanup_minigame(_with_none=False)

            if _return in C1S1_CLEANUP_KEYS:
                if c1s1_cleanup_collect(_return):
                    $ splay(C1S1_CLEANUP_PICKUP_SOUND, ext="ogg")
                show screen c1s1_cleanup_minigame
                with C1S1_CLEANUP_DISSOLVE
            elif _return == "done":
                $ c1s1_cleanup_finish()
            else:
                $ c1s1_cleanup_finish(skipped=True)
        else:
            $ c1s1_cleanup_finish(skipped=True)

    hide screen c1s1_cleanup_minigame
    $ dismiss_on()
    return
