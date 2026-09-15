default sm_test_audio_handles = ()
default sm_test_audio_old = None
default sm_test_audio_new = None

init python:
    def sm_test_audio_backend_ready(count, line=None):
        rows = tuple(row for row in sm_audio_snapshot(line) if row["active"])
        return len(rows) == count and all(
            renpy.music.get_playing(channel=row["channel"]) in row["filenames"]
            and (renpy.music.get_pos(channel=row["channel"]) or 0) > 0
            for row in rows)

    def sm_test_audio_preferences_begin():
        renpy.session["_sm_audio_preferences"] = tuple(
            (mixer, preferences.get_volume(mixer), preferences.get_mute(mixer))
            for mixer in ("main", "music", "voice", "sfx"))
        for mixer in ("main", "music", "voice", "sfx"):
            preferences.set_volume(mixer, 1.0)
            preferences.set_mute(mixer, False)

    def sm_test_audio_preferences_end():
        for mixer, volume, muted in renpy.session.pop("_sm_audio_preferences", ()):
            preferences.set_volume(mixer, volume)
            preferences.set_mute(mixer, muted)
        renpy.session.pop("_sm_audio_parent_state", None)
        renpy.session.pop("_sm_cleanup_saved_game", None)
        skip_stop()
        sm_audio_stop()


screen sm_test_audio_checkpoint(stage):
    modal True
    key "game_menu" action ShowMenu()
    textbutton _("Продолжить"):
        id "sm_audio_" + stage
        align (0.5, 0.5)
        action Return()
    textbutton _("Звук"):
        id "sm_audio_action"
        align (0.5, 0.65)
        action SFXPlay("click", fadein=0, fadeout=0, tag="action_probe", volume=0.0)


label sm_test_audio_idle hide:
    $ sm_audio_stop()
    call screen sm_test_audio_checkpoint("idle")
    return


label sm_test_audio_restore hide:
    $ sm_audio_stop()
    call screen sm_test_audio_checkpoint("ready")
    $ sm_test_audio_handles = (
        sm_audio_play("<silence 30.0>", line="music", tag="score", loop=True, volume=0.35),
        sm_audio_play("<silence 31.0>", tag="ambience", loop=True, volume=0.45),
        sm_audio_play("<silence 0.2>", line="voice", tag="line"))
    call screen sm_test_audio_checkpoint("first")
    $ sm_test_audio_handles = (
        sm_audio_play("<silence 32.0>", line="music", tag="score", loop=True),
        sm_audio_play("<silence 33.0>", tag="ambience", loop=True),
        sm_audio_play("<silence 34.0>", line="voice", tag="line"))
    call screen sm_test_audio_checkpoint("second")
    return


