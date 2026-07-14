# после label start обнуляем события игры:
# $ events = [ ]

# узнать, было ли событие (на входе может быть только одно)
# if has(event):

# узнать, было ли одно из событий (на входе указывается любое количество через запятую)
# if has_or(event1[, ...]):

# узнать, были ли все события (на входе указывается любое количество через запятую)
# if has_and(event1[, ...]):

# добавить событие
# $ add(event)

# вызвать меню выборов с поддержкой кнопок-картинок:
# menu(screen="img"):

# в тексте выборов указать картинку:
# "Текст подсказки{#img=sprite}"

# спрайты создавать с привязкой к координатам!
# image bed = At("bg room bed", pos(1270, 630))

# как задать выбор с картинкой (#img) и подсказкой (сам текст),
# а так же с условием активности кнопки (#if) и с альтернативным текстом подсказки (#else) -
# после menu(screen="img") добавить кнопку:
# "Здесь будет удобнее{#img=bed}{#if=has('movie')}{#else=Ну нельзя же так сразу!}":
    # $ add('bed')

# неактивные из-за тега #if кнопки-картинки не реагируют на клик, но поддерживают подсказки из #else

# положение текстовых кнопок можно указать:
# menu(screen="img", vbox_align=(.5, .05)):

# это меню можно использовать и только для обычных текстовых кнопок,
# но оно поддерживает выбор текста кнопки и активность из условий в тегах {#if=условие}{#else=текст}

init -2 python:
    # все события игры
    events = [ ]

    # произошло ли событие
    def has(event):
        return event in events

    # произошло ли одно из событий
    def has_or(*args):
        for i in args:
            if i in events:
                return True
        return False

    # произошли ли все события, что указаны на входе
    def has_or(*args):
        for i in args:
            if not i in events:
                return False
        return True

    # добавляем событие
    def add(event):
        if not has(event):
            store.events.append(event)

init -2:
    # поведение кнопки, вариант для кнопок с картинкой-подсветкой
    transform imghover(t=.35):
        # при наведении становится непрозрачной
        on hover:
            ease_back t alpha 1

        # в обычном состоянии кнопка-подсветка прозрачная
        on idle:
            linear t alpha 0

# своя версия меню выборов, которая поддерживает кнопки-картинки и неактивные кнопки
screen img(items, vbox_align=(.5, .4)):
    # флаг для обхода бага со срабатыванием на старте on hover
    default start = True

    if start:
        timer .01 action SetScreenVariable("start", False), Function(renpy.restart_interaction)

    # сначала покажем картинки-кнопки, если они есть
    for i in items:
        $ img = get_tag(i.caption, "img")

        if img:
            imagebutton:
                idle img
                pos(0, 0)
                xysize(config.screen_width, config.screen_height)

                focus_mask True

                # никаких реакций на старте
                if start:
                    at alpha(0)

                # реакция на наведение, но только при соблюдении условий в теге
                else:
                    if tag_if(i.caption):
                        at imghover
                    else:
                        at alpha(0)

                # обычная подсказка
                if tag_if(i.caption):
                    tooltip i.caption

                # подсказка из тега #else, если не выполнено условие из тега #if
                else:
                    tooltip get_tag(i.caption, "else")

                # кликать можно только по кнопкам, где выполнены условия или их нет
                if tag_if(i.caption):
                    action i.action

                # сохраняем активность для вывода подсказок,
                # но не даём никак реагировать на нажатие
                else:
                    action NullAction()
                    activate_sound None

    # затем обычные кнопки выборов
    style_prefix "choice"

    vbox:
        # относительное положение текстовых кнопок
        align vbox_align

        for i in items:
            # без картинок из тега #img
            if not get_tag(i.caption, "img"):
                $ cap = get_tag(i.caption, "else")

                # на кнопке тоже может быть альтернативный текст из тега #else
                # если тег #else НЕ пуст И выполнено условие из тега #if
                if tag_if(i.caption) or not cap:
                    $ cap = i.caption

                textbutton cap:
                    # кликать можно только по кнопкам, где выполнены условия или их нет
                    sensitive tag_if(i.caption)
                    action i.action
