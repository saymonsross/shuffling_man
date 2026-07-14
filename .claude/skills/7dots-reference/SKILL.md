---
name: 7dots-reference
description: Справочник по библиотеке 7dots.rpy для проекта Shuffling Man. Используй этот skill ПЕРЕД реализацией любой функциональности в Ren'Py скрипте — библиотека может уже содержать нужный инструмент.
---

# Правило использования 7dots

**ОБЯЗАТЕЛЬНО:** Перед реализацией любой функциональности в `.rpy` файлах — проверь этот справочник. Если нужное уже есть в 7dots, используй готовое без дублирования.

Библиотека загружается из `game/libs/7dots.rpy` и доступна глобально во всём проекте.

---

## Аудио

Все функции автоматически добавляют папку и расширение `.ogg`. Директории по умолчанию: музыка → `game/music/`, звуки → `game/audio/`, голос → `game/voices/`.

| Функция | Описание | Пример |
|---------|----------|--------|
| `mplay(name)` | Музыка с fade (1.5с) | `$ mplay("theme")` |
| `mplay([a, b])` | Плейлист по порядку | `$ mplay(["intro", "loop"])` |
| `rndplay([a, b])` | Плейлист в случайном порядке | `$ rndplay(["rain1", "rain2"])` |
| `mreplay(name)` | Перезапустить, даже если уже играет | `$ mreplay("theme")` |
| `mstop()` | Стоп музыку с fade | `$ mstop()` |
| `msave()` / `mrestore()` | Сохранить/восстановить играющую мелодию | `$ msave()` |
| `splay(name)` | Звуковой эффект (канал audio) | `$ splay("click")` |
| `sndplay(name)` | Звуковой эффект (канал sound) | `$ sndplay("door")` |
| `sfxplay(name)` | Зацикленный эффект (канал effect) | `$ sfxplay("wind")` |
| `sfxstop()` | Стоп зацикленный эффект | `$ sfxstop()` |
| `vplay(name)` | Голос из `voices/` | `$ vplay("marina_01")` |
| `sstop()` / `sndstop()` | Стоп звук | `$ sstop()` |

Action-версии для экранов: `MPlay`, `MStop`, `SPlay`, `SFXPlay`, `SFXStop`, `VPlay`, `FNPlay`.

Воспроизведение звука из transform/функции: `function renpy.curry(s_play)("click")` (однократно), `function renpy.curry(sfx_play)("wind")` (зациклено).

---

## Трансформации (применяются через `at`)

### Позиционирование

```renpy
show marina at left2      # слева (xalign=0.35 по умолчанию)
show marina at right2     # справа (xalign=0.65)
show marina at left0      # за левым краем экрана (offscreen)
show marina at right0     # за правым краем
show marina at align(0.5, 1.0)    # произвольное положение
show marina at pos(0.5, 0.0)      # через xpos/ypos
show marina at offset(5, 0)       # смещение в пикселях
show marina at aligning(0.3, 1., 0.7, 1., t=1)  # плавное движение
```

### Масштаб и поворот

```renpy
show bg at zoom(1.2)              # масштаб
show bg at zooming(1.0, 1.3, t=2) # плавное изменение масштаба
show bg at rotate(45)             # поворот (против часовой)
show bg at rotating(0, 360, t=3)  # вращение
show bg at hflip                  # зеркало по горизонтали
show bg at vflip                  # зеркало по вертикали
show bg at turnx(30)              # 3D-поворот вверх/вниз
show bg at turny(45)              # 3D-поворот влево/вправо
show bg at turnz(20)              # 3D-поворот по оси Z
show bg at turn(x=10, y=30, z=5)  # по всем осям сразу
show bg at crop(0, 0, 0.5, 1.0)   # вырезать часть
```

### Прозрачность, фильтры

```renpy
show bg at alpha(0.5)                     # прозрачность
show bg at alphing(0, 1, t=1)            # плавное появление
show bg at blur(8)                        # размытие
show bg at bluring(0, 16, t=2)           # нарастающее размытие
show bg at brightness(0.25)              # яркость
show bg at brightnessing(-0.2, 0.1, t=2) # изменение яркости
show bg at contrast(1.5)                 # контраст
show bg at saturation(0.3)               # насыщенность (0=ч/б)
show bg at saturationing(1., 0., t=3)   # обесцвечивание
show bg at color("#f00")                 # цветовой тинт
show bg at coloring("#fff", "#f00", t=2) # переход цвета
show bg at color2("#fff", "#adf", t=3)  # пульсация цвета
```

### Силуэты

```renpy
show monster at paint()           # белый силуэт
show monster at paint(color="#f00") # красный силуэт
show monster at painting("#fff", "#f00", t=2)  # переход силуэта
show monster at paint2("#fff", "#f00", t=2)    # пульсирующий силуэт
```

### Анимационные трансформы

```renpy
show marina at breath          # "дыхание" (тихое покачивание)
show marina at leap            # прыжок (одиночный)
show marina at boobs           # физика — покачивание (одиночное)
show marina at hover_at        # реакция на курсор мыши
show bg at zpunch              # "удар" масштабом (переход with)
show widget at show_hide       # плавное появление/исчезновение
show bg at xy_at               # прикрепить к позиции курсора
```

### Размеры

```renpy
show bg at xysize(1920, 1080)
show panel at xsize(400)
show panel at ysize(200)
```

---

## Переходы (with)

