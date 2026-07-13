#!/usr/bin/env python3
"""Extract the umalator Skill Chart from a page-print PDF into a compact CSV.

Usage:
    python3 parse_chart.py <chart.pdf | chart.txt> [--out reference/chart.csv]

Accepts either the printed-to-PDF umalator page (runs `pdftotext -layout`,
poppler required) or an already-extracted text dump. Layout facts this relies
on (stable across runs so far): each skill's values line ("min L max L mean L
median L") appears BEFORE its name line with only blank lines between; page
headers and "N/M" page markers are noise; the table ends at "Uma 1"; the
trailing skill legend marks owned skills with a "✕" suffix.

Output CSV columns: name,min,max,mean,median (owned skills are NOT rows — they
show 0.00 in the chart; the owned list is printed and appended as comment
lines "#owned,<name>" for build_csv.py).
"""
import argparse
import csv
import re
import subprocess
import sys
import tempfile
from pathlib import Path

VALUES_RE = re.compile(
    r"^\s*(-?\d+\.\d+) L\s+(-?\d+\.\d+) L\s+(-?\d+\.\d+) L\s+(-?\d+\.\d+) L\s*$")
PAGE_MARKER_RE = re.compile(r"^\s*\d+/\d+\s*$")


def pdf_to_text(path):
    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as tmp:
        tmp_path = Path(tmp.name)
    subprocess.run(["pdftotext", "-layout", str(path), str(tmp_path)], check=True)
    text = tmp_path.read_text(encoding="utf-8")
    tmp_path.unlink()
    return text


def is_noise(line):
    s = line.strip()
    return (not s or PAGE_MARKER_RE.match(s)
            or ("Skill name" in s and "Minimum" in s))


def parse(text):
    """Return (rows, owned): chart value rows and the ✕-marked owned legend."""
    lines = text.splitlines()
    rows, owned = [], []
    pending = None  # values waiting for their name line
    in_table = True
    for line in lines:
        s = line.strip()
        if s == "Uma 1":
            in_table = False
        if in_table:
            m = VALUES_RE.match(line)
            if m:
                if pending is not None:
                    sys.exit(f"error: two values lines without a name between "
                             f"them near: {line.strip()!r}")
                pending = m.groups()
                continue
            if pending is not None and not is_noise(line):
                rows.append({"name": s, "min": pending[0], "max": pending[1],
                             "mean": pending[2], "median": pending[3]})
                pending = None
        else:
            if s.endswith("✕"):
                owned.append(s.removesuffix("✕").strip())
    if pending is not None:
        sys.exit("error: values line at end of table without a skill name")
    return rows, owned


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("input", type=Path, help="umalator chart PDF or pdftotext dump")
    ap.add_argument("--out", type=Path,
                    default=Path(__file__).resolve().parent.parent.parent
                    / "reference" / "chart.csv")
    args = ap.parse_args()

    text = (args.input.read_text(encoding="utf-8")
            if args.input.suffix == ".txt" else pdf_to_text(args.input))
    rows, owned = parse(text)
    if not rows:
        sys.exit("error: no chart rows found — layout changed?")

    with open(args.out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["name", "min", "max", "mean", "median"])
        w.writeheader()
        w.writerows(rows)
        for name in owned:
            f.write(f"#owned,{name}\n")

    print(f"{len(rows)} chart rows -> {args.out}")
    print(f"owned ({len(owned)}): {', '.join(owned) or '(none)'}")


if __name__ == "__main__":
    main()
