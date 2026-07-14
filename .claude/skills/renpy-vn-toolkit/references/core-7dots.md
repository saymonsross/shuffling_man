# Core Library Reference: 7DOTS.rpy

The shared helper library several modules depend on. **Bundled with this skill at `sources/core/7DOTS.rpy`** — this is the canonical/newest version (1822 lines), copied from `test_bg_inventory/game/7DOTS.rpy` in the origin `renpy_7dots_tools` repo. Copy that one file alongside any module whose "Needs 7dots?" is "yes" (see `modules.md`).

**Provenance note — the origin repo ships several evolving versions, not identical copies.** For context, if you're working inside the origin repo directly:

| Version | Lines | Found in (origin repo) |
|---|---|---|
| canonical / newest (bundled here) | 1822 | `test_bg_inventory/game/7DOTS.rpy`, `test_choice_img/game/7DOTS.rpy`, `test_watcher/game/7DOTS.rpy` |
| | 1794 | `test_flashback/game/7DOTS.rpy` |
| | 1637 | `test_parallax_mm/game/7dots.rpy` |
| | 1400 | `test_xray/game/7dots.rpy` |
| oldest | 1304 | `test_flashlight/game/7dots.rpy` |

Older versions are subsets of newer ones (missing helpers like `Comp`, `dlc`, `set_val`, `str_cut`, `endswith`, `seen_one`/`seen_all`, `transitions`, and transforms `flasher`, `hover_at`, `side_move`, `breath`). One rename to watch for: the oldest version's `have_tag` was renamed **`has_tag`** in later versions — the bundled canonical copy uses `has_tag`.

All descriptions below are translated from the original Russian code comments.

---

## Transforms (visual)

| Name | Signature | Description |
|---|---|---|
| `zoom` / `xzoom` / `yzoom` | `(zoom=1)` | Scale uniformly / horizontally / vertically (subpixel). |
| `zooming` | `(zoom1=1., zoom2=1., t=1)` | Animated ease from zoom1 to zoom2. |
| `xyzooming` | `(xzoom1, yzoom1, xzoom2, yzoom2, t=1)` | Animated x/y zoom. |
| `alpha` | `(alpha=1.)` | Set opacity. |
| `alphing` | `(alpha1=0, alpha2=1, t=1)` | Fade opacity over time. |
| `blur` | `(blur=4)` | Gaussian blur. |
| `bluring` | `(blur1=0, blur2=16, t=1)` | Animated blur. |
| `brightness` / `brightnessing` | `(brightness=.25)` / `(b1, b2, t=2)` | `BrightnessMatrix`, static/animated. |
| `contrast` / `contrasting` | `(contrast=1.25)` / `(c1, c2, t=2)` | `ContrastMatrix`. |
| `saturation` / `saturationing` | `(saturation=1.)` / `(s1, s2, t=2)` | `SaturationMatrix`. |
| `color` / `coloring` / `color2` | `(color="#000")` / `(c1, c2, t=2)` | `TintMatrix` tint; `color2` pulses between two colors on repeat. |
| `paint` / `painting` / `paint2` | `(color="#fff")` | Recolor as a solid **silhouette** of a color (`Tint · Invert · Tint black`). Example: `image logo = "logo.png"; show logo at paint("#f00")` |
| `breath` | `(t=2.5, dz=.005)` | Subtle vertical "breathing" loop. |
| `hover_at` | `(hover_brightness=.15, hover_zoom=.15, t=.25)` | Widget zooms+brightens on mouse hover; anchor centered. |
| `show_hide` | `(t=.25)` | Fade in on show, fade out on hide. |
| `side_move` / `side_same` | `(old, new)` | Talking-head swap transforms for the textbox. |
| `leap` | `(dt=.25, dyz=.01, dxz=.005)` | Character hop/squash (bottom-anchored). |
| `boobs` | `(t=2)` | Damped vertical jiggle. |
| `left2` / `right2` | `(xa=.35)` / `(xa=.65)` | Place near-left / near-right (not at the very edge). |
| `left0` / `right0` | `()` | Place just off the left / right edge. |
| `rotate` / `rotating` | `(a=45, rotate_pad=False)` / `(a1, a2, t=1)` | 2D rotation (counter-clockwise), static/animated. |
| `hflip` / `vflip` | — | Mirror horizontally / vertically. |
| `crop` | `(x=0, y=0, w=1., h=1.)` | Crop region. |
| `align` / `xalign` / `yalign` / `aligning` | `(xalign=.5, yalign=1.)` | Relative positioning (+ animated `aligning`). |
| `pos` / `xpos` / `ypos` / `posing` | `(xpos=.5, ypos=.0)` | Absolute positioning (+ animated). |
| `offset` / `xoffset` / `yoffset` / `offseting` | `(xoffset=5, yoffset=0)` | Pixel offset (+ animated). |
| `anchor` / `xanchor` / `yanchor` / `anchoring` | `(xanchor=.5, yanchor=1.)` | Anchor point (+ animated). |
| `xysize` / `xsize` / `ysize` | `(width, height)` | Set displayable size. |
| `zpos` / `zposing` / `gl_depth` | `(zpos=0, depth=True, zzoom=False)` | Z-depth positioning (3D). |
| `flasher` / `flasher_off` | `(t=.25, b1=1, b2=.25)` | Gradient-shader color "flasher" strobe / disable. |
| `xy_at` | — | Pins an object to the mouse cursor (center-anchored, uses `xy_at_f`). |

