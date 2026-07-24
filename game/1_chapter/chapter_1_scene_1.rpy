################################################################################
## Глава 1 — сцена 1: тёмная комната → рука включает лампу (мгновенный переход
## в светлое состояние) → запуск метронома → пианино (отдаление от ГГ) → руки
## над клавишами. Чистая кат-сцена без реплик, управление игроку недоступно.
################################################################################

## Изображения ##################################################################

## Полноэкранные кадры сцены.
image chapter_1 lamp_dark = "images/1_chapter/chapter_1 lamp_dark.jpg"
image chapter_1 lamp_light = "images/1_chapter/chapter_1 lamp_light.jpg"
image chapter_1 piano = "images/1_chapter/chapter_1 piano.jpg"
image chapter_1 piano_hands = "images/1_chapter/chapter_1 piano_hands.jpg"

## Слои композиции у лампы (позиции сверены с ch_1_metronome_lamp_all_*.jpg
## по слоям PSD — точное попадание пиксель в пиксель).
image chapter_1_lampshade dark = "images/1_chapter/chapter_1_lampshade dark.png"
image chapter_1_lampshade light = "images/1_chapter/chapter_1_lampshade light.png"

image chapter_1_lamp_hand dark_reach = "images/1_chapter/chapter_1_lamp_hand dark_reach.png"
image chapter_1_lamp_hand dark_pull = "images/1_chapter/chapter_1_lamp_hand dark_pull.png"
image chapter_1_lamp_hand light_pull = "images/1_chapter/chapter_1_lamp_hand light_pull.png"
image chapter_1_lamp_hand light_metronome = "images/1_chapter/chapter_1_lamp_hand light_metronome.png"

image chapter_1_metronome_arrow = "images/1_chapter/chapter_1_metronome_arrow.png"

## Слои сцен с пианино.
image chapter_1_piano_gg = "images/1_chapter/chapter_1_piano_gg.png"
image chapter_1_piano_hand_left = "images/1_chapter/chapter_1_piano_hand_left.png"
image chapter_1_piano_hand_right = "images/1_chapter/chapter_1_piano_hand_right.png"

## Константы сцены ##############################################################

## Порядок слоёв: стрелка за всем, рука под абажуром, абажур, рука поверх.
define C1S1_Z_ARROW = 3
define C1S1_Z_HAND_BEHIND = 5
define C1S1_Z_SHADE = 10
define C1S1_Z_HAND_FRONT = 15

## Размещение (левые-верхние углы спрайтов, px; из bbox слоёв PSD).
define C1S1_LAMPSHADE_POS = (183, 0)
define C1S1_HAND_REACH_POS = (0, 178)      # рука легла на абажур (поверх)
define C1S1_HAND_PULL_POS = (0, 68)        # кисть под абажуром, у шнурка
## Поза у метронома смещена влево-вниз относительно слоя PSD (235, 200):
## так стрелки касаются кончики пальцев, а не ладонь (сверено рендером).
define C1S1_HAND_METRONOME_POS = (100, 330)
define C1S1_HAND_ENTER_POS = (-560, 700)   # въезд из-за нижнего левого края
define C1S1_HAND_LEAVE_POS = (150, 120)    # точка растворения позы у лампы
define C1S1_HAND_METRONOME_FROM = (-75, 450)  # поза у метронома проявляется в движении
define C1S1_HAND_EXIT_POS = (-320, 760)    # уход руки из кадра после толчка

## Тайминги руки.
define C1S1_HAND_ENTER_T = 1.8   # въезд в кадр; pause после show той же длины
define C1S1_PULL_DY = 18         # ход рывка за шнурок вниз, px
define C1S1_PULL_T = 0.16
define C1S1_RELEASE_OVER = 10    # заброс вверх по инерции после щелчка, px
define C1S1_RELEASE_T = 0.45
define C1S1_SETTLE_T = 0.35      # возврат из заброса в базовое положение
define C1S1_HAND_SWAP_T = 0.8    # кроссфейд поз в движении к метроному
define C1S1_HAND_EXIT_DELAY = 0.5  # заминка после толчка перед уходом
define C1S1_HAND_EXIT_T = 1.1

