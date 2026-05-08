# US Political Messaging & Issue Polling Dataset

**A structured, queryable dataset of US political issue polling, message testing A/B results, and ballot measure outcomes.** Exact wording, support percentages, methodology, and source links. Designed for message strategy, framing analysis, and campaign research.

**3,369 total data points** across 3 unified tables — 216 tested messages, 5,030 issue poll questions, 199 ballot measures — spanning **1972–2026** from **10+ sources**.

## 📁 Directory Structure

```
us-political-messaging-dataset/
├── README.md                          # This file — project overview
├── SOURCES.md                         # Full source methodology catalog
│
├── data/
│   ├── processed/                     # Cleaned, normalized datasets
│   │   ├── messages.csv               #   216 rows — A/B message tests
│   │   ├── issues.csv                 # 5,030 rows — issue polling
│   │   ├── referendums.csv            #   199 rows — ballot measures
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
|---|---|---|---|---|
| **messages.csv** | 216 | 2024–2026 | Blueprint (70), Navigator (53), DFP (93) | support%, preference_effect (MaxDiff) |
| **issues.csv** | 5,030 | 1972–2026 | Gallup (1,830), DFP (1,731), GSS (1,303), Pew (150) | support%, oppose%, net |
| **referendums.csv** | 199 | 2024–2025 | Ballotpedia, Wikipedia (9 states) | support%, threshold, margin |

### Message Testing

Three independent sources of A/B tested political messages with exact wording:

- **Blueprint Research** — 70 rows. MaxDiff preference scores, support percentages, demographic crosstabs. Covers vision messaging, closing arguments, abortion, SS/Medicare, economy, authoritarianism, candidate bios, ad testing. (2024–2026)
- **Navigator Research** — 53 rows. Poll questions with support/oppose percentages. Covers tax policy, Iran war, SAVE Act, tariffs, healthcare costs, trust, fraud/cuts, food prices. 51 rows have numeric support/oppose values. (2025–2026)
- **Data for Progress** — 93 rows. Issue-specific message tests. Many need richer extraction from raw chunks. (2018–2026)

### Issue Polling

Seven sources, dominated by three:

- **Gallup** — 1,830 rows. "Most Important Problem" monthly tracking, 2001–2026. Extracted via Datawrapper chart CSV APIs.
- **Data for Progress** — 1,731 rows. Issue polling 2024–2026. 1,732 more in staging.
- **General Social Survey** — 1,303 rows. 1972–2024, 21 topic areas. Extracted from Stata file via pyreadstat.
- **Pew Research** — 150 rows. State of the Union 2026 toplines + 4 typology PDFs.

### Ballot Measures

199 measures from 9 states, 2024–2025. 592 more raw records from Wikipedia and 600 from California UC Law still unprocessed.

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
4. **Ballotpedia** — 592 raw rows not yet structured into referendums.csv
5. **CES** — 675 MB Stata file downloaded, encoding issues to resolve
6. **ANES** — Cloudflare blocked
7. **California Propositions** — 600 rows raw, extraction script exists but not run

---

*Last updated: May 7, 2026*
*Project by Logan*
