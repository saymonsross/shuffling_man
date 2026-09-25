# Корпус: купленные демо и прототип

Локальный корпус — машинно-зависимые пути; на другой машине их может не быть, skill работает и без них.

- `OLD` = `D:/Dev/GameDev/RenPy/OLD/RenPy` — купленные демо 7dots (`test_*`, `pipes`, `7DOTS/test_*`) и сторонние
  краулеры. Знания в них — русские комментарии в коде и демо-сценарий `game/script.rpy`; отдельных гайдов нет.
  Демо написаны под 8.1–8.4 (в логах 8.3.4 и 8.4.2): сверяй всё по [engine-facts.md](engine-facts.md).
- `SHAMBLER` = `D:/Dev/GameDev/RenPy/RenPyProjects/0_Shambler` — прототип «Шаркающего человека».
- `<sdk>/tutorial/game/indepth_minigame.rpy` — Pong на CDD из туториала движка.

`renpy-vn-toolkit/sources/` — побайтные копии части этих демо (кроме переводов строк), с теми же дефектами.
Общие болезни почти всех демо: цикл на голом `pause`, состояние глобалами без `default`, параметры лейбла с общими
именами (`time`, `range`), результат глобалом, непереводимые строки, нет паритета ввода и тестов.

## Мини-игры

| Демо | Путь | Чему учит | Не копировать |
|---|---|---|---|
| BALANCE (маятник) | `OLD/test_balance/game/BALANCE/` | отсчёт 3-2-1 отдельным лейблом; «рабочая» часть полосы через crop второй рамки; жёсткие паузы «остыть» | голый `pause` (авточтение = автопроигрыш), проверка попадания постфактум `get_image_bounds`, `time=` в параметрах |
| SIMPLE_CLICKER (мэш) | `OLD/test_simple_clicker/game/SIMPLE_CLICKER/` | `key "dismiss"` как ввод всех устройств, `AnimatedValue`-шкала, `timer repeat` на убывание | `range=`/`time=` в параметрах, нет отклика на нажатие, откат не заблокирован |
| QTE_CIRCLE + QTE_KEYPAD | `OLD/test_qte_circle/game/QTE_CIRCLE/` | кольцо, сжимающееся ATL `xysize`; одна белая картинка + `TintMatrix` = вспышки любого цвета; механика «память» (`hide_after`) | цикл `while` + `pause`; промах по отпусканию любой клавиши; геймпад падает с `IndexError`, SELECT/START перепутаны; вспышки копятся на master |
| MOUSE | `OLD/test_mouse/game/MOUSE/` | `MouseDisplayable` с анимацией и `pressed_*`-вариантами | хотспот `.15` там — это пиксели, не доля |
| pipes (повороты) | `OLD/pipes/pipes/red_pipes/pipes.rpy` | представление клетки `[тип, поворот]`, редактор уровней с экспортом литерала; красно-чёрный скин под хоррор | «победа» по подписи ориентаций, а не по потоку; перемешивание в `default`; `show screen` + голый `pause`; сетка в `hbox` дёргается при `rotate` |

## Point-and-click и выбор картинкой

| Демо | Путь | Чему учит | Не копировать |
|---|---|---|---|
| bg_inventory (инвентарь) | `OLD/test_bg_inventory/test_bg_inventory/game/` | модель `Item` + диспетчер `use_<a>_<b>` в обоих порядках; невидимые хит-зоны (альфа 1/255 + `focus_mask`); курсор по режиму; очередь реплик-«разговоров» | показ предметов побочным эффектом ATL через `config.tag_transform`; `exec` из `{#…}`-тегов (мёртв в Python 3); локация поиском подстроки `bg`; `while` + `pause` |
| choice_img, fon_swap_selector, images_choose, test_renpy | `OLD/test_choice_img/game/`, `OLD/test_fon_swap_selector/game/`, `OLD/test_images_choose/game/`, `OLD/test_renpy/game/screens2.rpy` | хотспот-меню поверх фона; кроссфейд фона-«последствия» по наведению; путь `"[var]/файл"` — смена набора картинок одной переменной | данные пунктов в `{#…}`-тегах с `eval` (в 8.5 — аргументы `menu` и `i.kwargs`, `config.menu_include_disabled`); текст, запечённый в картинки |

## Эффекты

