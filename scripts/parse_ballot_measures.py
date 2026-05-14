#!/usr/bin/env python3
"""
Parse raw Wikipedia HTML files (wiki_ballot_*.html) to extract ballot measure data.
Updates referendums.csv with vote percentages, passage status, and descriptions.

Two formats:
- 2024: One big wikitable with 9 columns: State, Origin, Status, Measure, Description, Date, % req., Yes, No
        + Additional topic-specific wikitables with 8 columns: State, Origin, Status, Measure, Description, Date, % req., Result
- 2022: Per-state wikitables with 5 columns: Measure, Type, Description, Result, Reference
- 2008-2020: Simple list pages with no structured data (can't extract from these)

NOTE: The Description/Summary IS available, but FULL ballot wording is NOT in any of these pages.
"""

import csv
import re
import os
from collections import Counter

RAW_DIR = '/home/agentbot/workspace/us-political-messaging-dataset/data/raw'
CSV_PATH = '/home/agentbot/workspace/us-political-messaging-dataset/data/processed/referendums.csv'

# State name to code mapping
STATE_MAP = {
    'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR',
    'California': 'CA', 'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE',
    'Florida': 'FL', 'Georgia': 'GA', 'Hawaii': 'HI', 'Idaho': 'ID',
    'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA', 'Kansas': 'KS',
    'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD',
    'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN',
    'Mississippi': 'MS', 'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE',
    'Nevada': 'NV', 'New Hampshire': 'NH', 'New Jersey': 'NJ',
    'New Mexico': 'NM', 'New York': 'NY', 'North Carolina': 'NC',
    'North Dakota': 'ND', 'Ohio': 'OH', 'Oklahoma': 'OK', 'Oregon': 'OR',
    'Pennsylvania': 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC',
    'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT',
    'Vermont': 'VT', 'Virginia': 'VA', 'Washington': 'WA',
    'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY',
}

