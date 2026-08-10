################################################################################
## Глава 1 — сцена 1: тёмная комната → рука включает лампу (мгновенный переход
## в светлое состояние) → запуск метронома → пианино (отдаление от ГГ) → руки
## над клавишами → стук в дверь → холл → дверь крупным планом (со стороны
## подъезда) → та же дверь изнутри, замки. Каждый переход в цепочке стука
## склеен с ударом. Чистая кат-сцена без реплик, управление игроку недоступно.
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

## Холл: фон и слои-предметы (композиция сверена с hall_all.png попиксельно,
## позиции — из bbox слоёв PSD Ch_1_Hall).
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

## Дверь крупным планом: фон + рука (замах/удар), позиции — из bbox PSD
## Ch_1_Door knock.
image chapter_1 door = "images/1_chapter/chapter_1 door.jpg"
image chapter_1_door_hand wind = "images/1_chapter/chapter_1_door_hand wind.png"
image chapter_1_door_hand hit = "images/1_chapter/chapter_1_door_hand hit.png"

## Та же дверь изнутри квартиры: замки крупным планом (PSD Ch_1_Door _locks).
## Внимание: `chapter_1 hall_door` (кадр сцены) и `chapter_1_hall_door` выше
## (створка двери в холле) — разные образы, имена похожи из-за имён ассетов.
image chapter_1 hall_door = "images/1_chapter/chapter_1 hall_door.jpg"
image chapter_1_hall_door_bag = "images/1_chapter/chapter_1_hall_door_bag.png"

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

## Интерактив: две кнопки подряд, лампа и только потом метроном. Координаты
## мировые (кнопки едут с камерой, см. экраны ниже), центры — на самих
## предметах: у лампы между корпусом и основанием, у метронома на корпусе.
## Пятно тёмного варианта здесь не годится — обе сцены тёмные, нужен bg="dark".
define C1S1_LAMP_BTN_POS = (500, 700)
define C1S1_LAMP_BTN_SIZE = (330, 165)
## Подпись длиннее — пятно шире, иначе текст выходит за плотное ядро.
define C1S1_METRONOME_BTN_POS = (1025, 560)
define C1S1_METRONOME_BTN_SIZE = (430, 190)

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

## Стук в дверь (визуализация звука — flash_fx, common/flash_fx.rpy).
## Звук бьёт отовсюду: на каждый удар весь экран коротко вспыхивает и
## вздрагивает в такт (punch-транзишены). Две серии по три удара с паузой.
## Камера с первым ударом начинает заваливаться набок (uneasy_sway с base):
## завал тянется через обе серии — тревога нарастает всю концовку сцены.
## Пик вспышки растёт от удара к удару (доли белого): серия 1 — [0..2],
## серия 2 — [3..5], стук всё настойчивее.
define C1S1_KNOCK_FLASH_PEAKS = (0.18, 0.22, 0.26, 0.34, 0.40, 0.48)
define C1S1_KNOCK_FLASH_FALL_T = 0.22   # спад вспышки, сек
define C1S1_KNOCK_FLASH_FALL2_T = 0.16  # вторая серия — гаснет резче
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

## Холл: размещение слоёв (px, из bbox PSD Ch_1_Hall). Имена зонтов в PSD
## и в ассетах расходятся (зонт_2 ↔ umbrella_1) — сверено по размерам.
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

## Порядок слоёв холла: внутри групп предметы перекрываются по возрастанию
## (номера групп — из имён исходных ассетов 0_*…4_*), швабра поверх всех.
define C1S1_Z_HALL_DOOR = 3
define C1S1_Z_HALL_GROUP_0 = 10   # тумба справа: сапоги < пакет < игрушка
define C1S1_Z_HALL_GROUP_1 = 20   # комод слева: бумаги < сумка < бутылки
define C1S1_Z_HALL_GROUP_2 = 30   # зонты у комода
define C1S1_Z_HALL_MIRROR = 35
define C1S1_Z_HALL_MOP = 40

