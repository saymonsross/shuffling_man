define SM_TV_NOISE_SIZE = (603, 443)
define SM_TV_NOISE_FRAME_T = 0.18
define SM_TV_NOISE_GRAIN_SCALE = 3.0
define SM_TV_NOISE_BASE = "#202020"
define SM_TV_NOISE_CURVATURE = 0.16
define SM_TV_NOISE_CORNER_RADIUS = 26.0
define SM_TV_NOISE_VIGNETTE = 0.28

init python:
    def sm_tv_noise_frame(index):
        width = int(round(SM_TV_NOISE_SIZE[0] / SM_TV_NOISE_GRAIN_SCALE))
        height = int(round(SM_TV_NOISE_SIZE[1] / SM_TV_NOISE_GRAIN_SCALE))
        ## Берём центр исходного PNG: уменьшение всего 1920×1080 стирает зерно.
        texture = At("images/1_chapter/owner_review/tv_noise/noise_anim_%d.png" % index,
            crop((1920 - width) // 2, (1080 - height) // 2, width, height),
            xysize(*SM_TV_NOISE_SIZE))
        ## PNG полупрозрачны; подложка закрывает запечённую заглушку телевизора.
        return Composite(SM_TV_NOISE_SIZE,
            (0, 0), Solid(SM_TV_NOISE_BASE, xysize=SM_TV_NOISE_SIZE),
            (0, 0), texture)

    def sm_tv_screen(size, corners, displayable="sm_tv_noise"):
        return At(displayable, xysize(*size),
            sm_crt_glass(sm_crt_projection(corners, size),
                curvature=SM_TV_NOISE_CURVATURE,
                corner_radius=SM_TV_NOISE_CORNER_RADIUS * size[0] / SM_TV_NOISE_SIZE[0],
                vignette=SM_TV_NOISE_VIGNETTE))

    def sm_tv_scene(background, pos, size, corners):
        ## Эффект внутри самого кадра сохраняется при любом входе и загрузке игры.
        return Composite((1920, 1080),
            (0, 0), background,
            pos, sm_tv_screen(size, corners))

image sm_tv_noise_frame1 = sm_tv_noise_frame(1)
image sm_tv_noise_frame2 = sm_tv_noise_frame(2)
image sm_tv_noise_frame3 = sm_tv_noise_frame(3)
image sm_tv_noise_frame4 = sm_tv_noise_frame(4)
image sm_tv_noise_frame5 = sm_tv_noise_frame(5)
image sm_tv_noise_frame6 = sm_tv_noise_frame(6)
image sm_tv_noise_cycle = Ani("sm_tv_noise_frame", 6, delay=SM_TV_NOISE_FRAME_T, effect=None)
image sm_tv_noise = ConditionSwitch(
    "sm_reduced_motion() or sm_flashes_disabled()", "sm_tv_noise_frame1",
    True, "sm_tv_noise_cycle")
