# US Political Messaging & Issue Polling Dataset

**A structured, queryable dataset of US political issue polling, message testing A/B results, and ballot measure outcomes.** Exact wording, support percentages, methodology, and source links. Designed for message strategy, framing analysis, and campaign research.

**5,649 total data points** across 3 unified tables — 213 tested messages, 5,099 issue poll questions, 337 ballot measures — spanning **1972–2026** from **8 sources**.

## 📁 Directory Structure

```
us-political-messaging-dataset/
├── README.md                          # This file — project overview
├── SOURCES.md                         # Full source methodology catalog
│
├── data/
│   ├── processed/                     # Cleaned, normalized datasets
│   │   ├── messages.csv               #   255 rows — A/B message tests
│   │   ├── issues.csv                 # 5,030 rows — issue polling
│   │   ├── referendums.csv            #   315 rows — ballot measures
│   │   ├── gss_issues.csv             # 1,303 rows — GSS extracted (staging)
│   │   ├── dfp_new_messages.csv       #    95 rows — DFP staging
│   │   └── dfp_new_issues.csv         # 1,732 rows — DFP staging
│   │
│   └── raw/                           # Original source files, as collected
│       ├── dataforprogress/           #   4 chunks, 775 articles (921 KB)
│       ├── navigator/                 #   16 articles, full archive (126 KB)
│       ├── gallup/                    #   Gallup MIP extraction (1,830 rows)
│       ├── pew/                       #   4 PDFs + extraction script
│       ├── gss/                       #   GSS Stata data (598 MB) + codebooks
│       ├── ces/                       #   CES cumulative data (675 MB)
│       ├── california/                #   600 CA propositions
│       ├── yougov/                    #   YouGov extracts
│       └── wikipedia_ballot_measures.csv  # 592 raw measures
│
├── sources/                           # Source documentation & extracted data
│   ├── blueprint_message_testing_data.md   # 26 articles, MaxDiff scores
│   ├── dataset_inventory.md                # Master dataset inventory
│   ├── message_testing_source_catalog.md   # Org catalog (18 sources)
│   ├── polling_data_summary.md             # Polling source summaries
│   ├── ballot_measure_source_catalog.md    # Ballot source catalog
│   └── ballot_measures_research.md         # Ballot research notes
│
├── schema/                            # Data schema definitions
│   ├── messages_schema.md
│   ├── issues_schema.md
│   └── referendums_schema.md
│
├── scripts/                           # Extraction, processing, merge scripts
│   ├── extract_blueprint_messages.py  # Blueprint message extraction
│   ├── extract_gss.py                 # GSS extraction
│   ├── merge_gss.py                   # GSS → issues.csv merge
│   ├── merge_and_extract.py           # DFP merge + Navigator extraction
│   ├── parse_dfp_chunks.py            # DFP raw → structured
│   ├── rebuild_messages.py            # messages.csv rebuild
│   ├── scan_gss.py                    # GSS variable scanner
│   ├── scrape_wiki_ballot_measures.py # Ballot measure scraper
│   └── extract_uclaw.py              # CA proposition extractor
│
├── plans/
│   └── phase1_backfill.md            # Historical backfill plan (2010–2023)
│
└── .hermes/
    └── AGENTS.md                     # Project context for agent sessions
```

## 📊 Dataset Summary

| Table | Rows | Date Range | Primary Sources | Key Metrics |
|---|---|---|---|---|---|
|| **messages.csv** | **213** | 2024–2026 | Navigator (142), Blueprint (71) | support%, preference_effect (MaxDiff) |
|| **issues.csv** | **5,099** | 1972–2026 | Gallup (1,830), GSS (1,303), DFP (1,298), CES (447), Pew (205) | support%, oppose%, net |
|| **referendums.csv** | **337** | 2008–2024 | Wikipedia (national ballot measure pages) | support%, threshold, margin |

### Message Testing

Two independent sources of A/B tested political messages with exact wording:

- **Blueprint Research** — 71 rows. MaxDiff preference scores, support percentages. Covers vision messaging, closing arguments, abortion, SS/Medicare, economy, candidate bios, ad testing. (2024–2026)
- **Navigator Research** — 142 rows. Support/oppose percentages and tracking polls. Covers tax policy, Iran war, tariffs, healthcare costs, trust, party trust, immigration. (2025–2026)

**Training-ready:** 190 of 213 messages (89.2%) have wording + a quantitative metric.

### Issue Polling

Eight sources:

