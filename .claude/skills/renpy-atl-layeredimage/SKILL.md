---
name: renpy-atl-layeredimage
description: Reference for Ren'Py 8.5.3 ATL (Animation and Transformation Language) and LayeredImage. Use when writing or editing .rpy code involving transforms, animations, ATL blocks, sprite movement/zoom/rotation/alpha, or layered character sprites (layeredimage, attributes, groups, auto groups). Triggers: ATL, transform, layeredimage, анимация, спрайт, трансформация.
---

# Ren'Py ATL и LayeredImage (Ren'Py 8.5.3)

Справочник для проекта Shuffling Man. Полная документация: `renpy-8.5.3-sdk/doc/transforms.html`, `renpy-8.5.3-sdk/doc/layeredimage.html`, `renpy-8.5.3-sdk/doc/transform_properties.html`.

## ATL — Animation and Transformation Language

Три способа включить ATL-код в скрипт:

```renpy
# 1. Оператор transform (переиспользуемый, поддерживает параметры)
transform slide_right(duration=1.0):
    xalign 0.0
    linear duration xalign 1.0

# 2. Оператор image с ATL-блоком (анимированное изображение)
image walk_cycle:
    "man_step1" 
    pause 0.3
    "man_step2"
    pause 0.3
    repeat

# 3. Инлайн в show/scene
show shuffling_man:
    xalign 0.5
    linear 2.0 xalign 1.0
```

Применение: `show eileen happy at slide_right`, несколько через запятую (слева направо): `at halfsize, right`.

### Основные операторы ATL

| Оператор | Синтаксис | Назначение |
|---|---|---|
| Свойства | `xalign 0.5 alpha 1.0` | мгновенно установить значения |
| Пауза | `pause 2.0` или просто `2.0` | ждать N секунд |
| Интерполяция | `linear 1.0 xalign 1.0` | плавно изменить свойства за время (warper + duration + свойства) |
| `repeat [N]` | последний в блоке | повторить блок (N раз макс.) |
| `block:` | вложенный блок | группировка для repeat |
| `parallel:` | несколько подряд | блоки выполняются одновременно; не менять одно свойство в двух блоках |
| `choice [вес]:` | несколько подряд | случайный выбор блока |
| `on <event>:` | show, hide, replace, replaced, hover, idle... | обработчик событий |
| `time N` | | жёсткая привязка ко времени от старта блока; прерывает предыдущий оператор |
| `event <имя>` | | сгенерировать событие |
| `animation` | первый в блоке | использовать animation timebase (at) вместо shown (st) |
| `function f` | `f(trans, st, at) -> float\|None` | Python-логика; вернуть число = вызвать снова через N сек, None = дальше |
| `contains` | инлайн или блок | установить ребёнка трансформа |
| `pass` | | no-op, разделитель |
| Displayable | `"img.png" [with Dissolve(.5)]` | заменить ребёнка, опционально с переходом |

### Интерполяция — детали

```renpy
linear 2.0 xalign 0.5 yalign 0.5      # несколько свойств сразу
warp my_func 1.0 xalign 1.0            # свой warper (функция t -> t')
linear 2.0 xalign 0.5 knot 0.0         # сплайн: 1 knot = квадр. Безье, 2 = кубич., 3+ = Catmull-Rom
linear 2.0 yalign 0.0 clockwise circles 3   # круговое движение (полярные координаты)
ease 1.0 truecenter                    # интерполяция к transform-выражению с одним properties-оператором
```

