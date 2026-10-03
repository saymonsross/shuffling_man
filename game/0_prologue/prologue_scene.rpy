## Пролог: титры → тёмная комната → воспоминание → начало письма.

## Изображения

image prologue_dark_room = "images/0_prologue/prologue dark_room.png"

## Моргание играет внутри образа и не останавливает реплики; трансформ тега сохраняется.
image prologue head_blink:
    "prologue head"
    pause 0.1
    "prologue head_flick" with Dissolve(0.2)
    pause 0.6
    "prologue head" with Dissolve(0.2)

image prologue_note_bg = "images/0_prologue/prologue_hand anim bg.png"
image prologue_note_paper = "images/0_prologue/prologue_note_paper.png"

image prologue_pencil_close = "images/0_prologue/prologue pencil_close.png"

image prologue_hand_left = "images/0_prologue/prologue_hand_left.png"
image prologue_hand_right = "images/0_prologue/prologue_hand_right rest.png"
image prologue_hand_right_move = "images/0_prologue/prologue_hand_right move.png"
image prologue_hand_right_write = "images/0_prologue/prologue_hand_right write.png"

## Стили, переходы, состояние

style prologue_titles_text is default:
    font "fonts/roboto_condensed_regular.ttf"
    color "#ff0000"
    outlines [(2, "#1a1712d9", 0, 0)]
    slow_cps 0

## Титр: штрих группы show_text (tint 0 — свой цвет стиля), шрифт примеряется F8 (dev).
## Остальные аргументы — свойства текста, например slow_cps=25: титр печатается по буквам.
init python:
    def prologue_title(text, size, **properties):
        return At(sm_font_preview_text(text, style="prologue_titles_text", size=size, **properties),
            scratch("show_text", tint=0.0))

default note_hover_pencil = False
default note_eye_crumpled = False
default note_eye_stack = False
default note_eye_palms = False

## Вступительные титры

label prologue_titles:

    $ fx_vignette = True
    $ quick_menu = False
    $ sm_parallax_off = True

    $ mplay("opening/opening_titles", fadein=4.0)

    $ click_skip_block = True

    scene black with Dissolve(1.0)

    pause 1.0

    show expression prologue_title(_("HINTERLAND MOOD"), 130) as prologue_titles_text:
        truecenter
        yoffset -15
        align (0.5, 0.5)
        subpixel True
    with Dissolve(3.5)

    pause 3.0

    hide prologue_titles_text with Dissolve(2.0)

    pause 1.0

    show expression prologue_title(_("ПО РАССКАЗУ РОМАНА ЧЕРНОГО"), 50) as prologue_titles_text_2:
        truecenter
        align (0.5, 0.5)
        subpixel True
    with Dissolve(3.0)

    pause 3.0

    jump prologue_scene

## Сцена

