# US Political Messaging & Issue Polling Dataset

A cleaned, research-oriented dataset for U.S. political messaging analysis.

This repository now maintains **three canonical processed datasets** and a **single active project plan**.

## Current Project State (May 14, 2026)

- Repository documentation has been consolidated into:
  - `README.md` (this file)
  - `plans/project_plan_llm_political_messaging.md`
- Redundant intermediate reports and temporary planning docs were removed.
- Redundant/outdated processed staging datasets were removed.

## Canonical Data Products

All downstream analysis should use only these files:

- `data/processed/messages.csv` — **426 rows**
- `data/processed/issues.csv` — **5,099 rows**
- `data/processed/referendums.csv` — **337 rows**

> Row counts above are based on line counts (`wc -l`, header excluded).

## Repository Layout

- `data/processed/` — canonical production-ready datasets
- `data/raw/` — collected source materials and source-specific extraction artifacts
- `scripts/` — extraction, parsing, cleaning, and analysis scripts
- `schema/` — table schema definitions:
  - `schema/messages_schema.md`
  - `schema/issues_schema.md`
  - `schema/referendums_schema.md`
- `plans/project_plan_llm_political_messaging.md` — active roadmap and execution plan

## Data Usage Guidance

1. Treat `data/processed/*.csv` as the stable analysis interface.
2. Treat `data/raw/` as source evidence and reproducibility support.
3. Use `scripts/` for rebuilding or extending pipeline outputs.
4. If new sources are added, merge into canonical processed files and avoid adding long-lived staging duplicates.

## Maintenance Rules Going Forward

- Keep only one active plan file in `plans/`.
- Keep only canonical outputs in `data/processed/` unless a short-lived branch task requires temporary files.
- Remove temporary audit notes and one-off status markdown files after conclusions are merged into README + plan.

---

Project owner: Logan  
Last updated: **May 14, 2026**