def read_html(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def clean_text(text):
    """Remove HTML tags and decode entities."""
    text = re.sub(r'<br\s*/?>', ' | ', text)
    text = re.sub(r'<[^>]+>', '', text)
    text = text.replace('&#160;', ' ')
    text = text.replace('&amp;', '&')
    text = text.replace('&lt;', '<')
    text = text.replace('&gt;', '>')
    text = text.replace('&#91;', '[')
    text = text.replace('&#93;', ']')
    text = text.replace('&#95;', '_')
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def extract_table_blocks(html):
    """Find all <table class='wikitable'> blocks and return (start, end) positions."""
    blocks = []
    for m in re.finditer(r'<table\s+class="wikitable"', html):
        start = m.start()
        depth = 0
        i = start
        while i < len(html):
            if html[i] == '<':
                tag_start = i
                while i < len(html) and html[i] != '>':
                    i += 1
                tag = html[tag_start:i+1]
                if tag.startswith('<table'):
                    depth += 1
                elif tag.startswith('</table'):
                    depth -= 1
                    if depth == 0:
                        blocks.append((start, i + 1))
                        break
            i += 1
    return blocks

def parse_pct_votes(cell_text):
    """Parse a cell like '183,744 | 57.98%' or just '48.69%'."""
    text = clean_text(cell_text)
    pct = None
    votes = None
    
    pct_m = re.search(r'(\d+\.?\d*)\s*%', text)
    if pct_m:
        pct = float(pct_m.group(1))
    
    # Get vote count (before the %)
    parts = re.split(r'\s*\|\s*', text)
    if parts and parts[0].strip():
        try:
            votes = int(parts[0].strip().replace(',', ''))
        except ValueError:
            pass
    
    return pct, votes


def extract_2024_measures(html):
    """Parse 2024 wikitables - both the main table (9-col) and topic tables (8-col)."""
    measures = []
    blocks = extract_table_blocks(html)
    
    for start, end in table_blocks_for_html(html):
        table_html = html[start:end]
        
        # Get column count from header row
        rows = re.findall(r'<tr>(.*?)</tr>', table_html, re.DOTALL)
        header_count = 0
        for row_html in rows:
            headers_raw = re.findall(r'<th>(.*?)</th>', row_html, re.DOTALL)
            if headers_raw:
                header_count = len(headers_raw)
                headers_clean = [clean_text(h).lower() for h in headers_raw]
                break
        
        # Determine table type
        has_yes_no = any('yes' in h or 'no' in h for h in headers_raw)
        has_result_col = any('result' in h.lower() for h in headers_raw)
        has_state = any('state' in h.lower() for h in headers_raw)
        
        if not has_state:
            continue
        
        # Parse the table
        state_name = None
        for row_html in rows:
            # Get all cells
            cells = re.findall(r'<td[^>]*>(.*?)</td>', row_html, re.DOTALL)
            if not cells:
                continue
            
            # Check for state cell with/without rowspan
            rowspan_cells = re.findall(r'<td[^>]*rowspan[^>]*>(.*?)</td>', row_html, re.DOTALL)
            
            cell_texts = [clean_text(c) for c in cells]
            
            # Track state
            new_state = None
            if rowspan_cells:
                ns = clean_text(rowspan_cells[0])
                if ns in STATE_MAP:
                    new_state = ns
                    state_name = new_state
            elif cell_texts and cell_texts[0] in STATE_MAP:
                new_state = cell_texts[0]
                state_name = new_state
            
            # Determine cell indexing based on table type
            if has_yes_no and header_count >= 8:
                # Main table: State(1), Origin(1), Status(1), Measure(1), Desc(1), Date(1), %req(1), Yes(1), No(1) = 9 cols
                # Or with rowspan: Origin(1), Status(1), Measure(1), Desc(1), Date(1), %req(1), Yes(1), No(1) = 8 cols
                
                # If we have a state column, it's at index 0
                if new_state:
                    # Full row with state: state, origin, status, measure, desc, date, %req, yes, no = 9 cells
                    if len(cells) >= 9:
                        origin = clean_text(cells[1])
                        status_raw = clean_text(cells[2])
                        measure_name = clean_text(cells[3])
                        description = clean_text(cells[4])
                        vote_col_idx_yes = 7
                        vote_col_idx_no = 8
                    else:
                        continue
                else:
                    # Rowspan row (no state cell): origin, status, measure, desc, date, %req, yes, no = 8 cells
                    if len(cells) >= 8:
                        origin = cell_texts[0]
                        status_raw = cell_texts[1]
                        measure_name = cell_texts[2]
                        description = cell_texts[3]
                        vote_col_idx_yes = 6
                        vote_col_idx_no = 7
                    else:
                        continue
                
                yes_pct, yes_votes = parse_pct_votes(cells[vote_col_idx_yes])
                no_pct, no_votes = parse_pct_votes(cells[vote_col_idx_no])
                
            elif has_result_col and header_count >= 7:
                # Topic table: State(1), Origin(1), Status(1), Measure(1), Desc(1), Date(1), %req(1), Result(1) = 8 cols
                # Or with rowspan: Origin(1), Status(1), Measure(1), Desc(1), Date(1), %req(1), Result(1) = 7 cols
                
                if new_state:
                    if len(cells) >= 8:
                        origin = clean_text(cells[1])
                        status_raw = clean_text(cells[2])
                        measure_name = clean_text(cells[3])
                        description = clean_text(cells[4])
                        result_raw = clean_text(cells[7])
                    else:
                        continue
                else:
                    if len(cells) >= 7:
                        origin = cell_texts[0]
                        status_raw = cell_texts[1]
                        measure_name = cell_texts[2]
                        description = cell_texts[3]
                        result_raw = cell_texts[6]
                    else:
                        continue
                
                yes_pct, no_pct = None, None
                yes_votes, no_votes = None, None
            
            else:
                continue
            
            if not measure_name or measure_name == 'None':
                continue
            
            # Determine passed status
            passed = None
            # Check status column first
            if 'approved' in status_raw.lower():
                passed = True
            elif 'failed' in status_raw.lower():
                passed = False
            
            # If result column exists (topic tables), also check that
            if has_result_col:
                try:
                    result_text = result_raw
                    if 'passed' in result_text.lower() or 'approved' in result_text.lower():
                        passed = True
                    elif 'failed' in result_text.lower() or 'defeated' in result_text.lower():
                        passed = False
                    elif 'repealed' in result_text.lower():
                        passed = False
                    elif 'tbd' in result_text.lower() or 'on ballot' in result_text.lower():
                        pass  # Keep existing value
                except (NameError, UnboundLocalError):
                    pass
            
            if state_name and measure_name:
                measures.append({
                    'state': state_name,
                    'measure_name': measure_name,
                    'description': description,
                    'passed': passed,
                    'support_pct': yes_pct,
                    'oppose_pct': no_pct,
                    'votes_for': yes_votes,
                    'votes_against': no_votes,
                })
        
        # Reset state_name for next table
        state_name = None
    
    return measures

def table_blocks_for_html(html):
    """Yields (start, end) tuples for wikitable blocks."""
    blocks = extract_table_blocks(html)
    return blocks


def extract_2022_measures(html):
    """Parse 2022 per-state wikitables."""
    measures = []
    blocks = extract_table_blocks(html)
    
    # Find state headings
    state_headings = {}
    for m in re.finditer(r'<h2[^>]*id="([A-Z][a-z_]+)"', html):
        state_name = m.group(1).replace('_', ' ')
        pos = m.start()
        state_headings[pos] = state_name
    
    sorted_positions = sorted(state_headings.keys())
    
    for start, end in blocks:
        # Find nearest preceding state heading
        state_name = None
        for pos in reversed(sorted_positions):
            if pos < start:
                state_name = state_headings[pos]
                break
        
        if not state_name:
            continue
        
        table_html = html[start:end]
        
        # Check if it's a 2022-style table (has Measure, Type, Description, Result headers)
        if 'Type' not in table_html[:600] and 'Result' not in table_html[:600]:
            continue
        
        rows = re.findall(r'<tr>(.*?)</tr>', table_html, re.DOTALL)
        for row_html in rows:
            cells = re.findall(r'<td[^>]*>(.*?)</td>', row_html, re.DOTALL)
            if len(cells) < 4:
                continue
            
            measure_name = clean_text(cells[0])
            description = clean_text(cells[2])
            result_raw = clean_text(cells[3])
            
            if not measure_name or measure_name == 'None':
                continue
            
            passed = None
            rl = result_raw.lower()
            if rl in ('passed', 'approved'):
                passed = True
            elif rl in ('failed', 'repealed', 'defeated'):
                passed = False
            
            state_code = STATE_MAP.get(state_name, state_name)
            
            measures.append({
                'state': state_code,
                'measure_name': measure_name,
                'description': description,
                'passed': passed,
            })
    
    return measures


def normalize_name(name):
    """Normalize measure name for comparison."""
    name = name.strip()
    name = re.sub(r'^\d{4}\s+', '', name)
    name = re.sub(r'^Ballot\s+', '', name, flags=re.IGNORECASE)
    name = re.sub(r'^Initiated\s+', '', name, flags=re.IGNORECASE)
    name = re.sub(r'\s+', ' ', name)
    return name


def match_measure(csv_row, ext):
    """Try to match CSV row to extracted measure."""
    csv_name = normalize_name(csv_row['measure_name']).lower()
    ext_name = normalize_name(ext['measure_name']).lower()
    
    if csv_name == ext_name:
        return True
    if csv_name in ext_name or ext_name in csv_name:
        return True
    
    # Same numbers?
    csv_nums = set(re.findall(r'\d+', csv_name))
    ext_nums = set(re.findall(r'\d+', ext_name))
    if csv_nums and ext_nums and csv_nums == ext_nums:
        csv_types = set(re.findall(r'[a-z]+', csv_name))
        ext_types = set(re.findall(r'[a-z]+', ext_name))
        if csv_types & ext_types:
            return True
    
    return False


def load_csv(csv_path):
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)


