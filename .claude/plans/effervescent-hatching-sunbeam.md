# Пролог, сцена 1 — упрощение мини-игры «наведи порядок на столе»

## Контекст

Текущая мини-игра в `game/0_prologue/scene1.rpy` перегружена: рука следует за
мышкой (`mouse_follow` + `ConditionSwitch` поз grab/focus), предметы едут на место
за 3+2 клика с посчётной анимацией (`note2_move`, `note2_state`), камера трясётся и
идёт зерно с нарастанием «напряжения» (`note2_tension`, `mouse_parallax` c shake,
`noise_overlay`). Автор хочет упростить: беспорядок на столе → игрок наводит курсор
на карандаш или бумагу и делает **один клик** → сцена оказывается в состоянии
порядка. Тряску и множественные клики убираем; анимация руки — простое
«перетекание» между двумя позами (без слежения за курсором).

Автор добавил новые качественные ассеты в
`shuffling_man_assets/Черновик/1_Пролог/` — их нужно перенести в репозиторий и
использовать.

### Решения автора (подтверждены)

1. **Переход беспорядок→порядок — кросфейд композитов** (`Dissolve`), а не сдвиг
   слоёв. Используем готовые полнокадровые композиты с авторскими тенями/светом.
2. **Текст — только вступление и финал.** 5 инкрементальных реплик (3 про листы,
   2 про карандаш), привязанных к посчётным кликам, **удаляем** (автор согласовал).
3. **Атмосфера — зерно + мягкий параллакс.** Убираем только тряску (shake); зерно
   постоянное, параллакс камеры за мышкой остаётся.

## Шаг 1. Перенос ассетов

Скопировать 8 файлов в `game/images/0_prologue/` с переименованием под конвенцию
(нижний регистр, латиница, формат «тег атрибут» через пробел). Источник →
цель (имя образа в коде):

| Источник (`…/Черновик/1_Пролог/`) | Файл в `game/images/0_prologue/` | `image` |
|---|---|---|
| `Prologue_note_2_bg.jpg` | `prologue_note2 bg.jpg` | `prologue_note2_bg` |
| `Prologue_note_2.jpg` (беспорядок) | `prologue_note2 messy.jpg` | `prologue_note2_messy` |
| `Prologue_note.jpg` (порядок) | `prologue_note2 ordered.jpg` | `prologue_note2_ordered` |
| `paper.png` | `prologue_note2_paper.png` | `prologue_note2_paper` |
| `pencil.png` | `prologue_note2_pencil.png` | `prologue_note2_pencil` |
| `Prologue_hand anim right.png` (rest) | `prologue_hand2_right rest.png` | `prologue_hand2_right` |
| `Prologue_hand anim right move.png` | `prologue_hand2_right move.png` | `prologue_hand2_right_move` |
| `Prologue_hand anim left.png` | `prologue_hand2_left.png` | `prologue_hand2_left` |

Копировать через `Copy-Item` (PowerShell). Размеры: композиты 1920×1080; paper 559×676,
pencil 50×572, руки rest 384×624 / move 630×836 / left 550×666 (вырезанные объекты).

Примечание: при кросфейде композитов сам `prologue_note2 bg.jpg` не выводится в кадр
(фон уже запечён в оба композита). Переносим его по просьбе автора — как основу на
случай будущего перехода к послойной анимации; в этой сцене он не `show`-ится.

## Шаг 2. Полная переработка `game/0_prologue/scene1.rpy`

Интро-часть (тёмная комната → затылок ГГ, лейбл до записки) **не трогаем** — она
не относится к мини-игре и её текст неприкосновенен.

### Что удалить (весь механизм посчётных кликов и слежения за мышкой)

- Образы старых слоёв и рук: `note2_bg`, `note2_paper`/`note2_pencil` (Crop),
  `prologue_hand_left/right/right_move/right_write/grab_focus/grab`,
  `prologue_note_messy`, `prologue_note_center`, `prologue_hand_right_follow`
  (`ConditionSwitch`).
