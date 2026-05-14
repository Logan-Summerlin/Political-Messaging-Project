# Risk Register — Political Messaging Dataset Project

## Risk Scoring
| Score | Likelihood | Impact |
|-------|-----------|--------|
| 1 | Rare | Negligible |
| 2 | Unlikely | Minor |
| 3 | Possible | Moderate |
| 4 | Likely | Major |
| 5 | Almost Certain | Critical |

---

## Ethical & Legal Risks

| ID | Risk | Likelihood | Impact | Score | Mitigation | Status |
|----|------|-----------|--------|-------|-----------|--------|
| R1 | **Political persuasion misuse** — System could be used to generate deceptive or manipulative political messages | 3 | 5 | 15 | Human-in-the-loop requirement for any external output; safety filters; governance gating | Active |
| R2 | **Data rights violation** — Using poll data without proper attribution or beyond usage terms | 2 | 4 | 8 | All sources verified as freely accessible public data; provenance tracking for every row | Active |
| R3 | **Protected-class sensitivity** — Model outputs could disparage or stereotype demographic groups | 3 | 4 | 12 | Fairness instrumentation from day one; subgroup evaluation in swarm; bias checks | Active |
| R4 | **Deepfake/fake political ads** — System architecture could be repurposed for disinformation | 2 | 5 | 10 | Restricted access; no image/video generation; text-only output; abuse monitoring | Active |

## Technical Risks

| ID | Risk | Likelihood | Impact | Score | Mitigation | Status |
|----|------|-----------|--------|-------|-----------|--------|
| R5 | **Data leakage** — Temporal leakage where future data informs past predictions | 3 | 4 | 12 | Strict temporal train/eval splits; provenance-aware boundaries | Active |
| R6 | **Synthetic evaluator bias** — LLM persona judgments diverge from real voter behavior | 3 | 4 | 12 | Continuous calibration to real message-test and polling data | Active |
| R7 | **Opinion drift** — Rapid political opinion shifts invalidate model | 3 | 3 | 9 | Rolling retraining with recency weighting; drift alerts | Active |
| R8 | **Overfitting to historical campaigns** — Model memorizes winning messages instead of generalizing | 2 | 3 | 6 | Regularization; held-out test sets; diverse training data | Active |
| R9 | **Source availability changes** — Websites add paywalls, Cloudflare, or shut down | 3 | 3 | 9 | Multiple backup sources for each topic; local HTML snapshots; documented extraction dates | Active |
| R10 | **Extraction pipeline brittleness** — HTML structure changes break parsers | 4 | 2 | 8 | Modular parsers with validation; RSS feeds as primary discovery; snapshot raw HTML | Active |
| R11 | **Encoding/data corruption** — Stata/SPSS files have non-UTF-8 encoding issues | 3 | 2 | 6 | encoding='latin1' workaround for GSS; validation checks after extraction | Mitigated |
| R12 | **Staging data merge conflicts** — Duplicate records between staging files and main datasets | 3 | 2 | 6 | Dedup-by-poll_id before merge; auto-detect collision boundaries | Active |

## Operational Risks

| ID | Risk | Likelihood | Impact | Score | Mitigation | Status |
|----|------|-----------|--------|-------|-----------|--------|
| R13 | **Browser sandbox limitations** — No sudo/user namespaces blocks browser-based extraction | 4 | 3 | 12 | Prefer curl-based extraction; use Datawrapper CSV bypass for Gallup; document workarounds | Active |
| R14 | **API rate limiting** — Google News RSS, DuckDuckGo limits slow research | 3 | 2 | 6 | Staggered requests; cache results; prefer RSS feeds over web search | Active |
| R15 | **Storage limits** — Large datasets (CES 675MB, GSS 598MB) consume disk | 2 | 2 | 4 | Only store processed extracts; archive raw files to compressed format | Active |
| R16 | **Single point of failure** — Project depends on one operator | 3 | 3 | 9 | Document all processes in scripts; maintain README instructions; version everything | Active |

## Risk Response Plan

### Escalation Criteria
- **Critical (15-25):** Immediate review required; stop work if mitigation unavailable
- **High (10-14):** Active mitigation required before proceeding to affected phase
- **Medium (5-9):** Monitor and mitigate during normal work
- **Low (1-4):** Accept and document

### Review Cycle
- Full risk register review at each phase gate
- New risks added as discovered during extraction
- Mitigation effectiveness reviewed quarterly
