# Dataset Inventory — Unified CSVs
**Last updated:** May 7, 2026

## Processed Datasets

### `data/processed/issues.csv`
- **5,030 rows**
- **Sources:** Gallup (1,830), Data for Progress (1,731), General Social Survey (1,303), Pew Research Center (150), AP-NORC (6), YouGov (6), Ipsos/Reuters (4)
- **Years:** 1972–2026
- **Topics:** economy, healthcare, climate/environment, abortion, guns, immigration, crime, government, drugs, education, welfare, race, religion, family, technology, culture, media, foreign_policy, infrastructure, urban, social_security
- **Format:** poll_id, source, source_url, date, question_type, question_wording, topic, issue_area, support_pct, oppose_pct, net, sample_size, methodology, population, moe, tags, notes

### `data/processed/messages.csv`
- **216 rows**
- **Sources:** Blueprint Research (70), Navigator Research (53), Data for Progress (93)
- **Years:** 2024–2026
- **Topics:** democracy, economy, social_security, foreign_policy, climate, immigration, healthcare, technology, abortion, guns, housing, voting_rights, culture_war
- **Format:** message_id, source, source_url, date, topic, issue_area, message_type, wording, support_pct, oppose_pct, net_score, preference_effect, effect_scale, sample_size, methodology, population, moe, tags, notes

### `data/processed/referendums.csv`
- **199 rows**
- **Sources:** Ballotpedia, Wikipedia
- **Years:** 2024–2025
- **States:** 9
- **Topics:** Abortion, crime, minimum wage, cannabis, education, voting, taxes, environment
- **Format:** measure_id, state, year, election_date, election_type, measure_name, wording, summary, topic, subtopic, passed, support_pct, oppose_pct, threshold, margin, votes_for, votes_against, total_votes, partisan_leans, campaign_contributions, tags, source_url, notes

## Raw Data Holdings

| Data | Size | Format | Source |
|------|------|--------|--------|
| DFP articles (4 chunks) | 921 KB | Markdown | 775 polling articles extracted |
| Navigator full archive | 126 KB | Markdown | 16 articles with full content |
| CA propositions | 86 KB | CSV | 600 proposition references |
| Wikipedia ballot measures | 56 KB | CSV | 592 measures (2008–2024) |
| GSS cumulative | 189 MB zipped | SPSS/Stata | 1972–2024 |
| CES cumulative | 747 MB | Stata/R | 2006–2024 |

## Staging Data (not yet merged)

| File | Rows | Source | Ready? |
|------|------|--------|--------|
| `dfp_new_issues.csv` | 1,732 | Data for Progress | Yes — all unique poll_ids |
| `dfp_new_messages.csv` | 95 | Data for Progress | Yes — richer wording than existing DFP rows |
| `gss_issues.csv` | 1,303 | General Social Survey | Already merged into issues.csv |

## Key Notes
- Blueprint and Navigator data have the cleanest A/B message wording with exact preference scores and support percentages
- Navigator extraction covers 22 articles (16 from archive + 6 from RSS); 53 clean rows with 51 having numeric support/oppose values
- GSS data covers 21 topic areas from 1972–2024, extracted from the Stata cumulative file
- Referendums is the smallest dataset — 592 Wikipedia + 600 CA raw records remain unprocessed
