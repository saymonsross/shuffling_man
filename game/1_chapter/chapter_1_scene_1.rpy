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
    C1S1_TV_WIDE_POS, C1S1_TV_WIDE_SIZE, ((2, 2), (402, 2), (402, 282), (2, 282)))
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

define chapter_1_fade_in = Dissolve(2.0)
define chapter_1_dissolve = Dissolve(1.2)

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

## Трансформы сцены

transform c1s1_hand_pull(pos_xy, dy=18, t=0.16):
    subpixel True
    anchor (0.0, 0.0)
    pos pos_xy
    easein t yoffset dy

## Продолжает рывок из yoffset dy уже в светлой позе.
transform c1s1_hand_release(pos_xy, dy=18, over=10, up_t=0.45, settle_t=0.35):
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

transform c1s1_hand_fade_out(from_xy, to_xy, t=0.8):
    subpixel True
    anchor (0.0, 0.0)
    pos from_xy
    alpha 1.0
    ease t pos to_xy alpha 0.0

transform c1s1_hand_exit(from_xy, to_xy, t=1.1):
    subpixel True
    anchor (0.0, 0.0)
    pos from_xy
    ease t pos to_xy alpha 0.0

## Якорь стрелки совпадает с нижним креплением маятника (спрайт 45×368, bbox (985, 292)).
transform c1s1_arrow_rest(pos_xy=(1007, 660)):
    subpixel True
    transform_anchor True
    anchor (0.5, 1.0)
    pos pos_xy
    rotate 0.0

## Положительный rotate продолжает толчок руки вправо.
## Звуковой loop запускается вместе со стрелкой и переживает смену кадра.
transform c1s1_arrow_swing(pos_xy=(1007, 660), amp=20.0, half_t=C1S1_ARROW_HALF_T):
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

## ГГ заякорен за низ фигуры — это пивот покачивания и масштаба.
## transform_anchor не даёт rotate_pad сместить пивот фигуры.
## ГГ и руки — ближний план: parallax_near отделяет их от фона.
transform c1s1_gg_idle(pos_xy=(998, 1080)):
    subpixel True
    transform_anchor True
    anchor (0.5, 1.0)
    pos pos_xy
    xoffset 0.0 yoffset 0.0
    rotate 0.0
    parallel:
        function parallax_near_f
    parallel:
        ease 2.7 rotate (0.35 * sm_motion_scale()) yzoom (1.0 + 0.004 * sm_motion_scale())
        ease 3.4 rotate (-0.3 * sm_motion_scale()) yzoom 1.0
        repeat

## Координаты явно absolute: float без обёртки Ren'Py трактует как долю экрана.
transform c1s1_piano_hand_idle(pos_xy, dy=4, t_up=2.9, t_down=3.6):
    subpixel True
    anchor (0.0, 0.0)
    xpos absolute(pos_xy[0])
    ypos absolute(pos_xy[1])
    xoffset 0.0 yoffset 0.0
    parallel:
        function parallax_near_f
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
            pos=(475, 530),
            size=(330, 165))

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
            pos=(1005, 530),
            size=(430, 190))

## Сцена

