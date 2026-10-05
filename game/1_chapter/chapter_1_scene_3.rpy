## Глава 1, сцена 3: детская → холодильник → чаепитие → истерика → подъезд → диван, «Шаркающий человек».

## Изображения

image chapter_1 scene_3_sofa_tv_1 = sm_tv_scene("images/1_chapter/chapter_1 scene_3_sofa_tv_1.png",
    C1S3_TV_POS, C1S3_TV_SIZE, ((2, 2), (402, 2), (402, 282), (2, 282)))
define C1S3_TV_POS = (1228, 118)
define C1S3_TV_SIZE = (404, 284)

## Настя скачет на диване: взлёт → смаз → приземление → смаз. Меняется только фон под
## одним экраном помех (смена кадра внутри композита сбрасывала бы цикл шума). Камера в
## сцене вздрагивает на приземлении: паузы здесь и pause камеры менять вместе.
image c1s3_sofa_jump_bg:
    "images/1_chapter/chapter_1 scene_3_sofa_tv_1.png"
    pause 0.34
    "images/1_chapter/chapter_1 scene_3_sofa_tv.png"
    pause 0.07
    "images/1_chapter/chapter_1 scene_3_sofa_tv_2.png"
    pause 0.2
    "images/1_chapter/chapter_1 scene_3_sofa_tv.png"
    pause 0.07
    repeat
image chapter_1 scene_3_sofa_jump = sm_tv_scene("c1s3_sofa_jump_bg",
    C1S3_TV_POS, C1S3_TV_SIZE, ((2, 2), (402, 2), (402, 282), (2, 282)))

## Настя в детской — планы глубины: комната сзади, Настя спереди; три настроения на одном
## фоне. Имена прежних цельных кадров сохранены — слои путями к файлам.
## Спокойная Настя говорит: кадры «молчит» и «говорит» меняются по слогам её реплик.
image chapter_1 scene_3_children_room_girl_neutral = depth_scene(
    "images/1_chapter/child_room/chapter_1 scene_3_children_room_bg.png",
    TalkFrames("images/1_chapter/child_room/chapter_1 scene_3_children_room nast.png",
        "images/1_chapter/child_room/chapter_1 scene_3_children_room nast_say.png", "nas", fade=0.1))
## Мрачнеет: слёзы стоят в глазах — слой поверх лица, только блестят (water без flow —
## не стекают). Настя со слезами в одной группе дрожит всё сильнее (shake_grow: размах,
## px, и секунды до максимума), комната стоит. Часы дрожи — флаг c1s3_sad_shake, сцена
## взводит его на этом кадре: кадр истерики продолжает дрожь с того же места, вдвое сильнее.
image chapter_1 scene_3_children_room_girl_sad = depth_scene(
    "images/1_chapter/child_room/chapter_1 scene_3_children_room_bg.png",
    At(Fixed("images/1_chapter/child_room/chapter_1 scene_3_children_room nast_sad.png",
            At("images/1_chapter/chapter_1 scene_3_children_room_girl_sad tears.png", water()),
            xysize=(1920, 1080)),
        shake_grow(0.75, 4.0, start="c1s3_sad_shake")))
## Плачет: слёзы — слой поверх лица в той же группе, стекают по щекам (water: flow —
## участок слоя по вертикали, px), как у Марины в сцене 2; к показу уже стекли на 15 %,
## через 15 с начинают тускнеть. Крик «дышит»: рот (эллипс в px слоя) плавно раскрывается
## примерно на 5 % и смыкается обратно без пауз — сила отрицательная, вниз уходит только
## нижняя губа. Эффект на самом слое лица: эллипс едет вместе с планом при параллаксе.
## Настя дрожит вдвое сильнее прошлого кадра по тем же часам c1s3_sad_shake (дрожь уже
## набрана, на склейке удваивается) и со слезами отдельно от комнаты медленно наезжает
## вокруг лица.
transform c1s3_crying_push:
    subpixel True
    transform_anchor True
    anchor (0.45, 0.3) pos (0.45, 0.3)
    zoom (1.08 if sm_reduced_motion() else 1.0)
    ease sm_motion_time(20.0) zoom 1.08

