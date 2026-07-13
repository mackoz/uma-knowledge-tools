#!/usr/bin/env python3
"""Join OCR'd Learn rows with chart values and skill-db into an optimizer CSV.

Usage:
    python3 build_csv.py --style "Late Surger" --distance Sprint
                         [--exclude-debuffs] [--exclude NAME ...]
                         [--learn reference/learn.csv]
                         [--chart reference/chart.csv]
                         [--out examples/<date>-draft.csv]

Classifies every Learn-screen row (obtained / dead style / dead distance /
debuff / recovery / unmodeled / excluded / candidate), links gold-white
chains from skill-db (`requires` + incremental ΔL), validates every price
against baseCost × hint discount, and resolves names ocr_learn.py flagged as
ambiguous (◎/○/× tiers) by which variant's base cost matches the price.

Prints a compact report; anything under FLAGS needs a human (or a look at the
named source screenshot). The output CSV is optimize.py-ready: shown prices
verbatim, golds suffixed " (gold)" with `requires` on bundle rows.

Conditional greens (course/season/direction/post) are NOT auto-filtered —
they appear as candidates with their chart value; prune ones that don't
match the target race before running optimize.py.
"""
import argparse
import csv
import json
import sys
from datetime import date
from pathlib import Path
import re

from optimize import HINT_PCTS  # (100, 90, 80, 70, 65, 60) — none, Lv1..4, Max

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
HINT_BY_LEVEL = {0: 100, 1: 90, 2: 80, 3: 70, 4: 65, "max": 60}
STYLE_TAGS = {"Front Runner", "Pace Chaser", "Late Surger", "End Closer"}
DIST_TAGS = {"Sprint", "Mile", "Medium", "Long"}
DEBUFF_RE = re.compile(
    r"^(slightly |moderately |greatly )?(decrease velocity|increase fatigue|startle)",
    re.IGNORECASE)
RECOVERY_RE = re.compile(
    r"recover endurance|decrease fatigue|take a breather", re.IGNORECASE)


def read_learn(path):
    budget, rows = None, []
    with open(path, newline="", encoding="utf-8") as f:
        first = f.readline().strip()
        if first.startswith("#budget,"):
            raw = first.split(",", 1)[1]
            budget = int(raw) if raw.isdigit() else None
        else:
            f.seek(0)
        for row in csv.DictReader(f):
            row["price"] = int(row["price"]) if row["price"] else None
            row["hint"] = row["hint"] if row["hint"] == "max" else int(row["hint"] or 0)
            row["obtained"] = row["obtained"] == "True"
            rows.append(row)
    return budget, rows


def read_chart(path):
    chart = {}
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(l for l in f if not l.startswith("#")):
            chart[row["name"]] = {k: float(row[k])
                                  for k in ("min", "max", "mean", "median")}
    return chart


