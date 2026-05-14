# Phase 0-1 Quality Audit — May 9, 2026

## Executive Summary

**Subject matter expert review of the US Political Messaging Dataset (Phase 0-1).** A thorough audit was conducted on all three processed datasets, with cross-referencing against live source websites, re-extraction from raw sources, and systematic bug hunting. **Three critical data-quality bugs were found and fixed.** The dataset is now substantially more reliable for fine-tuning a political messaging LLM.

**Final state: 5,597 total data points** across 3 tables, 8+ sources, 1972-2026.

---

## Changes Implemented — Summary

### Files Modified

| File | Change | Detail |
|------|--------|--------|
| `scripts/extract_gss.py` | **Bug fixed** | Line 152: string-vs-int comparison corrected. Added integer-key lookup from value-label dict. Re-ran extraction — all 1,303 rows now have correct support_pct (3.1%–93.0%). |
| `scripts/re_extract_dfp_issues.py` | **New script created** | Proper DFP re-extraction from raw chunk1 with demographic percentage filtering, sample-size skipping, and `question_type` classification (20 types). |
| `data/processed/issues.csv` | **GSS + DFP replaced** | Old GSS rows (all zeros) replaced with corrected extraction. Old DFP rows (1,788 narrative fragments) replaced with 1,298 cleaner rows. Merged via timestamped backup. |
| `data/processed/messages.csv` | **NAV_NEW removed + Blueprint backfilled + 5 new** | Removed 16 NAV_NEW_10xx rows (DFP URLs mislabeled as Navigator). Backfilled 3 Blueprint BLP_20260121_* effect scores (+27 net_concern). Added 5 new Navigator messages from "Who Americans Trust" article. |
| `data/processed/dfp_issues_repaired.csv` | **Staging file created** | Temporary staging output from the DFP re-extraction, used for merge verification. |
| `README.md` | **Stats updated** | Corrected row counts, source breakdowns, date range, and training-ready percentage to reflect post-audit reality. Updated last-modified date. |
| `sources/phase1_critical_audit_2026-05-09.md` | **This report** | Full audit documentation. |

### Backups Created

All destructive operations were preceded by timestamped backups:

| Backup | Created Before |
|--------|---------------|
| `issues.csv.bak.20260509_150452` | GSS merge |
| `issues.csv.bak.20260509_150629` | DFP replacement |
| `issues.csv.bak.20260509_151317` | Final DFP merge |
| `messages.csv.bak.20260509_150629` | NAV_NEW removal + Blueprint backfill |
| `messages.csv.bak.20260509_151615` | New Navigator messages added |

### Before → After

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| messages.csv training-ready | 183 (82%) | 190 (89%) | +7 |
|| messages.csv short wordings (<30) | 12 | 0 | All expanded |
|| issues.csv data_quality flag | — | Added | DFP = narrative_finding |
|| referendums.csv rows | 315 | 337 | +22 (2020 Wikipedia backfill) |
|| Referendum support_pct missing | 239 (75.9%) | 204 (60.5%) | -35 |
|| Referendum passed missing | 118 (37.5%) | 83 (24.6%) | -35 |
|| 2020 referendum support_pct missing | 28 (100%) | 0 (0%) | Fully fixed |
|| 2018 referendum support_pct missing | 18 (78%) | 11 (48%) | Partially fixed |
| Sources with real data | 2 of 3 buggy | 3 of 3 verified | — |

### What Was NOT Changed

- **CES data** — 447 rows unchanged. Verified clean in audit.
- **Gallup MIP** — 1,830 rows unchanged. Verified clean.
- **Pew/YouGov/AP-NORC/Ipsos** — Minor sources unchanged.
- **Raw data directories** — All original source files preserved unmodified.

---

## Supplementary Fixes — May 9, 2026 (This Session)

### 6. 📊 Referendum Vote Data Backfill (2020: 100% complete)

**Before:** 315 rows total. 239 (75.9%) missing `support_pct`. Only 2024 had vote percentages. 2020 had 28 rows with 0% filled.

**After:** 337 rows total. 204 (60.5%) missing `support_pct`. 2020 fully backfilled (45 rows, 0% missing) with vote percentages extracted from Wikipedia Yes/No columns. 22 new rows added (states not previously captured).

| Year | Before | After | Change |
|------|--------|-------|--------|
| 2020 | 28 missing (100%) | 0 missing (0%) | Fully fixed |
| 2018 | 18 missing (78%) | 11 missing (48%) | 7 backfilled |
| 2008–2016 | 79 missing (100%) | 79 missing (100%) | Limited Wikipedia data |
| 2022 | 112 missing (100%) | 112 missing (100%) | No percentages on Wikipedia |

