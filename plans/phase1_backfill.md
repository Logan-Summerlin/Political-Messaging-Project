# Phase 1: Backfill 2010–2023 Historical Data

**Goal:** Expand the dataset from current (2024-2026) coverage back to 2010, giving ~16 years of continuous political polling and ballot measure data.

## Priority Order — Progress as of May 7, 2026

### P1 — Pew Research Toplines (PDF)
**Status:** ✅ 4 of ~8 PDFs downloaded, 143 rows extracted
**How:** `pymupdf` to extract from topline PDFs at pewresearch.org
**What to get:**
- Political Typology surveys (2011, 2014, 2017, 2020, 2023)
- Political Polarization surveys (2014, 2017, 2022)
- Values surveys (biennial, 2010-2023)
- Trust in government (annual, 2010-2023)
- Internet/technology surveys — only where politically relevant
- **Estimate:** ~8 PDFs, ~500 questions each = ~4,000 data points

### P1 — Gallup Most Important Problem
**Status:** ✅ Complete — 1,830 rows extracted (2001–2026)
**How:** Datawrapper chart CSV APIs (bypassed browser requirement)
**What to get:**
- Monthly "Most Important Problem" rankings, 2010-2023
- Annual "State of the Union" and "Satisfaction" polls
- **Estimate:** ~168 monthly data points + annual summaries

### P1 — GSS (General Social Survey)
**Status:** ✅ Complete — 1,303 rows extracted and merged into issues.csv (1972–2024, 21 topics)
**How:** Downloaded Stata file from gss.norc.org, extracted via pyreadstat with encoding='latin1'
**Variables:** 5,900+ covering economy, healthcare, abortion, guns, immigration, race, civil liberties, spending priorities, social security, environment, crime, education

### P2 — YouGov Issue Polling Archive (Browser)
**Why:** Extensive issue polling with demographic crosstabs
**How:** Browser extraction needed (Angular SPA, Chrome sandbox blocked)

### P2 — Ballotpedia Historical Measures
**Why:** Comprehensive ballot measure data 2010-2023
**How:** Wikipedia API action=query&prop=extracts for "List of United States ballot measures by year" pages
**Sources:**
- List of 2010 United States ballot measures
- List of 2011-2023 United States ballot measures
- **Estimate:** ~1,200 measures across 14 election cycles

### P2 — ANES / American National Election Studies
**Why:** Gold-standard academic survey, biennial since 1948, with extensive issue batteries
**How:** Download data from electionstudies.org (public access, requires registration)
- Cumulative data file (all years) in SPSS/Stata format
- **Estimate:** 100+ issue questions per year, ~1,600 questions 2010-2023

### P2 — Kaiser Family Foundation Health Tracking Poll
**Why:** Best ongoing healthcare-specific polling
**How:** Curl + browser extraction from kff.org/health-reform/poll-finding/
- Monthly health tracking polls
- **Estimate:** ~50 polls

### P3 — Cato/Reason Civil Liberties Surveys
**Why:** Annual surveys on civil liberties, free speech, privacy
**How:** cato.org + reason.com archives
- 2010-2023 annual surveys
- **Estimate:** ~13 surveys

### P3 — Public Policy Institute of California
**Why:** High-quality state-level issue polling
**How:** ppic.org survey archive
- Annual statewide surveys
- **Estimate:** ~26 reports (annual + special topics)

## Estimated Effort

| Phase | Sources | Data Points | Time Estimate |
|-------|---------|-------------|---------------|
| P1 (immediate) | Pew, Gallup, YouGov | ~4,400+ | 2-3 sessions |
| P2 (next) | Ballotpedia, ANES, KFF | ~2,850+ | 2-3 sessions |
| P3 (later) | Cato, PPIC, misc | ~500+ | 1 session |

## Technical Approach

### PDF Extraction (Pew)
```python
import fitz  # pymupdf
doc = fitz.open("pew_topline.pdf")
for page in doc:
    text = page.get_text()
    # Parse structured question→% format
```

### Browser Extraction (Gallup, YouGov)
```bash
agent-browser goto "https://news.gallup.com/poll/..."
agent-browser snapshot
# extract JS-rendered content from snapshot
```

### Wikipedia API (Ballot Measures)
```bash
curl "https://en.wikipedia.org/w/api.php?action=parse&page=List_of_${YEAR}_United_States_ballot_measures&format=json"
```
