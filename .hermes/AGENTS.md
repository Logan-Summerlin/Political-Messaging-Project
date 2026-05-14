# US Political Messaging Dataset — Project Context for Hermes

## Project
`/workspace/Political-Messaging-Project/`
Owner: Logan (Telegram)
Goal: Structured, queryable dataset of U.S. political issue polling, message A/B tests, and ballot measure results (2010+).

## Current Repository State (May 14, 2026)

This repository is now centered on three canonical processed outputs and one active plan:

- `data/processed/messages.csv`
- `data/processed/issues.csv`
- `data/processed/referendums.csv`
- `plans/project_plan_llm_political_messaging.md`

Use `README.md` + the active plan for project-wide status before running new extraction work.

## Key Files
- `README.md` — full project overview and maintenance rules
- `schema/messages_schema.md` — message testing data schema
- `schema/issues_schema.md` — issue polling data schema
- `schema/referendums_schema.md` — ballot measure data schema
- `sources/` — extracted source data documents
- `data/raw/` — original source files and extraction artifacts
- `data/processed/` — canonical cleaned datasets used by downstream analysis

## Scripts Folder Guidance

The `scripts/` folder was cleaned to remove redundant legacy variants. Prefer the newest implementations and avoid reintroducing numbered "final batch" script copies.

Primary scripts to use first:
- `build_new_extractions.py` — main extraction build pipeline
- `rebuild_messages.py` — message table rebuild workflow
- `extract_new_navigator_messages.py` — latest Navigator extractor
- `normalize_ballot_measures.py` + `parse_ballot_measures.py` — referendum normalization/parsing
- `validate_data_quality.py` + `final_quality_report.py` — quality validation/reporting

Treat other scripts as targeted utilities and only run them when their specific source/task requires it.

## Source Constraints / Notes
- Gallup and YouGov often require browser-assisted extraction.
- Roper Center iPoll is subscription-only.
- Pew toplines frequently require PDF parsing.
- Ballotpedia can block direct scraping; prefer permissive structured sources where possible.

## Working Norms
- Keep `data/processed/*.csv` as the stable analysis interface.
- Keep temporary outputs out of long-lived tracked state.
- When a utility script is superseded, consolidate functionality instead of creating additional versioned clones.
