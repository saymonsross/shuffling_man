## КАК ПОЛЬЗОВАТЬСЯ:
# добавить папку BEEP себе в проект
# ну и можно ещё добавить разные звуки псевдо-голосов
# и заполнить список исключений beep_other

init -2 python:
    # имя файла для звука, который будет воспроизводиться во время диалогов
    beep = "BEEP/voice_female.ogg"

    # исключения - другие звуки для указанных персонажей

    # пример разбиения озвучки на мужские и женские псевдо-голоса
    # define beep = "BEEP/voice.ogg" - по умолчанию у всех женский голос,
    # осталось добавить псевдо-голос для всех мужиков игры и отключить озвучку рассказчика:
    # beep_other = { None: [ None ], "BEEP/voice_male.ogg": [ _("Петя"), _("Саша"), _("Мужик1"), _("Мужик2") ] }

    # можно добавить новых мужиков в процессе:
    # $ beep_other["BEEP/voice_male.ogg"].append(_("Серёжа"))

    # None: None - рассказчик молчит
    beep_other = { None: [ None ] }

    ## ДАЛЕЕ ЛУЧШЕ НИЧЕГО НЕ МЕНЯТЬ

    # канал для зацикленного эффекта
    renpy.music.register_channel("beep", "sfx", loop=True, tight=True)

    # писк при выводе текста
    def beep_callback(event, interact=True, what=None, **kwargs):
        # пищим, пока выводится текст
        if event == "show":
            b = beep

            # проверяем исключения
            for sound in beep_other.keys():
                ch = beep_other[sound]

                if not isinstance(ch, (list, tuple)): ch = [ ch ]

                # все персонажи, которые должны воспроизводить текущий звук
                for i in ch:
                    # если один из них совпадает со спикером, то меняем звук
                    if str(i) == str(renpy.last_say().who): b = sound

            # если звук задан, воспроизводим его
            if b: renpy.music.play(b, channel="beep")

        # останавливаемся на паузах и в конце
        elif event == "slow_done" or event == "end":
            renpy.music.stop(channel="beep", fadeout=.5)

init python:
    # назначаем новый общий для всех персонажей обработчик вывода текста
    config.character_callback = beep_callback
