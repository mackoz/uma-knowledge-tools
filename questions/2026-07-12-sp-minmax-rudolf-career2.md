# 2026-07-12 — SP min-max: Symboli Rudolf career #2 @ Nakayama 1200m

**Question:** best way to spend end-of-career SP for a **second** Symboli Rudolf [Emperor's Path] career, **Late Surger**, target **Nakayama 1200m (outer, right), summer/firm** — same target as the [first Rudolf run](2026-07-12-sp-minmax-rudolf.md), different career so a different skill pool and different hint discounts.

## Budget

**2263 SP, no deductions.** Unlike the first career, the utility skills came from training: 564 Escapades, Dominator, Tether, and Uma Stan all show **Obtained** on the Learn screen (and read 0.00 / appear in the chart's owned ✕ legend). No pre-committed purchases this time.

## Method

Per [knowledge/sp-minmaxing.md](../knowledge/sp-minmaxing.md): umalator skill chart (mean ΔL, printed to PDF, generated with the owned skills in the build) × Learn-screen screenshots (hint-discounted costs) → filter dead skills → `tools/sp-optimizer` exact knapsack. Input CSV: `tools/sp-optimizer/examples/2026-07-12-symboli-rudolf-nakayama1200-career2.csv`, run log `tools/sp-optimizer/runs/2026-07-12T112639Z-…`.

Chart pairing (values row above name, sorted by median descending) verified against anchors: 564 Escapades and Uma Stan read 0.00; Nakayama Racecourse ○/◎ and Standard Distance ○/◎ read 0.00 (capped stats); Pace Chaser / End Closer / Mile / Long / Dirt skills absent.

### Key pool differences vs career #1

- No Slick Surge / On Your Left!, no Sprinting Gear, no Leap Forward, no 15,000,000 CC.
- Instead: **No Stopping Me!** (gold over Nimble Navigator — last-spurt maneuverability, chart total 1.58) and **Fast & Furious** (Late Surger gold over Position Pilfer).
- Let's Pump Some Iron! at Hint Lv4 → only 130 SP.
- Corner Adept ○ **not** owned this career, so Professor of Curvature's shown price (342) bundles it — see the correction below.

### Filtered out as dead

- Wrong style: Preferred Position, Pace Chaser Corners ○, Pace Chaser Savvy ○ (Pace Chaser), My True Strength (Pace/Long), Front Runner Savvy ○ (Front Runner), Straightaway Spurt, End Closer Corners ○ (End Closer).
- Wrong distance/surface: Shifting Gears, Opening Gambit (Mile), Extra Tank (Long), Forward, March! (Dirt).
- Wrong conditions: Fall Runner ○ (sim is summer).
- Absent from chart: **Ignited Spirit WIT** (dead here, same as career #1).
- Recovery/navigation, chart-unvalued; 1200m sprint so skipped: Straightaway Recovery, Lay Low, Calm in a Crowd, Go with the Flow, Meticulous Measures.
- Debuffs (chart can't value them; excluded, treat as unknown): Hesitant Front Runners 117, Subdued Late Surgers 130.

## ~~Result (first run — WRONG, superseded)~~

~~+6.97 L for 2230 SP, 14 skills~~ — this run **double-counted every gold chain**: it treated the gold's shown price as an *additional* cost on top of the white's, wasting ~537 phantom SP. See the correction below for what went wrong and the real answer.

## Correction: Learn-screen gold prices are bundles

Caught by the user after the first run: **when a gold's white prereq is unowned, the price shown on the gold already includes the white listed beneath it.** Fast & Furious "306" = 126 (its own base 180 at Hint Lv3) + 180 (Position Pilfer). Verified exactly for all six gold chains this career, cross-validated against base costs in `tools/skill-db/skills.json` (built from the umalator's own data — see `tools/skill-db/`).

Two consequences:

- `optimize.py` now computes a `requires` row's effective cost as *shown price − prereq's shown price*; CSVs keep recording shown prices verbatim.
- The Firm Conditions chain has a hidden middle tier: 246 (Firm Course Menace) = 117 gold (Lv1) + **71 Firm Conditions ◎ (Lv4)** + 58 ○ (Lv4) — the ◎ wasn't visible in the screenshots but the decomposition is exact. The CSV now models ○ → ◎ → gold explicitly (◎ contributes its own chart ΔL of 0.36).

**CORRECTED OPTIMAL: +8.22 L for 2235 SP (28 leftover), 17 skills** (run log `2026-07-12T115940Z-…`):

| Skill | effective SP | mean ΔL |
|---|---|---|
| Let's Pump Some Iron! | 130 | +2.00 |
| Nimble Navigator | 135 | +0.84 |
| No Stopping Me! (gold; shown 270) | 135 | +0.74 |
| Ignited Spirit PWR | 180 | +0.76 |
| Ignited Spirit GUTS | 140 | +0.54 |
| Firm Conditions ○ | 58 | +0.24 |
| Firm Conditions ◎ (shown ~129) | 71 | +0.36 |
| Firm Course Menace (gold; shown 246) | 117 | +0.56 |
| Position Pilfer | 180 | +0.25 |
| Fast & Furious (gold; shown 306) | 126 | +0.32 |
| Corner Adept ○ | 180 | +0.26 |
| Professor of Curvature (gold; shown 342) | 162 | +0.33 |
| Ignited Spirit SPD | 120 | +0.22 |
| Burning Spirit SPD (gold; shown 260) | 140 | +0.27 |
| Playtime's Over! | 144 | +0.25 |
| Ramp Up | 136 | +0.15 |
| Right-Handed ○ | 81 | +0.13 |

That's everything on the candidate list except It's On! (gold increment 136 for +0.18), Sprint Straightaways ○ (60, +0.10), and Outer Post Proficiency ○ (81, +0.04) — the corrected costs fit both big gold chains *and* the whole Ignited/Burning Spirit block. Runner-up +8.21/2240 swaps Ramp Up for Sprint Straightaways ○ + Outer Post Proficiency ○ — noise.

The 28 leftover SP buys nothing (cheapest skipped is Sprint Straightaways ○ at 60 for +0.10; adding it means dropping Ramp Up's +0.15). Hesitant Front Runners (117) still doesn't fit without dropping something better.

## Caveats

- ΔL additivity assumed. **Re-sim the full final build in umalator before buying.**
- Variance: Let's Pump Some Iron! is again ultra-consistent (min 1.85); No Stopping Me! and Nimble Navigator can whiff (min 0.00) — they only proc when blocked in the last spurt, which is position-dependent.
- Debuff purchases (Hesitant Front Runners / Subdued Late Surgers) are outside the model; if bought, re-run with the reduced budget.
