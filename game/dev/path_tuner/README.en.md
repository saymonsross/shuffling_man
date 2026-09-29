# Path Tuner

A graphical spline path editor inside a running Ren'Py game — think editing a
Cinemachine spline in Unity. Click the scene to drop through-points, the curve
passes through them; the end handles set the entry and exit tangents. A ghost
sprite plays the motion along the curve live, and the result is copied to the
clipboard as ready-to-paste ATL with `knot`.

The ghost position is computed by the same engine interpolation that executes
ATL splines, so the preview trajectory and the generated code match exactly —
including the uneven Catmull-Rom speed on unequal segments.

*Русская версия: [README.ru.md](README.ru.md)*

---

## How the curve works

| Points | Curve | Handles |
|---|---|---|
| 2 | cubic Bézier | handles are the Bézier control points |
| 3+ | Catmull-Rom through every point | handles set the start and end tangents |

A handle acts as a Bézier tangent of its own end segment: the entry/exit
direction and sweep do not change as points are added. Interior tangents are
computed by Catmull-Rom itself and update with every edit of the neighboring
points. An untouched handle sits at a third of its end segment — the classic
mirrored phantom (`2·P0 − P1`), the curve's "natural" entry. Handles are
attached to their end points and move along with them.

Time is split evenly between segments with no arc-length correction: the
sprite moves slower over a short segment and faster over a long one. The
ghost shows this honestly; even spacing between points gives even speed.

## Rotation modes

- **none** — no rotate in the output;
- **fixed values** — linear from a start angle to an end angle;
- **along tangent** — the angle is sampled at the through-points and splined
  between them: an approximation of the true tangent, so between points the
  angle can drift slightly from the curve's heading (the ghost shows exactly
  what goes into the code). The offset compensates the artwork's base
  orientation.

Whenever rotate is emitted, `transform_anchor True` is added — the anchor
doubles as the pivot (the rotate-transform-anchor rule).

## Usage

| Action | How |
|---|---|
| Open / close | **F6**, plus **Esc** to close |
| Add a point | click an empty spot in the scene (always appended to the end) |
| Move a point/handle | drag with the mouse |
| Precise move | **arrows** ±1 px, **Shift+arrows** ±10 px |
| Delete a point | **Del** or the button |
| Pause / play | **Space**; while paused, scrub with the panel bar |
| Anchor (ghost and code) | **Tab** / **Shift+Tab** |
| Undo / redo | **Ctrl+Z** / **Ctrl+Shift+Z** (or Ctrl+Y) |
| Copy ATL lines | **Ctrl+C** or the button |
| Copy the show block | **Ctrl+Shift+C** or the button |
| Move the panel aside | **H**, or the left/right buttons |

The ghost is the scene sprite picked in the list (its tag goes into the
`show` block) or a 110×110 placeholder.

### What gets copied

**Copy ATL** — lines to paste into an existing block:

```
anchor (0.5, 1.0) pos (300, 850) transform_anchor True rotate -48.4
easein 2.0 pos (1500, 250) knot (-100, 1300) knot (700, 400) knot (1150, 650) knot (1850, -150) rotate -48.9 knot -83.7 knot -13.2 knot -10.5 knot -87.2
```

**Copy show** — the same with a `show <sprite>:` header and indentation.

## Limitations

- **Camera.** The curve and the ghost are drawn in base screen coordinates
  and do not follow the scene's `camera` transforms. The numbers are still
  correct — they are exactly what `pos` expects. For a pixel-accurate picture
  use the sandbox (`dev_position_sandbox`).
- **Sprite zoom.** The ghost does not inherit the sprite's scene `zoom`; its
  size may differ, the trajectory and the code do not depend on it.
- **Points are only appended to the end of the path**; there is no mid-path
  insert — drag an appended point into place instead.
- **Undo** covers points and handles; duration, warper, rotation and anchor
  change via buttons without undo.
- **Write-to-code.** Clipboard only: a multi-line ATL block is not rewritten
  in place, unlike Position Tuner's `placed(...)`.

## Settings

All at the top of `path_tuner.rpy`: `PATH_HOTKEY` (F6), arrow steps, the
`PATH_HIT_R` grab radius, curve drawing density, colors, the
`PATH_WARPER_ORDER` warper list.

## Dependencies and tests

The folder uses Position Tuner helpers (`pt_showing`, `_pt_num`,
`PT_ANCHORS`) — `position_tuner/` must sit next to it. Tool state lives
outside rollback and player saves. Spline invariants and a screen smoke test —
`game/dev/path_tuner_regression_tests.rpy`.
