---
name: sp-optimizer
description: End-of-career SP min-max run for Uma Musume — turns staged inputs in reference/ (umalator chart PDF + Learn-screen screenshots) into an optimal skill buy list, a questions/ writeup, and a durable CSV. Use when the user asks for a new sp-optimizer run.
---

# SP optimizer run

All commands run in `tools/sp-optimizer/`. Inputs are staged by the user in `reference/`: one umalator skill-chart PDF (page print) and the full set of Learn-screen screenshots.

**Token rule: never Read the chart PDF/text or the screenshots.** The scripts below compress them; the only image you may Read is one specifically named in a `FLAG` line, to fix that one row.

## Steps

1. **Exclusions — ask once, up front** (skip if the invocation already says): use one AskUserQuestion covering (a) exclude debuff purchases? (b) exclude RNG golds (e.g. No Stopping Me!)? (c) anything else to rule out? This replaces the exclude-and-rerun loops of manual runs.

2. `python3 parse_chart.py "../../reference/<chart>.pdf"` → `reference/chart.csv`. Note the printed owned-legend list for the writeup.

3. `python3 ocr_learn.py ../../reference/*.png` → `reference/learn.csv` and the budget (from the Skill Points header). If it prints FLAG lines, they usually resolve in step 4; only act on ones that survive build_csv.

4. `python3 build_csv.py --style "<style>" --distance <band> [--exclude-debuffs] [--exclude "<name>"]... --out examples/<YYYY-MM-DD>-<uma>-<course>-careerN.csv`
   - Style/distance/course/conditions: from the user's message or the previous writeup for the same uma (`questions/`).
   - Read the report. Prune conditional greens that don't match the target race (wrong course/season/direction/post) by deleting their CSV rows — the report shows each with its ΔL.
   - `FLAG` lines are the only reason to Read a screenshot. Fix the CSV row, don't re-OCR.
   - Sanity: budget matches what the user said; candidate count ≤ 22; a "hidden ◎ tier" flag means constructing the middle row manually (see the career-3 writeup in `questions/`).

5. `python3 optimize.py <csv> <budget> --notes "<uma, course, conditions>"` — logs to `runs/`, clears `reference/`. Heed cross-check warnings; the expected note for a standalone gold (white not co-listed) is fine.

6. **Writeup**: new `questions/YYYY-MM-DD-sp-minmax-<uma>-….md` following the structure of the most recent sp-minmax file there (budget & obtained list, method links, pool differences, filtered-out lists from the build_csv report, result table with effective SP, skipped near-misses, caveats with chart min/median for consistency). Add the file to the worked-examples line in `knowledge/sp-minmaxing.md`.

7. **Reply** (one screen): buy-list table (skill, effective SP, ΔL), total ΔL/SP/leftover, notable skips from the Top-5 alternatives, variance caveats (min 0.00 skills), and the re-sim-in-umalator reminder.

**Do not commit** after the run — commit only when the user asks or the question is settled (standing preference).

If OCR fails wholesale (unreadable screenshots), fall back to the manual method in `knowledge/sp-minmaxing.md` (read images directly) rather than fighting the scripts mid-run.
