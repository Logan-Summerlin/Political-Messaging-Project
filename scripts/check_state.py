#!/usr/bin/env python3
"""Check current state and plan next steps"""
import csv
from collections import Counter

with open("data/processed/messages.csv", newline='', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

sources = Counter(r['source'] for r in rows)
print(f"Current total: {len(rows)}")
for s,c in sources.most_common():
    has_m = sum(1 for r in rows if r['source']==s and (r.get('support_pct','').strip() or r.get('preference_effect','').strip() or r.get('net_score','').strip()))
    print(f"  {s}: {c} rows, {has_m} with metrics")

# Navigator article URLs
nav = [r for r in rows if r['source'] == 'Navigator Research']
nav_urls = Counter(r['source_url'] for r in nav)
print(f"\nNavigator unique articles: {len(nav_urls)}")
for url, c in sorted(nav_urls.items(), key=lambda x: -x[1]):
    slug = url.rstrip('/').split('/')[-1] if url != 'https://navigatorresearch.org/' else '(generic)'
    print(f"  [{c:2d}] {slug}")

# Blueprint article URLs  
blp = [r for r in rows if r['source'] == 'Blueprint Research']
blp_urls = Counter(r['source_url'] for r in blp)
print(f"\nBlueprint unique articles: {len(blp_urls)}")
for url, c in sorted(blp_urls.items(), key=lambda x: -x[1]):
    slug = url.rstrip('/').split('/')[-1] if url != 'https://blueprint-research.com/' else '(generic)'
    print(f"  [{c:2d}] {slug}")

# What's the gap to 500?
print(f"\nGap to 500: {500 - len(rows)}")