```renpy
with Flash()             # белая вспышка (по умолчанию)
with Flash("#000", 2)    # чёрная вспышка, 2 секунды
with flash             # заранее объявленная белая вспышка
with zpunch            # "удар" масштабом
with TurnPage()        # перелистывание вправо
with TurnPage(reverse=True)   # перелистывание влево
with TurnPage(vertical=True)  # перелистывание вниз
with turn2left / turn2right / turn2up / turn2down  # готовые варианты
```

---

## Управление диалогом и интерфейсом

```renpy
$ dismiss_off()      # запретить переход по клику
$ dismiss_on()       # разрешить переход по клику
$ skip_once()        # пропустить одно ожидание
$ skip_stop()        # остановить перемотку
$ pause(2)           # жёсткая пауза 2 секунды
```

Для экранов — action-версии: `DismissOff()`, `DismissOn()`, `SkipOnce()`, `SkipStop()`.

---

## Экраны

```renpy
$ has_screen("history")           # показан ли экран
$ screen_exists("my_screen")      # объявлен ли экран
$ showhide("inventory")           # переключить видимость
ShowHide("inventory")             # то же как action
$ show_s("hud")                   # показать на слое master (не прячется по H)
$ hide_s("hud")
$ show_forever("overlay")         # не прячется по клавише H
$ hide_forever("overlay")
$ show_foreverest("always_on")    # не прячется вообще никогда
$ hide_foreverest("always_on")
```

---

## Информация о спрайтах на экране

```renpy
$ sprite_showed("marina")               # bool: показан ли спрайт
$ get_sprite_by_tag("marina")           # полное имя спрайта с тегом
$ get_showing_sprites()                 # список всех спрайтов на слое master
$ get_sprite_bounds("marina")           # (x, y, w, h) в пикселях
$ has_image("marina happy")             # объявлено ли изображение
$ has_images("a", "b")                  # объявлены ли все из списка
$ seen_one("marina sad", "marina cry")  # хотя бы одно показывалось
$ seen_all("marina happy", "marina sad") # все показывались
```

---

## Система "времён суток"

Автоматически применяет матрицы цвета к спрайтам и фонам.

```renpy
# Настройка (в init-блоке или options):
$ daytime_prefix = ["bg", "marina"]  # префиксы реагирующих спрайтов
$ alldaytime = ["day", "evening", "night", "morning"]  # список времён

# Переключение в скрипте:
$ setdaytime("night")    # установить конкретное
$ setdaytime()           # переключить на следующее в списке

# Настройки освещения (в init -99):
# night_bg_attrs = ("#9af", -.475, .375, .575)  # (цвет, яркость, насыщ, контраст)
# night_attrs    = ("#9af", -.1, .375, 1)

# Применить вручную:
show bg street at atdaytime(True)   # bg=True для фонов
show marina at atdaytime()           # для спрайтов
```

Именование файлов: `bg_street_day.png`, `bg_street_night.png` — первый суффикс (`day`) можно опустить.

---

## Анимация кадров

```renpy
# Объявить анимацию из файлов neko1.png, neko2.png ... neko5.png:
image neko = Ani("neko", 5, delay=0.1)

# С переменной скоростью (от 0.1 до 0.5 сек):
image neko = Ani("neko", 5, delay=(0.1, 0.5))

# Туда-обратно (ping-pong):
image neko = Ani("neko", 5, 0.1, reverse=True)

# С дополнительными параметрами:
image neko = Ani("neko", 5, 0.1, zoom=2.0, alpha=0.75)

# Из displayable (уже объявленных изображений), без ext:
image neko = Ani("neko", 5, 0.1, ext=None)
```

---

## Работа с текстом и тегами

```renpy
# Скрытые теги в тексте {#key=value}:
$ text = "Слова слова {#mood=sad} слова."
$ mood = get_tag(text, "mood")      # → "sad"
$ has_tag = have_tag(text, "mood")  # → True
$ clean = del_tags(text)            # убрать все {#...} теги
$ clean2 = del_all_tags(text)       # убрать все теги (включая Ren'Py)
$ short = str_cut(text, max_len=20) # обрезать с "…"
```

---

## Вспомогательные виджеты и displayable

```renpy
# Цифровые часы (реальное время):
image clock = Clock(size=48, color="#fff8", align=(0.05, 0.05))
show clock

# Маска по красному каналу (не альфа):
image masked = ImageMask("character", "mask_red")

# Показать кадр скриншота:
$ shot()   # сохраняет и возвращает FileCurrentScreenshot()
```

---

## Утилиты

```renpy
$ rnd(1, 10)          # случайное целое от 1 до 9 (верхний предел НЕ включается)
$ rndf(0.0, 1.0)      # случайное дробное
$ rnds("a", "b", "c") # случайный элемент из аргументов

$ lang()              # переключить язык на следующий
$ lang("russian")     # переключить на конкретный

$ cps_save()          # сохранить скорость текста
$ cps_set(30)         # задать скорость
$ cps_restore()       # восстановить сохраненную

$ get_music_list()    # список файлов из папки music/
$ get_file_list("images", "png")  # список файлов в папке

$ delete_saves()      # удалить все сохранения (с запросом)
$ delete_data()       # удалить все данные (с запросом)
```

Кнопка "Продолжить" для главного меню: `textbutton "Продолжить" action Continue()`

---

## Автообъявление изображений

Активируется в `init`-блоке:

```renpy
init python:
    images_auto()                        # из папки images/
    images_auto(["images", "sprites"])   # из нескольких папок
    layered_prefixes = ["char"]          # для LayeredImage — теги через "_"
```

После этого файл `images/marina_happy.png` автоматически объявляется как `image marina happy`.