image chapter_1 scene_3_children_room_girl_crying = depth_scene(
    "images/1_chapter/child_room/chapter_1 scene_3_children_room_bg.png",
    At(Fixed(At("images/1_chapter/child_room/chapter_1 scene_3_children_room nast_very_sad.png",
                mouth_loop((857, 408), (120, 58), strength=-0.65, period=4.0, hold=0.0, ease=2.0)),
            At("images/1_chapter/child_room/chapter_1 scene_3_children_room nast_very_sad tears.png",
                water(flow=(231, 453), run=15.0, hold=0.0, fade=6.0, fade_to=0.5, head=0.15)),
            xysize=(1920, 1080)),
        c1s3_crying_push, shake_grow(1.5, 4.0, start="c1s3_sad_shake")))

## Настя сверху, крупно — планы глубины: пол, Настя (со слезами и выбившимися прядями в
## одной группе), ближе всех — руки Вити. Пол и Настя весь кадр медленно наезжают вокруг
## лица, руки стоят на месте и только плавно плывут вверх-вниз — камера в сцене не зумит.
## Слёзы к показу стекли на треть, дотекают и не тускнеют; рот «дышит», как в кадре
## истерики; пряди колышутся (wind_warp: эллипс и корень в px слоя), лицо стоит. Параллакс
## между планами приглушён до пятой части (step).
transform c1s3_top_close_push:
    subpixel True
    transform_anchor True
    anchor (0.5, 0.42) pos (0.5, 0.42)
    zoom (1.16 if sm_reduced_motion() else 1.0)
    ease sm_motion_time(40.0) zoom 1.16

transform c1s3_top_close_wag:
    subpixel True
    yoffset (5.0 * sm_motion_scale())
    block:
        ease 1.0 yoffset (-5.0 * sm_motion_scale())
        ease 1.0 yoffset (5.0 * sm_motion_scale())
        repeat

image chapter_1 scene_3_daughter_top_close = depth_scene(
    At("images/1_chapter/chapter_1 scene_3_daughter_top_close.png", c1s3_top_close_push),
    (At("images/1_chapter/chapter_1 scene_3_daughter_top_close_child.png",
            mouth_loop((915, 510), (105, 75), strength=-0.9, period=4.0, hold=0.0, ease=2.0),
            c1s3_top_close_push),
        At("images/1_chapter/chapter_1 scene_3_daughter_top_close_tears.png",
            water(flow=(324, 528), run=15.0, head=0.35, fade_to=1.0),
            c1s3_top_close_push),
        At("images/1_chapter/chapter_1 scene_3_daughter_top_close_volosy.png",
            wind_warp((920, 260), (700, 520), (920, 40), amp=2.0, speed=1.0),
            c1s3_top_close_push)),
    At("images/1_chapter/chapter_1 scene_3_daughter_top_close_hands.png", c1s3_top_close_wag),
    step=0.2)

## Вторая соседка — прозрачный спрайт своим тегом поверх кадра с первой: тихо выдвигается
## из-за левого края на своё место (pos — место, px), проявляясь из прозрачности; сдвиг —
## 15% ширины экрана, кончается вместе с проявлением. На ходу чуть притопывает: три
## мелких шага (yoffset, px; перенос веса rotate, ° — вокруг ног). При «меньше движения» —
## только проявление.
## Говорит на репликах соседки (ключ "sos"): кадры «молчит» и «говорит» меняются по слогам,
## каждое открытие рта — одной длины (hold) и одинаковое: между открытиями рот закрыт
## не меньше gap секунд — дольше растворения кадров (fade), так что каждое раскрытие
## проходит целиком.
image c1s3_neighbor_2 = TalkFrames("images/1_chapter/chapter_1 scene_3_entrance_neighbors.png",
    "images/1_chapter/chapter_1 scene_3_entrance_neighbors say.png", "sos", fade=0.1, hold=0.2, gap=0.15)
