## Persistent-флаги ниже относятся только к проектным эффектам и мини-играм.

default persistent.sm_reduce_motion = False
default persistent.sm_disable_flashes = False
default persistent.sm_simplified_locks = False
## Без мыши курсор прыгает к точке касания — там параллакс по умолчанию выключен.
default persistent.sm_parallax = bool(renpy.variant("pc") or renpy.variant("web"))

init -20 python:

    def sm_reduced_motion():
        return bool(getattr(persistent, "sm_reduce_motion", False))

    def sm_flashes_disabled():
        return bool(getattr(persistent, "sm_disable_flashes", False))

    def sm_motion_scale():
        return 0.0 if sm_reduced_motion() else 1.0

    def sm_motion_time(duration):
        return 0.0 if sm_reduced_motion() else duration

    def _sm_stationary_transition(effect, old_widget, new_widget):
        ## Длительность доступна только после создания перехода с обоими кадрами.
        original = effect(old_widget=old_widget, new_widget=new_widget)
        return Pause(max(0.0, float(original.delay)))(
            old_widget=old_widget, new_widget=new_widget)

    def sm_motion_transition(effect):
        """Сохраняет ритм перехода, но убирает движение камеры."""
        if sm_reduced_motion():
            return renpy.curry(_sm_stationary_transition)(effect)
        return effect