## Метроном: пивот стрелки — низ маятника (спрайт 45×368, bbox (985, 292)).
define C1S1_ARROW_PIVOT_POS = (1007, 660)
define C1S1_ARROW_AMP = 20.0     # амплитуда качания, градусы
define C1S1_ARROW_HALF_T = 0.75  # полкачания между щелчками ≈ 80 BPM
define C1S1_TICKS_BEFORE_PIANO = 4

## Камера. Наезд у лампы — к точке между лампой и метрономом, чуть левее и
## выше центра кадра (динамика, не «в лоб»).
define C1S1_SCENE_PARALLAX = 8.0
define C1S1_CAM_Z_REST = 1.02      # зум покоя — запас краёв под параллакс
define C1S1_LAMP_FOCUS = (0.44, 0.44)
define C1S1_LAMP_Z0 = 1.04
define C1S1_LAMP_Z1 = 1.14
define C1S1_LAMP_PUSH_T = 25.0     # наезд длиннее сцены — не останавливается

## Пианино: старт вплотную к ГГ, длинное отдаление. Точка ГГ (0.52 ширины
## кадра) пришпилена к центру экрана (screen_align) — ГГ ровно по центру весь
## отъезд; конечный зум 1.06 оставляет для этого запас краёв. Переход к рукам —
## не дожидаясь конца (на C1S1_PIANO_HOLD_T), руки завершают движение.
## Длительность 10.5 с даёт тот же темп отдаления, что исходные 1.35→1.02
## за 12 с (путь укоротился с 0.33 до 0.29 — время сокращено пропорционально).
## Скорость зума в точке перехода ≈ 0.29 × (π/2) × sin(π×0.67) / 10.5 ≈ 0.038/с,
## стартовая скорость easein у рук 0.08 × (π/2) / 3.4 ≈ 0.037/с — совпадает.
define C1S1_PIANO_FOCUS = (0.52, 0.55)     # центр фигуры ГГ в долях кадра
define C1S1_PIANO_SCREEN = (0.5, 0.55)     # куда пришпилен: центр экрана по X
define C1S1_PIANO_Z0 = 1.35
define C1S1_PIANO_Z_END = 1.06
define C1S1_PIANO_OUT_T = 10.5
define C1S1_PIANO_HOLD_T = 7.0
define C1S1_HANDS_FOCUS = (0.51, 0.61)     # между кистями
define C1S1_HANDS_Z0 = 1.10
define C1S1_HANDS_T = 3.4

## Пианино: размещение. ГГ заякорен за низ фигуры по центру (левый край слоя
## PSD 817 + половина ширины 363) — пивот покачивания и «дыхания» корпуса.
define C1S1_GG_POS = (998, 1080)
define C1S1_GG_PARALLAX = 3.0    # очень слабый объектный параллакс ГГ
define C1S1_HANDS_LEFT_POS = (330, 284)
define C1S1_HANDS_RIGHT_POS = (1113, 276)

## Стук в дверь (визуализация звука — knock_at, common/knock_fx.rpy).
## Звук бьёт отовсюду: каждый удар вспыхивает в новой части экрана, экран
## вздрагивает в такт (punch-транзишены). Две серии по три удара с паузой.
## Камера с первым ударом начинает заваливаться набок (uneasy_sway с base):
## завал тянется через обе серии — тревога нарастает всю концовку сцены.
## Точки ударов: серия 1 — [0..2], серия 2 — [3..5]; в пределах видимой
## при зуме C1S1_KNOCK_PAD области кадра.
define C1S1_KNOCK_POSES = ((320, 260), (1500, 700), (980, 190), (430, 800), (1460, 250), (900, 560))
define C1S1_KNOCK_HOLD_T = 1.5      # тишина после остановки рук до первого удара
define C1S1_KNOCK_GAP_T = 0.3       # пауза между ударами (сверх punch-тряски)
define C1S1_KNOCK_GAP2_T = 0.18     # вторая серия — настойчивее
define C1S1_KNOCK_SERIES_GAP_T = 1.7  # тишина между сериями
define C1S1_KNOCK_TILT = -5.5       # базовый завал горизонта, градусы
define C1S1_KNOCK_TILT_T = 7.0      # время завала — накрывает обе серии
define C1S1_KNOCK_SWAY = 1.2        # амплитуда покачивания вокруг завала
## Запас зума под поворот: |TILT| + SWAY ≈ 6.7° требует ≥ cos + (16/9)·sin ≈ 1.20.
define C1S1_KNOCK_PAD = 1.22
define C1S1_KNOCK_DRIFT = 10.0      # дрейф покачивания, px
define C1S1_KNOCK_SWAY_SPEED = 1.4
## Дрожь замерших рук (px): включается с первым ударом и нарастает с каждым
## следующим — по шагу на удар (6 ударов). Накопитель дрожи (jitter_key)
## продолжается между show — смена амплитуды без рывка.
define C1S1_HANDS_TREMBLE_STEPS = (0.8, 1.4, 2.0, 2.8, 3.6, 4.5)

