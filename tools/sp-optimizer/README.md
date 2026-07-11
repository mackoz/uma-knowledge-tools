# SP Optimizer

Finds the skill purchase set that maximizes total estimated L gain within a skill-point budget — an exact 0/1 knapsack with prerequisite chains (gold skills needing their white base).

The method for gathering the input data (umalator skill chart for ΔL values, in-game Learn screen screenshots for hint-discounted costs) and its caveats live in [knowledge/sp-minmaxing.md](../../knowledge/sp-minmaxing.md).

## Usage

```
python3 optimize.py <skills.csv> <budget> [--top N]
```

Example (Curren Chan @ Nakayama 1200m, 524 SP — see [questions/2026-07-11-sp-minmax.md](../../questions/2026-07-11-sp-minmax.md)):

```
python3 optimize.py examples/2026-07-11-curren-chan-nakayama1200.csv 524
```

## Input CSV

| Column | Meaning |
|--------|---------|
| `name` | Skill name |
| `cost` | Actual SP cost from the Learn screen (hint discounts applied) |
| `value` | Mean ΔL from the umalator skill chart (incremental vs current build) |
| `requires` | Optional prerequisite skill name. For a gold whose white base is unowned, list the white as its own row and set the gold's `value` to ΔL(gold) − ΔL(white). |

Only include skills that can actually proc on the target course/style/conditions — filtering out dead skills is most of the work (and keeps the exhaustive search fast; it caps at 22 items).

Output: efficiency ranking, the optimal set, and the top N distinct sets so near-misses are visible.