label chapter_1_scene_1:

    $ dismiss_off()

    ## Лампа.
    camera at camera_push(C1S1_LAMP_FOCUS, 1.04, 1.14, 25.0)
    scene chapter_1 lamp_dark
    show chapter_1_lampshade dark zorder 10 at placed((183, 0))
    with chapter_1_fade_in

    $ pause(1.0)

    ## Интерактивы не создают развилок и пропускаются вместе со сценой.
    if not renpy.is_skipping():
        call screen c1s1_lamp_switch

    show chapter_1_lamp_hand dark_reach zorder 15 at slide_in((-560, 700), (0, 178), t=1.8)
    $ pause(1.8)
    $ pause(0.5)

    show chapter_1_lamp_hand dark_pull zorder 5 at placed((0, 68))
    with Dissolve(0.45)
    $ pause(0.4)

    show chapter_1_lamp_hand dark_pull at c1s1_hand_pull((0, 68))
    $ pause(0.16)

    ## Щелчок и мгновенная смена освещения без сброса камеры.
    $ sm_sfx("c1s1/lamp_switch", volume=0.9)
    ## Нижняя часть корпуса закрывает пивот стрелки, руки остаются перед метрономом.
    scene chapter_1 lamp_light
    show chapter_1_metronome_arrow zorder 3 at c1s1_arrow_rest()
    ## Точный фрагмент светлого фона ниже прорези: (835, 640, 1171, 777).
    show chapter_1_metronome_foreground zorder 4 at placed((835, 640))
    show chapter_1_lampshade light zorder 10 at placed((183, 0))
    show chapter_1_lamp_hand light_pull zorder 5 at c1s1_hand_release((0, 68))
    $ pause(0.45 + 0.35)
    $ pause(0.5)

    ## Метроном доступен только после включения света.
    if not renpy.is_skipping():
        call screen c1s1_metronome_start

    ## Две позы одновременно образуют кроссфейд в движении.
    show chapter_1_lamp_hand light_pull at c1s1_hand_fade_out((0, 68), (150, 120))
    show chapter_1_lamp_hand light_metronome as c1s1_hand_metronome zorder 15 at slide_in((-75, 450), (100, 330), t=0.8)
    $ pause(0.8)
    hide chapter_1_lamp_hand
    $ pause(0.25)

    ## Толчок руки и стрелка стартуют в один кадр.
    $ c1s1_metronome_audio = sfxplay(C1S1_METRONOME_LOOP_SOUND, ext="wav", fadein=0, fadeout=0, tag="c1s1_metronome", volume=C1S1_METRONOME_TICK_VOL)
    show chapter_1_lamp_hand light_metronome as c1s1_hand_metronome at c1s1_hand_poke((100, 330))
    show chapter_1_metronome_arrow zorder 3 at c1s1_arrow_swing()
    $ pause(0.5)

    show chapter_1_lamp_hand light_metronome as c1s1_hand_metronome at c1s1_hand_exit((100, 330), (-320, 760))
    $ pause(1.1)
    hide c1s1_hand_metronome

    ## Пауза учитывает уже прошедшее время ухода руки.
    $ pause(C1S1_ARROW_HALF_T / 2.0 + (4 - 1) * C1S1_ARROW_HALF_T - 0.5 - 1.1)

    ## Пианино: отъезд от ГГ к рукам.
    camera at camera_push((0.52, 0.55), 1.35, 1.06, 10.5, screen_align=(0.5, 0.55))
    scene chapter_1 piano
    show chapter_1_piano_gg at c1s1_gg_idle()
    with chapter_1_dissolve

    $ pause(7.0)

    ## Камера рук подхватывает отъезд до его завершения: скорости зума
    ## согласованы, ≈0.038/с у ГГ и ≈0.037/с у рук.
    camera at camera_settle((0.51, 0.61), 1.10, 1.02, 3.4)
    scene chapter_1 piano_hands
    show chapter_1_piano_hand_left at c1s1_piano_hand_idle((330, 284))
    show chapter_1_piano_hand_right at c1s1_piano_hand_idle((1113, 276), dy=3, t_up=3.3, t_down=2.7)
    with chapter_1_dissolve

    $ pause(3.4)

    $ pause(1.5)

    ## Первый удар запускает завал камеры на обе серии стука.
    ## Запас зума для поворота до 6.7°: минимум ≈1.20.
    $ c1s1_metronome_tension()
    camera at uneasy_sway(10.0, 1.2, speed=1.4, zoom_pad=1.22, base=-5.5, base_in_t=7.0, zoom0=1.02)

    ## Первая серия: три удара; show перед punch синхронизирует скачок дрожи.
    $ sm_sfx(("c1s1/knock_far_1", "c1s1/knock_far_2", "c1s1/knock_far_3"), volume=0.58)
    $ flash_fx(high=0.18, fall=0.22)
    show chapter_1_piano_hand_left at placed_jitter((330, 284), jitter_amp=0.8, jitter_key="c1s1_hand_l")
    show chapter_1_piano_hand_right at placed_jitter((1113, 276), jitter_amp=0.8, jitter_key="c1s1_hand_r")
    with sm_motion_transition(c1s1_knock_punch)
    $ pause(0.3)
    $ sm_sfx(("c1s1/knock_far_1", "c1s1/knock_far_2", "c1s1/knock_far_3"), volume=0.66)
    $ flash_fx(high=0.22, fall=0.22)
    show chapter_1_piano_hand_left at placed_jitter((330, 284), jitter_amp=1.4, jitter_key="c1s1_hand_l")
    show chapter_1_piano_hand_right at placed_jitter((1113, 276), jitter_amp=1.4, jitter_key="c1s1_hand_r")
    with sm_motion_transition(c1s1_knock_punch)
    $ pause(0.3)
    $ sm_sfx(("c1s1/knock_far_1", "c1s1/knock_far_2", "c1s1/knock_far_3"), volume=0.74)
    $ flash_fx(high=0.26, fall=0.22)
    show chapter_1_piano_hand_left at placed_jitter((330, 284), jitter_amp=2.0, jitter_key="c1s1_hand_l")
    show chapter_1_piano_hand_right at placed_jitter((1113, 276), jitter_amp=2.0, jitter_key="c1s1_hand_r")
    with sm_motion_transition(c1s1_knock_punch)

    ## Пауза между сериями.
    $ pause(1.7)

    ## Вторая серия: три усиленных удара.
    $ sm_sfx(("c1s1/knock_far_1", "c1s1/knock_far_2", "c1s1/knock_far_3"), volume=0.86)
    $ flash_fx(high=0.34, fall=0.16)
    show chapter_1_piano_hand_left at placed_jitter((330, 284), jitter_amp=2.8, jitter_key="c1s1_hand_l")
    show chapter_1_piano_hand_right at placed_jitter((1113, 276), jitter_amp=2.8, jitter_key="c1s1_hand_r")
    with sm_motion_transition(c1s1_knock_punch_hard)
    $ pause(0.18)
    $ sm_sfx(("c1s1/knock_far_1", "c1s1/knock_far_2", "c1s1/knock_far_3"), volume=0.93)
    $ flash_fx(high=0.40, fall=0.16)
    show chapter_1_piano_hand_left at placed_jitter((330, 284), jitter_amp=3.6, jitter_key="c1s1_hand_l")
    show chapter_1_piano_hand_right at placed_jitter((1113, 276), jitter_amp=3.6, jitter_key="c1s1_hand_r")
    with sm_motion_transition(c1s1_knock_punch_hard)
    $ pause(0.18)
    $ sm_sfx(("c1s1/knock_far_1", "c1s1/knock_far_2", "c1s1/knock_far_3"), volume=1.0)
    $ flash_fx(high=0.48, fall=0.16)
    show chapter_1_piano_hand_left at placed_jitter((330, 284), jitter_amp=4.5, jitter_key="c1s1_hand_l")
    show chapter_1_piano_hand_right at placed_jitter((1113, 276), jitter_amp=4.5, jitter_key="c1s1_hand_r")
    with sm_motion_transition(c1s1_knock_punch_hard)

    $ pause(2.0)

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

    $ pause(0.5)

    ## Стук продолжается в холле; предметы у стен дрожат.
    $ pause(1.0)
    show chapter_1_hall_mop zorder 40 at placed_jitter((924, 302), jitter_amp=2.0, jitter_key="hall_mop")
    show chapter_1_hall_umbrella_1 zorder 30 at placed_jitter((267, 562), jitter_amp=2.0, jitter_key="hall_umb1")
    show chapter_1_hall_umbrella_2 zorder 30 + 1 at placed_jitter((374, 655), jitter_amp=2.0, jitter_key="hall_umb2")
    show chapter_1_hall_bottles zorder 20 + 2 at placed_jitter((334, 463), jitter_amp=2.0, jitter_key="hall_bottles")

    $ sm_sfx(("c1s1/knock_hall_1", "c1s1/knock_hall_2", "c1s1/knock_hall_3"), volume=0.85)
    $ flash_fx(high=0.16, fall=0.3)
    with sm_motion_transition(c1s1_hall_knock_punch)
    $ pause(0.45)
    $ sm_sfx(("c1s1/knock_hall_1", "c1s1/knock_hall_2", "c1s1/knock_hall_3"), volume=0.85)
    $ flash_fx(high=0.16, fall=0.3)
    with sm_motion_transition(c1s1_hall_knock_punch)
    $ pause(0.45)

    ## Третий удар склеен с дверью крупным планом.
    $ sm_sfx(("c1s1/knock_hall_1", "c1s1/knock_hall_2", "c1s1/knock_hall_3"), volume=0.85)
    $ flash_fx(high=0.16, fall=0.3)
    with sm_motion_transition(c1s1_hall_knock_punch)
    $ pause(0.08)

    ## Вспышка на always_shown-экране досвечивает новый кадр после scene.
    scene chapter_1 door
    $ sm_sfx(("c1s1/knock_door_1", "c1s1/knock_door_2", "c1s1/knock_door_3"), volume=1.0)
    show chapter_1_door_hand hit at placed((1158, 147))
    with sm_motion_transition(c1s1_door_hit_punch)

    ## Ещё два удара с замахом.
    $ pause(0.6)
    show chapter_1_door_hand wind at placed((769, 131))
    $ pause(0.28)
    $ sm_sfx(("c1s1/knock_door_1", "c1s1/knock_door_2", "c1s1/knock_door_3"), volume=1.0)
    show chapter_1_door_hand hit at placed((1158, 147))
    with sm_motion_transition(c1s1_door_hit_punch)

    ## Последний удар склеен с видом двери из квартиры.
    $ pause(0.5)
    show chapter_1_door_hand wind at placed((769, 131))
    $ pause(0.28)
    $ flash_fx(high=0.22, fall=0.22)
    $ sm_sfx(("c1s1/knock_door_1", "c1s1/knock_door_2", "c1s1/knock_door_3"), volume=1.0)
    show chapter_1_door_hand hit at placed((1158, 147))
    with sm_motion_transition(c1s1_door_hit_punch)
    $ pause(0.08)

    ## Дверь изнутри: спокойный наезд на замки, сумка дрожит от ударов.
    ## Третий удар двери крупным планом уже озвучен: рез склеен с ним.
    camera at camera_push(C1S1_LOCKS_FOCUS, 1.02, 1.16, 8.8)
    scene chapter_1 hall_door
    show chapter_1_hall_door_bag zorder C1S1_Z_DOOR_BAG at placed_jitter(C1S1_DOOR_BAG_POS, anchor_xy=C1S1_DOOR_BAG_ANCHOR, jitter_amp=2.0, jitter_key="c1s1_door_bag")
    with sm_motion_transition(c1s1_locks_knock_punch)

    ## Ещё два удара; show перед punch синхронизирует дрожь сумки.
    $ pause(0.5)
    $ sm_sfx(("c1s1/knock_inside_1", "c1s1/knock_inside_2", "c1s1/knock_inside_3"), volume=0.88)
    $ flash_fx(high=0.26, fall=0.22)
    show chapter_1_hall_door_bag zorder C1S1_Z_DOOR_BAG at placed_jitter(C1S1_DOOR_BAG_POS, anchor_xy=C1S1_DOOR_BAG_ANCHOR, jitter_amp=2.6, jitter_key="c1s1_door_bag")
    with sm_motion_transition(c1s1_locks_knock_punch)
    $ pause(0.5)
    $ sm_sfx(("c1s1/knock_inside_1", "c1s1/knock_inside_2", "c1s1/knock_inside_3"), volume=0.94)
    $ flash_fx(high=0.30, fall=0.22)
    show chapter_1_hall_door_bag zorder C1S1_Z_DOOR_BAG at placed_jitter(C1S1_DOOR_BAG_POS, anchor_xy=C1S1_DOOR_BAG_ANCHOR, jitter_amp=3.2, jitter_key="c1s1_door_bag")
    with sm_motion_transition(c1s1_locks_knock_punch)

    ## Ложная тишина; общий jitter_key сохраняет фазу затухания.
    $ pause(1.6)
    show chapter_1_hall_door_bag zorder C1S1_Z_DOOR_BAG at placed_jitter(C1S1_DOOR_BAG_POS, anchor_xy=C1S1_DOOR_BAG_ANCHOR, jitter_amp=0.8, jitter_key="c1s1_door_bag")
    $ pause(1.4)

    ## Стук возвращается двумя усиленными ударами.
    $ sm_sfx(("c1s1/knock_inside_1", "c1s1/knock_inside_2", "c1s1/knock_inside_3"), volume=1.0)
    $ flash_fx(high=0.38, fall=0.16)
    show chapter_1_hall_door_bag zorder C1S1_Z_DOOR_BAG at placed_jitter(C1S1_DOOR_BAG_POS, anchor_xy=C1S1_DOOR_BAG_ANCHOR, jitter_amp=4.0, jitter_key="c1s1_door_bag")
    with sm_motion_transition(c1s1_locks_knock_punch_hard)
    $ pause(0.34)
    $ sm_sfx(("c1s1/knock_inside_1", "c1s1/knock_inside_2", "c1s1/knock_inside_3"), volume=1.0)
    $ flash_fx(high=0.44, fall=0.16)
    show chapter_1_hall_door_bag zorder C1S1_Z_DOOR_BAG at placed_jitter(C1S1_DOOR_BAG_POS, anchor_xy=C1S1_DOOR_BAG_ANCHOR, jitter_amp=4.8, jitter_key="c1s1_door_bag")
    with sm_motion_transition(c1s1_locks_knock_punch_hard)

    ## Финальное затухание.
    $ pause(1.6)
    show chapter_1_hall_door_bag zorder C1S1_Z_DOOR_BAG at placed_jitter(C1S1_DOOR_BAG_POS, anchor_xy=C1S1_DOOR_BAG_ANCHOR, jitter_amp=0.8, jitter_key="c1s1_door_bag")
    $ pause(1.6)
    show chapter_1_hall_door_bag zorder C1S1_Z_DOOR_BAG at placed_jitter(C1S1_DOOR_BAG_POS, anchor_xy=C1S1_DOOR_BAG_ANCHOR, jitter_amp=0.0, jitter_key="c1s1_door_bag")

    ## Переход к мини-игре с замками.
    call chapter_1_scene_1_minigame_locks from _call_c1s1_minigame_locks

    $ dismiss_on()

    call .after_locks from _call_chapter_1_scene_1_after_locks

    return

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

    return
