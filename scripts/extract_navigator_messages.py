#!/usr/bin/env python3
"""
Extract structured message A/B test data from Navigator Research topline PDFs.

This script extracts paired "Which side do you agree with more?" and 
"Which side do you find more convincing?" message tests from all
extracted Navigator Research text files.

Each test has two paired messages (democratic/progressive vs republican/trump)
with overall support percentage and demographic breakdowns.
"""

import csv
import os
import re
import sys

# Base directory for Navigator PDFs
PDF_DIR = os.path.expanduser(
    "~/workspace/us-political-messaging-dataset/data/raw/navigator/pdfs"
)
OUTPUT_DIR = os.path.expanduser(
    "~/workspace/us-political-messaging-dataset/data/processed"
)

# Files to process with metadata
FILES_TO_PROCESS = [
    ("Navigator-Topline-F04.07.25_extracted.txt", "2025-04-07"),
    ("Navigator-Topline-F09.08.25_extracted.txt", "2025-09-08"),
    ("Navigator-January-1-Topline-F01.12.26_extracted.txt", "2026-01-12"),
    ("Navigator-Topline-F02.02.26_extracted.txt", "2026-02-02"),
    ("Navigator-Toplines-03.16.2026_extracted.txt", "2026-03-16"),
    ("Navigator-April-1-Topline-F04.06.26_cleaned.txt", "2026-04-06"),
]

HEADER_INDICATORS = ["Latest Data by Party", "Latest Data by Race"]
COL_HEADERS = ["Dem", "Ind", "Rep", "Afr Am", "Hisp", "White", "AAPI"]

QUESTION_PATTERNS = [
    r'^Which side do you (agree with|find) more',
]

MONTH_MAP = {
    'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04',
    'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08',
    'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'
}


def is_dots_line(line):
    """Check if a line is mostly dots (separator)."""
    stripped = line.strip()
    if not stripped:
        return False
    dot_count = stripped.count('.')
    return dot_count > 0 and dot_count >= len(stripped) * 0.5


def is_number_line(stripped):
    """Check if a line is just a number (possibly with %)."""
    if not stripped:
        return False
    return bool(re.match(r'^\d+\.?\d*%?$', stripped))


def is_question_start(stripped):
    """Check if a line starts a new question."""
    if not stripped:
        return False
    return bool(re.match(r'^(Q\d+[A-Z]*\.|TARIFFS\d+\.)', stripped))


def is_text_data_line(stripped):
    """Check if a line is actual message text (not a header, number, or control line)."""
    if not stripped:
        return False
    if stripped in HEADER_INDICATORS or stripped in COL_HEADERS:
        return False
    if stripped == "AAPI":
        return False
    if re.match(r'^(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)$', stripped):
        return False
    if re.match(r'^\d{1,2}$', stripped):
        return False
    if is_question_start(stripped):
        return False
    if stripped.startswith("Latest Data") or stripped.startswith("Global Strategy Group"):
        return False
    if stripped.startswith("Page") or stripped.startswith("Changing topics") or stripped.startswith("Switching subjects"):
        return False
    if stripped.startswith("For statistical") or stripped.startswith("Not sure"):
        return False
    if stripped.startswith("Don't know enough to say"):
        return False
    if is_number_line(stripped):
        return False
    if is_dots_line(stripped):
        return False
    return True


def extract_demographics(lines, start_idx, max_look=25):
    """Extract demographic breakdown percentages after a message.
    Returns (overall_pct, d1-d7, next_idx) or (None,...,idx) on failure."""
    overall_pct = None
    nums = []
    found_data = False
    idx = start_idx
    
    while idx < min(start_idx + max_look, len(lines)):
        stripped = lines[idx].strip()
        
        if is_number_line(stripped):
            num_str = stripped.rstrip('%')
            try:
                num = float(num_str)
                if num <= 100:
                    nums.append(num)
                    found_data = True
                    if len(nums) >= 8:
                        return (nums[0], nums[1], nums[2], nums[3],
                                nums[4], nums[5], nums[6], nums[7], idx + 1)
            except ValueError:
                pass
        elif found_data:
            # If we've found some numbers, stop at non-number lines
            break
        
        idx += 1
    
    if nums:
        return (nums[0] if len(nums) > 0 else None,
                nums[1] if len(nums) > 1 else None,
                nums[2] if len(nums) > 2 else None,
                nums[3] if len(nums) > 3 else None,
                nums[4] if len(nums) > 4 else None,
                nums[5] if len(nums) > 5 else None,
                nums[6] if len(nums) > 6 else None,
                nums[7] if len(nums) > 7 else None,
                idx)
    return None, None, None, None, None, None, None, None, idx


