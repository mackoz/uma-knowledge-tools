# Uma Musume Knowledge Base & Tools

Personal knowledge base and homegrown tools for Uma Musume: Pretty Derby (**global version**). Started 2026-07-11; grows over time as questions get worked through and tools get built.

## Layout

| Path | Contents |
|------|----------|
| `knowledge/game-overview.md` | What the game is, global vs JP, current state |
| `knowledge/stats-and-aptitudes.md` | The five stats, aptitudes, running styles |
| `knowledge/racing-mechanics.md` | Race phases, HP/stamina, spurt mechanics |
| `knowledge/skills.md` | Skill types, proc mechanics, skill points & hints |
| `knowledge/training.md` | Career mode, support decks, inheritance |
| `knowledge/sp-minmaxing.md` | Method: spend leftover SP for max L gain (umalator chart + cost screenshots + knapsack) |
| `knowledge/glossary.md` | Community terms and abbreviations |
| `knowledge/umalator.md` | The umalator-global race simulator (external): usage, internals, caveats |
| `tools/` | Homegrown runnable tools, one subfolder each with its own README |
| `tools/sp-optimizer/` | Knapsack solver: best skill purchases for a given SP budget |
| `questions/` | One file per question worked through (skill picks, build comparisons, etc.) |
| `reference/` | Source materials: umalator PDF capture, game screenshots |

## Conventions

- Each knowledge file carries a **Last updated** date — the game evolves, so stale info should be re-verified (GameTora and Game8 are good sources).
- New learnings from future sessions go into the relevant `knowledge/` file, or a new dated file in `questions/` (e.g. `questions/2026-07-skill-purchases.md`) when it's a specific decision we worked through.
- Facts that couldn't be verified are marked **(unverified)**.
- New tools get their own `tools/<name>/` folder with a README (usage + input format), runnable code, and an `examples/` folder with real data from the session that motivated them. The methodology behind a tool lives in `knowledge/`, the implementation in `tools/`.

## Notes

- `reference/` materials were used for [questions/2026-07-11-sp-minmax.md](questions/2026-07-11-sp-minmax.md) (Curren Chan SP spend, Nakayama 1200m).
- poppler is installed; `pdftotext -layout` works well on umalator page-print PDFs.
