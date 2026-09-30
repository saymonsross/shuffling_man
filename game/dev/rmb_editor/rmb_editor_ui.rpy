## RMB EDITOR · жест, пауза и поле ввода (dev-only)
## Логика запроса — в rmb_editor.rpy; строки намеренно не локализуются.

define -30 RMB_PANEL_W = 760
## Высота панели без вложений — для выбора, куда ей расти от точки клика.
define -30 RMB_PANEL_H = 220
define -30 RMB_PANEL_GAP = 16
define -30 RMB_PANEL_MARGIN = 20

## Задержка отложенного открытия: за это время рисуется хотя бы один кадр.
define -30 RMB_DEFER_DELAY = 0.05


init -20 python:

    import pygame_sdl2 as _rmb_pygame

    ## EVENTNAME — события геймпада и renpy.queue_event: движок превращает их в имена keymap.
    _RMB_SINK_TYPES = (
        _rmb_pygame.KEYDOWN, _rmb_pygame.KEYUP, _rmb_pygame.TEXTINPUT, _rmb_pygame.TEXTEDITING,
        _rmb_pygame.MOUSEBUTTONDOWN, _rmb_pygame.MOUSEBUTTONUP, _rmb_pygame.MOUSEWHEEL,
        renpy.display.core.EVENTNAME)

    ## active — контекст поля сейчас исполняется. Перезагрузка скриптов сбрасывает его сама,
    ## а rmb_data()["open"] её переживает: по расхождению видно, что поле надо вернуть.
    _rmb_run = python_dict(active=False, pending=False, shot=None)

    def _rmb_shift():
        if _rmb_override["shift"] is not None:
            return _rmb_override["shift"]
        ## ev.mod события мыши устаревает при смене фокуса окна — читаем клавиатуру.
        return bool(_rmb_pygame.key.get_mods() & _rmb_pygame.KMOD_SHIFT)

    def _rmb_field_interact(layers):
        ## Очистка слоя не сбрасывает его camera: без этого function-трансформы камеры
        ## продолжали бы исполняться над пустым слоем и двигать своё состояние.
        for layer in layers:
            renpy.show_layer_at((), layer=layer, reset=True, camera=True)
            renpy.show_layer_at((), layer=layer, reset=True)
        renpy.show_screen("rmb_editor_field")
        return renpy.ui.interact(mouse="screen", type="screen", suppress_overlay=True)

    def _rmb_enter():
        """Поле живёт в новом контексте: это штатная пауза движка, как под игровым меню."""
        d = rmb_data()
        keep = False
        sent = False
        _rmb_run["active"] = True
        try:
            ## Очищаются все слои, а не только context_clear_layers: иначе копии слоёв сцены
            ## продолжали бы исполняться под фоном. Сквозные config.layer_transforms (параллакс,
            ## постеризация) остаются — как и под игровым меню.
            layers = tuple(config.layers) + tuple(config.top_layers) + tuple(config.bottom_layers)
            sent = renpy.invoke_in_new_context(_rmb_field_interact, layers, _clear_layers=layers)
        except renpy.game.UtterRestartException:
            ## Перезагрузка скриптов: признак «открыто» остаётся, поле вернётся после неё.
            keep = True
            raise
        finally:
            _rmb_run["active"] = False
            if not keep:
                d["open"] = False
        ## renpy.notify показывает экран в текущем контексте: внутри поля он исчез бы вместе с ним.
        if sent:
            renpy.notify("отправлено в VS Code")

    def rmb_open(x=None, y=None, files=()):
        ## _reload_slot лежит в сессии, пока идёт кадр «Reloading game...».
        if _rmb_run["active"] or "_reload_slot" in renpy.session:
            return
        if rmb_data()["open"]:
            ## Поле ещё не вернулось после перезагрузки скриптов: черновик не затирается.
            for path in files:
                rmb_add_file(path)
        else:
            rmb_begin(x, y, files)
        _rmb_enter()

    def rmb_open_from_hub():
        ## Скриншот — последний отрисованный кадр: поле откроется, когда хаб уже скрыт.
        _rmb_run["pending"] = True
        renpy.restart_interaction()

    def rmb_deferred_due():
        if _rmb_run["active"] or "_reload_slot" in renpy.session:
            return False
        return _rmb_run["pending"] or bool(rmb_data()["open"])

    def rmb_deferred():
        if not rmb_deferred_due():
            return
        _rmb_run["pending"] = False
        rmb_open()

    def rmb_backdrop():
        """Застывший кадр момента клика — тот же файл, что уходит в запрос."""
        d = rmb_data()
        path = _rmb_os.path.join(d["dir"], "shot.png") if d["dir"] else None
        if _rmb_run["shot"] is not None and _rmb_run["shot"][0] == path:
            return _rmb_run["shot"][1]
        shot = Solid("#000")
        try:
            ## Картинку вне game/ движок по пути не загружает.
            with _rmb_io.open(path, "rb") as f:
                shot = Transform(im.Data(f.read(), path), xysize=(config.screen_width, config.screen_height))
        except Exception:
            pass
        _rmb_run["shot"] = (path, shot)
        return shot

    def rmb_panel_place():
        """(pos, yanchor): панель растёт вниз от точки в верхней половине экрана и вверх — в нижней,
        поэтому с вложениями и длинным текстом не уходит за край."""
        ctx = rmb_data()["ctx"]
        point = ctx["point"] if ctx else None
        if not point:
            return ((int(round((config.screen_width - RMB_PANEL_W) / 2.0)),
                     int(round(config.screen_height / 2.0))), 0.5)
        x = min(max(point[0] + RMB_PANEL_GAP, RMB_PANEL_MARGIN),
                config.screen_width - RMB_PANEL_W - RMB_PANEL_MARGIN)
        if point[1] <= config.screen_height // 2:
            return ((int(x), int(max(point[1] + RMB_PANEL_GAP, RMB_PANEL_MARGIN))), 0.0)
        y = max(min(point[1] - RMB_PANEL_GAP, config.screen_height - RMB_PANEL_MARGIN), RMB_PANEL_H)
        return ((int(x), int(y)), 1.0)


