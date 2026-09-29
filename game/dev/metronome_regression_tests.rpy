init python:
    def sm_test_metronome_filter(handle):
        if handle is None:
            return None
        return renpy.audio.audio.get_channel(handle[0]).context.raw_audio_filter

    def sm_test_metronome_playing(handle):
        filename = "audio/sfx/" + C1S1_METRONOME_LOOP_SOUND + ".wav"
        return (handle is not None
            and renpy.music.get_playing(channel=handle[0]) == filename
            and renpy.music.get_loop(channel=handle[0]) == [filename]
            and (renpy.music.get_pos(channel=handle[0]) or 0) > 0
            and any(row["handle"] == handle and row["active"]
                for row in sm_audio_snapshot("sfx")))


label sm_test_metronome_restore hide:
    $ sm_audio_stop()
    call screen sm_test_audio_checkpoint("metronome_ready")
    $ c1s1_metronome_audio = sfxplay(C1S1_METRONOME_LOOP_SOUND, ext="wav", fadein=0, fadeout=0, tag="c1s1_metronome", volume=C1S1_METRONOME_TICK_VOL)
    $ c1s1_metronome_tension()
    call screen sm_test_audio_checkpoint("metronome_filtered")
    $ sm_audio_set_filter(c1s1_metronome_audio, None, duration=0)
    call screen sm_test_audio_checkpoint("metronome_dry")
    return


