#!/usr/bin/env python3
"""
Extract structured Blueprint message testing data from the compiled markdown source.
Appends new entries to messages.csv.

Usage:
    cd /home/agentbot/workspace/us-political-messaging-dataset
    python3 scripts/extract_blueprint_messages.py
"""

import csv
import re
import sys
from pathlib import Path
from collections import defaultdict

BASE = Path(__file__).parent.parent
PROC = BASE / 'data' / 'processed'
SRC = BASE / 'sources'

msg_fields = [
    'message_id', 'source', 'source_url', 'date', 'topic', 'issue_area',
    'message_type', 'wording', 'support_pct', 'oppose_pct', 'net_score',
    'preference_effect', 'effect_scale', 'sample_size', 'methodology',
    'population', 'moe', 'tags', 'notes'
]

def load_csv(path):
    rows = []
    if path.exists():
        with open(path, encoding='utf-8') as f:
            for row in csv.DictReader(f):
                rows.append(row)
    return rows

def write_csv(path, rows):
    with open(path, 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=msg_fields)
        w.writeheader()
        w.writerows(rows)

# Load existing messages to avoid duplicates
existing = load_csv(PROC / 'messages.csv')
existing_keys = set()
for r in existing:
    key = (r.get('source', ''), r.get('source_url', ''), r.get('wording', '')[:80])
    existing_keys.add(key)

# Parse Blueprint source
src_file = SRC / 'blueprint_message_testing_data.md'
with open(src_file, encoding='utf-8') as f:
    text = f.read()

# Split into sections
sections = re.split(r'\n##\s+', text)
print(f'Blueprint source: {len(sections)} sections found\n')

def extract_url(section_text):
    m = re.search(r'\*\*URL:\*\*\s*/polling/([^\s/]+)', section_text)
    if m:
        return f'https://blueprint-research.com/polling/{m.group(1)}/'
    return ''

def extract_date(section_title, section_text):
    m = re.search(r'\(([A-Z][a-z]+ \d+,? \d{4})\)', section_title)
    if m:
        from datetime import datetime
        try:
            dt = datetime.strptime(m.group(1), '%B %d, %Y')
            return dt.strftime('%Y-%m-%d')
        except:
            pass
    m = re.search(r'\(([A-Z][a-z]+ \d+,? \d{4})\)', section_text[:200])
    if m:
        from datetime import datetime
        try:
            dt = datetime.strptime(m.group(1), '%B %d, %Y')
            return dt.strftime('%Y-%m-%d')
        except:
            pass
    return ''

def extract_sample(section_text):
    m = re.search(r'\*\*Sample:\*\*\s*([\d,]+)', section_text)
    if m:
        return m.group(1).replace(',', '')
    return ''

def infer_topic(title, text):
    low = (title + ' ' + text[:300]).lower()
    topics = {
        'economy': ['inflation', 'price', 'economy', 'cost', 'afford', 'grocery', 'tax', 'debt', 'deficit'],
        'healthcare': ['health', 'medicare', 'drug', 'healthcare'],
        'immigration': ['immigra', 'border', 'asylum'],
        'abortion': ['abortion', 'roe', 'pro-choice', 'pro choice'],
        'democracy': ['democracy', 'vot', 'authoritarian', 'oligarchy'],
        'climate': ['climate', 'energy', 'environment'],
        'social_security': ['social security', 'ss', 'medicare'],
        'guns': ['gun', 'crime'],
        'foreign_policy': ['iran', 'israel', 'ukraine', 'china', 'nato', 'russia'],
        'technology': ['tech', 'musk', 'doge', 'social media'],
    }
    for topic, keywords in topics.items():
        for kw in keywords:
            if kw in low:
                return topic
    return 'politics'