## 3D rotations (perspective)

All set `perspective True` + `gl_depth`, using `RotateMatrix`. Example: `show card at turningy(180, t=1)`.

| Name | Signature | Description |
|---|---|---|
| `turnx` / `turningx` | `(x=45, depth=True)` / `(x, t=1)` | Tilt up/down (static / animated). |
| `turny` / `turningy` | `(y=45, depth=True)` / `(y, t=1)` | Turn left/right. |
| `turnz` / `turningz` | `(z=45, depth=True)` / `(z, t=1)` | Spin CCW/CW in-plane. |
| `turn` / `turning` | `(x=0, y=45, z=0, depth=True)` / `(..., t=1)` | Combined 3-axis rotation. |

## Transitions (`with`-statement effects)

| Name | Signature | Description |
|---|---|---|
| `TurnPage` | `(delay=.5, vertical=False, reverse=False, new_widget, old_widget)` | Page-turn transition. |
| `turn2left` / `turn2right` / `turn2up` / `turn2down` | prebuilt | Ready-made page-turn directions. |
| `zpunch` | `(old_widget, new_widget, dt=.5, dyz=.05, dxz=.05, align=(.5,.5), anchor=(.5,.5))` | Elastic "punch"/squash-stretch transition. Example: `scene bg2 with zpunch` |
| `Flash` | `(color="#fff", t=1)` | Colored screen flash (wraps `Fade`); `flash` = prebuilt white flash. Example: `$ renpy.transition(Flash("#f00"))` |
| `dissolveleft/right/top/bottom` | prebuilt | Directional slide+dissolve (`ComposeTransition`). Example: `scene page2 with turn2left` |
| `TurnPageAt` | transform | Underlying mesh-rotation transform used by `TurnPage`. |

## Audio helpers

Registers a looping `effect` channel. `default_fade = 1.5`; directories `audio_dir="audio"`, `music_dir="music"`. All accept bare names — no folder/extension needed.

