# SP Min-Maxing: Buying Skills for Maximum L Gain

*Last updated: 2026-07-12. Worked examples: [questions/2026-07-11-sp-minmax.md](../questions/2026-07-11-sp-minmax.md), [questions/2026-07-12-sp-minmax-rudolf.md](../questions/2026-07-12-sp-minmax-rudolf.md), [questions/2026-07-12-sp-minmax-rudolf-career2.md](../questions/2026-07-12-sp-minmax-rudolf-career2.md) (includes the gold bundle-price correction).*

Method for spending leftover skill points on the skills that most improve race performance on a **specific target course**.

## Data needed

1. **Value side — umalator skill chart** ([umalator.md](umalator.md)): set up the uma (stats, style, skills owned) and the exact target course/conditions in umalator-global, open the Skills Chart, and read each skill's **mean ΔL**. Owned skills show 0.00; listed values are incremental vs the current build. Export/print the page to PDF for offline analysis (`pdftotext -layout` extracts it cleanly).
2. **Cost side — in-game Learn screen**: screenshot the full scrollable skill list at end of career. This captures the **actual hint-discounted SP cost** (hints: Lv1–5 = 10/20/30/35/40% off), which the simulator can't know.

## Method

1. **Filter to skills that can actually proc.** Discard anything gated on the wrong running style, wrong distance band, wrong course/direction/season/condition. This usually eliminates most of the list — the Learn screen offers every hinted skill, not just useful ones.
2. **Join** remaining skills: cost from screenshots, mean ΔL from the chart.
3. **Model prerequisites:** a gold skill requires its white base, listed directly beneath it in the Learn screen — and the **gold's shown price is a bundle that already includes that white**. Record shown prices verbatim in the CSV with `requires`; the optimizer subtracts the prereq's shown price to get the true increment. Value side: chart ΔL is per-skill, so the gold row's value = ΔL(gold) − ΔL(white) when the white is a separate row. Green rare golds (Firm Course Menace style) hide a ◎ tier inside the bundle — model ○ → ◎ → gold as three rows. When unsure what pairs with what, `python3 tools/skill-db/lookup.py "<name>"` shows the partner, base cost, and every hint price; `optimize.py` also cross-checks the CSV against skill-db automatically.
4. **Optimize:** run [tools/sp-optimizer](../tools/sp-optimizer/README.md) — `python3 optimize.py <skills.csv> <budget> --notes "<uma, course, conditions>"` — an exact 0/1 knapsack with prerequisite chains. Each run is logged to `tools/sp-optimizer/runs/` (gitignored) with the full skill snapshot and results, and clears the `reference/` staging folder afterwards (`--keep-inputs` skips that). Greedy by L-per-SP is a good sanity check but can be beaten by the exact solve.
5. **Verify in umalator:** add the chosen set to the uma and re-sim vs the current build — ΔL additivity is an approximation.

## Traps

- **Recovery (blue) skills show no value in the skill chart by design** (the fork strips HP from it). They are not "bad" — they're a stamina fix. Check spurt/survival rate first: if it's already ~100%, skip them; if not, a recovery skill may beat every velocity skill on the list.
- **Stat passives can be worth 0** if the boosted stat is already capped (e.g. Standard Distance ◎ reading 0.00 at 1200 speed) — trust the chart over intuition.
- **Debuffs and RNG skills** (bracket-conditional, rushed-punishers) are poorly captured by mean ΔL; treat their chart value as unknown rather than 0 if they're cheap and CM-relevant.
- **Mean hides variance**: two skills with equal means can have very different floors (check the chart's min/median columns for consistency skills).
- Everything is **course-specific** — redo the whole exercise if the target race changes.
