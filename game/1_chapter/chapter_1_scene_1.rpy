## Глава 1: лампа → метроном → пианино → стук → холл → дверь → замки.
## Переходы в цепочке стука склеены с ударами.

## Изображения

image chapter_1 lamp_dark = "images/1_chapter/chapter_1 lamp_dark.jpg"
image chapter_1 lamp_light = "images/1_chapter/chapter_1 lamp_light.jpg"
image chapter_1 piano = "images/1_chapter/chapter_1 piano.jpg"
image chapter_1 piano_hands = "images/1_chapter/chapter_1 piano_hands.jpg"

## Слои композиции у лампы.
image chapter_1_lampshade dark = "images/1_chapter/chapter_1_lampshade dark.png"
image chapter_1_lampshade light = "images/1_chapter/chapter_1_lampshade light.png"

image chapter_1_lamp_hand dark_reach = "images/1_chapter/chapter_1_lamp_hand dark_reach.png"
image chapter_1_lamp_hand dark_pull = "images/1_chapter/chapter_1_lamp_hand dark_pull.png"
image chapter_1_lamp_hand light_pull = "images/1_chapter/chapter_1_lamp_hand light_pull.png"
image chapter_1_lamp_hand light_metronome = "images/1_chapter/chapter_1_lamp_hand light_metronome.png"

image chapter_1_metronome_arrow = "images/1_chapter/chapter_1_metronome_arrow.png"
image chapter_1_metronome_foreground = "images/1_chapter/owner_review/chapter_1_metronome_foreground.png"

image chapter_1_piano_gg = "images/1_chapter/chapter_1_piano_gg.png"
image chapter_1_piano_hand_left = "images/1_chapter/chapter_1_piano_hand_left.png"
image chapter_1_piano_hand_right = "images/1_chapter/chapter_1_piano_hand_right.png"

## Холл: фон и отдельные предметы.
image chapter_1 hall = "images/1_chapter/chapter_1 hall.jpg"
image chapter_1_hall_door = "images/1_chapter/chapter_1_hall_door.png"
image chapter_1_hall_mirror = "images/1_chapter/chapter_1_hall_mirror.png"
image chapter_1_hall_paper = "images/1_chapter/chapter_1_hall_paper.png"
image chapter_1_hall_bag = "images/1_chapter/chapter_1_hall_bag.png"
image chapter_1_hall_bottles = "images/1_chapter/chapter_1_hall_bottles.png"
image chapter_1_hall_umbrella_1 = "images/1_chapter/chapter_1_hall_umbrella_1.png"
image chapter_1_hall_umbrella_2 = "images/1_chapter/chapter_1_hall_umbrella_2.png"
image chapter_1_hall_boots = "images/1_chapter/chapter_1_hall_boots.png"
image chapter_1_hall_packet = "images/1_chapter/chapter_1_hall_packet.png"
image chapter_1_hall_toy = "images/1_chapter/chapter_1_hall_toy.png"
image chapter_1_hall_mop = "images/1_chapter/chapter_1_hall_mop.png"

## Дверь крупным планом: замах и удар.
image chapter_1 door = "images/1_chapter/chapter_1 door.jpg"
image chapter_1_door_hand wind = "images/1_chapter/chapter_1_door_hand wind.png"
image chapter_1_door_hand hit = "images/1_chapter/chapter_1_door_hand hit.png"

## `chapter_1 hall_door` — кадр изнутри; `chapter_1_hall_door` — створка в холле.
image chapter_1 hall_door = "images/1_chapter/chapter_1 hall_door.jpg"
image chapter_1_hall_door_bag = "images/1_chapter/chapter_1_hall_door_bag.png"

## Статические кадры продолжения сцены.
image chapter_1 scene_1_hall_vitya = "images/1_chapter/chapter_1 scene_1_hall_vitya.jpg"
image chapter_1 scene_1_hall_mess = "images/1_chapter/chapter_1 scene_1_hall_mess.jpg"
image chapter_1 scene_1_vitya_door = "images/1_chapter/chapter_1 scene_1_vitya_door.jpg"
image chapter_1 scene_1_vitya_outcome_fast = "images/1_chapter/chapter_1 scene_1_vitya_outcome_fast.jpg"
image chapter_1 scene_1_vitya_outcome_normal = "images/1_chapter/chapter_1 scene_1_vitya_outcome_normal.jpg"
image chapter_1 scene_1_sofa_tv = "images/1_chapter/chapter_1 scene_1_sofa_tv.jpg"
image chapter_1 scene_1_tv_close = sm_tv_scene("images/1_chapter/chapter_1 scene_1_tv_close.jpg",
    C1S1_TV_NOISE_POS, C1S1_TV_NOISE_SIZE, C1S1_TV_NOISE_CORNERS)
image chapter_1 scene_1_sofa_tv_night = sm_tv_scene("images/1_chapter/chapter_1 scene_1_sofa_tv_night.jpg",
    C1S1_TV_WIDE_POS, C1S1_TV_WIDE_SIZE, C1S1_TV_WIDE_CORNERS)
image chapter_1 scene_1_tv_close_night = sm_tv_scene("images/1_chapter/chapter_1 scene_1_tv_close_night.jpg",
    C1S1_TV_NOISE_POS, C1S1_TV_NOISE_SIZE, C1S1_TV_NOISE_CORNERS)
