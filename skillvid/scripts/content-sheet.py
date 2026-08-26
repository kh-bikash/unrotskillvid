#!/usr/bin/env python3
"""Build a reviewable storyboard content sheet from snapshot PNGs.

    python content-sheet.py --frames snapshots/frames --spec sheet.json \
                            --out snapshots/content-sheet.jpg

sheet.json:

    {
      "title":    "Passing Note  /  storyboard v6",
      "subtitle": "Every cut lands inside a real pause in the voiceover.",
      "meta":     "1080x1920  ·  29.0s  ·  4 scenes  ·  no render",
      "theme":    "dark",
      "cols":     4,
      "tiles": [
        { "file": "frame-00-at-3s.png", "index": "01", "name": "Hook",
          "time": "0.0 – 3.6s", "note": "words cascade; highlight on the spoken word",
          "vo":   "Claude Code agents can finally talk to each other." }
      ]
    }

`note` is the important field — say what the CAMERA or the MOTION is doing at that instant.
A sheet of pretty stills is decoration; a sheet that explains each moment is reviewable.

Requires Pillow.
"""

import argparse
import json
import pathlib
import sys

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    sys.exit("Pillow is required:  pip install pillow")

THEMES = {
    "dark":  {"bg": "#16120F", "fg": "#F7F2EB", "muted": "#A79C91",
              "rule": "#3B332B", "accent": "#D97757"},
    "light": {"bg": "#FBF7F1", "fg": "#241E19", "muted": "#6B615A",
              "rule": "#E4D9CE", "accent": "#D97757"},
}

FONT_CANDIDATES = {
    False: ["segoeui.ttf", "arial.ttf", "DejaVuSans.ttf", "Helvetica.ttc"],
    True:  ["segoeuib.ttf", "arialbd.ttf", "DejaVuSans-Bold.ttf", "Helvetica.ttc"],
}
FONT_DIRS = ["C:/Windows/Fonts", "/usr/share/fonts/truetype/dejavu", "/System/Library/Fonts"]


def font(size, bold=False):
    for d in FONT_DIRS:
        for name in FONT_CANDIDATES[bold]:
            p = pathlib.Path(d) / name
            if p.exists():
                try:
                    return ImageFont.truetype(str(p), size)
                except OSError:
                    continue
    return ImageFont.load_default()


def wrap(draw, text, fnt, max_width):
    lines, line = [], ""
    for word in text.split():
        probe = f"{line} {word}".strip()
        if draw.textlength(probe, font=fnt) <= max_width:
            line = probe
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--frames", required=True, help="directory holding the snapshot PNGs")
    ap.add_argument("--spec", required=True, help="sheet.json")
    ap.add_argument("--out", required=True)
    ap.add_argument("--thumb-width", type=int, default=460)
    ap.add_argument("--aspect", default="9:16", help="tile aspect, w:h (default 9:16)")
    args = ap.parse_args()

    spec = json.loads(pathlib.Path(args.spec).read_text(encoding="utf-8"))
    tiles = spec.get("tiles") or sys.exit("spec has no tiles")
    C = THEMES.get(spec.get("theme", "dark"), THEMES["dark"])
    cols = int(spec.get("cols", 4))

    aw, ah = (int(v) for v in args.aspect.split(":"))
    TW = args.thumb_width
    TH = round(TW * ah / aw)
    M, GAP, ROW_GAP = 56, 28, 48
    HEADER, LABEL, VO = 172, 96, 84

    rows = (len(tiles) + cols - 1) // cols
    W = M * 2 + TW * cols + GAP * (cols - 1)
    cell = LABEL + TH + VO
    H = HEADER + cell * rows + ROW_GAP * (rows - 1) + M

    canvas = Image.new("RGB", (W, H), C["bg"])
    d = ImageDraw.Draw(canvas)

    f_title, f_meta = font(32, True), font(23)
    f_num, f_name = font(26, True), font(26, True)
    f_time, f_note, f_vo = font(22, True), font(21), font(21)

    d.ellipse([M, 62, M + 22, 84], fill=C["accent"])
    d.text((M + 38, 56), spec.get("title", "Storyboard"), font=f_title, fill=C["fg"])
    meta = spec.get("meta", "")
    if meta:
        d.text((W - M - d.textlength(meta, font=f_meta), 64), meta, font=f_meta, fill=C["muted"])
    if spec.get("subtitle"):
        d.text((M + 38, 102), spec["subtitle"], font=f_meta, fill=C["muted"])
    d.rectangle([M, HEADER - 26, W - M, HEADER - 24], fill=C["rule"])

    frames_dir = pathlib.Path(args.frames)
    for i, t in enumerate(tiles):
        x = M + (i % cols) * (TW + GAP)
        y = HEADER + (i // cols) * (cell + ROW_GAP)

        if t.get("index"):
            d.text((x, y), t["index"], font=f_num, fill=C["accent"])
        d.text((x + 48, y), t.get("name", ""), font=f_name, fill=C["fg"])
        d.text((x, y + 38), t.get("time", ""), font=f_time, fill=C["muted"])
        if t.get("note"):
            d.text((x, y + 66), t["note"], font=f_note, fill=C["accent"])

        src = frames_dir / t["file"]
        if not src.exists():
            sys.exit(f"missing frame: {src}")
        im = Image.open(src).convert("RGB").resize((TW, TH), Image.Resampling.LANCZOS)
        canvas.paste(im, (x, y + LABEL))
        d.rectangle([x, y + LABEL, x + TW - 1, y + LABEL + TH - 1], outline=C["rule"], width=2)

        if t.get("vo"):
            vy = y + LABEL + TH + 16
            for line in wrap(d, f'"{t["vo"]}"', f_vo, TW)[:3]:
                d.text((x, vy), line, font=f_vo, fill=C["muted"])
                vy += 26

    out = pathlib.Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(out, "JPEG", quality=94, subsampling=0, optimize=True)
    print(f"Wrote {out} ({canvas.width}x{canvas.height}, {len(tiles)} tiles)")


if __name__ == "__main__":
    main()
