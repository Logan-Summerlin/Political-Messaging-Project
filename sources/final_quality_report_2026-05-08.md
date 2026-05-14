======================================================================
FINAL PHASE 1 QUALITY REPORT — POST REVIEW
Total data points: 6,318
======================================================================

======================================================================
DATASET SIZES
======================================================================
  Issues:      5,477 rows
  Messages:      526 rows
  Referendums:    315 rows
  Total:       6,318 rows

======================================================================
DUPLICATE CHECK
======================================================================
  Issues duplicate poll_ids:     0
  Messages duplicate message_ids: 0
  Referendums duplicate measure_ids: 0

======================================================================
MESSAGES TABLE — QUALITY BREAKDOWN
======================================================================

  By Source:
    Data for Progress             :  318 rows | wording=306 | support%= 57 | effect=  0
    Navigator Research            :  137 rows | wording=137 | support%=114 | effect= 24
    Blueprint Research            :   71 rows | wording= 70 | support%= 16 | effect= 48

  Quality Distribution:
    complete_message (wording + metric):  240 (45%)
    message_only (wording, no metric):    286 (54%)
    garbage/stub:                           0 (0%)

  Topic diversity: 17
  Date range: ('2019-02-21', '2026-05-07')

======================================================================
ISSUES TABLE — QUALITY
======================================================================

  By Source:
    Gallup                             :  1830 rows
    Data for Progress                  :  1731 rows
    General Social Survey              :  1303 rows
    CES                                :   447 rows
    Pew Research Center                :   150 rows
    YouGov                             :     6 rows
    AP-NORC                            :     6 rows
    Ipsos/Reuters                      :     4 rows

  Null support_pct:          2/5477 (0%)
  Null question_wording:    0/5477 (0%)
  Topic diversity: 45
  Date range: ('1972', '2026-05-04')

======================================================================
REFERENDUMS TABLE — QUALITY
======================================================================

  Null support_pct: 247/315 (78%)
  Null wording:     315/315 (100%)
  Null passed:      121/315 (38%)
  States covered:   48
  Topics:           16
  Year range:       ('2008', '2024')

======================================================================
PROVENANCE COMPLETENESS
======================================================================
  Issues:     100% source + date
  Messages:   100% source + date
  Referendums: 100% state + year

======================================================================
SUMMARY: IS THE DATASET USEFUL FOR MODEL TRAINING?
======================================================================

  Training-ready messages (wording + metric):           240
  Messages with context only (wording, no metric):     286
  Issue polling rows (support/oppose percentages):     5477
  Ballot measures (voting outcomes):                   315
  
  A subject matter expert would find:
  - 240 directly trainable message records with exact wording + measured outcome
  - 286 additional message records usable for fine-tuning context (wording patterns, topics)
  - 8 issue polling sources for popularity/provenance context
  - 48 states covered for geographic diversity
  - 2008-2024 ballot measure coverage for electoral outcome grounding