image chapter_1 scene_1_kitchen_sink = "images/1_chapter/chapter_1 scene_1_kitchen_sink.jpg"
image chapter_1 scene_1_living_room_mess = "images/1_chapter/cleanup/chapter_1_cleanup_mess.png"
image chapter_1 scene_1_vitya_sofa = "images/1_chapter/chapter_1 scene_1_vitya_sofa.jpg"

## Константы сцены

## Внутренний проём рамки, а не меньшая белая заглушка PSD Layer 20.
define C1S1_TV_NOISE_POS = (812, 109)
define C1S1_TV_NOISE_SIZE = (603, 443)
define C1S1_TV_NOISE_CORNERS = ((2, 2), (601, 19), (600, 438), (5, 441))
define C1S1_TV_WIDE_POS = (1228, 118)
define C1S1_TV_WIDE_SIZE = (404, 284)
define C1S1_TV_WIDE_CORNERS = ((2, 2), (402, 2), (402, 282), (2, 282))

## Нижняя часть корпуса закрывает пивот стрелки, руки остаются перед метрономом.
define C1S1_Z_ARROW = 3
define C1S1_Z_METRONOME_FOREGROUND = 4
define C1S1_Z_HAND_BEHIND = 5
define C1S1_Z_SHADE = 10
define C1S1_Z_HAND_FRONT = 15

## Левые верхние углы спрайтов, px.
define C1S1_LAMPSHADE_POS = (183, 0)
define C1S1_HAND_REACH_POS = (0, 178)
define C1S1_HAND_PULL_POS = (0, 68)
define C1S1_HAND_METRONOME_POS = (100, 330)
define C1S1_HAND_ENTER_POS = (-560, 700)
define C1S1_HAND_LEAVE_POS = (150, 120)
define C1S1_HAND_METRONOME_FROM = (-75, 450)
define C1S1_HAND_EXIT_POS = (-320, 760)

## Тайминги руки.
define C1S1_HAND_ENTER_T = 1.8   # синхронно с pause после show
define C1S1_PULL_DY = 18         # px
define C1S1_PULL_T = 0.16
define C1S1_RELEASE_OVER = 10    # px
define C1S1_RELEASE_T = 0.45
define C1S1_SETTLE_T = 0.35
define C1S1_HAND_SWAP_T = 0.8
define C1S1_HAND_EXIT_DELAY = 0.5
define C1S1_HAND_EXIT_T = 1.1

## Мировые координаты кнопок: сначала лампа, затем метроном.
define C1S1_LAMP_BTN_POS = (475, 530)
define C1S1_LAMP_BTN_SIZE = (330, 165)
define C1S1_METRONOME_BTN_POS = (1005, 530)
define C1S1_METRONOME_BTN_SIZE = (430, 190)

## Метроном: пивот стрелки — низ маятника (спрайт 45×368, bbox (985, 292)).
define C1S1_ARROW_PIVOT_POS = (1007, 660)
## Точный фрагмент светлого фона ниже прорези: (835, 640, 1171, 777).
define C1S1_METRONOME_FOREGROUND_POS = (835, 640)
define C1S1_ARROW_AMP = 20.0     # градусы
define C1S1_ARROW_HALF_T = 0.75  # полкачания между щелчками ≈ 80 BPM
define C1S1_TICKS_BEFORE_PIANO = 4

## Камера у лампы.
define C1S1_SCENE_PARALLAX = 8.0
define C1S1_CAM_Z_REST = 1.02      # зум покоя — запас краёв под параллакс
define C1S1_LAMP_FOCUS = (0.44, 0.44)
define C1S1_LAMP_Z0 = 1.04
define C1S1_LAMP_Z1 = 1.14
define C1S1_LAMP_PUSH_T = 25.0     # наезд длиннее сцены — не останавливается

## Переход к рукам подхватывает отъезд до его завершения. Скорости зума на
## склейке согласованы: ≈0.038/с у ГГ и ≈0.037/с у рук.
define C1S1_PIANO_FOCUS = (0.52, 0.55)     # центр фигуры ГГ в долях кадра
define C1S1_PIANO_SCREEN = (0.5, 0.55)     # куда пришпилен: центр экрана по X
define C1S1_PIANO_Z0 = 1.35
define C1S1_PIANO_Z_END = 1.06
define C1S1_PIANO_OUT_T = 10.5
define C1S1_PIANO_HOLD_T = 7.0
define C1S1_HANDS_FOCUS = (0.51, 0.61)
define C1S1_HANDS_Z0 = 1.10
define C1S1_HANDS_T = 3.4

## ГГ заякорен за низ фигуры — это пивот покачивания и масштаба.
define C1S1_GG_POS = (998, 1080)
define C1S1_GG_PARALLAX = 3.0
define C1S1_HANDS_LEFT_POS = (330, 284)
define C1S1_HANDS_RIGHT_POS = (1113, 276)

