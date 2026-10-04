## Озвучка реплик через пул sm_voice_* ради кроссфейда (docs/03_audio_system.md).
## Отбор реплики — штатный (SDK 00voice.rpy); заменены только воспроизведение,
## остановка и проверка «голос звучит».

## Время затухания остановленной реплики (кроме пропуска), с.
define SM_VOICE_FADEOUT = 0.3
## Слой реплик в группе voice: ручной vplay без tag их не заменяет и не останавливает.
define SM_VOICE_TAG = "_say"

## Реверб на канале реплики; хвост гаснет вместе с репликой, файлы остаются сухими.
init -10 python:

    fx_param("voice_reverb.enabled", True, doc="включить реверб озвучки")
    fx_param("voice_reverb.wet", 0.18, 0.0, 1.0, step=0.01, doc="громкость реверба поверх сухого голоса")
    fx_param("voice_reverb.resonance", 0.5, 0.0, 0.9, step=0.01, doc="длина хвоста; ближе к 0.9 — дольше")
    fx_param("voice_reverb.size", 1.0, 0.3, 3.0, step=0.05, doc="размер комнаты: множитель задержек отражений")
    fx_param("voice_reverb.dampening", 3000.0, 300.0, 12000.0, step=100.0, doc="срез верхов хвоста, Гц; меньше — глуше")
    fx_group("voice_reverb", "Реверб озвучки")

init -190 python:

    def _sm_voice_playing():
        ## Каналы пула доигрывают при mute беззвучно; штатный канал voice при mute
        ## останавливался, и автопереход не ждал голос — сохраняем это.
        if _preferences.mute.get("voice", False):
            return False
        serial, slots = _sm_audio_state()
        return any(slot["group"] == "voice" and slot["tag"] == SM_VOICE_TAG
            and slot["active"] and _sm_audio_busy(channel)
            for channel, slot in slots.items())

    def _sm_voice_volume():
        info = _voice.info
        return persistent._character_volume.get(info.tag if info is not None else None, 1.0)

    def _sm_voice_filter():
        if not fx_cfg("voice_reverb.enabled") or fx_cfg_bypassed():
            return None
        return renpy.audio.filter.Reverb(
            resonance=fx_cfg("voice_reverb.resonance"),
            dampening=fx_cfg("voice_reverb.dampening"),
            wet=fx_cfg("voice_reverb.wet"), dry=1.0,
            delay_multiplier=fx_cfg("voice_reverb.size"))

    ## Пул сбрасывает фильтр канала при каждом запуске, поэтому реверб ставится заново;
    ## правка в FX Tuner слышна со следующей реплики.
    def _sm_voice_play(filename, volume):
        handle = _sm_audio_play(filename, "voice", tag=SM_VOICE_TAG,
            fadeout=SM_VOICE_FADEOUT, volume=volume)
        if handle is not None:
            sm_audio_set_filter(handle, _sm_voice_filter(), duration=0)
        return handle

    def _sm_voice_stop(fadeout):
        _sm_audio_stop(group="voice", tag=SM_VOICE_TAG, fadeout=fadeout)

    ## Копия voice_interact из Ren'Py 8.5.3 renpy/common/00voice.rpy:
    ## renpy.sound.play/stop на канале "voice" заменены пулом.
    def _sm_voice_interact():

        if not config.has_voice:
            return

        if _voice.ignore_interaction:
            return

        mode = renpy.get_mode()

        if (mode is None) or (mode == "with"):
            return

        if getattr(renpy.context(), "_menu", False) and not _preferences.voice_after_game_menu:
            _sm_voice_stop(SM_VOICE_FADEOUT)
            _invoke_voice_callbacks("stop")
            _voice.playing_info = None
            return

        if _preferences.voice_sustain and not _voice.sustain:
            _voice.sustain = "preference"

        if _voice.play:
            _voice.sustain = False

        vi = VoiceInfo()

        if not _voice.sustain:
            _voice.info = vi

        if not vi.sustain:
            _voice.play = vi.filename
        else:
            _voice.play = None

        _voice.auto_file = vi.auto_filename
        _voice.sustain = vi.sustain
        _voice.tlid = vi.tlid

        volume = persistent._character_volume.get(_voice.tag, 1.0)

        if (not volume) or (_voice.tag in persistent._voice_mute):
            _sm_voice_stop(SM_VOICE_FADEOUT)
            _invoke_voice_callbacks("stop")
            store._last_voice_play = _voice.play
            _voice.playing_info = None

        elif _voice.play:
            if not config.skipping:
                renpy.stop_tts()
                _sm_voice_play(_voice.play, volume)
                _invoke_voice_callbacks("stop")
                _voice.playing_info = vi
                _invoke_voice_callbacks("play")

            store._last_voice_play = _voice.play

        elif not _voice.sustain and not (getattr(renpy.context(), "_menu", False) and _preferences.voice_after_game_menu):
            _sm_voice_stop(SM_VOICE_FADEOUT)
            _invoke_voice_callbacks("stop")
            _voice.playing_info = None

            if not getattr(renpy.context(), "_menu", False):
                store._last_voice_play = None

        if config.skipping:
            _sm_voice_stop(config.fadeout_audio)
            _invoke_voice_callbacks("stop")

        _voice.play = None
        _voice.sustain = False
        _voice.tag = None

    def _sm_voice_periodic():
        if _voice.playing_info is not None and not _sm_voice_playing():
            _invoke_voice_callbacks("stop")
            _voice.playing_info = None

    def _sm_voice_afm_callback():
        if _sm_voice_playing():
            _voice.last_playing = renpy.time.time()

        if _preferences.wait_voice:
            return renpy.time.time() > (_voice.last_playing + config.afm_voice_delay)
        else:
            return True

    def voice_replay():
        if _last_voice_play is not None:
            _sm_voice_play(_last_voice_play, _sm_voice_volume())

    def _sm_voice_swap(callbacks, names, replacement):
        ## Замена на месте сохраняет порядок колбэков; свои имена в names делают её
        ## идемпотентной при повторном init (autoreload).
        swapped = [replacement if getattr(callback, "__name__", None) in names else callback
            for callback in callbacks]
        if replacement not in swapped:
            raise Exception("SDK voice callback not found: {}".format(sorted(names)))
        callbacks[:] = swapped

    _sm_voice_swap(config.start_interact_callbacks,
        {"voice_interact", "_sm_voice_interact"}, _sm_voice_interact)
    _sm_voice_swap(config.fast_skipping_callbacks,
        {"voice_interact", "_sm_voice_interact"}, _sm_voice_interact)
    _sm_voice_swap(config.nointeract_callbacks,
        {"voice_interact", "_sm_voice_interact"}, _sm_voice_interact)
    _sm_voice_swap(config.periodic_callbacks,
        {"_voice_periodic_callback", "_sm_voice_periodic"}, _sm_voice_periodic)
    config.afm_callback = _sm_voice_afm_callback
