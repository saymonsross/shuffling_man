default last_music_fn = ""

init -200 python:
    import math as sm_audio_math

    SM_AUDIO_CHANNELS = {
        line: tuple("sm_{}_{}".format(line, index) for index in range(5))
        for line in ("music", "voice", "sfx")
    }
    SM_AUDIO_ROUTES = {
        "music": "music", "voice": "voice", "sfx": "sfx",
        "audio": "sfx", "sound": "sfx", "effect": "sfx",
    }

    for _sm_line, _sm_channels in SM_AUDIO_CHANNELS.items():
        for _sm_channel in _sm_channels:
            renpy.music.register_channel(_sm_channel, mixer=_sm_line,
                loop=False, tight=True, synchro_start=False,
                stop_on_mute=False)
            config.main_menu_stop_channels.append(_sm_channel)
            if _sm_line == "voice":
                config.tts_voice_channels.append(_sm_channel)

    def _sm_audio_state():
        return getattr(renpy.context(), "sm_audio_state", (0, {}))

    def _sm_audio_store(serial, slots):
        # Contexts share nested values: replace snapshots so menus cannot mutate gameplay.
        renpy.context().sm_audio_state = (serial, slots)

    def _sm_audio_number(value, name, upper=None):
        value = float(value)
        if not sm_audio_math.isfinite(value) or value < 0 or (upper is not None and value > upper):
            raise ValueError("{} must be finite and in range".format(name))
        return value

    def _sm_audio_busy(channel):
        # get_playing includes pending queues; get_loop also covers restoration before playback.
        return bool(renpy.music.get_playing(channel=channel) or renpy.music.get_loop(channel=channel))

    def _sm_audio_matches(slot, group=None, tag=None, handle=()):
        return ((group is None or slot["group"] == group)
            and (tag is None or slot["tag"] == tag)
            and (handle == () or slot["handle"] == handle))

    def _sm_audio_play(files, group="sfx", tag=None, loop=False, fadein=0,
            fadeout=0, volume=1.0, overlap=False, if_changed=False):
        if group not in SM_AUDIO_ROUTES:
            raise ValueError("Unknown audio group: {}".format(group))
        if not files:
            return None
        filenames = (files,) if isinstance(files, str) else tuple(files)
        if not all(isinstance(name, str) and name for name in filenames):
            raise ValueError("Audio filenames must be nonempty strings")
        if tag is not None and not isinstance(tag, str):
            raise ValueError("Audio tag must be a string or None")
        fadein = _sm_audio_number(fadein, "fadein")
        fadeout = _sm_audio_number(config.fadeout_audio if fadeout is None else fadeout, "fadeout")
        volume = _sm_audio_number(volume, "volume", 1.0)
        if config.skipping and config.skip_sounds and not loop:
            return None

        line = SM_AUDIO_ROUTES[group]
        channels = SM_AUDIO_CHANNELS[line]
        serial, saved_slots = _sm_audio_state()
        slots = dict(saved_slots)
        matching = [channel for channel in channels if channel in slots
            and slots[channel]["active"] and slots[channel]["group"] == group
            and slots[channel]["tag"] == tag]
        matching.sort(key=lambda channel: slots[channel]["handle"][1], reverse=True)
        target = None
        if if_changed:
            target = next((channel for channel in matching
                if renpy.music.get_playing(channel=channel) in filenames), None)
        continuing = target is not None
        if target is None:
            target = next((channel for channel in channels if not _sm_audio_busy(channel)), None)
        if target is None:
            occupied = sorted(channels, key=lambda channel: slots.get(channel, {}).get("handle", (channel, -1))[1])
            target = next((channel for channel in occupied
                if channel in slots and not slots[channel]["active"]), None)
            if target is None:
                target = next((channel for channel in occupied
                    if channel in slots and not slots[channel]["loop"]), None)
            if target is None:
                if loop:
                    target = occupied[0]
                elif not overlap and matching:
                    target = matching[-1]
                else:
                    return None

        if not overlap:
            for channel in matching:
                if channel != target:
                    renpy.music.stop(channel=channel, fadeout=fadeout)
                    slots[channel] = dict(slots[channel], active=False)

        if continuing:
            handle = slots[target]["handle"]
        else:
            # A full pool must release its victim immediately, otherwise play queues behind its fade.
            renpy.music.stop(channel=target, fadeout=0)
            serial += 1
            handle = (target, serial)
        renpy.music.set_volume(volume, channel=target)
        renpy.music.play(list(filenames), channel=target, loop=loop,
            fadein=fadein, fadeout=0, synchro_start=False,
            if_changed=continuing, relative_volume=1.0)
        slots[target] = dict(channel=target, handle=handle, group=group,
            tag=tag, filenames=filenames, loop=bool(loop), active=True, volume=volume)
        _sm_audio_store(serial, slots)
        return handle

    def sm_audio_play(files, line="sfx", tag=None, loop=False, fadein=0,
            fadeout=0, volume=1.0, overlap=False, if_changed=False):
        if line not in SM_AUDIO_CHANNELS:
            raise ValueError("Unknown audio line: {}".format(line))
        return _sm_audio_play(files, line, tag, loop, fadein, fadeout,
            volume, overlap, if_changed)

    def _sm_audio_stop(group=None, line=None, tag=None, handle=(), fadeout=0):
        fadeout = _sm_audio_number(config.fadeout_audio if fadeout is None else fadeout, "fadeout")
        if line is not None and line not in SM_AUDIO_CHANNELS:
            raise ValueError("Unknown audio line: {}".format(line))
        serial, saved_slots = _sm_audio_state()
        slots = dict(saved_slots)
        for channel, slot in saved_slots.items():
            if line is not None and channel not in SM_AUDIO_CHANNELS[line]:
                continue
            if _sm_audio_matches(slot, group, tag, handle):
                renpy.music.stop(channel=channel, fadeout=fadeout)
                slots[channel] = dict(slot, active=False)
        _sm_audio_store(serial, slots)

    def sm_audio_stop(line=None, tag=None, handle=(), fadeout=0):
        _sm_audio_stop(line=line, tag=tag, handle=handle, fadeout=fadeout)

    def sm_audio_set_volume(handle, volume, delay=0):
        volume = _sm_audio_number(volume, "volume", 1.0)
        delay = _sm_audio_number(delay, "delay")
        serial, saved_slots = _sm_audio_state()
        slot = next((slot for slot in saved_slots.values() if slot["handle"] == handle), None)
        if slot is None or not _sm_audio_busy(slot["channel"]):
            return False
        renpy.music.set_volume(volume, delay=delay, channel=slot["channel"])
        slots = dict(saved_slots)
        slots[slot["channel"]] = dict(slot, volume=volume)
        _sm_audio_store(serial, slots)
        return True

    def sm_audio_snapshot(line=None):
        if line is not None and line not in SM_AUDIO_CHANNELS:
            raise ValueError("Unknown audio line: {}".format(line))
        serial, slots = _sm_audio_state()
        return tuple(dict(slot, playing=renpy.music.get_playing(channel=channel))
            for channel, slot in sorted(slots.items())
            if line is None or channel in SM_AUDIO_CHANNELS[line])

    def _sm_audio_legacy_play(files, channel="music", loop=False, fadein=0,
            fadeout=0, tag=None, overlap=None, volume=1.0, if_changed=False):
        if channel not in SM_AUDIO_ROUTES:
            renpy.music.play(files, channel=channel, loop=loop, fadein=fadein,
                fadeout=fadeout, relative_volume=volume, if_changed=if_changed)
            return None
        if overlap is None:
            overlap = channel == "audio"
        handle = _sm_audio_play(files, channel, tag, loop, fadein, fadeout,
            volume, overlap, if_changed)
        if handle is not None and not overlap and tag is None and channel in ("music", "sound", "effect", "voice"):
            renpy.music.stop(channel=channel, fadeout=fadeout)
        return handle

    def _sm_audio_legacy_stop(channel="music", fadeout=0, tag=None, handle=()):
        # None is a rejected play handle, while () means no handle filter was supplied.
        if handle is None:
            return
        if channel not in SM_AUDIO_ROUTES:
            renpy.music.stop(channel=channel, fadeout=fadeout)
            return
        _sm_audio_stop(group=channel, tag=tag, handle=handle, fadeout=fadeout)
        # Also clear legacy tracks restored from saves made before the pool existed.
        if tag is None and handle == () and channel not in ("audio", "sfx"):
            renpy.music.stop(channel=channel, fadeout=fadeout)

    def _sm_audio_legacy_playing(channel="music"):
        serial, slots = _sm_audio_state()
        matching = sorted((slot for slot in slots.values()
            if slot["group"] == channel and slot["active"]),
            key=lambda slot: slot["handle"][1], reverse=True)
        for slot in matching:
            playing = renpy.music.get_playing(channel=slot["channel"])
            if playing:
                return playing
        return renpy.music.get_playing(channel=channel)

    def vstop(fadeout=0, channel="voice", tag=None, handle=()):
        _sm_audio_legacy_stop(channel, fadeout, tag, handle)

    VStop = renpy.curry(vstop)