| Name | Signature | Description |
|---|---|---|
| `mplay` | `(mname, fadein=1.5, fadeout=1.5, loop=True, channel="music", ext="ogg")` | Play music track or playlist (list). Example: `$ mplay("theme")` |
| `rndplay` | `(mname, ...)` | Play a shuffled playlist. |
| `mreplay` | `(mname, ...)` | Restart music even if the same track is already playing. |
| `fnplay` | `(new_fn, ..., if_changed=False)` | Play by full filename/path. |
| `msave` / `mrestore` | `()` / `(fadein, fadeout, channel)` | Remember / restore the currently playing track. |
| `splay` | `(mname, fadein=0, fadeout=0, channel=config.play_channel, ext="ogg")` | Play a sound (single or list) on a multithreaded `audio` channel. Example: `$ sndplay("click")` |
| `sndplay` | `(mname, ..., channel="sound")` | Play sound on the `sound` channel. |
| `sfxplay` | `(name, channel="effect", loop=True, fadein=1.5, fadeout=1.5, ext="ogg")` | Play a **looping** SFX. |
| `vplay` | `(mname, fadein=0, fadeout=0, channel="voice", ext="ogg")` | Play a voice clip from `voices/`. |
| `sstop` / `sndstop` / `mstop` / `sfxstop` | `(fadeout=..., channel=...)` | Stop audio/sound/music/effect channels. |
| `add_ext` | `(fn, ext="ogg")` | Append extension if missing. |
| `mdeletetags` | `(str)` | Strip `<...>` playback tags from a track string. |
| `s_play` / `sfx_play` / `sfx_stop` | `(sound, trans, st, at)` | Callbacks to fire sounds from inside an `image:` block. |
| Curried actions | — | `MPlay`, `SPlay`, `SFXPlay`, `SFXStop`, `FNPlay`, `VPlay`, `SStop`, `MStop`, `S_Play`, `SFX_Play` — screen-button-safe Action versions. Example: `textbutton "Play" action MPlay("battle")` |

## Image utilities

| Name | Signature | Description |
|---|---|---|
| `Ani` | `(img_name, frames, delay=.1, loop=True, reverse=False, effect=Dissolve(.1, alpha=True), start=1, ext=None, **properties)` | Auto-build a frame animation from numbered images; `delay` can be a `(from, to)` tuple for varying speed; extra kwargs (e.g. `zoom`, `alpha`) are allowed. Example: `image neko = Ani("neko", 5, 0.5)` |
| `get_size` / `get_width` / `get_height` | `(displayable)` | Rendered pixel size (not usable inside `init`). Example: `$ w, h = get_size("hero")` |
| `img2disp` | `(displayable)` | Coerce a string into a displayable. |
| `get_opaque` / `is_opaque` | `(img, x=None, y=None[, min_a=0])` | Pixel alpha at coordinates (default: bottom-right corner). |
| `has_image` | `(name)` | Is an image with this name declared? |
| `has_images` | `(*args)` | Do all listed images exist? |
| `seen_one` / `seen_all` | `(*args)` | Has the player seen any / all of these images? |
| `ImageMask` | `(image, mask, reverse=False)` | Mask by the mask's **red channel** rather than alpha (black = transparent). |
| `bg` | `(color="#000", bg="bg")` | Scene + show a solid-color background. |
| `Clock` / `clock_f` | `(**kwarg)` | Live digital-clock displayable. |
| `shot` | `(w, h)` | Screenshot displayable of a given size. |
| `images_auto` | `(folders=[], spaces=[' ','_','/'], minimum=1, dlc="DLC")` | Enable Ren'Py automatic image declaration including DLC folders. |
| `move_time` | `(delay=.5, effects=["move","ease"])` | Change default move-transition timing. |

## Python helpers

