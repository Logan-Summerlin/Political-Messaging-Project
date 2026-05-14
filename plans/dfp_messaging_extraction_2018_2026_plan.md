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

### Phase 2 — ToS-compliant Acquisition (COMPLETED DESIGN)

#### 2.1 Inputs, Outputs, and Idempotency
**Primary input:** `data/raw/dataforprogress/dfp_2018_2026_url_inventory.csv` with fields:
- `source_url`
- `publish_date`
- `content_class` (`poll_messaging`, `horserace_only`, `commentary`, `unknown`)
- `inventory_source` (`rss`, `sitemap`, `existing_index`, `manual_add`)
- `priority_score` (higher first)

**Acquisition scope filter:** fetch only rows where:
- `publish_date` in `[2018-01-01, 2026-12-31]`
- `content_class in ('poll_messaging','unknown')`

**Outputs:**
- HTML cache: `data/raw/dataforprogress/html/YYYY/MM/DD/<slug>.html`
- Response metadata sidecars: `.../<slug>.http.json`
- Optional assets: `data/raw/dataforprogress/assets/YYYY/MM/DD/<slug>/*`
- Request ledger: `data/raw/dataforprogress/request_log.csv`
- Fetch status table: `data/raw/dataforprogress/fetch_status.csv`

**Idempotency rules:**
- Never overwrite cached HTML unless `--refresh-stale` is passed.
- If URL already has status `ok_cached` and no refresh flag, skip network call.
- Use deterministic filename hashing for collision-safe slug paths.

#### 2.2 Request Policy (ToS Operational Controls)
1. **Human-rate throttle:** wait `uniform(10,20)` seconds before each request.
2. **Session pause:** every 25 requests, add pause `uniform(60,120)` seconds.
3. **Retry policy:** max 3 attempts on 429/5xx/timeouts.
   - Backoff schedule (seconds): `20`, `45`, `90` (+ jitter ±5s).
4. **Conditional requests:** send `If-None-Match` and `If-Modified-Since` when prior ETag/Last-Modified exists.
5. **User-Agent transparency:** explicit descriptive UA string including project + contact placeholder.
6. **Circuit breaker:** if 3 consecutive 429 responses, stop run and write `halt_reason=rate_limited`.

#### 2.3 Ledger + Auditability Schema
`request_log.csv` columns (append-only):
- `run_id` (UTC timestamp token)
- `request_ts_utc`
- `url`
- `method` (GET/HEAD)
- `attempt_no`
- `sleep_before_sec`
- `status_code`
- `bytes_received`
- `etag_sent`
- `etag_received`
- `last_modified_sent`
- `last_modified_received`
- `cache_outcome` (`hit_skip`,`304_not_modified`,`fetched_200`,`error`)
- `error_type` (`timeout`,`http_429`,`http_5xx`,`parse_error`,null)
- `elapsed_ms`

`fetch_status.csv` latest state per URL:
- `url`, `last_attempt_ts_utc`, `final_status`, `http_status`, `cache_path`, `http_meta_path`, `retry_count`, `next_action`, `notes`

#### 2.4 HTML and Metadata Capture Requirements
For each successful fetch:
- Persist raw HTML bytes exactly as returned.
- Persist normalized UTF-8 text copy only as derivative file (`.txt`)—never replace raw.
- Persist headers and request metadata JSON (`.http.json`):
  - request headers, response headers, redirect chain, final URL, content-type, encoding.

**Filename policy:**
- `slug = sanitize(url_path_last_segment)`
- If duplicate slug/day: suffix with 8-char SHA1 of URL.

#### 2.5 Optional Linked Asset Capture (Strictly Bounded)
Trigger only if on-page links match one of:
- anchor text contains `topline`, `crosstab`, `memo`, `pdf`, `methodology`
- href extension in `{.pdf,.csv,.xlsx}`

Asset fetch limits:
- max 2 assets/article unless `--allow-extra-assets`
- same throttling/ledger rules as HTML
- store checksum (`sha256`) and MIME in `asset_manifest.csv`

#### 2.6 Failure Handling + Resume
- Failures are non-fatal per URL; pipeline continues.
- Resume mode reads `fetch_status.csv` and processes only:
  - `final_status in ('pending','error_retryable')`
  - or stale entries older than configurable days.
- Terminal statuses:
  - `ok_cached`, `ok_fetched`, `ok_not_modified`, `skip_irrelevant`, `error_retryable`, `error_terminal`, `halt_rate_limit`

#### 2.7 CLI Contract for `scripts/fetch_dfp_pages_tos_compliant.py`
```bash
python scripts/fetch_dfp_pages_tos_compliant.py \
  --inventory data/raw/dataforprogress/dfp_2018_2026_url_inventory.csv \
  --out-root data/raw/dataforprogress \
  --min-delay 10 --max-delay 20 \
  --pause-every 25 --pause-min 60 --pause-max 120 \
  --retries 3 --timeout 30 \
  --resume
```

Required flags:
- `--dry-run` (validate scope and planned request counts)
- `--resume`
- `--refresh-stale <days>`
- `--max-urls <N>` for controlled batches

---

### Phase 3 — Structured Extraction Logic (COMPLETED DESIGN)

#### 3.1 Extraction Input and Record Granularity
**Input corpus:** cached HTML + optional assets from Phase 2.

**Granularity rule:** one output row = one interpretable metric tied to one question/message clause.
- If one sentence has support and oppose values, emit two rows.
- If a value is repeated across sections, keep highest-confidence row, preserve duplicates in audit table.

