# Umalator (Global)

*Last updated: 2026-07-11*

**URL:** https://kachi-dev.github.io/uma-tools/umalator-global/
**Source:** https://github.com/kachi-dev/uma-tools — fork lineage: `alpha123/uma-tools` → `IHATEJEKUTO/VFalator-Umalator-Fork-Yeah` → `kachi-dev` (global data, active as of 2026-07).

## What it is

A race simulator for global-server Uma Musume. Configure one or two umas — stats, aptitudes, running style, skill list — plus a course (racecourse/distance), ground condition, mood, and sim options, then run N simulated races. Intended primarily as a **CM planning tool**: where do skills proc on this course, how much are they worth, is my stamina enough.

## Outputs

- **Compare mode**: mean/median **bashin** difference between uma 1 and uma 2 across runs, with distribution — for A/B testing builds, skills, or stat trade-offs.
- **Skill chart**: where along the course each skill activated (trigger regions), velocity/position-over-distance charts for individual runs.
- **Spurt rate / survival rate**: % of runs with a full spurt / without running out of HP — **the** way to answer "do I have enough stamina for this course".

## Fork improvements over the original umalator

- **Wit variance mechanics**: Downhill Mode, Rushed, and skill proc chance are simulated. Spurt rates cross-referenced against in-game packet data are accurate to within a few percent.
- **Extended position keep**: the pacer uma is customizable (skills, wit, power), multiple pacers supported (simulate 2 front runners, 1 runaway, etc.), and mee1080's position-keep logic runs beyond the early race.
- **Lane movement**: lane-change simulation, enabling evaluation of lane-movement skills (niche; slows the sim).
- **Desynced RNG** between the two umas in compare mode (can re-sync when wit variance is off).
- **Skill chart has HP consumption removed** — deliberate: people were reading recovery-skill "+L" gains off the chart to derive stamina requirements, which is wrong. Use spurt/survival rate instead.
- Bug fixes vs original: start dash acceleration frames, velocity clamping when a speed skill expires, skill-chart trigger desync from skills targeting other umas, non-full spurt timing (original always delayed full spurts by 60m + candidate delay), section modifier leaking past late-race.

## Known limitations / caveats

- **Static + dynamic trigger conditions don't compose correctly**: e.g. Restless on Kyoto 3000m never activates in the sim (the pre-calculated trigger region is the 1st uphill, but the ≥5s dynamic condition resolves after the uma has left it). Distrust sims of skills mixing course-feature and time/duration conditions.
- It simulates 1–2 umas + pacers, not a full 9–18 field — pack dynamics, blocking, and real CM variance are only approximated.
- Maintainer's own warning: comparing 2 umas in the vacuum of a simulation "should never, ever be the end-all decider of which uma you use." Use it for direction and magnitude, not verdicts.

## Related tools in the same repo

- `skill-visualizer-global` — visualize skill trigger regions on any course without running a sim.
- `build-planner`, `umadle`, `rougelike` — misc side tools.
