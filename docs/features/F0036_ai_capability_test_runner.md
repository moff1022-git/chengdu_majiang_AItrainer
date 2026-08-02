# F0036 AI Capability Test Runner

Status: Approved

## Goal

Provide a standalone headless benchmark for `random`, `rule_ai`, `rule_ai_plus`, and `humanlike_v2` using reproducible game IDs. It supports 100/200/500/1000/2000/5000/10000 games, fixed seat mapping s0-s3, live progress, Ctrl-C checkpoint/resume, Markdown/CSV/JSON reports, selectable humanlike personality presets, and bounded concurrent workers (1/5/10/20/50/100).

## Scope

- Reuse `engine.orchestrator.run_players_game`; no UI, human proxy, rule or AI changes.
- Prefer IDs in `data/ai_capability/fixed_game_sets/<N>_games`; deterministic `batch-20260301-<index>` fallback for missing sets.
- Record scores, rankings, win/top1 rates, completion reason, elapsed time, and per-game decision latency when available.
- Results live under `data/ai_capability/results/` and do not alter Task 19 status.

## CLI

`python tools/ai_capability_test.py --games 100 --players random,rule_ai,rule_ai_plus,humanlike_v2`

Missing arguments are selected through numbered menus (mode, game count, target AI, or each seat); no free-form AI type entry is required. `--resume <run-dir>` continues from checkpoint; Ctrl-C writes a partial report.

Before a new run starts, the CLI presents an estimated duration, experiment count, and game count. The user must confirm; cancellation returns to parameter selection without starting games. Resume runs also show the remaining estimate.

## Outputs

`config.json`, `checkpoint.json`, `games.jsonl`, `summary.json`, `report.md`, and `report.csv`.
