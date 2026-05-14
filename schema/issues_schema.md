# Issue Polling Schema — `data/processed/issues.csv`

## Fields (16 columns)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `poll_id` | string | yes | Unique ID: `SRC_YYYYMMDD_###` or `SRC_YYYY_topic` |
| `source` | string | yes | Organization that conducted/commissioned |
| `source_url` | string | yes | Link to full poll report |
| `date` | date | yes | Field dates (YYYY-MM-DD or YYYY) |
| `question_type` | string | yes | "most_important_problem", "approval", "priority", "concern", "favor", "agree", "spending" |
| `question_wording` | text | yes | Exact question text as asked |
| `topic` | string | yes | Broad topic (same vocab as messages) |
| `issue_area` | string | no | Specific issue |
| `support_pct` | float | yes | % in agreement / support |
| `oppose_pct` | float | no | % in disagreement / opposition |
| `net` | float | no | support_pct - oppose_pct |
| `sample_size` | int | no | Respondents |
| `methodology` | string | no | "online_panel", "phone", "mixed_mode", "in_person" |
| `population` | string | no | "adults", "registered_voters", "likely_voters" |
| `moe` | float | no | Margin of error (percentage points) |
| `tags` | string | no | Semicolon-separated keywords |
|| `data_quality` | string | yes | "structured_poll" (question wording + support%) or "narrative_finding" (blog post narrative findings, e.g., DFP) |
|| `notes` | text | no | Context, caveats |

## Source Breakdown (5,099 rows)

| Source | Rows | Date Range |
|--------|------|-----------|
| Gallup | 1,830 | 2001–2026 |
| General Social Survey | 1,303 | 1972–2024 |
| Data for Progress | 1,298 | 2024–2026 |
| Pew Research Center | 205 | 2011–2026 |
| CES | 447 | 2006–2021 |
| AP-NORC | 6 | 2025–2026 |
| YouGov | 6 | 2026 |
| Ipsos/Reuters | 4 | 2026 |

## Example

```csv
poll_id,source,source_url,date,question_type,question_wording,topic,issue_area,support_pct,oppose_pct,net,sample_size,methodology,population,moe,tags,notes
PEW_20260101_001,Pew Research Center,https://www.pewresearch.org/2026/02/23/state-of-the-union-2026/,2026-01,approval,"How would you rate national economic conditions? Excellent, good, only fair, or poor?",economy,economy_general,28,72,-44,10000,online_panel,adults,,economy;approval;state_of_union,
GSS_1973_natenvir,General Social Survey,https://gss.norc.org,1973,spending,Improving & protecting the environment,climate,environment,0.0,7.9,-7.9,1413,in_person,adults,,gss;climate;environment;natenvir,
```
