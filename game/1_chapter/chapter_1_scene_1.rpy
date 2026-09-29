## Глава 1: лампа → метроном → пианино → стук → холл → дверь → замки.
## Переходы в цепочке стука склеены с ударами.

## Изображения

## Позы «тянет шнур» и «к метроному» на общем холсте 937×1012: при сдвиге (-272, 21)
## силуэты рук совпадают, и Dissolve между ними ничего не обрезает.
## Холст «тянет шнур» лежит в нём со сдвигом (272, 0).
image chapter_1_lamp_hand pull_wide = Fixed(
    Transform("chapter_1_lamp_hand light_pull", pos=(272, 0)), xysize=(937, 1012))
image chapter_1_lamp_hand metronome_wide = Fixed(
    Transform("chapter_1_lamp_hand light_metronome", pos=(0, 21)), xysize=(937, 1012))

## Телевизоры с помехами на экране.
image chapter_1 scene_1_tv_close = sm_tv_scene("images/1_chapter/chapter_1 scene_1_tv_close.png",
    C1S1_TV_NOISE_POS, C1S1_TV_NOISE_SIZE, C1S1_TV_NOISE_CORNERS)
image chapter_1 scene_1_sofa_tv_night = sm_tv_scene("images/1_chapter/chapter_1 scene_1_sofa_tv_night.png",
    C1S1_TV_WIDE_POS, C1S1_TV_WIDE_SIZE, ((2, 2), (402, 2), (402, 282), (2, 282)))
image chapter_1 scene_1_tv_close_night = sm_tv_scene("images/1_chapter/chapter_1 scene_1_tv_close_night.png",
    C1S1_TV_NOISE_POS, C1S1_TV_NOISE_SIZE, C1S1_TV_NOISE_CORNERS)

image chapter_1 scene_1_living_room_mess = "images/1_chapter/cleanup/chapter_1_cleanup_mess.png"

## Константы сцены

## Внутренний проём рамки, а не меньшая белая заглушка PSD Layer 20.
define C1S1_TV_NOISE_POS = (812, 109)
define C1S1_TV_NOISE_SIZE = (603, 443)
define C1S1_TV_NOISE_CORNERS = ((2, 2), (601, 19), (600, 438), (5, 441))
define C1S1_TV_WIDE_POS = (1228, 118)
define C1S1_TV_WIDE_SIZE = (404, 284)

## Полкачания стрелки между щелчками ≈ 80 BPM.
define C1S1_ARROW_HALF_T = 0.75

define C1S1_LAMP_FOCUS = (0.44, 0.44)

## Вторая серия ударов у пианино сильнее первой.
define c1s1_knock_punch = Move((0, 12), (0, -12), 0.09, bounce=True, repeat=True, delay=0.26)
define c1s1_knock_punch_hard = Move((0, 20), (0, -20), 0.08, bounce=True, repeat=True, delay=0.24)

## В холле три удара слабее, чем у пианино.
define c1s1_hall_knock_punch = Move((0, 6), (0, -6), 0.09, bounce=True, repeat=True, delay=0.22)

define c1s1_door_hit_punch = Move((0, 14), (0, -14), 0.08, bounce=True, repeat=True, delay=0.24)

## Сумка заякорена в нижнем левом углу обрезанного холста.
define C1S1_DOOR_BAG_POS = (0, 1080)
define C1S1_DOOR_BAG_ANCHOR = (0.0, 1.0)
define C1S1_Z_DOOR_BAG = 5

define C1S1_LOCKS_FOCUS = (0.50, 0.32)

define c1s1_locks_knock_punch = Move((0, 16), (0, -16), 0.08, bounce=True, repeat=True, delay=0.26)
define c1s1_locks_knock_punch_hard = Move((0, 22), (0, -22), 0.08, bounce=True, repeat=True, delay=0.24)

## Звук сцены. Файлы лежат в game/audio/sfx/c1s1/, кортеж = варианты удара.
define C1S1_METRONOME_TICK_VOL = 0.55
## WAV содержит полпериода тишины перед щелчком; длительность равна C1S1_ARROW_HALF_T.
define C1S1_METRONOME_LOOP_SOUND = "c1s1/metronome_loop"

default c1s1_metronome_audio = None

init python:
    def c1s1_metronome_tension():
        return sm_audio_set_filter(c1s1_metronome_audio, [
            renpy.audio.filter.Lowpass(2200.0),
            renpy.audio.filter.Reverb(resonance=0.72,
                dampening=2400.0, wet=0.55,
                dry=0.85, delay_multiplier=1.8),
        ], duration=7.0)

