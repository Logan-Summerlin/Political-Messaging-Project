#!/usr/bin/env python3
"""
Merge clean DFP messages into messages.csv.
Also extract clean DFP messages from chunk1 format.
"""
import csv, re
from pathlib import Path

BASE = Path(__file__).parent.parent
PROC = BASE / "data" / "processed"
CHUNK1 = BASE / "data" / "raw" / "dataforprogress" / "chunk1_polling_data.md"
CHUNK2 = BASE / "data" / "raw" / "dataforprogress" / "chunk2_polling_data.md"

msg_fieldnames = [
    'message_id', 'source', 'source_url', 'date', 'topic', 'issue_area',
    'message_type', 'wording', 'support_pct', 'oppose_pct', 'net_score',
    'preference_effect', 'effect_scale', 'sample_size', 'methodology',
    'population', 'moe', 'tags', 'notes'
]

# ====== Fragment filter (same as clean_dfp_messages.py) ======
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
    r'^Don\'?t Say Gay or Trans',
    r'^I often feel like my job',
]

def is_fragment(wording):
    w = wording.strip().strip('"').strip("'").strip('"')
    if len(w) < 28:
        return True
    for pat in FRAGMENT_PATTERNS:
        if re.match(pat, w, re.IGNORECASE):
            return True
    if w.lower().startswith(('which ', 'what ', 'how ', 'do you ', 'would you ', 'when asked')):
        return True
    return False

def clean_wording(w):
    """Clean up garbled DFP wording artifacts."""
    w = w.strip()
    # Remove leading space+quote artifacts like `" for` or `" In`
    w = re.sub(r'^["\u201c\u201d]\s*', '', w)
    w = re.sub(r'\s+["\u201c\u201d]$', '', w)
    # Remove trailing "s:
    w = re.sub(r'\s*["\u201d]+$', '', w)
    # Capitalize first letter
    if w:
        w = w[0].upper() + w[1:]
    return w.strip()

# ====== Extract from chunk1 ======
def extract_chunk1_messages():
    text = CHUNK1.read_text(encoding='utf-8')
    messages = []
    
    # Split by --- separators to get individual articles
    sections = re.split(r'\n---\n', text)
    
    for section in sections:
        if '### Message Wording Tested' not in section:
            continue
            
        # Extract URL from within section
        url_match = re.search(r'https://www\.dataforprogress\.org/blog/\d{4}/\d{1,2}/[^\s)]+', section)
        url = url_match.group(0) if url_match else ''
        
        # Extract date from URL
        date_match = re.search(r'/blog/(\d{4})/(\d{1,2})/', url)
        date = f"{date_match.group(1)}-{int(date_match.group(2)):02d}-01" if date_match else ''
        
        # Extract the message wording section
        msg_match = re.search(r'### Message Wording Tested\s*\n(.*?)(?:\n\n|\n---|\Z)', section, re.DOTALL)
        if not msg_match:
            continue
        
        block = msg_match.group(1)
        bullets = re.findall(r'[-*]\s*["\u201c]?\s*(.+?)\s*["\u201d]?\s*$', block, re.MULTILINE)
        
        for bullet in bullets:
            bullet = clean_wording(bullet)
            if bullet and not is_fragment(bullet) and len(bullet) >= 28:
                messages.append({
                    'wording': bullet,
                    'source_url': url,
                    'date': date,
                })
    
    return messages

# ====== Extract from chunk2 ======
def extract_chunk2_messages():
    text = CHUNK2.read_text(encoding='utf-8')
    messages = []
    
    # Find all Tested Message Wording sections
    for match in re.finditer(r'\*\*Tested Message Wording:\*\*\s*(.*?)(?:\n\n---|\Z)', text, re.DOTALL):
        block = match.group(1)
        bullets = re.findall(r'[-*]\s*["\u201c]?\s*(.+?)\s*["\u201d]?\s*$', block, re.MULTILINE)
        
        for bullet in bullets:
            bullet = clean_wording(bullet)
            if bullet and not is_fragment(bullet) and len(bullet) >= 28:
                messages.append({'wording': bullet})
    
    return messages

def topic_from_wording(w):
    """Infer topic from wording."""
    w_lower = w.lower()
    if any(kw in w_lower for kw in ['tax', 'irs', 'tax cut', 'tax break', 'tax refund']):
        return 'economy'
    if any(kw in w_lower for kw in ['gaza', 'israel', 'hostage', 'ceasefire', 'military', 'war', 'diplomatic', 'conflict']):
        return 'foreign_policy'
    if any(kw in w_lower for kw in ['gun', 'firearm', 'ammunition']):
        return 'crime'
    if any(kw in w_lower for kw in ['health', 'medicare', 'medicaid', 'drug', 'insurance', 'pregnant', 'abortion']):
        return 'healthcare'
    if any(kw in w_lower for kw in ['price', 'cost', 'inflation', 'grocery', 'energy', 'economy']):
        return 'economy'
    if any(kw in w_lower for kw in ['immigration', 'immigrant', 'border', 'asylum']):
        return 'immigration'
    if any(kw in w_lower for kw in ['lgbtq', 'discrimination', 'abortion', 'reproductive']):
        return 'social_issues'
    if any(kw in w_lower for kw in ['republican', 'democrat', 'party', 'govern', 'congress', 'politician']):
        return 'government'
    if any(kw in w_lower for kw in ['climate', 'environment', 'energy', 'fossil', 'oil']):
        return 'environment'
    return 'general'