def collect_message_text(lines, start_idx, max_look=50):
    """Collect all text lines that form a message.
    Returns (message_text_lines, end_idx)"""
    text_lines = []
    idx = start_idx
    
    while idx < min(start_idx + max_look, len(lines)):
        stripped = lines[idx].strip()
        
        if not stripped:
            idx += 1
            continue
        
        if is_dots_line(stripped):
            break
        
        if is_question_start(stripped):
            break
        
        # Stop at percentage/number lines
        if is_number_line(stripped):
            break
        
        if stripped.startswith("Not sure"):
            break
        if stripped.startswith("Don't know enough to say"):
            break
        
        # Skip headers
        if stripped in HEADER_INDICATORS or stripped in COL_HEADERS or stripped == "AAPI":
            idx += 1
            continue
        
        # Skip month/date lines
        if re.match(r'^(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)$', stripped):
            idx += 1
            continue
        if re.match(r'^\d{1,2}$', stripped):
            idx += 1
            continue
        
        if stripped.startswith("Latest Data") or stripped.startswith("Global Strategy Group"):
            idx += 1
            break
        if stripped.startswith("Page") or stripped.startswith("Changing topics") or stripped.startswith("Switching subjects") or stripped.startswith("For statistical"):
            idx += 1
            break
        
        # This is message text
        text_lines.append(stripped)
        idx += 1
    
    # Skip dots
    while idx < len(lines):
        stripped = lines[idx].strip()
        if not stripped or is_dots_line(stripped):
            idx += 1
        else:
            break
    
    return text_lines, idx


