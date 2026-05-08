# Data Quality Audit — May 8, 2026

## Scope
Reviewed code, documentation, raw datasets, and processed datasets with focus on:
1. Code issues
2. Dataset issues
3. Raw import issues
4. Raw source coverage/completeness

## Commands Run
- `python scripts/scrape_wiki_ballot_measures.py`
- ad-hoc Python CSV integrity checks (row counts, year coverage, duplicates)
- documentation cross-checks against actual file contents

## Findings

### 1) Code Issues
- `scripts/scrape_wiki_ballot_measures.py` only yields structured referendums for 2022 and 2024 in current logic.
  - The script reports `0 new` rows for 2020 and earlier despite those years being targeted.
  - Root cause: `to_referendum()` requires valid state attribution; `parse_2020_earlier()` rows are produced without reliable `state` values for older page formats.
- The script output (`data/processed/referendums_new_wiki.csv`) contains 187 measures, below documented raw holdings and below the expected 2022+2024 coverage implied by intermediate raw rows.

### 2) Dataset/Documentation Issues
- `README.md` states **199** rows in `data/processed/referendums.csv`, but file has **198** data rows.
- `sources/dataset_inventory.md` also states **199** rows in `referendums.csv`.
- `README.md` states **592** rows in raw Wikipedia ballot data, but split raw files currently total **592** only when combined:
  - `wikipedia_ballot_measures.csv`: 355 rows (2022, 2024)
  - `wikipedia_ballot_measures_complete.csv`: 237 rows (2008–2020)

### 3) Raw Import Issues
- Raw ingest is fragmented across two different schemas:
  - `wikipedia_ballot_measures.csv` schema: `year,state,measure,topic,yes_pct,no_pct,outcome`
  - `wikipedia_ballot_measures_complete.csv` schema: `year,measure_name,outcome,full_text`
- This split prevents straightforward merge into `referendums.csv` without additional normalization for state, topic, and vote metrics in the older-year file.
- Current processed referendums file does not incorporate the 2008–2020 `complete` raw file.

### 4) Raw Source Coverage / Completeness
- Local raw HTML snapshots exist for every election cycle year in intended range:
  - `wiki_ballot_2008.html`, `2010`, `2012`, `2014`, `2016`, `2018`, `2020`, `2022`, `2024`.
- Raw source coverage appears complete for the Wikipedia-based pipeline (files exist for all targeted years), but normalized import completeness is not achieved.

## Conclusion
- **Code issues:** Yes (older-year extraction path not producing normalized rows).
- **Dataset issues:** Yes (documentation count mismatch; partially integrated referendum pipeline).
- **Raw import issues:** Yes (schema fragmentation + missing normalization for older years).
- **Raw source completeness:** Source artifacts are present for targeted Wikipedia years, but imported/normalized completeness is incomplete.

## Recommended Next Actions
1. Add year-specific parsers for 2020/2018/2016/2014/2012/2010/2008 that preserve state context.
2. Normalize `wikipedia_ballot_measures_complete.csv` into referendum schema (state, measure id, topic, outcome confidence).
3. Rebuild referendum dataset and update documented row counts in README/inventory.
4. Add a reproducible validation script to assert:
   - per-year raw coverage,
   - per-year normalized import counts,
   - schema consistency checks.

## Addendum — Issue Polling & Message Testing Pipelines (May 8, 2026)

### Scope of this addendum
Reviewed Data for Progress (DFP), Navigator, and Gallup issue/message ingestion for:
1. pipeline behavior,
2. dataset completeness,
3. whether linked source websites currently contain extractable items not present in processed data.

### Additional Commands Run
- `python - <<'PY' ...` to summarize source counts and min/max dates in `data/processed/issues.csv` and `data/processed/messages.csv`.
- `curl -L -s --max-time 20 https://www.dataforprogress.org/blog?format=rss | head`
- `curl -L -s --max-time 20 https://navigatorresearch.org/feed/ | head`
- `python - <<'PY' ...` to compare feed links vs currently ingested `source_url` values.

### Findings — Pipeline/Data Issues

#### A) Data for Progress (DFP)
- Processed coverage is broad on issue polling (`1731` rows in `issues.csv`, max date `2026-05-04`) but much thinner for message testing (`93` rows in `messages.csv`, max date `2024-04-25`).
- This mismatch is structural in code:
  - `scripts/parse_dfp_chunks.py` extracts message rows only from a constrained section pattern (not all post formats).
  - `scripts/rebuild_messages.py` only pulls DFP messages from `chunk2_polling_data.md` `Tested Message Wording` sections, skipping message-like findings in other chunk formats.
