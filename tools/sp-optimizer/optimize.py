#!/usr/bin/env python3
"""Find the skill purchase set that maximizes total estimated L gain within an SP budget.

Usage:
    python3 optimize.py <skills.csv> <budget> [--top N] [--notes TEXT] [--no-log] [--keep-inputs]

CSV columns (header required):
    name      skill name
    cost      the SP price shown on the in-game Learn screen (hint-discounted),
              entered verbatim
    value     mean ΔL from the umalator skill chart (incremental vs current build)
    requires  (optional) name of prerequisite skill, e.g. the white base of a gold.
              For a gold whose base is unowned, set value = ΔL(gold) - ΔL(white).

Gold-skill pricing: when a gold's white prereq is unowned, the Learn screen shows
a BUNDLE price on the gold that already includes the white listed beneath it.
Enter that shown price and set `requires`; the effective cost used here is
cost(gold row) - cost(required row). When the white is already owned, the gold
shows only its own price — enter it with no `requires` and nothing is subtracted.
If tools/skill-db/skills.json exists, rows are cross-checked against it (known
gold missing `requires`, wrong prereq, cost not matching baseCost x hint discount)
and mismatches print warnings.

Each run is logged to runs/ next to this script (gitignored) unless --no-log is
given; use --notes to record the uma, course, and conditions in the log.

Each run also clears the repo's reference/ staging folder (the current run's
raw PDF/screenshot inputs) once the CSV has loaded — the log embeds the CSV
verbatim, so the raw inputs are disposable. Pass --keep-inputs to skip this
(e.g. when re-running mid-analysis).

Only include skills that can actually proc on the target course/style; see
knowledge/sp-minmaxing.md for the filtering method and caveats (recovery skills
and debuffs are not valued by the chart — handle them separately).
"""
import argparse
import csv
import json
import shutil
import sys
from datetime import datetime, timezone
from itertools import combinations
from pathlib import Path

HINT_PCTS = (100, 90, 80, 70, 65, 60)  # none, Lv1..Lv4, Max (price floored)


def load(path):
    with open(path, newline="", encoding="utf-8") as f:
        rows = []
        for row in csv.DictReader(f):
            rows.append({
                "name": row["name"].strip(),
                "cost": int(row["cost"]),        # shown Learn-screen price
                "value": float(row["value"]),
                "requires": (row.get("requires") or "").strip() or None,
            })
    by_name = {r["name"]: r for r in rows}
    for r in rows:
        r["display_cost"] = r["cost"]
    for r in rows:
        if r["requires"]:
            base = by_name.get(r["requires"])
            if base is None:
                sys.exit(f"error: {r['name']!r} requires unknown skill {r['requires']!r}")
            # shown gold price bundles the unowned white beneath it
            r["cost"] = r["display_cost"] - base["display_cost"]
            if r["cost"] <= 0:
                sys.exit(f"error: {r['name']!r} shown price {r['display_cost']} does not "
                         f"exceed its prereq {r['requires']!r} ({base['display_cost']})")
    cross_check(rows)
    return rows


