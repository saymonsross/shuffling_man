import argparse
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageChops, ImageStat


ITEMS = (
    ("blanket", ["Плед"], "Плед", (1490, 846)),
    ("pizza", ["Пицца"], "Коробка пиццы", (1455, 676)),
    ("ball", ["Мяч"], "Мяч", (220, 790)),
    ("stool_clothes", ["Шмот 3"], "Одежда на табурете", (584, 635)),
    ("floor_pillow", ["Подушка пол"], "Подушка на полу", (1740, 1003)),
    ("arm_clothes", ["Шмот 2"], "Одежда на подлокотнике", (1035, 609)),
    ("mug", ["кружка"], "Кружка", (940, 391)),
    ("juice", ["сок"], "Пакет сока", (856, 416)),
    ("wrapper", ["Пачка"], "Упаковка", (362, 400)),
    ("album", ["альбом", "Layer 51"], "Альбом и карандаши", (619, 426)),
    ("back_clothes", ["Шмот"], "Одежда на спинке дивана", (1430, 424)),
)


def photoshop_export(source, staging):
    # Photoshop preserves the authored Gradient Maps, which psd_tools ignores.
    jobs = [("bg", ["Background", "Layer 2", "Фон", "Подушка 1"])]
    jobs += [(key, layers) for key, layers, _, _ in ITEMS]
    script = """
(function () {
    var src = new File(SOURCE);
    var folder = new Folder(STAGING);
    var jobs = JOBS;
    var original = null;
    var wasOpen = false;
    var work = null;
    var previousDialogs = app.displayDialogs;
    try {
        app.displayDialogs = DialogModes.NO;
        for (var d = 0; d < app.documents.length; d++) {
            try {
                if (app.documents[d].fullName.fsName == src.fsName) {
                    original = app.documents[d]; wasOpen = true; break;
                }
            } catch (e) {}
        }
        if (!original) original = app.open(src);
        work = original.duplicate('cleanup_asset_export', false);
        if (!wasOpen) original.close(SaveOptions.DONOTSAVECHANGES);
        app.activeDocument = work;
        function save(name) {
            var opts = new PNGSaveOptions();
            opts.interlaced = false;
            work.saveAs(new File(folder.fsName + '/' + name + '.png'), opts, true, Extension.LOWERCASE);
        }
        save('full');
        for (var j = 0; j < jobs.length; j++) {
            for (var i = 0; i < work.layers.length; i++) work.layers[i].visible = false;
            for (var k = 0; k < jobs[j][1].length; k++) work.layers.getByName(jobs[j][1][k]).visible = true;
            save(jobs[j][0]);
        }
    } finally {
        if (work) work.close(SaveOptions.DONOTSAVECHANGES);
        app.displayDialogs = previousDialogs;
    }
}());
"""
    for token, value in (
        ("SOURCE", source.as_posix()),
        ("STAGING", staging.as_posix()),
        ("JOBS", jobs),
    ):
        script = script.replace(token, json.dumps(value, ensure_ascii=True))
    jsx = staging / "export.jsx"
    jsx.write_text(script, encoding="utf-8")
    quoted_path = str(jsx).replace("'", "''")
    subprocess.run(
        [
            "powershell.exe", "-NoProfile", "-Command",
            "$ErrorActionPreference = 'Stop'; "
            "$cleanupPhotoshop = New-Object -ComObject Photoshop.Application; "
            f"$cleanupPhotoshop.DoJavaScriptFile('{quoted_path}')",
        ],
        check=True,
    )


def package(source, staging, output):
    output.mkdir(parents=True, exist_ok=True)
    background = Image.open(staging / "bg.png").convert("RGBA")
    if background.size != (1920, 1080):
        raise ValueError(f"Unexpected canvas: {background.size}")
    if background.getchannel("A").getextrema() != (255, 255):
        raise ValueError("Clean background is not opaque")
    background.convert("RGB").save(output / "chapter_1_cleanup_room.png", optimize=True)
    assembled = background.copy()
    entries = []
    for key, layers, alt, click in ITEMS:
        layer = Image.open(staging / f"{key}.png").convert("RGBA")
        bounds = layer.getchannel("A").getbbox()
        if bounds is None or layer.getpixel(click)[3] < 250:
            raise ValueError(f"Missing or unsafe click target: {key}")
        asset_name = f"chapter_1_cleanup {key}.png"
        layer.crop(bounds).save(output / asset_name, optimize=True)
        assembled.alpha_composite(layer)
        entries.append({
            "key": key,
            "source_layers": layers,
            "image": f"images/1_chapter/cleanup/{asset_name}",
            "pos": list(bounds[:2]),
            "size": [bounds[2] - bounds[0], bounds[3] - bounds[1]],
            "alt": alt,
            "click": list(click),
        })
    full = Image.open(staging / "full.png").convert("RGB")
    difference = ImageChops.difference(assembled.convert("RGB"), full)
    stats = ImageStat.Stat(difference)
    if max(pair[1] for pair in stats.extrema) > 1:
        raise ValueError("Exported layers do not reproduce the native composition")
    assembled.convert("RGB").save(output / "chapter_1_cleanup_mess.png", optimize=True)
    manifest = {
        "source": str(source),
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "canvas": [1920, 1080],
        "method": "Native Photoshop export from an unsaved duplicate, original layer order and Gradient Maps preserved; transparent margins cropped without resampling.",
        "items_back_to_front": entries,
        "reassembled_mean_absolute_error": stats.mean,
        "reassembled_max_absolute_error": [pair[1] for pair in stats.extrema],
    }
    (staging / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    assembled.convert("RGB").save(staging / "reassembled.png")
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


def main():
    repository = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=repository.parent / "shuffling_man_assets/Черновик/Глава 1_сц_1 Начало/Ch_1_Living room _mess_2.psd")
    parser.add_argument("--output", type=Path, default=repository / "game/images/1_chapter/cleanup")
    parser.add_argument("--staging", type=Path)
    parser.add_argument("--package-only", action="store_true")
    args = parser.parse_args()
    staging = args.staging or Path(tempfile.mkdtemp(prefix="shuffling_cleanup_"))
    staging.mkdir(parents=True, exist_ok=True)
    source = args.source.resolve(strict=True)
    before = hashlib.sha256(source.read_bytes()).hexdigest()
    if not args.package_only:
        photoshop_export(source, staging.resolve())
    if hashlib.sha256(source.read_bytes()).hexdigest() != before:
        raise RuntimeError("Original PSD changed during export")
    package(source, staging, args.output)


if __name__ == "__main__":
    main()
