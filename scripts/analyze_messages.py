#!/usr/bin/env python3
"""Analyze current messages.csv quality"""
import csv
from collections import Counter

with open("data/processed/messages.csv", newline='', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

# Check which rows have metrics
has_metric = 0
has_support = 0
has_preference = 0
has_net = 0
no_metric = []

for r in rows:
    has = False
    if r.get('support_pct','').strip():
        has_support += 1
        has = True
    if r.get('preference_effect','').strip():
        has_preference += 1
        has = True
    if r.get('net_score','').strip():
        has_net += 1
        has = True
    if has:
        has_metric += 1
    else:
        no_metric.append(r['message_id'])

print(f"Total: {len(rows)}")
print(f"With metric: {has_metric}")
print(f"  With support_pct: {has_support}")
print(f"  With preference_effect: {has_preference}")
print(f"  With net_score: {has_net}")
if no_metric:
    print(f"\nNo metric ({len(no_metric)}):")
    for mid in no_metric:
        print(f"  {mid}")

# Source breakdown
sources = Counter(r['source'] for r in rows)
print(f"\nSource breakdown:")
for s,c in sources.most_common():
    has_m = sum(1 for r in rows if r['source']==s and (r.get('support_pct','').strip() or r.get('preference_effect','').strip() or r.get('net_score','').strip()))
    print(f"  {s}: {c} total, {has_m} with metrics")

# Topic coverage
topics = Counter(r['topic'] for r in rows)
print(f"\nTopic breakdown:")
for t,c in topics.most_common():
    print(f"  {t}: {c}")

# Wording quality
short_wording = [r for r in rows if len(r['wording'].strip()) < 30]
print(f"\nShort wordings (<30ch): {len(short_wording)}")
for r in short_wording[:10]:
    print(f"  {r['message_id']}: '{r['wording']}' ({len(r['wording'])}ch)")

# Check Blueprint-specific
blp = [r for r in rows if r['source'] == 'Blueprint Research']
blp_topics = Counter(r['topic'] for r in blp)
print(f"\nBlueprint ({len(blp)} rows) topic breakdown:")
for t,c in blp_topics.most_common():
    print(f"  {t}: {c}")

# Check Blueprint articles used
blp_urls = Counter(r['source_url'] for r in blp)
print(f"\nBlueprint unique URLs: {len(blp_urls)}")
for url, c in blp_urls.most_common():
    slug = url.split('/polling/')[-1] if '/polling/' in url else url
    print(f"  [{c:2d}] {slug}")