- Опорные точки и флаги руки: `NOTE2_HAND_REF`, `NOTE2_HAND_FOCUS_REF`,
  `NOTE2_HAND_GRAB_REF`, `NOTE2_HAND_SMOOTH`, `note2_hand_hover`, `note2_hand_grab`.
- Механику кликов: `NOTE2_PAPER`/`NOTE2_PENCIL` (dict с `from`/`to`/`clicks`),
  `note2_state()`, transforms `note2_move`, `note2_place`, экран
  `prologue_note_align`, `while`-цикл и посчётные ветки с 5 репликами.
- Параметры тряски: `NOTE2_SHAKE_AMP`, `NOTE2_RELAX`, `note2_tension` и их передачу
  в `mouse_parallax`/`noise_overlay`.

### Что добавить

**Образы** — по таблице Шага 1, плюс подсветки (переиспользуют шейдеры из
`common/shaders.rpy` — `outline_hover`, `hover_pulse`):

```renpy
image prologue_note2_paper_hl = At("prologue_note2_paper", outline_hover(), hover_pulse())
image prologue_note2_pencil_hl = At("prologue_note2_pencil", outline_hover(), hover_pulse())
```

**Статичная постановка предметов под беспорядок** (paper/pencil нарисованы прямо —
поворачиваем и ставим по позициям с `prologue_note2 messy.jpg`; значения-ориентиры,
финально подбираются в игре). Координаты — только `int`:

```renpy
transform note2_paper_messy:
    anchor (0.5, 0.5) pos (790, 415) rotate -8
transform note2_pencil_messy:
    anchor (0.5, 0.5) pos (835, 210) rotate 72
```

**Флаг наведения** (для смены позы правой руки):

```renpy
default note2_hover = False
```

**Экран интерактива** — модальный, две невидимые кнопки-предмета (idle alpha 0,
hover — пульсирующий контур, `focus_mask` по объекту для попиксельного хита); клик по
любому предмету завершает мини-игру. Позу-«move» правой руки кладём внутрь этого же
экрана через `showif` + `show_hide` из 7dots (перетекание alpha):

```renpy
screen prologue_note2_align():
    modal True
    imagebutton:
        at note2_paper_messy
        idle Transform("prologue_note2_paper", alpha=0.0)
        hover "prologue_note2_paper_hl"
        focus_mask "prologue_note2_paper"
        hovered SetVariable("note2_hover", True)
        unhovered SetVariable("note2_hover", False)
        action Return("done")
    imagebutton:
        at note2_pencil_messy
        idle Transform("prologue_note2_pencil", alpha=0.0)
        hover "prologue_note2_pencil_hl"
        focus_mask "prologue_note2_pencil"
        hovered SetVariable("note2_hover", True)
        unhovered SetVariable("note2_hover", False)
        action Return("done")
    ## Рука «тянется» — появляется/гаснет перетеканием (7dots show_hide).
    showif note2_hover:
        add "prologue_hand2_right_move" anchor (0.5, 0.5) pos (RMX, RMY) at show_hide
```

**Лейбл** (часть с запиской переписывается так):

```renpy
    ## Беспорядок: зерно + мягкий параллакс, без тряски.
    camera at mouse_parallax(NOTE2_PARALLAX, NOTE2_PARALLAX_SMOOTH)
    scene prologue_note2_messy
    $ note2_hover = False
    show prologue_hand2_left at note2_hand_pos(LX, LY)
    show prologue_hand2_right at note2_hand_pos(RX, RY)
    show fx_noise at noise_overlay(NOTE2_NOISE)
    with prologue_dissolve

    "Пора начинать. Но не так. Не с такого стола."
    "Листы лежат криво. И карандаш. Сначала нужно всё поправить — иначе не выйдет ни строчки."

    window hide
    call screen prologue_note2_align
    $ note2_hover = False
    window auto

    ## Порядок наведён — кросфейд композитов; рука-move уже погасла (hover=False),
    ## статичные руки и зерно уходят вместе с dissolve (scene очищает master).
    camera
    scene prologue_note2_ordered
    with Dissolve(0.6)

    "Теперь всё ровно. Можно начинать."
    "Я здесь после нервного срыва, что разрушил мою и без того распадавшуюся на части жизнь и подорванное здоровье."
    "Это письмо... должно помочь мне пережить произошедшее."
    return
```

