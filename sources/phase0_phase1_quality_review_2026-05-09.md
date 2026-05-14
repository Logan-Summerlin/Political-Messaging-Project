# COMPREHENSIVE PHASE 0 & PHASE 1 QUALITY REVIEW
# Date: 2026-05-09T05:56:44.791712

## Executive Summary

The Phase 0 (Program Setup) and Phase 1 (Data Compilation) work established a solid foundation
but has significant data quality issues that must be addressed before model training.

### What's Usable

| Source | Grade | Count | Notes |
|--------|-------|-------|-------|
| Blueprint Research | B+ | 63 | Good MaxDiff scores; wordings sometimes truncated |
| Navigator Research | A- | 132 | Solid extraction; some lack oppose_pct |
| DFP real messages | D | ~12 | Only 4% of DFP rows are actual tested messages |
| Issues.csv | A | 5,477 | 8 sources, 45 topics, 1972-2026 coverage. Solid. |
| Referendums.csv | F | 315 | 78% null support_pct, 100% null wording |

### Critical Issues Found

1. **DFP messages are polluted with non-message content (96% noise)**
   - 173 fragments/survey response options
   - 133 narrative text passages from article bodies
   - Only ~12 actual tested messages with metrics
   - Root cause: The parser extracted ANY bullet point with a % from DFP articles
   - Only `**Tested Message Wording:**` sections contain real messages

2. **Blueprint wordings are sometimes summaries, not exact wording**
   - 41 of 71 are < 50 characters - too short for message generation training
   - 8 are descriptions ("Trump healthcare net approval") not actual wording
   - Source articles are behind Substack login (accessible via Wayback Machine)

3. **Referendums have critical data gaps**
   - No wording/summary for any measure (100% null)
   - 78% missing vote percentages
   - 38% missing passage status

### Recommendations

1. **Strip DFP noise from messages.csv** — keep only the ~12-50 real tested messages
2. **Restore DFP narrative/fragment rows to the issues.csv** where they belong as poll findings
3. **Expand Blueprint wordings** by re-extracting from Wayback Machine snapshots
4. **Fix referendums** by re-scraping Wikipedia with proper table parsing
5. **Add oppose_pct to Navigator** by re-extracting from source articles
