"""Write info-card.svg: a neofetch-style card with a staggered reveal."""
import os
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "info-card.svg"
STATIC = os.environ.get("STATIC") == "1"

WIDTH, HEIGHT = 490, 290
BG, BORDER = "#0d1117", "#30363d"
TITLE_COLOR, KEY, VAL = "#7ee787", "#ff7b72", "#c9d1d9"
FONT = "monospace"

# Edit these lines to change the card.
TITLE = "mysticalmayfly@github"
INFO = [
    ("Now", "Building MysticalMayfly, my home for projects"),
    ("Prev", "Home OS, BOQ Tracker, World History Atlas"),
    ("Stack", "Everything Claude uses: Python, JS, HTML/CSS"),
    ("Projects", "Built for fun, e.g. GeM Sales Engine, 3D home"),
    ("Focus", "Vibe coding, but with production pipelines"),
]
# Colours from projects.json, shown as a bar at the bottom.
PROJECT_COLORS = ["#7c5cff", "#ff7a3d", "#ffa62b", "#00c2a0", "#3d8bff", "#ff4d7d", "#3fbf5f"]


def row(i, key, value):
    y = 84 + i * 32
    cls = "" if STATIC else ' class="r"'
    delay = "" if STATIC else f' style="animation-delay:{0.3 + i * 0.35:.2f}s"'
    return (
        f'<g{cls}{delay}>'
        f'<text x="24" y="{y}" fill="{KEY}" font-weight="bold" font-family="{FONT}" font-size="13">{escape(key)}</text>'
        f'<text x="112" y="{y}" fill="{VAL}" font-family="{FONT}" font-size="13">{escape(value)}</text>'
        f'</g>'
    )


def build_svg():
    style = "" if STATIC else (
        "<style>.r{opacity:0;animation:slide .5s ease forwards}"
        "@keyframes slide{from{opacity:0;transform:translateX(-6px)}to{opacity:1;transform:none}}</style>"
    )
    rows = "".join(row(i, k, v) for i, (k, v) in enumerate(INFO))
    bars = "".join(
        f'<rect x="{24 + i * 46}" y="{HEIGHT - 36}" width="40" height="10" rx="3" fill="{c}"/>'
        for i, c in enumerate(PROJECT_COLORS)
    )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" '
        f'width="{WIDTH}" height="{HEIGHT}">{style}'
        f'<rect x="0.5" y="0.5" width="{WIDTH - 1}" height="{HEIGHT - 1}" rx="10" fill="{BG}" stroke="{BORDER}"/>'
        f'<text x="24" y="28" fill="{TITLE_COLOR}" font-weight="bold" font-family="{FONT}" font-size="14">{escape(TITLE)}</text>'
        f'<line x1="24" y1="42" x2="{WIDTH - 24}" y2="42" stroke="{BORDER}"/>'
        f'{rows}{bars}</svg>'
    )


if __name__ == "__main__":
    OUT.write_text(build_svg(), encoding="utf-8")
    print(f"wrote {OUT.name}")