def try_preference_line(line):
    """Try to extract a message with preference effect from a line like:
    '- "Fights—really fights—for all of us" → +14 overall, +14 independents'
    """
    line = line.strip()
    if not line.startswith('-'):
        return None
    
    content = line.lstrip('- ').strip()
    
    # Pattern: "wording" → +X or wording → +X
    m = re.match(r'["\u201c\u201d]?(.+?)["\u201c\u201d]?\s*[-\u2192]\s*([+-]?\d+)', content)
    if m:
        wording = m.group(1).strip().rstrip(',').strip()
        score = m.group(2)
        # Clean up wording
        wording = re.sub(r'\s+overall.*$', '', wording)
        wording = re.sub(r'\s+\(.*?$', '', wording)
        wording = re.sub(r'^["\u201c\u201d]|["\u201c\u201d]$', '', wording)
        return {
            'wording': wording.strip(),
            'preference_effect': score,
            'effect_scale': 'maxdiff',
        }
    return None

def try_support_line(line):
    """Try to extract a support percentage from a line like:
    '- 61% overall, 61% independents'
    """
    line = line.strip()
    if not line.startswith('-'):
        return None
    
    content = line.lstrip('- ').strip()
    
    m = re.match(r'(\d+)%\s*(.+?)(?:\s+\(([^)]+)\))?$', content)
    if m:
        pct = m.group(1)
        rest = m.group(2).strip()
        return {
            'support_pct': pct,
            'wording': rest if len(rest) > 10 else '',
        }
    return None

# Track what we already have by URL
existing_urls = set()
for r in existing:
    if r['source'] == 'Blueprint Research':
        existing_urls.add(r.get('source_url', ''))

new_rows = []
BLUEPRINT_BASE_URL = 'https://blueprint-research.com/polling/'

# Map section titles to URLs and dates for known articles
SECTION_META = {
    'Message to Democrats': {'slug': 'dem-message-test-2-5', 'date': '2025-12-05'},
    'How to Become Do-Something Democrats': {'slug': 'do-something-dems-10-15', 'date': '2025-10-23'},
    'Defining Harris': {'slug': 'harris-poll-positive-message-8-8', 'date': '2024-08-08'},
    'Campaign Like It\'s 2008': {'slug': 'obama-broad-messaging-9-5', 'date': '2024-09-04'},
    'Debate Snap Poll and Message Test': {'slug': 'debate-test-9-11', 'date': '2024-09-11'},
    'The Case For More Kamala': {'slug': 'interview-test-9-19', 'date': '2024-09-19'},
    'Interview Test: Oprah and MSNBC': {'slug': 'harris-interviews-test-10-7', 'date': '2024-10-07'},
    'Go Your Own Way: Kamala and Joe': {'slug': 'biden-distance-10-2-message-test', 'date': '2024-10-02'},
    'Closing Arguments': {'slug': 'trump-closing-argument-10-16', 'date': '2024-10-16'},
    'Back to Basics': {'slug': 'back-to-basics-3-6', 'date': '2024-03-06'},
    'Why America Chose Trump': {'slug': 'why-trump-reasons-11-8', 'date': '2024-11-08'},
    'Authoritarian Test': {'slug': 'authoritarian-test', 'date': '2025-11-10'},
    'The View Alternate Universe': {'slug': 'distance-biden-ads-message-test-10-15', 'date': '2024-10-15'},
    'Positive Beats Negative': {'slug': 'ads-test-harris-8-30', 'date': '2024-08-30'},
    'Kamala Harris Unburdened': {'slug': 'harris-poll-message-test-7-24', 'date': '2024-07-24'},
    'Change Election, Kitchen Table Mandate': {'slug': 'post-mortem-3-nov-25', 'date': '2024-11-25'},
    'The Mad Libs Candidate': {'slug': 'build-a-dem-workshop', 'date': '2025-11-14'},
    'Haley Voters Part 1 and 2': {'slug': 'haley-voters', 'date': '2024-10-09'},
    'John Kelly Vs. The Economy': {'slug': 'swing-state-kelly-10-28', 'date': '2024-10-28'},
    'Donald Trump Is the New Joe Biden': {'slug': 'trump-economy-1-21', 'date': '2026-01-21'},
    'Trump-Musk Vulnerabilities': {'slug': 'trump-musk-vulnerabilities-3-20', 'date': '2024-03-20'},
    'Swing State Decision Points': {'slug': 'swing-state-decision-points-10-29', 'date': '2024-10-29'},
    'Obama-Trump-Harris Voter': {'slug': 'swing-state-issues-10-31', 'date': '2024-10-31'},
    'Rust Belt to Sun Belt': {'slug': 'swing-state-9-9', 'date': '2024-09-09'},
    'Meat and Potatoes': {'slug': 'man-survey-9-25', 'date': '2024-09-25'},
}

