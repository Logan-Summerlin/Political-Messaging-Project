# Dataset v1.0 Provenance Manifest
**Date:** 2026-05-08
**Snapshot:** `data/archive/v1.0.0/`
**Project:** US Political Messaging Dataset

## Snapshot Contents

| File | Rows | Sources | Year Range |
|------|------|---------|-----------|
| issues.csv | 5,477 | 8 | 1972 – 2026-05 |
| messages.csv | 387 | 3 | 2019 – 2026-05 |
| referendums.csv | 315 | 1 (Wikipedia) | 2008 – 2024 |
| **Total** | **6,179** | **11 organizations** | |

## Changes from Previous State

### Issues Table (was 5,030 → now 5,477)
| Change | Source | Rows |
|--------|--------|------|
| CES issue polling extracted and reshaped | CES (Cooperative Election Study) | +447 |
| DFP staging (already merged) | Data for Progress | 0 new (already present) |

### Messages Table (was 255 → now 387)
| Change | Source | Rows |
|--------|--------|------|
| DFP staging merge | Data for Progress | +94 |
| DFP new extracted (chunk1 Message Wording Tested sections) | Data for Progress | +20 |
| Navigator new articles from RSS feed | Navigator Research | +18 |
| **Net growth** | | **+132 rows** |

### Referendums Table (was 199 → now 315)
| Change | Source | Rows |
|--------|--------|------|
| Full Wikipedia integration (2008-2024) | Wikipedia scrape | +116 |
| | **Net growth** | **+116 rows** |

## Source Inventory

### Issue Polling Sources
| Source | Rows | Years | Access Method |
|--------|------|-------|---------------|
| Gallup (MIP) | 1,830 | 2001-2026 | Datawrapper CSV |
| Data for Progress | 1,731 | 2018-2026 | RSS + HTML |
| General Social Survey | 1,303 | 1972-2024 | Stata file |
| CES (Cooperative Election Study) | 447 | 2006-2021 | Stata file |
| Pew Research Center | 150 | 2026 | PDF extraction |
| YouGov | 6 | 2026 | Web scraping |
| AP-NORC | 6 | 2025-2026 | Curl HTML |
| Ipsos/Reuters | 4 | 2026 | Curl HTML |

### Message Testing Sources
| Source | Rows | Years | Type |
|--------|------|-------|------|
| Data for Progress | 318 | 2019-2026 | Issue message tests |
| Navigator Research | 60 | 2025-2026 | Pre/post exposure tests |
| Blueprint Research | 9 | 2024-2026 | MaxDiff preference scores |

### Ballot Measure Sources
| Source | Rows | Years | Notes |
|--------|------|-------|-------|
| Wikipedia | 315 | 2008-2024 | 48 states, 16 topics |

## Data Quality Metrics
| Metric | Issues | Messages | Referendums |
|--------|--------|----------|-------------|
| Provenance completeness | 100% | 100% | 100% |
| Duplicate rate | 0% | 0% | 0% |
| Null support_pct | 0.0% | 79% | 78% |
| Topic diversity | 45 topics | 15 topics | 16 topics |
| State coverage | National | National | 48 states |

## Schema Versions
- issues_schema.md — v1 (16 columns)
- messages_schema.md — v1 (19 columns)
- referendums_schema.md — v1 (22 columns)

## Extraction Pipelines Used
1. `scripts/merge_staging.py` — DFP staging → messages.csv
2. `scripts/merge_extracted_messages.py` — DFP extracted → messages.csv
3. `scripts/reshape_ces.py` — CES wide → long format
4. `scripts/merge_and_extract.py` — DFP + Navigator merge
5. `scripts/extract_gss.py` — GSS Stata extraction
6. `scripts/parse_dfp_chunks.py` — DFP chunk parsing
7. `scripts/scrape_wiki_ballot_measures.py` — Wikipedia scrape
8. `scripts/validate_data_quality.py` — Validation checks

## Known Limitations
- Navigator message tests may be undercounted: the actual test data is in image-based PDFs
- Referendum wording field is largely empty; Wikipedia pages list measure names but not full ballot text
- Gallup data has a freshness ceiling at 2026-03-02 (no newer public data available)
- DFP RSS feed extraction has 14 known URLs not yet ingested from the live feed
