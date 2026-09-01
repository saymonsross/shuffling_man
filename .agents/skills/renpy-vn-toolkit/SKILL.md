---
name: renpy-vn-toolkit
description: Router and reference for the "7dots" Ren'Py toolkit — a repo of copy-paste-ready modules for visual novels. Use when building or modifying a Ren'Py game and you need a flashlight/darkness spotlight, x-ray/reveal-under-cursor effect, mouse-following eyes, 2D parallax layers, flashback vignette or film color-grade, image-based or custom-styled choice menus, in-textbox choices, a pendulum/timing mini-game, per-character "beep" blip voices, multi-resolution asset switching, a pipe-rotation puzzle, a first-person dungeon crawler, or any of the shared 7dots.rpy helper functions (transforms, transitions, audio, tags, screens, daytime recoloring). Prefer reusing one of these modules over writing new Ren'Py code from scratch.
---

# Ren'Py VN Toolkit (7dots)

A task→module router, bundled with the actual source files, for a collection of small, self-contained, copy-paste Ren'Py modules (each one or two `.rpy` files, some with a tiny required asset folder) plus a shared helper library (`7DOTS.rpy`). This skill folder is **self-contained and portable** — everything needed to reuse a module lives under `sources/` inside this same skill, so it works when copied into any other project, not just inside the `renpy_7dots_tools` repo it was extracted from. Use this skill to find the existing module that already solves a feature request instead of building it from scratch.

## How to use this skill

1. **Match the task.** Scan the routing table below for the user's intent ("I want a flashlight effect", "I need a mini-game", "clickable image choices"…).
2. **Open the details.** Read the matching module section in `references/modules.md` for dependencies, side effects, config knobs, public API, and a verbatim copy-paste invocation snippet.
3. **Copy the module.** Copy the entire folder `sources/<module>/` (listed in the routing table below) into the target game's `game/` folder, preserving its internal subfolder structure (e.g. `sources/balance/BALANCE/` → `game/BALANCE/`) — it already contains the `.rpy` file plus any small image/audio assets the module needs to run. Add `sources/core/7DOTS.rpy` too if the module's "Needs 7dots?" column says yes (see `references/core-7dots.md` for version notes). Then follow the invocation snippet. There is no build step; just drop the files in and run the project through the Ren'Py launcher/SDK.
4. If the task is about a **general Ren'Py engine pattern** used across this repo (curried actions, `ImageMask`, `DynamicDisplayable`, the `{#tag}` metadata convention, persistent overlay screens, etc.) rather than a specific module, check `references/patterns.md`.
5. If the task needs a **helper function** (random ints, tag parsing, audio playback, screen-time-of-day recoloring, transforms like zoom/blur/paint…) rather than a whole module, check `references/core-7dots.md`.

## Folder layout

```
renpy-vn-toolkit/
  SKILL.md
  sources/                 # self-contained, copy-paste-ready — no external dependencies
    core/7DOTS.rpy
    flashlight/flashlight.rpy, images/flashlight.png
    xray/xray.rpy, images/xray/mask.png
    watcher/watcher.rpy, images/eye/0-3.png
    parallax2d/parallax2d.rpy
    flashback/FLASHBACK.rpy
    choice_img/choice_img.rpy
    cho/cho.rpy
    balance/BALANCE/BALANCE.rpy, audio/countdown.ogg, frame/*.png
    beep/BEEP/BEEP.rpy, *.ogg
    resolutions/resolutions.rpy
    pipes/pipes.rpy, *.png
    dungeon/script.rpy        # reference template — see modules.md, requires your own art
  references/
    modules.md, core-7dots.md, patterns.md
```

## Routing table

