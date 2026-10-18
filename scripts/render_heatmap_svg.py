"""Draw data/contributions.json as contrib-heatmap.svg with a diagonal reveal."""
import json
import os
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "contributions.json"
OUT = ROOT / "contrib-heatmap.svg"
STATIC = os.environ.get("STATIC") == "1"

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]  # GitHub levels 0-4
CELL, GAP = 11, 4
PITCH = CELL + GAP
WEEKS = 53
WIDTH = 860
GRID_W = WEEKS * PITCH - GAP
GRID_X = (WIDTH - GRID_W) // 2
GRID_Y = 50
GRID_H = 7 * PITCH - GAP
HEIGHT = 192
BG, BORDER, TEXT, MUTED = "#0d1117", "#30363d", "#e6edf3", "#8b949e"
FONT = "-apple-system,Helvetica,Arial,sans-serif"


def main():
    payload = json.loads(DATA.read_text(encoding="utf-8"))
    days = payload["days"]
    s = payload["stats"]
    offset = (date.fromisoformat(days[0]["date"]).weekday() + 1) % 7  # weeks start on Sunday

    cells = []
    for i, d in enumerate(days):
        col, row = divmod(i + offset, 7)
        x, y = GRID_X + col * PITCH, GRID_Y + row * PITCH
        color = PALETTE[min(max(d["level"], 0), 4)]
        cls = "" if STATIC else ' class="c"'
        delay = "" if STATIC else f' style="animation-delay:{(col + row) * 0.02:.2f}s"'
        when = date.fromisoformat(d["date"]).strftime("%b %d, %Y")
        cells.append(
            f'<rect{cls}{delay} x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="2" fill="{color}">'
            f'<title>{d["count"]} contributions on {when}</title></rect>'
        )

    style = "" if STATIC else (
        "<style>.c{opacity:0;animation:fadein .4s ease forwards}"
        "@keyframes fadein{to{opacity:1}}</style>"
    )

    best = s["best_day"]
    best_when = date.fromisoformat(best["date"]).strftime("%b %d, %Y")
    footer_y = GRID_Y + GRID_H + 28
    stats_line = (
        f'Total {s["total"]:,}  ·  Current streak {s["current_streak"]}d  ·  '
        f'Longest {s["longest_streak"]}d  ·  Best day {best["count"]} on {best_when}'
    )

    # Less -> More legend, right-aligned on the footer line.
    more_end = GRID_X + GRID_W
    legend_start = more_end - 34 - 5 * 14 + 4
    legend = [f'<text x="{more_end}" y="{footer_y}" fill="{MUTED}" font-size="11" text-anchor="end" font-family="{FONT}">More</text>']
    for i, c in enumerate(PALETTE):
        legend.append(f'<rect x="{legend_start + i * 14}" y="{footer_y - 9}" width="10" height="10" rx="2" fill="{c}"/>')
    legend.append(f'<text x="{legend_start - 6}" y="{footer_y}" fill="{MUTED}" font-size="11" text-anchor="end" font-family="{FONT}">Less</text>')

    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" width="{WIDTH}" height="{HEIGHT}">'
        f"{style}"
        f'<rect x="0.5" y="0.5" width="{WIDTH - 1}" height="{HEIGHT - 1}" rx="10" fill="{BG}" stroke="{BORDER}"/>'
        f'<text x="{GRID_X}" y="30" fill="{TEXT}" font-size="14" font-weight="600" font-family="{FONT}">'
        f"Contributions in the last year</text>"
        f'{"".join(cells)}'
        f'<text x="{GRID_X}" y="{footer_y}" fill="{MUTED}" font-size="12" font-family="{FONT}">{stats_line}</text>'
        f'{"".join(legend)}</svg>'
    )
    OUT.write_text(svg, encoding="utf-8")
    print(f"wrote {OUT.name}")


if __name__ == "__main__":
    main()
