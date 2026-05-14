# Ballot Measure Schema — `data/processed/referendums.csv`

## Fields (22 columns)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `measure_id` | string | yes | Unique ID: `STATE_YYYY_###` |
| `state` | string | yes | Two-letter state abbreviation |
| `year` | int | yes | Election year |
| `election_date` | date | no | Specific election date |
| `election_type` | string | yes | "general", "primary", "special" |
| `measure_name` | string | yes | Official ballot measure name/number |
| `wording` | text | yes | Exact ballot language |
| `summary` | text | no | Short description of what the measure does |
| `topic` | string | yes | Issue category (same vocab as messages) |
| `subtopic` | string | no | More specific category |
| `passed` | boolean | yes | true = passed, false = failed |
| `support_pct` | float | yes | % yes votes |
| `oppose_pct` | float | yes | % no votes |
| `threshold` | float | yes | % required to pass (50.0, 60.0, 55.0, etc.) |
| `margin` | float | no | support_pct - threshold (positive = passed) |
| `votes_for` | int | no | Yes vote count |
| `votes_against` | int | no | No vote count |
| `total_votes` | int | no | Total votes cast on measure |
| `partisan_leans` | text | no | Partisan support breakdown if available |
| `campaign_contributions` | text | no | If available: yes/oppose campaign spending |
| `tags` | string | no | Semicolon-separated keywords |
| `source_url` | string | no | Ballotpedia or Wikipedia link |
| `notes` | text | no | Context, notable dynamics |

## Current Status: 337 rows, 48 states + DC, 2008–2024

2020 vote data fully backfilled (45 rows, 0% missing).
2018 partially backfilled (23 rows, 11 still missing — states without wikitable tables on Wikipedia).
2008–2016: No vote percentages available on Wikipedia (no wikitable tables in those years).
2022: Has pass/fail outcomes but no vote percentage data on Wikipedia.
2024: 2 rows without vote data (procedural measures not voted on).

## Example

```csv
measure_id,state,year,election_date,election_type,measure_name,wording,summary,topic,subtopic,passed,support_pct,oppose_pct,threshold,margin,tags,source_url
AZ_2024_139,AZ,2024,,general,Prop 139,Protect and enshrine the right to abortion until fetal viability,,abortion,abortion_rights,TRUE,61.61,38.39,50.0,11.61,abortion_rights;passed;2024,
FL_2024_004,FL,2024,,general,Amendment 4,Limit government interference with abortion,,abortion,abortion_rights,FALSE,57.00,43.00,60.0,-3.0,abortion_rights;failed;60percent;2024,Failed at 57% - needed 60% supermajority
```
