#!/usr/bin/env python3
"""Merge dfp_new_extracted_messages.csv into messages.csv."""
import csv
import shutil

DATA = 'data/processed'
ARCHIVE = 'data/archive'

with open(DATA + '/messages.csv', newline='') as f:
    main = list(csv.DictReader(f))

with open(DATA + '/dfp_new_extracted_messages.csv', newline='') as f:
    extracted = list(csv.DictReader(f))

# Strip None keys if present
extracted = [{k: v for k, v in r.items() if k is not None} for r in extracted]

print('Main:', len(main), 'rows')
print('Extracted:', len(extracted), 'rows')

main_ids = {r['message_id'] for r in main}
new_rows = [r for r in extracted if r['message_id'] not in main_ids]
print('New unique IDs to add:', len(new_rows))

if len(new_rows) < len(extracted):
    dupes = [r['message_id'] for r in extracted if r['message_id'] in main_ids]
    print('  (skipping', len(extracted) - len(new_rows), 'conflicts:', dupes)

if not new_rows:
    print('No new rows to add.')
    exit(0)

shutil.copy2(DATA + '/messages.csv', ARCHIVE + '/messages_pre_extracted.bak')

all_msgs = main + new_rows

def sort_key(r):
    d = r.get('date', '') or '0000'
    return d

all_msgs.sort(key=sort_key, reverse=True)

seen = set()
for r in all_msgs:
    mid = r['message_id']
    if mid in seen:
        raise ValueError('Duplicate: ' + mid)
    seen.add(mid)

fieldnames = list(main[0].keys())
with open(DATA + '/messages.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=fieldnames)
    w.writeheader()
    w.writerows(all_msgs)

print('Done. Total:', len(all_msgs), 'messages')
