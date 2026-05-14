import csv, sys

# Check DFP new issues overlap with main issues
with open('data/processed/issues.csv') as f:
    main_issues = list(csv.DictReader(f))
main_ids = set(r['poll_id'] for r in main_issues)
main_urls = set(r['source_url'] for r in main_issues)

with open('data/processed/dfp_new_issues.csv') as f:
    staging_issues = list(csv.DictReader(f))
staging_ids = set(r['poll_id'] for r in staging_issues)
staging_urls = set(r['source_url'] for r in staging_issues)

overlap_ids = main_ids & staging_ids
overlap_urls = main_urls & staging_urls
print(f"Main issues: {len(main_issues)} rows, {len(main_ids)} unique IDs")
print(f"Staging issues: {len(staging_issues)} rows, {len(staging_ids)} unique IDs")
print(f"Overlap by poll_id: {len(overlap_ids)}")
print(f"Overlap by source_url: {len(overlap_urls)}")
print(f"New unique IDs to add: {len(staging_ids - main_ids)}")

# Check date range
main_dates = set(r['date'] for r in main_issues)
staging_dates = set(r['date'] for r in staging_issues)
main_min = min(main_dates) if main_dates else 'N/A'
main_max = max(main_dates) if main_dates else 'N/A'
staging_min = min(staging_dates) if staging_dates else 'N/A'
staging_max = max(staging_dates) if staging_dates else 'N/A'
print(f"\nMain date range: {main_min} to {main_max}")
print(f"Staging date range: {staging_min} to {staging_max}")
print()

# Check topic distribution in staging
from collections import Counter
staging_topics = Counter(r['topic'] for r in staging_issues)
print("Staging topics:")
for topic, count in staging_topics.most_common():
    print(f"  {topic}: {count}")

# Check DFP new messages overlap
print("\n--- MESSAGES ---")
with open('data/processed/messages.csv') as f:
    main_msgs = list(csv.DictReader(f))
main_msg_ids = set(r['message_id'] for r in main_msgs)
main_msg_urls = set(r['source_url'] for r in main_msgs)

with open('data/processed/dfp_new_messages.csv') as f:
    staging_msgs = list(csv.DictReader(f))
staging_msg_ids = set(r['message_id'] for r in staging_msgs)
staging_msg_urls = set(r['source_url'] for r in staging_msgs)

overlap_ids_msg = main_msg_ids & staging_msg_ids
overlap_urls_msg = main_msg_urls & staging_msg_urls
print(f"Main messages: {len(main_msgs)} rows, {len(main_msg_ids)} unique IDs")
print(f"Staging messages: {len(staging_msgs)} rows, {len(staging_msg_ids)} unique IDs")
print(f"Overlap by message_id: {len(overlap_ids_msg)}")
print(f"Overlap by source_url: {len(overlap_urls_msg)}")
print(f"New unique IDs to add: {len(staging_msg_ids - main_msg_ids)}")

staging_msg_topics = Counter(r['topic'] for r in staging_msgs)
print("Staging message topics:")
for topic, count in staging_msg_topics.most_common():
    print(f"  {topic}: {count}")
