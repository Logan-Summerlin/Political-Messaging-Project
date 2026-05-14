# Data Versioning Rules — US Political Messaging Dataset

## Versioning Scheme

Dataset versions follow **semantic versioning** with a data-specific modifier:

```
v<MAJOR>.<MINOR>.<PATCH>
```

| Bump | When |
|------|------|
| **MAJOR** | Schema-breaking changes (column drops, renaming, type changes) |
| **MINOR** | Significant row additions (≥10% growth), new sources, new tables |
| **PATCH** | Bug fixes, small additions, documentation updates, merge of staging data |

## Snapshot Format

Each versioned snapshot includes:

```
data/archive/v<MAJOR>.<MINOR>.<PATCH>/
├── issues.csv
├── messages.csv
├── referendums.csv
├── MANIFEST.md          # Provenance: what changed, when, from what sources
├── validation_report.md # Quality checks results for this snapshot
└── schema_snapshot.md   # Frozen schema at time of snapshot
```

## Change Tracking

- All changes to processed CSVs go through the `scripts/` pipeline (not manual editing)
- Each pipeline script logs its date, source URLs, row counts, and dedup stats
- Staging files in `data/processed/` (e.g., `dfp_new_*.csv`) are intermediate; merging them produces a new snapshot

## Snapshot Cadence

- **Minor version** after every major ingestion batch (weekly during active extraction)
- **Patch version** as needed for data quality fixes
- **Major version** only when schema changes — requires documented migration path

## Current Version

**v1.0.0** — Initial unified dataset (planned)

| Table | Rows | Sources | Year Range |
|-------|------|---------|-----------|
| issues.csv | 5,030 + staging | Gallup, DFP, GSS, Pew, AP-NORC, YouGov, Ipsos | 1972–2026 |
| messages.csv | 255 + staging | Blueprint, Navigator, DFP | 2024–2026 |
| referendums.csv | 315 | Wikipedia, Ballotpedia | 2008–2025 |