## Стук в холле: те же вспышки (flash_fx), но слабее — звук тот же, а слушают
## его уже из прихожей. Три удара; на каждый предметы у стен мелко дрожат
## и экран едва вздрагивает.
define C1S1_HALL_KNOCK_FLASH = 0.16      # пик вспышки, доля белого
define C1S1_HALL_KNOCK_FLASH_FALL_T = 0.3  # спад мягче, чем у пианино
define C1S1_HALL_KNOCK_HOLD_T = 1.0  # тишина после появления холла до стука
define C1S1_HALL_KNOCK_GAP_T = 0.45  # пауза между ударами
define C1S1_HALL_OBJ_TREMBLE = 2.0   # амплитуда дрожи предметов, px (несильно)

## Мягкое вздрагивание экрана на удар (тише, чем у пианино).
define c1s1_hall_knock_punch = Move((0, 6), (0, -6), 0.09, bounce=True, repeat=True, delay=0.22)

## Дверь крупным планом. На третьем ударе резкий (без перехода) переход сюда,
## склеенный с моментом удара руки. Позиции руки — из bbox PSD Ch_1_Door knock:
## замах — кулак у двери, удар — кулак отведён вправо.
define C1S1_DOOR_HAND_WIND_POS = (769, 131)
define C1S1_DOOR_HAND_HIT_POS = (1158, 147)
define C1S1_HALL_CUT_T = 0.08        # ринг-удар мигает и сразу рез — «резко»
define C1S1_DOOR_OPEN_HOLD_T = 0.6   # пауза после перехода до повторных ударов
define C1S1_DOOR_WIND_T = 0.28       # замах держится перед ударом
define C1S1_DOOR_KNOCK_GAP_T = 0.5   # пауза между ударами в дверь
define C1S1_DOOR_CUT_T = 0.08        # третий удар мигает и сразу рез — как в холле

## Вздрагивание экрана на удар в дверь крупным планом (тверже холла).
define c1s1_door_hit_punch = Move((0, 14), (0, -14), 0.08, bounce=True, repeat=True, delay=0.24)

## Замки: та же дверь, но изнутри квартиры. Третий удар крупного плана
## склеивается с этим кадром ровно тем же приёмом, что холл → дверь: вспышка
## уходит в рез и досвечивает уже новый кадр, поэтому первый из трёх ударов
## здесь — сам момент склейки, дальше добивают ещё два. После короткой тишины
## стук возвращается ещё двумя ударами — громче и настойчивее.
##
## Сумка у стены: слой PSD обрезан по холсту (у PNG плоские срезы по левому и
## нижнему краям), поэтому её нижний левый угол совпадает с нижним левым углом
## кадра — размер спрайта знать не нужно, якорь ставим в (0.0, 1.0).
define C1S1_DOOR_BAG_POS = (0, 1080)
define C1S1_DOOR_BAG_ANCHOR = (0.0, 1.0)
define C1S1_Z_DOOR_BAG = 5

## Камера успокаивается после тревожного завала: спокойный параллакс и
## медленный наезд на связку замков (шпингалет + сувальдный + ручка).
## Старт с зума покоя — на резе кадр не дёргается, наезд длиннее сцены.
define C1S1_LOCKS_FOCUS = (0.50, 0.32)
define C1S1_LOCKS_Z1 = 1.16
define C1S1_LOCKS_PUSH_T = 22.0

## Стук слышен вплотную за дверью — вспышки ярче холла и растут от удара
## к удару; экран вздрагивает твёрже, сумка у стены мелко трясётся.
## Индексы [0..2] — первая серия (три удара), [3..4] — вторая (два добора):
## она бьёт ярче, гаснет резче и паузу держит короче.
define C1S1_LOCKS_FLASH_PEAKS = (0.22, 0.26, 0.30, 0.38, 0.44)
define C1S1_LOCKS_FLASH_FALL_T = 0.22
define C1S1_LOCKS_FLASH_FALL2_T = 0.16
define C1S1_LOCKS_KNOCK_GAP_T = 0.5
define C1S1_LOCKS_KNOCK_GAP2_T = 0.34
define C1S1_LOCKS_SERIES_GAP_T = 1.4  # тишина между сериями
define C1S1_LOCKS_BAG_TREMBLE = (2.0, 2.6, 3.2, 4.0, 4.8)  # дрожь сумки, px
define C1S1_LOCKS_BAG_CALM = 0.8     # остаточное подрагивание в тишине
define C1S1_LOCKS_SETTLE_T = 1.6     # шаг затухания дрожи после последнего удара
define C1S1_LOCKS_HOLD_T = 2.5       # кадр держится в тишине

