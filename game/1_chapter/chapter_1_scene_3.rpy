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

## Правый магнит остаётся над авторским цветовым мазком; сдвигается сам лист.
image chapter_1 scene_3_fridge_hanging = Composite((1920, 1080),
    (0, 0), "images/1_chapter/owner_review/chapter_1_review_fridge base.png",
    (1060, 76), "images/1_chapter/owner_review/chapter_1_review_fridge portrait_right.png",
    (726, 239), "images/1_chapter/owner_review/chapter_1_review_fridge family_drawing.png",
    (1097, 41), "images/1_chapter/owner_review/chapter_1_review_fridge right_magnet.png")

image chapter_1 scene_3_fridge = Composite((1920, 1080),
    (0, 0), "chapter_1 scene_3_fridge_hanging",
    (897, 172), "images/1_chapter/owner_review/chapter_1_review_fridge front_magnet.png")

image chapter_1 scene_3_fridge_new_drawing = Composite((1920, 1080),
    (0, 0), "chapter_1 scene_3_fridge_hanging",
    (793, 217), "images/1_chapter/owner_review/chapter_1_review_fridge new_drawing.png",
    (897, 172), "images/1_chapter/owner_review/chapter_1_review_fridge front_magnet.png")

## Настя в детской — планы глубины: комната сзади, Настя спереди; три настроения на одном
## фоне. Имена прежних цельных кадров сохранены — слои путями к файлам.
image chapter_1 scene_3_children_room_girl_neutral = depth_scene(
    "images/1_chapter/child_room/chapter_1 scene_3_children_room_bg.png",
    "images/1_chapter/child_room/chapter_1 scene_3_children_room nast.png")
image chapter_1 scene_3_children_room_girl_sad = depth_scene(
    "images/1_chapter/child_room/chapter_1 scene_3_children_room_bg.png",
    "images/1_chapter/child_room/chapter_1 scene_3_children_room nast_sad.png")
## Плачет: слёзы — слой поверх лица в той же группе, стекают по щекам (water: flow —
## участок слоя по вертикали, px), как у Марины в сцене 2.
image chapter_1 scene_3_children_room_girl_crying = depth_scene(
    "images/1_chapter/child_room/chapter_1 scene_3_children_room_bg.png",
    ("images/1_chapter/child_room/chapter_1 scene_3_children_room nast_very_sad.png",
        At("images/1_chapter/child_room/chapter_1 scene_3_children_room nast_very_sad tears.png",
            water(flow=(231, 453), run=15.0, hold=0.0, fade=6.0, fade_to=0.5))))

image chapter_1_fridge_drawing = "images/1_chapter/owner_review/chapter_1_review_fridge new_drawing.png"
image chapter_1_fridge_magnet = "images/1_chapter/owner_review/chapter_1_review_fridge front_magnet.png"

default c1s3_teaparty_choice = None
default c1s3_neighbor_choice = None

## Сцена