| Name | Signature | Description |
|---|---|---|
| `rnd` | `(i_from=0, i_to=None)` | Random int (upper bound exclusive; single arg = `0..n`). Example: `$ x = rnd(1, 7)` |
| `rndf` | `(f_from=0, f_to=None)` | Random float in range. |
| `rnds` | `(*args)` | Random choice among the arguments. |
| `clip` | `lambda i, mini, maxi` | Clamp value to `[mini, maxi]`. Example: `$ hp = clip(hp, 0, 100)` |
| `fint` | `(x, default=0)` | Parse string to int, else float, else default. |
| `d2` | `(x, d=2)` | Integer division (Python-3-safe). |
| `modf` | `(x, y, precision=1000)` | Modulo for fractional numbers. |
| `sec_to_hms` | `(s)` | Seconds → `H:MM:SS` / `MM:SS` string. |
| `make_list` | `(param)` | Wrap a non-list value in a single-element list (`None` → `None`). |
| `get_tuple` | `(value, *args)` | Pad/trim a tuple to defaults. |
| `next_x` / `prev_x` | `(x, lst)` | Next / previous list element, cyclic. Example: `$ n = next_x(cur, options)` |
| `dict_get` / `get_by_key` | `(dictionary, key[, default])` | Safe dict lookup. |
| `copy` | `(*args)` | `deepcopy` shortcut. |
| `has_text` | `(where, what)` | Substring (or any-of-list) test. |
| `has_val` | `(key)` | Does a global variable of this name exist? |
| `get_between` | `(s, b1="(", b2=")")` | Text between delimiters. |
| `get_var_name` | `(var, default="")` | Reverse-lookup a variable's name via the stack. |
| `blank_list` | `(a)` | Drop empty rows/columns from a 2D grid. |
| `log` / `Log` | `(*args)` | Debug print. |
| `dlc` | `(label, *args, **kwarg)` | Call the first existing label from a list (DLC fallback pattern). |

## Tag parsing

Custom `{#tag=value}` inline-tag system for embedding metadata in dialogue/menu strings (prefix `#` by default).

| Name | Signature | Description |
|---|---|---|
| `get_tags` | `(text, prefix='#')` | Dict of all `{#tag=val}` found. |
| `get_tags_str` | `(text, prefix='#')` | List of raw tag strings. |
| `get_tags_list` | `(s)` | List of `(tag, value)` tuples (all `{}` tags). |
| `get_tag` | `(text, tag, default=None, prefix='#')` | Value of a named hidden tag. Example: `$ img = get_tag("Text {#image=logo.png} more", "image")` → `"logo.png"` |
| `get_tag_first` | `(s, tag, default=None)` | First matching tag value; supports `eval(...)`. |
| `has_tag` | `(text, tag, prefix='#')` | Is the tag present? (Named `have_tag` in the oldest library version — see version table above.) |
| `tag_if` | `(s, tag="#if", default=True)` | Evaluate a condition stored in a tag. |
| `del_tags` | `(s, prefix="#")` | Remove tags (by default, only `#`-prefixed ones). |
| `del_all_tags` | `(txt)` | Strip all text tags via Ren'Py's `filter_text_tags`. |
| `get_key_val` | `(text, sep='=')` | Split `key=val`, trimmed. |
| `str_cut` | `(s, max_len=11, dots="…", allow=[])` | Truncate text (ignoring tags). |

## Screen utilities

| Name | Signature | Description |
|---|---|---|
| `show_s` / `hide_s` | `(screen, *arg, **kwarg)` | Show/hide a screen on the **master** layer (survives interface-hide). Example: `$ show_s("hud")` |
| `show_forever` / `hide_forever` | `(screen)` | Show on a custom `forever` layer not dismissed by "h". |
| `show_foreverest` / `hide_foreverest` | `(screen)` | Add/remove from `config.always_shown_screens` (never hidden). |
| `has_screen` | `(*args, layer=None)` | Is any of the given screens showing? |
| `screen_exists` | `(name)` | Does the screen exist at all? |
| `showhide` / `ShowHide` | `(screen, effect=dissolve)` | Toggle a screen with a transition. Example: `textbutton "Menu" action ShowHide("menu")` |
| `set_val` / `SetVal` | `(**kwarg[, transition=dissolve])` | Set globals + refresh the interaction (screen action). |
| `get_input_text` | `(screen="input", id="input")` | Read current text of an input widget. |
| `MyFileAction` | `(name, page=None, **kwargs)` | Save/Load slot action storing the last say-text as the slot name. |
| `Continue` | `Action` subclass | Continue from the newest auto-save; disabled when there's nothing to load. |

