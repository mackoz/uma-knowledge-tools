#!/usr/bin/env python3
"""Look up a skill in skills.json: gold/white partner, base cost, hint prices.

Usage:
    python3 lookup.py <name fragment> [more fragments...]

Case-insensitive substring match. For each hit, prints the skill, its gold or
white partner, and the Learn-screen price at every hint level — use this while
building an sp-optimizer CSV to sanity-check screenshot prices and prereqs.
Remember: a gold with an UNOWNED white shows a bundle price in game
(gold hint price + white hint price).
"""
import json
import sys
from pathlib import Path

HINT_LEVELS = [("no hint", 100), ("Lv1", 90), ("Lv2", 80),
               ("Lv3", 70), ("Lv4", 65), ("Max", 60)]  # price is floored


def show(name, entry, db):
    kind = "gold" if entry["gold"] else ("white" if entry["pair"] else "-")
    print(f"{name}  [id {entry['id']}, {kind}]")
    if entry["baseCost"]:
        prices = "  ".join(f"{lbl} {entry['baseCost']*p//100}" for lbl, p in HINT_LEVELS)
        print(f"  base {entry['baseCost']} SP -> {prices}")
    else:
        print("  base cost unknown (not purchasable / not in meta)")
    if entry["pair"]:
        partner = db.get(entry["pair"], {})
        rel = "white prereq" if entry["gold"] else "gold upgrade"
        print(f"  {rel}: {entry['pair']} (base {partner.get('baseCost', '?')} SP)")
    if entry.get("middle"):
        mid = db.get(entry["middle"], {})
        print(f"  bundle also includes: {entry['middle']} (base {mid.get('baseCost', '?')} SP)"
              " — include its ΔL in the gold row's value")


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__.strip())
    query = " ".join(sys.argv[1:]).lower()
    db = json.loads((Path(__file__).resolve().parent / "skills.json")
                    .read_text(encoding="utf-8"))["skills"]
    hits = {n: e for n, e in db.items() if query in n.lower()}
    if not hits:
        sys.exit(f"no skill matching {query!r}")
    for name, entry in sorted(hits.items()):
        show(name, entry, db)


if __name__ == "__main__":
    main()