transform c1s3_neighbor_2_enter:
    subpixel True
    transform_anchor True
    anchor (0.245, 1.0)
    pos (470, 1080)
    alpha 0.0
    rotate 0.0
    xoffset (-288.0 * sm_motion_scale())
    parallel:
        easeout 1.5 alpha 1.0 xoffset 0.0
    parallel:
        easein 0.15 yoffset (6.0 * sm_motion_scale()) rotate (-0.6 * sm_motion_scale())
        easeout 0.35 yoffset 0.0 rotate 0.0
        easein 0.15 yoffset (5.0 * sm_motion_scale()) rotate (0.6 * sm_motion_scale())
        easeout 0.35 yoffset 0.0 rotate 0.0
        easein 0.15 yoffset (3.0 * sm_motion_scale()) rotate (-0.3 * sm_motion_scale())
        easeout 0.35 yoffset 0.0 rotate 0.0

## Пустая метка: её ATL запускает звук с задержкой от появления реплики, не дожидаясь клика.
image c1s3_sfx_cue = Null()

default c1s3_teaparty_choice = None
default c1s3_sad_shake = False
## Плач Насти (c1s1_nast_cry_step_2); handle нужен, чтобы глушить его за дверью подъезда.
default c1s3_cry_audio = None

init python:

    def c1s3_cry_reverb():
        """Плач в квартире: чистый, с лёгким эхом комнаты."""
        return renpy.audio.filter.Reverb(resonance=0.6, dampening=2000.0, wet=0.3, dry=0.9, delay_multiplier=1.6)

    def c1s3_cry_door_filter():
        """Плач из-за двери: тот же, но глухой (low-pass, Гц)."""
        return [renpy.audio.filter.Lowpass(900.0), c1s3_cry_reverb()]
default c1s3_neighbor_choice = None

## Сцена