testsuite sm_metronome_regression:
    before testcase:
        $ sm_test_audio_preferences_begin()
        run Function(dev_scene_nav_start, "sm_test_audio_idle")
        assert id "sm_audio_idle" timeout 5.0

    after testcase:
        $ sm_test_audio_preferences_end()
        if eval (not main_menu):
            run MainMenu(confirm=False)

    testcase loop_asset_phase:
        python hide:
            import wave
            with renpy.file("audio/sfx/" + C1S1_METRONOME_LOOP_SOUND + ".wav") as source:
                with wave.open(source, "rb") as sound:
                    assert sound.getsampwidth() == 2
                    rate = sound.getframerate()
                    ## Loop на две доли: «тик» на половине первой, «ток» — второй.
                    assert sound.getnframes() == round(2 * C1S1_ARROW_HALF_T * rate)
                    lead_frames = round(C1S1_ARROW_HALF_T * rate / 2.0)
                    assert not any(sound.readframes(lead_frames))
                    assert any(sound.readframes(max(1, round(rate * 0.02))))
                    assert any(sound.readframes(sound.getnframes()))

    testcase production_piano_knocks_and_reveal:
        run Function(dev_scene_nav_start, "chapter_1_scene_1")
        assert "Зажечь свет" timeout 8.0
        assert eval (c1s1_metronome_audio is None)
        click "Зажечь свет"
        assert "Завести метроном" timeout 15.0
        click "Завести метроном"
        assert eval (sm_test_metronome_playing(c1s1_metronome_audio)) timeout 5.0
        $ sm_test_audio_old = c1s1_metronome_audio
        assert eval (sm_test_metronome_filter(sm_test_audio_old) is None)

        assert eval (sprite_showed("chapter_1_piano_gg")) timeout 7.0
        assert eval (c1s1_metronome_audio == sm_test_audio_old and sm_test_metronome_playing(sm_test_audio_old))
        assert eval (sm_test_metronome_filter(sm_test_audio_old) is None)
        pause 1.0
        assert eval (sm_test_metronome_playing(sm_test_audio_old))
        assert eval (sprite_showed("chapter_1_piano_hand_left")) timeout 10.0
        assert eval (sm_test_metronome_filter(sm_test_audio_old) is None)
        assert eval (isinstance(sm_test_metronome_filter(sm_test_audio_old), renpy.audio.filter.Sequence)) timeout 8.0
        assert eval (sprite_showed("chapter_1_piano_hand_left") and c1s1_metronome_audio == sm_test_audio_old)
        assert eval (isinstance(renpy.audio.audio.get_channel(sm_test_audio_old[0]).context.audio_filter, renpy.audio.filter.Crossfade))
        assert eval (sm_test_metronome_playing(sm_test_audio_old))

        ## До первого стука маршрут идёт в реальном времени; механику замков проверяют отдельно.
        skip fast
        assert screen "c1s1_locks_open_door" timeout 15.0
        assert eval (c1s1_metronome_audio == sm_test_audio_old and sm_test_metronome_playing(sm_test_audio_old))
        assert eval (isinstance(sm_test_metronome_filter(sm_test_audio_old), renpy.audio.filter.Sequence))
        assert eval (len(tuple(row for row in sm_audio_snapshot("sfx") if row["active"] and row["tag"] == "c1s1_metronome")) == 1)
        click "Открыть дверь"
        assert screen "c1s1_locks_minigame" timeout 10.0
        assert eval (sm_test_metronome_playing(sm_test_audio_old))
        $ c1s1_mg_open_all()
        assert "Привет." timeout 10.0
        assert eval (c1s1_metronome_audio is None)
        assert eval (not any(row["active"] and row["tag"] == "c1s1_metronome" for row in sm_audio_snapshot("sfx")))
        assert eval (renpy.music.get_playing(channel=sm_test_audio_old[0]) is None) timeout 3.0
        assert eval (renpy.music.get_loop(channel=sm_test_audio_old[0]) is None)

    testcase late_skip_and_main_menu:
        run Function(dev_scene_nav_start, "chapter_1_scene_1")
        assert "Зажечь свет" timeout 8.0
        skip fast
        assert screen "c1s1_locks_open_door" timeout 15.0
        assert eval (sm_test_metronome_playing(c1s1_metronome_audio)) timeout 3.0
        assert eval (isinstance(sm_test_metronome_filter(c1s1_metronome_audio), renpy.audio.filter.Sequence))
        run MainMenu(confirm=False)
        assert eval (all(renpy.music.get_playing(channel=channel) is None and renpy.music.get_loop(channel=channel) is None for channel in SM_AUDIO_CHANNELS["sfx"])) timeout 3.0

    testcase filter_isolation_and_stale_handles:
        $ sm_test_audio_old = sm_audio_play("<silence 20.0>", tag="filtered", loop=True)
        assert eval (sm_test_audio_backend_ready(1, "sfx")) timeout 2.0
        python hide:
            assert sm_audio_set_filter(sm_test_audio_old, renpy.audio.filter.Lowpass(1200), duration=0)
            original = sm_test_metronome_filter(sm_test_audio_old)
            continuing = sm_audio_play("<silence 20.0>", tag="filtered", loop=True, if_changed=True)
            assert continuing == sm_test_audio_old
            assert sm_test_metronome_filter(continuing) is original
            other = sm_audio_play("<silence 21.0>", tag="dry", loop=True)
            assert sm_test_metronome_filter(other) is None
            assert sm_test_metronome_filter(sm_test_audio_old) is original
            sm_audio_stop(handle=sm_test_audio_old)
            assert not sm_audio_set_filter(sm_test_audio_old, None)
        assert eval (renpy.music.get_playing(channel=sm_test_audio_old[0]) is None) timeout 2.0
        python hide:
            reused = sm_audio_play("<silence 22.0>", tag="replacement", loop=True)
            assert reused[0] == sm_test_audio_old[0] and reused != sm_test_audio_old
            assert sm_test_metronome_filter(reused) is None
            assert not sm_audio_set_filter(sm_test_audio_old, renpy.audio.filter.Lowpass(600))
            assert not sm_audio_set_filter(None, renpy.audio.filter.Lowpass(600))
            assert sm_test_metronome_filter(reused) is None
        assert eval (sm_test_audio_backend_ready(2, "sfx")) timeout 2.0

    testcase filter_save_load_and_rollback:
        parameter restore_method = ["save", "rollback"]
        run Function(dev_scene_nav_start, "sm_test_metronome_restore")
        assert id "sm_audio_metronome_ready" timeout 5.0
        click id "sm_audio_metronome_ready"
        assert id "sm_audio_metronome_filtered" timeout 2.0
        assert eval (sm_test_metronome_playing(c1s1_metronome_audio)) timeout 2.0
        assert eval (isinstance(sm_test_metronome_filter(c1s1_metronome_audio), renpy.audio.filter.Sequence))
        if eval (restore_method == "save"):
            run Function(sm_test_cleanup_memory_save)
        click id "sm_audio_metronome_filtered"
        assert id "sm_audio_metronome_dry" timeout 2.0
        assert eval (sm_test_metronome_filter(c1s1_metronome_audio) is None)
        if eval (restore_method == "save"):
            run Function(sm_test_cleanup_memory_load)
        else:
            run Rollback()
        assert id "sm_audio_metronome_filtered" timeout 3.0
        assert eval (sm_test_metronome_playing(c1s1_metronome_audio)) timeout 2.0
        assert eval (isinstance(sm_test_metronome_filter(c1s1_metronome_audio), renpy.audio.filter.Sequence))
        assert eval ("_sm_cleanup_saved_game" not in renpy.session)
