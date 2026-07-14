# Module Reference

Detailed reference for the 12 mature, reusable modules bundled with this skill under `sources/`. All code snippets and `{#tag}` examples are quoted verbatim from the source files (Russian strings preserved). Each entry's **Copy from** path is self-contained inside this skill folder; the **Origin** path is provenance only — the module's original location in the `renpy_7dots_tools` repo it was extracted from, useful if you want to see the original demo project but not required to reuse the module elsewhere.

---

## flashlight

**Purpose:** Darkens the whole screen except for a spotlight around the mouse cursor (or touch point), zoomable with the scroll wheel.

**Use when:** the user wants a "flashlight", "darkness with a spot of light", or a scary/exploration reveal-under-cursor effect.

**Copy from:** `sources/flashlight/` (`flashlight.rpy` + `images/flashlight.png`, the spotlight-hole image). Origin in the `renpy_7dots_tools` repo: `test_flashlight/game/flashlight.rpy`.

**Needs 7dots?** No — self-contained. A `7dots.rpy` is bundled in the original project folder for the demo but the module itself doesn't call into it.

**Side effects:** None until shown.

**Invocation:**
```renpy
show screen flashlight
# ... your dialogue ...
hide screen flashlight
```

**Config knobs** (`init -2 python`):
- `fl_color = "#012"` — color of the darkness.
- `fl_z = 1` — spotlight zoom.
- `flashlight = "flashlight"` — image with a transparent hole for the spotlight.

**Public API:** `screen flashlight` (shown on the `master` layer, `zorder 200`); `transform light_at`; `transform paint(color)`; `LightZPlus(plus=.1)` (curried action, bound to mouse-wheel `rollback`/`rollforward` inside the screen).

