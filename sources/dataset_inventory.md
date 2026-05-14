# Dataset Inventory — Unified CSVs
**Last updated:** May 7, 2026

## Processed Datasets

### `data/processed/issues.csv`
- **5,477 rows**
- **Sources:** Gallup (1,830), Data for Progress (1,731), General Social Survey (1,303), CES (447), Pew Research Center (150), AP-NORC (6), YouGov (6), Ipsos/Reuters (4)
- **Years:** 1972–2026
- **Topics:** economy, democracy, foreign_policy, government, climate, abortion, immigration, healthcare, crime, education, environment, guns, race, welfare, social_security, technology, religion, family, culture, media, infrastructure, urban, drugs, lgbt_rights, energy, values, politics, gun_policy, presidential_approval, approval, general_outlook, general_politics, society, government_role, race_equality, priorities, affirmative_action, gay_marriage, trade
- **Format:** poll_id, source, source_url, date, question_type, question_wording, topic, issue_area, support_pct, oppose_pct, net, sample_size, methodology, population, moe, tags, notes

### `data/processed/messages.csv`
- **387 rows**
- **Sources:** Data for Progress (318), Navigator Research (60), Blueprint Research (9)
- **Years:** 2019–2026
- **Topics:** democracy, economy, foreign_policy, climate, healthcare, immigration, general, housing, politics, technology, social_security, abortion, voting_rights, culture_war, guns
- **Format:** message_id, source, source_url, date, topic, issue_area, message_type, wording, support_pct, oppose_pct, net_score, preference_effect, effect_scale, sample_size, methodology, population, moe, tags, notes

### `data/processed/referendums.csv`
- **315 rows**
- **Sources:** Wikipedia
- **Years:** 2008–2024
- **States:** 48
- **Topics:** government, voting_rights, taxes, abortion, crime, civil_rights, minimum_wage, education, healthcare, drugs, environment, labor, housing, transportation, immigration, gambling
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
- Navigator extraction covers 22+ articles; 60 clean rows with numeric support/oppose values
- GSS data covers 21 topic areas from 1972–2024, extracted from the Stata cumulative file
- CES data covers 11 topic areas from 2006–2021, extracted and reshaped into issues.csv format (447 rows)
- DFP message extraction expanded beyond chunk2 to include chunk1 "Message Wording Tested" sections (20 new messages extracted)
- Referendums cover 48 states from 2008–2024, scraped from Wikipedia
- Navigator PDF toplines contain additional message testing data in image-based format (not text-extractable)
