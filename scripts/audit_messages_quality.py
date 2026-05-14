#!/usr/bin/env python3
"""
Deep audit of messages.csv extraction quality.
Classifies each row by extraction quality and identifies issues.
"""
import csv
import re
from collections import Counter

with open('data/processed/messages.csv') as f:
    msgs = list(csv.DictReader(f))

print(f"Total messages: {len(msgs)}")
print()

# Source breakdown
sources = Counter(r['source'] for r in msgs)
print("=== Source Breakdown ===")
for s, c in sources.most_common():
    subset = [r for r in msgs if r['source'] == s]
    with_wording = sum(1 for r in subset if len(r.get('wording','').strip()) > 20)
    with_pct = sum(1 for r in subset if r.get('support_pct','').strip())
    with_effect = sum(1 for r in subset if r.get('preference_effect','').strip())
    print(f"\n{s} ({c} rows):")
    print(f"  Wording (>20 chars): {with_wording}/{c} ({100*with_wording//c}%)")
    print(f"  Support %: {with_pct}/{c} ({100*with_pct//c}%)")
    print(f"  Preference effect: {with_effect}/{c} ({100*with_effect//c}%)")

print("\n\n=== Quality Classification ===")

# Garbage wording patterns
garbage_patterns = [
    r'vc_col', r'vc_row', r'vc_empty', r'\[\/', r'\]\[\/', r'css=',
    r'wpb_row', r'wpb_column', r'\]\s*$', r'^\s*\]', r'^\*\*URL:',
    r'^\*\*Slug:', r'Support % patterns', r'Oppose % patterns',
    r'^\s*vc_'
]

def classify_quality(r):
    """Classify a message row's extraction quality."""
    wording = r.get('wording', '')
    src = r.get('source', '')
    
    if not wording.strip():
        return 'empty_wording'
    
    # Check for garbage/HTML remnants
    for pat in garbage_patterns:
        if re.search(pat, wording, re.IGNORECASE):
            return 'garbage_wording'
    
    # Check for stub/placeholder
    if len(wording) < 20:
        return 'stub_wording'
    
    # Check for phrases that aren't tested messages
    low_info = ['support % patterns found', 'oppose % patterns found', 'url:', 'slug:']
    for li in low_info:
        if li in wording.lower():
            return 'data_metadata_not_message'
    
    # Has both wording and at least one metric
    has_metric = bool(r.get('support_pct','').strip() or r.get('preference_effect','').strip())
    if has_metric:
        return 'complete_message'
    else:
        return 'message_only'

quality_counts = Counter()
by_source_quality = {}

for r in msgs:
    q = classify_quality(r)
    quality_counts[q] += 1
    src = r['source']
    if src not in by_source_quality:
        by_source_quality[src] = Counter()
    by_source_quality[src][q] += 1

print(f"Overall quality distribution:")
for q, c in quality_counts.most_common():
    print(f"  {q}: {c} ({100*c//len(msgs)}%)")

print(f"\nBy source:")
for src in sorted(by_source_quality):
    print(f"\n  {src}:")
    for q, c in by_source_quality[src].most_common():
        print(f"    {q}: {c}")

# Show examples of garbage
print("\n\n=== Garbage Wording Examples ===")
garbage = [r for r in msgs if classify_quality(r) == 'garbage_wording']
for i, r in enumerate(garbage[:10]):
    print(f"\n  [{r['source']}] {r['message_id']}:")
    print(f"    Wording: {r['wording'][:120]}")

# Show examples of complete messages
print("\n\n=== Complete Message Examples ===")
complete = [r for r in msgs if classify_quality(r) == 'complete_message']
for i, r in enumerate(complete[:10]):
    print(f"\n  [{r['source']}] {r['message_id']} ({r['date']}):")
    print(f"    Topic: {r['topic']} | Issue: {r.get('issue_area','')}")
    print(f"    Wording: {r['wording'][:120]}")
    print(f"    Support: {r.get('support_pct','N/A')} | Oppose: {r.get('oppose_pct','N/A')} | Effect: {r.get('preference_effect','N/A')}")

# Date range by source
print("\n\n=== Date Range by Source ===")
for s in sorted(sources):
    subset = [r for r in msgs if r['source'] == s]
    dates = [r['date'] for r in subset if r.get('date','').strip()]
    if dates:
        print(f"  {s}: {min(dates)} to {max(dates)}")
