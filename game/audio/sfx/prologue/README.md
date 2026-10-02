# Звуки пролога

Файлы кладутся **сюда**: `game/audio/sfx/prologue/`.
Формат: **OGG Vorbis**, 48 kHz, q5–q6, пик ≈ −3 dBFS, без тишины в начале
(атака в первых ~5 мс). Громкость выставляется кодом; путь внутри `audio/sfx`
пишется без расширения.

| Файл | Длит. | Что это | Где вызывается |
|---|---|---|---|
| `pencil_grab.ogg` | 0.07 с | короткий сухой пластиковый щелчок-хват (Splice `ESM_HDLM_fx_foley_prop_digital_mouth_thermometer_plastic_case_cap_off_grab_single_03.wav`) | через 0.5 с после клика по «ВЗЯТЬ» у карандаша в письме (`prologue_scene.letter`) |
