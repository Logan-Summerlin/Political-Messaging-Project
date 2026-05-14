# Data For Progress Messaging Extraction Plan (2018–2026)

## Objective
Build a reproducible, ToS-compliant extraction pipeline for **Data For Progress** blog polling/messaging pages (2018–2026) that captures:
- article metadata,
- question/message wording,
- support/oppose/topline percentages,
- sample/methodology fields,
- provenance and quality flags.

## Terms-of-Service Constraint (Operationalized)
DFP ToS prohibits excessive automated requests (“robots/spiders… more request messages than a human can reasonably produce”).

Implementation guardrails:
1. **Human-rate traffic only**: max 1 request every 10–20 seconds (jittered), plus periodic longer pauses.
2. **Conditional fetching**: use `If-Modified-Since`/`ETag` where available.
3. **Single-pass crawl**: prioritize sitemap/RSS indexing over brute-force discovery.
4. **Caching-first**: never re-fetch unchanged pages.
5. **Stop/resume ledger**: maintain request log with timestamps + URL to prove conservative request behavior.

## Current Project State (relevant to DFP)
- Repository already contains DFP staging artifacts under `data/raw/dataforprogress/` (RSS + chunked markdown + article index) and scripts for parsing/cleaning DFP rows.  
- Existing scripts extract many issue rows and some message rows, but extraction quality is uneven for “narrative findings” and incomplete for precise **topline support tied to explicit question/message wording**.

## Quick Analysis of the Example Page
URL analyzed:  
`/blog/2024/12/11/voters-want-biden-to-continue-advancing-diplomatic-ties-with-cuba-during-his-lame-duck-session`

Observed structure characteristics to design for:
1. The page exposes a reliable `datePublished` in embedded JSON-LD.
2. The Open Graph/description metadata includes a usable topline sentence (e.g., “Fifty-eight percent … support …”).
3. Squarespace pages often include narrative prose plus media/graphics; not all numeric findings are guaranteed in machine-friendly tables.
4. Therefore extraction should be **multi-layered**: structured metadata first, article body second, and linked assets/toplines third.

## End-to-End Plan

### Phase 1 — Inventory (2018–2026)
1. Build canonical URL list from:
   - existing `article_index.csv`,
   - RSS feed snapshots,
   - sitemap(s) for `/blog/` entries.
2. Filter date window strictly to `2018-01-01` through `2026-12-31`.
3. Classify candidate pages into:
   - polling/messaging briefs,
   - election horserace-only posts,
   - non-poll commentary.

**Deliverable:** `data/raw/dataforprogress/dfp_2018_2026_url_inventory.csv`

### Phase 2 — ToS-compliant Acquisition
1. Create a downloader with:
   - randomized sleep (10–20s),
   - retry with backoff,
   - local HTML cache,
   - request ledger CSV.
2. Fetch only pages in inventory that are polling/messaging relevant.
3. Optional linked-file capture (PDF toplines/crosstabs) only when referenced on-page.

**Deliverables:**
- `data/raw/dataforprogress/html/YYYY/...html`
- `data/raw/dataforprogress/request_log.csv`

### Phase 3 — Structured Extraction Logic
Extract fields per article into normalized long format:
- `source_url`, `publish_date`, `title`
- `question_or_message_text`
- `metric_type` (`support`, `oppose`, `favorability`, `concern`, etc.)
- `value_pct`
- `population`, `sample_size`, `field_dates`, `mode`, `moe`
- `extraction_source` (`jsonld`, `meta_description`, `article_body`, `linked_pdf`)
- `confidence_score` + `needs_review`

Parsing order:
1. **Metadata layer**: JSON-LD + OG description for fast toplines.
2. **Body layer**: sentence-level percentage extraction + nearby clause binding.
3. **Asset layer**: parse linked PDF/graphic text when body is insufficient.

### Phase 4 — “Elegant Topline” Resolver
Implement a resolver that maps percentages to tested prompts/questions:
1. Detect candidate percentages in each paragraph/sentence.
2. Resolve the nearest policy/question clause.
3. Rank candidates and select primary topline(s) using rules:
   - appears in headline/dek/lead paragraph,
   - explicitly paired with support/oppose language,
   - repeated in methodology/topline sections.
4. Preserve alternates in audit columns (not discarded).

### Phase 5 — QA + Dedup + Merge
1. Validate ranges (`0–100`), parse dates, and de-duplicate repeated findings.
2. Compare against existing DFP rows in `issues.csv` and `dfp_new_issues.csv`.
3. Mark `data_quality` as:
   - `structured_poll` when wording+% linkage is explicit,
   - `narrative_finding` otherwise.
4. Human-review queue for low-confidence rows.

### Phase 6 — Final Outputs
1. Produce DFP-specific output tables:
   - `data/processed/dfp_messaging_toplines_2018_2026.csv`
   - `data/processed/dfp_messaging_toplines_2018_2026_review_queue.csv`
2. Integrate accepted rows into canonical `issues.csv` and/or `messages.csv` based on schema fit.
3. Publish extraction report with coverage stats by year.

## Suggested Implementation Tasks in This Repo
1. New script: `scripts/build_dfp_inventory_2018_2026.py`
2. New script: `scripts/fetch_dfp_pages_tos_compliant.py`
3. New script: `scripts/extract_dfp_toplines.py`
4. New script: `scripts/resolve_dfp_topline_support.py`
5. New QA script: `scripts/audit_dfp_toplines.py`

## Success Criteria
- >=95% of DFP polling/messaging pages in 2018–2026 identified.
- >=85% of extracted toplines have explicit wording-to-percentage linkage.
- 100% of requests logged and compliant with human-rate throttle policy.
- Re-runs are deterministic from cached HTML + versioned scripts.
