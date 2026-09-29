## Нарезка сэмплов клавиш пианино из записи game/audio/keys/keys_set_c3-b5.ogg
## (см. game/audio/chapter_1_piano_minigame/README.md). Запуск из корня проекта: python tools/cut_piano_keys.py
import struct, math, subprocess, os, re, glob, tempfile
S = tempfile.gettempdir()
P = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = P + "/game/audio/keys/keys_set_c3-b5.ogg"
OUT = P + "/game/audio/keys"
## Пик каждой ноты после нормализации, dBFS.
TARGET_DB = -4.0
FF = glob.glob(r"C:/Users/redch/AppData/Local/Microsoft/WinGet/Packages/Gyan.FFmpeg*/ffmpeg-*/bin/ffmpeg.exe")[0]

names = ["c", "c#", "d", "d#", "e", "f", "f#", "g", "g#", "a", "a#", "b"]
## Грубые моменты ударов (по огибающей) и их научные ноты по гармоническому ряду;
## имя файла — в системе проекта: на октаву выше научной (c3 файла = C2 = 65.4 Гц).
coarse = [0.0, 5.64, 11.29, 16.94, 22.58, 28.23, 33.88, 39.53, 45.17, 50.82, 56.47, 62.11, 67.76, 73.41, 79.05, 84.7,
    90.35, 96.0, 101.64, 107.29, 112.94, 118.58, 124.23, 129.88, 135.53, 141.17, 146.82, 152.47, 158.11, 163.76, 169.41, 175.06, 180.7]
midi = [36, 37, 38, 39, 40, 41, 42, 43, 45, 47, 48, 49, 50, 51, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71]
assert len(coarse) == len(midi)
label = lambda m: names[m % 12] + str(m // 12 - 1 + 1)

sr = 48000
raw = S + "/keyset48.raw"
if not os.path.exists(raw):
    subprocess.check_call([FF, "-v", "error", "-y", "-i", SRC, "-ac", "1", "-ar", str(sr), "-f", "s16le", "-t", "600", raw])
d = open(raw, "rb").read(); n = len(d) // 2
x = struct.unpack("<%dh" % n, d)
total = n / float(sr)

def onset(t):
    a, b = int((t - 0.08) * sr), int((t + 0.15) * sr)
    seg = x[max(a, 0):b]
    pk = max(abs(v) for v in seg)
    for i, v in enumerate(seg):
        if abs(v) > 0.06 * pk:
            return max(a, 0) / float(sr) + i / float(sr)
    return t

ons = [onset(t) for t in coarse]
plan = []
for i, (o, m) in enumerate(zip(ons, midi)):
    nxt = ons[i + 1] if i + 1 < len(ons) else total
    start = max(0.0, o - 0.003)
    length = min(nxt - 0.1, start + 5.0) - start
    plan.append((label(m), start, length))

def peak_db(args_in, length, extra_af=""):
    """Пик стерео-куска после фильтров: нормализация считается по тому, что реально кодируется."""
    af = ("%s," % extra_af if extra_af else "") + "volumedetect"
    r = subprocess.run([FF, "-v", "info", "-y"] + args_in + ["-t", "%.4f" % length, "-af", af, "-f", "null", "-"],
        capture_output=True, text=True)
    return float(re.search(r"max_volume: ([-0-9.]+) dB", r.stderr).group(1))

def encode(args_in, out, length, extra_af=""):
    gain_db = TARGET_DB - peak_db(args_in, length, extra_af)
    af = ("%s," % extra_af if extra_af else "") + "volume=%.2fdB,afade=t=out:st=%.3f:d=0.1" % (gain_db, length - 0.1)
    subprocess.check_call([FF, "-v", "error", "-y"] + args_in + ["-t", "%.4f" % length, "-af", af,
        "-ar", "48000", "-c:a", "libvorbis", "-q:a", "6", "-fs", "4000000", out])
    return gain_db

for lab, start, length in plan:
    g = encode(["-ss", "%.4f" % start, "-i", SRC], "%s/%s.ogg" % (OUT, lab), length)
    print("%-4s start %8.3f len %.2f gain %+.1f dB" % (lab, start, length, g))

## Пропущенные в записи ноты — сдвиг соседней на полутон (rubberband сохраняет длительность).
by = {lab: (start, length) for lab, start, length in plan}
for lab, src, semis in (("g#3", "g3", 1), ("a#3", "a3", 1), ("e4", "f4", -1)):
    start, length = by[src]
    g = encode(["-ss", "%.4f" % start, "-i", SRC], "%s/%s.ogg" % (OUT, lab), length,
        "rubberband=pitch=%.6f:pitchq=quality" % (2 ** (semis / 12.0)))
    print("%-4s <- %s %+d gain %+.1f dB" % (lab, src, semis, g))
print("done", len(plan) + 3)
