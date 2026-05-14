#!/usr/bin/env python3
"""Check backup files for source counts"""
import csv, sys
from collections import Counter

files = [
    "data/processed/messages.csv.bak_pre_cleanup",
    "data/processed/messages.csv.bak.20260509_162623",
    "data/processed/messages.csv.bak.20260509_150629",
    "data/processed/messages.csv.bak.20260509_151615",
    "data/processed/messages.csv.bak.20260509_150629",
    "data/archive/v1.0.0/messages.csv",
    "data/archive/v1.1.0/messages.csv",
    "data/archive/messages.csv.bak",
]

base = "/home/agentbot/workspace/us-political-messaging-dataset"

for f in files:
    path = f"{base}/{f}"
    try:
        with open(path, newline='', encoding='utf-8') as fh:
            rows = list(csv.DictReader(fh))
        sources = Counter(r['source'] for r in rows)
        print(f"{f}: {len(rows)} rows | {' | '.join(f'{s}={c}' for s,c in sources.most_common())}")
    except Exception as e:
        print(f"{f}: ERROR {e}")