### Effects & shaders
| You want to… | Module | Copy from | Needs 7dots? |
|---|---|---|---|
| Darken the screen except for a spotlight that follows the mouse/touch | flashlight | `sources/flashlight/` | bundled, not required |
| Reveal what's under a clothing/cover layer where the cursor hovers ("x-ray") | xray | `sources/xray/` | yes |
| Give a sprite eyes that track the mouse cursor | watcher | `sources/watcher/` | no (bundled, unused) |
| Add 2D parallax drift to background/sprite layers following the mouse | parallax2d | `sources/parallax2d/` | bundled, not required |
| Show a blurred, tinted vignette and/or flickering old-film color grade for a flashback | FLASHBACK | `sources/flashback/` | yes |

### UI & menus
| You want to… | Module | Copy from | Needs 7dots? |
|---|---|---|---|
| Make menu choices clickable image hotspots on a background, with conditional/disabled options | choice_img | `sources/choice_img/` | yes |
| Replace the default choice menu with a custom-styled, skinnable one | cho | `sources/cho/` | no |
| Support multiple screen resolutions (1K/2K/4K…) with a dropdown/toggle switcher | resolutions | `sources/resolutions/` | no |

### Mini-games
| You want to… | Module | Copy from | Needs 7dots? |
|---|---|---|---|
| Add a pendulum-timing skill check ("stop it in the target zone") | BALANCE | `sources/balance/` | no |
| Add a pipe-rotation connection puzzle (with a level editor) | pipes | `sources/pipes/` | no |

### Audio
| You want to… | Module | Copy from | Needs 7dots? |
|---|---|---|---|
| Give each character a per-line "blip"/beep pseudo-voice while text types out | BEEP | `sources/beep/` | no |

### 3D / pre-rendered crawlers
| You want to… | Module | Copy from | Needs 7dots? |
|---|---|---|---|
| Build a first-person, turn-based dungeon crawler from pre-rendered perspective slices | dungeon (reference template) | `sources/dungeon/script.rpy` — code only, you supply the perspective-slice art | no |

## Install & side-effect notes

Copying a module means copying its whole `sources/<module>/` folder into the target project's `game/` folder (see the tree in "Folder layout" above for how each one's internal subfolders should land). Most modules are inert until invoked (a `call`, `show screen`, or setting a flag). **Three modules are "install and always-on"** — they mutate global config as soon as they're loaded, with no explicit activation step:

- **BEEP** sets `config.character_callback = beep_callback` — every character's dialogue immediately gets blip sounds.
- **xray** appends `"xray"` to `config.overlay_screens` — the x-ray overlay is always present (toggle behavior via the `xray` variable).
- **FLASHBACK** adds a new `"vignette"` render layer above `"screens"` via `renpy.add_layer` — this happens at load time regardless of whether `vignette_on()` is ever called.

Flag this to the user before adding one of these three to a project that already has conflicting behavior (e.g. an existing `config.character_callback`).

## Further reference

- **`references/modules.md`** — full per-module reference: purpose, trigger phrases, dependencies, side effects, copy-paste invocation, config knobs, public API, gotchas, for all mature modules.
- **`references/core-7dots.md`** — categorized reference for the shared `7dots.rpy`/`7DOTS.rpy` helper library (transforms, 3D rotation, transitions, audio, image utilities, python helpers, tag parsing, screen utilities, daytime recoloring, auto-image declaration).
- **`references/patterns.md`** — reusable Ren'Py engine idioms demonstrated across this repo (curried actions, init-priority ordering, `ImageMask`, `DynamicDisplayable`, persistent overlay screens, `{#tag}` metadata, LayeredImage prefix merging, master-layer screens, perspective/3D, resolution-scaling helpers).

## Provenance & running the original demos

These modules were extracted from the `renpy_7dots_tools` repo ("7dots"), where each also has a standalone runnable demo project (e.g. `test_flashlight/`, with a full `game/` folder including this module). If you're working inside that repo and want to see a module's original demo rather than reuse the portable copy, point the Ren'Py launcher, or `renpy.exe <path>`, at the matching `test_*` folder (`pipes/` is flat, no `game/`). That's optional context, not required for reusing `sources/` elsewhere — this skill's `sources/` folder has everything needed on its own, with no build step.