## Daytime system

Automatic sprite/background re-coloring by time of day.

| Name | Signature | Description |
|---|---|---|
| `alldaytime` | list, default `["day", "night"]` | Allowed times of day (`"night"` required). |
| `daytime_prefix` | list | Sprite/bg prefixes whose lighting depends on time of day, e.g. `["bg", "eileen"]`. |
| `daytime_suffix` | `= alldaytime[0]` | Suffix for the base (default) daytime variant. |
| `curdaytime` | var | Current time of day. |
| `setdaytime` | `(newdaytime=None, effect=dissolve)` | Switch to a given time, or cycle to the next; on-screen sprites update immediately. Example: `$ setdaytime("night")` / `$ setdaytime()` (cycle) |
| `atdaytime` | `(bg=False)` | The lighting transform (color matrix) for the current time. |
| `time_of_day` | `(hours=None, morning=7, day=11, evening=18, night=23)` | English name of the time period from an hour (system time if `None`). |
| `color_of_day` / `color_filters` | `(hours=None)` | Overlay tint color for the time of day. |
| `daytime_light` / `daytime_empty` | transforms | Apply the color matrix / no-op. |
| `def_daytime` | `(st, at, img)` | `DynamicDisplayable` callback: picks the time-specific image or recolors the base. |
| `*_bg_attrs` / `*_attrs` | tuples `(color, brightness, saturation, contrast)` | Recolor settings per period (day/evening/night/morning). |

Example setup: `daytime_prefix = ["bg", "eileen"]` then declare art normally via `images_auto()` — matching images get automatic time-of-day variants.

## Auto-image declaration

`create_automatic_images()` — an extended replacement for Ren'Py's built-in auto-declaration:
- Supports `.png/.jpg/.jpeg/.webp` images **and** `.webm/.ogv/.mp4` videos (declared as `Movie`).
- Names matching a prefix in `layered_prefixes` are joined with `_` (kept intact for `LayeredImage`) instead of being split into tags.
- Names with a prefix in `daytime_prefix` get a daytime suffix and become `DynamicDisplayable`s reacting to `curdaytime`.
- Helpers: `endswith(s, exts=None, case=False)`; lists `all_image_extensions`, `all_video_extensions`.

## Other notable helpers (uncategorized)

- **Config/setup:** `Comp` (Composite with configurable anchor), `transitions(transition)` (set one transition for the whole game), `auto_hide`/`auto_hide_off` (extend `config.window_auto_hide`), `window_center`, `pause`.
- **Text speed:** `cps_save`/`cps_get`/`cps_set`/`cps_restore` (+ `CPS` action).
- **Dismiss/skip control:** `skip_once`/`SkipOnce`, `skip_stop`/`SkipStop`, `dismiss_on`/`dismiss_off` (+ curried), `stop_skip`.
- **Language:** `lang`/`Lang`.
- **Saves:** `delete_saves(_now)`, `delete_data(_now)` (+ curried Actions), `get_music_list`, `get_file_list`.
- **Characters:** `get_name_color`, `CH` (formatted name for a missing `Character`).
- **On-screen sprite queries:** `get_showing_images`, `get_showing_sprites`, `get_showing_sprite`, `sprite_showed`, `get_sprite_by_tag`, `get_sprite_bounds`.
- **Misc:** `mystr` (Linux-safe `str`, `define mystr = eval("lambda i: '%s' % i")`), `has_mouse`, `cur_time`, `clock_tformat`.

**Key top-of-file defines:** `mystr`; `dissolveleft/right/top/bottom`; module-level tunables `layered_prefixes=[]`, `default_fade=1.5`, `def_list_sound=None`, `audio_dir`/`music_dir`, `config.has_autosave=True`; a registered `example.gradient` shader (used by `flasher`).
