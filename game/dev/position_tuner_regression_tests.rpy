## Запись Position Tuner в код: разбор show-строки и переписывание литералов без файлов.
testcase pt_write_rewrite:
    python hide:
        t = PTTarget("prologue_note_paper", {"pos": (990, 455), "anchor": (0.5, 0.5), "rotate": None, "natural": (10, 10), "bounds": None, "zoom": 1.0, "alpha": 1.0, "from_scene": True})
        t.pos = (1000, 460)
        assert _pt_show_matches("    show prologue_note_paper at placed((990, 455), (0.5, 0.5))\r\n", t)
        assert not _pt_show_matches("    show prologue_note_pencil at placed((990, 455))\n", t)
        new, why = _pt_rewrite_call("placed((990, 455), (0.5, 0.5))", PT_WRITE_CALLS["placed"], t)
        assert new == "placed((1000, 460), (0.5, 0.5))", (new, why)

        t.anchor, t.rotate = (0.0, 1.0), 12.5
        new, why = _pt_rewrite_call("placed((990, 455))", PT_WRITE_CALLS["placed"], t)
        assert new == "placed((1000, 460), anchor_xy=(0.0, 1.0), angle=12.5)", (new, why)

        new, why = _pt_rewrite_call("placed(C1S1_DOOR_BAG_POS)", PT_WRITE_CALLS["placed"], t)
        assert new is None and why == "pos не литерал"
        new, why = _pt_rewrite_call("placed((1, 2))", PT_WRITE_CALLS["placed"], t)
        assert new is None

        bag = PTTarget("chapter_1_hall_door_bag", {"pos": (0, 1080), "anchor": (0.0, 1.0), "rotate": None, "natural": (10, 10), "bounds": None, "zoom": 1.0, "alpha": 1.0, "from_scene": True})
        bag.pos = (4, 1070)
        new, why = _pt_rewrite_call('placed_jitter((0, 1080), anchor_xy=(0.0, 1.0), jitter_amp=2.0, jitter_key="bag")', PT_WRITE_CALLS["placed_jitter"], bag)
        assert new == "placed_jitter((4, 1070), anchor_xy=(0.0, 1.0), jitter_amp=2.0, jitter_key='bag')", (new, why)

        hand = PTTarget("c1s1_hand_metronome", {"pos": (0, 0), "anchor": (0.0, 0.0), "rotate": None, "natural": (1, 1), "bounds": None, "zoom": 1.0, "alpha": 1.0, "from_scene": True})
        assert _pt_show_matches("    show chapter_1_lamp_hand light_metronome as c1s1_hand_metronome zorder 15 at placed((0, 0))\n", hand)