Warpers: `pause`, `linear`, `ease`, `easein` (быстро→медленно), `easeout` (медленно→быстро), плюс функции Пеннера: `ease_quad`, `ease_cubic`, `ease_elastic`, `ease_bounce`, `ease_back`, `easein_*`, `easeout_*` и т.д. (см. easings.net; имена Ren'Py инвертированы относительно easings.net: `easein_quad` = easeOut_quad). Свой warper — через `@renpy.atl_warper` в `python early`.

### Часто используемые transform-свойства

Позиция: `pos`, `xpos/ypos`, `anchor`, `xanchor/yanchor`, `align`, `xalign/yalign`, `xycenter`, `offset`, `xoffset/yoffset`. Размер/масштаб: `zoom`, `xzoom/yzoom` (отрицательный = отражение), `xysize`, `fit`. Вращение: `rotate`, `rotate_pad`, `transform_anchor`. Прозрачность: `alpha`, `additive`. Обрезка: `crop`. Цвет: `matrixcolor` (`TintMatrix`, `SepiaMatrix`...). Полярные: `angle`, `radius`, `around`. Значения float 0.0–1.0 = доля экрана/размера, int = пиксели.

### События (on)

Автоматические: `start`, `show` (нет image с таким тегом), `replace`, `hide`, `replaced`, `hover`, `idle`, `selected_hover` и т.п. (для кнопок).

```renpy
transform fade_in_out:
    on show:
        alpha 0.0
        linear .5 alpha 1.0
    on hide:
        linear .5 alpha 0.0
```

### Важные механики

- **`rotate` (или анимируемый `zoom`) + позиционирование по `anchor`/`pos` → всегда ставить `transform_anchor True`.** Активный `rotate` с дефолтным `rotate_pad` расширяет холст спрайта до квадрата со стороной-диагональю (у 363×793 получится ≈872×872 — «размер с одинаковыми сторонами»), и без `transform_anchor` якорь отсчитывается от этого квадрата — объект уезжает с позиции. С `transform_anchor True` якорь считается по самому спрайту и одновременно становится пивотом поворота/масштаба (нужен низ маятника — `anchor (0.5, 1.0)`). Примеры в проекте: `c1s1_arrow_swing`, `c1s1_gg_idle` в `1_chapter/chapter_1_scene_1.rpy`.
- **Замена трансформов**: при `show ... at new_transform` свойства старого трансформа наследуются новым (включая промежуточные значения анимации). Позиционные свойства ребёнка перекрывают родительские. Сброс — hide + show, либо `show tag: pass` (сброс анимации с сохранением позиции), либо трансформ `reset`.
- **Timebases**: `st` — с момента показа этого displayable; `at` — с момента показа тега. `animation` переключает блок на `at` — нужно для смены выражений без сброса анимации позиции.
- **Каррирование**: `transform t(a, b=1)` можно частично вызывать: `define t2 = t(b=2)` — результат снова трансформ.
- **Параметр child**: `transform ts(child):` — ребёнок автоматически подставляется, можно временно подменять displayable (jump scare) или оборачивать в `contains:`.
- Выражения в ATL вычисляются при первом запуске трансформа, не на каждом операторе.
- ATL-трансформы создаются в init time; это displayables, их можно передавать в `Add`, `renpy.show()` и т.д.
- Python: `At(d, t)` — универсальный способ применить трансформ; класс `Transform(child, function=..., **props)`.

## LayeredImage — послойные спрайты

Решает комбинаторный взрыв: персонаж с 4 нарядами × 6 эмоций = 24 комбинации из отдельных слоёв вместо 24 файлов. Определяется в init time.

```renpy
layeredimage augustina:
    zoom 1.4                    # transform-свойства применяются ко всему образу
    at recolor_transform        # или at transform: с ATL-блоком

    always:                     # слой, показанный всегда
        "augustina_base"

    group outfit:               # атрибуты в группе взаимоисключающие
        attribute dress default # default = активен, если ничего из группы не вызвано
        attribute uniform

    group face auto:            # auto: атрибуты добираются из имён файлов по паттерну
        pos (100, 100)          # свойства группы наследуются атрибутами
        attribute neutral default

    if glasses == "evil":       # условие, вычисляется в рантайме (ConditionSwitch)
        "augustina_glasses_evil"
    else:
        "augustina_glasses"

label start:
    show augustina                  # dress + neutral (дефолты)
    show augustina happy            # happy заменит neutral (та же группа)
    show augustina uniform -happy   # uniform вместо dress, -happy убирает атрибут
```

### Паттерн имён файлов

Изображение атрибута без явного displayable ищется как `имя_группа_вариант_атрибут` (пробелы в имени → подчёркивания). Для `layeredimage augustina work`, группы `eyes`, варианта `blue`, атрибута `closed` → `augustina_work_eyes_blue_closed.png`. Опции: `image_format "sprites/eileen/{image}.png"` (не влияет на auto-группы), `format_function`, `attribute_function`.

### Ключевые элементы

- `always:` — слой без атрибута, displayable обязателен. Свойства: `when`, `at`, transform-свойства.
- `attribute <имя> [default] [null]` — `null` = атрибут без displayable (для логики when).
- `group <имя> [auto] [multiple]` — `multiple` = без взаимоисключения; `variant <слово>` и `prefix <слово>` влияют на паттерн/имена. Несколько групп с одним именем = одна группа (для слоёв спереди/сзади). Атрибут может состоять в нескольких группах.
- `if/elif/else` — рантайм-условия по переменным.
- `when <выражение>` — условие по активным атрибутам: `when b and not c`. Заменяет устаревшие `if_all/if_any/if_not`.
- `LayeredImageProxy("augustina", Transform(...))` — дубликат с трансформом (боковой портрет, сепия и т.п.), принимает атрибуты в отличие от `Transform("augustina")`.

### Советы из документации

- Использовать подчёркивания в именах файлов слоёв, не пробелы — иначе спрайт слоя может показаться сам по себе (глаза, парящие в воздухе).
- Не нужно обрезать слои вручную — Ren'Py сам кропит по bounding box непрозрачных пикселей.
- Всё в блоке layeredimage (кроме условий if) вычисляется в init time — не использовать меняющиеся в рантайме данные; для динамики — `config.adjust_attributes`, `attribute_function`.
- Выбор синтаксиса: всегда видимый слой → `always` или `attribute x default`; зависит от show-атрибутов → `attribute`; зависит от переменной → `if`; от обоих → атрибуты + `config.adjust_attributes`.
- Показ слоя при отсутствии атрибутов группы: добавить в группу `attribute notop null default`, затем `attribute hair_patch when notop`.

## Комбинирование ATL + LayeredImage

```renpy
layeredimage hero:
    attribute base default
    attribute glow:
        image:                       # ATL-анимация внутри атрибута
            "hero_glow"
            alpha 0.5
            linear 1.0 alpha 1.0
            linear 1.0 alpha 0.5
            repeat

transform breathing:
    yzoom 1.0
    ease 2.0 yzoom 1.005
    ease 2.0 yzoom 1.0
    repeat

label start:
    show hero glow at breathing
```
