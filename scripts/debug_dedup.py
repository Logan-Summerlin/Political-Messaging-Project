#!/usr/bin/env python3
"""Debug: check which Wikipedia rows with descriptions are already in referendums.csv"""
import csv, re

# Load existing referendums
existing = {}
with open('data/processed/referendums.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        existing[(row['state'], row['year'], row['measure_name'].strip().lower())] = row

# Load Wikipedia
wiki = []
with open('data/raw/wikipedia_ballot_measures_complete.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        wiki.append(row)

# Rows to check: all rows with non-trivial full_text
checked = set()
for row in wiki:
    mn = row['measure_name'].strip()
    ft = row['full_text'].strip()
    yr = row['year']
    
    if not mn or not ft:
        continue
    if ft == mn:
        continue  # Just the name, no description
    
    # Get state
    state = None
    for sn, sa in [('Alabama','AL'),('Alaska','AK'),('Arizona','AZ'),('Arkansas','AR'),
                    ('California','CA'),('Colorado','CO'),('Florida','FL'),
                    ('Illinois','IL'),('Kentucky','KY'),('Maine','ME'),
                    ('Minnesota','MN'),('Nebraska','NE'),('Nevada','NV'),
                    ('Oklahoma','OK'),('Utah','UT'),('Washington','WA'),
                    ('West Virginia','WV'),('Idaho','ID'),('Oregon','OR'),
                    ('Massachusetts','MA'),('Missouri','MO'),('Montana','MT'),
                    ('Virginia','VA'), ('Los Angeles','CA'), ('Anchorage','AK')]:
        if sn in mn:
            state = sa
            break
    
    # Clean name
    display = re.sub(r'^(Legislatively-referred|Citizen-initiated|Initiated|Indirect initiated|Indirect)\s+(constitutional\s+)?(amendment|state\s+statute|bond\s+act|state\s+statue)\s*:\s*(?:\d{4}\s+)?', '', mn, flags=re.IGNORECASE)
    display = re.sub(r'^\d{4}\s+', '', display)
    display = re.sub(r'\s*\[\s*\d+\s*\]', '', display)
    display = re.sub(r'\s+', ' ', display).strip().lower()
    
    nums_new = set(re.findall(r'\b(\d+|[A-Z])\b', display))
    
    found = None
    for (es, ey, em), erow in existing.items():
        if es == state and ey == yr:
            nums_old = set(re.findall(r'\b(\d+|[A-Z])\b', em))
            common = nums_new.intersection(nums_old)
            if common:
                found = (erow['measure_name'], em)
                break
    
    outcome = row['outcome'].strip() if row['outcome'].strip() else 'NONE'
    
    key = (yr, state, display[:40])
    if key not in checked:
        checked.add(key)
        status = "DUPLICATE (in existing)" if found else "** NEW **"
        print(f'[{yr}] {state} | {display[:55]:55s} | {status} | ft_len={len(ft)} | outcome={outcome}')
        if found:
            print(f'    -> Existing: "{found[0][:60]}"')
