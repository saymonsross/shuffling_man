## Сценовые действия: menu(screen="scene_choice"). Каждый пункт — glow_button,
## аргументы пункта меню уходят в него (pos, size, bg, hovered...).
## Под кнопками — разлом сцены (common/rift.rpy).
## follow — трансформ мирового контейнера; skippable — поздний пропуск выбирает
## первый пункт, только для меню без развилки.

init -5 python:
    ## Позиции, перетащенные Choice Placer (dev/choice_placer.rpy) в этой сессии:
    ## (файл и строка menu, подпись) → pos. В релизе словарь пуст.
    _sm_choice_moved = {}

    def sm_choice_kwargs(where, item):
        pos = _sm_choice_moved.get((where, item.caption))
        if pos is None:
            return item.kwargs
        kwargs = dict(item.kwargs)
        kwargs["pos"] = pos
        return kwargs

screen scene_choice(items, follow=None, skippable=False):
    modal True
    $ _sc_where = renpy.get_filename_line()
    $ _sc_placing = config.developer and renpy.get_screen("dev_choice_placer") is not None

    ## SkipOnce здесь нельзя: menu примет его True за индекс пункта 1.
    if skippable and renpy.is_skipping():
        timer 0.01 action items[0].action modal True

    fixed:
        id "world"
        at (follow if follow is not None else [])
        xysize (config.screen_width, config.screen_height)
        for i in items:
            if _sc_placing:
                use dev_choice_drag(i, _sc_where)
            else:
                use glow_button(i.caption, i.action, rift=("follow" if follow is not None else "screen"), **sm_choice_kwargs(_sc_where, i))
