# Message Testing Schema — `data/processed/messages.csv`

## Fields (19 columns)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `message_id` | string | yes | Unique ID: `SRC_YYYYMMDD_###` |
| `source` | string | yes | Organization name (e.g., "Blueprint Research") |
| `source_url` | string | yes | Full article URL |
| `date` | date (ISO 8601) | yes | When fielded (YYYY-MM-DD) |
| `topic` | string | yes | Broad topic e.g. "economy", "healthcare", "democracy" |
| `issue_area` | string | no | Specific issue e.g. "inflation", "SS/Medicare", "abortion" |
| `message_type` | string | yes | "vision", "closing_argument", "rebuttal", "contrast", "positive", "negative", "values", "tested_message", "poll_question", "favorability" |
| `wording` | text | yes | Exact message wording as tested (verbatim) |
| `support_pct` | float | no | % who found convincing / agreed / supported |
| `oppose_pct` | float | no | % who found unconvincing / disagreed / opposed |
| `net_score` | float | no | support_pct - oppose_pct |
| `preference_effect` | float | no | MaxDiff or conjoint preference score (+/-) |
| `effect_scale` | string | no | "maxdiff", "percentage_point", "net", "qualitative", "net_concern" |
| `sample_size` | int | no | Number of respondents |
| `methodology` | string | no | e.g., "online_panel", "phone", "maxdiff", "conjoint" |
| `population` | string | no | "likely_voters", "registered_voters", "adults" |
| `moe` | float | no | Margin of error (percentage points) |
| `tags` | string | no | Semicolon-separated keywords |
| `notes` | text | no | Caveats, methodology details, context |

**Note:** The actual CSV contains only these 19 columns. Demographic breakdown fields (dem_*, dem_all) were part of the initial schema design but are not yet populated in the dataset — they exist as empty columns in the CSV header and should be populated from source data as available.

## Source Breakdown

| Source | Rows | Key Metrics |
|--------|------|-------------|
| Blueprint Research | 70 | preference_effect (MaxDiff), support_pct |
| Navigator Research | 53 | support_pct, oppose_pct |
| Data for Progress | 93 | wording fragments (richer data in staging) |

## Controlled Vocabularies

### `topic`
economy, healthcare, immigration, democracy, foreign_policy, climate, abortion, guns, crime, education, taxes, voting_rights, social_security, technology, trade, civil_rights, energy, housing, drugs, corruption, government, culture_war, politics

### `message_type`
vision, closing_argument, rebuttal, contrast, positive, negative, values, policy_proposal, attack, defense, character, urgency, fear, hope, aspirational, populist, unity, partisan, tested_message, poll_question, favorability, qualitative

## Example Entries

```csv
message_id,source,source_url,date,topic,issue_area,message_type,wording,support_pct,oppose_pct,net_score,preference_effect,effect_scale,sample_size,methodology,population,moe,tags,notes
BLP_20251205_001,Blueprint Research,https://blueprint-research.com/polling/dem-message-test-2-5/,2025-12-05,democracy,vision,vision,"Fights—really fights—for all of us",,,,14,maxdiff,2572,online_panel,likely_voters,2.2,maxdiff;vision;fight;all_of_us,MaxDiff of 10 Democratic vision statements
NAV_20260216_002,Navigator Research,https://navigatorresearch.org/special-battleground-report-on-food-and-health-part-ii-messages/,2026-02-16,economy,food_prices,negative,"Trump and Republicans allowed food companies to take advantage of inflation to raise prices.",68,,,1500,online_panel,likely_voters,2.5,price_gouging;food_prices,68% concerned
```

## Validation Rules
- `message_id` must be unique
- `date` must be valid ISO 8601 (YYYY-MM-DD) where present
- Percentages 0-100 (or null)
- `source_url` should be a valid URL
