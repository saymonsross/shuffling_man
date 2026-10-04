# Звуки сцены 1 главы 1

Файлы кладутся **сюда**: `game/audio/sfx/c1s1/`.
Формат: **OGG Vorbis**, 48 kHz, стерео или моно, q5–q6, пик ≈ −3 dBFS,
без «подушки» тишины в начале (атака в первых ~5 мс — иначе удар разойдётся
со вспышкой). Громкость выставляется кодом, поэтому все варианты одного
звука сводятся к одной громкости.

Имена в коде задаются константами (`C1S1_*_SOUND` / `*_SOUNDS`); путь
внутри `audio/sfx` пишется без расширения.

| Файл | Длит. | Что это | Где вызывается |
|---|---|---|---|
| `../metronome_1.ogg`, `../metronome_2.ogg` | 0.74 с | «тик» и «ток» метронома (`game/audio/sfx/`) | источники для `metronome_loop.wav` |
| `metronome_loop.wav` | 1.412 с | два такта, 85 BPM — темп мелодии пианино: «тик» на половине первой доли, «ток» — второй | непрерывно от запуска стрелки до открытия двери; такт мини-игры пианино |
| `lamp_switch.ogg` | 0.1–0.2 с | щелчок клавиши выключателя лампы | момент включения света |
| `knock_far_1.ogg`<br>`knock_far_2.ogg`<br>`knock_far_3.ogg` | 0.4–0.8 с | глухой стук через стену/квартиру, приглушённые верха | 6 ударов у пианино (2 серии по 3) |
| `knock_hall_1.ogg`<br>`knock_hall_2.ogg`<br>`knock_hall_3.ogg` | 0.4–0.8 с | тот же стук, слышимый из прихожей: ближе, чуть больше тела | 3 удара в холле |
| `knock_door_1.ogg`<br>`knock_door_2.ogg` | 2.1 / 2.25 с | серия из шести ударов кулаком по двери; моменты ударов (`C1S1_MG_KNOCKS`, `c1s1_knocks_1/2`) измерены по огибающей | стук А / стук Б в сцене и весь стук мини-игры замков (серия выбирается случайно) |
| `lock_grab.ogg` | 0.54 с | лёгкий щелчок-тап: пальцы зацепили деталь (из `../ESM_HDLM_fx_foley_tool_saw_cover_open_small_gentle_tap_click_light_01_1x140bpm.wav`, пик −3 dBFS) | не используется: зацеп и отпускание деталей — общий `../click.ogg` вполголоса (`C1S1_MG_GRAB_*`) |
| `shekolda_slide.ogg` | 16.4 с | скольжение металла по металлу, петля | пока тащат щеколду, нижнюю щеколду большого замка и крутят его вертушку; громкость по скорости хода (`C1S1_*_SLIDE_*`) |
| `latch_open.ogg` | 0.7 с | щеколда отошла: деревянно-металлический поворот рычага (из Splice `ESM_Empire_Game_Chest_Lockbox_Lock_Unlock_Handling_Open_Turn_Lever_3_Wooden.wav`) | ушко щеколды доведено до конца, первый замок открыт (`C1S1_LATCH_OPEN_SOUND`) |
| `shekolda_open.ogg` | 1.7 с | прежний лязг щеколды | не используется |
| `2_lock_declaine.ogg` | 1.7 с | отказ вертушки: глухой клац запертого механизма | клик по вертушке большого замка, пока нижняя щеколда не сдвинута |
| `big_lock_latch_open.ogg` | — | защёлка отошла: щелчок засова сундука (из Splice `ESM_Empire_Game_Chest_Open_Treasure_Loot_Lock_Unlock_2_Latch_Only.wav`) | нижняя щеколда большого замка дошла до упора (`C1S1_BIG_LATCH_OPEN_SOUND`) |
| `2_lock_step_1_open.ogg` | — | прежний щелчок механизма большого замка | не используется |
| `big_lock_open.ogg` | 0.3 с | лязг механизма: ригель большого замка отошёл (из Splice `ESM_Ancient_Game_Metal_Lock_Close_Gear_Open_Slide_Texture.wav`) | вертушка провёрнута до конца, второй замок открыт (`C1S1_BIG_LOCK_SOUND`) |
| `handle_squeak.ogg` | 0.8 с, петля | скрип ручки под нажимом (из Splice `ESM_HDGM_Cinematic_FX_squeak_thin_package_handling_stress_04.wav`, хвост тишины обрезан) | пока ручку третьего замка тянут вниз; громкость по скорости (`C1S1_HANDLE_SLIDE_*`) |
| `handle_open.ogg` | — | щелчок язычка дверной ручки | ручка довёрнута, третий замок открыт (`C1S1_HANDLE_SOUND`) |
| `c1s1_door_lock_oppen.ogg` | 3.4 с | дверь отперта | все три замка открыты, мини-игра пройдена (`C1S1_MG_DOOR_OPEN_SOUND`) |
| `c1s1_tv_remote_click.ogg` | 0.04 с | щелчок кнопки пульта (Splice `MO_YFBOB_perc_idm_click.wav`) | телевизор: нажатие на пульт днём (включение) и ночью (переключение канала) |
| `tv_news_malchik_lost.ogg` | 11.6 с | ведущая новостей: сводка о пропавшем мальчике (речь 0.4–9.5 с) | днём: один раз при включении телевизора, панорама 0.1 вправо |
| `c1s1_tv_hiss.ogg` | 10.8 с | тихое шипение включившегося кинескопа (`quiet-with-a-bit-of-hiss55.mp3`); исходник на 32 дБ тише, громкость в коде возвращает его уровень | днём: один раз при включении телевизора на новостях |
| `c1s1_hall_clothes_drop.ogg` | 0.52 с | шорох одежды, брошенной на комод (Splice `ESM_Battle_Game_Collect_Item_Inventory_Drop_Stock_Item_Cloth_Swipe_Whoosh_Rustle_1_One_Shot.wav`) | холл без Вити: появление кадра с вещами |
| `tv_turn_on.ogg` | 2.9 с | включение кинескопного телевизора: щелчок и разгорание | днём: экран разгорается после нажатия на пульт |
| `c1s1_konan_tv.ogg` | 43 с | «Конан-варвар» из телевизора, петля | ночь у телевизора: с переключения канала до затемнения в конце сцены, панорама 0.1 вправо |
| `c1s1_footbal_tv.ogg` | 55 с | трансляция футбола из телевизора, петля | ночь у телевизора: с перехода в ночь до переключения канала на «Конана», панорама 0.1 вправо |
| `c1s1_cleanup_hover.ogg` | 0.10 с | тонкий металлический тап (Splice `ESM_FX_ui_metal_tap_hover_over_indicate_thin_metal_03.wav`) | уборка: наведение на предмет, громкость `C1S1_CLEANUP_HOVER_VOLUME` |
| `c1s1_cleanup_blanket.ogg` | 0.42 с | ткань: плед сдёрнули с дивана (Splice `ESM_Explainer_Video_One_Shot_Foley_Cloth_Backpack_Gear_Bag_Grab_Pick_Up_3.wav`) | уборка: взят плед |
| `c1s1_cleanup_back_clothes.ogg` | 1.07 с | ткань: ворох одежды (Splice `ESM_Battle_Game_Bag_Foley_Cloth_Grab_Body_Equipment_Satchel_Crafting_1_One_Shot.wav`) | уборка: одежда со спинки дивана |
| `c1s1_cleanup_arm_clothes.ogg` | 1.02 с | ткань: тот же ворох одежды, что у спинки дивана, на 5% выше (Splice `ESM_Battle_Game_Bag_Foley_Cloth_Grab_Body_Equipment_Satchel_Crafting_1_One_Shot.wav`) | уборка: рубашка на подлокотнике |
| `c1s1_cleanup_stool_clothes.ogg` | 0.24 с | ткань: короткий хват (Splice `ClothGrab_SFXB.824.wav`) | уборка: одежда с табурета у пианино |
| `c1s1_cleanup_pillow_back_clothes.ogg`<br>`c1s1_cleanup_pillow_arm_clothes.ogg`<br>`c1s1_cleanup_pillow_stool_clothes.ogg` | 1.15 / 1.10 / 0.26 с | звуки одежды со спинки, с подлокотника и с табурета, на 7% ниже | уборка: подушка с пола — тот из трёх, что не звучал на двух предыдущих предметах |
| `c1s1_cleanup_juice.ogg` | 0.19 с | пакет сока (Splice `ClothGrab_SFXB.825.wav`) | уборка: пакет сока |
| `c1s1_cleanup_album.ogg` | 0.63 с | бумага с шорохом: раскраски и карандаши (Splice `ESM_Battle_Game_Grab_Foley_Paper_Item_Pick_Up_Rustle_Crackle_2_Slide_Quick_One_Shot.wav`) | уборка: альбом и карандаши |
| `c1s1_cleanup_wrapper.ogg` | 0.65 с | хрустящая пачка чипсов (Splice `ESM_HDS2_Cinematic_FX_plastic_bag_crinkle_squeeze_handling_34.wav`) | уборка: упаковка на пианино |
| `c1s1_cleanup_pizza.ogg` | 0.24 с | картонная коробка (Splice `CardboardBoxGrab_S011FO.118.wav`) | уборка: коробка пиццы |
| `c1s1_cleanup_mug.ogg` | 0.48 с | кружку подняли с деревянной поверхности (Splice `ESM_Explainer_Video_One_Shot_Foley_Cup_Drink_Glass_Pick_Up_Off_Wood_Surface_1.wav`) | уборка: кружка |
| `c1s1_cleanup_ball.ogg` | 0.44 с | резиновый мяч, хват (Splice `ESM_HDS2_Cinematic_FX_rubber_ball_bouncy_toy_grab_hit_catch_20.wav`) | уборка: мяч |

