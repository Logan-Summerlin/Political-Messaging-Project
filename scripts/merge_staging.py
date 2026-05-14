#!/usr/bin/env python3
"""
Merge staging data into main datasets.
- Fix duplicate message_ids in main dataset by deduplicating
- Merge dfp_new_messages.csv → messages.csv (94 new rows)
"""
import csv, sys, os
from collections import Counter

DATA_DIR = 'data/processed'
BACKUP_DIR = 'data/archive'

def load_csv(path):
    with open(path, newline='') as f:
        return list(csv.DictReader(f))

def write_csv(path, rows, fieldnames):
    with open(path, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)
    print(f"  Wrote {len(rows)} rows to {path}")

def backup_file(path):
    import shutil
    if os.path.exists(path):
        os.makedirs(BACKUP_DIR, exist_ok=True)
        bak = os.path.join(BACKUP_DIR, os.path.basename(path) + '.bak')
        shutil.copy2(path, bak)
        print(f"  Backed up to {bak}")

def deduplicate_ids(rows, id_field='message_id'):
    """Ensure all IDs are unique by appending _## suffix to duplicates."""
    ids = [r[id_field] for r in rows]
    counts = Counter(ids)
    dupe_ids = {k for k, v in counts.items() if v > 1}
    
    if not dupe_ids:
        return rows
    
    print(f"  Found {len(dupe_ids)} duplicate IDs to fix")
    counter = {}
    for r in rows:
        mid = r[id_field]
        if mid in dupe_ids:
            counter[mid] = counter.get(mid, 0) + 1
            r[id_field] = f"{mid}_{counter[mid]}"
    return rows

print("=" * 60)
print("STAGING DATA MERGE")
print("=" * 60)

# --- Messages merge ---
print("\n--- Messages ---")
main_msgs = load_csv(os.path.join(DATA_DIR, 'messages.csv'))
staging_msgs = load_csv(os.path.join(DATA_DIR, 'dfp_new_messages.csv'))

# Fix duplicate IDs in main file first
print("  Processing main file duplicates...")
main_msgs = deduplicate_ids(main_msgs)
main_ids = set(r['message_id'] for r in main_msgs)
staging_ids = set(r['message_id'] for r in staging_msgs)

print(f"  Main: {len(main_msgs)} rows, {len(main_ids)} unique IDs")
print(f"  Staging: {len(staging_msgs)} rows, {len(staging_ids)} unique IDs")

# Check overlap with staging
overlap = main_ids & staging_ids
print(f"  Overlap by message_id: {len(overlap)}")
if overlap:
    for mid in sorted(overlap):
        print(f"    Existing: {mid}")
        print(f"    In staging: {[r for r in staging_msgs if r['message_id'] == mid][0].get('source_url','')[:80]}")

new_rows = [r for r in staging_msgs if r['message_id'] not in main_ids]
print(f"  New rows to add: {len(new_rows)}")

if new_rows:
    backup_file(os.path.join(DATA_DIR, 'messages.csv'))
    
    all_msgs = main_msgs + new_rows
    all_msgs.sort(key=lambda r: (r.get('date','') or '0000'), reverse=True)
    
    # Final verification
    all_ids = [r['message_id'] for r in all_msgs]
    assert len(all_ids) == len(set(all_ids)), f"Duplicate message_ids after merge! {[k for k,v in Counter(all_ids).items() if v > 1]}"
    
    fieldnames = main_msgs[0].keys()
    write_csv(os.path.join(DATA_DIR, 'messages.csv'), all_msgs, fieldnames)
    print(f"  ✓ Merged. Total: {len(all_msgs)} messages")
else:
    print("  No new rows to merge.")

print("\nDone.")
