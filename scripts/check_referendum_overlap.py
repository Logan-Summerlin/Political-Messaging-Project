import csv

main_ids = set(r['measure_id'] for r in csv.DictReader(open('data/processed/referendums.csv')))
wiki_ids = set(r['measure_id'] for r in csv.DictReader(open('data/processed/referendums_new_wiki.csv')))
print(f'Main IDs == Wiki IDs: {main_ids == wiki_ids}')
print(f'Main - Wiki: {main_ids - wiki_ids}')
print(f'Wiki - Main: {wiki_ids - main_ids}')
print()

main_rows = {r['measure_id']: r for r in csv.DictReader(open('data/processed/referendums.csv'))}
wiki_rows = {r['measure_id']: r for r in csv.DictReader(open('data/processed/referendums_new_wiki.csv'))}

diffs = 0
common_ids = main_ids & wiki_ids
for mid in sorted(common_ids)[:5]:
    print(f"--- {mid} ---")
    m = main_rows[mid]
    w = wiki_rows[mid]
    for key in m:
        if m[key] != w[key]:
            print(f"  {key}: main='{m[key]}' vs wiki='{w[key]}'")

null_main = sum(1 for r in main_rows.values() if not r.get('support_pct',''))
null_wiki = sum(1 for r in wiki_rows.values() if not r.get('support_pct',''))
print(f'\nMain null support_pct: {null_main}')
print(f'Wiki null support_pct: {null_wiki}')
print(f'Main rows: {len(main_ids)}, Wiki rows: {len(wiki_ids)}')
