# 2026-07-12 — SP min-max: Symboli Rudolf career #3 @ Nakayama 1200m

**Question:** best way to spend end-of-career SP for a **third** Symboli Rudolf [Emperor's Path] career, **Late Surger**, target **Nakayama 1200m (outer, right), summer/firm** — same target as [career #1](2026-07-12-sp-minmax-rudolf.md) and [career #2](2026-07-12-sp-minmax-rudolf-career2.md), different skill pool and hint discounts.

## Budget

**2065 SP, no deductions.** In-career training already granted 564 Escapades, Lay Low, Dominator, and Tether (all show **Obtained** on the Learn screen; the chart's owned ✕ legend lists 564 Escapades, Kyoto Racecourse ○, Lay Low, Dominator).

## Method

Per [knowledge/sp-minmaxing.md](../knowledge/sp-minmaxing.md): umalator skill chart (mean ΔL, printed to PDF) × 13 Learn-screen screenshots (hint-discounted shown prices, recorded verbatim; the optimizer subtracts prereq bundles) → filter dead skills → `tools/sp-optimizer` exact knapsack. Input CSV: `tools/sp-optimizer/examples/2026-07-12-symboli-rudolf-nakayama1200-career3.csv`, run log `tools/sp-optimizer/runs/2026-07-12T135635Z-…`.

All six gold bundle prices decomposed exactly against `tools/skill-db` base costs (e.g. On Your Left! 342 = 162 Lv1 + 180 Slick Surge; Firm Course Menace 257 = 117 Lv1 + 77 hidden ◎ Lv3 + 63 ○ Lv3), and the optimizer cross-check passed (only the expected Playtime's Over! standalone note — See Ya Later! wasn't co-listed, and 144 is the exact standalone Lv1 price).

### Key pool differences vs career #2

- **Slick Surge / On Your Left! are back** (career #1's best chain) *and* **No Stopping Me! over Nimble Navigator** (career #2's) — first career with both.
- **Sprinting Gear** (128 at Lv2, +1.02) and **Louder! Tracen Cheer!** (140 at Lv3, +0.86) — big, cheap, new.
- No Fast & Furious / Position Pilfer, no Ignited Spirit PWR this time.
- Let's Pump Some Iron! at Hint Max → 120 SP for +1.93, again the top efficiency by far.

### Filtered out as dead

- Wrong course: Kyoto Racecourse ◎ 77, Chukyo Racecourse ○ 81.
- Wrong ground/weather/season: Wet Conditions ○ 81, Rainy Days ○ 72, Winter Runner ○ 81.
- Wrong style (Pace Chaser): Preferred Position 180, Prepared to Pass 162, Pace Chaser Corners ○ 130, Pace Chaser Savvy ○ 99.
- Wrong distance: Updrafters 128 (Mile), Pressure 144 (Long), Smoke Screen 88 (Long), All I've Got 104 (Medium).
- Absent from chart (unmodeled; value unknown, not zero): **Meticulous Measures 126** (Sprint-valid positioning — the one real unknown), Ignited Spirit WIT 130, Sharp Gaze 144, Subdued Late Surgers 130, Hesitant Front Runners 91.
- Recovery blues (chart strips HP by design; 1200m spurt not stamina-limited): Corner Recovery ○ 136, A Small Breather 144, Be Still 144.
- Near-zero chart value, dropped to stay under the optimizer's 22-item cap: Focus 91 (+0.01), Target in Sight ○ 81 (+0.03), Inner Post Proficiency ○ 81 (+0.04).

Hesitant Late Surgers was initially kept (unlike the other debuffs it has a chart entry, +0.22 at 91 SP), but the user ruled out the hesitant skills entirely — see the final result below.

## ~~First result (superseded — included Hesitant Late Surgers)~~

~~+9.44 L for 2059 SP, 16 skills~~ (run log `2026-07-12T135635Z-…`) — same as the final set below except it bought Hesitant Late Surgers (+0.22), Playtime's Over! (+0.25), and Burning Spirit SPD (+0.29) instead of Professor of Curvature, Firm Conditions ◎, and Firm Course Menace. Dropped per user: no debuff purchases.

## Result (final — no debuffs)

**OPTIMAL: +9.34 L for 2058 SP (7 leftover), 16 skills** (run log `2026-07-12T135922Z-…`) — still the biggest haul of the three careers:

| Skill | effective SP | mean ΔL |
|---|---|---|
| Let's Pump Some Iron! | 120 | +1.93 |
| Slick Surge | 180 | +1.16 |
| On Your Left! (gold; shown 342) | 162 | +0.79 |
| Sprinting Gear | 128 | +1.02 |
| Louder! Tracen Cheer! | 140 | +0.86 |
| Nimble Navigator | 150 | +0.75 |
| No Stopping Me! (gold; shown 285) | 135 | +0.69 |
| Ignited Spirit GUTS | 180 | +0.48 |
| Ignited Spirit SPD | 120 | +0.25 |
| Burning Spirit SPD (gold; shown 260) | 140 | +0.29 |
| Firm Conditions ○ | 63 | +0.24 |
| Firm Conditions ◎ (shown 140) | 77 | +0.11 |
| Firm Course Menace (gold; shown 257) | 117 | +0.21 |
| Corner Adept ○ | 180 | +0.23 |
| Professor of Curvature (gold; shown 360) | 180 | +0.34 |
| Right-Handed ○ | 63 | +0.14 |
| Summer Runner ○ | 63 | +0.14 |

Skipped: Playtime's Over! (144 for +0.25), Burning Spirit SPD (140 for +0.29 — its base Ignited Spirit SPD *is* bought), It's On! + Ramp Up (306 for +0.36), Straightaway Acceleration (153 for +0.16).

Removing Hesitant Late Surgers reshuffled more than one slot: versus the first run, Playtime's Over! and the Burning Spirit SPD gold also drop out, and the freed 375 SP buys Professor of Curvature plus the full Firm chain (◎ + Firm Course Menace) for a net +0.66. Runner-up +9.33/2045 keeps Burning Spirit SPD + Playtime's Over! instead of PoC + Firm Course Menace — 0.01 L difference, pure noise; pick either if one is easier to tap through.

## Caveats

- ΔL additivity assumed. **Re-sim the full 16-skill build in umalator before buying.**
- Consistency: Let's Pump Some Iron! (min 1.81) and Slick Surge (min 0.77) are near-guaranteed; No Stopping Me!/Nimble Navigator (min 0.00) only proc when blocked in the last spurt.
- Meticulous Measures (126, Sprint-valid) is unvalued by the chart, not worthless — if it ever gets modeled, re-check.
