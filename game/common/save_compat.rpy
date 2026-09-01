## Миграция сохранений между внутренними версиями проекта.

label after_load:
    ## Старые save не хранили прогресс замка: продолжаем с начала текущего.
    if c1s1_mg_knocking:
        $ c1s1_mg_ensure_state()
        $ c1s1_mg_sync_pointer_after_context()
        $ _mg_set("clock", sm_time.monotonic())
        show screen c1s1_mg_runtime
        ## Миграция не должна откатываться к устаревшему grab/clock.
        $ renpy.block_rollback()

    return