## Стук у пианино: две серии по три удара; вспышка, дрожь и завал усиливаются.
define C1S1_KNOCK_FLASH_PEAKS = (0.18, 0.22, 0.26, 0.34, 0.40, 0.48)
define C1S1_KNOCK_FLASH_FALL_T = 0.22
define C1S1_KNOCK_FLASH_FALL2_T = 0.16
define C1S1_KNOCK_HOLD_T = 1.5
define C1S1_KNOCK_GAP_T = 0.3
define C1S1_KNOCK_GAP2_T = 0.18
define C1S1_KNOCK_SERIES_GAP_T = 1.7
define C1S1_KNOCK_TILT = -5.5       # базовый завал горизонта, градусы
define C1S1_KNOCK_TILT_T = 7.0      # накрывает обе серии
define C1S1_KNOCK_SWAY = 1.2
## Запас зума для поворота до 6.7°: минимум ≈1.20.
define C1S1_KNOCK_PAD = 1.22
define C1S1_KNOCK_DRIFT = 10.0      # дрейф покачивания, px
define C1S1_KNOCK_SWAY_SPEED = 1.4
## По одному уровню дрожи на удар; общий jitter_key исключает скачки фазы.
define C1S1_HANDS_TREMBLE_STEPS = (0.8, 1.4, 2.0, 2.8, 3.6, 4.5)

## Вторая серия ударов сильнее первой.
define c1s1_knock_punch = Move((0, 12), (0, -12), 0.09, bounce=True, repeat=True, delay=0.26)
define c1s1_knock_punch_hard = Move((0, 20), (0, -20), 0.08, bounce=True, repeat=True, delay=0.24)

## Позиции слоёв холла, px.
define C1S1_HALL_DOOR_POS = (634, 128)
define C1S1_HALL_MIRROR_POS = (328, 86)
define C1S1_HALL_PAPER_POS = (343, 521)
define C1S1_HALL_BAG_POS = (431, 413)
define C1S1_HALL_BOTTLES_POS = (334, 463)
define C1S1_HALL_UMBRELLA_1_POS = (267, 562)
define C1S1_HALL_UMBRELLA_2_POS = (374, 655)
define C1S1_HALL_BOOTS_POS = (1077, 564)
define C1S1_HALL_PACKET_POS = (1075, 594)
define C1S1_HALL_TOY_POS = (1102, 618)
define C1S1_HALL_MOP_POS = (924, 302)

## Внутри групп zorder растёт по порядку предметов; швабра поверх всех.
define C1S1_Z_HALL_DOOR = 3
define C1S1_Z_HALL_GROUP_0 = 10   # тумба справа: сапоги < пакет < игрушка
define C1S1_Z_HALL_GROUP_1 = 20   # комод слева: бумаги < сумка < бутылки
define C1S1_Z_HALL_GROUP_2 = 30   # зонты у комода
define C1S1_Z_HALL_MIRROR = 35
define C1S1_Z_HALL_MOP = 40

## В холле три удара слабее, чем у пианино.
define C1S1_HALL_KNOCK_FLASH = 0.16      # доля белого
define C1S1_HALL_KNOCK_FLASH_FALL_T = 0.3
define C1S1_HALL_KNOCK_HOLD_T = 1.0
define C1S1_HALL_KNOCK_GAP_T = 0.45
define C1S1_HALL_OBJ_TREMBLE = 2.0   # px

define c1s1_hall_knock_punch = Move((0, 6), (0, -6), 0.09, bounce=True, repeat=True, delay=0.22)

## Третий удар в холле склеен с ударом по двери крупным планом.
define C1S1_DOOR_HAND_WIND_POS = (769, 131)
define C1S1_DOOR_HAND_HIT_POS = (1158, 147)
define C1S1_HALL_CUT_T = 0.08        # ринг-удар мигает и сразу рез — «резко»
define C1S1_DOOR_OPEN_HOLD_T = 0.6
define C1S1_DOOR_WIND_T = 0.28
define C1S1_DOOR_KNOCK_GAP_T = 0.5
define C1S1_DOOR_CUT_T = 0.08        # третий удар мигает и сразу рез — как в холле

define c1s1_door_hit_punch = Move((0, 14), (0, -14), 0.08, bounce=True, repeat=True, delay=0.24)

## Замки изнутри: три удара, пауза, затем два более сильных.
## Сумка заякорена в нижнем левом углу обрезанного холста.
define C1S1_DOOR_BAG_POS = (0, 1080)
define C1S1_DOOR_BAG_ANCHOR = (0.0, 1.0)
define C1S1_Z_DOOR_BAG = 5

## После реза камера возвращается к спокойному параллаксу и едет к замкам.
define C1S1_LOCKS_FOCUS = (0.50, 0.32)
define C1S1_LOCKS_Z1 = 1.16
define C1S1_LOCKS_PUSH_T = 8.8

## Индексы [0..2] — первая серия, [3..4] — усиленная вторая.
define C1S1_LOCKS_FLASH_PEAKS = (0.22, 0.26, 0.30, 0.38, 0.44)
define C1S1_LOCKS_FLASH_FALL_T = 0.22
define C1S1_LOCKS_FLASH_FALL2_T = 0.16
define C1S1_LOCKS_KNOCK_GAP_T = 0.5
define C1S1_LOCKS_KNOCK_GAP2_T = 0.34
define C1S1_LOCKS_SERIES_GAP_T = 1.4
define C1S1_LOCKS_BAG_TREMBLE = (2.0, 2.6, 3.2, 4.0, 4.8)  # px
define C1S1_LOCKS_BAG_CALM = 0.8
define C1S1_LOCKS_SETTLE_T = 1.6

