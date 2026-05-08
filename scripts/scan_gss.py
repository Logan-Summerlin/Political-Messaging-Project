#!/usr/bin/env python3
"""Scan GSS dataset for political/messaging-related variables."""
import pyreadstat
import sys

dta_path = "/home/agentbot/workspace/us-political-messaging-dataset/data/raw/gss/stata_extracted/gss7224_r3.dta"

print("Reading GSS metadata (variable names and labels)...")
df, meta = pyreadstat.read_dta(dta_path, row_limit=1, encoding='latin1')

# Print all variable names and labels
print(f"\nTotal variables: {len(meta.column_names)}")
print(f"Total rows: approx {meta.number_rows}\n")

# Search for politically relevant variables
keywords = [
    'party', 'polit', 'ideol', 'liberal', 'conserv',
    'spending', 'spend', 'priority', 'nat',
    'approv', 'confid', 'conf', 'trust',
    'abort', 'gun', 'death', 'capit', 'crime',
    'immig', 'race', 'equal', 'fair',
    'pres', 'vote', 'election',
    'economy', 'inflat', 'unemploy',
    'health', 'medic',
    'tax', 'welfar', 'aid',
    'relig', 'church',
    'moral', 'family',
    'free', 'right',
    'satisf', 'happi',
]

found_vars = {}
for name, label in zip(meta.column_names, meta.column_labels):
    name_lower = name.lower()
    label_lower = (label or '').lower()
    for kw in keywords:
        if kw in name_lower or kw in label_lower:
            found_vars[name] = label
            break

print(f"\n=== Matching political variables: {len(found_vars)} ===\n")

# Group by topic
topics = {
    'Party/Id': ['partyid', 'polviews', 'libcon'],
    'Nat spending': [n for n in found_vars if n.startswith('nat')],
    'Confidence': [n for n in found_vars if n.startswith('con') or 'conf' in n.lower()],
    'Abortion': [n for n in found_vars if 'abort' in n.lower() or n.startswith('ab')],
    'Gun/Death/Crime': [n for n in found_vars if any(k in n.lower() for k in ['gun', 'cappun', 'courts', 'crime', 'porn', 'drug'])] if False else [],
    'Vote/Pres': [n for n in found_vars if n.startswith('pres') or n.startswith('vote')],
    'Economy/Jobs': [n for n in found_vars if any(k in n.lower() for k in ['econom', 'inflat', 'unemploy', 'job', 'prices'])],
    'Immigration': [n for n in found_vars if 'immig' in n.lower()],
    'Race/Equality': [n for n in found_vars if any(k in n.lower() for k in ['rac', 'equal', 'discrim', 'prej', 'affrm'])] if False else [],
    'Health': [n for n in found_vars if 'health' in n.lower() or 'medic' in n.lower() or n.startswith('natheal')],
    'Welfare/Tax': [n for n in found_vars if any(k in n.lower() for k in ['welfar', 'tax', 'aid'])],
    'Other': [],
}

# Print found vars in groups
for topic, varnames in topics.items():
    if not varnames:
        continue
    print(f"\n--- {topic} ---")
    for v in varnames:
        if v in found_vars:
            label = found_vars[v][:80] if found_vars[v] else '(no label)'
            print(f"  {v:30s} {label}")
