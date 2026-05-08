# US Political Messaging Dataset — Project Context for Hermes

## Project
`/home/agentbot/workspace/us-political-messaging-dataset/`
Owner: Logan (Telegram)
Goal: Structured, queryable dataset of US political issue polling, message A/B tests, and ballot measure results (2010+).

## Key Files
- `README.md` — Full project overview
- `schema/messages_schema.md` — Message testing data schema
- `schema/issues_schema.md` — Issue polling data schema
- `schema/referendums_schema.md` — Ballot measure data schema
- `sources/` — All extracted source data documents
- `data/raw/` — Original source files
- `data/processed/` — Cleaned CSV datasets (to be built)
- `plans/phase1_backfill.md` — Plan for backfilling 2010-2023

## Core Research Findings (May 2026)
- Blueprint Research: 26 articles with exact message wording + preference effects (MaxDiff)
- Navigator Research: 10 articles with pre/post message tests
- Pew, AP-NORC, Ipsos issue polling with exact %s
- Gallup, YouGov: JS-rendered content (needs browser extraction via agent-browser)
- 60+ ballot measures (2024-25) with exact language and vote shares
- 10 academic framing papers identified

## Schema Summary
Messages table: message_id, source, date, topic, issue_area, wording, support_pct, oppose_pct, net_score, preference_effect, sample_size, methodology, demographics...
Issues table: poll_id, source, date, question_wording, topic, support_pct, oppose_pct, sample...
Referendums table: measure_id, state, year, wording, topic, passed, support_pct, threshold...

## Known Sources Not Yet Extracted
- Gallup: JS-rendered (use agent-browser with AGENT_BROWSER_ARGS=--no-sandbox)
- YouGov: Angular SPA (use agent-browser)
- Roper Center iPoll: Subscription-only
- Pew toplines: PDF format (use pymupdf)
- Ballotpedia: Blocked direct scraping (use Wikipedia API instead)

## Web Research Notes
- Google News RSS: no rate limits, supports site: operator, 100 results/query
- DDG HTML search: ~3 queries/min rate limit
- Wikipedia API: use action=query&prop=extracts for content
- agent-browser: at /usr/local/bin/agent-browser, needs --no-sandbox
