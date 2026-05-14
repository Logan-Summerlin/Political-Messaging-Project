#!/usr/bin/env python3
"""
Safe merge of clean DFP messages only.
No fresh chunk2 extraction - only uses verified clean data.
"""
import csv, re
from pathlib import Path

BASE = Path(__file__).parent.parent
PROC = BASE / "data" / "processed"
CHUNK1 = BASE / "data" / "raw" / "dataforprogress" / "chunk1_polling_data.md"

msg_fieldnames = [
    'message_id', 'source', 'source_url', 'date', 'topic', 'issue_area',
    'message_type', 'wording', 'support_pct', 'oppose_pct', 'net_score',
    'preference_effect', 'effect_scale', 'sample_size', 'methodology',
    'population', 'moe', 'tags', 'notes'
]

FRAGMENT_PATTERNS = [
    r'^Of the choices listed below', r'^In the voting booth',
    r'^the cost of (food|groceries)', r'^jobs and the economy',
    r'^somewhat of a problem', r'^already have enough influence',
    r'^responsible investing', r'^not (at all|confident|very|too)',
    r'^only a little confident', r'^a violent insurrection',
    r'^Congress is dysfunctional', r'^while \d+ percent say',
    r'^nonignorable', r'^free from controlled hazards',
    r'^protecting tenants', r'^manufacturing renaissance',
    r'^new license to discriminate', r'^compromise, waive, or release',
    r'^\d+,\d+ IRS agents', r'^in U\.S\. communities',
    r'^held in prisons', r'^87,000 IRS agents',
    r'^medically necessary\.?$', r'^unfairly raise prices\.?$',
    r'^the Biden administration', r'^low political interest',
    r'^next big climate test', r'^I\'?m concerned in general',
    r'^Environmental, Social, and Governance \(ESG\)$',
    r'^Don\'?t Say Gay or Trans', r'^I often feel like my job',
]

def is_fragment(wording):
    w = wording.strip().strip('"').strip("'").strip('"').strip()
    if len(w) < 28:
        return True
    for pat in FRAGMENT_PATTERNS:
        if re.match(pat, w, re.IGNORECASE):
            return True
    if w.lower().startswith(('which ', 'what ', 'how ', 'do you ', 'would you ', 'when asked')):
        return True
    return False

def clean_wording(w):
    w = w.strip()
    w = re.sub(r'^["\u201c\u201d]\s*', '', w)
    w = re.sub(r'\s*["\u201d]+$', '', w)
    if w:
        w = w[0].upper() + w[1:]
    return w.strip()

def topic_from_wording(w):
    wl = w.lower()
    if any(k in wl for k in ['tax', 'irs', 'tax cut', 'tax refund']): return 'economy'
    if any(k in wl for k in ['gaza', 'israel', 'hostage', 'ceasefire', 'military action', 'war', 'diplomatic', 'conflict', 'venezuela', 'maduro', 'putin']): return 'foreign_policy'
    if any(k in wl for k in ['gun', 'firearm', 'ammunition']): return 'crime'
    if any(k in wl for k in ['health', 'medicare', 'medicaid', 'drug', 'insurance', 'pregnant', 'abortion', 'hospital']): return 'healthcare'
    if any(k in wl for k in ['price', 'cost', 'inflation', 'grocery', 'energy', 'economy', 'tariff']): return 'economy'
    if any(k in wl for k in ['immigration', 'immigrant', 'border', 'asylum', 'ice']): return 'immigration'
    if any(k in wl for k in ['lgbtq', 'discrimination', 'abortion', 'marijuana', 'gay', 'trans', 'pride']): return 'social_issues'
    if any(k in wl for k in ['republican', 'democrat', 'party', 'government', 'congress', 'politician', 'vote', 'election']): return 'government'
    if any(k in wl for k in ['climate', 'environment', 'energy', 'fossil', 'oil', 'plastic', 'green']): return 'environment'
    if any(k in wl for k in ['school', 'education', 'student', 'teacher', 'child']): return 'education'
    return 'general'

