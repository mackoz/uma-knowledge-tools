#!/usr/bin/env python3
"""Find the skill purchase set that maximizes total estimated L gain within an SP budget.

Usage:
    python3 optimize.py <skills.csv> <budget> [--top N]

CSV columns (header required):
    name      skill name
    cost      actual SP cost from the in-game Learn screen (hint-discounted)
    value     mean ΔL from the umalator skill chart (incremental vs current build)
    requires  (optional) name of prerequisite skill, e.g. the white base of a gold.
              For a gold whose base is unowned, set value = ΔL(gold) - ΔL(white).

Only include skills that can actually proc on the target course/style; see
knowledge/sp-minmaxing.md for the filtering method and caveats (recovery skills
and debuffs are not valued by the chart — handle them separately).
"""
import argparse
import csv
import sys
from itertools import combinations


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


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("csv_path")
    ap.add_argument("budget", type=int)
    ap.add_argument("--top", type=int, default=5, help="show N best distinct sets")
    args = ap.parse_args()

    items = load(args.csv_path)
    by_name = {i["name"]: i for i in items}

    print(f"{len(items)} skills, budget {args.budget} SP\n")
    print("Efficiency ranking (L per 100 SP):")
    for i in sorted(items, key=lambda i: i["value"] / i["cost"], reverse=True):
        req = f"  (requires {i['requires']})" if i["requires"] else ""
        print(f"  {i['value']/i['cost']*100:5.2f}  {i['name']:32s} {i['cost']:>4} SP  +{i['value']:.2f} L{req}")

    results = solve(items, args.budget)
    best = results[0]
    print(f"\nOPTIMAL: +{best[0]:.2f} L for {best[1]} SP (leftover {args.budget - best[1]})")
    for name in best[2]:
        i = by_name[name]
        print(f"  {name:32s} {i['cost']:>4} SP  +{i['value']:.2f} L")

    print(f"\nTop {args.top} sets:")
    seen = set()
    for value, cost, names in results:
        if names in seen:
            continue
        seen.add(names)
        print(f"  +{value:.2f} L / {cost:>3} SP: {', '.join(names)}")
        if len(seen) >= args.top:
            break


if __name__ == "__main__":
    main()