msg_counter = 1
for existing_row in existing:
    mid = existing_row.get('message_id', '')
    if mid.startswith('BLP_'):
        num = int(mid.split('_')[-1])
        if num >= msg_counter:
            msg_counter = num + 1

for section in sections:
    title = section.split('\n')[0].strip()
    
    # Skip intro/quick reference sections
    if not title or 'Quick Reference' in title:
        continue
    
    # Get metadata
    meta = None
    for key in SECTION_META:
        if key.lower() in title.lower():
            meta = SECTION_META[key]
            break
    
    if not meta:
        print(f'  SKIP (no meta): {title[:60]}')
        continue
    
    url = f'{BLUEPRINT_BASE_URL}{meta["slug"]}/'
    
    # Skip if we already have messages from this URL
    if url in existing_urls:
        print(f'  SKIP (already processed): {title[:60]}')
        continue
    
    date = meta['date']
    sample = extract_sample(section)
    topic = infer_topic(title, section)
    
    lines = section.split('\n')
    extracted = []
    
    for line in lines:
        result = try_preference_line(line)
        if result:
            extracted.append(result)
            continue
        
        result = try_support_line(line)
        if result and result.get('wording'):
            extracted.append(result)
    
    if not extracted:
        print(f'  NO DATA: {title[:60]}')
        continue
    
    for item in extracted:
        row = {
            'message_id': f'BLP_{date.replace("-", "")}_{msg_counter:03d}',
            'source': 'Blueprint Research',
            'source_url': url,
            'date': date,
            'topic': topic,
            'issue_area': '',
            'message_type': 'tested_message',
            'wording': item.get('wording', ''),
            'support_pct': item.get('support_pct', ''),
            'oppose_pct': '',
            'net_score': '',
            'preference_effect': item.get('preference_effect', ''),
            'effect_scale': item.get('effect_scale', ''),
            'sample_size': sample,
            'methodology': 'online_panel',
            'population': 'likely_voters',
            'moe': '',
            'tags': f'blueprint;{topic}',
            'notes': f'From: {title[:120]}'
        }
        for col in msg_fields:
            if col not in row:
                row[col] = row.get(col, '')
        
        # Check for duplicates
        key = ('Blueprint Research', url, row['wording'][:80])
        if key not in existing_keys:
            new_rows.append(row)
            existing_keys.add(key)
            msg_counter += 1
    
    print(f'  EXTRACTED {len(extracted)} items: {title[:60]}')

print(f'\nTotal new Blueprint messages: {len(new_rows)}')

if new_rows:
    existing.extend(new_rows)
    write_csv(PROC / 'messages.csv', existing)

b_count = sum(1 for r in existing if r['source'] == 'Blueprint Research')
n_count = sum(1 for r in existing if r['source'] == 'Navigator Research')
d_count = sum(1 for r in existing if r['source'] == 'Data for Progress')
print(f'\nFinal messages.csv: {len(existing)} rows')
print(f'  Blueprint: {b_count}')
print(f'  Navigator: {n_count}')
print(f'  DFP:       {d_count}')
print('Done.')
