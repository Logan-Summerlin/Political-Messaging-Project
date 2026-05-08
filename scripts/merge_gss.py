#!/usr/bin/env python3
"""Merge GSS extracted data into main issues.csv."""
import csv
from pathlib import Path

PROC = Path("/home/agentbot/workspace/us-political-messaging-dataset/data/processed")

def load_csv(path, key_fn=None):
    rows = []
    if path.exists():
        with open(path, encoding='utf-8') as f:
            for row in csv.DictReader(f):
                rows.append(row)
    if key_fn:
        return {key_fn(r): r for r in rows}
    return rows

def write_csv(path, rows, fieldnames):
    with open(path, 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)

issue_fields = [
    'poll_id', 'source', 'source_url', 'date', 'question_type',
    'question_wording', 'topic', 'issue_area', 'support_pct', 'oppose_pct',
    'net', 'sample_size', 'methodology', 'population', 'moe', 'tags', 'notes'
]

# Load existing issues
existing = load_csv(PROC / 'issues.csv')
existing_ids = {r['poll_id'] for r in existing}
print(f"Existing issues: {len(existing)} rows")

# Load GSS data
gss = load_csv(PROC / 'gss_issues.csv')
print(f"GSS data: {len(gss)} rows")

# Filter out duplicates
added = 0
skipped = 0
for r in gss:
    pid = r.get('poll_id', '')
    if pid not in existing_ids:
        for col in issue_fields:
            if col not in r:
                r[col] = r.get(col, '')
        existing.append(r)
        existing_ids.add(pid)
        added += 1
    else:
        skipped += 1

write_csv(PROC / 'issues.csv', existing, issue_fields)
print(f"Added: {added}")
print(f"Skipped (duplicate): {skipped}")
print(f"Total issues.csv: {len(existing)} rows")