def allowed_prices(base):
    return {base * p // 100 for p in HINT_PCTS}


def resolve_ambiguous(row, db, notes):
    """Pick among ◎/○/× tier candidates by which base cost fits the price."""
    flags = [f for f in row["flag"].split(";") if f]
    amb = next((f for f in flags if f.startswith("ambiguous-name:")), None)
    if not amb:
        return
    cands = [c for c in amb.split(":", 1)[1].split("|")
             if not c.endswith("×")]  # × greens are never sold on the Learn screen
    fits = [c for c in cands
            if row["price"] is not None and db.get(c, {}).get("baseCost")
            and row["price"] in allowed_prices(db[c]["baseCost"])]
    if len(fits) == 1 or len(cands) == 1:
        pick = fits[0] if len(fits) == 1 else cands[0]
        if pick != row["name"]:
            notes.append(f"{row['name']} -> {pick} (price fits baseCost)")
        row["name"] = pick
        flags.remove(amb)
        row["flag"] = ";".join(flags)


def tag_of(desc, tags):
    for m in re.findall(r"\(([^)]+)\)", desc):
        if m.strip() in tags:
            return m.strip()
    return None


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--style", required=True,
                    help='running style, e.g. "Late Surger"')
    ap.add_argument("--distance", required=True,
                    help="distance band: Sprint/Mile/Medium/Long")
    ap.add_argument("--exclude-debuffs", action="store_true")
    ap.add_argument("--exclude", action="append", default=[],
                    help="skill name to exclude (repeatable)")
    ap.add_argument("--learn", type=Path, default=REPO / "reference" / "learn.csv")
    ap.add_argument("--chart", type=Path, default=REPO / "reference" / "chart.csv")
    ap.add_argument("--db", type=Path, default=HERE.parent / "skill-db" / "skills.json")
    ap.add_argument("--out", type=Path,
                    default=HERE / "examples" / f"{date.today()}-draft.csv")
    args = ap.parse_args()

    budget, learn = read_learn(args.learn)
    chart = read_chart(args.chart)
    db = json.loads(args.db.read_text(encoding="utf-8"))["skills"]
    excl = {e.casefold() for e in args.exclude}

    buckets = {k: [] for k in ("obtained", "dead", "debuff", "recovery",
                               "unmodeled", "excluded", "negative", "candidate")}
    notes, flags = [], []
    for row in learn:
        resolve_ambiguous(row, db, notes)
        if row["flag"]:
            flags.append(f"{row['name']} ({row['source']}): {row['flag']}")
        name, desc = row["name"], row["desc"]
        style_tag = tag_of(desc, STYLE_TAGS)
        dist_tag = tag_of(desc, DIST_TAGS)
        if row["obtained"]:
            bucket = "obtained"
        elif name.casefold() in excl:
            bucket = "excluded"
        elif style_tag and style_tag != args.style:
            bucket = "dead"
        elif dist_tag and dist_tag != args.distance:
            bucket = "dead"
        elif DEBUFF_RE.match(desc) and args.exclude_debuffs:
            bucket = "debuff"
        elif name not in chart:
            bucket = "recovery" if RECOVERY_RE.search(desc) else "unmodeled"
        elif chart[name]["mean"] <= 0:
            bucket = "negative"
        else:
            bucket = "candidate"
        row["mean"] = chart.get(name, {}).get("mean")
        buckets[bucket].append(row)

    cand = {r["name"]: r for r in buckets["candidate"]}

    # link gold chains: requires + incremental value vs the immediate prereq
    for r in cand.values():
        entry = db.get(r["name"], {})
        r["gold"], r["requires"], r["value"] = entry.get("gold", False), None, r["mean"]
        if not (entry.get("gold") and entry.get("pair")):
            continue
        prereq = None
        if entry.get("middle"):
            if entry["middle"] in cand:
                prereq = entry["middle"]
            elif entry["pair"] in cand:
                flags.append(f"{r['name']}: bundle hides the ◎ tier "
                             f"({entry['middle']} not on the Learn screen) — construct "
                             "the middle row manually, see the career-3 writeup")
        if prereq is None and entry["pair"] in cand:
            prereq = entry["pair"]
        if prereq:
            r["requires"] = prereq
            r["value"] = round(r["mean"] - cand[prereq]["mean"], 2)
    # middle tiers (◎ of a green chain) require their ○
    for r in cand.values():
        entry = db.get(r["name"], {})
        if not r["requires"] and entry.get("pair") and not entry.get("gold"):
            golds = [g for g in cand.values()
                     if db.get(g["name"], {}).get("middle") == r["name"]]
            if golds and entry["pair"] in cand:
                r["requires"] = entry["pair"]
                r["value"] = round(r["mean"] - cand[entry["pair"]]["mean"], 2)

    # price validation: effective cost must equal baseCost x the seen hint
    for r in cand.values():
        base = db.get(r["name"], {}).get("baseCost")
        if not base or r["price"] is None:
            continue
        eff = r["price"] - (cand[r["requires"]]["price"] if r["requires"] else 0)
        expected = base * HINT_BY_LEVEL[r["hint"]] // 100
        if eff != expected:
            if eff in allowed_prices(base):
                notes.append(f"{r['name']}: price fits baseCost but not the OCR'd "
                             f"hint level ({r['hint']}) — hint chip likely misread")
            else:
                flags.append(f"{r['name']} ({r['source']}): effective {eff} SP matches "
                             f"no discount of baseCost {base} — check the screenshot")

    rows = list(cand.values())
    if len(rows) > 22:
        rows.sort(key=lambda r: r["value"], reverse=True)
        keep = {r["name"] for r in rows[:22]} | {r["requires"] for r in rows[:22]
                                                 if r["requires"]}
        dropped = [r for r in rows if r["name"] not in keep]
        rows = [r for r in rows if r["name"] in keep]
        notes.append("over optimize.py's 22-item cap; dropped lowest-value: "
                     + ", ".join(f"{r['name']} (+{r['value']})" for r in dropped))

    order = {r["name"]: i for i, r in enumerate(learn)}
    rows.sort(key=lambda r: order[r["name"]])
    with open(args.out, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["name", "cost", "value", "requires"])
        for r in rows:
            # suffix marks bundle rows (matches past CSVs); standalone golds
            # (white owned or absent) read cleaner without it
            suffix = " (gold)" if r["gold"] and r["requires"] else ""
            w.writerow([r["name"] + suffix, r["price"], f"{r['value']:.2f}",
                        r["requires"] or ""])

    def listing(key, with_price=True):
        return ", ".join(
            f"{r['name']}" + (f" {r['price']}" if with_price and r["price"] else "")
            for r in buckets[key]) or "(none)"

    print(f"budget: {budget if budget else 'UNKNOWN — ask the user'}")
    print(f"candidates: {len(rows)} -> {args.out}\n")
    for r in rows:
        c = chart[r["name"]]
        req = f"  requires {r['requires']}" if r["requires"] else ""
        print(f"  {r['name']:32s} shown {r['price']:>4}  ΔL {r['value']:+.2f}  "
              f"(min {c['min']:.2f} / med {c['median']:.2f}){req}")
    print()
    print(f"obtained:  {listing('obtained', with_price=False)}")
    print(f"dead:      {listing('dead')}")
    print(f"debuffs:   {listing('debuff')}" + (" [excluded]" if args.exclude_debuffs else ""))
    print(f"recovery:  {listing('recovery')}  [unmodeled by chart — stamina fix, "
          "check spurt rate]")
    print(f"unmodeled: {listing('unmodeled')}  [no chart value; not zero]")
    print(f"excluded:  {listing('excluded')}")
    print(f"negative:  {listing('negative')}")
    for n in notes:
        print(f"note: {n}")
    for fl in flags:
        print(f"FLAG: {fl}")
    if not flags:
        print("no flags")
    if budget:
        print(f"\nnext: python3 {HERE / 'optimize.py'} {args.out} {budget} "
              f"--notes '<uma, course, conditions>'")


if __name__ == "__main__":
    main()
