# Reusable Ren'Py Patterns

Engine idioms used repeatedly across this repo. Reach for these when a task is about *how to build something in Ren'Py* rather than *which module already does it* (for the latter, see `modules.md`).

---

### `renpy.curry()` for screen-safe callables

**What:** Screens can only call `Action`-compatible objects — a plain Python function with arguments can't be used directly as a `textbutton ... action`. `renpy.curry(fn)` returns a curried, `Action`-compatible wrapper around `fn` so it can be partially applied and used from a screen.

**Why:** avoids writing a full `Action` subclass for every small callback.

**Example** (from `flashlight.rpy`):
```renpy
def light_z_plus(plus=.1):
    global fl_z
    fl_z += plus
LightZPlus = renpy.curry(light_z_plus)
# then in a screen:
key "rollback" action LightZPlus()
key "rollforward" action LightZPlus(-.1)
```
Also see `transform get_bounds_at(tag): function renpy.curry(get_bounds_at_f)(tag)` in `watcher.rpy`, and `par(index=0, ...): function renpy.curry(par_f)(index, ...)` in `parallax2d.rpy`.

---

### `init` priority ordering

**What:** Ren'Py runs `init` blocks in ascending priority order (default `0`). This repo uses a consistent convention:
- `init -999` — foundational helpers that everything else depends on (e.g. `Comp`, `mystr` in `7dots.rpy`).
- `init -2` (or `-2 python`) — **user-editable configuration**, by convention ending with a `## ДАЛЕЕ ЛУЧШЕ НИЧЕГО НЕ МЕНЯТЬ` ("don't change below this line") comment, so it's guaranteed to run before consuming code but is easy for a game author to find and override.
- `init -1` — module-local setup (e.g. `FLASHBACK.rpy`'s generated vignette masks).
- default `init` / `init python` — the bulk of implementation.
- `init 1900 python hide` — runs very late, used for the custom auto-image declaration override in `7dots.rpy` so it can see every other declared image/prefix first.

**Why:** guarantees utilities and user-configurable variables exist before the code that reads them runs, without forcing a particular file order.

---

### `ImageMask` for non-alpha masking

**What:** `ImageMask(image, mask, reverse=False)` (defined in `7dots.rpy`) masks `image` using **the mask's red channel** instead of its alpha channel — useful when you want to author masks as plain grayscale/color images rather than manage alpha channels.

**Used by:** `xray.rpy` (spot-reveal mask built from `Composite`), `FLASHBACK.rpy`'s `Vignette()` (masks a solid color with a procedurally generated `bw_circle`/`bw_oval` shape).

**Example:**
```renpy
def Vignette(color="#000", a=.75, b=50, mask="bw_oval"):
    return At(ImageMask(color, mask), alpha(a), blur(b))
```

---

### `DynamicDisplayable` for per-frame procedural rendering

**What:** `DynamicDisplayable(fn, **kwargs)` calls `fn(st, at, **kwargs)` every frame (or on redraw) and shows whatever displayable it returns — used for anything that needs to react continuously to game state (mouse position, a clock, current time-of-day) without a screen.

**Used by:** `watcher.rpy` (eyes tracking the cursor via `eye_f`), `7dots.rpy`'s `Clock`/`clock_f`, and `def_daytime` (daytime system — swaps in the time-appropriate sprite variant).

**When to reach for a `Displayable` subclass instead:** if you also need custom `event()` handling (mouse clicks/hover) in addition to rendering — see `xray.rpy`'s `class XRay(renpy.Displayable)`, which overrides `render()`, `event()`, and `visit()`.

---

### Persistent overlay/master-layer screens

**What:** three related techniques for showing something that survives normal interface-hide behavior:
- `config.overlay_screens.append("name")` — screen renders every interaction automatically, without an explicit `show screen`. Used by `xray.rpy` to keep its cursor-highlight overlay always active.
- `show_s(screen)` / `hide_s(screen)` (in `7dots.rpy`) — show/hide on the `"master"` layer, which is not cleared by pressing "h" (hide interface).
- `renpy.add_layer("name", above="screens")` — adds an entirely new persistent render layer above the default screens layer. Used by `FLASHBACK.rpy` for its `"vignette"` layer, so the vignette can sit above dialogue/menus.

**Caution:** all three are "always on once loaded" side effects — see the Install & side-effect notes in `SKILL.md` before combining modules that use them.

---

### The `{#key=value}` invisible-tag metadata convention

**What:** modules that need to attach metadata to a dialogue/menu-choice *string* (without it being visible to the player) embed it as `{#key=value}` and strip/parse it with `get_tag()`/`tag_if()`/`del_tags()` from `7dots.rpy`.

**Used by:** `choice_img.rpy` — `{#img=bed}` (which sprite is the clickable hotspot), `{#if=condition}` / `{#else=alt text}` (conditional choice availability + hover hint).

**Example:**
```renpy
"Здесь будет удобнее{#img=bed}{#if=has('movie')}{#else=Ну нельзя же так сразу!}":
    $ add('bed')
```
```renpy
# reading it back:
$ img = get_tag(choice.caption, "img")
$ available = tag_if(choice.caption, "#if")
```

---

### `LayeredImage` prefix merging via `layered_prefixes`

**What:** Ren'Py's automatic image declaration normally splits an image filename into space-separated tags/attributes. `layered_prefixes` (a list checked by the extended `create_automatic_images()` in `7dots.rpy`) makes filenames starting with a listed prefix get joined with `_` instead — so a `LayeredImage`'s attribute layers keep their full compound name instead of being torn apart by the auto-declarer.

**Used by:** any project combining `LayeredImage` sprites with `images_auto()` (e.g. `xray.rpy`'s `nike` layered sprite).

---

### Perspective / `gl_depth` for fake 3D

**What:** setting `perspective True` together with the `zpos`/`gl_depth` transform (in `7dots.rpy`) and `turnx`/`turny`/`turnz`/`turn` puts a 2D displayable into Ren'Py's GL perspective projection, letting flat images be rotated/positioned as if in 3D space.

**Used by:** `7dots.rpy`'s 3D rotation transforms; the dungeon-crawler projects (`test_dungeon/`) stack perspective-rotated slices to build a first-person view. Note the mature `Renpy_First_Person_Dungeon_Exploration/` module instead fakes 3D purely with **pre-rendered image slices** and does *not* use this pattern — pick whichever approach matches whether you have pre-rendered art (use image stacking) or need runtime-generated angles (use `gl_depth`/`turn`).

---

### Multi-resolution scaling via `K()`

**What:** `resolutions.rpy`'s pattern for resolution-independent UI: wrap every raw pixel number passed to `gui.*` defines and screen properties in `K(x)`, which scales it against the currently selected resolution profile (`persistent.resolution_k`), and wrap every image path in `K("gui")` / use `IK(img)` for resolution-suffixed art variants.

**Why this instead of Ren'Py's built-in scaling:** lets a project ship genuinely different art assets per resolution tier (not just upscale one asset set), switchable at runtime through a dropdown/toggle.

**See:** `modules.md` → *resolutions* for the full setup invocation.