## Вздрагивание экрана в такт удару (по образцу штатного vpunch, амплитуда
## своя). Вторая серия бьёт сильнее и резче.
define c1s1_knock_punch = Move((0, 12), (0, -12), 0.09, bounce=True, repeat=True, delay=0.26)
define c1s1_knock_punch_hard = Move((0, 20), (0, -20), 0.08, bounce=True, repeat=True, delay=0.24)

define chapter_1_fade_in = Dissolve(2.0)
define chapter_1_dissolve = Dissolve(1.2)

## Трансформы сцены #############################################################

## Рывок за шнурок: короткое резкое движение вниз с остановкой.
transform c1s1_hand_pull(pos_xy, dy=C1S1_PULL_DY, t=C1S1_PULL_T):
    subpixel True
    anchor (0.0, 0.0)
    pos pos_xy
    easein t yoffset dy

## После щелчка: рука по инерции уходит вверх мимо базовой точки и оседает.
## Стартует из нижней точки рывка (yoffset dy) — состояние подхватывается
## визуально, хотя спрайт уже светлый.
transform c1s1_hand_release(pos_xy, dy=C1S1_PULL_DY, over=C1S1_RELEASE_OVER, up_t=C1S1_RELEASE_T, settle_t=C1S1_SETTLE_T):
    subpixel True
    anchor (0.0, 0.0)
    pos pos_xy
    yoffset dy
    easein up_t yoffset -over
    ease settle_t yoffset 0

## Толчок стрелки метронома: короткое движение кисти слева направо и мягкий
## возврат.
transform c1s1_hand_poke(pos_xy, dx=14, t=0.15):
    subpixel True
    anchor (0.0, 0.0)
    pos pos_xy
    easein t xoffset dx
    ease 0.3 xoffset 0

## Кроссфейд позы в движении: уходящая поза продолжает движение и растворяется.
transform c1s1_hand_fade_out(from_xy, to_xy, t=C1S1_HAND_SWAP_T):
    subpixel True
    anchor (0.0, 0.0)
    pos from_xy
    alpha 1.0
    ease t pos to_xy alpha 0.0

## Рука отходит от метронома и уходит из кадра, открывая метроном.
transform c1s1_hand_exit(from_xy, to_xy, t=C1S1_HAND_EXIT_T):
    subpixel True
    anchor (0.0, 0.0)
    pos from_xy
    ease t pos to_xy alpha 0.0

## Стрелка метронома в покое. transform_anchor — вращение вокруг якоря:
## якорь в низу маятника, крепление стрелки.
transform c1s1_arrow_rest(pos_xy=C1S1_ARROW_PIVOT_POS):
    subpixel True
    transform_anchor True
    anchor (0.5, 1.0)
    pos pos_xy
    rotate 0.0

## Качание стрелки вокруг нижнего крепления: разгон от толчка (пальцы толкают
## стрелку слева направо — по часовой, rotate положительный), дальше маятник
## между крайними положениями. Щелчок метронома — на каждом крайнем положении.
## TODO(звук): щелчки метронома (добавим позже).
transform c1s1_arrow_swing(pos_xy=C1S1_ARROW_PIVOT_POS, amp=C1S1_ARROW_AMP, half_t=C1S1_ARROW_HALF_T):
    subpixel True
    transform_anchor True
    anchor (0.5, 1.0)
    pos pos_xy
    rotate 0.0
    easein half_t / 2.0 rotate amp
    block:
        ease half_t rotate -amp
        ease half_t rotate amp
        repeat

