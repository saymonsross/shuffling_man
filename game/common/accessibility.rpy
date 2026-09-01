## Persistent-флаги ниже относятся только к проектным эффектам и мини-играм.

default persistent.sm_reduce_motion = False
default persistent.sm_disable_flashes = False
default persistent.sm_simplified_locks = False

init -20 python:

    def sm_reduced_motion():
        return bool(getattr(persistent, "sm_reduce_motion", False))

    def sm_flashes_disabled():
        return bool(getattr(persistent, "sm_disable_flashes", False))

    def sm_motion_scale():
        return 0.0 if sm_reduced_motion() else 1.0

    def sm_motion_time(duration):
        return 0.0 if sm_reduced_motion() else duration

    def sm_motion_transition(effect):
        """Сохраняет ритм перехода, но убирает движение камеры."""
        if sm_reduced_motion():
            return Pause(max(0.0, float(effect.delay)))
        return effect
