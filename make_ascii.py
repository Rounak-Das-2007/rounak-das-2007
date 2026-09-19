#!/usr/bin/env python3
"""
Turn any image into ASCII art for the profile card.

    python make_ascii.py my_photo.jpg            # writes ascii_art.txt
    python make_ascii.py my_photo.jpg --invert   # dark subject on light background
    python make_ascii.py logo.png --cols 40 --rows 25 --contrast 1.6

Then rebuild the card:   python build_card.py

Tips
  * A close-up face/logo with a plain background works best.
  * If the result looks washed out, raise --contrast (1.4 - 2.2).
  * If the subject looks "inverted" (bright where it should be dark), add --invert.
"""
import argparse
from PIL import Image, ImageOps, ImageEnhance

# darkest -> brightest.  Feel free to tweak the character set.
RAMP = " .,:;|!ilrjk%M@"

# One character cell is roughly 10px wide x 20px tall in the SVG, so the source
# image is cropped to the same aspect ratio before being sampled.
CELL_W, CELL_H = 10, 20


def image_to_ascii(path, cols, rows, invert, contrast, gamma):
    img = Image.open(path)
    if img.mode in ("RGBA", "LA") or "transparency" in img.info:
        img = img.convert("RGBA")
        bg = Image.new("RGBA", img.size, (0, 0, 0, 255))
        img = Image.alpha_composite(bg, img)
    img = img.convert("L")

    # centre-crop to the card's aspect ratio
    target = (cols * CELL_W) / (rows * CELL_H)
    w, h = img.size
    if w / h > target:
        new_w = int(h * target)
        img = img.crop(((w - new_w) // 2, 0, (w - new_w) // 2 + new_w, h))
    else:
        new_h = int(w / target)
        img = img.crop((0, (h - new_h) // 2, w, (h - new_h) // 2 + new_h))

    img = ImageOps.autocontrast(img, cutoff=2)
    img = ImageEnhance.Contrast(img).enhance(contrast)
    img = img.resize((cols, rows), Image.LANCZOS)
    if invert:
        img = ImageOps.invert(img)

    lines = []
    for y in range(rows):
        row = ""
        for x in range(cols):
            v = (img.getpixel((x, y)) / 255) ** gamma
            row += RAMP[min(len(RAMP) - 1, int(v * len(RAMP)))]
        lines.append(row.rstrip())
    return lines


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Convert an image to ascii_art.txt")
    ap.add_argument("image")
    ap.add_argument("--out", default="ascii_art.txt")
    ap.add_argument("--cols", type=int, default=40)
    ap.add_argument("--rows", type=int, default=25)
    ap.add_argument("--invert", action="store_true")
    ap.add_argument("--contrast", type=float, default=1.3)
    ap.add_argument("--gamma", type=float, default=1.0)
    a = ap.parse_args()

    art = image_to_ascii(a.image, a.cols, a.rows, a.invert, a.contrast, a.gamma)
    with open(a.out, "w", encoding="utf-8") as f:
        f.write("\n".join(art) + "\n")
    print("\n".join(art))
    print(f"\nSaved {a.out} ({a.cols}x{a.rows}). Now run:  python build_card.py")
