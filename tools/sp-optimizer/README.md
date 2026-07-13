# SP Optimizer

Finds the skill purchase set that maximizes total estimated L gain within a skill-point budget — an exact 0/1 knapsack with prerequisite chains (gold skills needing their white base).

The method for gathering the input data (umalator skill chart for ΔL values, in-game Learn screen screenshots for hint-discounted costs) and its caveats live in [knowledge/sp-minmaxing.md](../../knowledge/sp-minmaxing.md).

## Input pipeline (scripted; used by the `/sp-optimizer` skill)

Three scripts turn the raw inputs staged in `reference/` into an optimizer-ready CSV without anyone re-reading the PDFs/screenshots:

```
python3 parse_chart.py "../../reference/<chart>.pdf"   # → reference/chart.csv (+ owned ✕ legend)
python3 ocr_learn.py ../../reference/*.png             # → reference/learn.csv (+ budget from header)
python3 build_csv.py --style "Late Surger" --distance Sprint \
    [--exclude-debuffs] [--exclude "No Stopping Me!"] --out examples/<date>-<run>.csv
```

- `parse_chart.py` parses the umalator page-print PDF (values line precedes each skill name; owned skills carry a `✕` in the trailing legend).
- `ocr_learn.py` OCRs the Learn screenshots with Apple Vision (bundled `ocr.swift`; `--engine tesseract` as fallback), fuzzy-matches every name against `../skill-db/skills.json`, dedupes scroll overlap, and extracts the SP budget. Misreads can't survive silently: unresolved names/prices are flagged with their source screenshot.
- `build_csv.py` joins the two with skill-db: classifies rows (obtained / dead style/distance / debuff / recovery / unmodeled / candidate), links gold chains (`requires` + incremental ΔL), resolves ◎/○ ambiguity by base-cost fit, and validates every price against baseCost × hint discount. Conditional greens (course/season/direction) are left in with their chart values — prune the non-matching ones by hand. Anything under `FLAG` needs a human look at the named screenshot.

## Usage

```
python3 optimize.py <skills.csv> <budget> [--top N] [--notes TEXT] [--no-log] [--keep-inputs]
```

Example (Curren Chan @ Nakayama 1200m, 524 SP — see [questions/2026-07-11-sp-minmax.md](../../questions/2026-07-11-sp-minmax.md)):

```
python3 optimize.py examples/2026-07-11-curren-chan-nakayama1200.csv 524
```

## Input CSV

| Column | Meaning |
|--------|---------|
| `name` | Skill name |
| `cost` | The SP price **shown on the Learn screen**, entered verbatim (hint discounts applied) |
| `value` | Mean ΔL from the umalator skill chart (incremental vs current build) |
| `requires` | Optional prerequisite skill name. For a gold whose white base is unowned, list the white as its own row and set the gold's `value` to ΔL(gold) − ΔL(white). |

**Gold bundle pricing:** when a gold's white prereq is unowned, the game shows a *bundle* price on the gold that already includes the white listed beneath it (e.g. Fast & Furious "306" = 126 own + 180 Position Pilfer). Enter shown prices verbatim; for rows with `requires`, the optimizer uses shown − prereq's shown as the effective cost. When the white is already owned, the gold shows only its own price — omit `requires` and nothing is subtracted. Green-skill rare golds (e.g. Firm Course Menace) bundle a hidden ◎ tier too: model the chain ○ → ◎ → gold as three rows (see `tools/skill-db/README.md`).

If `../skill-db/skills.json` exists, every row is cross-checked against it (gold missing `requires` while its white is also listed, wrong prereq name, effective cost not matching baseCost × any hint discount) and mismatches print warnings.

Only include skills that can actually proc on the target course/style/conditions — filtering out dead skills is most of the work (and keeps the exhaustive search fast; it caps at 22 items).

Output: efficiency ranking, the optimal set, and the top N distinct sets so near-misses are visible.

## Run logs

Every run also writes a markdown log to `runs/` next to the script (gitignored — session data, not repo content), named `<UTC timestamp>-<csv stem>.md`. It records the command line, budget, notes, the full skill snapshot (costs, ΔL, efficiency), the optimal/alternative sets, and the input CSV verbatim so the run stays reproducible after the CSV changes. Pass `--notes "Curren Chan, Nakayama 1200m, firm"` to capture the context the CSV can't, or `--no-log` to skip logging.

## Input staging cleanup

The raw inputs for a run (umalator chart PDF, Learn-screen screenshots) are staged in the repo's `reference/` folder (gitignored). Because the run log embeds everything durable, each run **clears `reference/`** once the CSV loads successfully, so the folder only ever holds the current run's inputs. Pass `--keep-inputs` to skip clearing (e.g. when re-running mid-analysis while the screenshots are still needed).
