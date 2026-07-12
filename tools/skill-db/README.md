# skill-db

Local database of global-version skill facts: official names, base SP costs, and
gold/white prerequisite pairs. Built to prevent the gold-price double-count
mistake (see `questions/2026-07-12-sp-minmax-rudolf-career2.md`): the in-game
Learn screen shows a **bundle price** on a gold whose white prereq is unowned.

## Usage

```
python3 lookup.py "on your left"     # skill + partner + price at every hint level
python3 fetch.py                     # refresh skills.json from the network
```

`lookup.py` is the one to reach for while building an sp-optimizer CSV: it shows
what a shown price should decompose into. `sp-optimizer/optimize.py` also reads
`skills.json` automatically and warns about CSV rows that contradict it.

## Data source

`fetch.py` pulls from **kachi-dev/uma-tools** — the umalator's own repo, so the
data is global-aligned by construction:

- `skill_meta.json` (master branch): skill ID → `baseCost`, `groupId`, `iconId`.
- deployed `umalator-global/bundle.js`: embedded skill ID → official global
  English name map (global-released skills only).

Alternatives considered: GameTora loads its skill data dynamically (nothing
scrapeable in the HTML or webpack chunks); umamusu.wiki's `Game:List_of_Skills`
(MediaWiki API at `/w/api.php`) has base costs and JP-only flags but no prereq
column. The wiki remains a decent manual cross-check.

## Structure rules encoded in skills.json

- Trainable skill ids (`2xxxxx`): within a `groupId`, suffix `1` is the upgrade
  (rare gold, or ◎ for green skills), suffix `2` its prereq (white/○), suffix
  `3` the × variant.
- Green families have a suffix-`4` rare gold (e.g. Firm Course Menace) whose
  Learn-screen bundle stacks the whole ○ → ◎ → gold chain; recorded with
  `pair` = the ○ and `middle` = the ◎ (include the ◎'s ΔL when valuing it).
- A name under both a `1xxxxx` id (a character's unique, baseCost 0) and a
  `9xxxxx` id (purchasable inherited version) resolves to the purchasable one.
- Hint discounts: Lv1 10%, Lv2 20%, Lv3 30%, Lv4 35%, Max 40%; prices floored.

`skills.json` is committed (small, needed offline); the `fetched` field records
the refresh date. The bundle.js extraction is anchored on a known id/name pair,
so if upstream renames things `fetch.py` fails loudly rather than silently.