define c1s1_locks_knock_punch = Move((0, 16), (0, -16), 0.08, bounce=True, repeat=True, delay=0.26)
define c1s1_locks_knock_punch_hard = Move((0, 22), (0, -22), 0.08, bounce=True, repeat=True, delay=0.24)

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

## Экраны интерактива ###########################################################

## Обе кнопки лежат в мире, а не приклеены к экрану: внешний контейнер во весь
## кадр повторяет параллакс и наезд камеры (follow_camera читает готовые
## накопители ключа "cam"), поэтому позиции — мировые координаты, и пятно
## держится за предметом, пока камера едет. Как в прологе.
screen c1s1_lamp_switch():
    modal True
    fixed:
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
    fixed:
        at follow_camera()
        xysize (config.screen_width, config.screen_height)
        use glow_button(
            _("Завести метроном"),
            Return("done"),
            bg="dark",
            pos=C1S1_METRONOME_BTN_POS,
            size=C1S1_METRONOME_BTN_SIZE)

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

    ## Первый шаг игрока: зажечь лампу. Развилки сюжета нет и состояние игры не
    ## меняется — при пропуске (Ctrl/«Пропуск») экран не зовём, сцена проходится
    ## насквозь (правило .claude/rules/skippable-scenes.md).
    if not renpy.is_skipping():
        call screen c1s1_lamp_switch

    ## Ответ на клик: рука входит из-за нижнего левого края и ложится на абажур
    ## (поверх него).
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

    ## Второй шаг: метроном. Кнопка появляется только теперь — рука всё это
    ## время ждёт у шнурка, порядок действий задан жёстко.
    if not renpy.is_skipping():
        call screen c1s1_metronome_start

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

    ## Первая серия: три удара, на каждый экран вспыхивает и вздрагивает
    ## (punch — блокирующий транзишен, даёт и часть паузы; вспышка идёт
    ## параллельно ему и сценарий не держит).
    ## С первого же удара замершие руки начинают мелко дрожать; каждый
    ## следующий удар усиливает дрожь на шаг C1S1_HANDS_TREMBLE_STEPS —
    ## show руки идёт до punch, чтобы скачок амплитуды совпал с ударом.
    $ flash_fx(high=C1S1_KNOCK_FLASH_PEAKS[0], fall=C1S1_KNOCK_FLASH_FALL_T)
    show chapter_1_piano_hand_left at placed_jitter(C1S1_HANDS_LEFT_POS, jitter_amp=C1S1_HANDS_TREMBLE_STEPS[0], jitter_key="c1s1_hand_l")
    show chapter_1_piano_hand_right at placed_jitter(C1S1_HANDS_RIGHT_POS, jitter_amp=C1S1_HANDS_TREMBLE_STEPS[0], jitter_key="c1s1_hand_r")
    with c1s1_knock_punch
    $ pause(C1S1_KNOCK_GAP_T)
    $ flash_fx(high=C1S1_KNOCK_FLASH_PEAKS[1], fall=C1S1_KNOCK_FLASH_FALL_T)
    show chapter_1_piano_hand_left at placed_jitter(C1S1_HANDS_LEFT_POS, jitter_amp=C1S1_HANDS_TREMBLE_STEPS[1], jitter_key="c1s1_hand_l")
    show chapter_1_piano_hand_right at placed_jitter(C1S1_HANDS_RIGHT_POS, jitter_amp=C1S1_HANDS_TREMBLE_STEPS[1], jitter_key="c1s1_hand_r")
    with c1s1_knock_punch
    $ pause(C1S1_KNOCK_GAP_T)
    $ flash_fx(high=C1S1_KNOCK_FLASH_PEAKS[2], fall=C1S1_KNOCK_FLASH_FALL_T)
    show chapter_1_piano_hand_left at placed_jitter(C1S1_HANDS_LEFT_POS, jitter_amp=C1S1_HANDS_TREMBLE_STEPS[2], jitter_key="c1s1_hand_l")
    show chapter_1_piano_hand_right at placed_jitter(C1S1_HANDS_RIGHT_POS, jitter_amp=C1S1_HANDS_TREMBLE_STEPS[2], jitter_key="c1s1_hand_r")
    with c1s1_knock_punch

    ## Тишина. Стук не повторяется — только руки продолжают дрожать.
    $ pause(C1S1_KNOCK_SERIES_GAP_T)

    ## Вторая серия: три удара громче и настойчивее — вспышки ярче и резче,
    ## паузы короче, тряска сильнее; дрожь рук доходит до предела.
    $ flash_fx(high=C1S1_KNOCK_FLASH_PEAKS[3], fall=C1S1_KNOCK_FLASH_FALL2_T)
    show chapter_1_piano_hand_left at placed_jitter(C1S1_HANDS_LEFT_POS, jitter_amp=C1S1_HANDS_TREMBLE_STEPS[3], jitter_key="c1s1_hand_l")
    show chapter_1_piano_hand_right at placed_jitter(C1S1_HANDS_RIGHT_POS, jitter_amp=C1S1_HANDS_TREMBLE_STEPS[3], jitter_key="c1s1_hand_r")
    with c1s1_knock_punch_hard
    $ pause(C1S1_KNOCK_GAP2_T)
    $ flash_fx(high=C1S1_KNOCK_FLASH_PEAKS[4], fall=C1S1_KNOCK_FLASH_FALL2_T)
    show chapter_1_piano_hand_left at placed_jitter(C1S1_HANDS_LEFT_POS, jitter_amp=C1S1_HANDS_TREMBLE_STEPS[4], jitter_key="c1s1_hand_l")
    show chapter_1_piano_hand_right at placed_jitter(C1S1_HANDS_RIGHT_POS, jitter_amp=C1S1_HANDS_TREMBLE_STEPS[4], jitter_key="c1s1_hand_r")
    with c1s1_knock_punch_hard
    $ pause(C1S1_KNOCK_GAP2_T)
    $ flash_fx(high=C1S1_KNOCK_FLASH_PEAKS[5], fall=C1S1_KNOCK_FLASH_FALL2_T)
    show chapter_1_piano_hand_left at placed_jitter(C1S1_HANDS_LEFT_POS, jitter_amp=C1S1_HANDS_TREMBLE_STEPS[5], jitter_key="c1s1_hand_l")
    show chapter_1_piano_hand_right at placed_jitter(C1S1_HANDS_RIGHT_POS, jitter_amp=C1S1_HANDS_TREMBLE_STEPS[5], jitter_key="c1s1_hand_r")
    with c1s1_knock_punch_hard

    ## Камера доваливается до предельного угла; сцена замирает в наклонном
    ## тревожном покачивании над дрожащими руками.
    $ pause(2.0)

    ## Холл: простая смена сцены (эффектный переход — отдельной задачей).
    ## Камера сбрасывается к спокойному параллаксу.
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

    ## Тишина — и стук настигает уже здесь, в прихожей. Экран вспыхивает
    ## слабее, чем у пианино, предметы у стен начинают мелко дрожать —
    ## реагируют на удары.
    $ pause(C1S1_HALL_KNOCK_HOLD_T)
    show chapter_1_hall_mop zorder C1S1_Z_HALL_MOP at placed_jitter(C1S1_HALL_MOP_POS, jitter_amp=C1S1_HALL_OBJ_TREMBLE, jitter_key="hall_mop")
    show chapter_1_hall_umbrella_1 zorder C1S1_Z_HALL_GROUP_2 at placed_jitter(C1S1_HALL_UMBRELLA_1_POS, jitter_amp=C1S1_HALL_OBJ_TREMBLE, jitter_key="hall_umb1")
    show chapter_1_hall_umbrella_2 zorder C1S1_Z_HALL_GROUP_2 + 1 at placed_jitter(C1S1_HALL_UMBRELLA_2_POS, jitter_amp=C1S1_HALL_OBJ_TREMBLE, jitter_key="hall_umb2")
    show chapter_1_hall_bottles zorder C1S1_Z_HALL_GROUP_1 + 2 at placed_jitter(C1S1_HALL_BOTTLES_POS, jitter_amp=C1S1_HALL_OBJ_TREMBLE, jitter_key="hall_bottles")

    ## Три удара.
    ## TODO(звук): стук в дверь (добавим позже).
    $ flash_fx(high=C1S1_HALL_KNOCK_FLASH, fall=C1S1_HALL_KNOCK_FLASH_FALL_T)
    with c1s1_hall_knock_punch
    $ pause(C1S1_HALL_KNOCK_GAP_T)
    $ flash_fx(high=C1S1_HALL_KNOCK_FLASH, fall=C1S1_HALL_KNOCK_FLASH_FALL_T)
    with c1s1_hall_knock_punch
    $ pause(C1S1_HALL_KNOCK_GAP_T)

    ## Третий удар — экран вспыхивает, и на этом же ударе резкий переход:
    ## кадр склеивается с моментом удара рукой (дверь крупным планом).
    $ flash_fx(high=C1S1_HALL_KNOCK_FLASH, fall=C1S1_HALL_KNOCK_FLASH_FALL_T)
    with c1s1_hall_knock_punch
    $ pause(C1S1_HALL_CUT_T)

    ## Резкая смена сцены (без перехода): дверь крупным планом, кулак уже
    ## в позе удара — синхронно с третьим стуком, первый из трёх ударов
    ## (scene очищает слой, предметы холла гасятся сами; вспышка живёт на
    ## своём always_shown-экране и досветит поверх нового кадра).
    scene chapter_1 door
    show chapter_1_door_hand hit at placed(C1S1_DOOR_HAND_HIT_POS)
    with c1s1_door_hit_punch

    ## Небольшая пауза — и рука добивает ещё два раза: замах → удар.
    ## TODO(звук): стук в дверь крупным планом (добавим позже).
    $ pause(C1S1_DOOR_OPEN_HOLD_T)
    show chapter_1_door_hand wind at placed(C1S1_DOOR_HAND_WIND_POS)
    $ pause(C1S1_DOOR_WIND_T)
    show chapter_1_door_hand hit at placed(C1S1_DOOR_HAND_HIT_POS)
    with c1s1_door_hit_punch

    ## Третий удар — и на нём же рез: вспышка уходит вперёд кадра и досветит
    ## уже дверь изнутри, тот же удар слышен теперь из квартиры.
    $ pause(C1S1_DOOR_KNOCK_GAP_T)
    show chapter_1_door_hand wind at placed(C1S1_DOOR_HAND_WIND_POS)
    $ pause(C1S1_DOOR_WIND_T)
    $ flash_fx(high=C1S1_LOCKS_FLASH_PEAKS[0], fall=C1S1_LOCKS_FLASH_FALL_T)
    show chapter_1_door_hand hit at placed(C1S1_DOOR_HAND_HIT_POS)
    with c1s1_door_hit_punch
    $ pause(C1S1_DOOR_CUT_T)

    ## Дверь изнутри: замки крупным планом, у стены — сумка. Камера сбрасывает
    ## завал и покачивание, дальше только спокойный параллакс и медленный
    ## наезд на замки. Дрожь сумки включается с этим же ударом.
    ## TODO(звук): стук в дверь изнутри квартиры (добавим позже).
    camera at parallax_push(C1S1_LOCKS_FOCUS, C1S1_CAM_Z_REST, C1S1_LOCKS_Z1, C1S1_LOCKS_PUSH_T, strength=C1S1_SCENE_PARALLAX)
    scene chapter_1 hall_door
    show chapter_1_hall_door_bag zorder C1S1_Z_DOOR_BAG at placed_jitter(C1S1_DOOR_BAG_POS, anchor_xy=C1S1_DOOR_BAG_ANCHOR, jitter_amp=C1S1_LOCKS_BAG_TREMBLE[0], jitter_key="c1s1_door_bag")
    with c1s1_locks_knock_punch

    ## Ещё два удара: экран вспыхивает и вздрагивает, сумка трясётся сильнее.
    ## show сумки идёт до punch — скачок амплитуды совпадает с ударом.
    $ pause(C1S1_LOCKS_KNOCK_GAP_T)
    $ flash_fx(high=C1S1_LOCKS_FLASH_PEAKS[1], fall=C1S1_LOCKS_FLASH_FALL_T)
    show chapter_1_hall_door_bag zorder C1S1_Z_DOOR_BAG at placed_jitter(C1S1_DOOR_BAG_POS, anchor_xy=C1S1_DOOR_BAG_ANCHOR, jitter_amp=C1S1_LOCKS_BAG_TREMBLE[1], jitter_key="c1s1_door_bag")
    with c1s1_locks_knock_punch
    $ pause(C1S1_LOCKS_KNOCK_GAP_T)
    $ flash_fx(high=C1S1_LOCKS_FLASH_PEAKS[2], fall=C1S1_LOCKS_FLASH_FALL_T)
    show chapter_1_hall_door_bag zorder C1S1_Z_DOOR_BAG at placed_jitter(C1S1_DOOR_BAG_POS, anchor_xy=C1S1_DOOR_BAG_ANCHOR, jitter_amp=C1S1_LOCKS_BAG_TREMBLE[2], jitter_key="c1s1_door_bag")
    with c1s1_locks_knock_punch

    ## Короткая тишина: кажется, что всё кончилось — сумка почти замирает.
    ## Тем же ключом дрожь затухает без рывка (накопитель живёт между show).
    $ pause(C1S1_LOCKS_SETTLE_T)
    show chapter_1_hall_door_bag zorder C1S1_Z_DOOR_BAG at placed_jitter(C1S1_DOOR_BAG_POS, anchor_xy=C1S1_DOOR_BAG_ANCHOR, jitter_amp=C1S1_LOCKS_BAG_CALM, jitter_key="c1s1_door_bag")
    $ pause(C1S1_LOCKS_SERIES_GAP_T)

    ## ...и стук возвращается: ещё два удара, громче и настойчивее — вспышки
    ## ярче и резче, пауза короче, экран вздрагивает сильнее.
    $ flash_fx(high=C1S1_LOCKS_FLASH_PEAKS[3], fall=C1S1_LOCKS_FLASH_FALL2_T)
    show chapter_1_hall_door_bag zorder C1S1_Z_DOOR_BAG at placed_jitter(C1S1_DOOR_BAG_POS, anchor_xy=C1S1_DOOR_BAG_ANCHOR, jitter_amp=C1S1_LOCKS_BAG_TREMBLE[3], jitter_key="c1s1_door_bag")
    with c1s1_locks_knock_punch_hard
    $ pause(C1S1_LOCKS_KNOCK_GAP2_T)
    $ flash_fx(high=C1S1_LOCKS_FLASH_PEAKS[4], fall=C1S1_LOCKS_FLASH_FALL2_T)
    show chapter_1_hall_door_bag zorder C1S1_Z_DOOR_BAG at placed_jitter(C1S1_DOOR_BAG_POS, anchor_xy=C1S1_DOOR_BAG_ANCHOR, jitter_amp=C1S1_LOCKS_BAG_TREMBLE[4], jitter_key="c1s1_door_bag")
    with c1s1_locks_knock_punch_hard

    ## Теперь уже насовсем: стук не повторяется, сумка подрагивает и замирает.
    $ pause(C1S1_LOCKS_SETTLE_T)
    show chapter_1_hall_door_bag zorder C1S1_Z_DOOR_BAG at placed_jitter(C1S1_DOOR_BAG_POS, anchor_xy=C1S1_DOOR_BAG_ANCHOR, jitter_amp=C1S1_LOCKS_BAG_CALM, jitter_key="c1s1_door_bag")
    $ pause(C1S1_LOCKS_SETTLE_T)
    show chapter_1_hall_door_bag zorder C1S1_Z_DOOR_BAG at placed_jitter(C1S1_DOOR_BAG_POS, anchor_xy=C1S1_DOOR_BAG_ANCHOR, jitter_amp=0.0, jitter_key="c1s1_door_bag")
    $ pause(C1S1_LOCKS_HOLD_T)

    ## Дальше — мини-игра с замками (chapter_1_scene_1_minigame_locks.rpy):
    ## камера встаёт в кадр мини-игры, стук идёт без перерыва, над замками
    ## загорается кнопка «Открыть дверь».
    call chapter_1_scene_1_minigame_locks from _call_c1s1_minigame_locks

    $ dismiss_on()

    ## Временная выдержка для отладки (дальше пока ничего нет).
    $ pause(30)

    ## Продолжение сцены за отпертой дверью — следующим шагом.
    return