**Method:** New script `scripts/backfill_referendum_votes.py` scrapes 2020 and 2018 Wikipedia pages using `<h3>` state headings and wikitable Yes/No columns containing vote counts and percentages. Uses multi-strategy fuzzy matching to reconcile short measure names ("Amendment 1") with full Wikipedia names ("Kentucky Constitutional Amendment 1, Marsy's Law Crime Victims Rights Amendment").

**Remaining gaps:** 2008–2016 Wikipedia pages have no wikitable tables (only `<ul><li>` lists without vote data). 2022 Wikipedia has pass/fail outcomes only. These would require Ballotpedia (WAF-protected) integration.

### 7. 📋 `data_quality` Field Added to issues.csv

**Before:** All issue rows treated equally in schema, despite DFP rows being narrative poll findings rather than structured question-wording pairs.

**After:** New `data_quality` column with two values:
- `structured_poll` — 3,771 rows (Gallup, GSS, CES, Pew, YouGov, AP-NORC, Ipsos)
- `narrative_finding` — 1,298 rows (Data for Progress)

**Impact:** Training pipelines can now filter by data quality. DFP rows provide topical coverage but are not clean question→support% pairs. Schema documentation updated.

### 8. ✏️ Blueprint Short Entries Expanded

**Before:** 12 Blueprint entries had wording <30 chars (summary labels like "Calling out oligarchy", "Elon Musk favorability"). 1 Navigator entry also short.

**After:** All 12 expanded to descriptive wordings (30–114 chars). Notes field records that these were expanded from survey category labels. 0 entries now <30 chars.

**Impact:** All 213 messages now have substantially descriptive wording. Training quality improved for NLP tasks requiring meaningful input text.

---

## Critical Bugs Found & Fixed

### 1. 🚨 GSS: All 1,303 Rows Had `support_pct = 0.0`

**Severity:** Critical. Rendered the entire GSS dataset useless for training.

**Root cause:** In `scripts/extract_gss.py` line 152, `support_value` is a string (`'too_little'`, `'favor'`, etc.) but the comparison `valid == support_value` compares against integer codes (1, 2, 3) in the Stata data. Every row evaluated to 0.

**Fix:** Added integer-key lookup from the value-label dict before comparison. Support percentages now range from 3.1% to 93.0% across 35 years and 45 variables.

**Impact:** 1,303 rows restored from all-zero to correct values. GSS data now covers 1972-2024 with real support percentages.

### 2. 🚨 DFP Issues: 1,788 Rows Were Narrative Fragments, Not Polling Data

**Severity:** Critical. The `question_wording` field contained narrative text from blog posts (e.g., "Younger voters (73%) and renters (64%) are even more likely..."), not actual poll question wording. The `support_pct` values were the first percentage found in the text — often demographic breakdowns, not actual support rates.

**Root cause:** The original DFP chunk parser (`parse_dfp_chunks.py`) extracted every bullet point containing a percentage and treated it as a polling data point, without distinguishing support percentages from demographic breakdowns.

**Fix:** Re-extracted all DFP data from raw chunks with:
- Demographic percentage filtering (50 identified as pure demographic)
- Sample-size bullet skipping (145 removed)
- No-percentage bullet removal (228 removed)
- Proper question_type classification (20 distinct types vs. 1)
- Article URL and title context preserved

**Impact:** 1,788 → 1,298 rows. 490 fragments removed. Remaining rows have contextualized findings. The `question_wording` field is still narrative (not question text), but the `question_type` field now honestly labels each as `support`, `disapproval`, `trust`, `priority`, etc.

**Remaining limitation:** DFP blog posts do not contain structured poll question wording. The data is best understood as "polling findings" rather than traditional "issue polling." See recommendations below.

### 3. 🚨 NAV_NEW: 16 Rows Had DFP URLs Labeled as Navigator

**Severity:** High. Rows NAV_NEW_1001 through NAV_NEW_1016 had `source = "Navigator Research"` but `source_url = dataforprogress.org/...`. These were DFP tested statements mistakenly classified as Navigator during Phase 1 extraction.

**Fix:** Removed from messages.csv. These were qualitative tested statements without support percentages — not usable for training regardless.

**Impact:** messages.csv reduced from 224 → 213 rows (removed 16 misclassified, added 5 new from "Who Americans Trust" article).

### 4. 🐛 DFP_20210409_1604 Had `support_pct = 120.0`

**Severity:** Medium. Out-of-range value.

**Root cause:** The parser picked up "120%" from "capping the price... at 120% of the cost" (drug price cap percentage) instead of the actual support percentage (69%).

**Fix:** Corrected to 69.0 based on source article context.

### 5. 📊 Blueprint BLP_20260121_* Missing Effect Scores

**Severity:** Medium. Three Blueprint rows had empty `preference_effect` fields when the source article clearly reported net concern scores.

**Fix:** Backfilled +27 net concern scores from Wayback Machine verification. Effect scale set to `net_concern`.

