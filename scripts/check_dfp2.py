#!/usr/bin/env python3
"""Analyze DFP messages quality"""
import csv
from collections import Counter

with open("data/processed/dfp_new_messages.csv", newline='', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

# Check support_pct presence
with_pct = [r for r in rows if r.get("support_pct", "").strip()]
print(f"DFP messages with support_pct: {len(with_pct)}")
for r in with_pct[:15]:
    print(f"  {r['message_id']}: {r['support_pct']}% | {r['wording'][:90]}")

print("\nUnique source URLs:")
urls = Counter(r["source_url"] for r in rows if r["source_url"])
for url, c in urls.most_common(10):
    art = url.split("/blog/")[-1] if "/blog/" in url else url
    print(f"  [{c:2d}] {art[:70]}")

# Check which have actual tested wording vs fragments
# Look at wording lengths
print(f"\nWording length distribution:")
lens = Counter(len(r['wording']) for r in rows)
for l in sorted(lens.keys()):
    print(f"  {l}: {lens[l]} rows")