if __name__ == '__main__':
    print("=" * 60)
    print("DFP MESSAGE CLEANUP & MERGE")
    print("=" * 60)
    
    # Read existing messages.csv
    with open(PROC / 'messages.csv', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        existing = list(reader)
    
    existing_ids = set(r['message_id'] for r in existing)
    print(f"Existing messages.csv: {len(existing)} rows")
    
    # ====== STAGE 1: Read clean DFP from dfp_new_messages.csv ======
    with open(PROC / 'dfp_new_messages.csv', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        dfp_rows = list(reader)
    
    dfp_clean = []
    dfp_rejected = 0
    for r in dfp_rows:
        w = clean_wording(r['wording'])
        if not is_fragment(w) and len(w) >= 28:
            r['wording'] = w
            r['message_id'] = r['message_id'].strip()
            dfp_clean.append(r)
        else:
            dfp_rejected += 1
    
    print(f"\nDFP from dfp_new_messages: {len(dfp_clean)} clean, {dfp_rejected} rejected")
    
    # ====== STAGE 2: Extract from chunk1 ======
    chunk1_msgs = extract_chunk1_messages()
    print(f"Chunk1 messages extracted: {len(chunk1_msgs)}")
    
    for m in chunk1_msgs:
        print(f"  [{m['date']}] '{m['wording'][:80]}'")
    
    # ====== STAGE 3: Extract from chunk2 (fresh) ======
    chunk2_msgs = extract_chunk2_messages()
    print(f"\nChunk2 messages extracted (fresh): {len(chunk2_msgs)}")
    
    # ====== STAGE 4: Merge ======
    added = 0
    
    # First, get the current highest DFP ID
    dfp_ids = [r['message_id'] for r in existing if r['message_id'].startswith('DFP_')]
    dfp_nums = []
    for mid in dfp_ids:
        try:
            dfp_nums.append(int(mid.split('_')[-1]))
        except:
            pass
    next_num = max(dfp_nums) + 1 if dfp_nums else 0
    
    # Merge clean DFP from csv
    for r in dfp_clean:
        mid = r['message_id']
        if mid not in existing_ids:
            # Ensure all fields exist
            new_row = {k: r.get(k, '') for k in msg_fieldnames}
            new_row['source'] = 'Data for Progress'
            new_row['message_type'] = 'tested_message'
            new_row['tags'] = 'dfp;message_test'
            if not new_row.get('topic'):
                new_row['topic'] = topic_from_wording(new_row['wording'])
            existing.append(new_row)
            existing_ids.add(new_row['message_id'])
            added += 1
    
    # Merge chunk1 messages (need new IDs)
    for m in chunk1_msgs:
        mid = f"DFP_{next_num:05d}"
        next_num += 1
        while mid in existing_ids:
            mid = f"DFP_{next_num:05d}"
            next_num += 1
        
        new_row = {k: '' for k in msg_fieldnames}
        new_row['message_id'] = mid
        new_row['source'] = 'Data for Progress'
        new_row['source_url'] = m['source_url']
        new_row['date'] = m['date']
        new_row['topic'] = topic_from_wording(m['wording'])
        new_row['message_type'] = 'tested_message'
        new_row['wording'] = m['wording']
        new_row['tags'] = 'dfp;message_test'
        new_row['notes'] = 'Extracted from DFP chunk1 Message Wording Tested section.'
        existing.append(new_row)
        existing_ids.add(mid)
        added += 1
    
    # Merge chunk2 messages (fresh)
    for m in chunk2_msgs:
        # Check for dupes
        w = m['wording'].lower().strip()
        is_dup = False
        for r in existing:
            if r['source'] == 'Data for Progress' and r['wording'].lower().strip() == w:
                is_dup = True
                break
        if is_dup:
            continue
        
        mid = f"DFP_{next_num:05d}"
        next_num += 1
        while mid in existing_ids:
            mid = f"DFP_{next_num:05d}"
            next_num += 1
        
        new_row = {k: '' for k in msg_fieldnames}
        new_row['message_id'] = mid
        new_row['source'] = 'Data for Progress'
        new_row['source_url'] = ''
        new_row['date'] = ''
        new_row['topic'] = topic_from_wording(m['wording'])
        new_row['message_type'] = 'tested_message'
        new_row['wording'] = m['wording']
        new_row['tags'] = 'dfp;message_test'
        new_row['notes'] = 'Extracted from DFP chunk2 Tested Message Wording section.'
        existing.append(new_row)
        existing_ids.add(mid)
        added += 1
    
    print(f"\nTotal new DFP messages added: {added}")
    print(f"Final messages.csv: {len(existing)} rows")
    
    # Write
    with open(PROC / 'messages.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=msg_fieldnames)
        writer.writeheader()
        writer.writerows(existing)
    
    print("Updated messages.csv written.")
    
    # Print sample of new DFP rows
    print("\n--- New DFP rows added ---")
    for r in existing:
        if r['source'] == 'Data for Progress' and len(r['wording']) > 30:
            print(f"  {r['message_id']}: {r['wording'][:90]}")