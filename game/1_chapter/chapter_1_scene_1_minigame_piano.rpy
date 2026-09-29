## Пианино под метроном (ядро — common/minigame_piano.rpy): партии мелодии подряд.

define C1S1_PIANO_DIR = "audio/chapter_1_piano_minigame/"

## Эталон мелодии — MIDI: одна дорожка, шаги по несколько нот (бас + мелодия); октавы нот
## берутся из него, клавиатура — одна октава.
define C1S1_PIANO_PARTS = ("audio/keys/minigame_first_piano.mid",)

## "clean" / "flawed" / "skipped"; None — ещё не играли.
default c1s1_piano_outcome = None

## Такт — метроном сцены (C1S1_ARROW_HALF_T): он звучит всю игру, ядро держит такт по его позиции.
## Последний шаг не доигрывается: возврат — в момент обрушения нот, стук А и падение осколков
## ставит сцена.
label chapter_1_scene_1_minigame_piano:
    call minigame_piano(C1S1_PIANO_PARTS, c1s1_metronome_audio, C1S1_ARROW_HALF_T, C1S1_METRONOME_PHASE, "c1s1_piano_hand_step", 1) from _call_c1s1_minigame_piano
    $ c1s1_piano_outcome = _return
    return
