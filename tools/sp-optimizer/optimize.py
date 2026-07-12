#!/usr/bin/env python3
"""Find the skill purchase set that maximizes total estimated L gain within an SP budget.

Usage:
    python3 optimize.py <skills.csv> <budget> [--top N] [--notes TEXT] [--no-log] [--keep-inputs]

CSV columns (header required):
    name      skill name
    cost      actual SP cost from the in-game Learn screen (hint-discounted)
    value     mean ΔL from the umalator skill chart (incremental vs current build)
    requires  (optional) name of prerequisite skill, e.g. the white base of a gold.
              For a gold whose base is unowned, set value = ΔL(gold) - ΔL(white).

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
import shutil
import sys
from datetime import datetime, timezone
from itertools import combinations
from pathlib import Path


def load(path):
    with open(path, newline="", encoding="utf-8") as f:
        rows = []
        for row in csv.DictReader(f):
            rows.append({
                "name": row["name"].strip(),
                "cost": int(row["cost"]),
                "value": float(row["value"]),
                "requires": (row.get("requires") or "").strip() or None,
            })
    names = {r["name"] for r in rows}
    for r in rows:
        if r["requires"] and r["requires"] not in names:
            sys.exit(f"error: {r['name']!r} requires unknown skill {r['requires']!r}")
    return rows


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

    lines.append("Efficiency ranking (L per 100 SP):")
    for i in sorted(items, key=lambda i: i["value"] / i["cost"], reverse=True):
        req = f"  (requires {i['requires']})" if i["requires"] else ""
        lines.append(f"  {i['value']/i['cost']*100:5.2f}  {i['name']:32s} "
                     f"{i['cost']:>4} SP  +{i['value']:.2f} L{req}")

    best = results[0]
    lines += ["", f"OPTIMAL: +{best[0]:.2f} L for {best[1]} SP (leftover {budget - best[1]})"]
    for name in best[2]:
        i = by_name[name]
        lines.append(f"  {name:32s} {i['cost']:>4} SP  +{i['value']:.2f} L")

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