def process_file(filepath, default_date):
    """Process a single topline file and extract all message tests."""
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        lines = f.readlines()
    
    messages = []
    
    # Find all "Which side" questions
    question_indices = []
    for i, line in enumerate(lines):
        stripped = line.strip()
        for pattern in QUESTION_PATTERNS:
            if re.match(pattern, stripped, re.IGNORECASE):
                q_number = ""
                for j in range(max(0, i-5), i):
                    prev_line = lines[j].strip()
                    q_match = re.match(r'^(Q\d+[A-Z]*\.)', prev_line)
                    if q_match:
                        q_number = q_match.group(1)
                        break
                    t_match = re.match(r'^(TARIFFS\d+\.)', prev_line)
                    if t_match:
                        q_number = t_match.group(1)
                        break
                question_indices.append((i, q_number, stripped))
                break
    
    if not question_indices:
        print(f"  No 'Which side' questions found")
        return messages
    
    print(f"  Found {len(question_indices)} 'Which side' question instances")
    
    for idx, (q_line_idx, q_number, q_text) in enumerate(question_indices):
        # Find data start (after AAPI header)
        data_start = None
        for i in range(q_line_idx, min(q_line_idx + 50, len(lines))):
            stripped = lines[i].strip()
            if stripped == "AAPI":
                data_start = i + 1
                break

        if data_start is None:
            # Try finding month/date pattern
            for i in range(q_line_idx, min(q_line_idx + 30, len(lines))):
                stripped = lines[i].strip()
                if re.match(r'^(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)$', stripped):
                    for j in range(i, min(i + 15, len(lines))):
                        if lines[j].strip() == "AAPI":
                            data_start = j + 1
                            break
                    if data_start:
                        break
        
        if data_start is None:
            print(f"    WARNING: Could not find data start for {q_number}")
            continue
        
        # Extract date
        date_str = default_date
        for i in range(q_line_idx, min(q_line_idx + 20, len(lines))):
            stripped = lines[i].strip()
            m = re.match(r'^(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)$', stripped)
            if m:
                month = m.group(1)
                if i + 1 < len(lines):
                    day = lines[i + 1].strip()
                    if re.match(r'^\d{1,2}$', day):
                        month_num = MONTH_MAP.get(month, '01')
                        year = default_date[:4]
                        date_str = f"{year}-{month_num}-{day.zfill(2)}"
                break
        
        # Skip text that belongs to previous section's "Not sure" or "Don't know enough to say"
        # Check if data_start points to leftover text
        check_idx = data_start
        while check_idx < min(data_start + 5, len(lines)):
            stripped = lines[check_idx].strip()
            if stripped.startswith("Not sure") or stripped.startswith("Don't know enough to say") or is_number_line(stripped):
                # This is leftover from previous question, skip
                check_idx += 1
                if is_number_line(stripped):
                    # Skip the rest of the numbers
                    for k in range(check_idx, min(check_idx + 20, len(lines))):
                        if not is_number_line(lines[k].strip()):
                            check_idx = k
                            break
            else:
                break
        data_start = check_idx
        
        # Collect first message text
        msg1_lines, idx1 = collect_message_text(lines, data_start)
        
        # Get percentages for first message
        ov1, d1, i1, r1, aa1, h1, w1, aapi1, idx2 = extract_demographics(lines, idx1)
        
        if ov1 is None:
            print(f"    WARNING: Could not find percentages for first message in {q_number}")
            continue
        
        # Find second message start - skip to where text starts
        skip_idx = idx2
        for i in range(idx2, min(idx2 + 5, len(lines))):
            stripped = lines[i].strip()
            if stripped.startswith("Not sure") or stripped.startswith("Don't know enough to say"):
                # Skip "Not sure" section (usually 8 numbers)
                ns_count = 0
                for j in range(i + 1, min(i + 15, len(lines))):
                    if is_number_line(lines[j].strip()):
                        ns_count += 1
                    else:
                        break
                    if ns_count >= 7:
                        skip_idx = j + 1
                        break
                break
            if is_question_start(stripped):
                skip_idx = i
                break
            if not stripped or is_dots_line(stripped):
                continue
            if len(stripped) > 5 and not is_number_line(stripped):
                # This is message text - second message starts here
                skip_idx = i
                break
        
        # Collect second message text
        msg2_lines, idx3 = collect_message_text(lines, skip_idx)
        
        # Get percentages for second message
        ov2, d2, i2, r2, aa2, h2, w2, aapi2, idx4 = extract_demographics(lines, idx3)
        
        if ov2 is None:
            print(f"    WARNING: Could not find percentages for second message in {q_number}")
            continue
        
        msg1_text = ' '.join(msg1_lines)
        msg2_text = ' '.join(msg2_lines)
        
        topic = determine_topic(q_number, msg1_text, msg2_text, q_text)
        
        msg_type = "contrast" if "find more convincing" in q_text.lower() else "tested_message"
        
        # Create two message records with demographic breakdowns in dem_all
        for side_num, (text, ov, d, ind, r, aa, h, w, api) in enumerate([
            (msg1_text, ov1, d1, i1, r1, aa1, h1, w1, aapi1),
            (msg2_text, ov2, d2, i2, r2, aa2, h2, w2, aapi2)
        ], 1):
            dem_str = f"Dem:{d}%;Ind:{ind}%;Rep:{r}%;AfrAm:{aa}%;Hisp:{h}%;White:{w}%;AAPI:{api}%"
            if any(v is None for v in [d, ind, r, aa, h, w, api]):
                # Build partial dem string
                parts = []
                for label, val in [("Dem", d), ("Ind", ind), ("Rep", r), 
                                    ("AfrAm", aa), ("Hisp", h), ("White", w), ("AAPI", api)]:
                    if val is not None:
                        parts.append(f"{label}:{val}%")
                dem_str = ";".join(parts)
            
            messages.append({
                'source': 'Navigator Research',
                'date': date_str,
                'topic': topic,
                'issue_area': '',
                'message_type': msg_type,
                'wording': text,
                'support_pct': ov if (ov is not None and ov <= 100) else None,
                'sample_size': 1000,
                'methodology': 'online_panel',
                'population': 'registered_voters',
                'moe': 3.1,
                'tags': f'navigator;{topic}',
                'notes': f'From Navigator topline {os.path.basename(filepath)}, question {q_number} - side {side_num}. Field: {date_str}.',
                'dem_all': dem_str
            })
        
        print(f"    {q_number}: {ov1:.0f}% / {ov2:.0f}% - '{msg1_text[:55]}...' vs '{msg2_text[:55]}...'")
    
    return messages


