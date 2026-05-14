#!/usr/bin/env python3
"""
Clean Navigator garbage rows from messages.csv.
Then attempt fresh extraction from problematic URLs.
"""
import csv, shutil, re

with open('data/processed/messages.csv') as f:
    msgs = list(csv.DictReader(f))

garbage_patterns = [
    r'vc_col', r'vc_row', r'vc_empty', r'css=',
    r'wpb_row', r'wpb_column',
    r'^Support % patterns found', r'^Oppose % patterns found',
    r'^\*\*URL:', r'^\*\*Slug:',
]

def is_garbage(r):
    wording = r.get('wording', '')
    for pat in garbage_patterns:
        if re.search(pat, wording, re.IGNORECASE):
            return True
    return False

garbage_ids = set()
nav_garbage_urls = set()
for i, r in enumerate(msgs):
    if r['source'] == 'Navigator Research' and is_garbage(r):
        garbage_ids.add(r['message_id'])
        nav_garbage_urls.add(r['source_url'])

print(f"Garbage rows to remove: {len(garbage_ids)}")

# Remove from main list
clean = [r for r in msgs if r['message_id'] not in garbage_ids]
print(f"After cleaning: {len(clean)} rows (was {len(msgs)})")

# Backup and write
shutil.copy2('data/processed/messages.csv', 'data/archive/messages_pre_clean.bak')
fieldnames = list(msgs[0].keys())
with open('data/processed/messages.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=fieldnames)
    w.writeheader()
    w.writerows(clean)
print(f"✓ Written. {len(clean)} messages")

# Save the list of URLs to re-extract
print(f"\nURLs to attempt fresh extraction from ({len(nav_garbage_urls)}):")
for url in sorted(nav_garbage_urls):
    # Check how many good rows already exist from this URL
    good_at_url = [r for r in clean if r['source_url'] == url and r['source'] == 'Navigator Research']
    print(f"  {url} ({len(good_at_url)} good rows already)")
