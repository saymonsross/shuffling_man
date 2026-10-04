## Уборка гостиной после реплики о разбросанных носках.

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
define C1S1_CLEANUP_HOVER_SOUND = "c1s1/c1s1_cleanup_hover"
define C1S1_CLEANUP_HOVER_VOLUME = 0.044
## Звуки уборки идут через общий фильтр комнаты: доля глухого low-pass 700 Гц и доля эха.
define C1S1_CLEANUP_LOWPASS = 0.10
define C1S1_CLEANUP_REVERB = 0.15
## Звук взятия — свой у каждого предмета (audio/sfx/c1s1/README.md); у кого своего нет — щелчок.
define C1S1_CLEANUP_PICKUP_SOUND = "click"
define C1S1_CLEANUP_PICKUP_SOUNDS = {
    "blanket": "c1s1/c1s1_cleanup_blanket",
    "pizza": "c1s1/c1s1_cleanup_pizza",
    "ball": "c1s1/c1s1_cleanup_ball",
    "stool_clothes": "c1s1/c1s1_cleanup_stool_clothes",
    "arm_clothes": "c1s1/c1s1_cleanup_arm_clothes",
    "mug": "c1s1/c1s1_cleanup_mug",
    "juice": "c1s1/c1s1_cleanup_juice",
    "album": "c1s1/c1s1_cleanup_album",
    "wrapper": "c1s1/c1s1_cleanup_wrapper",
    "back_clothes": "c1s1/c1s1_cleanup_back_clothes",
    }
## Подушка звучит одной из куч одежды, на 7% ниже (отдельные файлы pillow_*).
define C1S1_CLEANUP_PILLOW_SOURCES = ("back_clothes", "arm_clothes", "stool_clothes")
define C1S1_CLEANUP_PICKUP_VOLUME = 0.30
## Наведённый предмет чуть темнеет, а под ним проявляется процарапанная обводка.
define C1S1_CLEANUP_HOVER_BRIGHTNESS = -0.03
define C1S1_CLEANUP_OUTLINE_ALPHA = 0.65
define C1S1_CLEANUP_OUTLINE_FADE = 0.12
## Подсказка: если долго ничего не брать, у одного из оставшихся предметов еле заметно
## проявляется та же обводка — через DELAY секунд после последнего взятого, раз в PERIOD.
## Предмет — случайный из POOL самых мелких оставшихся: застревают на мелочи. ORDER — от
## мелких к крупным по площади непрозрачных пикселей PNG; при замене картинок пересчитать.
define C1S1_CLEANUP_HINT_ORDER = ("juice", "mug", "album", "wrapper", "pizza", "stool_clothes",
    "ball", "arm_clothes", "floor_pillow", "back_clothes", "blanket")
define C1S1_CLEANUP_HINT_POOL = 5
define C1S1_CLEANUP_HINT_DELAY = 8.0
define C1S1_CLEANUP_HINT_PERIOD = 6.5
define C1S1_CLEANUP_HINT_ALPHA = 0.3
## Пауза на чистой комнате после последнего предмета.
define C1S1_CLEANUP_DONE_PAUSE = 1.2
## Дыхание яркости всей комнаты: от LO до HI и обратно, T секунд в одну сторону. Те же
## числа — у кадра гостиной перед уборкой в сцене: оба дышат по часам кадра, в одной фазе,
## и на стыке картинка не меняется. Менять вместе.
define C1S1_CLEANUP_BREATH_LO = 0.0
define C1S1_CLEANUP_BREATH_HI = -0.04
define C1S1_CLEANUP_BREATH_T = 6.0
## Доли bloom и виньетки на комнате (fx_frame) — те же, что у кадра гостиной перед уборкой.
define C1S1_CLEANUP_FX_BLOOM = 0.0
define C1S1_CLEANUP_FX_VIGNETTE = 0.6

init -10 python:
    scratch_params("cleanup_items", "Обводка предметов уборки", 2.1, 0.3, 2.1, 0.9)

## Комната уборки — на своём слое мира под интерфейсом: её, как и кадры сцены, обрабатывают
## эффекты слоя сцены (bloom, ретушь, постеризация), а виньетка ложится сверху. Надпись —
## отдельным экраном на слое интерфейса, мимо обработки.
init python:
    if "cleanupgame" not in config.layers:
        renpy.add_layer("cleanupgame", below="screens")

default c1s1_cleanup_collected = ()
default c1s1_cleanup_outcome = None
default c1s1_cleanup_hint = None