define c1s1_locks_knock_punch = Move((0, 16), (0, -16), 0.08, bounce=True, repeat=True, delay=0.26)
define c1s1_locks_knock_punch_hard = Move((0, 22), (0, -22), 0.08, bounce=True, repeat=True, delay=0.24)

define chapter_1_fade_in = Dissolve(2.0)
define chapter_1_dissolve = Dissolve(1.2)

## Трансформы сцены

transform c1s1_hand_pull(pos_xy, dy=C1S1_PULL_DY, t=C1S1_PULL_T):
    subpixel True
    anchor (0.0, 0.0)
    pos pos_xy
    easein t yoffset dy

## Продолжает рывок из yoffset dy уже в светлой позе.
transform c1s1_hand_release(pos_xy, dy=C1S1_PULL_DY, over=C1S1_RELEASE_OVER, up_t=C1S1_RELEASE_T, settle_t=C1S1_SETTLE_T):
    subpixel True
    anchor (0.0, 0.0)
    pos pos_xy
    yoffset dy
    easein up_t yoffset -over
    ease settle_t yoffset 0

transform c1s1_hand_poke(pos_xy, dx=14, t=0.15):
    subpixel True
    anchor (0.0, 0.0)
    pos pos_xy
    easein t xoffset dx
    ease 0.3 xoffset 0

transform c1s1_hand_fade_out(from_xy, to_xy, t=C1S1_HAND_SWAP_T):
    subpixel True
    anchor (0.0, 0.0)
    pos from_xy
    alpha 1.0
    ease t pos to_xy alpha 0.0

transform c1s1_hand_exit(from_xy, to_xy, t=C1S1_HAND_EXIT_T):
    subpixel True
    anchor (0.0, 0.0)
    pos from_xy
    ease t pos to_xy alpha 0.0

## Якорь стрелки совпадает с нижним креплением маятника.
transform c1s1_arrow_rest(pos_xy=C1S1_ARROW_PIVOT_POS):
    subpixel True
    transform_anchor True
    anchor (0.5, 1.0)
    pos pos_xy
    rotate 0.0

## Положительный rotate продолжает толчок руки вправо.
## TODO(звук): щелчки метронома.
transform c1s1_arrow_swing(pos_xy=C1S1_ARROW_PIVOT_POS, amp=C1S1_ARROW_AMP, half_t=C1S1_ARROW_HALF_T):
    subpixel True
    transform_anchor True
    anchor (0.5, 1.0)
    pos pos_xy
    rotate 0.0
    easein half_t / 2.0 rotate (amp * sm_motion_scale())
    block:
        ease half_t rotate (-amp * sm_motion_scale())
        ease half_t rotate (amp * sm_motion_scale())
        repeat

## transform_anchor не даёт rotate_pad сместить пивот фигуры.
transform c1s1_gg_idle(pos_xy=C1S1_GG_POS, strength=C1S1_GG_PARALLAX):
    subpixel True
    transform_anchor True
    anchor (0.5, 1.0)
    pos pos_xy
    xoffset 0.0 yoffset 0.0
    rotate 0.0
    parallel:
        function renpy.curry(mouse_parallax_f)(strength, 0.08, 0.0, 0.04, None, "gg")
    parallel:
        ease 2.7 rotate (0.35 * sm_motion_scale()) yzoom (1.0 + 0.004 * sm_motion_scale())
        ease 3.4 rotate (-0.3 * sm_motion_scale()) yzoom 1.0
        repeat

## Координаты явно absolute: float без обёртки Ren'Py трактует как долю экрана.
transform c1s1_piano_hand_idle(pos_xy, key, strength=C1S1_GG_PARALLAX, dy=4, t_up=2.9, t_down=3.6):
    subpixel True
    anchor (0.0, 0.0)
    xpos absolute(pos_xy[0])
    ypos absolute(pos_xy[1])
    xoffset 0.0 yoffset 0.0
    parallel:
        function renpy.curry(mouse_parallax_f)(strength, 0.08, 0.0, 0.04, None, key)
    parallel:
        ease t_up ypos absolute(pos_xy[1] - dy * sm_motion_scale())
        ease t_down ypos absolute(pos_xy[1])
        repeat

## Экраны интерактива

## Кнопки используют мировые координаты и следуют за камерой.
screen c1s1_lamp_switch():
    modal True
    use sm_skippable_interaction
    fixed:
        id "lamp_world"
        at follow_camera()
        xysize (config.screen_width, config.screen_height)
        use glow_button(
            _("Зажечь свет"),
            Return("done"),
            bg="dark",
            pos=C1S1_LAMP_BTN_POS,
            size=C1S1_LAMP_BTN_SIZE)

screen c1s1_metronome_start():
    modal True
    use sm_skippable_interaction
    fixed:
        id "metronome_world"
        at follow_camera()
        xysize (config.screen_width, config.screen_height)
        use glow_button(
            _("Завести метроном"),
            Return("done"),
            bg="dark",
            pos=C1S1_METRONOME_BTN_POS,
            size=C1S1_METRONOME_BTN_SIZE)

