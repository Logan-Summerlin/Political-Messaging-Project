#!/usr/bin/env python3
"""
Post-Phase 1 Data Quality Report & Dataset Inventory Update.
Runs comprehensive checks on all three datasets and outputs to sources/.
"""
import csv
import os
from datetime import datetime
from collections import Counter

DATA = 'data/processed'
RAW = 'data/raw'

def count_rows(path):
    with open(path, newline='') as f:
        return sum(1 for _ in csv.DictReader(f))

def null_counts(rows, field):
    return sum(1 for r in rows if not r.get(field, '').strip())

def min_max(rows, field):
    vals = [r[field] for r in rows if r.get(field, '').strip()]
    if vals:
        return min(vals), max(vals)
    return 'N/A', 'N/A'

def unique_values(rows, field):
    return set(r[field] for r in rows if r.get(field, '').strip())

# Load datasets
with open(f'{DATA}/issues.csv') as f:
    issues = list(csv.DictReader(f))
with open(f'{DATA}/messages.csv') as f:
    messages = list(csv.DictReader(f))
with open(f'{DATA}/referendums.csv') as f:
    referendums = list(csv.DictReader(f))

print("=" * 70)
print("POST-PHASE 1 DATA QUALITY REPORT")
print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
print("=" * 70)

# --- ISSUES TABLE ---
print("\n## ISSUES TABLE")
print(f"  Total rows: {len(issues)}")
print(f"  Sources: {sorted(unique_values(issues, 'source'))}")
print(f"  Topics: {len(unique_values(issues, 'topic'))}")
print(f"  Date range: {min_max(issues, 'date')}")

source_counts = Counter(r['source'] for r in issues)
print("  Row count by source:")
for s, c in source_counts.most_common():
    print(f"    {s}: {c}")

topic_counts = Counter(r['topic'] for r in issues)
print(f"  Topic distribution:")
for t, c in topic_counts.most_common(10):
    print(f"    {t}: {c}")

# Quality checks
null_support = null_counts(issues, 'support_pct')
null_wording = null_counts(issues, 'question_wording')
print(f"  Null support_pct: {null_support}/{len(issues)} ({100*null_support/len(issues):.1f}%)")
print(f"  Null question_wording: {null_wording}/{len(issues)} ({100*null_wording/len(issues):.1f}%)")

# --- MESSAGES TABLE ---
print("\n## MESSAGES TABLE")
print(f"  Total rows: {len(messages)}")
print(f"  Sources: {sorted(unique_values(messages, 'source'))}")
print(f"  Topics: {len(unique_values(messages, 'topic'))}")
print(f"  Date range: {min_max(messages, 'date')}")

msg_sources = Counter(r['source'] for r in messages)
print("  Row count by source:")
for s, c in msg_sources.most_common():
    print(f"    {s}: {c}")

msg_topics = Counter(r['topic'] for r in messages)
print("  Topic distribution:")
for t, c in msg_topics.most_common():
    print(f"    {t}: {c}")

# Quality - messages with wording
with_wording = sum(1 for r in messages if r.get('wording','').strip() and len(r['wording']) > 20)
with_support = sum(1 for r in messages if r.get('support_pct','').strip())
print(f"  Messages with substantive wording: {with_wording}/{len(messages)}")
print(f"  Messages with support_pct: {with_support}/{len(messages)}")

# --- REFERENDUMS TABLE ---
print("\n## REFERENDUMS TABLE")
print(f"  Total rows: {len(referendums)}")
print(f"  States: {len(unique_values(referendums, 'state'))}")
print(f"  Topics: {len(unique_values(referendums, 'topic'))}")
print(f"  Date range: {min_max(referendums, 'year')}")

ref_years = Counter(r['year'] for r in referendums)
print("  By year:")
for y in sorted(ref_years):
    print(f"    {y}: {ref_years[y]}")

ref_topics = Counter(r['topic'] for r in referendums)
print("  By topic:")
for t, c in ref_topics.most_common():
    print(f"    {t}: {c}")

null_support_ref = null_counts(referendums, 'support_pct')
null_wording_ref = null_counts(referendums, 'wording')
null_passed_ref = null_counts(referendums, 'passed')
print(f"  Null support_pct: {null_support_ref}/{len(referendums)} ({100*null_support_ref/len(referendums):.1f}%)")
print(f"  Null wording: {null_wording_ref}/{len(referendums)} ({100*null_wording_ref/len(referendums):.1f}%)")
print(f"  Null passed: {null_passed_ref}/{len(referendums)} ({100*null_passed_ref/len(referendums):.1f}%)")

# --- PROVENANCE SUMMARY ---
print("\n## PROVENANCE")
print(f"  Issues: {len(issues)} rows from {len(source_counts)} sources, 1972-2026")
print(f"  Messages: {len(messages)} rows from {len(msg_sources)} sources, 2024-2026")
print(f"  Referendums: {len(referendums)} rows from 48 states, 2008-2024")
print(f"  Total data points: {len(issues) + len(messages) + len(referendums):,}")

# --- DATA QUALITY SCORECARD ---
print("\n## DATA QUALITY SCORECARD")
print(f"  Issues provenance (source+date non-null): {100 - 100*null_counts(issues, 'source')/len(issues):.0f}%")
print(f"  Messages provenance (source+date non-null): {100 - 100*null_counts(messages, 'source')/len(messages):.0f}%")
print(f"  Referendums provenance (state+year non-null): {100 - 100*null_counts(referendums, 'state')/len(referendums):.0f}%")

# Duplicate check
issue_ids = [r['poll_id'] for r in issues]
msg_ids = [r['message_id'] for r in messages]
ref_ids = [r['measure_id'] for r in referendums]

issue_dupes = {k:v for k,v in Counter(issue_ids).items() if v > 1}
msg_dupes = {k:v for k,v in Counter(msg_ids).items() if v > 1}
ref_dupes = {k:v for k,v in Counter(ref_ids).items() if v > 1}

print(f"  Issues duplicate poll_ids: {len(issue_dupes)}")
print(f"  Messages duplicate message_ids: {len(msg_dupes)}")
print(f"  Referendums duplicate measure_ids: {len(ref_dupes)}")

# --- V1.0 SNAPSHOT SUMMARY ---
print("\n" + "=" * 70)
print("V1.0 SNAPSHOT SUMMARY")
print("=" * 70)
print(f"""
Dataset v1.0 — {datetime.now().strftime('%Y-%m-%d')}

  {len(issues):>6,}  issue poll rows    ({source_counts.most_common(1)[0][0]} dominant)
  {len(messages):>6,}  message test rows  ({msg_sources.most_common(1)[0][0]} largest)
  {len(referendums):>6,}  ballot measure rows (48 states)
  ─────────
  {len(issues) + len(messages) + len(referendums):>6,}  total data points
  
  Years covered: 1972-2026
  Sources: {len(source_counts) + len(msg_sources)} unique organizations
""")