init python:

    def c1s1_cleanup_reset():
        store.c1s1_cleanup_collected = ()
        store.c1s1_cleanup_outcome = None
        c1s1_cleanup_pick_hint()

    def c1s1_cleanup_pick_hint():
        ## renpy.random — тот же выбор после отката и загрузки.
        left = [k for k in C1S1_CLEANUP_HINT_ORDER if k not in store.c1s1_cleanup_collected]
        store.c1s1_cleanup_hint = renpy.random.choice(left[:C1S1_CLEANUP_HINT_POOL]) if left else None

    def c1s1_cleanup_collect(key):
        if (store.c1s1_cleanup_outcome is not None
                or key not in C1S1_CLEANUP_KEYS
                or key in store.c1s1_cleanup_collected):
            return False
        ## Новое значение tuple сохраняется и откатывается вместе с call screen.
        store.c1s1_cleanup_collected += (key,)
        c1s1_cleanup_pick_hint()
        return True

    def c1s1_cleanup_pickup_sound(key):
        """Звук только что взятого предмета key. Подушке — одна из куч одежды, не звучавшая
        на двух предыдущих взятых предметах: повтор подряд было бы слышно."""
        if key == "floor_pillow":
            recent = store.c1s1_cleanup_collected[-3:-1]
            source = next(k for k in C1S1_CLEANUP_PILLOW_SOURCES if k not in recent)
            return "c1s1/c1s1_cleanup_pillow_" + source
        return C1S1_CLEANUP_PICKUP_SOUNDS.get(key, C1S1_CLEANUP_PICKUP_SOUND)

    def c1s1_cleanup_play(name, volume):
        sm_audio_set_filter(sm_sfx(name, volume=volume), [
            renpy.audio.filter.WetDry(renpy.audio.filter.Lowpass(700.0),
                wet=C1S1_CLEANUP_LOWPASS, dry=1.0 - C1S1_CLEANUP_LOWPASS),
            renpy.audio.filter.Reverb(resonance=0.72, dampening=2400.0,
                wet=C1S1_CLEANUP_REVERB, dry=1.0 - C1S1_CLEANUP_REVERB, delay_multiplier=1.8),
            ], duration=0)

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
## Интерфейса нет: прогресс — сама комната, которая пустеет. waiting — экран вызван ждать
## клика: только тогда он сам завершает уборку, когда убрано всё (в том числе кодом).
## Показ через show screen — лишь растворение взятого предмета, его не обрывает.
## finished — пауза на чистой комнате: экран вызван и сам закрывается своим таймером.
## pause здесь не годится: модальный экран глушит и её таймер.
screen c1s1_cleanup_minigame(waiting=False, finished=False):
    layer "cleanupgame"
    modal True
    roll_forward True
    use sm_skippable_interaction

    if waiting and c1s1_cleanup_complete():
        timer 0.01 action Return("done")
    if finished:
        timer C1S1_CLEANUP_DONE_PAUSE action Return()

    ## Комната с предметами повторяет камеру и параллакс слоя сцены: отъезд кадра перед
    ## уборкой доезжает уже во время неё, и на стыке картинка не прыгает. Дышит яркостью,
    ## как кадры сцены. Фаза — от часов кадра: экран пересоздаётся на каждом взятом предмете.
    fixed:
        at follow_camera(zoom_pad=1.0), breath_brightness_clock(C1S1_CLEANUP_BREATH_LO, C1S1_CLEANUP_BREATH_HI, C1S1_CLEANUP_BREATH_T), fx_frame(bloom=C1S1_CLEANUP_FX_BLOOM, vignette=C1S1_CLEANUP_FX_VIGNETTE)

        add "chapter_1_cleanup_room" id "cleanup_background"

        for key, item_image, item_pos, item_caption in C1S1_CLEANUP_ITEMS:
            if key not in c1s1_cleanup_collected:
                ## Таймер подсказки идёт от показа экрана — от последнего взятого предмета.
                if key == c1s1_cleanup_hint:
                    add item_image pos item_pos at c1s1_cleanup_hint_pulse
                ## Обводка и затемнение — от состояния самой кнопки (события hover/idle её
                ## детям), а не от hovered/unhovered: мышь, переведённая на предмет во время
                ## растворения взятого, даёт фокус без hovered, и обводка не появлялась. Размер
                ## кнопки — по картинке: запас текстуры под штрих не сбивает зону клика.
                button:
                    id "cleanup_" + key
                    style "empty"
                    pos item_pos
                    xysize renpy.image_size(item_image)
                    focus_mask item_image
                    alt item_caption
                    hovered Function(c1s1_cleanup_play, C1S1_CLEANUP_HOVER_SOUND, C1S1_CLEANUP_HOVER_VOLUME)
                    action Return(key)
                    add item_image at c1s1_cleanup_outline
                    add item_image at c1s1_cleanup_item_hover