label prologue_scene:

    scene black with Dissolve(3.0)

    $ sm_parallax_off = False

    pause 0.3

    scene prologue_dark_room with Dissolve(4.0):
        zoom 1.0
        truecenter
        subpixel True
        parallel:
            linear 30.5 zoom 1.05
        parallel:
            breath_brightness(-0.01, -0.04, 6.0)

    $ mplay("opening/prologue_1", fadein=10.0, fadeout=18.0, volume=1.3)

    $ click_skip_block = False
    $ quick_menu = True

    "Чтобы заговорить о чём-то тяжёлом, лучше всего для начала представиться."

    ## Голова — ближний план. Картинка упирается в края кадра: стартовый зум 1.05
    ## закрывает сдвиг parallax.near до 48 px, при большем near поднять.
    show prologue head:
        zoom 1.05 alpha 0.0
        truecenter
        subpixel True
        parallel:
            function parallax_near_f
        parallel:
            linear 36.5 zoom 1.2
        parallel:
            linear 8.0 alpha 1.0

    ## Новый ATL наследует текущий zoom комнаты: наезд продолжается без скачка.
    show prologue_dark_room:
        parallel:
            linear 25.0 zoom 1.15
        parallel:
            linear 8.0 blur 1.0
        parallel:
            brightness_to(-0.07, 7.0)

    "Так сказать..."
    show prologue head_blink
    "...вспомнить, кто ты есть."

    show prologue_head_bg behind prologue:
        zoom 1.0 alpha 0.0
        parallel:
            linear 50.5 zoom 1.2
        parallel:
            linear 4.0 alpha 1.0
        parallel:
            breath_brightness(-0.01, -0.04, 6.0)

    "Меня зовут Марина Александровна Шрайбер."

    show prologue head_blink

    "Я пишу эти строки не в первый раз."

    pause 1.0

    "Сейчас я довольно далеко от места, что называла домом."
    "Кажется, осталось позади всё, что когда-то было мне ценно."

    $ click_skip_block = True
    window auto hide

    pause 1.0

    $ click_skip_block = False
    "{cps=5}...{/cps}"

    # "Сейчас у меня нет дома."

    show prologue head_blink
    hide prologue_dark_room
    show prologue_note_paper_0 behind prologue_head_bg:
        truecenter
        subpixel True
    ## Без стартовых значений: zoom и alpha наследуются, фон не прыгает.
    show prologue_head_bg behind prologue:
        parallel:
            linear 50.5 zoom 1.2
        parallel:
            linear 22.0 alpha 0.0

    "Я нахожусь здесь после нервного срыва, что разрушил мои и без того распадавшуюся на части жизнь и подорванное здоровье."
    # 

    "То был не первый мой срыв, и не второй, если говорить начистоту."

    pause 1.0

    "Но прошлые разы не шли с этим ни в какое сравнение."

    $ click_skip_block = True
    window auto hide

    show prologue head:
        linear 11.0 alpha 0.0
    show prologue_note_paper_0:
        parallel:
            linear 25.0 zoom 1.05
        parallel:
            breath_brightness(-0.01, -0.07, 8.0)
    with Dissolve(3.0)

    $ click_skip_block = False
    # sdkjfbsokdfg[r]
    "Это письмо..."
    "...должно помочь мне пережить произошедшее."

    show prologue_note_paper_0:
        parallel:
            linear 45.0 zoom 1.1

## Начало письма; отдельный вход каталога сцен.