## ГГ за пианино: очень слабый объектный параллакс (свой ключ накопителей,
## сильнее фонового — фигура читается ближе) + едва заметное «дыхание»:
## лёгкий наклон корпуса и рост от нижнего якоря. Взаимодействие с
## инструментом, но ещё не игра. transform_anchor обязателен: активный
## rotate расширяет холст спрайта до квадрата со стороной-диагональю
## (rotate_pad), и без него anchor/pos отсчитывались бы от этого квадрата —
## позиционирование уезжает; с ним якорь считается по самой фигуре и
## одновременно служит пивотом поворота и масштаба.
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
        ease 2.7 rotate 0.35 yzoom 1.004
        ease 3.4 rotate -0.3 yzoom 1.0
        repeat

## Руки над клавишами: слабый объектный параллакс (ключ уникален на руку) +
## едва заметное парение над клавишами — руки живут, но ещё не играют.
## Периоды у рук разные (параметры) — движение не синхронно. Дрейф — через
## pos: xoffset/yoffset заняты параллакс-функцией (правило _fx_state).
transform c1s1_piano_hand_idle(pos_xy, key, strength=C1S1_GG_PARALLAX, dy=4, t_up=2.9, t_down=3.6):
    subpixel True
    anchor (0.0, 0.0)
    pos pos_xy
    xoffset 0.0 yoffset 0.0
    parallel:
        function renpy.curry(mouse_parallax_f)(strength, 0.08, 0.0, 0.04, None, key)
    parallel:
        ease t_up pos (pos_xy[0], pos_xy[1] - dy)
        ease t_down pos pos_xy
        repeat

## Сцена ########################################################################

