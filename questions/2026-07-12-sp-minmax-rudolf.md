# 2026-07-12 — SP min-max: Symboli Rudolf @ Nakayama 1200m

**Question:** best way to spend end-of-career SP for Symboli Rudolf [Emperor's Path], **Late Surger**, target **Nakayama 1200m (outer, right), summer/firm** — same course as the [Curren Chan run](2026-07-11-sp-minmax.md).

## Budget

| | SP |
|---|---|
| Total available | 2059 |
| − 564 Escapades (pre-committed, hint Lv1) | 180 |
| − Dominator (pre-committed) | 160 |
| **Optimizer budget** | **1719** |

564 Escapades and Dominator were locked in by choice before optimizing and modeled as already owned. Note the chart values them at ~0 here: 564 Escapades mean 0.05 L, and Dominator is **Medium-gated so it can't proc at 1200m at all** (absent from the chart) — both are being bought for reasons outside this race.

## Method

Per [knowledge/sp-minmaxing.md](../knowledge/sp-minmaxing.md): umalator skill chart (mean ΔL, printed to PDF) × Learn-screen screenshots (hint-discounted costs) → filter dead skills → `tools/sp-optimizer` exact knapsack (run log: `tools/sp-optimizer/runs/2026-07-12T102307Z-…`, input CSV: `tools/sp-optimizer/examples/2026-07-12-symboli-rudolf-nakayama1200.csv`).

Chart-note: this chart pairs each value row with the skill name *below* it in `pdftotext` output, sorted by median descending; verified via owned skills (Corner Adept ○, Position Pilfer, 1,500,000 CC, Uma Stan → all 0.00).

### Filtered out as dead (absent from chart or 0.00)

- Wrong style: Speed Star / Prepared to Pass / Disorient / Pace Chaser Corners ○ (Pace Chaser), All Set (Pace/Long).
- Wrong distance/surface: Productive Plan, Mile Straightaways ○, Speed Eater (Mile), Thunderbolt Step, **Dominator** (Medium), Extra Tank (Long), Familiar Ground (Dirt).
- Wrong conditions: Left-Handed ○ (right-handed course), Sunny Days ○, Fall Runner ○ (sim is summer, weather not sunny), Chukyo/Hakodate Racecourse ○.
- Capped stats: **Nakayama Racecourse ○ reads 0.00** (81 SP saved — trust the chart, the stat boost lands on capped stats).
- Absent from chart with no obvious gate: **Ignited Spirit WIT** (treated as dead; wit navigation early-race apparently contributes nothing here).
- Recovery (chart-unvalued by design): Lay Low, A Small Breather — 1200m sprint, spurt rate is not a concern; skipped.
- Debuffs (chart can't value them; excluded, treat as unknown): Hesitant Front Runners 84, Hesitant Pace Chasers 117, Subdued Late Surgers 130, Flustered Late Surgers 117. Hesitant Front Runners is cheap — a candidate if leftover SP ever materializes.

## Result

**OPTIMAL: +8.61 L for 1719 SP — exactly the budget, 0 SP leftover** (exhaustive search over 19 candidates; beats greedy-by-efficiency, which reaches +8.50):

| Skill | SP | mean ΔL |
|---|---|---|
| Let's Pump Some Iron! | 160 | +1.93 |
| Slick Surge | 180 | +1.15 |
| On Your Left! (gold, over Slick Surge) | 342 | +1.02 |
| Leap Forward | 162 | +1.04 |
| Sprinting Gear | 144 | +0.99 |
| Ignited Spirit PWR | 140 | +0.66 |
| Corner Acceleration ○ | 144 | +0.53 |
| Ignited Spirit GUTS | 160 | +0.47 |
| Professor of Curvature (gold, over owned Corner Adept ○) | 126 | +0.29 |
| Sprint Corners ○ | 80 | +0.28 |
| Firm Conditions ○ | 81 | +0.25 |

Runner-up (+8.56, 1713 SP) swaps Professor of Curvature + Firm Conditions ○ for Ignited Spirit SPD — a 0.05 L difference, effectively noise.

Skipped by the optimizer: Burning Spirit SPD (gold increment only +0.29 for 260+120 SP), It's On!/Ramp Up chain (+0.35 for 442 SP), Playtime's Over!, Triumphant Pulse, 15,000,000 CC, Sprint Straightaways ○, Ignited Spirit SPD.

## Re-check: chart regenerated with 564 Escapades + Dominator owned

The sim was re-run with the two pre-committed skills added to the build (they show as owned: 564 Escapades reads 0.00, Dominator in the ✕ owned list), removing the "chart generated without them" caveat. CSV: `…-v2.csv`, run log `2026-07-12T102802Z-…`. Value shifts worth noting — both consistent with 564 Escapades' "activate 1 rare skill regardless of its conditions" effect:

- **On Your Left! total dropped 2.17 → 1.99** (increment over Slick Surge 1.02 → 0.81).
- **15,000,000 CC jumped 0.18 → 0.34** (max 0.25 → 2.04 — Escapades can force-proc it).
- Everything else moved ≤ 0.09.

New optimum is a **statistical tie** with the v1 set:

1. +8.55 L / 1677 SP: v1 set with Professor of Curvature → **15,000,000 CC** (42 SP leftover).
2. +8.55 L / 1719 SP: the **v1 set unchanged**.

**Decision: keep the v1 buy list** (all 11 skills above). Expected L is identical to 2 decimals, leftover SP is worthless at end of career, and the extra learned skill adds a bit of evaluation score. Adding 15,000,000 CC instead of Professor of Curvature is equally defensible.

## Caveats

- ΔL additivity assumed. **Re-sim the full final build in umalator before buying.**
- Mean hides variance: Let's Pump Some Iron! is remarkably consistent (min 1.74); Leap Forward/Sprinting Gear can whiff (min ~0). On Your Left!'s floor fell to 0.34 in the v2 chart.