## Сцена

label chapter_1_scene_1:

    ## Кинематограф: клик не проматывает паузы и переходы; выборы и мини-игра — без блока.
    $ click_skip_block = True

    ## Лампа.
    camera at camera_push(C1S1_LAMP_FOCUS, 1.04, 1.14, 25.0)
    scene chapter_1 lamp_dark:
        breath_brightness(-0.05, -0.08, 6.0)
    show chapter_1_lampshade dark zorder 10:
        placed((183, 0))
        breath_brightness(-0.05, -0.08, 6.0)
    with Dissolve(2.0)

    pause 1.0

    ## Интерактивы не создают развилок и пропускаются вместе со сценой.
    $ click_skip_block = False
    if not renpy.is_skipping():
        menu(screen="scene_choice", follow=follow_camera(), skippable=True):
            "ВКЛЮЧИТЬ" (pos=(475, 530), size=(330, 165)):
                pass
    $ click_skip_block = True

    show chapter_1_lamp_hand dark_reach zorder 5:
        subpixel True
        anchor (0, 0)
        pos (-360, 700) alpha 0.0
        ease 1.1 pos (0, 108) alpha 1.0
    pause 1.1

    ## Холст «тянет» совмещён с «тянется» сдвигом (6, -16): растворение без двоения.
    ## Пальцы под абажуром нащупывают шнурок, короткая заминка — и рывок вниз.
    show chapter_1_lamp_hand dark_pull zorder 5:
        pos (6, 92)
        easeout 0.5 pos (0, 58)
        pause 0.15
        easein 0.12 yoffset 22
    with Dissolve(0.3)
    pause (0.5 + 0.15 + 0.12 - 0.3)

    ## Щелчок и мгновенная смена освещения без сброса камеры.
    $ sm_sfx("c1s1/lamp_switch", volume=0.9)
    ## Нижняя часть корпуса закрывает пивот стрелки, руки остаются перед метрономом.
    scene chapter_1 lamp_light:
        breath_brightness(-0.04, -0.08, 6.0)
    ## Якорь стрелки совпадает с нижним креплением маятника (спрайт 45×368, bbox (985, 292)).
    show chapter_1_metronome_arrow zorder 3:
        subpixel True
        transform_anchor True
        anchor (0.5, 1.0)
        pos (1007, 660)
        rotate 0.0
    ## Точный фрагмент светлого фона ниже прорези: (835, 640, 1171, 777).
    show chapter_1_metro_patch zorder 4:
        breath_brightness(-0.04, -0.08, 6.0)
    show chapter_1_lampshade light zorder 10:
        anchor (0, 0)
        pos (183, 0)
        
    ## Рука отпускает шнур: из рывка вниз подскакивает и оседает.
    show chapter_1_lamp_hand light_pull zorder 5:
        subpixel True
        anchor (0, 0)
        pos (0, 58)
        yoffset 22
        easein 0.45 yoffset -10
        # ease 0.35 yoffset 0
        easein 2.0 xoffset 240 yoffset 350

    ## Поза перерастворяется в «метроном» внутри ATL: позиция и качание не прерываются.
    ## Переход на общий холст — в том же кадре: pos компенсирует его сдвиг (272, 0).
    show chapter_1_lamp_hand metronome_wide:
        "chapter_1_lamp_hand pull_wide"
        pos (-272, 58)
        "chapter_1_lamp_hand metronome_wide" with Dissolve(0.4)
        block:
            ease 1.25 xoffset 230 yoffset 360
            ease 1.25 xoffset 240 yoffset 350
            repeat

    ## Метроном доступен только после включения света.
    if not renpy.is_skipping():
        menu(screen="scene_choice", follow=follow_camera(), skippable=True):
            "ЗАУПУСТИТЬ" (pos=(1017, 547), size=(430, 190)):
                pass

    ## Та же рука из качания дотягивается кончиками пальцев до палки маятника.
    show chapter_1_lamp_hand metronome_wide:
        ease 0.6 xoffset 372 yoffset 251
    pause 0.6

    ## Толчок руки и стрелка стартуют в один кадр.
    $ c1s1_metronome_audio = sfxplay(C1S1_METRONOME_LOOP_SOUND, ext="wav", fadein=0, fadeout=0, tag="c1s1_metronome", volume=C1S1_METRONOME_TICK_VOL)
    show chapter_1_lamp_hand metronome_wide:
        easein 0.15 xoffset 386
        ease 0.3 xoffset 372
    ## Положительный rotate продолжает толчок руки вправо; loop звука и стрелка — в одном такте.
    show chapter_1_metronome_arrow zorder 3:
        easein (C1S1_ARROW_HALF_T / 2.0) rotate (20.0 * sm_motion_scale())
        block:
            ease C1S1_ARROW_HALF_T rotate (-20.0 * sm_motion_scale())
            ease C1S1_ARROW_HALF_T rotate (20.0 * sm_motion_scale())
            repeat
    pause 0.5

    show chapter_1_lamp_hand metronome_wide:
        ease 1.1 pos (-320, 739) xoffset 0 yoffset 0 alpha 0.0
    pause 1.1
    hide chapter_1_lamp_hand

    ## Пауза учитывает уже прошедшее время ухода руки.
    pause (C1S1_ARROW_HALF_T / 2.0 + (4 - 1) * C1S1_ARROW_HALF_T - 0.5 - 1.1)

    # ## Пианино: отъезд от ГГ к рукам.
    # scene chapter_1 piano:
    #     truecenter
    #     subpixel True
    #     zoom 1.0
    #     parallel:
    #         linear 40.0 zoom 1.07
    #     parallel:
    #         breath_brightness(-0.03, -0.09, 6.0)
    # with Dissolve(2.2)

    # pause 4.0

    ## Камера рук подхватывает отъезд до его завершения: скорости зума
    ## согласованы, ≈0.038/с у ГГ и ≈0.037/с у рук.
    camera at camera_settle((0.51, 0.61), 1.03, 1.0, 13.4)
    scene chapter_1 piano_hands:
        truecenter
        subpixel True
        breath_brightness(-0.03, -0.08, 6.0)
    ## Руки — ближний план: parallax_near отделяет их от фона. Дыхание — ypos в absolute:
    ## float без обёртки Ren'Py трактует как долю экрана.
    show chapter_1_piano_hand_left:
        subpixel True
        anchor (0, 0)
        pos (330, 284)
        xoffset 0.0 yoffset 0.0
        parallel:
            function parallax_near_f
        parallel:
            ease 2.9 ypos absolute(284 - 4 * sm_motion_scale())
            ease 3.6 ypos 284
            repeat
    show chapter_1_piano_hand_right:
        subpixel True
        anchor (0, 0)
        pos (1113, 276)
        xoffset 0.0 yoffset 0.0
        parallel:
            function parallax_near_f
        parallel:
            ease 3.3 ypos absolute(276 - 3 * sm_motion_scale())
            ease 2.7 ypos 276
            repeat
    with Dissolve(1.2)

    pause 

    show chapter_1_piano:
        truecenter
        subpixel True
        breath_brightness(-0.03, -0.08, 6.0)
    ## Маятник метронома на пианино: пивот — низ палочки в основании, такт — как у звука.
    show metro_arrow_single:
        subpixel True
        transform_anchor True
        anchor (0.5, 1.0)
        pos (846, 392)
        rotate (-14.0 * sm_motion_scale())
        block:
            ease C1S1_ARROW_HALF_T rotate (14.0 * sm_motion_scale())
            ease C1S1_ARROW_HALF_T rotate (-14.0 * sm_motion_scale())
            repeat
    with Dissolve(1.2)

    pause
    pause 1.5

    ## Первый удар запускает завал камеры на обе серии стука.
    ## Запас зума для поворота до 6.7°: минимум ≈1.20.
    $ c1s1_metronome_tension()
    camera at uneasy_sway(10.0, 1.2, speed=1.4, zoom_pad=1.22, base=-5.5, base_in_t=7.0, zoom0=1.02)

    ## Первая серия: три удара; show перед punch синхронизирует скачок дрожи.
    $ sm_sfx(("c1s1/knock_far_1", "c1s1/knock_far_2", "c1s1/knock_far_3"), volume=0.58)

    show chapter_1_piano_hand_left at placed_jitter((330, 284), jitter_amp=0.8, jitter_key="c1s1_hand_l")
    show chapter_1_piano_hand_right at placed_jitter((1113, 276), jitter_amp=0.8, jitter_key="c1s1_hand_r")
    with sm_motion_transition(c1s1_knock_punch)
    pause 0.3
    $ sm_sfx(("c1s1/knock_far_1", "c1s1/knock_far_2", "c1s1/knock_far_3"), volume=0.66)

    show chapter_1_piano_hand_left at placed_jitter((330, 284), jitter_amp=1.4, jitter_key="c1s1_hand_l")
    show chapter_1_piano_hand_right at placed_jitter((1113, 276), jitter_amp=1.4, jitter_key="c1s1_hand_r")
    with sm_motion_transition(c1s1_knock_punch)
    pause 0.3
    $ sm_sfx(("c1s1/knock_far_1", "c1s1/knock_far_2", "c1s1/knock_far_3"), volume=0.74)

    show chapter_1_piano_hand_left at placed_jitter((330, 284), jitter_amp=2.0, jitter_key="c1s1_hand_l")
    show chapter_1_piano_hand_right at placed_jitter((1113, 276), jitter_amp=2.0, jitter_key="c1s1_hand_r")
    with sm_motion_transition(c1s1_knock_punch)

    ## Пауза между сериями.
    pause 1.7

    ## Вторая серия: три усиленных удара.
    $ sm_sfx(("c1s1/knock_far_1", "c1s1/knock_far_2", "c1s1/knock_far_3"), volume=0.86)
    $ flash_fx(high=0.34, fall=0.16)
    show chapter_1_piano_hand_left at placed_jitter((330, 284), jitter_amp=2.8, jitter_key="c1s1_hand_l")
    show chapter_1_piano_hand_right at placed_jitter((1113, 276), jitter_amp=2.8, jitter_key="c1s1_hand_r")
    with sm_motion_transition(c1s1_knock_punch_hard)
    pause 0.18
    $ sm_sfx(("c1s1/knock_far_1", "c1s1/knock_far_2", "c1s1/knock_far_3"), volume=0.93)
    $ flash_fx(high=0.40, fall=0.16)
    show chapter_1_piano_hand_left at placed_jitter((330, 284), jitter_amp=3.6, jitter_key="c1s1_hand_l")
    show chapter_1_piano_hand_right at placed_jitter((1113, 276), jitter_amp=3.6, jitter_key="c1s1_hand_r")
    with sm_motion_transition(c1s1_knock_punch_hard)
    pause 0.18
    $ sm_sfx(("c1s1/knock_far_1", "c1s1/knock_far_2", "c1s1/knock_far_3"), volume=1.0)
    $ flash_fx(high=0.48, fall=0.16)
    show chapter_1_piano_hand_left at placed_jitter((330, 284), jitter_amp=4.5, jitter_key="c1s1_hand_l")
    show chapter_1_piano_hand_right at placed_jitter((1113, 276), jitter_amp=4.5, jitter_key="c1s1_hand_r")
    with sm_motion_transition(c1s1_knock_punch_hard)

    pause 2.0

    ## Холл: камера возвращается к покою.
    camera at camera_rest(1.02)
    scene chapter_1 hall
    ## Внутри групп zorder растёт по порядку предметов; швабра поверх всех.
    show chapter_1_hall_door zorder 3 at placed((634, 128))
    show chapter_1_hall_boots zorder 10 at placed((1077, 564))
    show chapter_1_hall_packet zorder 10 + 1 at placed((1075, 594))
    show chapter_1_hall_toy zorder 10 + 2 at placed((1102, 618))
    show chapter_1_hall_paper zorder 20 at placed((343, 521))
    show chapter_1_hall_bag zorder 20 + 1 at placed((431, 413))
    show chapter_1_hall_bottles zorder 20 + 2 at placed((334, 463))
    show chapter_1_hall_umbrella_1 zorder 30 at placed((267, 562))
    show chapter_1_hall_umbrella_2 zorder 30 + 1 at placed((374, 655))
    show chapter_1_hall_mirror zorder 35 at placed((328, 86))
    show chapter_1_hall_mop zorder 40 at placed((924, 302))

    pause 0.5

    ## Стук продолжается в холле; предметы у стен дрожат.
    pause 1.0
    show chapter_1_hall_mop zorder 40 at placed_jitter((924, 302), jitter_amp=2.0, jitter_key="hall_mop")
    show chapter_1_hall_umbrella_1 zorder 30 at placed_jitter((267, 562), jitter_amp=2.0, jitter_key="hall_umb1")
    show chapter_1_hall_umbrella_2 zorder 30 + 1 at placed_jitter((374, 655), jitter_amp=2.0, jitter_key="hall_umb2")
    show chapter_1_hall_bottles zorder 20 + 2 at placed_jitter((334, 463), jitter_amp=2.0, jitter_key="hall_bottles")

    $ sm_sfx(("c1s1/knock_hall_1", "c1s1/knock_hall_2", "c1s1/knock_hall_3"), volume=0.85)
    $ flash_fx(high=0.16, fall=0.3)
    with sm_motion_transition(c1s1_hall_knock_punch)
    pause 0.45
    $ sm_sfx(("c1s1/knock_hall_1", "c1s1/knock_hall_2", "c1s1/knock_hall_3"), volume=0.85)
    $ flash_fx(high=0.16, fall=0.3)
    with sm_motion_transition(c1s1_hall_knock_punch)
    pause 0.45

    ## Третий удар склеен с дверью крупным планом.
    $ sm_sfx(("c1s1/knock_hall_1", "c1s1/knock_hall_2", "c1s1/knock_hall_3"), volume=0.85)
    $ flash_fx(high=0.16, fall=0.3)
    with sm_motion_transition(c1s1_hall_knock_punch)
    pause 0.08

    ## Вспышка на always_shown-экране досвечивает новый кадр после scene.
    scene chapter_1 door
    $ sm_sfx(("c1s1/knock_door_1", "c1s1/knock_door_2", "c1s1/knock_door_3"), volume=1.0)
    show chapter_1_door_hand hit at placed((1158, 147))
    with sm_motion_transition(c1s1_door_hit_punch)

    ## Ещё два удара с замахом.
    pause 0.6
    show chapter_1_door_hand wind at placed((769, 131))
    pause 0.28
    $ sm_sfx(("c1s1/knock_door_1", "c1s1/knock_door_2", "c1s1/knock_door_3"), volume=1.0)
    show chapter_1_door_hand hit at placed((1158, 147))
    with sm_motion_transition(c1s1_door_hit_punch)

    ## Последний удар склеен с видом двери из квартиры.
    pause 0.5
    show chapter_1_door_hand wind at placed((769, 131))
    pause 0.28
    $ flash_fx(high=0.22, fall=0.22)
    $ sm_sfx(("c1s1/knock_door_1", "c1s1/knock_door_2", "c1s1/knock_door_3"), volume=1.0)
    show chapter_1_door_hand hit at placed((1158, 147))
    with sm_motion_transition(c1s1_door_hit_punch)
    pause 0.08

    ## Дверь изнутри: спокойный наезд на замки, сумка дрожит от ударов.
    ## Третий удар двери крупным планом уже озвучен: рез склеен с ним.
    camera at camera_push(C1S1_LOCKS_FOCUS, 1.02, 1.16, 8.8)
    scene chapter_1 hall_door
    show chapter_1_hall_door_bag zorder C1S1_Z_DOOR_BAG at placed_jitter(C1S1_DOOR_BAG_POS, anchor_xy=C1S1_DOOR_BAG_ANCHOR, jitter_amp=2.0, jitter_key="c1s1_door_bag")
    with sm_motion_transition(c1s1_locks_knock_punch)

    ## Ещё два удара; show перед punch синхронизирует дрожь сумки.
    pause 0.5
    $ sm_sfx(("c1s1/knock_inside_1", "c1s1/knock_inside_2", "c1s1/knock_inside_3"), volume=0.88)
    $ flash_fx(high=0.26, fall=0.22)
    show chapter_1_hall_door_bag zorder C1S1_Z_DOOR_BAG at placed_jitter(C1S1_DOOR_BAG_POS, anchor_xy=C1S1_DOOR_BAG_ANCHOR, jitter_amp=2.6, jitter_key="c1s1_door_bag")
    with sm_motion_transition(c1s1_locks_knock_punch)
    pause 0.5
    $ sm_sfx(("c1s1/knock_inside_1", "c1s1/knock_inside_2", "c1s1/knock_inside_3"), volume=0.94)
    $ flash_fx(high=0.30, fall=0.22)
    show chapter_1_hall_door_bag zorder C1S1_Z_DOOR_BAG at placed_jitter(C1S1_DOOR_BAG_POS, anchor_xy=C1S1_DOOR_BAG_ANCHOR, jitter_amp=3.2, jitter_key="c1s1_door_bag")
    with sm_motion_transition(c1s1_locks_knock_punch)

    ## Ложная тишина; общий jitter_key сохраняет фазу затухания.
    pause 1.6
    show chapter_1_hall_door_bag zorder C1S1_Z_DOOR_BAG at placed_jitter(C1S1_DOOR_BAG_POS, anchor_xy=C1S1_DOOR_BAG_ANCHOR, jitter_amp=0.8, jitter_key="c1s1_door_bag")
    pause 1.4

    ## Стук возвращается двумя усиленными ударами.
    $ sm_sfx(("c1s1/knock_inside_1", "c1s1/knock_inside_2", "c1s1/knock_inside_3"), volume=1.0)
    $ flash_fx(high=0.38, fall=0.16)
    show chapter_1_hall_door_bag zorder C1S1_Z_DOOR_BAG at placed_jitter(C1S1_DOOR_BAG_POS, anchor_xy=C1S1_DOOR_BAG_ANCHOR, jitter_amp=4.0, jitter_key="c1s1_door_bag")
    with sm_motion_transition(c1s1_locks_knock_punch_hard)
    pause 0.34
    $ sm_sfx(("c1s1/knock_inside_1", "c1s1/knock_inside_2", "c1s1/knock_inside_3"), volume=1.0)
    $ flash_fx(high=0.44, fall=0.16)
    show chapter_1_hall_door_bag zorder C1S1_Z_DOOR_BAG at placed_jitter(C1S1_DOOR_BAG_POS, anchor_xy=C1S1_DOOR_BAG_ANCHOR, jitter_amp=4.8, jitter_key="c1s1_door_bag")
    with sm_motion_transition(c1s1_locks_knock_punch_hard)

    ## Финальное затухание.
    pause 1.6
    show chapter_1_hall_door_bag zorder C1S1_Z_DOOR_BAG at placed_jitter(C1S1_DOOR_BAG_POS, anchor_xy=C1S1_DOOR_BAG_ANCHOR, jitter_amp=0.8, jitter_key="c1s1_door_bag")
    pause 1.6
    show chapter_1_hall_door_bag zorder C1S1_Z_DOOR_BAG at placed_jitter(C1S1_DOOR_BAG_POS, anchor_xy=C1S1_DOOR_BAG_ANCHOR, jitter_amp=0.0, jitter_key="c1s1_door_bag")

    ## Переход к мини-игре с замками.
    $ click_skip_block = False
    call chapter_1_scene_1_minigame_locks from _call_c1s1_minigame_locks

