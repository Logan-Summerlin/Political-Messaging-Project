======================================================================
POST-PHASE 1 DATA QUALITY REPORT
Generated: 2026-05-08 16:04
======================================================================

## ISSUES TABLE
  Total rows: 5477
  Sources: ['AP-NORC', 'CES', 'Data for Progress', 'Gallup', 'General Social Survey', 'Ipsos/Reuters', 'Pew Research Center', 'YouGov']
  Topics: 45
  Date range: ('1972', '2026-05-04')
  Row count by source:
    Gallup: 1830
    Data for Progress: 1731
    General Social Survey: 1303
    CES: 447
    Pew Research Center: 150
    YouGov: 6
    AP-NORC: 6
    Ipsos/Reuters: 4
  Topic distribution:
    economy: 1175
    democracy: 800
    foreign_policy: 512
    government: 367
    climate: 344
    abortion: 329
    immigration: 251
    healthcare: 243
    crime: 137
    education: 111
  Null support_pct: 2/5477 (0.0%)
  Null question_wording: 0/5477 (0.0%)

## MESSAGES TABLE
  Total rows: 387
  Sources: ['Blueprint Research', 'Data for Progress', 'Navigator Research']
  Topics: 15
  Date range: ('2019-02-21', '2026-05-07')
  Row count by source:
    Data for Progress: 318
    Navigator Research: 60
    Blueprint Research: 9
  Topic distribution:
    democracy: 154
    economy: 59
    foreign_policy: 39
    climate: 38
    healthcare: 37
    immigration: 23
    general: 17
    housing: 7
    politics: 3
    technology: 3
    social_security: 2
    abortion: 2
    voting_rights: 1
    culture_war: 1
    guns: 1
  Messages with substantive wording: 375/387
  Messages with support_pct: 82/387

## REFERENDUMS TABLE
  Total rows: 315
  States: 48
  Topics: 16
  Date range: ('2008', '2024')
  By year:
    2008: 25
    2010: 9
    2012: 16
    2014: 11
    2016: 18
    2018: 18
    2020: 28
    2022: 112
    2024: 78
  By topic:
    government: 168
    voting_rights: 41
    taxes: 41
    abortion: 16
    crime: 8
    civil_rights: 7
    minimum_wage: 6
    education: 6
    healthcare: 5
    drugs: 5
    environment: 3
    labor: 3
    housing: 3
    transportation: 1
    immigration: 1
    gambling: 1
  Null support_pct: 247/315 (78.4%)
  Null wording: 315/315 (100.0%)
  Null passed: 121/315 (38.4%)

## PROVENANCE
  Issues: 5477 rows from 8 sources, 1972-2026
  Messages: 387 rows from 3 sources, 2024-2026
  Referendums: 315 rows from 48 states, 2008-2024
  Total data points: 6,179

## DATA QUALITY SCORECARD
  Issues provenance (source+date non-null): 100%
  Messages provenance (source+date non-null): 100%
  Referendums provenance (state+year non-null): 100%
  Issues duplicate poll_ids: 0
  Messages duplicate message_ids: 0
  Referendums duplicate measure_ids: 0

======================================================================
V1.0 SNAPSHOT SUMMARY
======================================================================

Dataset v1.0 — 2026-05-08

   5,477  issue poll rows    (Gallup dominant)
     387  message test rows  (Data for Progress largest)
     315  ballot measure rows (48 states)
  ─────────
   6,179  total data points
  
  Years covered: 1972-2026
  Sources: 11 unique organizations

