#!/usr/bin/env python3
"""OCR in-game Learn-screen screenshots into a compact CSV of skill rows.

Usage:
    python3 ocr_learn.py reference/*.png [--engine vision|tesseract]
                         [--out reference/learn.csv]

Engine: Apple Vision via the bundled ocr.swift helper (default, no deps) or
tesseract as fallback. Every OCR'd skill name is fuzzy-matched against
tools/skill-db/skills.json, so misreads either resolve to the real name or
get flagged — build_csv.py then price-validates every row, so an undetected
misread cannot silently survive. Rows that can't be resolved carry a `flag`
and the source screenshot path: read ONLY those images manually.

Output CSV: leading `#budget,<SP>` comment, then
    name,price,hint,obtained,desc,source,flag
- price is the shown (hint-discounted) Learn-screen number, blank if Obtained
- hint is 0..4 or "max" (0 = no hint chip seen)
- desc keeps the description text incl. the (style)/(distance) tag

Screenshots must be passed in scroll order (sort by filename works for
sequential screenshots); overlapping rows across screenshots are deduped,
preferring the complete (priced) copy and flagging price conflicts.
"""
import argparse
import csv
import json
import re
import subprocess
import sys
from difflib import SequenceMatcher
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_DB = HERE.parent / "skill-db" / "skills.json"
DEFAULT_OUT = HERE.parent.parent / "reference" / "learn.csv"

PRICE_RE = re.compile(r"^\d{2,4}$")
HINT_RE = re.compile(r"hint\s*lv.{0,2}\s*(\d|max)", re.IGNORECASE)
BUDGET_RE = re.compile(r"skill\s*points\s*([\d,]+)?", re.IGNORECASE)
UI_STOP_WORDS = ("confirm", "reset", "back", "full stats")
MATCH_THRESHOLD = 0.80
TIE_MARGIN = 0.02


def norm(s):
    """Lowercase, strip everything but letters/digits/spaces (kills ○◎☆♪ etc.)."""
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]", " ", s.lower())).strip()


def ocr_vision(paths):
    cmd = ["swift", str(HERE / "ocr.swift")] + [str(p) for p in paths]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        sys.exit(f"ocr.swift failed:\n{res.stderr}")
    return json.loads(res.stdout)


def ocr_tesseract(paths):
    out = {}
    for p in paths:
        res = subprocess.run(["tesseract", str(p), "stdout", "tsv"],
                             capture_output=True, text=True, check=True)
        rows = list(csv.DictReader(res.stdout.splitlines(), delimiter="\t"))
        page = next(r for r in rows if r["level"] == "1")
        pw, ph = float(page["width"]), float(page["height"])
        lines = {}
        for r in rows:
            if r["level"] != "5" or not r["text"].strip():
                continue
            key = (r["block_num"], r["par_num"], r["line_num"])
            lines.setdefault(key, []).append(r)
        out[str(p)] = [{
            "text": " ".join(w["text"] for w in ws),
            "x": min(int(w["left"]) for w in ws) / pw,
            "y": min(int(w["top"]) for w in ws) / ph,
            "w": (max(int(w["left"]) + int(w["width"]) for w in ws)
                  - min(int(w["left"]) for w in ws)) / pw,
            "h": max(int(w["height"]) for w in ws) / ph,
            "conf": min(float(w["conf"]) for w in ws) / 100,
        } for ws in lines.values()]
    return out


def glyph_rank(raw, name):
    """Order tied ◎/○/× tier variants by the glyph OCR actually saw."""
    tail = raw.strip()[-2:]
    if name.endswith("◎"):
        return 0 if ("◎" in tail or "@" in tail or "©" in tail) else 1
    if name.endswith("○"):
        return 0 if ("○" in tail or tail.rstrip().endswith("O")
                     or tail.rstrip().endswith("0")) else 1
    if name.endswith("×"):
        return 0 if ("×" in tail or tail.rstrip().lower().endswith("x")) else 1
    return 0


def match_name(text, db_names_norm):
    """Return (candidates, ratio): db names tied for best fuzzy match.

    Several db names collapse under norm() (◎/○/× tiers, case variants), so a
    normalized key maps to a LIST of names; ties are ordered by glyph evidence
    and left for price validation in build_csv.py to settle.
    """
    n = norm(text)
    if len(n) < 3:
        return [], 0.0
    scored = [(SequenceMatcher(None, n, dn).ratio(), names)
              for dn, names in db_names_norm.items()]
    scored.sort(key=lambda s: -s[0])
    best = scored[0][0]
    if best < MATCH_THRESHOLD:
        return [], best
    cands = [name for r, names in scored if r >= best - TIE_MARGIN
             for name in names]
    cands.sort(key=lambda name: glyph_rank(text, name))
    return cands, best


