# Racing Mechanics

*Last updated: 2026-07-11*

How a race actually resolves (this is what umalator simulates).

## Phases

A course of length D splits into:

- **Opening leg**: 0 → D/6 — start dash, position keep sorts the field by style.
- **Middle leg**: D/6 → 2D/3 — cruising at style-dependent base speed.
- **Final leg**: 2D/3 → finish — base speed rises, and the **last spurt** begins somewhere in here.

Courses are also divided into 24 **sections** for skill triggers and random per-section speed variance.

## HP (stamina) model

- Starting HP ≈ `distance + 0.8 × stamina × strategy modifier` (front runners get less effective HP than closers).
- HP drains continuously as a function of current speed (roughly quadratic in speed above a baseline); draining is worse on non-firm ground, and **Guts reduces drain in the last spurt**.
- Recovery (blue) skills restore a % of max HP.

## Last spurt

At the start of the final leg the uma computes whether it can hold **maximum spurt speed** (a function of speed stat + distance aptitude) to the finish with its remaining HP:

- Enough HP → **full spurt** (ideal).
- Not enough → it picks a slower spurt speed / delays the spurt — this is a **non-full spurt** and costs serious time.
- HP hits 0 → severe slowdown ("dying on the hill"); guts softens this.

**This is why stamina questions are answered by spurt rate**: run the sim, look at the % of runs achieving a full spurt (and survival rate), not at recovery-skill length gains on the chart.

## Wit variance effects (modeled in umalator-global fork)

- **Skill procs**: each skill checks `max(100 − 9000/wit, 20)%` chance to activate when its conditions are met.
- **Rushed** (kakari): random chance (reduced by wit) to lose control and burn extra HP.
- **Downhill Mode**: wit-based chance to gain speed cheaply on downhill segments.
- **Position keep**: wit affects the early-race speed-up/slow-down dance to hold the style's proper position.

## Other factors

- **Track conditions**: Good/Yielding/Soft/Heavy (firm → wet) change base speed, power effectiveness, and HP drain.
- **Course geometry**: each racecourse has its own straights, corners, slopes — this is why course-specific skills and CM course analysis matter.
- **Bashin** (身): margin unit ≈ 2.5m — how sim comparisons are usually reported.