testsuite sm_audio_regression:
    before testcase:
        $ sm_test_audio_preferences_begin()
        run Function(dev_scene_nav_start, "sm_test_audio_idle")
        assert id "sm_audio_idle" timeout 5.0

    after testcase:
        $ sm_test_audio_preferences_end()
        if eval (not main_menu):
            run MainMenu(confirm=False)

    testcase simultaneous_channels_and_mixers:
        python hide:
            handles = []
            for line in ("music", "voice", "sfx"):
                for index in range(5):
                    handle = sm_audio_play("<silence 20.0>", line=line,
                        tag=str(index), loop=True)
                    assert handle is not None
                    assert handle[0] == "sm_{}_{}".format(line, index)
                    assert renpy.audio.audio.get_channel(handle[0]).mixer == line
                    assert handle[0] in config.main_menu_stop_channels
                    handles.append(handle)
            assert len(set(handles)) == 15
            assert len(sm_audio_snapshot()) == 15
            store.sm_test_audio_handles = tuple(handles)
        assert eval (sm_test_audio_backend_ready(15)) timeout 3.0
        python hide:
            for handle in sm_test_audio_handles:
                assert renpy.music.get_loop(channel=handle[0]) == ["<silence 20.0>"]
        run MainMenu(confirm=False)
        assert eval (all(renpy.music.get_playing(channel="sm_{}_{}".format(line, index)) is None for line in ("music", "voice", "sfx") for index in range(5))) timeout 2.0

    testcase crossfade_and_idle_reuse:
        $ sm_test_audio_old = sm_audio_play("<silence 20.0>", line="music", tag="score", loop=True)
        assert eval (sm_test_audio_backend_ready(1, "music")) timeout 2.0
        pause 0.15
        $ sm_test_audio_new = sm_audio_play("<silence 21.0>", line="music", tag="score", loop=True, fadein=1.0, fadeout=1.0)
        assert eval (sm_test_audio_old[0] != sm_test_audio_new[0])
        assert eval (renpy.music.get_playing(channel=sm_test_audio_old[0]) == "<silence 20.0>" and renpy.music.get_playing(channel=sm_test_audio_new[0]) == "<silence 21.0>" and (renpy.music.get_pos(channel=sm_test_audio_new[0]) or 0) > 0) timeout 0.6
        python hide:
            rows = {row["handle"]: row for row in sm_audio_snapshot("music")}
            assert not rows[sm_test_audio_old]["active"]
            assert rows[sm_test_audio_new]["active"]
            before = tuple(row["handle"] for row in sm_audio_snapshot("music"))
            sm_audio_play("<silence 21.0>", line="music", tag="score", loop=True, if_changed=True)
            assert tuple(row["handle"] for row in sm_audio_snapshot("music")) == before
        assert eval (renpy.music.get_playing(channel=sm_test_audio_old[0]) is None) timeout 2.0
        python hide:
            reused = sm_audio_play("<silence 22.0>", line="music", tag="other", loop=True)
            assert reused[0] == sm_test_audio_old[0]
            assert reused != sm_test_audio_old
            assert not sm_audio_set_volume(sm_test_audio_old, 0.1)
            assert sm_audio_set_volume(reused, 0.25)
            sm_audio_stop(handle=sm_test_audio_old)
            rows = {row["handle"]: row for row in sm_audio_snapshot("music")}
            assert rows[reused]["active"] and rows[reused]["volume"] == 0.25
        assert eval (sm_test_audio_backend_ready(2, "music")) timeout 2.0

    testcase capacity_and_stale_handles:
        python hide:
            handles = tuple(sm_audio_play("<silence 20.0>", tag=str(index), overlap=True)
                for index in range(5))
            replacement = sm_audio_play("<silence 21.0>", tag="sixth", overlap=True)
            assert replacement[0] == handles[0][0] and replacement != handles[0]
            assert not sm_audio_set_volume(handles[0], 0.1)
            sm_audio_stop(handle=handles[0])
            assert len(tuple(row for row in sm_audio_snapshot("sfx") if row["active"])) == 5
            sm_audio_stop()
            handles = tuple(sm_audio_play("<silence 22.0>", tag=str(index), loop=True)
                for index in range(5))
            assert sm_audio_play("<silence 23.0>", tag="drop", overlap=True) is None
            sm_audio_stop(handle=None)
            assert tuple(row["handle"] for row in sm_audio_snapshot("sfx")) == handles
            assert all(row["active"] for row in sm_audio_snapshot("sfx"))
            replacement = sm_audio_play("<silence 24.0>", tag="new_loop", loop=True)
            assert replacement[0] == handles[0][0] and replacement != handles[0]
            assert not sm_audio_set_volume(handles[0], 0.1)
            store.sm_test_audio_old = handles[1]
            store.sm_test_audio_new = replacement
        assert eval (sm_test_audio_backend_ready(5, "sfx")) timeout 2.0
        $ sm_audio_stop(handle=sm_test_audio_old, fadeout=2.0)
        $ sm_test_audio_new = sm_audio_play("<silence 25.0>", tag="tail_replacement")
        assert eval (sm_test_audio_new[0] == sm_test_audio_old[0] and sm_test_audio_new != sm_test_audio_old)
        assert eval (sm_test_audio_backend_ready(5, "sfx")) timeout 2.0

    testcase wrappers_and_group_stops:
        python hide:
            # Старые сейвы могут содержать музыку на штатных каналах до миграции.
            for channel in ("music", "sound", "effect", "voice"):
                renpy.music.play("<silence 20.0>", channel=channel, loop=True)
            first = splay("click", volume=0.0)
            second = splay("click", volume=0.0)
            sound = sndplay("click", volume=0.0)
            effect = sfxplay("click", fadein=0, fadeout=0, volume=0.0)
            voice = vplay("click", voice_dir="audio/sfx", volume=0.0)
            music = mplay("shuffling_man_piano_source", ext="mp3", fadein=0, fadeout=0, volume=0.0)
            rows = {row["handle"]: row for row in sm_audio_snapshot()}
            assert first[0] != second[0]
            for handle, group in ((first, "audio"), (second, "audio"), (sound, "sound"), (effect, "effect"), (voice, "voice")):
                assert rows[handle]["group"] == group
                assert rows[handle]["filenames"] == ("audio/sfx/click.ogg",)
            assert rows[music]["filenames"] == ("audio/music/shuffling_man_piano_source.mp3",)
            assert all(renpy.music.get_loop(channel=channel) is None for channel in ("music", "sound", "effect", "voice"))
            sfxstop(handle=None)
            rows = {row["handle"]: row for row in sm_audio_snapshot()}
            assert rows[effect]["active"]
            sstop(fadeout=0)
            rows = {row["handle"]: row for row in sm_audio_snapshot()}
            assert not any(row["active"] and row["group"] == "audio" for row in rows.values())
            assert rows[sound]["active"] and rows[effect]["active"] and rows[voice]["active"]
            sndstop()
            rows = {row["handle"]: row for row in sm_audio_snapshot()}
            assert rows[effect]["active"]
            vstop()
            store.sm_test_audio_handles = (music, effect)
        assert eval (sm_test_audio_backend_ready(2)) timeout 2.0
        $ msave()
        assert eval (last_music_fn == "audio/music/shuffling_man_piano_source.mp3")
        $ mstop(fadeout=0)
        $ mrestore(fadein=0, fadeout=0)
        assert eval (sm_test_audio_backend_ready(2)) timeout 2.0
        $ sfxstop(fadeout=0)
        assert eval (sm_test_audio_backend_ready(1, "music")) timeout 2.0
        assert eval (not any(row["active"] for row in sm_audio_snapshot("sfx")))
        click id "sm_audio_action"
        assert id "sm_audio_idle"
        assert eval (sm_test_audio_backend_ready(1, "sfx")) timeout 2.0

    testcase mute_and_skip:
        $ preferences.set_mute("sfx", True)
        $ sm_test_audio_old = sm_audio_play("<silence 20.0>", tag="muted_loop", loop=True)
        pause 0.15
        assert eval (renpy.music.get_loop(channel=sm_test_audio_old[0]) == ["<silence 20.0>"])
        assert eval (any(row["handle"] == sm_test_audio_old and row["active"] for row in sm_audio_snapshot("sfx")))
        $ preferences.set_mute("sfx", False)
        assert eval (sm_test_audio_backend_ready(1, "sfx")) timeout 2.0
        python hide:
            skipping = config.skipping
            skip_sounds = config.skip_sounds
            try:
                config.skip_sounds = True
                for mode in ("normal", "fast"):
                    config.skipping = mode
                    assert sm_audio_play("<silence 21.0>", tag="skip_transient") is None
                    assert splay("click") is None
                    assert vplay("click", voice_dir="audio/sfx") is None
                    assert sm_audio_play("<silence 22.0>", line="music", tag="skip_loop", loop=True) is not None
            finally:
                config.skipping = skipping
                config.skip_sounds = skip_sounds
        assert eval (sm_test_audio_backend_ready(1, "music")) timeout 2.0

    testcase menu_context_isolation:
        $ sm_test_audio_old = sm_audio_play("<silence 20.0>", line="music", tag="score", loop=True)
        assert eval (sm_test_audio_backend_ready(1, "music")) timeout 2.0
        $ renpy.session["_sm_audio_parent_state"] = renpy.context().sm_audio_state
        run ShowMenu("preferences")
        assert screen "preferences" timeout 2.0
        $ sm_audio_play("<silence 21.0>", line="music", tag="menu", loop=True)
        assert eval (renpy.context().sm_audio_state is not renpy.session["_sm_audio_parent_state"])
        $ sm_audio_stop(line="music", tag="score")
        assert eval (not any(row["active"] and row["tag"] == "score" for row in sm_audio_snapshot("music")))
        keysym "game_menu"
        assert id "sm_audio_idle" timeout 2.0
        assert eval (renpy.context().sm_audio_state is renpy.session["_sm_audio_parent_state"])
        assert eval (sm_test_audio_backend_ready(1, "music")) timeout 2.0
        assert eval (renpy.music.get_playing(channel=sm_test_audio_old[0]) == "<silence 20.0>")
        assert eval (not any(row["active"] and row["tag"] == "menu" for row in sm_audio_snapshot("music")))

    testcase save_load_and_rollback:
        parameter restore_method = ["save", "rollback"]
        run Function(dev_scene_nav_start, "sm_test_audio_restore")
        assert id "sm_audio_ready" timeout 5.0
        click id "sm_audio_ready"
        assert id "sm_audio_first" timeout 2.0
        assert eval (sm_test_audio_backend_ready(1, "music") and sm_test_audio_backend_ready(1, "sfx")) timeout 2.0
        assert eval (all(renpy.music.get_playing(channel="sm_voice_" + str(index)) is None for index in range(5))) timeout 2.0
        if eval (restore_method == "save"):
            run Function(sm_test_cleanup_memory_save)
        click id "sm_audio_first"
        assert id "sm_audio_second" timeout 2.0
        assert eval (sm_test_audio_backend_ready(1, "voice")) timeout 2.0
        assert eval (renpy.music.get_playing(channel=sm_test_audio_handles[0][0]) == "<silence 32.0>") timeout 2.0
        if eval (restore_method == "save"):
            run Function(sm_test_cleanup_memory_load)
        else:
            run Rollback()
        assert id "sm_audio_first" timeout 3.0
        assert eval (renpy.music.get_playing(channel=sm_test_audio_handles[0][0]) == "<silence 30.0>") timeout 2.0
        assert eval (renpy.music.get_playing(channel=sm_test_audio_handles[1][0]) == "<silence 31.0>") timeout 2.0
        assert eval (all(renpy.music.get_playing(channel="sm_voice_" + str(index)) is None for index in range(5))) timeout 2.0
        python hide:
            rows = {row["tag"]: row for row in sm_audio_snapshot() if row["active"]}
            assert rows["score"]["volume"] == 0.35
            assert rows["ambience"]["volume"] == 0.45
            assert renpy.music.get_loop(channel=rows["score"]["channel"]) == ["<silence 30.0>"]
            assert renpy.music.get_loop(channel=rows["ambience"]["channel"]) == ["<silence 31.0>"]
            assert "_sm_cleanup_saved_game" not in renpy.session
            assert not config.save and not config.save_persistent
