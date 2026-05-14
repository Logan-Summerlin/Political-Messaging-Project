# Project Plan: Political Messaging Dataset + Modeling Roadmap

**Status date:** May 14, 2026  
**Scope:** Maintain a high-quality U.S. political messaging dataset and prepare it for rigorous modeling/evaluation workflows.

## 1) What Was Completed in This Cleanup Pass

### Documentation consolidation
- Consolidated project-level status documentation into two files only:
  - `README.md`
  - `plans/project_plan_llm_political_messaging.md` (this file)

### Dataset cleanup
- Declared canonical processed outputs as:
  - `data/processed/messages.csv` (426 rows)
  - `data/processed/issues.csv` (5,099 rows)
  - `data/processed/referendums.csv` (337 rows)
- Removed outdated/redundant processed staging derivatives to reduce ambiguity.

### Project hygiene
- Removed superseded one-off plan files and historical phase checklists from active planning surfaces.
- Reduced documentation sprawl so project state can be understood from README + this plan.

## 2) Active Objectives

1. **Dataset reliability:** preserve clean, reproducible canonical tables.
2. **Schema consistency:** keep all additions aligned with schema definitions in `schema/`.
3. **Model readiness:** structure future data additions for message-generation and evaluation workflows.
4. **Governance readiness:** keep provenance and methodological notes embedded in data fields, not scattered across ad hoc docs.

## 3) Current Data Baseline

### Canonical tables
- `messages.csv`: 426 rows (message tests and related structured messaging entries)
- `issues.csv`: 5,099 rows (issue polling and structured/narrative issue findings)
- `referendums.csv`: 337 rows (state ballot measure outcomes, normalized)

### Supported schema references
- `schema/messages_schema.md`
- `schema/issues_schema.md`
- `schema/referendums_schema.md`

## 4) Operating Plan (Next 30 Days)

### A. Data quality hardening
- Run duplicate-key checks for each canonical table.
- Validate required fields against schema docs.
- Spot-check date normalization and source URL completeness.

### B. Pipeline discipline
- When adding new extractions, write to temporary branch-local outputs first.
- Merge only validated records into canonical processed files.
- Delete temporary outputs before merge unless explicitly needed for reproducibility.

### C. Model preparation
- Define a strict training view from `messages.csv` with inclusion/exclusion rules.
- Define an evaluation slice from `issues.csv` + `referendums.csv` for out-of-sample checks.

### D. Documentation discipline
- Keep progress updates in this plan’s “Change Log” section.
- Keep README focused on current-state operational guidance.

## 5) Risks and Mitigations

- **Risk: Reintroduction of duplicate staging files in `data/processed/`.**
  - Mitigation: enforce canonical-only policy; move experiments to branch-local temp files.

- **Risk: Schema drift across future source integrations.**
  - Mitigation: require schema validation before merge to processed outputs.

- **Risk: Documentation fragmentation recurring over time.**
  - Mitigation: all status updates route to README + this plan only.

## 6) Definition of Done for Ongoing Work

A future update is considered complete when:
1. Canonical datasets are updated and validated.
2. No redundant processed derivatives remain in `data/processed/`.
3. README and this plan reflect the new state in clear, concise terms.

## 7) Change Log

- **2026-05-14:** Major repository cleanup completed; docs consolidated; redundant datasets and outdated planning/status files removed.