label chapter_1_scene_1:

    $ dismiss_off()

    ## Тёмная комната: фон + абажур, камера сразу живёт — параллакс и
    ## медленный наезд к лампе с метрономом.
    camera at parallax_push(C1S1_LAMP_FOCUS, C1S1_LAMP_Z0, C1S1_LAMP_Z1, C1S1_LAMP_PUSH_T, strength=C1S1_SCENE_PARALLAX)
    scene chapter_1 lamp_dark
    show chapter_1_lampshade dark zorder C1S1_Z_SHADE at placed(C1S1_LAMPSHADE_POS)
    with chapter_1_fade_in

    $ pause(1.0)

    ## Рука входит из-за нижнего левого края и ложится на абажур (поверх него).
    show chapter_1_lamp_hand dark_reach zorder C1S1_Z_HAND_FRONT at slide_in(C1S1_HAND_ENTER_POS, C1S1_HAND_REACH_POS, t=C1S1_HAND_ENTER_T)
    $ pause(C1S1_HAND_ENTER_T)
    $ pause(0.5)

    ## Кисть уходит под абажур, к шнурку выключателя.
    show chapter_1_lamp_hand dark_pull zorder C1S1_Z_HAND_BEHIND at placed(C1S1_HAND_PULL_POS)
    with Dissolve(0.45)
    $ pause(0.4)

    ## Рывок за шнурок вниз...
    show chapter_1_lamp_hand dark_pull at c1s1_hand_pull(C1S1_HAND_PULL_POS)
    $ pause(C1S1_PULL_T)

    ## ...щелчок — свет. Композиция та же, состояние мгновенно светлое;
    ## рука по инерции продолжает движение вверх уже при свете.
    ## Камера не сбрасывается — наезд и параллакс непрерывны.
    ## TODO(звук): splay щелчка выключателя (добавим позже).
    scene chapter_1 lamp_light
    show chapter_1_metronome_arrow zorder C1S1_Z_ARROW at c1s1_arrow_rest()
    show chapter_1_lampshade light zorder C1S1_Z_SHADE at placed(C1S1_LAMPSHADE_POS)
    show chapter_1_lamp_hand light_pull zorder C1S1_Z_HAND_BEHIND at c1s1_hand_release(C1S1_HAND_PULL_POS)
    $ pause(C1S1_RELEASE_T + C1S1_SETTLE_T)
    $ pause(0.5)

    ## Рука движется к метроному, на ходу перетекая во вторую позу:
    ## уходящая поза растворяется, не прекращая движения, новая — проявляется,
    ## продолжая его (второй спрайт под своим именем — позы живут одновременно).
    show chapter_1_lamp_hand light_pull at c1s1_hand_fade_out(C1S1_HAND_PULL_POS, C1S1_HAND_LEAVE_POS)
    show chapter_1_lamp_hand light_metronome as c1s1_hand_metronome zorder C1S1_Z_HAND_FRONT at slide_in(C1S1_HAND_METRONOME_FROM, C1S1_HAND_METRONOME_POS, t=C1S1_HAND_SWAP_T)
    $ pause(C1S1_HAND_SWAP_T)
    hide chapter_1_lamp_hand
    $ pause(0.25)

    ## Толчок слева направо — стрелка идёт вместе с рукой: оба движения
    ## стартуют в один кадр (пальцы уже на стрелке).
    show chapter_1_lamp_hand light_metronome as c1s1_hand_metronome at c1s1_hand_poke(C1S1_HAND_METRONOME_POS)
    show chapter_1_metronome_arrow zorder C1S1_Z_ARROW at c1s1_arrow_swing()
    $ pause(C1S1_HAND_EXIT_DELAY)

    ## Рука отходит и выходит из кадра — в центре внимания остаётся метроном.
    show chapter_1_lamp_hand light_metronome as c1s1_hand_metronome at c1s1_hand_exit(C1S1_HAND_METRONOME_POS, C1S1_HAND_EXIT_POS)
    $ pause(C1S1_HAND_EXIT_T)
    hide c1s1_hand_metronome

    ## Оставшиеся щелчки метронома: всего C1S1_TICKS_BEFORE_PIANO с момента
    ## запуска стрелки (разгон до первого крайнего положения + полукачания),
    ## часть времени уже ушла на уход руки.
    $ pause(C1S1_ARROW_HALF_T / 2.0 + (C1S1_TICKS_BEFORE_PIANO - 1) * C1S1_ARROW_HALF_T - C1S1_HAND_EXIT_DELAY - C1S1_HAND_EXIT_T)

    ## Пианино: камера стартует вплотную к ГГ и плавно отдаляется;
    ## ГГ держится строго по центру экрана.
    camera at parallax_push(C1S1_PIANO_FOCUS, C1S1_PIANO_Z0, C1S1_PIANO_Z_END, C1S1_PIANO_OUT_T, strength=C1S1_SCENE_PARALLAX, screen_align=C1S1_PIANO_SCREEN)
    scene chapter_1 piano
    show chapter_1_piano_gg at c1s1_gg_idle()
    with chapter_1_dissolve

    ## Отдаление не завершается — переход к рукам на середине движения.
    $ pause(C1S1_PIANO_HOLD_T)

    ## Руки над клавишами: камера чуть ближе полного кадра, движение
    ## подхватывает скорость отдаления и затухая завершает его.
    camera at parallax_settle(C1S1_HANDS_FOCUS, C1S1_HANDS_Z0, C1S1_CAM_Z_REST, C1S1_HANDS_T, strength=C1S1_SCENE_PARALLAX)
    scene chapter_1 piano_hands
    show chapter_1_piano_hand_left at c1s1_piano_hand_idle(C1S1_HANDS_LEFT_POS, "hand_l")
    show chapter_1_piano_hand_right at c1s1_piano_hand_idle(C1S1_HANDS_RIGHT_POS, "hand_r", dy=3, t_up=3.3, t_down=2.7)
    with chapter_1_dissolve

    $ pause(C1S1_HANDS_T)

    ## Руки замерли над клавишами — и в тишине раздаётся стук в дверь.
    $ pause(C1S1_KNOCK_HOLD_T)

    ## С первым ударом камера начинает медленно заваливаться набок и тревожно
    ## покачиваться; завал (и доводка зума из C1S1_CAM_Z_REST) растянуты на обе
    ## серии стука. Параллакс при этом гаснет — мир перестаёт слушаться.
    ## TODO(звук): стук в дверь (добавим позже).
    camera at uneasy_sway(C1S1_KNOCK_DRIFT, C1S1_KNOCK_SWAY, speed=C1S1_KNOCK_SWAY_SPEED, zoom_pad=C1S1_KNOCK_PAD, base=C1S1_KNOCK_TILT, base_in_t=C1S1_KNOCK_TILT_T, zoom0=C1S1_CAM_Z_REST)

    ## Первая серия: три удара в разных частях экрана, экран вздрагивает
    ## в такт каждому (punch — блокирующий транзишен, даёт и часть паузы).
    ## С первого же удара замершие руки начинают мелко дрожать; каждый
    ## следующий удар усиливает дрожь на шаг C1S1_HANDS_TREMBLE_STEPS —
    ## show руки идёт до punch, чтобы скачок амплитуды совпал с ударом.
    $ knock_at(C1S1_KNOCK_POSES[0], zoom=0.9)
    show chapter_1_piano_hand_left at placed_jitter(C1S1_HANDS_LEFT_POS, jitter_amp=C1S1_HANDS_TREMBLE_STEPS[0], jitter_key="c1s1_hand_l")
    show chapter_1_piano_hand_right at placed_jitter(C1S1_HANDS_RIGHT_POS, jitter_amp=C1S1_HANDS_TREMBLE_STEPS[0], jitter_key="c1s1_hand_r")
    with c1s1_knock_punch
    $ pause(C1S1_KNOCK_GAP_T)
    $ knock_at(C1S1_KNOCK_POSES[1])
    show chapter_1_piano_hand_left at placed_jitter(C1S1_HANDS_LEFT_POS, jitter_amp=C1S1_HANDS_TREMBLE_STEPS[1], jitter_key="c1s1_hand_l")
    show chapter_1_piano_hand_right at placed_jitter(C1S1_HANDS_RIGHT_POS, jitter_amp=C1S1_HANDS_TREMBLE_STEPS[1], jitter_key="c1s1_hand_r")
    with c1s1_knock_punch
    $ pause(C1S1_KNOCK_GAP_T)
    $ knock_at(C1S1_KNOCK_POSES[2], zoom=1.1)
    show chapter_1_piano_hand_left at placed_jitter(C1S1_HANDS_LEFT_POS, jitter_amp=C1S1_HANDS_TREMBLE_STEPS[2], jitter_key="c1s1_hand_l")
    show chapter_1_piano_hand_right at placed_jitter(C1S1_HANDS_RIGHT_POS, jitter_amp=C1S1_HANDS_TREMBLE_STEPS[2], jitter_key="c1s1_hand_r")
    with c1s1_knock_punch

    ## Тишина. Стук не повторяется — только руки продолжают дрожать.
    $ pause(C1S1_KNOCK_SERIES_GAP_T)

    ## Вторая серия: три удара громче и настойчивее — кольца крупнее, паузы
    ## короче, тряска сильнее; точки снова новые, дрожь рук доходит до предела.
    $ knock_at(C1S1_KNOCK_POSES[3], zoom=1.3)
    show chapter_1_piano_hand_left at placed_jitter(C1S1_HANDS_LEFT_POS, jitter_amp=C1S1_HANDS_TREMBLE_STEPS[3], jitter_key="c1s1_hand_l")
    show chapter_1_piano_hand_right at placed_jitter(C1S1_HANDS_RIGHT_POS, jitter_amp=C1S1_HANDS_TREMBLE_STEPS[3], jitter_key="c1s1_hand_r")
    with c1s1_knock_punch_hard
    $ pause(C1S1_KNOCK_GAP2_T)
    $ knock_at(C1S1_KNOCK_POSES[4], zoom=1.45)
    show chapter_1_piano_hand_left at placed_jitter(C1S1_HANDS_LEFT_POS, jitter_amp=C1S1_HANDS_TREMBLE_STEPS[4], jitter_key="c1s1_hand_l")
    show chapter_1_piano_hand_right at placed_jitter(C1S1_HANDS_RIGHT_POS, jitter_amp=C1S1_HANDS_TREMBLE_STEPS[4], jitter_key="c1s1_hand_r")
    with c1s1_knock_punch_hard
    $ pause(C1S1_KNOCK_GAP2_T)
    $ knock_at(C1S1_KNOCK_POSES[5], zoom=1.6)
    show chapter_1_piano_hand_left at placed_jitter(C1S1_HANDS_LEFT_POS, jitter_amp=C1S1_HANDS_TREMBLE_STEPS[5], jitter_key="c1s1_hand_l")
    show chapter_1_piano_hand_right at placed_jitter(C1S1_HANDS_RIGHT_POS, jitter_amp=C1S1_HANDS_TREMBLE_STEPS[5], jitter_key="c1s1_hand_r")
    with c1s1_knock_punch_hard

    ## Камера доваливается до предельного угла; сцена замирает в наклонном
    ## тревожном покачивании над дрожащими руками.
    $ pause(2.0)
    $ knock_clear()

    $ dismiss_on()

    ## Продолжение (реакция ГГ на стук) — следующим шагом.
    return