label .letter:

    $ note_hover_pencil = False
    $ note_eye_crumpled = False
    $ note_eye_stack = False
    $ note_eye_palms = False

    window auto hide

    # "Долго я не находила в себе сил, чтобы записать случившееся."
    # "Ушло много попыток."

    "Долго я не находила в себе сил, чтобы записать случившееся."
    "Ушло много попыток."
    
    # "Даже чтобы просто вспоминать призошедшее:"

    pause 1.0

    "Меня трясло."
    "Рвало."
    "Руки непроизвольно тянулись закрыть лицо."
    "Хотелось спрятаться в ладонях от страшного мира, прямо как в детстве..."
    "Лишь бы не вспоминать."

    # "{sc=0.3:2}Не было сил вспоминать: меня трясло, рвало, руки непроизвольно тянулись закрыть лицо.{/sc}"

    ## Подсветка карандаша при наведении на «ВЗЯТЬ»: последнее число — прибавка яркости.
    ## image выполняется при запуске игры, здесь он только для удобства правки.
    image prologue_note_pencil = hover_lit("images/0_prologue/prologue_note_pencil.png", "note_hover_pencil", -0.1)

    show prologue_note_paper_0:
        parallel:
            linear 3.0 blur 7.15
        parallel:
            brightness_to(-0.23, 3.0)
    ## Наезд камерой из camera_fx: кнопка «ВЗЯТЬ» (follow_camera) повторяет её зум.
    $ click_skip_block = True
    camera at camera_push((0.5, 0.5), 1.0, 1.07, 30.0)
    scene prologue_note_bg at breath_brightness(-0.01, -0.05, 6.0)
    show prologue_note_paper at placed((990, 455), (0.5, 0.5))
    show prologue_note_pencil at placed((1264, 431), (0.5, 0.5))
    show prologue_hand_left at placed((271, 417))
    show prologue_hand_right at placed((1358, 468))
    with Dissolve(3.0)

    window auto hide

    pause 0.5

    ## Блокировщик выше сценовых кнопок и съел бы клики по ним.
    $ click_skip_block = False

    ## Осмотр стола: развилки нет, но каждый глазик обязателен кликом.
    ## Ранний пропуск обходит осмотр целиком; поздний выбирает пункты по очереди,
    ## непрочитанная реплика останавливает его как обычно.
    if not renpy.is_skipping():
        while not (note_eye_crumpled and note_eye_stack and note_eye_palms):
            menu(screen="scene_choice", follow=follow_camera(), skippable=True):
                "Скомканная бумажка" (icon=GLOW_ICON_INSPECT, pos=(1774, 353), size=(220, 150)) if not note_eye_crumpled:
                    $ note_eye_crumpled = True
                    "Очередной неудачный черновик."
                    "В перечёркнутых карандашом строках {sc=0.3:2.5}я снова вижу его.{/sc}"
                    "Нельзя отвлекаться."
                "Стопка бумаги" (icon=GLOW_ICON_INSPECT, bg="light", pos=(212, 153), size=(220, 150)) if not note_eye_stack:
                    $ note_eye_stack = True
                    "В этот раз точно получится."
                    "Должно получиться."
                    "В любом случае, на другую попытку я уже не найду сил."
                "Ладони" (icon=GLOW_ICON_INSPECT, pos=(581, 773), size=(220, 150)) if not note_eye_palms:
                    $ note_eye_palms = True
                    "Сейчас мои руки послушны."
                    "Перестали дрожать."
                    "Это добрый знак."
                with Dissolve(0.2)

    $ click_skip_block = True
    window auto hide

    pause 0.7

    $ click_skip_block = False

    "Обо всём случившемся невыносимо думать."
    "Но я должна излить наружу то, что пожирает меня изнутри."

    $ click_skip_block = True
    pause 0.4
    $ click_skip_block = False

    ## Координаты — карандаш в кадре без зума; follow_camera переносит их за камерой.
    if not renpy.is_skipping():
        menu(screen="scene_choice", follow=follow_camera(), skippable=True):
            "ВЗЯТЬ" (bg="light", pos=(1264, 431), size=(260, 140), click_volume=0.75,
                    hovered=SetVariable("note_hover_pencil", True),
                    unhovered=SetVariable("note_hover_pencil", False)):
                ## Тишина в очереди канала отодвигает звук от клика, не задерживая сцену.
                $ sm_audio_play(("<silence 0.5>", "audio/sfx/prologue/pencil_grab.ogg"), overlap=True)
            with Dissolve(0.2)

    ## После закрытия экрана unhovered не вызывается.
    $ note_hover_pencil = False
    window auto

    $ dismiss_off()

    show prologue_hand_left:
        subpixel True
        easein 1.0 placed((261, 427))

    show prologue_hand_right_move:
        subpixel True
        anchor (0.0, 0.0)
        pos (1358, 468)
        linear 0.4 pos (1217, 211)
    hide prologue_hand_right
    with Dissolve(0.1)
    $ pause(0.2)

    ## Позы на разных холстах совмещены по кончику карандаша.
    show prologue_hand_right_write:
        subpixel True
        anchor (0.0, 0.0)
        pos (1217, 211)
        easein 1.2 pos (1050, 198) blur 1.5
    hide prologue_hand_right_move
    hide prologue_note_pencil
    with Dissolve(0.1)
    $ dismiss_on()

    $ click_skip_block = True
    camera:
        zoom 1.0
        truecenter
        subpixel True
        linear 30.0 zoom 1.07

    scene prologue_pencil_close:
        breath_brightness(-0.01, -0.07, 6.0)
    ## Подъезд — через ypos: shake каждый кадр перезаписывает xoffset/yoffset.
    show prologue_pencil_close_hand:
        subpixel True
        xalign 0.5 yanchor 1.0 ypos 930
        parallel:
            shake(1.5)
        parallel:
            breath_brightness(-0.01, -0.06, 6.0)
        parallel:
            easein 1.0 xalign 0.5 yanchor 1.0 ypos 980
            linear 40.0 ypos 1030
    with Dissolve(1.3)

    $ click_skip_block = False
    "Я не уверена, что осмелюсь вернуться к карандашу и бумаге снова."
    # ", так что это будет спринтерский забег."

    pause 1.0

    "Это будет моя последняя попытка. Так сказать... спринтерский забег."
    "Я расскажу всё на одном дыхании. Здесь и сейчас."

    $ quick_menu = False

    $ mstop(fadeout=14.0)

    ## Граница между прологом и первой главой. Камера сбрасывается уже на чёрном:
    ## до растворения сброс рывком отъехал бы от наезда кадра.
    $ click_skip_block = True
    scene black with Dissolve(2.0)
    camera:
        zoom 1.0
        truecenter
        subpixel True
    $ fx_vignette = False
    $ pause(1.2)

    jump chapter_1_scene_1