def cross_check(rows):
    """Warn about rows inconsistent with tools/skill-db/skills.json, if present."""
    db_path = Path(__file__).resolve().parent.parent / "skill-db" / "skills.json"
    if not db_path.is_file():
        return
    db = json.loads(db_path.read_text(encoding="utf-8"))["skills"]
    for r in rows:
        name = r["name"].removesuffix(" (gold)").strip()
        entry = db.get(name)
        if entry is None:
            continue
        ok_requires = {entry["pair"], entry.get("middle")} - {None}
        if entry["gold"] and entry["pair"] and not r["requires"]:
            if any(row["name"].removesuffix(" (gold)").strip() == entry["pair"]
                   for row in rows):
                print(f"warning: {r['name']!r} and its white {entry['pair']!r} are both "
                      "listed but not linked with `requires` — the gold's shown price "
                      "bundles the white; add `requires` or you'll double-count")
            else:
                print(f"note: {r['name']!r} is the gold of {entry['pair']!r}; fine if the "
                      "white wasn't listed beneath it in-game (then the shown price is "
                      "standalone), but if it was, add a row + `requires`")
        elif r["requires"] and ok_requires and r["requires"] not in ok_requires:
            print(f"warning: {r['name']!r} requires {r['requires']!r} "
                  f"but skill-db pairs it with {entry['pair']!r}")
        if entry.get("middle") and r["requires"] != entry["middle"]:
            continue  # bundle also contains the ◎ tier; per-skill cost check n/a
        if entry.get("baseCost"):
            # the game floors discounted prices (90 SP at Lv4 -> 58)
            allowed = {entry["baseCost"] * p // 100 for p in HINT_PCTS}
            if r["cost"] not in allowed:
                print(f"warning: {r['name']!r} effective cost {r['cost']} doesn't match "
                      f"baseCost {entry['baseCost']} at any hint discount")


def clear_reference():
    """Empty the repo's reference/ staging folder of run inputs."""
    ref_dir = Path(__file__).resolve().parent.parent.parent / "reference"
    if not ref_dir.is_dir():
        return
    removed = []
    for entry in sorted(ref_dir.iterdir()):
        if entry.name == ".DS_Store":
            continue
        shutil.rmtree(entry) if entry.is_dir() else entry.unlink()
        removed.append(entry.name)
    if removed:
        print(f"cleared reference/ ({len(removed)} entries): {', '.join(removed)}\n")


def solve(items, budget):
    """Exhaustive search over subsets honoring prerequisites. Returns sorted results."""
    if len(items) > 22:
        sys.exit(f"error: {len(items)} items is too many for exhaustive search; "
                 "prune skills that can't proc first")
    results = []
    for k in range(len(items) + 1):
        for combo in combinations(items, k):
            names = {c["name"] for c in combo}
            if any(c["requires"] and c["requires"] not in names for c in combo):
                continue
            cost = sum(c["cost"] for c in combo)
            if cost > budget:
                continue
            value = sum(c["value"] for c in combo)
            results.append((round(value, 6), cost, tuple(sorted(names))))
    results.sort(key=lambda r: (-r[0], r[1]))
    return results


def render_report(items, results, budget, top):
    """Render the ranking / optimal set / alternatives as text sections."""
    by_name = {i["name"]: i for i in items}
    lines = [f"{len(items)} skills, budget {budget} SP", ""]

    def bundle_note(i):
        if i["display_cost"] != i["cost"]:
            return f"  (shown {i['display_cost']}, includes {i['requires']})"
        return ""

    lines.append("Efficiency ranking (L per 100 SP):")
    for i in sorted(items, key=lambda i: i["value"] / i["cost"], reverse=True):
        req = f"  (requires {i['requires']})" if i["requires"] else ""
        lines.append(f"  {i['value']/i['cost']*100:5.2f}  {i['name']:32s} "
                     f"{i['cost']:>4} SP  +{i['value']:.2f} L{req}{bundle_note(i)}")

    best = results[0]
    lines += ["", f"OPTIMAL: +{best[0]:.2f} L for {best[1]} SP (leftover {budget - best[1]})"]
    for name in best[2]:
        i = by_name[name]
        lines.append(f"  {name:32s} {i['cost']:>4} SP  +{i['value']:.2f} L{bundle_note(i)}")

    lines += ["", f"Top {top} sets:"]
    seen = set()
    for value, cost, names in results:
        if names in seen:
            continue
        seen.add(names)
        lines.append(f"  +{value:.2f} L / {cost:>3} SP: {', '.join(names)}")
        if len(seen) >= top:
            break
    return "\n".join(lines)


def write_log(csv_path, report, args, timestamp):
    runs_dir = Path(__file__).resolve().parent / "runs"
    runs_dir.mkdir(exist_ok=True)
    log_path = runs_dir / f"{timestamp:%Y-%m-%dT%H%M%SZ}-{csv_path.stem}.md"
    csv_text = csv_path.read_text(encoding="utf-8").rstrip()
    notes = args.notes or "(none)"
    log_path.write_text(f"""\
# sp-optimizer run — {timestamp:%Y-%m-%d %H:%M:%S} UTC

- **Command:** `python3 {' '.join(sys.argv)}`
- **Input:** `{csv_path}`
- **Budget:** {args.budget} SP
- **Notes:** {notes}

## Result

```
{report}
```

## Input CSV (verbatim)

```csv
{csv_text}
```

---
Caveats (see `knowledge/sp-minmaxing.md`): ΔL values come from the umalator skill
chart and assume additivity — re-sim the chosen set combined before buying.
Recovery skills and debuffs are not valued by the chart; check spurt rate separately.
""", encoding="utf-8")
    return log_path


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("csv_path", type=Path)
    ap.add_argument("budget", type=int)
    ap.add_argument("--top", type=int, default=5, help="show N best distinct sets")
    ap.add_argument("--notes", help="run context (uma, course, conditions) recorded in the log")
    ap.add_argument("--no-log", action="store_true", help="skip writing a log file to runs/")
    ap.add_argument("--keep-inputs", action="store_true",
                    help="don't clear the reference/ staging folder")
    args = ap.parse_args()

    items = load(args.csv_path)
    if not args.keep_inputs:
        clear_reference()
    results = solve(items, args.budget)
    report = render_report(items, results, args.budget, args.top)
    print(report)

    if not args.no_log:
        log_path = write_log(args.csv_path, report, args, datetime.now(timezone.utc))
        print(f"\nlogged to {log_path}")


if __name__ == "__main__":
    main()