def determine_topic(q_number, msg1, msg2, q_text):
    """Determine the topic from message content."""
    combined = (msg1 + ' ' + msg2 + ' ' + q_text).lower()
    
    if any(w in combined for w in ['tariff', 'tariffs', 'tariff rebate']):
        return 'economy'
    if any(w in combined for w in ['immigra', 'border', 'ice ', 'deport', 'pathway to citizenship', 'birthright']):
        return 'immigration'
    if any(w in combined for w in ['maduro', 'venezuela', 'iran', 'military operation', 'troops', 'war with']):
        return 'foreign_policy'
    if any(w in combined for w in ['medicaid', 'snap', 'affordable care act', 'health care', 'healthcare', 'health insurance', 'drug compan']):
        return 'healthcare'
    if any(w in combined for w in ['gerrymander', 'congressional map', 'redrawing', 'voters first']):
        return 'democracy'
    if any(w in combined for w in ['data center', 'data centers']):
        return 'technology'
    if any(w in combined for w in ['tax cut', 'tax refund', 'tax break', 'taxes on tips', 'overtime pay', 'tax system', 'fair share in taxes']):
        return 'economy'
    if any(w in combined for w in ['one big beautiful bill', 'obb', 'republican budget', 'tax increases']):
        return 'economy'
    if any(w in combined for w in ['waste, fraud', 'waste fraud', 'government spend']):
        return 'government'
    if any(w in combined for w in ['national guard', 'crime', 'safety', 'deploying troops']):
        return 'crime'
    if any(w in combined for w in ['vaccine', 'misinformation', 'science']):
        return 'healthcare'
    if any(w in combined for w in ['corporation', 'corporate', 'big corporat', 'polluter', 'chemical']):
        return 'politics'
    
    return 'politics'


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    all_messages = []
    message_counter = 1
    
    for filename, date in FILES_TO_PROCESS:
        filepath = os.path.join(PDF_DIR, filename)
        if not os.path.exists(filepath):
            print(f"File not found: {filepath}")
            continue
        
        print(f"\nProcessing: {filename}")
        messages = process_file(filepath, date)
        
        # Assign message IDs
        for msg in messages:
            date_compact = date.replace('-', '')
            msg['message_id'] = f"NAV_{date_compact}_{message_counter:03d}"
            message_counter += 1
        
        all_messages.extend(messages)
    
    # Write output CSV
    output_path = os.path.join(OUTPUT_DIR, 'navigator_pdf_messages.csv')
    
    fieldnames = [
        'message_id', 'source', 'source_url', 'date', 'topic', 'issue_area',
        'message_type', 'wording', 'support_pct', 'oppose_pct', 'net_score',
        'preference_effect', 'effect_scale', 'sample_size', 'methodology',
        'population', 'moe', 'tags', 'notes', 'dem_all'
    ]
    
    source_url = "https://navigatorresearch.org/"
    
    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for msg in all_messages:
            row = {k: msg.get(k, '') for k in fieldnames}
            row['source_url'] = source_url
            writer.writerow(row)
    
    print(f"\n{'='*60}")
    print(f"EXTRACTION SUMMARY")
    print(f"{'='*60}")
    print(f"Files processed: {len(FILES_TO_PROCESS)}")
    print(f"Messages extracted: {len(all_messages)}")
    print(f"Paired tests: {len(all_messages)//2}")
    print(f"Output file: {output_path}")
    
    topics = {}
    for msg in all_messages:
        t = msg['topic']
        topics[t] = topics.get(t, 0) + 1
    print("\nMessages by topic:")
    for t, c in sorted(topics.items(), key=lambda x: -x[1]):
        print(f"  {t}: {c}")


if __name__ == '__main__':
    main()