Тройки `_1/_2/_3` — варианты одного удара, код выбирает случайный, чтобы
серия не звучала как петля. Можно положить и один файл, но тогда убрать
лишние имена из кортежа в константах, иначе в лог пойдут сообщения
`sm_sfx: нет файла ...` (сцена при этом не падает — звук просто молчит).

Метроном играет отдельным зацикленным слоем `c1s1_metronome`: смена кадра на
пианино, руки, холл или дверь его не перезапускает. Первый стук запускает
плавное изменение обработки за `C1S1_METRONOME_FILTER_T` (7 с): low-pass до
`C1S1_METRONOME_LOWPASS_HZ` (2200 Гц) и реверберацию с
`C1S1_METRONOME_REVERB_RESONANCE = 0.72`, `C1S1_METRONOME_REVERB_WET = 0.55`.
После замков слой затихает за `C1S1_METRONOME_FADEOUT_T` (1.2 с).
Настройки находятся в `game/1_chapter/chapter_1_scene_1.rpy`.

Loop — два такта: щелчки чередуются, у каждого отрезано мягкое вступление (~30 мс до порога),
чтобы атака была в первых миллисекундах, хвост обрезан до 0.68 с с затуханием, пик
нормализован до −3 dBFS. Длина WAV — `2 * C1S1_ARROW_HALF_T`, атаки — на половине каждой
доли (точка разворота стрелки). При замене щелчков повторить из корня проекта, подставив в
`-ss` начало атаки каждого щелчка (`-t` и `-fs` ограничивают вывод: без них `apad` пишет
бесконечный файл):