## Сцена

label chapter_1_scene_1:

    $ dismiss_off()

    ## Лампа.
    camera at parallax_push(C1S1_LAMP_FOCUS, C1S1_LAMP_Z0, C1S1_LAMP_Z1, C1S1_LAMP_PUSH_T, strength=C1S1_SCENE_PARALLAX)
    scene chapter_1 lamp_dark
    show chapter_1_lampshade dark zorder C1S1_Z_SHADE at placed(C1S1_LAMPSHADE_POS)
    with chapter_1_fade_in

    $ pause(1.0)

    ## Интерактивы не создают развилок и пропускаются вместе со сценой.
    if not renpy.is_skipping():
        call screen c1s1_lamp_switch

    show chapter_1_lamp_hand dark_reach zorder C1S1_Z_HAND_FRONT at slide_in(C1S1_HAND_ENTER_POS, C1S1_HAND_REACH_POS, t=C1S1_HAND_ENTER_T)
    $ pause(C1S1_HAND_ENTER_T)
    $ pause(0.5)

    show chapter_1_lamp_hand dark_pull zorder C1S1_Z_HAND_BEHIND at placed(C1S1_HAND_PULL_POS)
    with Dissolve(0.45)
    $ pause(0.4)

    show chapter_1_lamp_hand dark_pull at c1s1_hand_pull(C1S1_HAND_PULL_POS)
    $ pause(C1S1_PULL_T)

    ## Щелчок и мгновенная смена освещения без сброса камеры.
    ## TODO(звук): splay щелчка выключателя.
    scene chapter_1 lamp_light
    show chapter_1_metronome_arrow zorder C1S1_Z_ARROW at c1s1_arrow_rest()
    show chapter_1_metronome_foreground zorder C1S1_Z_METRONOME_FOREGROUND at placed(C1S1_METRONOME_FOREGROUND_POS)
    show chapter_1_lampshade light zorder C1S1_Z_SHADE at placed(C1S1_LAMPSHADE_POS)
    show chapter_1_lamp_hand light_pull zorder C1S1_Z_HAND_BEHIND at c1s1_hand_release(C1S1_HAND_PULL_POS)
    $ pause(C1S1_RELEASE_T + C1S1_SETTLE_T)
    $ pause(0.5)

    ## Метроном доступен только после включения света.
    if not renpy.is_skipping():
        call screen c1s1_metronome_start

    ## Две позы одновременно образуют кроссфейд в движении.
    show chapter_1_lamp_hand light_pull at c1s1_hand_fade_out(C1S1_HAND_PULL_POS, C1S1_HAND_LEAVE_POS)
    show chapter_1_lamp_hand light_metronome as c1s1_hand_metronome zorder C1S1_Z_HAND_FRONT at slide_in(C1S1_HAND_METRONOME_FROM, C1S1_HAND_METRONOME_POS, t=C1S1_HAND_SWAP_T)
    $ pause(C1S1_HAND_SWAP_T)
    hide chapter_1_lamp_hand
    $ pause(0.25)

    ## Толчок руки и стрелка стартуют в один кадр.
    show chapter_1_lamp_hand light_metronome as c1s1_hand_metronome at c1s1_hand_poke(C1S1_HAND_METRONOME_POS)
    show chapter_1_metronome_arrow zorder C1S1_Z_ARROW at c1s1_arrow_swing()
    $ pause(C1S1_HAND_EXIT_DELAY)

    show chapter_1_lamp_hand light_metronome as c1s1_hand_metronome at c1s1_hand_exit(C1S1_HAND_METRONOME_POS, C1S1_HAND_EXIT_POS)
    $ pause(C1S1_HAND_EXIT_T)
    hide c1s1_hand_metronome

    ## Пауза учитывает уже прошедшее время ухода руки.
    $ pause(C1S1_ARROW_HALF_T / 2.0 + (C1S1_TICKS_BEFORE_PIANO - 1) * C1S1_ARROW_HALF_T - C1S1_HAND_EXIT_DELAY - C1S1_HAND_EXIT_T)

    ## Пианино: отъезд от ГГ к рукам.
    camera at parallax_push(C1S1_PIANO_FOCUS, C1S1_PIANO_Z0, C1S1_PIANO_Z_END, C1S1_PIANO_OUT_T, strength=C1S1_SCENE_PARALLAX, screen_align=C1S1_PIANO_SCREEN)
    scene chapter_1 piano
    show chapter_1_piano_gg at c1s1_gg_idle()
    with chapter_1_dissolve

    $ pause(C1S1_PIANO_HOLD_T)

    ## Камера рук подхватывает скорость предыдущего отъезда.
    camera at parallax_settle(C1S1_HANDS_FOCUS, C1S1_HANDS_Z0, C1S1_CAM_Z_REST, C1S1_HANDS_T, strength=C1S1_SCENE_PARALLAX)
    scene chapter_1 piano_hands
    show chapter_1_piano_hand_left at c1s1_piano_hand_idle(C1S1_HANDS_LEFT_POS, "hand_l")
    show chapter_1_piano_hand_right at c1s1_piano_hand_idle(C1S1_HANDS_RIGHT_POS, "hand_r", dy=3, t_up=3.3, t_down=2.7)
    with chapter_1_dissolve

    $ pause(C1S1_HANDS_T)

    $ pause(C1S1_KNOCK_HOLD_T)

    ## Первый удар запускает завал камеры на обе серии стука.
    ## TODO(звук): стук в дверь.
    camera at uneasy_sway(C1S1_KNOCK_DRIFT, C1S1_KNOCK_SWAY, speed=C1S1_KNOCK_SWAY_SPEED, zoom_pad=C1S1_KNOCK_PAD, base=C1S1_KNOCK_TILT, base_in_t=C1S1_KNOCK_TILT_T, zoom0=C1S1_CAM_Z_REST)

    ## Первая серия: три удара; show перед punch синхронизирует скачок дрожи.
    $ flash_fx(high=C1S1_KNOCK_FLASH_PEAKS[0], fall=C1S1_KNOCK_FLASH_FALL_T)
    show chapter_1_piano_hand_left at placed_jitter(C1S1_HANDS_LEFT_POS, jitter_amp=C1S1_HANDS_TREMBLE_STEPS[0], jitter_key="c1s1_hand_l")
    show chapter_1_piano_hand_right at placed_jitter(C1S1_HANDS_RIGHT_POS, jitter_amp=C1S1_HANDS_TREMBLE_STEPS[0], jitter_key="c1s1_hand_r")
    with sm_motion_transition(c1s1_knock_punch)
    $ pause(C1S1_KNOCK_GAP_T)
    $ flash_fx(high=C1S1_KNOCK_FLASH_PEAKS[1], fall=C1S1_KNOCK_FLASH_FALL_T)
    show chapter_1_piano_hand_left at placed_jitter(C1S1_HANDS_LEFT_POS, jitter_amp=C1S1_HANDS_TREMBLE_STEPS[1], jitter_key="c1s1_hand_l")
    show chapter_1_piano_hand_right at placed_jitter(C1S1_HANDS_RIGHT_POS, jitter_amp=C1S1_HANDS_TREMBLE_STEPS[1], jitter_key="c1s1_hand_r")
    with sm_motion_transition(c1s1_knock_punch)
    $ pause(C1S1_KNOCK_GAP_T)
    $ flash_fx(high=C1S1_KNOCK_FLASH_PEAKS[2], fall=C1S1_KNOCK_FLASH_FALL_T)
    show chapter_1_piano_hand_left at placed_jitter(C1S1_HANDS_LEFT_POS, jitter_amp=C1S1_HANDS_TREMBLE_STEPS[2], jitter_key="c1s1_hand_l")
    show chapter_1_piano_hand_right at placed_jitter(C1S1_HANDS_RIGHT_POS, jitter_amp=C1S1_HANDS_TREMBLE_STEPS[2], jitter_key="c1s1_hand_r")
    with sm_motion_transition(c1s1_knock_punch)

    ## Пауза между сериями.
    $ pause(C1S1_KNOCK_SERIES_GAP_T)

    ## Вторая серия: три усиленных удара.
    $ flash_fx(high=C1S1_KNOCK_FLASH_PEAKS[3], fall=C1S1_KNOCK_FLASH_FALL2_T)
    show chapter_1_piano_hand_left at placed_jitter(C1S1_HANDS_LEFT_POS, jitter_amp=C1S1_HANDS_TREMBLE_STEPS[3], jitter_key="c1s1_hand_l")
    show chapter_1_piano_hand_right at placed_jitter(C1S1_HANDS_RIGHT_POS, jitter_amp=C1S1_HANDS_TREMBLE_STEPS[3], jitter_key="c1s1_hand_r")
    with sm_motion_transition(c1s1_knock_punch_hard)
    $ pause(C1S1_KNOCK_GAP2_T)
    $ flash_fx(high=C1S1_KNOCK_FLASH_PEAKS[4], fall=C1S1_KNOCK_FLASH_FALL2_T)
    show chapter_1_piano_hand_left at placed_jitter(C1S1_HANDS_LEFT_POS, jitter_amp=C1S1_HANDS_TREMBLE_STEPS[4], jitter_key="c1s1_hand_l")
    show chapter_1_piano_hand_right at placed_jitter(C1S1_HANDS_RIGHT_POS, jitter_amp=C1S1_HANDS_TREMBLE_STEPS[4], jitter_key="c1s1_hand_r")
    with sm_motion_transition(c1s1_knock_punch_hard)
    $ pause(C1S1_KNOCK_GAP2_T)
    $ flash_fx(high=C1S1_KNOCK_FLASH_PEAKS[5], fall=C1S1_KNOCK_FLASH_FALL2_T)
    show chapter_1_piano_hand_left at placed_jitter(C1S1_HANDS_LEFT_POS, jitter_amp=C1S1_HANDS_TREMBLE_STEPS[5], jitter_key="c1s1_hand_l")
    show chapter_1_piano_hand_right at placed_jitter(C1S1_HANDS_RIGHT_POS, jitter_amp=C1S1_HANDS_TREMBLE_STEPS[5], jitter_key="c1s1_hand_r")
    with sm_motion_transition(c1s1_knock_punch_hard)

    $ pause(2.0)

    ## Холл: камера возвращается к спокойному параллаксу.
    camera at mouse_parallax(strength=C1S1_SCENE_PARALLAX, zoom_pad=C1S1_CAM_Z_REST)
    scene chapter_1 hall
    show chapter_1_hall_door zorder C1S1_Z_HALL_DOOR at placed(C1S1_HALL_DOOR_POS)
    show chapter_1_hall_boots zorder C1S1_Z_HALL_GROUP_0 at placed(C1S1_HALL_BOOTS_POS)
    show chapter_1_hall_packet zorder C1S1_Z_HALL_GROUP_0 + 1 at placed(C1S1_HALL_PACKET_POS)
    show chapter_1_hall_toy zorder C1S1_Z_HALL_GROUP_0 + 2 at placed(C1S1_HALL_TOY_POS)
    show chapter_1_hall_paper zorder C1S1_Z_HALL_GROUP_1 at placed(C1S1_HALL_PAPER_POS)
    show chapter_1_hall_bag zorder C1S1_Z_HALL_GROUP_1 + 1 at placed(C1S1_HALL_BAG_POS)
    show chapter_1_hall_bottles zorder C1S1_Z_HALL_GROUP_1 + 2 at placed(C1S1_HALL_BOTTLES_POS)
    show chapter_1_hall_umbrella_1 zorder C1S1_Z_HALL_GROUP_2 at placed(C1S1_HALL_UMBRELLA_1_POS)
    show chapter_1_hall_umbrella_2 zorder C1S1_Z_HALL_GROUP_2 + 1 at placed(C1S1_HALL_UMBRELLA_2_POS)
    show chapter_1_hall_mirror zorder C1S1_Z_HALL_MIRROR at placed(C1S1_HALL_MIRROR_POS)
    show chapter_1_hall_mop zorder C1S1_Z_HALL_MOP at placed(C1S1_HALL_MOP_POS)

    $ pause(0.5)

    ## Стук продолжается в холле; предметы у стен дрожат.
    $ pause(C1S1_HALL_KNOCK_HOLD_T)
    show chapter_1_hall_mop zorder C1S1_Z_HALL_MOP at placed_jitter(C1S1_HALL_MOP_POS, jitter_amp=C1S1_HALL_OBJ_TREMBLE, jitter_key="hall_mop")
    show chapter_1_hall_umbrella_1 zorder C1S1_Z_HALL_GROUP_2 at placed_jitter(C1S1_HALL_UMBRELLA_1_POS, jitter_amp=C1S1_HALL_OBJ_TREMBLE, jitter_key="hall_umb1")
    show chapter_1_hall_umbrella_2 zorder C1S1_Z_HALL_GROUP_2 + 1 at placed_jitter(C1S1_HALL_UMBRELLA_2_POS, jitter_amp=C1S1_HALL_OBJ_TREMBLE, jitter_key="hall_umb2")
    show chapter_1_hall_bottles zorder C1S1_Z_HALL_GROUP_1 + 2 at placed_jitter(C1S1_HALL_BOTTLES_POS, jitter_amp=C1S1_HALL_OBJ_TREMBLE, jitter_key="hall_bottles")

    ## TODO(звук): стук в дверь.
    $ flash_fx(high=C1S1_HALL_KNOCK_FLASH, fall=C1S1_HALL_KNOCK_FLASH_FALL_T)
    with sm_motion_transition(c1s1_hall_knock_punch)
    $ pause(C1S1_HALL_KNOCK_GAP_T)
    $ flash_fx(high=C1S1_HALL_KNOCK_FLASH, fall=C1S1_HALL_KNOCK_FLASH_FALL_T)
    with sm_motion_transition(c1s1_hall_knock_punch)
    $ pause(C1S1_HALL_KNOCK_GAP_T)

    ## Третий удар склеен с дверью крупным планом.
    $ flash_fx(high=C1S1_HALL_KNOCK_FLASH, fall=C1S1_HALL_KNOCK_FLASH_FALL_T)
    with sm_motion_transition(c1s1_hall_knock_punch)
    $ pause(C1S1_HALL_CUT_T)

    ## Вспышка на always_shown-экране досвечивает новый кадр после scene.
    scene chapter_1 door
    show chapter_1_door_hand hit at placed(C1S1_DOOR_HAND_HIT_POS)
    with sm_motion_transition(c1s1_door_hit_punch)

    ## Ещё два удара с замахом.
    ## TODO(звук): стук в дверь крупным планом.
    $ pause(C1S1_DOOR_OPEN_HOLD_T)
    show chapter_1_door_hand wind at placed(C1S1_DOOR_HAND_WIND_POS)
    $ pause(C1S1_DOOR_WIND_T)
    show chapter_1_door_hand hit at placed(C1S1_DOOR_HAND_HIT_POS)
    with sm_motion_transition(c1s1_door_hit_punch)

    ## Последний удар склеен с видом двери из квартиры.
    $ pause(C1S1_DOOR_KNOCK_GAP_T)
    show chapter_1_door_hand wind at placed(C1S1_DOOR_HAND_WIND_POS)
    $ pause(C1S1_DOOR_WIND_T)
    $ flash_fx(high=C1S1_LOCKS_FLASH_PEAKS[0], fall=C1S1_LOCKS_FLASH_FALL_T)
    show chapter_1_door_hand hit at placed(C1S1_DOOR_HAND_HIT_POS)
    with sm_motion_transition(c1s1_door_hit_punch)
    $ pause(C1S1_DOOR_CUT_T)

    ## Дверь изнутри: спокойный наезд на замки, сумка дрожит от ударов.
    ## TODO(звук): стук в дверь изнутри квартиры.
    camera at parallax_push(C1S1_LOCKS_FOCUS, C1S1_CAM_Z_REST, C1S1_LOCKS_Z1, C1S1_LOCKS_PUSH_T, strength=C1S1_SCENE_PARALLAX)
    scene chapter_1 hall_door
    show chapter_1_hall_door_bag zorder C1S1_Z_DOOR_BAG at placed_jitter(C1S1_DOOR_BAG_POS, anchor_xy=C1S1_DOOR_BAG_ANCHOR, jitter_amp=C1S1_LOCKS_BAG_TREMBLE[0], jitter_key="c1s1_door_bag")
    with sm_motion_transition(c1s1_locks_knock_punch)

    ## Ещё два удара; show перед punch синхронизирует дрожь сумки.
    $ pause(C1S1_LOCKS_KNOCK_GAP_T)
    $ flash_fx(high=C1S1_LOCKS_FLASH_PEAKS[1], fall=C1S1_LOCKS_FLASH_FALL_T)
    show chapter_1_hall_door_bag zorder C1S1_Z_DOOR_BAG at placed_jitter(C1S1_DOOR_BAG_POS, anchor_xy=C1S1_DOOR_BAG_ANCHOR, jitter_amp=C1S1_LOCKS_BAG_TREMBLE[1], jitter_key="c1s1_door_bag")
    with sm_motion_transition(c1s1_locks_knock_punch)
    $ pause(C1S1_LOCKS_KNOCK_GAP_T)
    $ flash_fx(high=C1S1_LOCKS_FLASH_PEAKS[2], fall=C1S1_LOCKS_FLASH_FALL_T)
    show chapter_1_hall_door_bag zorder C1S1_Z_DOOR_BAG at placed_jitter(C1S1_DOOR_BAG_POS, anchor_xy=C1S1_DOOR_BAG_ANCHOR, jitter_amp=C1S1_LOCKS_BAG_TREMBLE[2], jitter_key="c1s1_door_bag")
    with sm_motion_transition(c1s1_locks_knock_punch)

    ## Ложная тишина; общий jitter_key сохраняет фазу затухания.
    $ pause(C1S1_LOCKS_SETTLE_T)
    show chapter_1_hall_door_bag zorder C1S1_Z_DOOR_BAG at placed_jitter(C1S1_DOOR_BAG_POS, anchor_xy=C1S1_DOOR_BAG_ANCHOR, jitter_amp=C1S1_LOCKS_BAG_CALM, jitter_key="c1s1_door_bag")
    $ pause(C1S1_LOCKS_SERIES_GAP_T)

    ## Стук возвращается двумя усиленными ударами.
    $ flash_fx(high=C1S1_LOCKS_FLASH_PEAKS[3], fall=C1S1_LOCKS_FLASH_FALL2_T)
    show chapter_1_hall_door_bag zorder C1S1_Z_DOOR_BAG at placed_jitter(C1S1_DOOR_BAG_POS, anchor_xy=C1S1_DOOR_BAG_ANCHOR, jitter_amp=C1S1_LOCKS_BAG_TREMBLE[3], jitter_key="c1s1_door_bag")
    with sm_motion_transition(c1s1_locks_knock_punch_hard)
    $ pause(C1S1_LOCKS_KNOCK_GAP2_T)
    $ flash_fx(high=C1S1_LOCKS_FLASH_PEAKS[4], fall=C1S1_LOCKS_FLASH_FALL2_T)
    show chapter_1_hall_door_bag zorder C1S1_Z_DOOR_BAG at placed_jitter(C1S1_DOOR_BAG_POS, anchor_xy=C1S1_DOOR_BAG_ANCHOR, jitter_amp=C1S1_LOCKS_BAG_TREMBLE[4], jitter_key="c1s1_door_bag")
    with sm_motion_transition(c1s1_locks_knock_punch_hard)

    ## Финальное затухание.
    $ pause(C1S1_LOCKS_SETTLE_T)
    show chapter_1_hall_door_bag zorder C1S1_Z_DOOR_BAG at placed_jitter(C1S1_DOOR_BAG_POS, anchor_xy=C1S1_DOOR_BAG_ANCHOR, jitter_amp=C1S1_LOCKS_BAG_CALM, jitter_key="c1s1_door_bag")
    $ pause(C1S1_LOCKS_SETTLE_T)
    show chapter_1_hall_door_bag zorder C1S1_Z_DOOR_BAG at placed_jitter(C1S1_DOOR_BAG_POS, anchor_xy=C1S1_DOOR_BAG_ANCHOR, jitter_amp=0.0, jitter_key="c1s1_door_bag")

    ## Переход к мини-игре с замками.
    call chapter_1_scene_1_minigame_locks from _call_c1s1_minigame_locks

    $ dismiss_on()

    call .after_locks from _call_chapter_1_scene_1_after_locks

    return

label .after_locks:

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

    return