def save_csv(csv_path, rows):
    fieldnames = rows[0].keys() if rows else []
    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def update_2024(rows, html_path):
    """Update CSV rows with 2024 data."""
    html = read_html(html_path)
    extracted = extract_2024_measures(html)
    
    print(f"2024: Extracted {len(extracted)} measures from HTML")
    
    updates = 0
    for ext in extracted:
        ext_state = STATE_MAP.get(ext['state'], ext['state'])
        
        for row in rows:
            if row['year'] != '2024':
                continue
            if row['state'].upper() != ext_state.upper():
                continue
            if not match_measure(row, ext):
                continue
            
            updated = False
            
            # Update support/oppose pct
            if ext.get('support_pct') is not None and not row.get('support_pct'):
                row['support_pct'] = str(round(ext['support_pct'], 2))
                if ext.get('oppose_pct') is not None:
                    row['oppose_pct'] = str(round(ext['oppose_pct'], 2))
                updated = True
            
            # Update passed
            if ext.get('passed') is not None and not row.get('passed'):
                row['passed'] = str(ext['passed']).upper()
                updated = True
            
            # Update votes
            if ext.get('votes_for') is not None and not row.get('votes_for'):
                row['votes_for'] = str(ext['votes_for'])
                if ext.get('votes_against') is not None:
                    row['votes_against'] = str(ext['votes_against'])
                updated = True
            
            if updated:
                updates += 1
    
    print(f"2024: Updated {updates} cells")
    return updates