```powershell
ffmpeg -y -ss 0.0299 -i game/audio/sfx/metronome_1.ogg -t 0.68 -af "afade=t=in:d=0.002,afade=t=out:st=0.60:d=0.08" -ar 48000 -c:a pcm_s16le -fs 2000000 click1.wav
ffmpeg -y -ss 0.0325 -i game/audio/sfx/metronome_2.ogg -t 0.68 -af "afade=t=in:d=0.002,afade=t=out:st=0.60:d=0.08" -ar 48000 -c:a pcm_s16le -fs 2000000 click2.wav
ffmpeg -y -i click1.wav -i click2.wav -filter_complex "[0:a]adelay=352.941:all=1[a];[1:a]adelay=1058.824:all=1[b];[a][b]amix=inputs=2:normalize=0:duration=longest,apad=whole_dur=1.411765[out]" -map "[out]" -t 1.411765 -ar 48000 -c:a pcm_s16le -fs 2000000 game/audio/sfx/c1s1/metronome_loop.wav
```

Затем нормализовать пик WAV до −3 dBFS (`volumedetect` → `volume=<-3 − max>dB`).

При изменении темпа одновременно менять `C1S1_ARROW_HALF_T`, задержки атак (половина и
полторы доли в миллисекундах) и длину WAV (две доли в секундах).