**Gotchas:** has a separate branch for `renpy.variant("touch")` (adds a "»" button to continue, since touch can't distinguish a tap-to-advance from a tap-to-look).

---

## xray

**Purpose:** Reveals an underlying sprite layer (e.g. skin under clothing) in a soft-edged spot around the cursor, when an x-ray mode flag is on.

**Use when:** the user wants a "see-through"/x-ray/censor-reveal effect on a layered sprite.

**Copy from:** `sources/xray/` (`xray.rpy` + `images/xray/mask.png`, the spot-reveal mask). Also copy `sources/core/7DOTS.rpy`. Origin: `test_xray/game/xray.rpy`.

**Needs 7dots?** Yes — uses `get_size`, `paint`, `images_auto`, `ImageMask` from `7DOTS.rpy`.

**Side effects:** `config.overlay_screens.append("xray")` runs at load time — the x-ray overlay screen is *always* present; actual reveal only happens when the `xray` variable is `True`.

**Invocation:**
```renpy
# enable x-ray mode
$ xray = True

# a layered sprite
layeredimage nike:
    # merge the layers
    at Flatten
    # body
    always:
        name + "girl_body"
    always:
        # dress that can be x-rayed
        # input: character tag and full name of the clothing layer image
        XRay("girl_dress")
```

**Config knobs** (`init -2 python`):
- `xray_mask = "xray mask"` — spot image.
- `xray = False` — x-ray mode toggle.
- `xray_light_alpha = .25` — cursor highlight opacity (`0` disables it).
- `xray_light_color = "#fff"`.

**Public API:** `class XRay(renpy.Displayable)` — wrap a layer image in this to make it x-rayable; global `xray` flag; `screen xray` (auto-registered overlay for the cursor highlight); `images_auto()` call.

**Gotchas:** requires an `xray_mask` image to be declared/auto-declared; masking uses the mask's alpha via `ImageMask`+`Flatten(Composite(...))`, computed per-frame from mouse position.

---

## watcher

**Purpose:** Eyes (white/iris/pupil/eyelids, built from 4 PNGs) that track the mouse cursor — for sprites shown on the `master` layer only (does not work inside `screen`s).

**Use when:** the user wants a character portrait/sprite with eyes that follow the mouse.

**Copy from:** `sources/watcher/` (`watcher.rpy` + `images/eye/0.png`..`3.png`). Origin: `test_watcher/game/watcher.rpy`.

**Needs 7dots?** No — self-contained (`7DOTS.rpy` is present in the original project folder but unused by this module).

**Side effects:** None until an `eye*` image is shown.

**Invocation:**
```renpy
init:
    # the tag must match the name that follows the word "image"!
    image eye1 = Eye("eye1")

    # optionally add an iris color
    image eye1 = Eye("eye1", "#348")

label start:
    show eye1 as truecenter
```
Requires an `eye/` folder with 4 PNGs named `0.png`..`3.png` (0 = white/alpha mask, 1 = iris, 2 = pupil, 3 = eyelids; 1 and 2 must be smaller than 0 for realistic movement range).

**Config knobs** (`init -2 python`): `eye_default_color = "#589"`; `eyes_fps = 30`.

**Public API:** `Eye(tag, color)` constructor; `image eye 0..3`; `transform color(color)`; `transform get_bounds_at(tag)`.

---

## parallax2d

**Purpose:** 2D multi-layer parallax with eased inertia, drifting/zooming layers based on cursor position; supports composing small sprites onto a full-screen positioned canvas.

**Use when:** the user wants background/foreground layers (menus, CGs, scenes) that drift with the mouse for a sense of depth.

**Copy from:** `sources/parallax2d/parallax2d.rpy`. Origin: `test_parallax_mm/game/parallax2d.rpy`.

**Needs 7dots?** No required use — bundled `7dots.rpy` in the original project is for the demo only.

**Side effects:** `persistent.parallax` defaults to `True` on PC/web, `False` elsewhere (touch/mobile), set on first load.

**Invocation:**
```renpy
# test image with the girl on the right
image cg test = Par("bg forest", Pos("girl", xalign=.75))

# main-menu background, girl centered but mirrored
image mm bg = Par("mm 1", Pos("mm 2", xzoom=-1))

# a toggle button, e.g. in quick_menu or preferences
textbutton _("Параллакс") action Parallax()
```

**Config knobs** (`init -2 python`): `par_easing_factor = .1` — lower = slower easing; `par_zoom_plus = .05` — zoom increment per layer index.

**Public API:** `Par(*layers, xaxis=True, yaxis=True, w=None, h=None, **kw)` — build a parallax-composited image from any number of `Pos(...)` layers; `Pos(image, **kw)` — position/distort one layer's sprite before compositing (any transform kwargs allowed); `Comp(size, *args)` — position-based Composite variant; `class Parallax(Action)` — toggle `persistent.parallax` (optional `blink=True` flashes red/green feedback); `par_f` — the per-frame easing callback (used internally by the `par(index, xaxis, yaxis)` transform).

---

## FLASHBACK

**Purpose:** Two independent tools: (1) a blurred, tinted, alpha vignette overlay, and (2) a global color-grade (brightness/tint/saturation/contrast) with optional flicker ("blink"), both applied above the `screens` layer.

**Use when:** the user wants a flashback mood — vignette framing and/or an old-film / desaturated / flickering color treatment over the whole scene.

**Copy from:** `sources/flashback/FLASHBACK.rpy`. Also copy `sources/core/7DOTS.rpy`. Origin: `test_flashback/game/FLASHBACK.rpy`.

**Needs 7dots?** Yes — uses `alpha`, `blur`, `paint`, `ImageMask`, `crop` from `7DOTS.rpy`.

**Side effects:** `renpy.add_layer("vignette", above="screens")` runs at load time — a new persistent render layer is always added, whether or not the vignette is ever shown.

**Invocation:**
```renpy
# vignette
$ vignette_on()
$ vignette_on(color="#000", a=.75, b=50, mask="bw_oval")   # color, alpha, blur radius, mask image
$ vignette_off()

# color grade (any subset of kwargs)
$ color_on(brightness=.1)                                    # slightly brighter
$ color_on(tint="#bcf", saturation=0, contrast=1.5, blink=.05)  # flickering film look
$ color_off()
```

**Public API:** `vignette_on(color="#000", a=.75, b=50, mask="bw_oval")` / `vignette_off()`; `Vignette(color, a, b, mask)` displayable factory (e.g. `show expression Vignette("#124", a=.25)`); `color_on(**kwargs)` / `color_off()` for the master-layer color matrix; generated images `bw_circle` / `bw_oval` (procedural masks via `Text` glyph + `Flatten(Composite(...))`); `screen vignette(color, a, b, mask)` on the `"vignette"` layer.

**Gotchas:** vignette and color-grade are independent — combine both for a full "flashback" look.

---

## choice_img

**Purpose:** A drop-in replacement `menu(screen="img")` that lets choices be image hotspots (via an invisible `{#img=tag}` tag on the choice caption) with conditional enable/disable (`{#if=}` / `{#else=}`), plus a minimal event-flag system (`has`/`has_or`/`has_and`/`add`) commonly used to drive those conditions.

**Use when:** the user wants clickable image buttons for choices overlaid on a background (point-and-click hotspots), or wants text choices with conditional availability and an alternate hover hint.

**Copy from:** `sources/choice_img/choice_img.rpy`. Also copy `sources/core/7DOTS.rpy`. Origin: `test_choice_img/game/choice_img.rpy`.

**Needs 7dots?** Yes — uses `get_tag`/`tag_if` (tag parsing) and a `focus_mask`-based highlight.

**Side effects:** None until `menu(screen="img")` is used.

**Invocation:**
```renpy
# reset event flags after label start
$ events = [ ]

# a sprite bound to fixed coordinates, so hotspots line up with the background
image bed = At("bg room bed", pos(1270, 630))

menu(screen="img"):
    "Здесь будет удобнее{#img=bed}{#if=has('movie')}{#else=Ну нельзя же так сразу!}":
        $ add('bed')

# plain text choices also support {#if=}{#else=} without an {#img=} tag
# positioning of text buttons:
menu(screen="img", vbox_align=(.5, .05)):
    ...
```

**Public API:** `events = []`; `has(event)`; `has_or(*args)`; `has_and(*args)`; `add(event)`; `screen img(items, vbox_align=(.5, .4))`; `transform imghover(t=.35)`.

**Gotchas:** the source file defines `has_or` **twice** — the second definition (the "all events present" logic) overwrites the first and shadows the intended `has_and`, so as shipped, calling `has_and` will raise `NameError`; treat `has_or` in this file as actually implementing "all of" semantics and verify before relying on true "any of" behavior.

---

## cho

**Purpose:** A custom-styled, skinnable replacement for the default choice screen (fixed-width buttons, hover tint, centered vbox).

**Use when:** the user wants a nicer-looking, easily restyled choice menu without building one from scratch.

**Copy from:** `sources/cho/cho.rpy`. Origin: `test_cho/game/cho.rpy`.

**Needs 7dots?** No.

**Side effects:** None — pure screen/style definitions.

**Invocation:**
```renpy
menu(screen="cho"):
    "Option A":
        pass
```

**Config knobs** (GUI defines at top of file): `gui.cho_button_width` (default: `config.screen_width // 3`), `gui.cho_button_height`, `gui.cho_button_tile`, `gui.cho_button_borders`, `gui.cho_button_text_font/size`, `gui.cho_button_text_xalign/yalign`, `gui.cho_button_text_idle_color/hover_color/selected_color/insensitive_color`, `gui.cho_spacing`.

**Public API:** `screen cho`; `transform ch_at(t=.5)` (fade in/out); `transform ch_hover_at(t=.5, color="#fd8", brightness=.25)` (hover tint); styles `cho_label`, `cho_label_text`, `cho_vbox`, `cho_button`.

---

## BALANCE

**Purpose:** A pendulum-timing mini-game — a thumb swings back and forth; the player must press to stop it inside a target zone.

**Use when:** the user wants a skill/timing check, tension mini-game, or lock-picking-style challenge.

**Copy from:** `sources/balance/BALANCE/` (`BALANCE.rpy` + `frame/*.png` + `audio/countdown.ogg` — the whole folder is required, image/audio assets included). Origin: `test_balance/game/BALANCE/BALANCE.rpy`.

**Needs 7dots?** No.

**Side effects:** None until `call balance` is used.

**Invocation:**
```renpy
call balance
# or with explicit difficulty parameters:
call balance(time=2, target_width=80, target_xalign=.5, frame_xysize=(600, 80), frame_align=(.5, .5), frame_xpadding=23)

# read the result immediately after the call returns:
if balance_win:
    "Ты справился!"
else:
    "Не вышло..."
```
Parameters: `time` (seconds for the pendulum to swing one way), `target_width` (target-zone width), `target_xalign` (target-zone position inside the frame), `frame_xysize`, `frame_align`, `frame_xpadding`. Pendulum width comes from the size of `BALANCE/frame/thumb.png`.

**Public API:** `label balance(...)` — **communicates its result through the global variable `balance_win`, not `_return`** — check `balance_win` right after the `call` returns; `label balance_ready` (3-2-1 countdown before play); `hard_fade(color="#fff", t=1, hard=True)` — an uninterruptible screen flash; `image balance_thumb`; `transform balance_show_hide(t=.5)`; `style balance_count`.

**Gotchas:** result is a global, not a return value — don't expect `$ result = (call balance)`.

---

## BEEP

**Purpose:** Plays a short "blip"/beep sound per character while their dialogue text is typing out (Undertale-style pseudo-voice), with per-character sound overrides.

**Use when:** the user wants cheap pseudo-voice-acting feedback without recording real VO.

**Copy from:** `sources/beep/BEEP/` (`BEEP.rpy` + the default `beep.ogg`/`voice_female.ogg`/`voice_male.ogg` — copy the whole folder). Origin: `test_beep/game/BEEP/BEEP.rpy`.

**Needs 7dots?** No.

**Side effects:** Sets `config.character_callback = beep_callback` at load time — **every** character's dialogue immediately gets blip sounds; this overwrites any existing `config.character_callback` the project may have had.

**Invocation:**
```renpy
# copy the BEEP folder into your project, then optionally customize:
beep = "BEEP/voice_female.ogg"   # default voice for everyone

# split into per-gender pseudo-voices; None:[None] silences the narrator
beep_other = { None: [ None ], "BEEP/voice_male.ogg": [ _("Петя"), _("Саша") ] }

# add more names later
$ beep_other["BEEP/voice_male.ogg"].append(_("Серёжа"))
```

**Public API:** `beep` (default sound filename); `beep_other` (dict mapping sound filename → list of `who` names that use it; `None` key = narrator override); `beep_callback` (the `config.character_callback` implementation, plays on `"show"`, stops on `"slow_done"`/`"end"` via a dedicated looping `"beep"` channel).

---

## resolutions

**Purpose:** Lets a project ship graphics for several resolutions (e.g. 1K/2K/4K) and switch between them at runtime, scaling all GUI coordinates through a helper.

**Use when:** the user wants runtime multi-resolution support (a settings dropdown or a quick-menu toggle) rather than a single fixed-resolution GUI.

**Copy from:** `sources/resolutions/resolutions.rpy`. Origin: `test_resolutions_all/game/resolutions.rpy` (generalized successor of the simpler `test_resolutions/`, which only toggles between two fixed resolutions and is out of scope here).

**Needs 7dots?** No.

**Side effects:** Sets `config.automatic_images_minimum_components`, `config.automatic_images`, `config.automatic_images_strip` to support suffix-based automatic image variants.

**Invocation:**
```renpy
# 1. declare available resolutions (height in px) — do this first
resolution_dpi = {"1K": 1080, "2K": 1440, "4K": 2160}
resolution_aliaces = {"1K": "FullHD"}   # optional display-name overrides

# 2. rewrite gui.rpy / screens.rpy numeric values through K()
# gui.init(K(1920), K(1080))
# define gui.quick_button_borders = Borders(K(15), K(6), K(15), K(0))

# 3. rewrite image paths through K("gui") and declare resolution-suffixed art via IK()
# style window: background Image(K("gui") + "/textbox.png", ...)
# image bg room = IK("bg room")   # needs images "bg room 1K.png", "bg room 2K.png", "bg room 4K.png"

# 4. add UI controls:
textbutton resolution_aliace() action ToggleResolution()                         # quick-menu toggle
textbutton res_dropbox.text xsize config.screen_width // 6 action DropBoxDrop(res_dropbox)  # preferences dropdown
```
Requires per-resolution asset subfolders (`gui_2K/`, `gui_4K/`, …) and suffixed image names (`img 2K.png`, `img 4K.png`).

**Public API:** `K(x)` — scale a raw number to the current resolution; `IK(img)` — pick the resolution-suffixed image variant; `resolution_aliace(key=None)`; `ToggleResolution` action; `class DropBox` + `DropBoxDrop` action; `res_dropbox` instance; state stored in `persistent.resolution_k`.

---

## pipes

**Purpose:** A pipe-rotation connection puzzle mini-game, plus an in-game level editor/maker.

**Use when:** the user wants a pipe-connecting or rotate-the-tile puzzle, or wants to author new puzzle levels visually.

**Copy from:** `sources/pipes/` (`pipes.rpy` + the 7 pipe-piece PNGs: `bend.png`, `cap.png`, `cross.png`, `ground.png`, `sink.png`, `straight.png`, `t.png`). Origin: `pipes/pipes.rpy` — **flat project layout, no `game/` subfolder** in the original repo (the one exception there).

**Needs 7dots?** No (original README notes an optional soft reference to a `clip_put` helper used by the level maker's "copy" function, for clipboard export of authored maps).

**Side effects:** None until a `pipes`/`pipes_maker` screen is shown.

**Invocation:**
```renpy
# play a single board
show screen pipes(pipes_map_1)
pause
hide screen pipes

# or the built-in 6-level demo chain
call pipes_game_chain

# level editor — design a board, then "copy" exports it as map literal
show screen pipes_maker(pipes_map_create)
```
Maps are nested lists: `[[pipe_type, rotation], ...]` per row.

**Public API:** `class pipe_handler` (`__init__(map, wh)`, `shuffle()` randomizes all rotations, `rotate(row, col)`, `sum(map)` reduces to a comparable signature); `class pipe_maker_handler` (editor: `rotate`, `change`, `add_row`, `add_column`, `copy()`); `screen pipes(g=pipes_map_1)`; `screen pipes_maker(g=pipes_map_create)`; `transform pipes_rotate(r)`; `label pipes_game_chain` (plays maps `pipes_map_1`..`pipes_map_6` in sequence); prebuilt maps `pipes_map_1`..`pipes_map_6`, `pipes_map_create`.

---

## Renpy_First_Person_Dungeon_Exploration

**Purpose:** A turn-based, first-person dungeon crawler built from pre-rendered perspective-view image "slices" stacked to fake a 3D corridor, with a mini-map — not a real 3D engine (compare `test_dungeon/`, which *does* use GL 3D and shaders, but is out of scope here as a demo-only project).

**Use when:** the user wants a Dungeon-Master/Wizardry-style first-person grid crawler without a 3D engine, or wants a template/reference implementation to build one from.

**Copy from:** `sources/dungeon/script.rpy` — **code only, no art**. This is a **full standalone game/template, not a drop-in module**; reuse means studying and adapting this script, not dropping in a working feature. The original demo project (`Renpy_First_Person_Dungeon_Exploration/`) ships ~211 pre-rendered perspective-slice PNGs that aren't bundled here (too large and inherently project-specific art) — you'll need to author or source your own matching set. Origin: `Renpy_First_Person_Dungeon_Exploration/game/script.rpy`.

**Needs 7dots?** No dependency.

**Side effects:** Adds several keys to `config.keymap['dismiss']` and disables rollback (turn-based movement isn't compatible with Ren'Py's rollback).

**Entry points (labels in `game/script.rpy`):**
- `start` (~line 490) — game entry point.
- `FPE_calculate_position` (~line 525) — resolves the player's position/facing into the perspective image stack to show.
- `FPE_Environments_Display` (~line 868) — draws the layered environment slices + mini-map.
- `FPE_movement` (~line 1673) — the turn-based input/movement loop.
- `game_over` (~line 1724).

**Key data shape:** the player position is a single integer coordinate (e.g. `player_position = 505`) into a flat map array (e.g. `map_001`); each step re-renders the perspective cone from stacked `show image` calls for that position/facing.

**Gotchas:** requires a large matched set of perspective-slice art (~211 PNGs in the reference project) authored per direction/depth — this is the main cost of reusing the pattern, not the script logic. See its own `README.md` in that folder for the full walkthrough.