if __name__ == '__main__':
    print("=" * 60)
    print("DFP MERGE - CLEAN ONLY")
    print("=" * 60)
    
    # Read existing
    with open(PROC / 'messages.csv', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        existing = list(reader)
    existing_ids = set(r['message_id'] for r in existing)
    print(f"Existing: {len(existing)} rows")
    
    added = 0
    
    # === STAGE 1: 42 clean DFP messages from dfp_new_messages ===
    with open(PROC / 'dfp_new_messages.csv', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        dfp_rows = list(reader)
    
    for r in dfp_rows:
        w = clean_wording(r['wording'])
        if is_fragment(w):
            continue
        mid = r['message_id'].strip()
        if mid in existing_ids:
            continue
        new_row = {k: r.get(k, '') for k in msg_fieldnames}
        new_row['wording'] = w
        new_row['source'] = 'Data for Progress'
        new_row['message_type'] = 'tested_message'
        new_row['topic'] = topic_from_wording(w)
        if 'tags' not in r or not r.get('tags'):
            new_row['tags'] = 'dfp;message_test'
        existing.append(new_row)
        existing_ids.add(mid)
        added += 1
    
    print(f"From dfp_new_messages.csv: {added} added")
    
    # === STAGE 2: Chunk1 messages ===
    text = CHUNK1.read_text(encoding='utf-8')
    sections = re.split(r'\n---\n', text)
    chunk1_count = 0
    
    for section in sections:
        if '### Message Wording Tested' not in section:
            continue
        url_match = re.search(r'https://www\.dataforprogress\.org/blog/\d{4}/\d{1,2}/[^\s)]+', section)
        url = url_match.group(0) if url_match else ''
        date_match = re.search(r'/blog/(\d{4})/(\d{1,2})/', url)
        date = f"{date_match.group(1)}-{int(date_match.group(2)):02d}-01" if date_match else ''
        
        msg_match = re.search(r'### Message Wording Tested\s*\n(.*?)(?:\n\n|\n---|\Z)', section, re.DOTALL)
        if not msg_match:
            continue
        
        block = msg_match.group(1)
        bullets = re.findall(r'[-*]\s*["\u201c]?\s*(.+?)\s*["\u201d]?\s*$', block, re.MULTILINE)
        
        for bullet in bullets:
            w = clean_wording(bullet)
            if not w or is_fragment(w) or len(w) < 28:
                continue
            
            # Generate unique ID
            base_id = f"DFP_{len([r for r in existing if r['source']=='Data for Progress']):05d}"
            while base_id in existing_ids:
                base_id = f"DFP_{int(base_id.split('_')[1])+1:05d}"
            
            new_row = {k: '' for k in msg_fieldnames}
            new_row['message_id'] = base_id
            new_row['source'] = 'Data for Progress'
            new_row['source_url'] = url
            new_row['date'] = date
            new_row['topic'] = topic_from_wording(w)
            new_row['message_type'] = 'tested_message'
            new_row['wording'] = w
            new_row['tags'] = 'dfp;message_test'
            new_row['notes'] = 'Extracted from DFP chunk1 Message Wording Tested section.'
            existing.append(new_row)
            existing_ids.add(base_id)
            chunk1_count += 1
            added += 1
    
    print(f"From chunk1: {chunk1_count} added")
    print(f"\nTotal added: {added}")
    print(f"Final: {len(existing)} rows")
    
    # Write
    with open(PROC / 'messages.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=msg_fieldnames)
        writer.writeheader()
        writer.writerows(existing)
    print("Saved.")
    
    # Summary
    from collections import Counter
    sources = Counter(r['source'] for r in existing)
    print("\nSource breakdown:")
    for s,c in sources.most_common():
        print(f"  {s}: {c}")
    
    # Show new DFP rows
    print("\nSample of new DFP message rows:")
    for r in existing:
        if r['source'] == 'Data for Progress' and not r['message_id'].startswith('DFP_02'):
            print(f"  {r['message_id']}: {r['wording'][:90]}")
            break
    for r in existing:
        if r['source'] == 'Data for Progress' and r['message_id'] >= 'DFP_000':
            print(f"  {r['message_id']}: {r['wording'][:90]}")