init -20 python:

    class RMBCatcher(renpy.Displayable):

        def render(self, width, height, st, at):
            return renpy.Render(width, height)

        def event(self, ev, x, y, st):
            if ev.type == _rmb_pygame.MOUSEBUTTONUP and ev.button == 3 and _rmb_shift():
                rmb_open(x, y)
                ## Keysym mouseup_3 у game_menu и button_alternate совпадает и с Shift+ПКМ.
                raise renpy.IgnoreEvent()

            if ev.type == _rmb_pygame.DROPFILE:
                path = getattr(ev, "file", None)
                if path:
                    if _rmb_run["active"]:
                        rmb_add_file(path)
                        renpy.restart_interaction()
                    else:
                        ## Событие не несёт координат: бросок прикрепляет, а не указывает место.
                        rmb_open(files=(path,))
                raise renpy.IgnoreEvent()

            return None

    class RMBSink(renpy.Displayable):
        """Гасит клавиши и клики, не взятые полем: always-shown контроллеры хоткеев и underlay
        есть и в контексте поля. DROPFILE и события времени идут дальше."""

        def render(self, width, height, st, at):
            return renpy.Render(width, height)

        def event(self, ev, x, y, st):
            if ev.type in _RMB_SINK_TYPES:
                raise renpy.IgnoreEvent()
            return None


init -10 python:
    rmb_catcher = RMBCatcher()
    rmb_sink = RMBSink()


screen rmb_editor_field():

    layer "top"
    zorder RMB_FIELD_ZORDER

    ## События раздаются от последнего ребёнка к первому: поглотитель стоит первым.
    add rmb_sink
    add rmb_backdrop()

    $ rmb_d = rmb_data()
    $ rmb_pos, rmb_yanchor = rmb_panel_place()

    frame:
        style "rmb_panel"
        pos rmb_pos
        yanchor rmb_yanchor
        xsize RMB_PANEL_W

        vbox:
            spacing 8

            text ("→ CLAUDE · " + _dev_hub_quote(rmb_summary(rmb_d["ctx"]))) style "rmb_head" substitute False

            ## Вложения стоят выше поля: дети получают события с конца, и Enter при курсоре
            ## на кнопке «×» иначе нажимал бы её (button_select), а не отправлял запрос.
            for i, path in enumerate(rmb_d["files"]):
                hbox:
                    spacing 8
                    textbutton "×" style "rmb_button" action Function(rmb_remove_file, i)
                    text _dev_hub_quote(path) style "rmb_file" substitute False yalign 0.5

            frame:
                style "rmb_card"
                input:
                    style "rmb_input"
                    value DictInputValue(rmb_d, "text")
                    multiline True
                    copypaste True
                    action Function(rmb_send)

            if rmb_d["error"]:
                text _dev_hub_quote(rmb_d["error"]) style "rmb_error" substitute False

            text "Enter — во вкладку VS Code · Shift+Enter — новая строка · Esc — отмена · файл можно бросить на окно" style "rmb_hint"

    key "K_ESCAPE" action Function(rmb_cancel)


screen rmb_editor_catcher():

    layer "top"
    zorder RMB_CATCHER_ZORDER

    add rmb_catcher

    ## Новый контекст открывается только из обработчика события, не из кода экрана.
    if rmb_deferred_due():
        timer RMB_DEFER_DELAY action Function(rmb_deferred)

init python:
    if config.developer:
        config.always_shown_screens.append("rmb_editor_catcher")
        ## Ren'Py блокирует события SDL не из своего списка; этот список читается один раз
        ## при запуске, поэтому бросок файла заработает после полного перезапуска игры.
        config.pygame_events.append(_rmb_pygame.DROPFILE)


style rmb_panel is frame:
    background "#0b0b0bf0"
    padding (18, 14)

style rmb_card is frame:
    background "#ffffff14"
    padding (10, 8)
    xfill True
    yminimum 96

## Шрифт движка, а не игровой gui.text_font: служебная панель читается одинаково
## при любом оформлении игры.
style rmb_text is text:
    font "DejaVuSans.ttf"

style rmb_head is rmb_text:
    size 15
    color "#9fffcf"

style rmb_input is rmb_text:
    size 20
    color "#ffffff"

style rmb_file is rmb_text:
    size 14
    color "#cccccc"

style rmb_error is rmb_text:
    size 14
    color "#ff6666"

style rmb_hint is rmb_text:
    size 13
    color "#999999"

style rmb_button is button:
    padding (8, 2)
    background "#ffffff18"
    hover_background "#ffffff33"

style rmb_button_text is button_text:
    font "DejaVuSans.ttf"
    size 15
    color "#dddddd"
    hover_color "#ffffff"