- **Gallup** — 1,830 rows. "Most Important Problem" monthly tracking, 2001–2026. Extracted via Datawrapper chart CSV APIs.
- **General Social Survey** — 1,303 rows. 1972–2024, 45 variables across national spending, confidence, abortion, guns, immigration. Extracted from Stata file via pyreadstat.
- **Data for Progress** — 1,298 rows. Narrative polling findings from 194 articles (2019–2026). Re-extracted May 9, 2026 with demographic filtering. Flagged as `data_quality: narrative_finding` in issues.csv (distinct from structured poll questions).
- **CES (Cooperative Election Study)** — 447 rows. 2006–2021, 11 topic areas. Extracted from cumulative Stata file (675 MB).
- **Pew Research Center** — 205 rows. Typology surveys (2011, 2014, 2017, 2021) and appendix topline. Extracted from PDF via pymupdf. +30 rows added May 9, 2026 from re-extraction covering 2011 and 2017 questions not previously captured.
- **AP-NORC, YouGov, Ipsos** — 16 rows combined. 2025–2026 issue priorities and tracking.

### Ballot Measures

337 measures from 2008–2024 normalized from Wikipedia sources. **May 2026 backfill:** 22 new rows added with vote percentages from 2020 Wikipedia tables; 2020 coverage now 100% complete. 2022 has pass/fail outcomes only (no vote percentages on Wikipedia). 2008–2016 have limited Wikipedia data.

Raw holdings split across `wikipedia_ballot_measures.csv` and `wikipedia_ballot_measures_complete.csv`, plus ~600 California UC Law records pending integration.

## 📐 Schema

### messages.csv (19 columns)
`message_id`, `source`, `source_url`, `date`, `topic`, `issue_area`, `message_type`, `wording`, `support_pct`, `oppose_pct`, `net_score`, `preference_effect`, `effect_scale`, `sample_size`, `methodology`, `population`, `moe`, `tags`, `notes`

### issues.csv (16 columns)
`poll_id`, `source`, `source_url`, `date`, `question_type`, `question_wording`, `topic`, `issue_area`, `support_pct`, `oppose_pct`, `net`, `sample_size`, `methodology`, `population`, `moe`, `tags`, `notes`

### referendums.csv (22 columns)
`measure_id`, `state`, `year`, `election_date`, `election_type`, `measure_name`, `wording`, `summary`, `topic`, `subtopic`, `passed`, `support_pct`, `oppose_pct`, `threshold`, `margin`, `votes_for`, `votes_against`, `total_votes`, `partisan_leans`, `campaign_contributions`, `tags`, `source_url`, `notes`

Full schema details in `schema/` directory — see `messages_schema.md`, `issues_schema.md`, `referendums_schema.md` for field types, required status, controlled vocabularies, and validation rules.

## 🔧 Extraction & Processing

- **Direct scrape** — curl + Python stdlib for server-rendered sites (Blueprint, DFP, AP-NORC, Chicago Council)
- **RSS feeds** — Google News RSS for broad article discovery (no rate limits, 100 results/query)
- **PDF extraction** — pymupdf for Pew topline PDFs
- **Academic data** — pyreadstat for GSS/CSV Stata files (note: encoding='latin1' required)
- **Datawrapper API** — Gallup chart data extracted from embedded Datawrapper CSVs
- **Browser extraction** — agent-browser (Playwright/Chromium) for JS-rendered content as needed

## 🗺️ Phase 1 Priority: Historical Backfill (2010–2023)

1. **Pew PDF toplines** — ~8 target PDFs, 4 downloaded + 143 rows extracted
2. **Gallup MIP** — ✅ Complete (1,830 rows)
3. **YouGov** — Blocked by browser sandbox; alternative method needed
4. **Wikipedia/ballot-measure raw splits** — 592 raw rows normalized via the referendum pipeline with ongoing schema harmonization checks
5. **CES** — 675 MB Stata file downloaded, encoding issues to resolve
6. **ANES** — Cloudflare blocked
7. **California Propositions** — 600 rows raw, extraction script exists but not run

---

*Last updated: May 9, 2026 — Critical bug fixes applied (GSS support_pct, DFP narrative fragments, NAV_NEW reclassification); data_quality field added; referendum vote data backfilled (2020 100%); Blueprint short entries expanded; Pew PDF re-extraction (+30 rows, 2014 appendix added); referendums 337 rows; issues 5,099 rows*
*See sources/phase1_critical_audit_2026-05-09.md for full quality audit report.*
*Project by Logan*
