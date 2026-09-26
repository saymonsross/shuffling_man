# Position Tuner

A drop-in tool for inspecting and working out coordinates inside a running
Ren'Py game. Open it in any scene: it outlines the sprites on screen and reports
their exact parameters — position, anchor, rotation, zoom, image size and
on-screen bounds. The selected sprite can be moved, rotated and re-anchored so
you can work out numbers and copy them into your code.

**The tool never writes anything and never changes the scene.** It reads the
scene's live transforms and does the arithmetic; numbers move into the code by
hand, via the clipboard.

*Русская версия: [README.ru.md](README.ru.md)*

---

## What it shows

For every sprite on screen:

| Value | Where it comes from |
|---|---|
| `pos` | position from the scene's transform, in pixels |
| `anchor` | anchor point, as a fraction of the sprite's side |
| `rotate` | **rotation in degrees** (`—` when there is none) |
| `zoom` | scale factor |
| `картинка` | the image's own size, px |
| `на экране` | the resulting rectangle, zoom and rotation included |

Every sprite is outlined dimly straight away, so you see the whole composition
and how layers overlap. The selected one gets a bright outline that **follows
the rotation** — not an axis-aligned box, but a rectangle turned along with the
sprite. Full-screen guides run through the anchor point and the point itself is
marked with a crosshair, so you can see what the sprite pivots around.

---

## Installing into a project

1. Copy the `position_tuner/` folder into your project's `game/dev/`.
2. Exclude the dev folder from distributions — in `options.rpy`, inside the
   `init python` block next to the other `build.classify` calls:

   ```renpy
   build.classify('game/dev/**', None)
   ```

3. Run the game in developer mode and press **F9**.

That is all: no data files, no project setup. The tool uses only public Ren'Py
APIs, has no third-party dependencies, and does not rely on any images from
your `gui/` folder.

### Verifying it is excluded

```
renpy.sh launcher distribute --dest /tmp/dist --package pc --format zip <project>
```

The resulting archive should contain no files from `game/dev/`.

---

## Using it

| Action | How |
|---|---|
| Open / close | **F9**, or **Esc** to close |
| Select a sprite | click it on screen, or click its row in the list |
| Move | drag with the mouse (outside the panel) |
| Move precisely | **arrows** ±1 px, **Shift+arrows** ±10 px |
| Rotate | **[** and **]** ±1°, with **Shift** ±15° |
| Anchor point | **Tab** forward, **Shift+Tab** back |
| Undo / redo | **Ctrl+Z** / **Ctrl+Shift+Z** (or Ctrl+Y) |
| Restore the scene's values | **R** or the "Сбросить" button |
| Copy | **Ctrl+C** or the buttons |
| Get the panel out of the way | **H**, or the left/right buttons |

A click picks the sprite under the cursor; when several overlap, the smallest
one wins, so a small prop is not swallowed by the background behind it.

While the values still match the scene, no ghost is drawn — just the outline
and the numbers. As soon as you move something, a translucent copy appears at
the new spot and the panel adds a "в сцене: …" line with the original values.

### What gets copied

**Копировать ATL** — a block to paste straight into a scene:

```
anchor (0.5, 0.5)
pos (1264, 431)
rotate 80.0
```

**Копировать вызов** — a transform call built from a template:

```
at placed((1264, 431), (0.5, 0.5), 80.0)
```

The template is one line at the top of `position_tuner.rpy`:

```renpy
define -30 PT_CALL_TEMPLATE = "at placed({pos}, {anchor}, {angle})"
```

The placeholders are `{pos}`, `{anchor}` and `{angle}`. Adjust it there to
match your own set of transforms.

### After pasting into the code

Press **Shift+R**. Ren'Py reloads the script, but the sprite already on screen
stays where it was: a transform receives its coordinate at `show` time and
remembers it, and a reload restores the scene from the last checkpoint, which
sits at the dialogue line *after* the `show`. To see the result, replay the
scene — roll back past the `show` with the mouse wheel and step forward again.

That is why tuning is easier in a sandbox: a short label that shows the sprites
you need and then just waits (see `dev_position_sandbox` in
`game/dev/dev_utils.rpy`). Replaying it is one keypress.

---

## Limitations

- **Camera.** Outlines and the ghost are drawn in base screen coordinates and
  do not follow the scene's `camera` transforms (zoom, frame tilt).
  The numbers are still correct — they are exactly what `pos` expects — but the
  drawing can drift from what you see. Use a camera-free sandbox for precision.
  The `master` layer parallax (`common/parallax.rpy`) is off while the tuner is open.
- **Animation.** A moving sprite's readout changes every frame. That is honest,
  but there is nothing to tune; stop the scene on the frame you need.
- **Exotic positioning.** `xalign` / `xcenter` / `xoffset` and friends are
  reduced to a `pos` + `anchor` pair; if a sprite has no transform at all, the
  values come from its on-screen bounds and the panel says so.

---

## Settings

All at the top of `position_tuner.rpy`:

| Variable | Default | Meaning |
|---|---|---|
| `PT_UNDO_LIMIT` | `1000` | undo stack depth |
| `PT_COALESCE_T` | `0.35` | seconds within which a run of edits merges into one undo step |
| `PT_STEP` / `PT_STEP_BIG` | `1` / `10` | arrow-key step, px |
| `PT_STEP_ANGLE` / `PT_STEP_ANGLE_BIG` | `1.0` / `15.0` | rotation step, degrees |
| `PT_ANCHORS` | 9 anchors | what Tab cycles through |
| `PT_GHOST_ALPHA` | `0.55` | ghost opacity |
| `PT_CALL_TEMPLATE` | `at placed(…)` | template for the "copy call" button |
| `PT_HOTKEY` | `"K_F9"` | key that opens the tuner |
| `PT_COLOR_BOX` / `PT_COLOR_DIM` / `PT_COLOR_GUIDE` / `PT_COLOR_MARK` | | outline and marker colours |

---

## How it works

| File | Contents |
|---|---|
| `position_tuner.rpy` | settings, scene reading, model, undo stack, draw and mouse layers |
| `position_tuner_ui.rpy` | screen, hotkeys, styles |

Four things that are easy to get wrong when extending it:

1. **`renpy.get_at_list` returns the transform prototype, not the live
   instance.** The prototype's properties are all empty — its ATL block was
   never executed on it, so `rotate` is always `None` there. The real values
   only exist on the object from `renpy.scene_lists().layers[layer]`.
2. **`absolute` is a subclass of `float`.** It has to be checked before
   `float`, or a pixel value of `400.0` would be read as 400 screen widths.
3. **Ren'Py caches renders.** The model changes outside the screen (arrows,
   Tab, undo), so the draw layer asks for its own redraw from `render()` via
   `renpy.redraw`. Without that the outline stays where it was.
4. **Child order matters twice.** Children are drawn front-to-back but receive
   events back-to-front. So the outlines are added first (they sit under the
   panel) and the mouse-capture layer last (it sees events before the buttons);
   clicks that land on the panel are passed through.

The tilted outline is not built by hand from four corners: a border rectangle
exactly the size of the image is wrapped in the same
`Transform(pos, anchor, rotate, transform_anchor=True)` as the sprite. That way
it lands on the sprite exactly, at any angle and any anchor.

Tool state lives in an object derived from `python_object` rather than in plain
store variables, so it never enters rollback or the player's save files.
