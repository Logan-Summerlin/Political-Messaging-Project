# Gallup Most Important Problem — Data Freshness Check

**Date:** 2026-05-08
**Task:** Check Gallup MIP Datawrapper chart data vs. existing issues.csv

---

## Existing Dataset Status

| Metric | Value |
|--------|-------|
| File | `data/processed/issues.csv` |
| Total Gallup rows | 1,830 |
| Gallup max date | **2026-03-02** |
| Gallup min date | 2001-01-01 |

## Datawrapper Sources Checked

### 1. Main Gallup MIP Page (`/poll/1675/most-important-problem.aspx`)

| Chart ID | Description | Latest Date |
|----------|-------------|-------------|
| `54LJ4/1` → `/5` | % Mentioning (economy focus) | Oct 1, 2022 |
| `vEKjO/2` → `/4` | Issue category breakdown by month | Sep 2022 |
| `J195D/2` → `/4` | Party handling (historical) | 1945–2021 |

All stopped updating in late 2022. **Not current.**

### 2. Newer Article — "Government Still Leads as Nation's Top Problem" (`/poll/702719/`)

| Chart ID | Description | Latest Date |
|----------|-------------|-------------|
| `PxSaL/1` | Immigration mentions by party | Feb 2026 |
| `VQzZg/1` | Immigration mentions (alternate) | Feb 2026 |
| `qs4jb/1` | Top problems breakdown (Government, Immigration, Economy, Inflation) | Feb 2026 |
| `rK0nB/1` | Government mentions (long trend) | Feb 2026 |

These 4 CSV files were downloaded to `data/raw/gallup/`.

## Conclusion

**❌ No newer data found.** The freshest Datawrapper chart data (Feb 2026) is older than our existing issues.csv max date of **2026-03-02**. Our Gallup MIP data is already the most current available from public Gallup sources.

## Files Downloaded (for reference)

- `data/raw/gallup/gallup_mip_PxSaL_1.csv` — 121 rows, immigration by party, 2016–Feb 2026
- `data/raw/gallup/gallup_mip_VQzZg_1.csv` — 122 rows, immigration by party, Jan 2016–Feb 2026
- `data/raw/gallup/gallup_mip_qs4jb_1.csv` — 25 rows, top problems breakdown, Feb 2024–Feb 2026
- `data/raw/gallup/gallup_mip_rK0nB_1.csv` — 303 rows, government mentions, Mar 2000–Feb 2026