def update_2022(rows, html_path):
    """Update CSV rows with 2022 data."""
    html = read_html(html_path)
    extracted = extract_2022_measures(html)
    
    print(f"2022: Extracted {len(extracted)} measures from HTML")
    
    # Debug unmatched
    matched = set()
    updates = 0
    
    for ext in extracted:
        for i, row in enumerate(rows):
            if row['year'] != '2022':
                continue
            if row['state'].upper() != ext['state'].upper():
                continue
            if not match_measure(row, ext):
                continue
            
            updated = False
            
            if ext.get('passed') is not None and not row.get('passed'):
                row['passed'] = str(ext['passed']).upper()
                updated = True
            
            if updated:
                matched.add(i)
                updates += 1
    
    print(f"2022: Updated {updates} cells")
    return updates


def main():
    rows = load_csv(CSV_PATH)
    print(f"Loaded {len(rows)} rows")
    
    # Pre-count
    null_w = sum(1 for r in rows if not r['wording'])
    null_s = sum(1 for r in rows if not r['support_pct'])
    null_p = sum(1 for r in rows if not r['passed'])
    print(f"Before: wording={null_w} null, support={null_s} null, passed={null_p} null")
    
    # Process 2024
    p2024 = os.path.join(RAW_DIR, 'wiki_ballot_2024.html')
    if os.path.exists(p2024):
        update_2024(rows, p2024)
    
    # Process 2022
    p2022 = os.path.join(RAW_DIR, 'wiki_ballot_2022.html')
    if os.path.exists(p2022):
        update_2022(rows, p2022)
    
    # Save
    save_csv(CSV_PATH, rows)
    
    # Summary
    null_w = sum(1 for r in rows if not r['wording'])
    null_s = sum(1 for r in rows if not r['support_pct'])
    null_p = sum(1 for r in rows if not r['passed'])
    
    print(f"\n=== After Update ===")
    print(f"Total rows: {len(rows)}")
    print(f"Null wording: {null_w}/{len(rows)} ({100*null_w//len(rows)}%)")
    print(f"Null support_pct: {null_s}/{len(rows)} ({100*null_s//len(rows)}%)")
    print(f"Null passed: {null_p}/{len(rows)} ({100*null_p//len(rows)}%)")
    
    for y in sorted(Counter(r['year'] for r in rows).keys()):
        yr = [r for r in rows if r['year'] == y]
        ns = sum(1 for r in yr if not r['support_pct'])
        npd = sum(1 for r in yr if not r['passed'])
        nw = sum(1 for r in yr if not r['wording'])
        print(f"  {y}: {len(yr)} rows, wording={nw}, support={ns}, passed={npd}")


if __name__ == '__main__':
    main()
