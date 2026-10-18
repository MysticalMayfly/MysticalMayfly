"""Write info-card.svg: a neofetch-style card with a staggered reveal."""
import os
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "info-card.svg"
STATIC = os.environ.get("STATIC") == "1"

WIDTH = 490
LINE_H = 28
TOP = 80
BG, BORDER = "#0d1117", "#30363d"
TITLE_COLOR, BULLET, VAL = "#7ee787", "#ff7b72", "#c9d1d9"
FONT = "monospace"

# Edit these lines to change the card. "item" lines get a bullet.
TITLE = "mysticalmayfly@github"
LINES = [
    ("text", "I build stuff just for fun."),
    ("text", "I vibe code, so I use whatever Claude uses."),
    ("text", "Not the lazy kind, though. Lately I'm deep"),
    ("text", "into how real production pipelines work:"),
    ("item", "Git branches and pull requests"),
    ("item", "Databases, Supabase auth and OAuth"),
    ("item", "CD pipeline with Netlify"),
    ("item", "GitHub Actions that keep this page updated"),
    ("text", "That's about it."),
]
ACCENTS = ["#7c5cff", "#ff7a3d", "#ffa62b", "#00c2a0", "#3d8bff", "#ff4d7d", "#3fbf5f"]

BARS_Y = TOP + len(LINES) * LINE_H
HEIGHT = BARS_Y + 34


def line(i, kind, text):
    y = TOP + i * LINE_H
    cls = "" if STATIC else ' class="r"'
    delay = "" if STATIC else f' style="animation-delay:{0.3 + i * 0.25:.2f}s"'
    body = f'<text x="{44 if kind == "item" else 24}" y="{y}" fill="{VAL}" font-family="{FONT}" font-size="13">{escape(text)}</text>'
    if kind == "item":
        body = f'<text x="26" y="{y}" fill="{BULLET}" font-weight="bold" font-family="{FONT}" font-size="13">›</text>' + body
    return f"<g{cls}{delay}>{body}</g>"


def build_svg():
    style = "" if STATIC else (
        "<style>.r{opacity:0;animation:slide .5s ease forwards}"
        "@keyframes slide{from{opacity:0;transform:translateX(-6px)}to{opacity:1;transform:none}}</style>"
    )
    lines = "".join(line(i, k, t) for i, (k, t) in enumerate(LINES))
    bars = "".join(
        f'<rect x="{24 + i * 46}" y="{BARS_Y}" width="40" height="10" rx="3" fill="{c}"/>'
        for i, c in enumerate(ACCENTS)
    )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" '
        f'width="{WIDTH}" height="{HEIGHT}">{style}'
        f'<rect x="0.5" y="0.5" width="{WIDTH - 1}" height="{HEIGHT - 1}" rx="10" fill="{BG}" stroke="{BORDER}"/>'
        f'<text x="24" y="28" fill="{TITLE_COLOR}" font-weight="bold" font-family="{FONT}" font-size="14">{escape(TITLE)}</text>'
        f'<line x1="24" y1="42" x2="{WIDTH - 24}" y2="42" stroke="{BORDER}"/>'
        f'{lines}{bars}</svg>'
    )


if __name__ == "__main__":
    OUT.write_text(build_svg(), encoding="utf-8")
    print(f"wrote {OUT.name}")
