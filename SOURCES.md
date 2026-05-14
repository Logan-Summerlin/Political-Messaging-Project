# US Political Messaging Dataset — Sources & Methodology
**Last updated:** May 7, 2026
**Project:** `/home/agentbot/workspace/us-political-messaging-dataset/`

---

## 1. MESSAGE TESTING DATA (A/B Tests with Exact Wording)

### 1a. Blueprint Research
- **Website:** [blueprint-research.com](https://blueprint-research.com)
- **Type:** Democratic message testing cooperative (run by Slingshot Strategies)
- **Data range:** July 2024 – February 2026
- **Articles extracted:** 26 total; 19 in messages.csv (70 rows), 7 with format limitations
- **Methodology:** MaxDiff analysis, preference effects, favorability deltas, A/B comparisons
- **Sample sizes:** 1,383 – 5,764 likely/registered voters
- **Key metrics:** Preference effect scores (+/-), support %, demographic crosstabs
- **Topics covered:** Vision messaging, closing arguments, abortion, SS/Medicare, economy, authoritarianism, immigration, candidate bios, ad testing
- **Access:** Free, no Cloudflare, all articles publicly available
- **File:** `sources/blueprint_message_testing_data.md` (400 lines, 15 KB)
- **Rows in messages.csv:** 70 (36 with preference_effect, 29 with support_pct)

### 1b. Navigator Research
- **Website:** [navigatorresearch.org](https://navigatorresearch.org)
- **Type:** Progressive message testing cooperative
- **Data range:** March 2025 – May 2026 (22 articles identified)
- **Articles extracted:** 13 with structured poll data; 9 qualitative-only (Do's and Don'ts, guidance)
- **Methodology:** Pre/post message exposure tests, agree/disagree scales, convincingness ratings
- **Sample sizes:** ~1,500 likely voters per wave (Impact Research/GSG)
- **Key metrics:** Support %, net favorability
- **Topics:** Tax policy, Iran war, SAVE Act, tariffs, healthcare costs, trust, fraud/cuts, food prices, budget priorities, ICE/immigration, DOGE/Musk, MAHA
- **Access:** Free, WordPress RSS feed at /feed/
- **File:** `data/raw/navigator/navigator_full_archive.md` (1,509 lines, 126 KB)
- **Rows in messages.csv:** 53 (51 with support/oppose values)

### 1c. Data for Progress
- **Website:** [dataforprogress.org](https://www.dataforprogress.org)
- **Type:** Progressive polling and research firm
- **Data range:** 2018 – present
- **RSS feed:** Working (20 items per page, paginated at `?format=rss&page=N`)
- **Methodology:** Online panel surveys with exact polling percentages
- **Topics:** Economy, healthcare, immigration, Iran war, China, AI, minimum wage, climate, housing
- **Access:** Free, NO Cloudflare (Squarespace), fully scrapeable
- **Estimated volume:** 775+ articles in 4 raw chunks (921 KB)
- **Rows in messages.csv:** 318 (93 original + 94 staging + 20 chunk1 extracted + 111 cross-referenced from existing)
- **Rows in issues.csv:** 1,731

### 1d. Other Sources Investigated
| Source | Verdict | Reason |
|--------|---------|--------|
| **Echelon Insights** | Partial | Some public polling reports, less focused on A/B message testing |
| **YouGov** | Partial | Extensive tracker data but not structured as A/B message tests |
| **Lake Research Partners** | ❌ No public data | Corporate brochure site |
| **Tarrance Group** | ❌ No public data | Corporate brochure site |
| **GS Strategy Group** | ❌ No public data | Corporate brochure site |
| **Public Opinion Strategies** | ❌ SSL error | |
| **PSB Insights** | ❌ No public data | Corporate site |
| **Winning Message** | ❌ Defunct | Domain unresolvable |
| **Equis Research** | ❌ Defunct | Domain expired |
| **HIT Strategies** | ⚠️ Partial | Some research publications, JS-heavy Wix site |

---

## 2. ISSUE POLLING DATA (Exact Question Wording + Percentages)

### 2a. Gallup — Most Important Problem
- **Rows in issues.csv:** 1,830
- **Years:** 2001–2026 monthly
- **Extraction:** Datawrapper chart CSV APIs (bypassed browser requirement)
- **Method:** Economy mentions (2001–2021) + detailed topic breakdowns (2022–2026) across 15 categories
- **Access:** news.gallup.com/poll/1675/most-important-problem.aspx

### 2b. Data for Progress — Issue Polling
- **Rows in issues.csv:** 1,731 (1,732 more in staging)
- **Years:** 2024–2026
- **Source:** 775 articles in 4 raw markdown chunks (921 KB)
- **Method:** Squarespace RSS + HTML scraping

### 2c. General Social Survey (GSS)
- **Rows in issues.csv:** 1,303 (merged)
- **Years:** 1972–2024
- **Variables:** 5,900+ across 21 topic areas
- **Topics:** Environment, abortion (7 conditions), guns, immigration, healthcare, race, civil liberties, spending priorities, social security, welfare, crime, education, family, religion, technology
- **Source:** gss.norc.org — free download
- **File:** `data/raw/gss/` — Stata (.dta, 598 MB), SPSS (.sav, 3.8 GB), codebooks
- **Extraction:** pyreadstat with encoding='latin1'

### 2d. Pew Research Center
- **Rows in issues.csv:** 150
- **Source:** State of the Union 2026 analysis (Feb 23, 2026) + 4 typology PDFs
- **Key stats:** Economy (28% good), tariffs (60% disapprove), healthcare costs (71% concerned), food prices (66%), housing (62%)
- **PDF toplines:** 4 of ~8 target PDFs downloaded (2011/2014/2017/2021 typologies); 143 rows extracted
- **Remaining:** Values surveys (2010–2023), trust in government, polarization 2017/2022

### 2e. AP-NORC
- **Rows in issues.csv:** 6
- **Source:** December 2025 + January 2026 polls
- **Access:** Server-rendered HTML, accessible via curl

### 2f. Ipsos / Reuters
- **Rows in issues.csv:** 4
- **Source:** March 2026 tracking poll
- **Access:** Cloudflare-protected but article text accessible

### 2g. YouGov
- **Rows in issues.csv:** 6
- **Access:** Angular SPA — needs browser extraction (Chrome sandbox blocked)
- **Status:** Minimal data extracted

### 2h. CES (Cooperative Election Study)
- **Rows in issues.csv:** 447
- **Years:** 2006–2021
- **Source:** Harvard Dataverse (doi:10.7910/DVN/II2DB6)
- **Method:** Cumulative Stata file (675 MB), extracted via pyreadstat with 11 policy topic areas (abortion, affirmative action, presidential approval, economy, environment, foreign policy, gay marriage, guns, healthcare, immigration, trade)
- **Variables extracted:** Approval ratings, economy perceptions, abortion views (6 sub-questions), gun policy (4 types), immigration (8 types), healthcare (ACA, Medicare), environment (carbon tax, renewable energy, fuel standards), trade policy, gay marriage, military policy, spending priorities
- **Access:** Free download from Harvard Dataverse

---

## 3. ACADEMIC SURVEY DATASETS

### Cooperative Election Study (CES)
- **Files:** `cumulative_2006-2024.dta` (675 MB), `cumulative_2006-2024.rds` (38 MB), 2 codebook PDFs
- **Years:** 2006–2024 cumulative (50,000+ respondents/year)
- **Variables:** 109 covering voting, party ID, ideology, approval, policy preferences
- **Source:** Harvard Dataverse (doi:10.7910/DVN/II2DB6) — free download
- **Status:** Downloaded; Stata file has encoding issues blocking extraction

---

## 4. BALLOT MEASURE / REFERENDUM DATA

### Processed
- **referendums.csv:** 199 rows, 9 states, 2024–2025
- **Topics:** Abortion (largest), crime, minimum wage, cannabis, education, voting, taxes, environment

### Raw — Unprocessed
| Source | Rows | Coverage | Status |
|--------|------|----------|--------|
| Wikipedia ballot measures | 592 | 2008–2024 national | Not merged into referendums.csv |
| California UC Law | 600+ | 1911–2020 CA propositions | Extraction script exists |
| Ballotpedia | Unlimited | All states, all years | WAF-blocked (AWS WAF challenge) |

---

## 5. COMPILED DATASETS (Processed)

| Dataset | File | Rows | Content |
|---------|------|------|---------|
| Message tests | `data/processed/messages.csv` | 216 | A/B message wording + preference effects + support% |
| Issue polling | `data/processed/issues.csv` | 5,030 | Exact question wording + support%/oppose%/net |
| Ballot measures | `data/processed/referendums.csv` | 199 | Measure language + vote shares + thresholds |
| GSS staging | `data/processed/gss_issues.csv` | 1,303 | (Already merged into issues.csv) |
| DFP staging (issues) | `data/processed/dfp_new_issues.csv` | 1,732 | Ready for merge |
| DFP staging (messages) | `data/processed/dfp_new_messages.csv` | 95 | Ready for merge |

---

## 6. EXTRACTION METHODOLOGY

### JavaScript-Rendered Sites (need browser)
- **Gallup** — Bypassed via embedded Datawrapper CSV APIs
- **YouGov** — Angular SPA, browser required

### Cloudflare-Protected Sites
- **Pew PDF toplines** — Cloudflare challenge (partially extracted via downloaded PDFs)
- **Ballotpedia** — AWS WAF challenge
- **NCSL** — Cloudflare

### Direct Access (curl works)
- **Blueprint Research** — Server-rendered HTML
- **Data for Progress** — Squarespace, no bot protection
- **AP-NORC** — Server-rendered HTML
- **Chicago Council** — Server-rendered HTML
- **CA SoS / UC Law SF** — No bot protection
- **GSS** — Direct file download (NORC)
- **CES** — Harvard Dataverse API

---

*Compiled May 7, 2026 | Questions or corrections: contact project owner*