---

## Source Verification Results

### Navigator Research — ✅ Verified Accurate

Cross-referenced 3 articles against live website:
- **Healthcare costs** (May 7): All 7 extracted percentages match (61%, 52%, 47%, 39%, 59%, etc.)
- **Tariffs** (Feb 20): All 3 extracted percentages match (30%, 69%)
- **Iran war** (Apr 29): All 6 extracted percentages match (50%, 49%, 58%, 64%, 70%, etc.)

**Source URL quality issue:** 72 of 142 Navigator rows have `source_url = "https://navigatorresearch.org/"` (homepage, not article-specific). These came from PDF topline extraction where the article URL wasn't captured. Non-critical but reduces provenance traceability.

### Blueprint Research — ✅ Verified Accurate

Cross-referenced 2 articles via Wayback Machine:
- **Trump Economy** (Jan 2026): Net concern scores verified (+27 for all 3)
- **Dem Message Test** (Dec 2025): MaxDiff scores match (+14, +12, +11)

**Wording quality note:** 12 of 71 Blueprint messages are <30 chars. These are summaries/metadata (e.g., "Trump healthcare net approval", "Elon Musk favorability") rather than tested message wording. Low-impact — they don't have metrics anyway.

---

## Dataset State After Fixes

### messages.csv — 213 rows

| Source | Rows | With Metric | Quality |
|--------|------|:----------:|---------|
| Navigator Research | 142 | 125 (88%) | ✅ Verified against live site |
| Blueprint Research | 71 | 63 (89%) | ✅ Verified via Wayback Machine |
| **Total** | **213** | **190 (89%)** | **Training-ready** |

- 0 out-of-range values
- 0 duplicate IDs
- 13 topics (economy 54, healthcare 38, immigration 30, foreign_policy 25, politics 21, democracy 20)
- Date range: 2024-02-16 to 2026-05-07
- 12 short wordings (<30 chars) — summaries, not messages

### issues.csv — 5,069 rows

| Source | Rows | Notes |
|--------|------|-------|
| Gallup | 1,830 | MIP monthly tracking, 2001-2026 |
| General Social Survey | 1,303 | **FIXED** — was all zeros, now correct |
| Data for Progress | 1,298 | **CLEANED** — 490 fragments removed |
| CES | 447 | 2006-2021, 11 topics |
| Pew Research Center | 175 | PDF toplines + SOTU |
| YouGov | 6 | Historic tracker data |
| AP-NORC | 6 | 2025-2026 issue priorities |
| Ipsos/Reuters | 4 | Trump approval, cost of living |
| **Total** | **5,069** | **8 sources, 49 years (1972-2026)** |

- 0 out-of-range support_pct values
- 0 duplicate poll_ids
- 47 topics
- 20 question types
- GSS support_pct range: 3.1%–93.0% (fixed from all-zeros)
- 65.4% null oppose_pct (expected — many sources report only support)

### referendums.csv — 337 rows

| State | Years | Notes |
|-------|-------|-------|
| 48 states + DC | 2008-2024 | 16 topics |

- **60.5% missing support_pct** (204 rows; was 75.9% before backfill)
- **24.6% missing passed status** (83 rows; was 37.5% before backfill)
- **2020: 0% missing** — fully backfilled from Wikipedia Yes/No columns
- 100% null: subtopic, total_votes, partisan_leans, campaign_contributions
- 0 duplicate measure_ids

---

## Remaining Gaps & Recommendations

### High Priority

1. ~~**Referendum vote data (75.9% missing):** Only 76 of 315 rows have actual support/oppose percentages. The Wikipedia ballot measure pages contain full vote totals for all measures since 2008. Re-scrape from Wikipedia HTML or Wiki API to backfill.~~ ✅ **Partially fixed (May 9).** 2020 data fully backfilled (0% missing). 2018 partially backfilled (48%→11 remaining). 2008–2016 and 2022 still lack vote percentages — Wikipedia pages for these years do not contain wikitable tables with Yes/No columns. Ballotpedia (WAF-protected) would be needed.

2. ~~**Referendum pass/fail (37.5% missing):** 118 rows have no outcome. Wikipedia pages clearly state whether each measure passed or failed. Can be extracted from the same source.~~ ✅ **Partially fixed (May 9).** Backfilled 35 rows via Wikipedia backfill. 83 rows remain missing (71 from 2008–2016 which lack structured tables; 12 from 2018 states without tables).

3. **Pew PDFs (2010-2023 gap):** The Phase 1 backfill plan identified ~8 target Pew PDFs filling the 2010-2023 gap. Only 4 PDFs downloaded and parsed so far (2011, 2014, 2017, 2021 typology/polarization). Search `site:assets.pewresearch.org topline pdf` for additional years. PDFs at assets.pewresearch.org are directly downloadable via curl — no Cloudflare.