label chapter_1_scene_3:

    $ quick_menu = True

    ## Постановка — смены кадра, паузы между репликами — идёт под click_skip_block: клик
    ## проматывает только реплики; Ctrl/«Пропуск» работают всегда. Меню и истерика — без
    ## пауз: выбор ждёт игрока, крики идут встык.

    ## ══════════ КАДР 1 · ДЕТСКАЯ, ПОЛ ══════════
    ## Из чёрного, медленный наезд. Пол детской и холодильник — без bloom (fx_frame): со
    ## следующего кадра он возвращается сам.
    $ click_skip_block = True
    window auto hide
    camera at camera_push((0.5, 0.5), 1.00, 1.09, 30.0)
    scene chapter_1 scene_3_children_room_floor:
        parallel:
            breath_brightness(-0.03, -0.08, 6.0)
        parallel:
            fx_frame(bloom=0.0)
    with Dissolve(3.0)
    $ click_skip_block = False

    "Моя дочь как раз проходила через сложный период взросления..."
    "...и невыносимо трепала наши нервы в процессе."

    $ click_skip_block = True
    window auto hide

    ## ══════════ КАДР 2 · ХОЛОДИЛЬНИК ══════════
    ## Наезд на рисунки. Дыхания нет: яркость ровная, пока новый рисунок не повешен.
    camera at camera_push((0.56, 0.42), 1.02, 1.09, 30.0)
    scene chapter_1 scene_3_fridge:
        fx_frame(bloom=0.0)
    with Dissolve(0.8)
    $ click_skip_block = False

    "То есть вела себя как обычно, но всё же чуть-чуть беспокойней, а это о чём-то да говорит."
    "Она могла отказываться от еды \"неправильного\" цвета."
    "Или отказывалась идти на прогулку, пока не дорисует."

    $ click_skip_block = True
    window auto hide
    ## Шорох бумаги — новый рисунок прижимают к дверце.
    $ sm_sfx("c1s3/c1s3_fridge_paper", volume=0.3)
    scene chapter_1 scene_3_fridge_new_drawing:
        parallel:
            fade_brightness(0.0, -0.09, 8.0)
        parallel:
            fx_frame(bloom=0.0)
    with Dissolve(0.8)

    pause 0.5

    "Последней её потрясающей выдумкой был панический страх оставаться дома одной."

    ## Поверх рисунка с семьёй появляется новый. Кадр темнеет до нижней границы: выход из
    ## холодильника — через затемнение. Камера не сбрасывается.


    # "Последней её потрясающей выдумкой был панический страх оставаться дома одной."

    ## ══════════ КАДР 3 · НАСТЯ ══════════
    ## Наезд на лицо.
    window auto hide
    camera at camera_push((0.38, 0.27), 1.02, 1.08, 18.0)
    scene chapter_1 scene_3_children_room_girl_neutral:
        breath_brightness(-0.03, -0.08, 6.0)
    with Dissolve(2.0)
    $ click_skip_block = False

    nas "Спасибо, что побыла на нашем чаепитии!" (callback=talk_callback("nas", drop=1))
    nas "А Полли не пришёл сегодня..." (callback=talk_callback("nas", drop=1))
    nas "Как тебе профессор Косолап?" (callback=talk_callback("nas", drop=1))

    ## ══════════ КАДР 4 · ЧАЕПИТИЕ ══════════
    ## Наезд на профессора Косолапа.
    $ click_skip_block = True
    window auto hide
    camera at camera_push((0.25, 0.32), 1.02, 1.08, 30.0)
    scene chapter_1 scene_3_toys:
        breath_brightness(-0.03, -0.08, 6.0)
    with Dissolve(1.0)
    $ click_skip_block = False

    ## Выбор влияет на дальнейшее — меню ждёт игрока и при пропуске. Кнопки разбросаны по
    ## кадру; двигать — Choice Placer (F7).
    menu(screen="scene_choice", follow=follow_camera()):
        "Очаровашка!" (pos=(309, 160), size=(330, 165)):
            $ click_skip_block = True
            pause 0.5
            $ click_skip_block = False
            $ c1s3_teaparty_choice = "charming"
            mar "Очень милый медведь! А какие манеры!"
            $ click_skip_block = True
            pause 0.5
            $ click_skip_block = False
            nas "А то! Выпускник Лесной академии!"

        "Зануда!" (pos=(608, 382), size=(330, 165)):
            $ click_skip_block = True
            pause 0.5
            $ click_skip_block = False
            $ c1s3_teaparty_choice = "boring"
            mar "Его лекция о мёдоведении была совершенно ни к месту!"
            $ click_skip_block = True
            pause 0.5
            $ click_skip_block = False
            nas "Он очень гордится своей научной... Штукой!"

        "Странный!" (pos=(328, 580), size=(330, 165)):
            $ click_skip_block = True
            pause 0.5
            $ click_skip_block = False
            $ c1s3_teaparty_choice = "strange"
            mar "Кажется, он помешан на еловых шишках..."
            $ click_skip_block = True
            pause 0.5
            $ click_skip_block = False
            nas "В лесу нет конфеток! Вот и приходится шишами чай закусывать..."

        "А где Полли?" (pos=(1052, 478), size=(330, 165)):
            $ click_skip_block = True
            pause 0.5
            $ click_skip_block = False
            $ c1s3_teaparty_choice = "where_is_polly"
            mar "Я стеснялась спросить! А где Полли?"
            $ click_skip_block = True
            pause 0.5
            $ click_skip_block = False
            nas "Он испугался и сбежал... Трусишка!"

    pause 1.0

    mar "Я пойду встречу папу с работы. Посиди, пока одна..."

    ## ══════════ КАДР 5 · НАСТЯ МРАЧНЕЕТ ══════════
    $ click_skip_block = True
    window auto hide
    camera at camera_push((0.42, 0.33), 1.03, 1.15, 26.0)
    $ c1s3_sad_shake = True
    scene chapter_1 scene_3_children_room_girl_sad:
        breath_brightness(-0.04, -0.09, 6.0)
    with Dissolve(3.0)
    $ click_skip_block = False

    pause 1.5

    ## ══════════ КАДР 6 · ИСТЕРИКА ══════════
    ## Склейка встык на крик, окно диалога остаётся (show, не scene). Камера продолжает
    ## наезд прошлого кадра; Настя в образе наезжает ещё и сама, отдельно от комнаты.
    show chapter_1 scene_3_children_room_girl_crying:
        breath_brightness(-0.04, -0.09, 6.0)
    with Dissolve(0.5)

    $ sm_sfx("c1s1/c1s1_nast_cry_step_1", tag="c1s3_cry")
    nas "НЕТ!"
    nas "НЕ УХОДИ!"
    mar "Почему?.."
    nas "ПОЖАЛУЙСТА!"
    $ c1s3_sad_shake = False

    # ## ══════════ КАДР 7 · ПРЫЖКИ НА ДИВАНЕ ══════════
    # ## Вход через чёрный. Кадр прыжков (c1s3_sofa_jump_bg) подставляется в тег первого
    # ## кадра; камера вздрагивает на приземлении — pause до толчка равен взлёту и смазу.
    # ## При «меньше движения» кадр стоит.
    # $ click_skip_block = True
    # window auto hide
    # scene black with Dissolve(1.0)

    # pause 0.4

    # if sm_reduced_motion():
    #     camera
    #     scene chapter_1 scene_3_sofa_tv_1:
    #         breath_brightness(-0.03, -0.08, 6.0)
    # else:
    #     camera:
    #         subpixel True
    #         align (0.5, 0.5)
    #         rotate 0.0
    #         xoffset 0.0 yoffset 0.0
    #         zoom 1.04
    #         block:
    #             pause 0.41
    #             linear 0.04 yoffset 5.0
    #             easein 0.23 yoffset 0.0
    #             repeat
    #     scene chapter_1 scene_3_sofa_tv_1:
    #         "chapter_1 scene_3_sofa_jump"
    #         breath_brightness(-0.03, -0.08, 6.0)
    # with Dissolve(1.5)
    # $ click_skip_block = False

    ## ══════════ КАДР 8 · ПОДЪЕЗД ══════════
    ## Наезд вверх по лестнице, к двери.
    $ click_skip_block = True
    window auto hide
    camera at camera_push((0.54, 0.40), 1.02, 1.10, 26.0)
    scene chapter_1 scene_3_entrance:
        breath_brightness(-0.04, -0.09, 6.0)
    with Dissolve(2.0)
    $ click_skip_block = False

    ## Кипиш за дверью — через секунду после появления первой строки.
    show c1s3_sfx_cue:
        pause 1.0
        function renpy.curry(sm_sfx_f)("c1s1/c1s1_nastya_solo_kipish", 1.5)
    "Стоило нам с Витей обоим ненадолго отлучиться, как наша принцесса начинала вопить, греметь кастрюлями, орать под телевизор на полную громкость, в общем, стоять на голове."
    "Мы пыталась с ней по-хорошему поговорить, объяснить, что взрослым девочкам так вести себя должно быть стыдно."
    "Потом просто ругались."

    ## ══════════ КАДР 9 · НАСТЯ СВЕРХУ ══════════
    ## Камера стоит: наезд на лицо идёт внутри кадра, планами пола и Насти, а руки должны
    ## оставаться на месте. Плач Насти идёт отсюда один раз до конца без фейда: здесь чисто,
    ## с эхом комнаты; на кадрах из подъезда дальше — глухо, из-за двери
    ## (c1s3_cry_door_filter), переключение — за время растворения кадра.
    $ click_skip_block = True
    window auto hide
    camera
    $ c1s3_cry_audio = sm_sfx("c1s1/c1s1_nast_cry_step_2", tag="c1s3_cry")
    $ sm_audio_set_filter(c1s3_cry_audio, c1s3_cry_reverb(), duration=0)
    scene chapter_1 scene_3_daughter_top_close:
        breath_brightness(-0.04, -0.09, 6.0)
    with Dissolve(3.0)
    $ click_skip_block = False

    vit "Это ни в какие рамки. Ну что это за поведение, а?"

    $ click_skip_block = True
    pause 0.5
    $ click_skip_block = False

    "Вот она: охрипшая от крика, наша маленькая принцесса истерии, с красным заплаканным лицом."

    $ click_skip_block = True
    pause 0.5
    $ click_skip_block = False

    vit "Мама и так почти целыми днями дома торчит. Тебя нельзя оставить на час?"

    $ click_skip_block = True
    pause 0.5
    $ click_skip_block = False

    nas "Нельзя..."

    $ click_skip_block = True
    pause 0.5
    $ click_skip_block = False

    "Один раз мне пришлось выйти из дома, потому что закончились лекарства."
    "Я оставила её одну всего на жалкие десять минут."

    ## ══════════ КАДР 10 · СОСЕДКА ══════════
    ## Наезд на фигуру наверху лестницы.
    $ click_skip_block = True
    window auto hide
    camera at camera_push((0.50, 0.35), 1.03, 1.10, 14.0)
    $ sm_audio_set_filter(c1s3_cry_audio, c1s3_cry_door_filter(), duration=1.0)
    scene chapter_1 scene_3_entrance_neighbor:
        breath_brightness(-0.04, -0.09, 6.0)
    with Dissolve(1.0)
    $ click_skip_block = False

    "А по возвращению у двери меня уже встречали соседи..."

    ## Вторая соседка выдвигается слева в тишине (1.5 с); три шага в звуке совпадают с тремя
    ## притопами (c1s3_neighbor_2_enter). Встала — ещё 0.5 с, и заговорила.
    $ click_skip_block = True
    window auto hide
    $ sm_sfx("c1s1/2_netrence_sosedka_footsteps", volume=0.8)
    show c1s3_neighbor_2 at c1s3_neighbor_2_enter, breath_brightness(-0.04, -0.09, 6.0)
    pause 2.0
    $ click_skip_block = False

    sos "Ну наконец-то явилась! И что это за дела?" (callback=talk_callback("sos", moves=4, hold=0.2, step=0.35))
    sos "Вам самим нормально жить с таким воем?" (callback=talk_callback("sos", drop=3))
    sos "Вы пробовали воспитывать ребёнка?" (callback=talk_callback("sos", drop=3))

    ## ══════════ КАДР 11 · ОТВЕТ СОСЕДКАМ ══════════
    ## Обе соседки в кадре; камера продолжает наезд.

    ## Выбор влияет на дальнейшее — меню ждёт игрока и при пропуске; двигать — F7.
    menu(screen="scene_choice", follow=follow_camera()):
        "Простите..." (pos=(962, 538), size=(330, 165)):
            $ click_skip_block = True
            pause 0.5
            $ click_skip_block = False
            $ c1s3_neighbor_choice = "apologize"
            ## Извинилась: камера медленно уходит мимо соседки к двери наверху.
            # camera at camera_push((0.50, 0.30), 1.04, 1.16, 20.0)
            mar "У неё просто тяжёлый возраст. Извините, пожалуйста."

            $ click_skip_block = True
            pause 0.5
            $ click_skip_block = False

            sos "Ну Мариш, это несерьёзно. Ребёнка надо воспитывать!" (callback=talk_callback("sos", moves=4, step=0.42))

            $ click_skip_block = True
            pause 1.0
            $ click_skip_block = False

            "Я знала. Просто не понимала, как. Мы пытались разобраться..."

        "Заткнитесь!" (pos=(619, 772), size=(330, 165)):
            $ click_skip_block = True
            pause 0.5
            $ click_skip_block = False
            $ c1s3_neighbor_choice = "confront"
            ## Сорвалась: удар камерой в лицо соседке.
            # camera at camera_settle((0.26, 0.55), 1.14, 1.07, 0.4)
            mar "И вы тоже разораться решили?! Закройте рты и идите домой!"

            $ click_skip_block = True
            pause 0.5
            $ click_skip_block = False

            sos "О, психованная семейка! Ничего-ничего, потом вызовем милицию..." (callback=talk_callback("sos", moves=5, step=0.42))

            $ click_skip_block = True
            pause 0.5
            $ click_skip_block = False

            "Какое право они не имели нравоучать нас?!"
            "Пусть лучше приглядывают за своими детьми, болтающимися без дела по двору, как оборванцы."

    ## ══════════ КАДР 12 · МАРИНА НА ДИВАНЕ ══════════
    ## После «Простите» — долгое растворение, после «Заткнитесь» — склейка встык.
    $ click_skip_block = True
    window auto hide
    camera at camera_push((0.75, 0.35), 1.02, 1.10, 30.0)
    scene chapter_1 scene_3_sofa_marina:
        breath_brightness(-0.04, -0.09, 6.0)
    if c1s3_neighbor_choice == "apologize":
        with Dissolve(2.5)
    $ click_skip_block = False

    "Конечно, мы ходили с дочкой к психологу."
    "Именно там, далеко не на первом сеансе, Настя шёпотом рассказала, что на самом деле не боится оставаться одна."

    ## ══════════ КАДР 13 · НАСТЯ ШЁПОТОМ ══════════
    ## Очень долгий непрерывный наезд на лицо Насти — на весь разговор.
    $ click_skip_block = True
    window auto hide
    camera at camera_push((0.37, 0.42), 1.02, 1.22, 90.0)
    scene chapter_1 scene_3_sofa_daughter:
        breath_brightness(-0.04, -0.09, 6.0)
    with Dissolve(2.0)
    $ click_skip_block = False

    nas "{sc}Он{/sc} приходит, когда дома становится слишком тихо..."

    $ click_skip_block = True
    pause 0.5
    $ click_skip_block = False

    mar "Кто приходит, дорогая?"

    $ click_skip_block = True
    pause 0.5
    $ click_skip_block = False

    vit "Кто-кто?.. Это Полли? Или как там его..."

    $ click_skip_block = True
    pause 0.5
    $ click_skip_block = False

    nas "Нет. Полли сбежал... {sc}Он{/sc}, как я, испугался..."

    $ click_skip_block = True
    pause 0.5
    $ click_skip_block = False

    vit "Твоего нового воображаемого друга?"

    $ click_skip_block = True
    pause 0.5
    $ click_skip_block = False

    # nas "Мы с ним не друзья..."
    nas "{sc}Он{/sc} мне не друг..."

    ## Кадр темнеет до нижней границы и замирает перед именем.
    show chapter_1 scene_3_sofa_daughter:
        brightness_to(-0.09, 4.0)

    $ click_skip_block = True
    pause 0.5
    $ click_skip_block = False

    vit "А кто же \"он\" тогда?"

    $ click_skip_block = True
    pause 1.0
    $ click_skip_block = False

    nas "Шаркающий человек."

    ## Тишина после имени.
    $ click_skip_block = True
    window auto hide

    pause 2.0

    camera
    $ click_skip_block = False

    ## Глава 2 ещё не подключена: вместо jump chapter_2_scene_1 — заглушка.
    jump end_dev_yet

## Конец готовой части: титр-заглушка и выход в главное меню.

label end_dev_yet:
    $ quick_menu = False
    $ sm_parallax_off = True

    scene black with Dissolve(1.0)

    show expression prologue_title(_("СПАСИБО, ЧТО ПРОШЛИ ДЕМОВЕРСИЮ ИГРЫ!"), 55) as prologue_titles_text_2:
        align (0.5, 0.45)
        subpixel True
    with Dissolve(2.0)

    pause

    ## jump main_menu остался бы в игре: флаг main_menu не взводится, параллакс не гаснет.
    $ MainMenu(confirm=False)()