| Демо | Путь | Чему учит | Не копировать |
|---|---|---|---|
| flashlight | `OLD/test_flashlight/game/flashlight.rpy` | «поиск в темноте» как механика | лист 7680×4320 (~133 МБ кэша) |
| xray + censure | `OLD/test_xray/game/` | CDD с локальными координатами курсора | пересборка `Flatten`/`AlphaMask` каждый кадр; вечный оверлей; `images_auto()` включает автообъявление для всей игры |
| eyes, watcher | `OLD/test_eyes/game/`, `OLD/test_watcher/game/watcher.rpy` | зрачок меньше радужки → псевдо-3D; веки через `ImageDissolve` по градиенту | асимметричная формула взгляда; опрос мыши навсегда |
| parallax2d | `OLD/test_parallax_mm/game/parallax2d.rpy` | слои не меньше экрана, маленький спрайт — на полноэкранный холст | вертикаль делится на ширину экрана, шаг зависит от FPS — в проекте есть `mouse_parallax` |
| BW/LIQUID-шейдеры, FLASHBACK | `OLD/test_bwshader/game/`, `OLD/test_flashback/test_flashback/game/` | структура шейдерных частей, слой виньетки | непремультиплицированный цвет (ореолы), растущий `u_time`, одинаковые имена переменных |
| rain, steps | `OLD/7DOTS/test_rain/test_rain/game/`, `OLD/7DOTS/test_steps/test_steps/game/` | дешёвая погода 4 кадрами; несоизмеримые периоды молний; ритм шагов | звук из ATL (живёт после `scene`); `rnd(1)` всегда 0 |

## Краулеры

| Демо | Путь | Чему учит | Не копировать |
|---|---|---|---|
| 7dots dungeon v4 (3D Stage) | `OLD/test_dungeon_v4/game/DUNGEON/` | квады стен, FOV 90° через `config.perspective`, твин камеры, ходьба удержанием (флаги CDD + опрос трансформом), события-метки `D_*` через `renpy.get_all_labels()`, редактор с генерацией `.rpy` | голый `pause`; позиция в `define`; `config.perspective` не восстанавливается; кнопка действия геймпада = BACK (откат) |
| FPE (2D-срезы) | `OLD/Renpy_First_Person_Dungeon_Exploration/game/script.rpy` | схема срезов «глубина × колонка», порядок художника `1,7,2,6,3,5,4` — образец пайплайна ассетов | старт из `splashscreen` (нет меню и сейвов), сотни `if`, цепочки `jump` |
| Dungeon_Crawl 2.0 | `OLD/Dungeon_Crawl-2.0-all/Dungeon_Crawl-2.0-all/game/dungeon.rpy` | позиция + вектор `(dy, dx)`, зеркальные срезы `xzoom -1`, автокарта с памятью | движок Ren'Py 6; события на поворотах |
| Dungeon_Crawler (вид сверху) | `OLD/Dungeon_Crawler/game/scripts/dungeon_crawler/` | виньетка `Fog.png`, маски за стенами | отрицательные индексы Python читают другой край карты; утечка `quick_menu` |

## Прототип и эталоны

| Источник | Путь | Чему учит |
|---|---|---|
| Прототип «открыть дверь» | `SHAMBLER/game/minigames/act0/open_door/` | каталог ошибок, исправленных в замках: тупики без выхода, перерисовка только через отладочный `renpy.notify`, угол от центра экрана, drag как контроллер вращения, `global` после использования |
| BALANCE/CLICKER прототипа | `SHAMBLER/game/BALANCE/`, `SHAMBLER/game/SIMPLE_CLICKER/`, сценарий `script.rpy` (`piano_test`) | контракт фразы пианино: исход `True/False/None` + время, окно по музыке, фальшивая нота, повтор с облегчением, финальная фраза доигрывается |
| Pong | `<sdk>/tutorial/game/indepth_minigame.rpy` | каркас CDD: `dt` из `st`, `renpy.redraw(self, 0)`, итог через `renpy.timeout(0)`, свежая партия из `default` экрана |
| Замки, уборка | `game/1_chapter/chapter_1_scene_1_minigame_locks.rpy`, `…_cleanup.rpy` | эталоны проекта: модели C и A, три уровня состояния, захват указателя, тесты в `game/dev/` |