#### 3.2 Canonical Output Schema (`dfp_messaging_toplines_2018_2026.csv`)
Required fields:
- `row_id` (stable hash over `source_url|question_text_norm|metric_type|value_pct`)
- `source_url`
- `publish_date` (ISO date)
- `title`
- `question_or_message_text`
- `question_text_norm`
- `metric_type` (`support`,`oppose`,`favorability_pos`,`favorability_neg`,`concern`,`salience`,`agreement`,`other`)
- `value_pct` (float, 0–100)
- `value_text_raw` (e.g., “Fifty-eight percent”)
- `population`
- `sample_size_n`
- `field_dates`
- `mode`
- `moe_pct`
- `geography`
- `party_breakout` (nullable)
- `extraction_source` (`jsonld`,`meta_description`,`article_body`,`linked_pdf`)
- `evidence_snippet`
- `evidence_char_start`, `evidence_char_end`
- `confidence_score` (0.00–1.00)
- `needs_review` (bool)
- `review_reason`
- `parser_version`
- `extracted_at_utc`

#### 3.3 Multi-layer Parsing Strategy
1. **Layer A: JSON-LD/metadata parser**
   - Parse `application/ld+json` for `headline`, `datePublished`, description-like fields.
   - Parse OG/Twitter meta description for topline percentage claims.
   - Extract spelled-out percentages (“fifty-eight percent”) + numeric (`58%`).

2. **Layer B: Article-body parser**
   - DOM-clean content zone: remove nav/footer/script/style/captions where possible.
   - Sentence segmentation + clause splitting.
   - Percentage detector patterns:
     - `\b\d{1,3}(?:\.\d+)?\s?%\b`
     - `\b(one|two|...|ninety|hundred)\b ... percent` (word-number parser)
   - Metric cue lexicon window (±12 tokens):
     - support cues: `support`, `back`, `favor`
     - oppose cues: `oppose`, `against`, `reject`
     - concern cues: `concerned`, `worried`
   - Question/message candidate extraction:
     - quoted strings
     - “whether they support …” subordinate clauses
     - policy noun-phrase immediately following cue verbs.

3. **Layer C: Linked asset parser (fallback)**
   - PDF text extraction (page-wise) for topline tables and question wording.
   - Detect table-like rows: `question text | support | oppose | undecided`.
   - Map asset findings back to article via `source_url` and anchor context.

#### 3.4 Question–Percentage Binding Algorithm
For each detected percentage candidate:
1. Build candidate question spans from same sentence, prior sentence, and header/dek.
2. Score each candidate with weighted features:
   - same sentence proximity (+0.35)
   - cue alignment support/oppose match (+0.25)
   - quoted/prompt-like structure (+0.15)
   - appears in lead paragraph (+0.10)
   - repeated in methodology/topline section (+0.10)
   - parse cleanliness penalty (-0.15)
3. Select top candidate if score ≥0.60; otherwise `needs_review=true`.
4. Keep alternate bindings in audit output:
   - `candidate_question_2`, `candidate_score_2`, etc. (sidecar CSV)

#### 3.5 Confidence Scoring + Review Queue Rules
Base score from binding model, then adjustments:
- +0.10 if value appears as numeric `%` not only words
- +0.10 if sample/methodology metadata also parsed
- -0.20 if sentence contains >1 percentage and ambiguous cue mapping
- -0.15 if only metadata layer and no body corroboration

`needs_review=true` when any:
- `confidence_score < 0.70`
- `metric_type='other'`
- missing `question_or_message_text`
- parsed `value_pct` outside 0–100 before normalization

Review output: `dfp_messaging_toplines_2018_2026_review_queue.csv` with `review_reason` enum.

#### 3.6 Normalization Rules
- Convert spelled-out percentages to numeric float (e.g., “fifty-eight percent” → `58.0`).
- Strip hedge words (“about”, “roughly”) but preserve in snippet.
- Standardize text whitespace + unicode punctuation.
- Normalize question text for dedup:
  - lowercase, trim punctuation, collapse spaces, remove leading framing phrases.

#### 3.7 Determinism + Versioning
- Parser must be deterministic given same cached files and `parser_version`.
- Include explicit `parser_version` constant in script.
- Any regex/lexicon changes require version bump and changelog note.

#### 3.8 CLI Contract for `scripts/extract_dfp_toplines.py`
```bash
python scripts/extract_dfp_toplines.py \
  --html-root data/raw/dataforprogress/html \
  --asset-root data/raw/dataforprogress/assets \
  --out data/processed/dfp_messaging_toplines_2018_2026.csv \
  --review-out data/processed/dfp_messaging_toplines_2018_2026_review_queue.csv \
  --parser-version 2.0.0
```

Flags:
- `--use-assets` (enable Layer C)
- `--min-confidence <float>`
- `--max-articles <N>` (debug subset)
- `--write-audit-sidecar`

#### 3.9 QA Checks for Phase 3 Completion
- Coverage: `% of fetched poll/messaging articles yielding >=1 metric row`.
- Linkage: `% rows with non-empty question text and confidence >=0.70`.
- Validity: `% rows with `0<=value_pct<=100` and valid ISO dates`.
- Duplication: duplicate rate by (`source_url`,`question_text_norm`,`metric_type`,`value_pct`).
- Sampling completeness: `% rows with sample_size/mode/field_dates available`.

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
