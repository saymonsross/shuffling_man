init python:
    def sm_test_tv_assert_scene(image_name, pos, size, displayable=None, animated=None):
        """Проверяет конечный фон, чтобы отдельное превью не скрывало пропуск интеграции."""
        displayable = image_name if displayable is None else displayable
        background = "images/1_chapter/" + image_name + ".png"
        first = renpy.render_to_surface(displayable, width=1920, height=1080,
            st=0.03, resize=True)
        raw = renpy.render_to_surface(background, width=1920, height=1080,
            st=0.03, resize=True)
        left, top = pos
        width, height = size
        points = [(x, y)
            for y in range(top + 40, top + height - 40, 20)
            for x in range(left + 40, left + width - 40, 20)]
        pixels = [tuple(first.get_at(point)) for point in points]
        changed = sum(max(abs(a - b) for a, b in zip(pixel[:3], raw.get_at(point)[:3])) > 20
            for point, pixel in zip(points, pixels))
        assert changed > len(points) * 0.75, image_name + ": TV still shows the baked placeholder"
        mean = sum(pixel[0] for pixel in pixels) / float(len(pixels))
        deviation = (sum(pixel[0] ** 2 for pixel in pixels) / float(len(pixels)) - mean ** 2) ** 0.5
        assert deviation > 30.0, image_name + ": noise is not visibly textured"

        for y in range(10, 1080, 40):
            for x in range(10, 1920, 40):
                if left <= x <= left + width and top <= y <= top + height:
                    continue
                assert max(abs(a - b) for a, b in zip(first.get_at((x, y)), raw.get_at((x, y)))) <= 1, image_name + ": TV effect changed the surrounding scene"

        if animated is not None:
            later = renpy.render_to_surface(displayable, width=1920, height=1080,
                st=SM_TV_NOISE_FRAME_T + 0.03, resize=True)
            later_pixels = [tuple(later.get_at(point)) for point in points]
            if animated:
                assert sum(a != b for a, b in zip(pixels, later_pixels)) > len(points) * 0.5, image_name + ": TV animation is absent"
            else:
                assert pixels == later_pixels, image_name + ": accessibility preference did not freeze TV noise"
            for y in range(10, 1080, 40):
                for x in range(10, 1920, 40):
                    if left <= x <= left + width and top <= y <= top + height:
                        continue
                    assert first.get_at((x, y)) == later.get_at((x, y)), image_name + ": noise animates outside the TV"
        return True

    def sm_test_tv_assert_shown(image_name, wide=False):
        ## Показанный кадр обёрнут в постановочный ATL (дыхание яркости, кадры прыжка):
        ## пиксели проверяются у образа, показ — по sprite_showed.
        assert sprite_showed(image_name), "Unexpected TV scene"
        if image_name == "chapter_1 scene_3_sofa_tv_1":
            pos, size = C1S3_TV_POS, C1S3_TV_SIZE
        else:
            pos = C1S1_TV_WIDE_POS if wide else C1S1_TV_NOISE_POS
            size = C1S1_TV_WIDE_SIZE if wide else C1S1_TV_NOISE_SIZE
        return sm_test_tv_assert_scene(image_name, pos, size)

testcase dev_tv_crt_geometry:
    run Function(dev_scene_nav_start, "chapter_1_scene_1.tv")
    advance until "Наконец-то..." timeout 15.0
    assert eval (sprite_showed("chapter_1 scene_1_tv_close"))

    python hide:
        def sample(displayable):
            return renpy.render_to_surface(displayable,
                width=C1S1_TV_NOISE_SIZE[0], height=C1S1_TV_NOISE_SIZE[1],
                st=0.03, resize=True)

        frame = sample(sm_tv_screen(C1S1_TV_NOISE_SIZE, C1S1_TV_NOISE_CORNERS,
            displayable="sm_tv_noise_frame1"))
        for point in ((10, 210), (589, 210), (300, 428)):
            assert frame.get_at(point).a >= 254, "Glass did not reach the inner bezel"
        for point in ((0, 200), (602, 200), (580, 4), (300, 442)):
            assert frame.get_at(point).a == 0, "CRT painted over the outer casing"
        assert frame.get_at((12, 12)).a >= 254, "Rounded corner lost its dark backing"
        assert frame.get_at((12, 12)).r < 15, "CRT corner is still a square noise overlay"

        ## Белая заглушка запечена в JPG: ни один её пиксель не должен просвечивать.
        old_mask = renpy.render_to_surface("dev/tv_noise_screen_mask.png",
            width=571, height=413, st=0.03, resize=True)
        for y in range(413):
            for x in range(571):
                if old_mask.get_at((x, y)).a > 128:
                    assert frame.get_at((x + 23, y + 6)).a >= 254, "White placeholder can show through"

        ## Полоса делает искажение UV измеримым, отдельно от затемнения шума.
        size = C1S1_TV_NOISE_SIZE
        projection = sm_crt_projection(((0, 0), (size[0], 0), size, (0, size[1])), size)
        stripe = Composite(size, (0, 0), Solid("#080808", xysize=size),
            (145, 0), Solid("#ffffff", xysize=(8, size[1])))
        flat = sample(At(stripe, sm_crt_glass(projection, curvature=0.0, vignette=0.0)))
        curved = sample(At(stripe, sm_crt_glass(projection, curvature=SM_TV_NOISE_CURVATURE, vignette=0.0)))

        def stripe_x(surface, y):
            positions = [x for x in range(60, 200) if surface.get_at((x, y)).r > 180]
            assert positions, "CRT stripe vanished or was clamped away"
            return sum(positions) / float(len(positions))

        assert abs(stripe_x(flat, 221) - 148.5) < 1.0, "Zero curvature is not an identity mapping"
        assert stripe_x(curved, 221) < stripe_x(flat, 221) - 20, "CRT shader only shades; UVs are not distorted"
        assert stripe_x(curved, 80) > stripe_x(curved, 221) + 3, "CRT stripe stayed straight"

    run MainMenu(confirm=False)
    assert screen "main_menu" timeout 5.0

