# RMB Editor

Sends a request to Claude straight from the running game. `Shift`+right-click
on an object pauses the frame and opens an input field; pressing `Enter` opens
a new Claude Code chat tab in VS Code with your text and the click context
already filled in: what was under the cursor, where it lives in the code,
where the script is, and what the frame looked like.

*Русская версия: [README.ru.md](README.ru.md)*

---

## Usage

1. Run the game in developer mode with the project open in VS Code.
2. Hold `Shift` and right-click a sprite, a button, a mini-game part or empty
   space. It works in a scene, in a mini-game, in the main menu and in the
   game menu.
3. Type what to do and press `Enter`.
4. VS Code comes to the front with a new Claude tab, the text placed in its
   input box. Press `Enter` once more, in VS Code. The extension has no
   auto-submit.

| Key | Action |
|---|---|
| `Shift`+RMB | open the field |
| `Enter` | send to a VS Code tab |
| `Shift+Enter` | new line |
| `Ctrl+V` | paste text |
| `Esc` | close without sending |

`Enter` on an empty field opens a tab with the context alone, so the prompt
can be typed in VS Code. A right-click without `Shift` behaves as usual.

Dev Hub (`F12`) has an **RMB Editor** row: it opens the field without a click
point, and the request carries the script position, screens and screenshot.

### Files

Drop a file from Explorer onto the game window to attach it to the request.
If the field is closed it opens; if it is open the file is added to the list
above the field. The `×` button removes an attachment. The request carries
the path; the file itself is neither copied nor modified.

A drop means "attach", not "here": the place in the scene is given by a click
or in the text. When the field opens near the bottom edge, the panel grows
upwards.

---

## Pause

While the field is open the game is paused the same way as under the game
menu: the script does not advance, game screens and their timers do not run,
and input does not reach the game. The screen shows a frozen shot of the
moment of the click.

- Sound keeps playing during the pause.
- Time does not stop. After the field closes, waits and animations behave as
  if the paused time had passed: a `pause` whose timeout has expired ends at
  once, and ATL is further along.
- A transition (`with`) running at the moment of the click is cancelled.
- Layer-wide effects from `config.layer_transforms` (parallax, posterize) keep
  being computed, as they do under the game menu; the scene camera and the
  sprites under the shot do not run.

---

## What Claude receives

In the tab's input box:

```
<your text>

Поймано в игре: prologue_dark_room · game/0_prologue/prologue_scene.rpy:95
Файлы:
- D:\SoundAssets\door_creak.wav
Контекст и скриншот: .rmb_editor/req_20260930_183344_055/request.md
```

If the text with attachments does not fit into the link (`RMB_URL_MAX`), the
input box receives only an instruction to read the request file; the full
text is in that file.

The request folder `.rmb_editor/req_<date>_<time>_<ms>/` in the project root:

| File | Contents |
|---|---|
| `request.md` | text, attachments and click context |
| `shot.png` | the frame without the input field, at game window size |

Click context in `request.md`:

- the point in 1920×1080 game coordinates and the same point in screenshot
  pixels;
- scene sprites under the point: tag with attributes, layer,
  pos/anchor/rotate/zoom as written in code, and the `show`/`scene` lines of
  that tag in script files;
- screen elements under the point: screen, type, visible text, size and the
  file:line where it is defined;
- script position, label and the screens being shown.

The last 10 requests are kept (`RMB_KEEP`); older ones are removed when a new
one is created. The folder is excluded from git and from builds. `Esc`
removes the folder of a cancelled request.

---

## Limitations

- **Sprite hit-testing** uses the rectangle of the drawn sprite, with camera
  and parallax applied but without transparency or overlap. Every sprite
  whose rectangle covers the point is included. In the main and game menus
  sprites are not collected.
- **Screen elements** are named by the screen statement that declares them.
  Content drawn by a single custom displayable cannot be told apart.
- **Pasting** joins multi-line text into one line; this is how Ren'Py's
  `input` works. Use `Shift+Enter` for a line break; long pastes are easier
  in the VS Code tab.
- **Several VS Code windows.** The link goes to the last active window; if
  another project is open there, the tab appears in it.
- **File drop right after the tool first appears** may need a full restart of
  the game: the list of window events is read once at startup.
- **Script reload while the field is open.** The field comes back with the
  same text, attachments and frame. The game position is restored the same
  way as with a regular `Shift+R`.
- **Request folder size.** A window-size screenshot takes several megabytes;
  ten requests take tens of megabytes.
- The tool targets Windows: the link is opened with `os.startfile`.

---

## Internals

- `rmb_editor.rpy` — click context, request file, link.
- `rmb_editor_ui.rpy` — gesture and file-drop catcher, pause, input field.

The input field lives in a new Ren'Py context, like the game menu, which is
what pauses the game. The background is the screenshot taken before the field
opens. Request data is kept in `renpy.session` and never reaches saves or
rollback.

Parameters are the `RMB_*` constants at the top of both files. Screens that
must not appear in the click context are listed in `RMB_SKIP_SCREENS`.

Tests live in `game/dev/rmb_editor_regression_tests.rpy`. Under tests the
real link is never opened.
