## Глава 1, сцена 3.

## Изображения

image chapter_1 scene_3_sofa_tv_1 = sm_tv_scene("images/1_chapter/chapter_1 scene_3_sofa_tv_1.png",
    C1S3_TV_POS, C1S3_TV_SIZE, ((2, 2), (402, 2), (402, 282), (2, 282)))
define C1S3_TV_POS = (1228, 118)
define C1S3_TV_SIZE = (404, 284)

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

image chapter_1_fridge_drawing = "images/1_chapter/owner_review/chapter_1_review_fridge new_drawing.png"
image chapter_1_fridge_magnet = "images/1_chapter/owner_review/chapter_1_review_fridge front_magnet.png"

default c1s3_teaparty_choice = None
default c1s3_neighbor_choice = None


label chapter_1_scene_3:

    camera at zoom(1.10), align(0.5, 0.5)
    scene chapter_1 scene_3_children_room_floor

    "Моя дочь как раз проходила через сложный период взросления и невыносимо трепала наши нервы в процессе."

    window hide
    ## Сдвиг кадра вправо направляет взгляд налево; зум закрывает края.
    camera at zoom(1.10), align(0.5, 0.5), offseting(0, 0, int(80 * sm_motion_scale()), 0, sm_motion_time(0.85))
    $ pause(sm_motion_time(0.85))
    camera
    scene chapter_1 scene_3_fridge
    with Dissolve(0.8)

    "То есть вела себя как обычно, но всё же чуть-чуть беспокойней, а это о чём-то да говорит."

    window hide
    scene chapter_1 scene_3_fridge_hanging
    show chapter_1_fridge_drawing zorder 1 at move_between((793, 1080), (793, 217), t=sm_motion_time(0.7))
    $ pause(sm_motion_time(0.7))
    show chapter_1_fridge_magnet zorder 2 at placed((897, 172)), show_hide(0.18)
    $ pause(0.18)
    ## Статическая сборка даёт дальнейшим репликам и сейвам один законченный кадр.
    scene chapter_1 scene_3_fridge_new_drawing

    "Последней её потрясающей выдумкой был панический страх оставаться дома одной."

    scene chapter_1 scene_3_children_room_girl_neutral

    nas "Спасибо, что побыла на нашем чаепитии! Полли не пришёл сегодня..."
    nas "Как тебе профессор Косолап?"

    scene chapter_1 scene_3_toys

    menu(screen="textbox"):
        "\"Очаровашка!\"":
            $ c1s3_teaparty_choice = "charming"
            mar "Очень милый медведь! А какие манеры!"
            nas "А то! Выпускник Лесной академии!"

        "\"Зануда!\"":
            $ c1s3_teaparty_choice = "boring"
            mar "Его лекция о мёдоведении была совершенно ни к месту!"
            nas "Он очень гордится своей научной... Штукой!"

        "\"Странный!\"":
            $ c1s3_teaparty_choice = "strange"
            mar "Кажется, он помешан на еловых шишках..."
            nas "В лесу нет конфеток! Вот и приходится шишами чай закусывать..."

        "\"А где Полли?\"":
            $ c1s3_teaparty_choice = "where_is_polly"
            mar "Я стеснялась спросить! А где Полли?"
            nas "Он испугался и сбежал... Трусишка!"

    scene chapter_1 scene_3_children_room_girl_sad

    mar "Я пойду встречу папу с работы. Посиди, пока..."

    scene chapter_1 scene_3_children_room_girl_crying

    nas "НЕТ!"
    nas "НЕ УХОДИ!"
    mar "Почему?.."
    nas "НЕЛЬЗЯ!"

    scene chapter_1 scene_3_sofa_tv_1

    "Стоило нам с Витей обоим ненадолго отлучиться, как наша принцесса начинала вопить, греметь кастрюлями, орать под телевизор."

    scene chapter_1 scene_3_entrance

    "Мы пыталась с ней по-хорошему поговорить, объяснить, что взрослым девочкам так вести себя должно быть стыдно."
    "Потом просто ругалась."

    scene chapter_1 scene_3_daughter_top

    vit "Это ни в какие рамки. Ну что это за поведение, а?"

    scene chapter_1 scene_3_daughter_top_close

    "Вот она: охрипшая от крика, наша маленькая принцесса истерии, с красным заплаканным лицом."
    vit "Мама и так почти целыми днями дома торчит. Тебя нельзя оставить на час?"
    nas "Нельзя..."
    vit "Это несерьёзно... Сходи заткни соседей!"

    scene chapter_1 scene_3_entrance_neighbor

    sos "Ну наконец-то явились! И что за дела? Лучше бы вы стены сверлили круглосуточно!"

    scene chapter_1 scene_3_entrance_neighbors

    menu(screen="textbox"):
        "\"Простите...\"":
            $ c1s3_neighbor_choice = "apologize"
            mar "У неё просто тяжёлый возраст. Извините, пожалуйста."
            sos "Ну Мариш, это несерьёзно. Ребёнка надо воспитывать!"
            "Я знала. Просто не понимала, как. Мы пытались разобраться..."

        "\"Заткнитесь!\"":
            $ c1s3_neighbor_choice = "confront"
            mar "И вы тоже разораться решили?! Закройте рты и валите домой!"
            sos "О, психованная семейка! Ничего-ничего, потом вызовем милицию..."
            "Они не имели права нравоучать нас."
            "Пусть лучше приглядывают за своими детьми, болтающимися без дела по двору, как оборванцы."

    scene chapter_1 scene_3_sofa_marina

    "Конечно, мы ходили с дочкой к психологу."
    "Именно там, далеко не на первом сеансе, Настя шёпотом рассказала, что на самом деле не боится оставаться одна."

    scene chapter_1 scene_3_sofa_daughter

    nas "Он приходит, когда дома тихо, когда солнышка почти нет..."
    mar "Кто приходит, дорогая?"
    vit "Кто-кто?.. Это Полли? Или как там его..."
    nas "Полли сбежал... Он, как я, испугался..."
    vit "Твоего нового воображаемого друга? И как его зовут?"
    nas "Он не друг... И у него нет имени. Просто..."
    nas "Шаркающий человек."

    ## Глава 2 ещё не подключена: вместо jump chapter_2_scene_1 — заглушка.
    jump end_dev_yet

## Конец готовой части: титр-заглушка и выход в главное меню.

label end_dev_yet:
    $ quick_menu = False
    $ sm_parallax_off = True

    scene black with Dissolve(1.0)

    show expression prologue_title(_("пока всё"), 50) as prologue_titles_text_2:
        align (0.5, 0.5)
        subpixel True
    with Dissolve(2.0)

    pause

    ## jump main_menu остался бы в игре: флаг main_menu не взводится, параллакс не гаснет.
    $ MainMenu(confirm=False)()
