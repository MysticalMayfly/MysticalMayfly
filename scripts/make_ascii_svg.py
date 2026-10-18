"""Turn assets/portrait.png into an animated ASCII-art SVG. Run locally and commit the output."""
import os
from pathlib import Path
from xml.sax.saxutils import escape

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "assets" / "portrait.png"
OUT = ROOT / "ascii-portrait.svg"

COLS = 64                # characters across
CHAR_W = 7.2             # cell width in SVG units (12px monospace)
CHAR_H = 12              # line height in SVG units
RAMP = " .`:-=+*cs#%@"   # dark -> bright
FILL = "#58a6ff"
STATIC = os.environ.get("STATIC") == "1"  # frozen frame for local previews


def to_grid(path):
    img = Image.open(path).convert("RGBA")
    w, h = img.size
    rows = max(1, round((h / w) * COLS * CHAR_W / CHAR_H))
    img = img.resize((COLS, rows), Image.BOX)
    arr = np.asarray(img).astype(float)
    r, g, b, a = arr[..., 0], arr[..., 1], arr[..., 2], arr[..., 3]
    lum = (0.299 * r + 0.587 * g + 0.114 * b) / 255
    lum[a < 128] = 0  # transparent background becomes blank
    idx = np.clip((lum * (len(RAMP) - 1)).round().astype(int), 0, len(RAMP) - 1)
    return ["".join(RAMP[i] for i in row) for row in idx]


def build_svg(lines):
    width = COLS * CHAR_W
    height = len(lines) * CHAR_H
    style = "" if STATIC else "<style>.r{opacity:0;animation:fadein .4s ease forwards}@keyframes fadein{to{opacity:1}}</style>"
    rows = []
    for i, line in enumerate(lines):
        cls = "" if STATIC else ' class="r"'
        delay = "" if STATIC else f' style="animation-delay:{i * 0.03:.2f}s"'
        rows.append(f'<text x="0" y="{(i + 1) * CHAR_H - 2}"{cls}{delay} xml:space="preserve">{escape(line)}</text>')
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width:g} {height:g}" '
        f'width="{width:g}" height="{height:g}">{style}'
        f'<g font-family="monospace" font-size="12" fill="{FILL}">{"".join(rows)}</g></svg>'
    )


if __name__ == "__main__":
    OUT.write_text(build_svg(to_grid(SRC)), encoding="utf-8")
    print(f"wrote {OUT.name}")