- Website delta check: DFP RSS feed currently surfaces a post URL not in processed DFP URLs:
  - `https://www.dataforprogress.org/blog/2026/4/20/voters-in-multiple-states-say-iran-war-benefits-israel-and-that-us-military-aid-to-the-country-should-be-halted`
- Conclusion: DFP is partially incomplete in both recency and format coverage for `messages.csv`.

#### B) Navigator Research
- Processed message rows (`53`) span through `2026-05-07`, but only `13` unique Navigator URLs are represented.
- Current Navigator feed has URLs that are absent from the dataset (example set):
  - `https://navigatorresearch.org/health-care-focus-group-part-2`
  - `https://navigatorresearch.org/health-care-focus-group-part-1`
  - `https://navigatorresearch.org/what-do-americans-want-to-fund-not-ice-not-war-not-a-ballroom-healthcare`
- Root cause is likely source selection/heuristics rather than parser crash: current parser favors explicit bullets with percentages/quoted text and may skip qualitative or differently formatted message content.
- Conclusion: Navigator ingestion is not fully complete relative to linked live feed pages.

#### C) Gallup
- `issues.csv` already has large Gallup coverage (`1830` rows; max date `2026-03-02`), but project artifacts suggest mixed generations of extraction tables (`mip_table_v*.csv`) and static CSV pipelines.
- Given Gallup’s site rendering behavior and frequent publication cadence, the March 2, 2026 ceiling likely indicates lag versus current site content.
- Conclusion: Gallup data appears directionally strong historically, but likely not fully current and may miss newly published issue values after `2026-03-02`.

### Overall Addendum Conclusion
- **Issue polling pipeline:** substantial coverage, but with freshness gaps (especially Gallup).
- **Political message testing pipeline:** clear incompleteness in DFP and Navigator due to format-limited extraction heuristics.
- **Source-page missingness:** confirmed for both DFP and Navigator using live feed URL comparisons.

### Recommended Next Actions (Issue/Message Pipelines)
1. Generalize DFP message extraction beyond `chunk2` “Tested Message Wording” blocks to include message-test evidence in chunk1/3/4 formats.
2. Add a feed-diff QA check (per source) that flags feed URLs absent from processed `source_url` inventories.
3. Expand Navigator parser to ingest non-bullet/qualitative message findings where explicit message text exists.
4. Add a staleness guardrail: fail CI or warn when max source date lags feed `pubDate` by more than N days.


## Implementation Status Update (May 8, 2026)

### Original Recommended Next Actions — Status
- [x] **1. Add year-specific parsers for 2020/2018/2016/2014/2012/2010/2008 that preserve state context.**
  - Implemented via normalization logic that ingests and maps older-year rows from `wikipedia_ballot_measures_complete.csv` into the unified referendum schema.
- [x] **2. Normalize `wikipedia_ballot_measures_complete.csv` into referendum schema (state, measure id, topic, outcome confidence).**
  - Implemented in the rebuilt referendum pipeline with outcome-confidence handling (including explicit unknowns).
- [x] **3. Rebuild referendum dataset and update documented row counts in README/inventory.**
  - Completed; processed referendum outputs were rebuilt and documentation counts updated.
- [x] **4. Add a reproducible validation script** for per-year raw coverage, per-year normalized counts, and schema checks.
  - Completed via `scripts/validate_data_quality.py`.

### Addendum Recommended Next Actions — Status
- [x] **1. Generalize DFP message extraction beyond chunk2 “Tested Message Wording” blocks.**
  - Completed by broadening extraction across multiple chunk formats and message-test cues.
- [x] **2. Add a feed-diff QA check** that flags feed URLs absent from processed `source_url` inventories.
  - Completed in `scripts/validate_data_quality.py`.
- [x] **3. Expand Navigator parser** to ingest non-bullet/qualitative message findings with explicit message text.
  - Completed through expanded heuristic extraction in message rebuild logic.
- [~] **4. Add a staleness guardrail** when max source date lags feed `pubDate` by more than N days.
  - **Partially completed:** staleness reporting is implemented in validation output, but no CI-enforced fail/warn threshold is configured in this repository yet.

### Remaining Incomplete Work
1. Wire `scripts/validate_data_quality.py` into CI (or a scheduled job) with a concrete staleness threshold `N` and failing/warning policy.
2. Optionally add per-source threshold configuration (e.g., different lag tolerance for DFP, Navigator, Gallup).
