#!/usr/bin/env python3
"""Identify Navigator garbage rows and their source URLs."""
import csv
import re

with open('data/processed/messages.csv') as f:
    msgs = list(csv.DictReader(f))

garbage_patterns = [
    r'vc_col', r'vc_row', r'vc_empty', r'css=',
    r'wpb_row', r'wpb_column', 
    r'Support % patterns found', r'Oppose % patterns found',
    r'^\*\*URL:', r'^\*\*Slug:',
]

def is_garbage(r):
    wording = r.get('wording','')
    for pat in garbage_patterns:
        if re.search(pat, wording, re.IGNORECASE):
            return True
    return False

garbage = [r for r in msgs if r['source'] == 'Navigator Research' and is_garbage(r)]
print(f"Navigator garbage rows: {len(garbage)}")
print()

# Group by source_url
from collections import Counter
urls = Counter(r['source_url'] for r in garbage)
print("By source URL:")
for url, count in urls.most_common():
    print(f"\n  {url} ({count} rows):")
    rows = [r for r in garbage if r['source_url'] == url]
    for r in rows:
        print(f"    [{r['message_id']}] {r['wording'][:100]}")

# Also check which source URLs have garbage AND good rows
print("\n\nSource URLs with both good and garbage rows:")
nav_urls = set(r['source_url'] for r in msgs if r['source'] == 'Navigator Research')
for url in sorted(nav_urls):
    rows_at_url = [r for r in msgs if r['source'] == 'Navigator Research' and r['source_url'] == url]
    garbage_count = sum(1 for r in rows_at_url if is_garbage(r))
    good_count = len(rows_at_url) - garbage_count
    if garbage_count > 0 and good_count > 0:
        print(f"  {url}: {garbage_count} garbage, {good_count} good")
