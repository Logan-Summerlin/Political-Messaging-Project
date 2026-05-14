#!/usr/bin/env python3
"""
Clean DFP messages: filter fragments from dfp_new_messages.csv,
keep only genuine tested political messages with actual wording.
"""
import csv, re
from pathlib import Path

BASE = Path(__file__).parent.parent
PROC = BASE / "data" / "processed"
CHUNK2 = BASE / "data" / "raw" / "dataforprogress" / "chunk2_polling_data.md"

# Fragment patterns - these are NOT genuine political messages
FRAGMENT_PATTERNS = [
    r'^Of the choices listed below',
    r'^In the voting booth',
    r'^the cost of (food|groceries)',
    r'^jobs and the economy',
    r'^somewhat of a problem',
    r'^already have enough influence',
    r'^responsible investing',
    r'^not (at all|confident|very|too)',
    r'^only a little confident',
    r'^a violent insurrection',
    r'^Congress is dysfunctional',
    r'^while \d+ percent say',
    r'^nonignorable, nonobservable',
    r'^free from controlled hazards',
    r'^protecting tenants from displacement',
    r'^manufacturing renaissance',
    r'^new license to discriminate',
    r'^compromise, waive, or release',
    r'^\d+,\d+ IRS agents',
    r'^in U\.S\. communities',
    r'^held in prisons',
    r'^87,000 IRS agents',
    r'^medically necessary\.?$',
    r'^unfairly raise prices\.?$',
    r'^the Biden administration',
    r'^low political interest',
    r'^next big climate test',
    r'^I\'?m concerned in general',
    r'^Environmental, Social, and Governance \(ESG\)$',
    r'^Don\'?t Say Gay or Trans',
    r'^I often feel like my job',
]

def is_fragment(wording):
    """Check if a wording is a fragment, not a genuine political message."""
    w = wording.strip().strip('"').strip("'").strip('"')
    
    # Too short
    if len(w) < 30:
        return True, f"too_short ({len(w)}ch)"
    
    # Match fragment patterns
    for pat in FRAGMENT_PATTERNS:
        if re.match(pat, w, re.IGNORECASE):
            return True, f"pattern_match: {pat}"
    
    # Survey question text (starts with question words about choices)
    if w.lower().startswith(('which', 'what', 'how', 'do you', 'would you', 'when asked')):
        return True, "survey_question"
    
    # Response options that are just labels
    non_message_endings = ['?', ':']
    if w.startswith('"') and w.endswith('"'):
        w_inner = w.strip('"').strip()
    else:
        w_inner = w
    
    # Extract just a label without being a real message
    # Real messages typically describe a policy position or argument
    # Fragments are just descriptive labels
    
    return False, ""

# Also extract fresh from chunk2 raw data for better quality
def extract_from_chunk2(chunk2_path):
    """Extract Tested Message Wording sections from chunk2 raw data."""
    text = chunk2_path.read_text(encoding='utf-8')
    
    messages = []
    # Split by ## headings to get individual articles
    sections = re.split(r'^## ', text, flags=re.MULTILINE)
    
    for section in sections:
        if not section.strip():
            continue
        
        # Extract URL
        url_match = re.search(r'\*\*URL:\*\*\s*(https?://[^\s]+)', section)
        url = url_match.group(1) if url_match else ''
        
        # Extract date
        date_match = re.search(r'\*\*Date:\*\*\s*(\d{4}-\d{2}-\d{2})', section)
        date = date_match.group(1) if date_match else ''
        
        # Extract article title (first line if it's not metadata)
        lines = section.strip().split('\n')
        title = lines[0].strip()
        if title.startswith('**URL:') or title.startswith('**Date:') or title.startswith('--'):
            title = ''
        
        # Extract Tested Message Wording
        msg_match = re.search(r'\*\*Tested Message Wording:\*\*\s*(.*?)(?:\n\n|\*\*Polling)', section, re.DOTALL)
        if msg_match:
            block = msg_match.group(1)
            # Each bullet point is a message
            bullets = re.findall(r'[-*]\s*["\u201c]?\s*([^"\n]+?)\s*["\u201d]?\s*', block)
            for bullet in bullets:
                b = bullet.strip()
                if b:
                    messages.append({
                        'wording': b,
                        'source_url': url,
                        'date': date,
                        'title': title,
                    })
        
        # Also look for ### Message Wording Tested (chunk1 format)
        msg_match2 = re.search(r'### Message Wording Tested\s*(.*?)(?:\n\n|---)', section, re.DOTALL)
        if msg_match2:
            block2 = msg_match2.group(1)
            bullets = re.findall(r'[-*]\s*["\u201c]?\s*([^"\n]+?)\s*["\u201d]?\s*', block2)
            for bullet in bullets:
                b = bullet.strip()
                if b:
                    messages.append({
                        'wording': b,
                        'source_url': url,
                        'date': date,
                        'title': title,
                    })
    
    return messages

if __name__ == '__main__':
    # Read existing dfp_new_messages.csv
    with open(PROC / 'dfp_new_messages.csv', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        all_rows = list(reader)
    
    print(f"Total rows in dfp_new_messages: {len(all_rows)}")
    
    # Classify each row
    passes = []
    rejects = []
    for r in all_rows:
        is_bad, reason = is_fragment(r['wording'])
        if is_bad:
            rejects.append((r, reason))
        else:
            passes.append(r)
    
    print(f"PASS (genuine messages): {len(passes)}")
    print(f"REJECT (fragments): {len(rejects)}")
    
    print("\n--- PASSING messages ---")
    for r in passes:
        w = r['wording'][:100]
        print(f"  {r['message_id']}: {w}")
    
    print("\n--- REJECTED fragments (first 20) ---")
    for r, reason in rejects[:20]:
        w = r['wording'][:80]
        print(f"  [{reason}] {w}")
    
    # Also try fresh extraction from chunk2
    print("\n\n=== Fresh extraction from chunk2 ===")
    fresh_msgs = extract_from_chunk2(CHUNK2)
    print(f"Raw messages from chunk2: {len(fresh_msgs)}")
    
    # Filter fresh ones
    clean_fresh = []
    for m in fresh_msgs:
        is_bad, reason = is_fragment(m['wording'])
        if not is_bad:
            clean_fresh.append(m)
    
    print(f"Clean messages from chunk2: {len(clean_fresh)}")
    for m in clean_fresh:
        print(f"  [{m['date']}] ({len(m['wording'])}ch) {m['wording'][:100]}")