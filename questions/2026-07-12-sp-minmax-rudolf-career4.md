# 2026-07-12 — SP min-max: Symboli Rudolf career #4 @ Nakayama 1200m

**Question:** best way to spend end-of-career SP for a **fourth** Symboli Rudolf [Emperor's Path] career, **Late Surger**, target **Nakayama 1200m (outer, right), summer/firm** — same target as careers [#1](2026-07-12-sp-minmax-rudolf.md), [#2](2026-07-12-sp-minmax-rudolf-career2.md), [#3](2026-07-12-sp-minmax-rudolf-career3.md). Per user, up front: **no No Stopping Me!, no debuff purchases.**

## Budget

**1858 SP, no deductions.** In-career training granted 564 Escapades, Let's Pump Some Iron!, **Firm Course Menace (with Firm Conditions ◎)**, Dominator, and Uma Stan (all show **Obtained**) — the first career where two of the usual top buys (LPSI, Firm chain) came free.

## Method

Per [knowledge/sp-minmaxing.md](../knowledge/sp-minmaxing.md): umalator skill chart (mean ΔL, printed to PDF) × 13 Learn-screen screenshots (hint-discounted shown prices recorded verbatim; optimizer subtracts prereq bundles) → filter dead skills → `tools/sp-optimizer` exact knapsack. Input CSV: `tools/sp-optimizer/examples/2026-07-12-symboli-rudolf-nakayama1200-career4.csv`, run log `tools/sp-optimizer/runs/2026-07-13T014627Z-…`.

All five candidate gold bundles decomposed exactly against `tools/skill-db` base costs (On Your Left! 342 = 162 Lv1 + 180 Slick Surge; Fast & Furious 306 = 126 Lv3 + 180 Position Pilfer; It's On! 272 = 136 Lv2 + 136 Ramp Up Lv2; Burning Spirit SPD 260 = 140 Lv3 + 120 Ignited Spirit SPD Max; Professor of Curvature 360 = 180 + 180 Corner Adept ○, no hints). Cross-check passed (expected Playtime's Over! standalone note only — See Ya Later! not co-listed, 144 is the exact standalone Lv1 price).

### Key pool differences vs career #3

- **LPSI and the whole Firm chain are pre-owned** — ~360 SP of last run's buys came free, but the budget is also ~200 lower (1858 vs 2065) and chart values run smaller overall (top buy +0.94 vs +1.93).
- **Fast & Furious / Position Pilfer are back** (absent in #3); **Sprinting Gear and Ignited Spirit GUTS are gone**.
- **Corner Acceleration ○** offered for the first time — 126 at Hint Lv3 for +0.45 mean (but median 0.00; it can proc on a non-final corner).
- No Right-Handed ○ / Summer Runner ○ greens this time (only ◎ tiers exist in the chart, not offered on the Learn screen).

### Excluded per user

No Stopping Me! 270 (Nimble Navigator kept as candidate); debuffs: Trick (Rear) 126, Hesitant Front Runners 117, Subdued Late Surgers 130, Hesitant Late Surgers 91, Sharp Gaze 117, Tether (price not captured — cut off between screenshots, moot).

### Filtered out as dead

- Wrong course: Hakodate Racecourse ○ 63.
- Wrong style (Pace Chaser): Preferred Position 180, Prepared to Pass 126, Pace Chaser Corners ○ 130, Hydrate 144, Pace Chaser Savvy ○ 99, Head-On 126.
- Wrong distance: Productive Plan 128 + Updrafters 144 (Mile), Steadfast 128 + With All My Soul 128 (Medium), Deep Breaths 112 + Long Straightaways ○ 70 (Long).
- Absent from chart (unmodeled; value unknown, not zero): **Meticulous Measures 112** (Sprint-valid positioning, again the one real unknown), Go with the Flow 108, Ignited Spirit WIT 120.
- Recovery blues (chart strips HP by design): Calm in a Crowd 119, Be Still 144.

## Result

**OPTIMAL: +5.53 L for 1838 SP (20 leftover), 13 skills** (run log `2026-07-13T014627Z-…`):

| Skill | effective SP | mean ΔL |
|---|---|---|
| Slick Surge | 180 | +0.94 |
| On Your Left! (gold; shown 342) | 162 | +0.60 |
| Nimble Navigator | 135 | +0.65 |
| Louder! Tracen Cheer! | 160 | +0.56 |
| Ignited Spirit PWR | 140 | +0.53 |
| Corner Acceleration ○ | 126 | +0.45 |
| Fast & Furious (gold; shown 306) | 126 | +0.33 |
| Position Pilfer | 180 | +0.25 |
| Ignited Spirit SPD | 120 | +0.22 |
| Burning Spirit SPD (gold; shown 260) | 140 | +0.28 |
| Late Surger Corners ○ | 117 | +0.25 |
| Competitive Spirit ○ | 72 | +0.17 |
| Triumphant Pulse | 180 | +0.30 |

Skipped: Professor of Curvature + Corner Adept ○ (360 for +0.54), It's On! + Ramp Up (272 for +0.34), Playtime's Over! (144 for +0.25), Straightaway Adept (153 for +0.13), Straightaway Acceleration (136 for +0.09), Inner Post Proficiency ○ (63 for +0.02).

Runner-up +5.50/1842 swaps Burning Spirit SPD for Playtime's Over! (−0.03 L). The Corner Adept ○ → Professor of Curvature chain never makes the top 5 — at 0.12/0.18 L per 100 SP it's below everything bought.

## Caveats

- ΔL additivity assumed. **Re-sim the full 13-skill build in umalator before buying.**
- Consistency: Slick Surge (min 0.47) and On Your Left! (min 0.34) are near-guaranteed; Louder! Tracen Cheer! min 0.37. **Corner Acceleration ○ is high-variance** (median 0.00 — often procs on an early corner for nothing); Nimble Navigator (min 0.00) only procs when blocked in the last spurt.
- Meticulous Measures (112, Sprint-valid) unvalued by the chart again, not worthless — re-check if it ever gets modeled.