testcase dev_tv_noise_mask_and_phases:
    $ persistent.sm_reduce_motion = False
    $ persistent.sm_disable_flashes = False
    run Function(dev_scene_nav_start, "chapter_1_scene_1.tv")
    advance until "Наконец-то..." timeout 15.0
    assert eval (sprite_showed("chapter_1 scene_1_tv_close"))

    python hide:
        def sample(displayable, st):
            return renpy.render_to_surface(sm_tv_screen(C1S1_TV_NOISE_SIZE,
                C1S1_TV_NOISE_CORNERS, displayable=displayable),
                width=C1S1_TV_NOISE_SIZE[0], height=C1S1_TV_NOISE_SIZE[1],
                st=st, resize=True)

        def signature(surface):
            return tuple(tuple(surface.get_at((x, y)))
                for y in range(30, 390, 20) for x in range(30, 540, 20))

        frames = [sample("sm_tv_noise_frame" + str(i), 0.03) for i in range(1, 7)]
        signatures = [signature(frame) for frame in frames]
        for frame in frames:
            assert frame.get_size() == C1S1_TV_NOISE_SIZE
            assert frame.get_at((550, 2)).a == 0, "Noise escaped above the screen slope"
            assert frame.get_at((100, 150)).a > 250, "Screen centre lost opacity"
        for first in range(6):
            for second in range(first + 1, 6):
                changed = sum(a != b for a, b in zip(signatures[first], signatures[second]))
                assert changed > len(signatures[first]) * 0.5, "Noise frames look identical"
        means = [sum(pixel[0] for pixel in sig) / len(sig) for sig in signatures]
        assert all(55.0 < mean < 130.0 for mean in means), "Unexpected noise brightness"
        assert max(means) - min(means) < 15.0, "Phase swap changes overall brightness"
        for sig, mean in zip(signatures, means):
            deviation = (sum(pixel[0] ** 2 for pixel in sig) / len(sig) - mean ** 2) ** 0.5
            assert deviation > 40.0, "Noise grain washed out into a flat screen"
        for index in range(7):
            current = signature(sample("sm_tv_noise_cycle", index * SM_TV_NOISE_FRAME_T + 0.03))
            assert current == signatures[index % 6], "Six-frame sequence or loop is broken"

    run MainMenu(confirm=False)
    assert screen "main_menu" timeout 5.0

testcase dev_tv_noise_accessibility:
    parameter flags = [0, 1, 2, 3]
    $ persistent.sm_reduce_motion = bool(flags & 1)
    $ persistent.sm_disable_flashes = bool(flags & 2)
    run Function(dev_scene_nav_start, "chapter_1_scene_1.tv")
    advance until "Наконец-то..." timeout 15.0
    assert eval (sprite_showed("chapter_1 scene_1_tv_close"))

    python hide:
        for image_name in ("chapter_1 scene_1_tv_close", "chapter_1 scene_1_tv_close_night"):
            sm_test_tv_assert_scene(image_name, C1S1_TV_NOISE_POS, C1S1_TV_NOISE_SIZE,
                animated=not (sm_reduced_motion() or sm_flashes_disabled()))
        sm_test_tv_assert_scene("chapter_1 scene_1_sofa_tv_night", C1S1_TV_WIDE_POS, C1S1_TV_WIDE_SIZE,
            animated=not (sm_reduced_motion() or sm_flashes_disabled()))
        sm_test_tv_assert_scene("chapter_1 scene_3_sofa_tv_1", C1S3_TV_POS, C1S3_TV_SIZE,
            animated=not (sm_reduced_motion() or sm_flashes_disabled()))
        ## Кадр прыжков: первый кадр цикла — тот же фон, экран помех общий.
        sm_test_tv_assert_scene("chapter_1 scene_3_sofa_tv_1", C1S3_TV_POS, C1S3_TV_SIZE,
            displayable="chapter_1 scene_3_sofa_jump",
            animated=not (sm_reduced_motion() or sm_flashes_disabled()))

    run MainMenu(confirm=False)
    assert screen "main_menu" timeout 5.0
