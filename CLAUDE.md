# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A personal knowledge base **plus homegrown tools** for **Uma Musume: Pretty Derby (global version)**, started 2026-07-11. The user plays global and uses this folder across sessions to research game mechanics, work through decisions (builds, skill purchases, Champions Meeting planning), and build small tools that automate those decisions. There is no build system or test suite; tools are standalone Python scripts run directly.

## Structure

- `README.md` — index and conventions; read it first.
- `knowledge/` — one markdown file per mechanics topic (stats, racing, skills, training, glossary, game overview). Includes `umalator.md`, notes on the umalator-global race simulator (https://kachi-dev.github.io/uma-tools/umalator-global/, source: github.com/kachi-dev/uma-tools), the main external tool used for build comparisons and stamina/spurt-rate checks.
- `tools/` — runnable tools the user builds over time, one subfolder each (README with usage + input format, script, `examples/` with real session data). Current: `sp-optimizer/` (knapsack over skill costs/ΔL values; run `python3 optimize.py <csv> <budget>` — Learn-screen prices are entered verbatim; gold rows with `requires` are bundle prices and the prereq's price is subtracted automatically) and `skill-db/` (global skill names/base costs/gold-white pairs from the umalator repo's data; `lookup.py` for price sanity checks, auto-cross-checked by the optimizer). The methodology for a tool belongs in `knowledge/`, the implementation here.
- `questions/` — one dated file per question worked through (e.g. `2026-07-11-sp-minmax.md`), capturing the decision and reasoning.
- `reference/` — **local-only, gitignored staging** for the current run's raw inputs (game screenshots, saved pages; poppler is installed — `pdftotext -layout` handles umalator page-print PDFs well). Each sp-optimizer run clears it (skip with `--keep-inputs`); the durable record of a run is the CSV in `tools/sp-optimizer/examples/`, the local log in `tools/sp-optimizer/runs/`, and the `questions/` writeup.

## Conventions

- Every `knowledge/` file carries a *Last updated* date. The global game changes fast (accelerated JP schedule), so treat stale content as suspect and re-verify against GameTora (gametora.com/umamusume) or Game8 before relying on it.
- Mark facts that couldn't be verified as **(unverified)**. Keep content global-version-specific — JP mechanics/content don't always apply.
- New durable learnings from a session go into the relevant `knowledge/` file; decision-specific work gets a new `questions/` file. Don't leave conclusions only in conversation.
- When answering stamina/stat questions, prefer umalator spurt/survival rates over rules of thumb; see caveats in `knowledge/umalator.md` (notably: the skill chart deliberately omits HP, and static+dynamic skill conditions simulate incorrectly).
- Before writing one-off analysis scripts, check `tools/` for an existing tool that already does it; extend the tool rather than forking scratch copies.
