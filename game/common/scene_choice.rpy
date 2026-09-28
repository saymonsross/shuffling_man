## Сценовые действия: menu(screen="scene_choice"). Каждый пункт — glow_button,
## аргументы пункта меню уходят в него (pos, size, bg, hovered...).
## follow — трансформ мирового контейнера; skippable — поздний пропуск выбирает
## первый пункт, только для меню без развилки.

screen scene_choice(items, follow=None, skippable=False):
    modal True

    ## SkipOnce здесь нельзя: menu примет его True за индекс пункта 1.
    if skippable and renpy.is_skipping():
        timer 0.01 action items[0].action modal True

    fixed:
        id "world"
        at (follow if follow is not None else [])
        xysize (config.screen_width, config.screen_height)
        for i in items:
            use glow_button(i.caption, i.action, **i.kwargs)