label .after_locks:

    $ sfxstop(handle=c1s1_metronome_audio, fadeout=1.2)
    $ c1s1_metronome_audio = None
    camera

    if c1s1_locks_outcome == "timeout":
        $ c1s1_locks_outcome = "normal"

    if c1s1_locks_outcome == "fast":
        scene chapter_1 scene_1_vitya_outcome_fast

        vit "Привет."

        scene chapter_1 scene_1_hall_vitya

        "Часто Витя бывал просто невыносим."

        scene chapter_1 scene_1_hall_mess

        "Ничего серьёзного: какие-то банальности, быт... И эти его дурацкие, неискоренимые привычки."

    else:
        scene chapter_1 scene_1_vitya_outcome_normal

        vit "Ну наконец-то, бля."

        scene chapter_1 scene_1_hall_vitya

        "Часто Витя бывал просто невыносим."

        scene chapter_1 scene_1_hall_mess

        "Ничего серьёзного: какие-то банальности, быт... И эти его дурацкие, неискоренимые привычки."

    "Раньше мне хватало сил их не замечать. Терпеть."

label .tv:
    camera
    scene chapter_1 scene_1_tv_close

label .tv_dialogue:
    vit "Наконец-то..."

label .cleanup:
    camera
    scene chapter_1 scene_1_living_room_mess

    "Разбросанные носки, не опускающийся стульчак, как типично!"

    call chapter_1_scene_1_minigame_cleanup from _call_c1s1_household_cleanup

    scene chapter_1 scene_1_kitchen_sink

    mar "Ты в магазин зашёл?"
    "Нарушенные обещания..."

    scene chapter_1 scene_1_sofa_tv_night

    vit "Не-а."
    "Ну, мелочь. И ещё одна. И ещё одна. День за днём."
    mar "У нас на завтра..."
    "Раз за разом просишь, напоминаешь, умоляешь…"

    scene chapter_1 scene_1_tv_close_night

    vit "Не, завтра не могу никак."
    mar "Но мы договаривались!"

    scene chapter_1 scene_1_vitya_sofa

    vit "Не ори!"
    mar "Сам не ори!"
    "Скандалишь, наконец. Но тебя не слышат. Как это выводило меня из себя."
    vit "Ты опять начинаешь?!"
    "И так по кругу. Снова и снова."

    jump chapter_1_scene_2
