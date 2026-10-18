"""Fetch the contribution calendar for USER and save it to data/contributions.json."""
import json
import re
from datetime import datetime, timezone
from pathlib import Path

import requests
from bs4 import BeautifulSoup

USER = "MysticalMayfly"
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "contributions.json"
URL = f"https://github.com/users/{USER}/contributions"
COUNT = re.compile(r"(\d[\d,]*) contributions? on")


def parse_count(text):
    m = COUNT.search(text)
    return int(m.group(1).replace(",", "")) if m else 0


def fetch_days():
    r = requests.get(URL, headers={"User-Agent": "profile-art-script"}, timeout=30)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    tips = {t.get("for"): t.get_text(" ", strip=True) for t in soup.select("tool-tip")}
    days = {}
    for td in soup.select("td.ContributionCalendar-day"):
        date = td.get("data-date")
        if not date:
            continue
        days[date] = {
            "date": date,
            "level": int(td.get("data-level", 0)),
            "count": parse_count(tips.get(td.get("id"), "")),
        }
    return sorted(days.values(), key=lambda d: d["date"])


def stats(days):
    counts = [d["count"] for d in days]
    longest = run = 0
    for c in counts:
        run = run + 1 if c > 0 else 0
        longest = max(longest, run)
    # Today may not have a contribution yet, so an empty today does not break the streak.
    current = 0
    for i, d in enumerate(reversed(days)):
        if d["count"] > 0:
            current += 1
        elif i == 0:
            continue
        else:
            break
    best = max(days, key=lambda d: d["count"])
    return {
        "total": sum(counts),
        "current_streak": current,
        "longest_streak": longest,
        "best_day": {"date": best["date"], "count": best["count"]},
    }


if __name__ == "__main__":
    days = fetch_days()
    if len(days) < 300:
        raise SystemExit(f"Only {len(days)} days found; refusing to overwrite data.")
    payload = {
        "user": USER,
        "updated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "days": days,
        "stats": stats(days),
    }
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"wrote {OUT.name}: {len(days)} days, total {payload['stats']['total']}")
