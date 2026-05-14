#!/usr/bin/env python3
"""Check git history for messages.csv"""
import subprocess, csv, sys
from collections import Counter

for commit in ["HEAD", "HEAD~1", "HEAD~2", "HEAD~3"]:
    try:
        blob = subprocess.run(
            ["git", "show", f"{commit}:data/processed/messages.csv"],
            capture_output=True, text=True, cwd="/home/agentbot/workspace/us-political-messaging-dataset"
        )
        if blob.returncode != 0:
            print(f"{commit}: NOT FOUND")
            continue
        rows = list(csv.DictReader(blob.stdout.splitlines()))
        sources = Counter(r['source'] for r in rows)
        print(f"{commit}: {len(rows)} rows | {' | '.join(f'{s}={c}' for s,c in sources.most_common())}")
    except Exception as e:
        print(f"{commit}: ERROR {e}")