label chapter_1_scene_3:

    $ quick_menu = True

    ## ══════════ КАДР 1 · ДЕТСКАЯ, ПОЛ ══════════
    ## Из чёрного. Зум 1.10 — запас краёв под поворот взгляда в конце кадра.
    window auto hide
    camera:
        subpixel True
        align (0.5, 0.5)
        rotate 0.0
        xoffset 0.0 yoffset 0.0
        zoom 1.10
        linear sm_motion_time(30.0) zoom 1.15
    scene chapter_1 scene_3_children_room_floor:
        breath_brightness(-0.03, -0.08, 6.0)
    with Dissolve(3.0)

    "Моя дочь как раз проходила через сложный период взросления..."
    "...и невыносимо трепала наши нервы в процессе."

    ## Взгляд уходит влево — и в растворение на холодильник.
    window auto hide
    camera:
        subpixel True
        ease sm_motion_time(0.85) xoffset int(80 * sm_motion_scale())
    pause sm_motion_time(0.85)

    ## ══════════ КАДР 2 · ХОЛОДИЛЬНИК ══════════
    ## Наезд на рисунки. Дыхания нет: яркость ровная, пока новый рисунок не повешен.
    camera at camera_push((0.56, 0.42), 1.02, 1.09, 30.0)
    scene chapter_1 scene_3_fridge
    with Dissolve(0.8)

    "То есть вела себя как обычно, но всё же чуть-чуть беспокойней, а это о чём-то да говорит."
    "Она могла отказываться от еды \"неправильного\" цвета."
    "Или отказывалась идти на прогулку, пока не дорисует."
    "Последней её потрясающей выдумкой был панический страх оставаться дома одной."

    ## Передний магнит снят: новый лист выезжает снизу, магнит проявляется поверх.
    window auto hide
    scene chapter_1 scene_3_fridge_hanging
    show chapter_1_fridge_drawing zorder 1 at move_between((793, 1080), (793, 217), t=sm_motion_time(0.7))
    pause sm_motion_time(0.7)
    show chapter_1_fridge_magnet zorder 2 at placed((897, 172)), show_hide(0.18)
    pause 0.18

    ## Статическая сборка даёт дальнейшим репликам и сейвам один законченный кадр.
    ## На реплике он темнеет до нижней границы: выход из холодильника — через затемнение.
    scene chapter_1 scene_3_fridge_new_drawing:
        fade_brightness(0.0, -0.09, 8.0)

    # "Последней её потрясающей выдумкой был панический страх оставаться дома одной."

    ## ══════════ КАДР 3 · НАСТЯ ══════════
    ## Наезд на лицо.
    window auto hide
    camera at camera_push((0.38, 0.27), 1.02, 1.08, 18.0)
    scene chapter_1 scene_3_children_room_girl_neutral:
        breath_brightness(-0.03, -0.08, 6.0)
    with Dissolve(2.0)

    nas "Спасибо, что побыла на нашем чаепитии! Полли не пришёл сегодня..."
    nas "Как тебе профессор Косолап?"

    ## ══════════ КАДР 4 · ЧАЕПИТИЕ ══════════
    ## Наезд на профессора Косолапа.
    window auto hide
    camera at camera_push((0.25, 0.32), 1.02, 1.08, 30.0)
    scene chapter_1 scene_3_toys:
        breath_brightness(-0.03, -0.08, 6.0)
    with Dissolve(1.0)

    ## Выбор влияет на дальнейшее — меню ждёт игрока и при пропуске. Кнопки разбросаны по
    ## кадру; двигать — Choice Placer (F7).
    menu(screen="scene_choice", follow=follow_camera()):
        "\"Очаровашка!\"" (pos=(620, 180), size=(330, 165)):
            pause 0.5
            $ c1s3_teaparty_choice = "charming"
            mar "Очень милый медведь! А какие манеры!"
            nas "А то! Выпускник Лесной академии!"

        "\"Зануда!\"" (pos=(1180, 330), size=(330, 165)):
            pause 0.5
            $ c1s3_teaparty_choice = "boring"
            mar "Его лекция о мёдоведении была совершенно ни к месту!"
            nas "Он очень гордится своей научной... Штукой!"

        "\"Странный!\"" (pos=(330, 840), size=(330, 165)):
            pause 0.5
            $ c1s3_teaparty_choice = "strange"
            mar "Кажется, он помешан на еловых шишках..."
            nas "В лесу нет конфеток! Вот и приходится шишами чай закусывать..."

        "\"А где Полли?\"" (pos=(1250, 880), size=(330, 165)):
            pause 0.5
            $ c1s3_teaparty_choice = "where_is_polly"
            mar "Я стеснялась спросить! А где Полли?"
            nas "Он испугался и сбежал... Трусишка!"

    ## ══════════ КАДР 5 · НАСТЯ МРАЧНЕЕТ ══════════
    window auto hide
    camera at camera_push((0.42, 0.33), 1.03, 1.10, 16.0)
    scene chapter_1 scene_3_children_room_girl_sad:
        breath_brightness(-0.04, -0.09, 6.0)
    with Dissolve(1.0)

    mar "Я пойду встречу папу с работы. Посиди, пока одна..."

    ## ══════════ КАДР 6 · ИСТЕРИКА ══════════
    ## Склейка встык на крик, окно диалога остаётся (show, не scene). Камера продолжает
    ## наезд прошлого кадра.
    show chapter_1 scene_3_children_room_girl_crying:
        breath_brightness(-0.04, -0.09, 6.0)

    nas "НЕТ!"
    nas "НЕ УХОДИ!"
    mar "Почему?.."
    nas "ПОЖАЛУЙСТА!"

    ## ══════════ КАДР 7 · ПРЫЖКИ НА ДИВАНЕ ══════════
    ## Вход через чёрный. Кадр прыжков (c1s3_sofa_jump_bg) подставляется в тег первого
    ## кадра; камера вздрагивает на приземлении — pause до толчка равен взлёту и смазу.
    ## При «меньше движения» кадр стоит.
    window auto hide
    scene black with Dissolve(1.0)

    pause 0.4

    if sm_reduced_motion():
        camera
        scene chapter_1 scene_3_sofa_tv_1:
            breath_brightness(-0.03, -0.08, 6.0)
    else:
        camera:
            subpixel True
            align (0.5, 0.5)
            rotate 0.0
            xoffset 0.0 yoffset 0.0
            zoom 1.04
            block:
                pause 0.41
                linear 0.04 yoffset 5.0
                easein 0.23 yoffset 0.0
                repeat
        scene chapter_1 scene_3_sofa_tv_1:
            "chapter_1 scene_3_sofa_jump"
            breath_brightness(-0.03, -0.08, 6.0)
    with Dissolve(1.5)

    "Стоило нам с Витей обоим ненадолго отлучиться, как наша принцесса начинала вопить, греметь кастрюлями, орать под телевизор на полную громкость, в общем, стоять на голове."

    ## ══════════ КАДР 8 · ПОДЪЕЗД ══════════
    ## Наезд вверх по лестнице, к двери.
    window auto hide
    camera at camera_push((0.54, 0.40), 1.02, 1.10, 26.0)
    scene chapter_1 scene_3_entrance:
        breath_brightness(-0.04, -0.09, 6.0)
    with Dissolve(2.0)

    "Мы пыталась с ней по-хорошему поговорить, объяснить, что взрослым девочкам так вести себя должно быть стыдно."
    "Потом просто ругались."

    ## ══════════ КАДР 9 · НАСТЯ СВЕРХУ ══════════
    ## Один наезд на лицо через два кадра: на втором руки растворяются (show без ATL —
    ## дыхание и камера не сбрасываются).
    window auto hide
    camera at camera_push((0.50, 0.42), 1.03, 1.14, 45.0)
    scene chapter_1 scene_3_daughter_top:
        breath_brightness(-0.04, -0.09, 6.0)
    with Dissolve(1.0)

    vit "Это ни в какие рамки. Ну что это за поведение, а?"

    show chapter_1 scene_3_daughter_top_close
    with Dissolve(0.8)

    "Вот она: охрипшая от крика, наша маленькая принцесса истерии, с красным заплаканным лицом."

    pause 0.5

    vit "Мама и так почти целыми днями дома торчит. Тебя нельзя оставить на час?"

    pause 0.5

    nas "Нельзя..."

    pause 0.5

    "Один раз мне пришлось выйти из дома, потому что закончились лекарства."
    "Я оставила её одну всего на жалкие десять минут."
    "А по возвращению у двери меня уже встречали соседи..."

    ## ══════════ КАДР 10 · СОСЕДКА ══════════
    ## Наезд на фигуру наверху лестницы.
    window auto hide
    camera at camera_push((0.50, 0.35), 1.03, 1.10, 14.0)
    scene chapter_1 scene_3_entrance_neighbor:
        breath_brightness(-0.04, -0.09, 6.0)
    with Dissolve(1.0)

    sos "Ну наконец-то явились! И что это за дела?"
    sos "Вам самим нормально жить с таким воем?"
    sos "Вы пробовали воспитывать ребёнка?"

    ## ══════════ КАДР 11 · ВТОРАЯ СОСЕДКА ══════════
    ## Склейка встык: лицо вырастает перед камерой, камера отшатывается.
    camera at camera_settle((0.26, 0.55), 1.12, 1.04, 0.6)
    show chapter_1 scene_3_entrance_neighbors:
        breath_brightness(-0.04, -0.09, 6.0)

    ## Выбор влияет на дальнейшее — меню ждёт игрока и при пропуске; двигать — F7.
    menu(screen="scene_choice", follow=follow_camera()):
        "Простите..." (pos=(608, 746), size=(330, 165)):
            pause 0.5
            $ c1s3_neighbor_choice = "apologize"
            ## Извинилась: камера медленно уходит мимо соседки к двери наверху.
            camera at camera_push((0.50, 0.30), 1.04, 1.16, 20.0)
            mar "У неё просто тяжёлый возраст. Извините, пожалуйста."
            sos "Ну Мариш, это несерьёзно. Ребёнка надо воспитывать!"

            pause 1.0

            "Я знала. Просто не понимала, как. Мы пытались разобраться..."

        "Заткнитесь!" (pos=(963, 542), size=(330, 165)):
            pause 0.5
            $ c1s3_neighbor_choice = "confront"
            ## Сорвалась: удар камерой в лицо соседке.
            camera at camera_settle((0.26, 0.55), 1.14, 1.07, 0.4)
            mar "И вы тоже разораться решили?! Закройте рты и идите домой!"

            pause 0.5

            sos "О, психованная семейка! Ничего-ничего, потом вызовем милицию..."

            pause 0.5

            "Какое право они не имели нравоучать нас?!"
            "Пусть лучше приглядывают за своими детьми, болтающимися без дела по двору, как оборванцы."

    ## ══════════ КАДР 12 · МАРИНА НА ДИВАНЕ ══════════
    ## После «Простите» — долгое растворение, после «Заткнитесь» — склейка встык.
    window auto hide
    camera at camera_push((0.75, 0.35), 1.02, 1.10, 30.0)
    scene chapter_1 scene_3_sofa_marina:
        breath_brightness(-0.04, -0.09, 6.0)
    if c1s3_neighbor_choice == "apologize":
        with Dissolve(2.5)

    "Конечно, мы ходили с дочкой к психологу."
    "Именно там, далеко не на первом сеансе, Настя шёпотом рассказала, что на самом деле не боится оставаться одна."

    ## ══════════ КАДР 13 · НАСТЯ ШЁПОТОМ ══════════
    ## Очень долгий непрерывный наезд на лицо Насти — на весь разговор.
    window auto hide
    camera at camera_push((0.37, 0.42), 1.02, 1.22, 90.0)
    scene chapter_1 scene_3_sofa_daughter:
        breath_brightness(-0.04, -0.09, 6.0)
    with Dissolve(2.0)

    nas "{sc}Он{/sc} приходит, когда дома становится слишком тихо..."
    mar "Кто приходит, дорогая?"
    vit "Кто-кто?.. Это Полли? Или как там его..."
    nas "Нет. Полли сбежал... {sc}Он{/sc}, как я, испугался..."
    vit "Твоего нового воображаемого друга?"

    # nas "Мы с ним не друзья..."
    nas "{sc}Он{/sc} мне не друг..."

    ## Кадр темнеет до нижней границы и замирает перед именем.
    show chapter_1 scene_3_sofa_daughter:
        brightness_to(-0.09, 4.0)

    vit "А кто же \"он\" тогда?"
    
    pause 1.0

    nas "Шаркающий человек."

    ## Тишина после имени.
    window auto hide

    pause 2.0

    camera

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
