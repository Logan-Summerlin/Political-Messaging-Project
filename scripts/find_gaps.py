#!/usr/bin/env python3
"""Find untapped Navigator articles from archive and RSS."""
import csv, re
from pathlib import Path

BASE = Path(__file__).parent.parent
PROC = BASE / "data" / "processed"
ARCHIVE = BASE / "data" / "raw" / "navigator" / "navigator_full_archive.md"

# Get URLs already in messages.csv
with open(PROC / 'messages.csv', newline='', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

nav_urls = set(r['source_url'] for r in rows if r['source'] == 'Navigator Research')
print(f"Existing NAV URLs in CSV: {len(nav_urls)}")
for u in sorted(nav_urls):
    slug = u.rstrip('/').split('/')[-1] if '/navigatorresearch.org/' not in u else u.split('/')[-1]
    print(f"  {slug}")

print("\n\nArticles in archive file:")
text = ARCHIVE.read_text(encoding='utf-8')
for m in re.finditer(r'\*\*URL:\*\*\s*(https?://[^\s]+)', text):
    url = m.group(1).rstrip('.')
    slug = url.rstrip('/').split('/')[-1]
    in_csv = "✅" if url in nav_urls else "❌ NOT IN CSV"
    print(f"  {in_csv} | {slug}")
