#!/usr/bin/env python3
"""Check quality of DFP messages in dfp_new_messages.csv"""
import csv
from collections import Counter

with open('data/processed/dfp_new_messages.csv', newline='', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

print(f"Total rows: {len(rows)}")

long = [r for r in rows if len(r['wording'].strip()) >= 40]
medium = [r for r in rows if len(r['wording'].strip()) >= 25 and len(r['wording'].strip()) < 40]
short = [r for r in rows if len(r['wording'].strip()) < 25]

print(f"Long (>=40ch): {len(long)}")
print(f"Medium (25-39ch): {len(medium)}")
print(f"Short (<25ch): {len(short)}")

# Check for survey response patterns
fragment_patterns = [
    'corporation', 'price of', 'cost of', 'employee', 'somewhat', 'problem',
    'the top three', 'candidate?', 'issue?', 'influence', 'listed below',
    'supplier', 'amount of'
]
# Also check for punctuation-only fragments
import re
for r in rows:
    w = r['wording'].strip().lower()
    # Remove quotes
    w_clean = w.strip('"\'')

print("\n--- Short rows (<25ch) ---")
for r in short[:20]:
    print(f"  [{len(r['wording'])}ch] '{r['wording'][:60]}'")

print("\n--- Medium rows (25-39ch, first 20) ---")
for r in medium[:20]:
    print(f"  [{len(r['wording'])}ch] '{r['wording'][:80]}'")

print("\n--- Long rows (>=40ch, first 30) ---")
for r in long[:30]:
    print(f"  [{len(r['wording'])}ch] {r['wording'][:100]} | {r['source_url'][:70]}")