def parse_image(lines, db_names_norm, source):
    """Turn one screenshot's OCR lines into skill rows + maybe a budget."""
    lines = sorted(lines, key=lambda l: (l["y"], l["x"]))

    budget, top_cut, bottom_cut = None, 0.0, 1.0
    for l in lines:
        m = BUDGET_RE.search(l["text"])
        if m:
            top_cut = l["y"] + l["h"]
            if m.group(1):
                budget = int(m.group(1).replace(",", ""))
            else:  # number is a separate observation on the same band
                for o in lines:
                    if (PRICE_RE.match(o["text"].strip()) and o["x"] > l["x"]
                            and abs(o["y"] - l["y"]) < l["h"]):
                        budget = int(o["text"])
                        break
        if (norm(l["text"]) in UI_STOP_WORDS and l["y"] > 0.6
                and l["y"] < bottom_cut):
            bottom_cut = l["y"]

    body = [l for l in lines if top_cut < l["y"] + l["h"] / 2 < bottom_cut]

    anchors = []
    for l in body:
        cands, ratio = match_name(l["text"], db_names_norm)
        if cands:
            anchors.append((l, cands, ratio))
    # a name and its own description can both fuzzy-match; keep the better
    # match when two anchors are closer than a card's height
    deduped = []
    for a in sorted(anchors, key=lambda a: a[0]["y"]):
        if deduped and a[0]["y"] - deduped[-1][0]["y"] < 0.05:
            if a[2] > deduped[-1][2]:
                deduped[-1] = a
            continue
        deduped.append(a)
    anchors = deduped

    rows = []
    for i, (anchor, cands, ratio) in enumerate(anchors):
        y0 = anchor["y"] - 0.005
        y1 = anchors[i + 1][0]["y"] - 0.01 if i + 1 < len(anchors) else bottom_cut
        card = [l for l in body if y0 <= l["y"] + l["h"] / 2 < y1 and l is not anchor]

        price, hint, obtained, desc, flag = None, 0, False, [], []
        for l in card:
            t = l["text"].strip()
            xc = l["x"] + l["w"] / 2
            if PRICE_RE.match(t) and xc > 0.6:
                price = int(t) if price is None else price
            elif HINT_RE.search(t):
                g = HINT_RE.search(t).group(1).lower()
                hint = g if g == "max" else int(g)
            elif "obtained" in t.lower():
                obtained = True
            elif "% off" in t.lower() or t in ("+", "-", "—"):
                continue
            elif xc < 0.65:
                desc.append(t)

        if len(cands) > 1:
            flag.append("ambiguous-name:" + "|".join(cands))
        if not obtained and price is None:
            flag.append("no-price")
        rows.append({
            "name": cands[0], "candidates": cands, "price": price, "hint": hint,
            "obtained": obtained, "desc": " ".join(desc), "source": source,
            "flag": ";".join(flag),
        })
    return rows, budget


def dedupe(all_rows):
    merged = {}
    for r in all_rows:
        prev = merged.get(r["name"])
        if prev is None:
            merged[r["name"]] = r
        elif prev["price"] is None and not prev["obtained"]:
            merged[r["name"]] = r  # later copy is the complete one
        elif (r["price"] is not None and prev["price"] is not None
              and r["price"] != prev["price"]):
            prev["flag"] = ";".join(filter(None, [
                prev["flag"], f"price-conflict:{prev['price']}vs{r['price']}@{r['source']}"]))
    return list(merged.values())


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("images", nargs="+", type=Path)
    ap.add_argument("--engine", choices=("vision", "tesseract"), default="vision")
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--db", type=Path, default=DEFAULT_DB)
    args = ap.parse_args()

    db = json.loads(args.db.read_text(encoding="utf-8"))["skills"]
    db_names_norm = {}
    for name in db:
        db_names_norm.setdefault(norm(name), []).append(name)

    paths = sorted(args.images)
    ocr = ocr_vision(paths) if args.engine == "vision" else ocr_tesseract(paths)

    all_rows, budgets = [], []
    for p in paths:
        rows, budget = parse_image(ocr[str(p)], db_names_norm, p.name)
        all_rows.extend(rows)
        if budget:
            budgets.append(budget)

    rows = dedupe(all_rows)
    budget = max(set(budgets), key=budgets.count) if budgets else None

    with open(args.out, "w", newline="", encoding="utf-8") as f:
        f.write(f"#budget,{budget if budget is not None else 'UNKNOWN'}\n")
        w = csv.DictWriter(f, fieldnames=["name", "price", "hint", "obtained",
                                          "desc", "source", "flag"])
        w.writeheader()
        for r in rows:
            w.writerow({k: ("" if r[k] is None else r[k])
                        for k in w.fieldnames})

    flagged = [r for r in rows if r["flag"]]
    print(f"{len(rows)} skills, budget {budget} -> {args.out}")
    if budget is None:
        print("warning: budget not found in any screenshot header")
    for r in flagged:
        print(f"  FLAG {r['name']} ({r['source']}): {r['flag']}")
    if not flagged:
        print("no flags")


if __name__ == "__main__":
    main()
