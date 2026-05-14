import csv

with open('data/processed/ces_reshaped.csv') as f:
    rows = list(csv.DictReader(f))

print(f'CES reshaped: {len(rows)} rows')
topics = set(r.get('topic','') for r in rows)
print(f'Topics: {sorted(topics)}')
years = set(r.get('date','') for r in rows)
print(f'Years: {sorted(years)}')
sources = set(r.get('source','') for r in rows)
print(f'Sources: {sources}')
print()

with open('data/processed/issues.csv') as f:
    main = list(csv.DictReader(f))

main_ids = set(r['poll_id'] for r in main)
ces_ids = set(r['poll_id'] for r in rows)
overlap = main_ids.intersection(ces_ids)
print(f'Overlap by poll_id: {len(overlap)}')
if overlap:
    ol = list(overlap)
    print(f'  Examples: {ol[:5]}')
print(f'New CES rows to add: {len(ces_ids - main_ids)}')

# Show a few CES rows
for r in rows[:5]:
    print(f'  {r["poll_id"]}: {r["date"]} | {r["topic"]} | support={r["support_pct"]} | oppose={r["oppose_pct"]} | wording={r["question_wording"][:60]}')