Где `note2_hand_pos(x, y)` — маленький transform `anchor (0.5,0.5) pos (x,y)`.
`mouse_parallax` без 3-го/4-го аргумента → `shake_amp=0`, `tension_var=None` (тряски
нет); `noise_overlay(NOTE2_NOISE)` без `tension_var` → постоянное зерно. Параметры
`NOTE2_PARALLAX`, `NOTE2_PARALLAX_SMOOTH`, `NOTE2_NOISE` уже определены — оставляем.

Плейсхолдеры координат (`RMX/RMY`, `LX/LY`, `RX/RY`, а также pos/rotate в
`note2_*_messy`) подбираются визуально в игре — см. Шаг 4.

### Текст — что остаётся дословно, что удаляется

Остаются (без изменений): вступительные `"Пора начинать…"` и `"Листы лежат криво…"`;
финальные `"Теперь всё ровно…"`, `"Я здесь после нервного срыва…"`,
`"Это письмо…"`. Весь блок «затылка ГГ» до записки — без изменений.

Удаляются 5 инкрементальных реплик (по решению автора): `"Я подравняла стопку…"`,
`"Это «чуть-чуть» невыносимо. Ещё раз."`, `"Вот. Края совпали…"`,
`"Карандаш лежал поперёк листа…"`, `"Вдоль правого края…"`.

## Шаг 3. Чистка осиротевших ассетов (с подтверждением)

`prologue_note`/`prologue_hand`/`note2` встречаются только в `scene1.rpy`, поэтому
после переработки старые файлы можно удалить. Удалить осиротевший
`game/0_prologue/scene1.rpyc` (пересоберётся). Кандидаты на удаление из
`game/images/0_prologue/`: `prologue_note.jpg`, `prologue_note center.jpg`,
`prologue_note 2_bg.jpg`, `prologue_note 2_papaer.png`, `prologue_note 2_pencil.png`,
старые полнокадровые руки (`prologue_hand_left.png`, `prologue_hand_right.png`,
`prologue_hand_right move.png`, `prologue_hand_right write.png`) и незакоммиченные
эксперименты `prologue_hand_right grab*.png/.jpg`. Оставить `prologue dark_room.jpg`,
`prologue head.jpg`, `prologue pencil_close.jpg` (используются/задел). Список удаления
согласовать с автором перед выполнением.

## Шаг 4. Проверка (обязательно в реальной игре)

1. Запустить проект (skill `run` / Ren'Py SDK в `../renpy-8.5.3-sdk`), дойти до
   сцены записки (`script.rpy` → `jump prologue_s1`).
2. Проверить сценарий: беспорядок с зерном и лёгким параллаксом (без тряски) →
   наведение на бумагу/карандаш даёт контур-подсветку и рука перетекает в позу
   «move» → один клик → кросфейд в состояние порядка → финальные реплики.
3. Подобрать координаты по кадру: pos/rotate предметов в `note2_*_messy` (контур
   должен точно облегать бумагу и карандаш на `prologue_note2 messy.jpg`) и позиции
   рук (`LX/LY`, `RX/RY`, `RMX/RMY`) так, чтобы rest и move не «прыгали» при
   перетекании. Свериться с референс-композитом `Prologue_hand anim.jpg`.
4. Прогнать `renpy.sh <project> lint` — убедиться, что нет нераспознанных образов и
   ошибок.

## Возможные тонкости

- `focus_mask` на повёрнутой кнопке — паттерн из прежнего кода; проверить, что хит
  корректен после смены слоёв (иначе fallback — прямоугольная зона).
- Поза-«move» лежит на экране (над master) и не участвует в параллаксе, в отличие от
  статичных рук на master; при заметном рассинхроне на hover — уменьшить параллакс
  или продублировать смещение. Ожидается пренебрежимо малый эффект при 10 px.
