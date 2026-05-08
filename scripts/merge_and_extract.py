#!/usr/bin/env python3
"""
Merge new DFP data + extract all Navigator messages.

Usage:
    cd /home/agentbot/workspace/us-political-messaging-dataset
    python3 scripts/merge_and_extract.py
"""

import csv
import re
import sys
from pathlib import Path

BASE = Path(__file__).parent.parent
PROC = BASE / "data" / "processed"
RAW = BASE / "data" / "raw"

# Smart quotes for cleanup
LEFT_DQ = '\u201c'
RIGHT_DQ = '\u201d'
LEFT_SQ = '\u2018'
RIGHT_SQ = '\u2019'
BULLET = '\u2022'
ALL_QUOTES = '"' + LEFT_DQ + RIGHT_DQ + LEFT_SQ + RIGHT_SQ

def load_csv(path):
    rows = []
    if not path.exists():
        return rows
    with open(path, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows

def write_csv(path, rows, fieldnames):
    with open(path, 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)

# ====== STEP 1: Merge messages ======
print('=' * 60)
print('STEP 1: Merging DFP new messages')
print('=' * 60)

msg_fields = [
    'message_id', 'source', 'source_url', 'date', 'topic', 'issue_area',
    'message_type', 'wording', 'support_pct', 'oppose_pct', 'net_score',
    'preference_effect', 'effect_scale', 'sample_size', 'methodology',
    'population', 'moe', 'tags', 'notes'
]

existing_msgs = load_csv(PROC / 'messages.csv')
new_msgs = load_csv(PROC / 'dfp_new_messages.csv')

existing_msg_keys = set()
for r in existing_msgs:
    key = (r.get('source_url', ''), r.get('wording', '')[:80])
    existing_msg_keys.add(key)

added_m = 0
skipped_m = 0
for r in new_msgs:
    key = (r.get('source_url', ''), r.get('wording', '')[:80])
    if key not in existing_msg_keys:
        for col in msg_fields:
            if col not in r:
                r[col] = r.get(col, '')
        existing_msgs.append(r)
        existing_msg_keys.add(key)
        added_m += 1
    else:
        skipped_m += 1

# Reassign DFP sequential IDs
next_id = 1000
for r in existing_msgs:
    if r['source'] == 'Data for Progress':
        r['message_id'] = f'DFP_{next_id:04d}'
        next_id += 1

write_csv(PROC / 'messages.csv', existing_msgs, msg_fields)
b_count = sum(1 for r in existing_msgs if r['source'] == 'Blueprint Research')
n_count = sum(1 for r in existing_msgs if r['source'] == 'Navigator Research')
d_count = sum(1 for r in existing_msgs if r['source'] == 'Data for Progress')
print(f'  Total messages.csv: {len(existing_msgs)} rows')
print(f'  Added: {added_m}, Skipped dupes: {skipped_m}')
print(f'  Blueprint={b_count}, Navigator={n_count}, DFP={d_count}')

# ====== STEP 2: Merge issues ======
print()
print('=' * 60)
print('STEP 2: Merging DFP new issues')
print('=' * 60)

issue_fields = [
    'poll_id', 'source', 'source_url', 'date', 'question_type',
    'question_wording', 'topic', 'issue_area', 'support_pct', 'oppose_pct',
    'net', 'sample_size', 'methodology', 'population', 'moe', 'tags', 'notes'
]

existing_issues = load_csv(PROC / 'issues.csv')
new_issues = load_csv(PROC / 'dfp_new_issues.csv')

existing_issue_ids = {r['poll_id'] for r in existing_issues}

added_i = 0
skipped_i = 0
for r in new_issues:
    pid = r.get('poll_id', '')
    if pid not in existing_issue_ids:
        for col in issue_fields:
            if col not in r:
                r[col] = r.get(col, '')
        existing_issues.append(r)
        existing_issue_ids.add(pid)
        added_i += 1
    else:
        skipped_i += 1

write_csv(PROC / 'issues.csv', existing_issues, issue_fields)
print(f'  Total issues.csv: {len(existing_issues)} rows')
print(f'  Added: {added_i}, Skipped dupes: {skipped_i}')

# ====== STEP 3: Navigator extraction ======
print()
print('=' * 60)
print('STEP 3: Full Navigator archive extraction')
print('=' * 60)

nav_file = RAW / 'navigator' / 'navigator_full_archive.md'
if not nav_file.exists():
    print('  ERROR: navigator_full_archive.md not found')
    sys.exit(1)

with open(nav_file, encoding='utf-8') as f:
    text = f.read()

articles = re.split(r'## \d+\.\s+', text)
print(f'  Found {len(articles) - 1} articles in archive')

# Track already-extracted Navigator articles
existing_nav_urls = set()
for r in existing_msgs:
    if r['source'] == 'Navigator Research':
        existing_nav_urls.add(r.get('source_url', ''))

TOPIC_KW = [
    ('food', 'healthcare'), ('health', 'healthcare'), ('medicare', 'healthcare'),
    ('medicaid', 'healthcare'), ('rfk', 'healthcare'),
    ('immigra', 'immigration'), ('border', 'immigration'), ('ice', 'immigration'),
    ('tariff', 'economy'), ('tax', 'economy'), ('budget', 'economy'),
    ('inflation', 'economy'), ('price', 'economy'), ('cost', 'economy'),
    ('save act', 'voting_rights'), ('voter', 'democracy'), ('voting', 'democracy'),
    ('iran', 'foreign_policy'), ('israel', 'foreign_policy'), ('china', 'foreign_policy'),
    ('ukraine', 'foreign_policy'), ('russia', 'foreign_policy'),
    ('abortion', 'abortion'), ('gun', 'guns'), ('climate', 'climate'),
    ('doge', 'government'), ('musk', 'technology'), ('elon', 'technology'),
    ('social security', 'social_security'), ('ss', 'social_security'),
    ('trump', 'politics'), ('gop', 'politics'), ('republican', 'politics'),
    ('democrat', 'politics'), ('congress', 'politics'),
    ('tariffs', 'economy'), ('trade', 'economy'), ('taxes', 'taxes'),
    ('shutdown', 'government'), ('budget', 'economy'),
]

def infer_topic(title, body):
    low = (title + ' ' + body[:300]).lower()
    for kw, topic in TOPIC_KW:
        if kw in low:
            return topic
    return 'general'

def extract_sample_size(text):
    m = re.search(r'Sample[:\s]*([\d,]+)', text)
    if m:
        return m.group(1).replace(',', '')
    m = re.search(r'n\s*=\s*([\d,]+)', text)
    if m:
        return m.group(1).replace(',', '')
    return ''

def extract_date(text):
    m = re.search(r'(\d{4}-\d{2}-\d{2})', text[:500])
    if m:
        return m.group(1)
    months = {
        'January': '01', 'February': '02', 'March': '03', 'April': '04',
        'May': '05', 'June': '06', 'July': '07', 'August': '08',
        'September': '09', 'October': '10', 'November': '11', 'December': '12'
    }
    m = re.search(
        r'(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d+),?\s+(\d{4})',
        text[:500]
    )
    if m:
        return f"{m.group(3)}-{months[m.group(1)]}-{int(m.group(2)):02d}"
    return ''

def clean_text(s):
    """Strip bullet markers and quotes from text."""
    s = s.strip()
    for ch in ['-', '*', BULLET]:
        if s.startswith(ch):
            s = s[1:].strip()
    for q in [LEFT_DQ, RIGHT_DQ, LEFT_SQ, RIGHT_SQ, '"', "'"]:
        s = s.strip(q)
    return s.strip()

nav_extracted = []
msg_counter = len(existing_msgs) + 1

for article in articles[1:]:
    lines = article.split('\n')
    title = lines[0].strip() if lines else ''

    # Extract URL
    url = ''
    for line in lines:
        for m in re.finditer(r'(https?://navigatorresearch\.org[^\s\)\"]+)', line):
            url = m.group(1).rstrip(')')
            break
        if url:
            break

    if not url:
        continue

    # Skip if we already have messages from this article
    if url in existing_nav_urls:
        continue

    date = extract_date(article)
    sample = extract_sample_size(article)
    topic = infer_topic(title, article)
    body_text = ' '.join(lines[1:])

    # Strategy 1: Find quoted passages with nearby percentages
    extracted = []
    
    # Find quoted text (any kind of quotes)
    for m in re.finditer(
        r'[' + LEFT_DQ + RIGHT_DQ + LEFT_SQ + RIGHT_SQ + r'\"\']'
        r'([^' + LEFT_DQ + RIGHT_DQ + LEFT_SQ + RIGHT_SQ + r'\'\"]{20,300})'
        r'[' + LEFT_DQ + RIGHT_DQ + LEFT_SQ + RIGHT_SQ + r'\"\']',
        body_text
    ):
        quoted = m.group(1).strip()
        if len(quoted) > 25:
            # Look for percentage near the quote
            window = body_text[max(0, m.start()-100):m.end()+100]
            pct = ''
            pc = re.search(r'(\d+)%', window)
            if pc:
                pct = pc.group(1)
            extracted.append((quoted, pct))

    # Strategy 2: Bullet points with percentages
    for line in lines:
        s = line.strip()
        if not s:
            continue
        if s.startswith('-') or s.startswith('*') or s.startswith(BULLET):
            cleaned = clean_text(s)
            if len(cleaned) > 25 and '%' in cleaned:
                # Already captured?
                already = any(cleaned[:40] in e[0] or e[0][:40] in cleaned for e in extracted)
                if not already:
                    pc = re.search(r'(\d+)%', cleaned)
                    pct = pc.group(1) if pc else ''
                    # Extract the framing, not the percentage line itself
                    # Try to get the actual message wording
                    msg_text = re.sub(r'\s*\d+%.*$', '', cleaned).strip()
                    if len(msg_text) > 25:
                        extracted.append((msg_text, pct))

    if not extracted:
        continue

    for wording, pct in extracted:
        row = {
            'message_id': f'NAV_{msg_counter:04d}',
            'source': 'Navigator Research',
            'source_url': url,
            'date': date,
            'topic': topic,
            'issue_area': '',
            'message_type': 'tested_message',
            'wording': wording[:500],
            'support_pct': pct,
            'oppose_pct': '',
            'net_score': '',
            'preference_effect': '',
            'effect_scale': '',
            'sample_size': sample,
            'methodology': 'online_panel',
            'population': 'likely_voters',
            'moe': '',
            'tags': f'navigator;{topic}',
            'notes': f'From: {title[:120]}'
        }
        for col in msg_fields:
            if col not in row:
                row[col] = row.get(col, '')
        nav_extracted.append(row)
        msg_counter += 1

    existing_nav_urls.add(url)

print(f'  New Navigator messages extracted: {len(nav_extracted)}')

if nav_extracted:
    existing_msgs.extend(nav_extracted)

    # Reassign DFP IDs cleanly
    next_id = 1000
    for r in existing_msgs:
        if r['source'] == 'Data for Progress':
            r['message_id'] = f'DFP_{next_id:04d}'
            next_id += 1

    write_csv(PROC / 'messages.csv', existing_msgs, msg_fields)

b_count = sum(1 for r in existing_msgs if r['source'] == 'Blueprint Research')
n_count = sum(1 for r in existing_msgs if r['source'] == 'Navigator Research')
d_count = sum(1 for r in existing_msgs if r['source'] == 'Data for Progress')
print(f'  Final messages.csv: {len(existing_msgs)} rows')
print(f'    Blueprint: {b_count} | Navigator: {n_count} | DFP: {d_count}')

# ====== FINAL SUMMARY ======
print()
print('=' * 60)
print('SUMMARY')
print('=' * 60)
print(f'  messages.csv: {len(existing_msgs)} rows')
print(f'  issues.csv:   {len(existing_issues)} rows')
print('Done.')
