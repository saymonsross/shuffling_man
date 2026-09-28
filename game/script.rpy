# Точка входа. Сценарий глав лежит в папках 0_prologue ... 4_endings;
# сцены связаны цепочкой jump, последняя сцена делает return в главное меню.

label start:

    ## Трек главного меню идёт на штатном канале music вне пула 7dots — обёртки его не видят.
    $ renpy.music.stop(channel="music", fadeout=3.0)

    jump prologue_titles
