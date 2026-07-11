# Stats and Aptitudes

*Last updated: 2026-07-11*

## The five stats (cap 1200)

| Stat | What it does |
|------|--------------|
| **Speed** | Raises target/top speed in every phase. Biggest driver of final-spurt velocity. |
| **Stamina** | Sets the HP pool (see `racing-mechanics.md`). You need "enough" for the distance + strategy; past that point extra stamina does little. |
| **Power** | Acceleration, and ability to push through/overtake when surrounded (lane changes). |
| **Guts** | Sustains speed once HP runs low in the last spurt; also factors into last-spurt speed and rushing resistance. Historically undervalued; matters more at higher stat totals. |
| **Wit** | Skill activation rate, better positioning decisions, lower chance of getting Rushed, and small speed gains from Downhill Mode. Low wit = skills fail to fire. |

Rough global-meta prior (URA-era): Speed ≥ Stamina-to-threshold > Power > Wit > Guts, with stamina needs depending heavily on distance and running style. Always sanity-check stamina via umalator's spurt/survival rate rather than rules of thumb.

## Aptitudes (letter grades G → A, raisable to S via inheritance)

Three groups; each affects racing differently:

- **Surface** (Turf / Dirt): below A imposes heavy penalties (mainly to power/acceleration). Don't race off-surface without fixing this.
- **Distance** (Sprint 1000–1400m / Mile 1401–1800m / Medium 1801–2400m / Long 2401m+): multiplies speed (and accel). **S gives ~1.05× speed** — a meaningful boost, common CM inheritance goal.
- **Style** (running strategy): scales how effectively wit is applied. A is fine; S is a minor gain.

## Running styles

| Global name | JP term | Behavior |
|------|------|----------|
| Front Runner | nige (逃げ) | Takes the lead immediately, tries to wire the race. Pace-sensitive; hates other front runners. |
| Pace Chaser | senkou (先行) | Sits just behind the front. Most consistent/safe style. |
| Late Surger | sashi (差し) | Mid-pack, surges in the final leg. |
| End Closer | oikomi (追込) | Dead last, all-in on the last spurt. Depends on power to cut through traffic. |

Style choice interacts with the CM field: e.g. a lone Front Runner is strong, multiple front runners burn each other out. Umalator's multi-pacer feature exists precisely to test this.