4. ~~**DFP issue data — structural limitation:** DFP blog posts contain narrative polling findings, not structured question wording. The `question_wording` field contains findings text, not question text. For training purposes, this is better treated as context/knowledge embedding data rather than structured polling data. Consider adding a `data_quality` field to flag narrative-vs-structured.~~ ✅ **Fixed (May 9).** Added `data_quality` column to issues.csv. DFP rows = `narrative_finding`. All other sources = `structured_poll`.

### Medium Priority

5. **Navigator source_urls (72 rows have homepage URL):** PDF topline extraction didn't capture per-article URLs. Re-extract from PDF filenames or article pages to assign specific URLs.

6. ~~**Blueprint wording quality (12 short/summary entries):** 12 entries under 30 chars are topic summaries, not tested messages. Review and clean. Low-impact since they lack metrics.~~ ✅ **Fixed (May 9).** All 12 expanded to descriptive wordings (30–114 chars). Notes clarify these were survey category labels.

7. **YouGov endpoint degraded:** The YouGov homepage was redesigned as a corporate marketing site (May 2026). The Angular SPA with political tracker data is no longer accessible. Alternative: per-article Datawrapper chart extraction.

8. **ANES data access:** The ANES cumulative file requires manual browser download (Cloudflare). Once downloaded, extract 1948-2024 trend data using pyreadstat (similar to GSS/CES pipeline).

### Low Priority

9. **Chunks 2-4 DFP re-extraction:** The new re-extraction script only processed chunk1 (194 articles). Chunks 2-4 use different markdown formats and were not parsed. Chunk2 primarily contains message tests (already assessed and cleaned from messages.csv). Chunks 3-4 have older data (2021-2022) with different metadata formats.

10. **Ballotpedia integration:** ~1,200 additional ballot measures available but behind WAF. Wikipedia API alternative partially explored.

11. **California propositions:** ~600 CA propositions (1911-2020) with full ballot text from UC Law SF. Extraction script exists but not yet run.

---

## Training Utility Assessment

### What Works Well

- **213 tested messages with exact wording** — 190 (89%) have support percentages or preference effects. Excellent for supervised fine-tuning on political message generation and effectiveness prediction.
- **5,069 issue polling data points** — 49 years of coverage. Strong for embedding political knowledge and issue salience patterns.
- **315 ballot measures** — 48 states, good for understanding referendum framing and outcome patterns.
- **Multi-source triangulation** — 8 sources prevent overfitting to any single pollster's methodology.

### What's Missing for Comprehensive Training

- **Message A/B tests are only 2 sources** — Blueprint (MaxDiff) and Navigator (support%). No DFP message tests survived quality audit. A third source would improve robustness.
- **Messages are 2024-2026 only** — No historical message tests before 2024. Limits ability to learn framing evolution.
- **DFP "issue" data is narrative, not structured** — 1,298 rows are blog-post findings, not question-wording+support% pairs. They provide topical coverage but not the clean input-output pairs needed for direct supervised training.
- **No demographic crosstabs in messages** — Schema has `dem_*` fields but none are populated. Limits ability to learn audience-specific messaging.
- **Referendums missing vote data** — 75.9% lack the core training signal (support/oppose percentages).

### Recommended Next Steps for Training Readiness

1. ~~**Fix referendum vote data** — scrape from Wikipedia (highest ROI, unlocks 239 rows)~~ ✅ **Partially done.** 2020 fully fixed. 2018 partially fixed. 2008–2016 and 2022 require Ballotpedia (WAF-protected) or alternative source.
2. **Download ANES cumulative file** — manual browser download, then pyreadstat extraction (adds 1948-2024 issue trend data)
3. **Backfill Pew PDFs 2010-2023** — fill the historical gap (potential ~4,000 new issue rows)
4. ~~**Add `data_quality` field to issues.csv** — flag DFP rows as "narrative_finding" vs "structured_poll"~~ ✅ **Done.**
5. **Consider message data augmentation** — if 213 messages is insufficient, re-approach DFP chunk2 with the improved parser for additional tested message wording

---

## Audit Methodology

1. **Schema compliance:** Column-by-column comparison against schema definitions
2. **Value range validation:** All percentage fields checked for 0-100 bounds
3. **ID uniqueness:** Primary key deduplication verified
4. **Null rate analysis:** Per-column with context assessment
5. **Source verification:** 5 articles cross-referenced against live websites/web archives
6. **Re-extraction:** DFP and GSS data re-extracted from raw sources with corrected parsers
7. **Regression testing:** All fixes verified post-merge with fresh CSV reads

---

*Audited by: Makima (research director persona)*
*Date: May 9, 2026*
*Supplementary fixes: same date, post-audit implementation*
*Project: /home/agentbot/workspace/us-political-messaging-dataset/*
