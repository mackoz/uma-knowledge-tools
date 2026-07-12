# Skills

*Last updated: 2026-07-12*

## Types

| Category | In-game look | Effect |
|----------|--------------|--------|
| **Unique** | Rainbow banner, top slot | Character's signature skill. Level scales with character awakening/talent; inherited copies are weaker (single-circle version). |
| **Gold (rare)** | Gold background | Stronger version of a white skill; usually obtained from support card hints or events. |
| **White (normal)** | White background | Standard speed/accel/recovery/positioning skills. |
| **Green (passive)** | Green icon | Unconditional stat boosts gated on a condition being true at race start (e.g. `Standard Distance ◎`, `Tokyo Racecourse ○`, `Left-Handed ○`). Cheap, reliable value since they always "proc" if the condition matches. |
| **Blue (recovery)** | | Restore HP; the way to patch stamina shortfalls. |
| **Debuffs** | Red/purple text | Hit *other* runners (e.g. drain their HP/vision). Team Trials / CM support tools. |

`○` vs `◎` on a skill name = lesser vs greater version of the same passive.

## Activation

- A skill fires when its **trigger conditions** are met (phase, section, position, course feature, surroundings), passing a **wit-based proc check**: `max(100 − 9000/wit, 20)%` per skill per race.
- Where a skill can trigger on a given course = its **trigger region** — the skill-visualizer / umalator skill chart shows these. Skill value is highly course-dependent (a "final corner" skill is worthless if the final corner is in the wrong place).
- Speed/accel skills add to target speed or acceleration for a duration scaled by course length.

## Skill points, hints, discounts

- Trainees buy skills during/after career with **skill points**.
- **Hint levels** (from support card training events) discount the cost: Lv1 −10%, Lv2 −20%, Lv3 −30%, Lv4 −35%, Lv5 −40%. Discounted prices are **floored** (90 base at Lv4 → 58).
- A gold requires its white: when the white is unowned, the Learn screen lists it beneath the gold and the **gold's shown price is a bundle** that already includes the white (each part at its own hint discount). E.g. Fast & Furious shown 306 = 126 (base 180, Lv3) + 180 Position Pilfer. When the white is owned, the gold shows only its own price. Verified in-game 2026-07-12.
- Green-skill rare golds (e.g. Firm Course Menace over Firm Conditions) bundle the whole ○ → ◎ → gold chain — the ◎ is included even if it isn't visible on screen (exact price decomposition confirms it).
- Base costs, gold/white pairs, and hint price tables: `tools/skill-db/` (`python3 lookup.py "<name>"`), built from the umalator repo's own data.
- General buying priority for a race target: skills that reliably proc on the target course (matching passives, well-placed speed/accel skills) > generic recovery as needed for spurt rate > everything else. Verify with umalator's skill chart / bashin comparison.
- For spending leftover SP optimally, see [sp-minmaxing.md](sp-minmaxing.md).
