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
- Corner Adept ○ **not** owned this career, so Professor of Curvature costs 342+180 for the chain.

### Filtered out as dead

- Wrong style: Preferred Position, Pace Chaser Corners ○, Pace Chaser Savvy ○ (Pace Chaser), My True Strength (Pace/Long), Front Runner Savvy ○ (Front Runner), Straightaway Spurt, End Closer Corners ○ (End Closer).
- Wrong distance/surface: Shifting Gears, Opening Gambit (Mile), Extra Tank (Long), Forward, March! (Dirt).
- Wrong conditions: Fall Runner ○ (sim is summer).
- Absent from chart: **Ignited Spirit WIT** (dead here, same as career #1).
- Recovery/navigation, chart-unvalued; 1200m sprint so skipped: Straightaway Recovery, Lay Low, Calm in a Crowd, Go with the Flow, Meticulous Measures.
- Debuffs (chart can't value them; excluded, treat as unknown): Hesitant Front Runners 117, Subdued Late Surgers 130.

## Result

**OPTIMAL: +6.97 L for 2230 SP (33 leftover), 14 skills** (exhaustive over 19 candidates):

| Skill | SP | mean ΔL |
|---|---|---|
| Let's Pump Some Iron! | 130 | +2.00 |
| Nimble Navigator | 135 | +0.84 |
| No Stopping Me! (gold, over Nimble Navigator) | 270 | +0.74 |
| Ignited Spirit PWR | 180 | +0.76 |
| Ignited Spirit GUTS | 140 | +0.54 |
| Firm Conditions ○ | 58 | +0.24 |
| Firm Course Menace (gold, over Firm Conditions ○) | 246 | +0.32 |
| Position Pilfer | 180 | +0.25 |
| Fast & Furious (gold, over Position Pilfer) | 306 | +0.32 |
| Corner Adept ○ | 180 | +0.26 |
| Playtime's Over! | 144 | +0.25 |
| Ignited Spirit SPD | 120 | +0.22 |
| Right-Handed ○ | 81 | +0.13 |
| Sprint Straightaways ○ | 60 | +0.10 |

Exact tie at +6.97 (2260 SP, 3 leftover): swap **Fast & Furious + Sprint Straightaways ○** for **Burning Spirit SPD + Ramp Up**. Kept the primary set — Fast & Furious is a Late-Surger-tailored mid-race velocity gold with a tighter proc condition already satisfied by the style, and the tie set leaves the same expected L. Either is defensible.

Skipped by the optimizer: Professor of Curvature chain (342+180 for +0.59 total — priced out this career), It's On!/Ramp Up chain, Burning Spirit SPD, Outer Post Proficiency ○ (mean 0.04, median 0.00 — bracket lottery).

The 33 leftover SP buys nothing on the list (cheapest skipped item is Outer Post Proficiency ○ at 81, +0.04 — noise). Hesitant Front Runners (117) doesn't fit either.

## Caveats

- ΔL additivity assumed. **Re-sim the full final build in umalator before buying.**
- Variance: Let's Pump Some Iron! is again ultra-consistent (min 1.85); No Stopping Me! and Nimble Navigator can whiff (min 0.00) — they only proc when blocked in the last spurt, which is position-dependent.
- Debuff purchases (Hesitant Front Runners / Subdued Late Surgers) are outside the model; if bought, re-run with the reduced budget.
