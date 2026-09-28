## Цели Font Picker (dev/font_picker.rpy, F8): тексты sm_font_preview_text и стили,
## отмеченные на экране sm_font_preview_style. Вне developer-режима — обычный Text и Null.

init -5 python:

    ## python_dict — вне rollback и сейвов: примерка шрифта не игровое состояние.
    ## seen — стиль → время последнего показа: Font Picker правит только то, что на экране.
    _sm_font_override = python_dict(font=None, seen=python_dict())

    def _sm_font_mark(name):
        import time
        _sm_font_override["seen"][name] = time.time()

    def _sm_font_preview_f(st, at, text, kwargs):
        if "style" in kwargs:
            _sm_font_mark(kwargs["style"])
        kw = python_dict(kwargs)
        if _sm_font_override["font"]:
            kw["font"] = _sm_font_override["font"]
        return Text(text, **kw), 0.1

    def sm_font_preview_text(text, **kwargs):
        if not config.developer:
            return Text(text, **kwargs)
        return DynamicDisplayable(_sm_font_preview_f, text, kwargs)

    def _sm_font_style_f(st, at, name):
        _sm_font_mark(name)
        return Null(), 0.2

    def sm_font_preview_style(name):
        """Невидимая метка: стиль name сейчас на экране и доступен Font Picker."""
        if not config.developer:
            return Null()
        return DynamicDisplayable(_sm_font_style_f, name)