## Держится до конца уборки и уходит вместе с растворением последнего предмета: пропав
## раньше, читалась бы как «готово».
screen c1s1_cleanup_prompt():
    if not c1s1_cleanup_complete():
        text _("ПРИБЕРИСЬ В КОМНАТЕ"):
            id "cleanup_prompt"
            style "c1s1_cleanup_prompt"
            at scratch("scene_choice_text", tint=0.0)


## Белый силуэт предмета под ним: штрих (tint 1 — белый) рвёт его край наружу, как у деталей
## замков. Проявляется, пока кнопка предмета наведена.
transform c1s1_cleanup_outline():
    alpha 0.0
    parallel:
        scratch("cleanup_items", tint=1.0, idle_color="#ffffff", hover_color="#ffffff", pad=24)
    parallel:
        on hover, selected_hover:
            linear C1S1_CLEANUP_OUTLINE_FADE alpha C1S1_CLEANUP_OUTLINE_ALPHA
        on idle, selected_idle, insensitive:
            linear C1S1_CLEANUP_OUTLINE_FADE alpha 0.0

transform c1s1_cleanup_item_hover():
    on hover, selected_hover:
        matrixcolor BrightnessMatrix(C1S1_CLEANUP_HOVER_BRIGHTNESS)
    on idle, selected_idle, insensitive:
        matrixcolor BrightnessMatrix(0.0)

## Не c1s1_cleanup_hint: так называется переменная с ключом предмета, она затёрла бы трансформ.
transform c1s1_cleanup_hint_pulse():
    alpha 0.0
    parallel:
        scratch("cleanup_items", tint=1.0, idle_color="#ffffff", hover_color="#ffffff", pad=24)
    parallel:
        pause C1S1_CLEANUP_HINT_DELAY
        block:
            ease (C1S1_CLEANUP_HINT_PERIOD * 0.25) alpha C1S1_CLEANUP_HINT_ALPHA
            ease (C1S1_CLEANUP_HINT_PERIOD * 0.35) alpha 0.0
            pause (C1S1_CLEANUP_HINT_PERIOD * 0.4)
            repeat


## Голос сценовых действий — как подписи кнопок в сценах («Зажечь свет»).
style c1s1_cleanup_prompt is glow_button_text:
    size 34
    xalign 0.5
    yalign 0.97


label chapter_1_scene_1_minigame_cleanup hide:
    $ c1s1_cleanup_reset()
    $ dismiss_off()
    $ quick_menu = False
    window hide
    ## Камера кадра перед уборкой не сбрасывается: её повторяет комната мини-игры.
    ## Комната слоя сцены дышит и держит доли эффектов как экран: после мини-игры она
    ## остаётся одна, и без них bloom вернулся бы к сюжетному — кадр вспыхнул бы перед
    ## переходом.
    scene chapter_1_cleanup_room:
        parallel:
            breath_brightness_clock(C1S1_CLEANUP_BREATH_LO, C1S1_CLEANUP_BREATH_HI, C1S1_CLEANUP_BREATH_T)
        parallel:
            fx_frame(bloom=C1S1_CLEANUP_FX_BLOOM, vignette=C1S1_CLEANUP_FX_VIGNETTE)

    if not renpy.is_skipping():
        show screen c1s1_cleanup_minigame
        show screen c1s1_cleanup_prompt
        with C1S1_CLEANUP_DISSOLVE

    while c1s1_cleanup_outcome is None:
        if not renpy.is_skipping():
            ## Return создаёт отдельный checkpoint для каждого взятого предмета.
            ## _with_none=False сохраняет предыдущий кадр для dissolve одного слоя.
            call screen c1s1_cleanup_minigame(waiting=True, _with_none=False)

            if _return in C1S1_CLEANUP_KEYS:
                if c1s1_cleanup_collect(_return):
                    $ c1s1_cleanup_play(c1s1_cleanup_pickup_sound(_return), C1S1_CLEANUP_PICKUP_VOLUME)
                show screen c1s1_cleanup_minigame
                with C1S1_CLEANUP_DISSOLVE
            elif _return == "done":
                $ c1s1_cleanup_finish()
            else:
                $ c1s1_cleanup_finish(skipped=True)
        else:
            $ c1s1_cleanup_finish(skipped=True)

    ## Пауза на чистой комнате — тем же экраном: call screen прячет его при возврате, и
    ## паузу держала бы голая комната слоя сцены — с параллаксом, кадр дёрнулся бы.
    if c1s1_cleanup_outcome == "done":
        call screen c1s1_cleanup_minigame(finished=True, _with_none=False)

    hide screen c1s1_cleanup_minigame
    hide screen c1s1_cleanup_prompt
    $ dismiss_on()
    $ quick_menu = True
    return
