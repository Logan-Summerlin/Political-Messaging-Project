#!/usr/bin/env python3
"""
Scrape US ballot measure data from Wikipedia (2008-2024).

Handles multiple Wikipedia page formats:
- 2024: Single table with all states, has vote percentages
- 2022: Per-state tables with outcome (pass/fail), no percentages
- 2020-2008: Various formats (may need per-year handling)
"""

import csv, re, sys, urllib.request, time, json
from pathlib import Path
from collections import Counter

BASE = Path(__file__).parent.parent
OUT = BASE / "data" / "processed"

HEADERS = {'User-Agent': 'USPoliticalMessaging/1.0 (research)'}

# US state full name → abbreviation map
STATE_ABBR = {
    'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR',
    'California': 'CA', 'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE',
    'Florida': 'FL', 'Georgia': 'GA', 'Hawaii': 'HI', 'Idaho': 'ID',
    'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA', 'Kansas': 'KS',
    'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD',
    'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS',
    'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV',
    'New Hampshire': 'NH', 'New Jersey': 'NJ', 'New Mexico': 'NM', 'New York': 'NY',
    'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH', 'Oklahoma': 'OK',
    'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC',
    'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT',
    'Vermont': 'VT', 'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV',
    'Wisconsin': 'WI', 'Wyoming': 'WY', 'District of Columbia': 'DC',
}

STATE_NAMES_SET = set(k.lower() for k in STATE_ABBR)

TOPIC_KEYWORDS = {
    'abortion': ['abortion', 'fetal', 'reproductive', 'unborn', 'pro-life', 'viability'],
    'taxes': ['tax', 'taxation', 'taxpayer', 'income tax', 'property tax', 'sales tax', 'levy', 'bond'],
    'voting_rights': ['voting', 'election', 'voter', 'ballot', 'electoral', 'ranked', 'redistrict', 'gerrymander'],
    'drugs': ['marijuana', 'cannabis', 'drug', 'psychedelic', 'psilocybin', 'opioid'],
    'crime': ['crime', 'criminal', 'penalty', 'sentencing', 'felony', 'theft', 'prison', 'police'],
    'guns': ['gun', 'firearm', 'weapon', 'ammunition', 'second amendment'],
    'education': ['education', 'school', 'student', 'teacher', 'classroom', 'voucher', 'tuition'],
    'healthcare': ['health', 'medicaid', 'hospital', 'insurance', 'medical'],
    'minimum_wage': ['minimum wage', 'wage', 'hourly', 'overtime', 'paid leave'],
    'environment': ['environment', 'energy', 'conservation', 'wildlife', 'park', 'water', 'renewable', 'nuclear', 'solar', 'climate'],
    'civil_rights': ['civil rights', 'discrimination', 'affirmative', 'equality', 'lgbt', 'marriage', 'slavery'],
    'immigration': ['immigra', 'border', 'sanctuary', 'citizenship', 'alien'],
    'housing': ['housing', 'rent', 'homeless', 'zoning', 'property'],
    'gambling': ['gambling', 'casino', 'lottery', 'betting', 'sports betting'],
    'transportation': ['transportation', 'transit', 'road', 'highway', 'bridge', 'rail'],
    'labor': ['labor', 'union', 'worker', 'employee', 'collective bargaining'],
    'government': ['government', 'legislature', 'constitutional amendment', 'term limits', 'initiative',
                   'referendum', 'veto', 'supermajority'],
}

def infer_topic(desc, name):
    text = (name + ' ' + desc).lower()
    for topic, kws in TOPIC_KEYWORDS.items():
        if any(kw in text for kw in kws):
            return topic
    return 'government'

def fetch_page(year):
    url = f"https://en.wikipedia.org/wiki/{year}_United_States_ballot_measures"
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode('utf-8')

def extract_state_sections(html):
    """Find state names in section headings.
    
    2024 format: <h2><span class="mw-headline" id="Alabama">Alabama</span></h2>
    2022 format: <h2 id="Alabama">Alabama</h2>  (wrapped in mw-heading div)
    """
    states_found = []
    # Try multiple patterns
    patterns = [
        r'<h[23][^>]*id="([A-Z][a-z]+(?:_[A-Z][a-z]+)*)"',                        # <h2 id="Alabama">Alabama</h2>
        r'<span[^>]*class="mw-headline"[^>]*id="([A-Z][a-z]+(?:_[A-Z][a-z]+)*)"', # <span class="mw-headline" id="Alabama">
    ]
    
    for pattern in patterns:
        for match in re.finditer(pattern, html):
            name = match.group(1).replace('_', ' ')
            if name.lower() in STATE_NAMES_SET or name == 'District of Columbia':
                if name not in states_found:
                    states_found.append(name)
        if states_found:
            break
    
    return states_found

def parse_2024_table(table_html, year):
    """Parse 2024 comprehensive format: State|Origin|Status|Measure|Description|Date|% req.|Yes|No"""
    rows = []
    # Column labels in order
    col_labels = ['state', 'origin', 'status', 'measure', 'description', 'date', 'threshold', 'yes_or_result', 'no']
    
    trs = re.findall(r'<tr>(.*?)</tr>', table_html, re.DOTALL)
    for tr in trs[1:]:
        cells = re.findall(r'<t[dh][^>]*>(.*?)</t[dh]>', tr, re.DOTALL)
        if len(cells) < 5:
            continue
        
        row = {'year': year}
        for i, label in enumerate(col_labels):
            if i < len(cells):
                text = re.sub(r'<[^>]+>', ' ', cells[i])
                text = text.replace('&nbsp;', ' ').replace('&#160;', ' ')
                text = re.sub(r'\[.*?\]', '', text)
                row[label] = re.sub(r'\s+', ' ', text).strip()
            else:
                row[label] = ''
        
        # Extract yes/no percentages
        yes_text = row.get('yes_or_result', '')
        m = re.search(r'(\d+\.?\d*)%', yes_text)
        row['yes_pct'] = float(m.group(1)) if m else None
        
        no_text = row.get('no', '')
        m = re.search(r'(\d+\.?\d*)%', no_text)
        row['no_pct'] = float(m.group(1)) if m else None
        
        # If no separate no column, try parsing yes column as combined result
        if row['no_pct'] is None:
            m = re.search(r'(\d+\.?\d*)%[–\-]\s*(\d+\.?\d*)%', yes_text)
            if m:
                row['yes_pct'] = float(m.group(1))
                row['no_pct'] = float(m.group(2))
        
        rows.append(row)
    return rows

def parse_2022_tables(tables, year):
    """Parse 2022 per-state tables: Measure|Type|Description|Result|Reference.
    Returns list of rows, each with state name pre-assigned."""
    rows = []
    
    # For each table, we need the state context. The 2022 page has
    # each table preceded by <h2 id="StateName">StateName</h2>
    # But we're receiving table HTML fragments without position context.
    # The tables are in page order, and the state sections follow the
    # same order as state_order. However, some states have multiple tables
    # (e.g., 1-row + multi-row). So we need to track the state per-table.
    #
    # Since we can't match directly here, we return them without state
    # and the caller will assign state based on the full HTML context.
    
    for table_html in tables:
        trs = re.findall(r'<tr>(.*?)</tr>', table_html, re.DOTALL)
        if not trs:
            continue
        
        headers = [re.sub(r'<[^>]+>', '', h).strip().lower() for h in 
                   re.findall(r'<th[^>]*>(.*?)</th>', trs[0], re.DOTALL)]
        
        if not any('result' in h for h in headers):
            continue
        
        for tr in trs[1:]:
            cells = re.findall(r'<t[dh][^>]*>(.*?)</t[dh]>', tr, re.DOTALL)
            if len(cells) < 2:
                continue
            
            clean = [re.sub(r'<[^>]+>', ' ', c).replace('&nbsp;', ' ').replace('&#160;', ' ')
                    .replace('\u2013', '-').replace('\u2014', '-') for c in cells]
            clean = [re.sub(r'\[.*?\]', '', c).strip() for c in clean]
            
            row = {'year': year,
                   'measure': clean[0] if len(clean) > 0 else '',
                   'origin': clean[1] if len(clean) > 1 else '',
                   'description': re.sub(r'\s+', ' ', clean[2]).strip() if len(clean) > 2 else '',
                   'result': clean[3] if len(clean) > 3 else '',
                   'yes_pct': None}
            rows.append(row)
    
    return rows

def parse_2020_earlier(html, year):
    """Parse 2020 and earlier formats (bullet lists, smaller tables)."""
    rows = []
    
    # Try using the old CSV data which we know works for 2022
    # For 2020/2018, Wikipedia uses different formats - try extracting from 
    # the page content
    
    # First: try to find any wikitable/sortable tables
    tables = re.findall(r'<table[^>]*class="[^"]*(?:wikitable|sortable)[^"]*"[^>]*>.*?</table>', html, re.DOTALL)
    
    if tables:
        for t in tables:
            trs = re.findall(r'<tr>(.*?)</tr>', t, re.DOTALL)
            if not trs:
                continue
            headers = [re.sub(r'<[^>]+>', '', h).strip().lower() for h in 
                       re.findall(r'<th[^>]*>(.*?)</th>', trs[0], re.DOTALL)]
            
            # Check if this looks like a ballot table
            if any(h in ' '.join(headers) for h in ['measure', 'description', 'result']):
                for tr in trs[1:]:
                    cells = re.findall(r'<t[dh][^>]*>(.*?)</t[dh]>', tr, re.DOTALL)
                    if len(cells) < 2:
                        continue
                    clean = [re.sub(r'<[^>]+>', ' ', c).replace('&nbsp;', ' ').replace('&#160;', ' ')
                            for c in cells]
                    clean = [re.sub(r'\[.*?\]', '', c).strip() for c in clean]
                    row = {'year': year, 'measure': clean[0] if len(clean) > 0 else '',
                           'description': clean[1] if len(clean) > 1 else '',
                           'result': clean[-1], 'yes_pct': None}
                    rows.append(row)
    
    return rows

def to_referendum(row):
    """Map parsed row → referendums schema."""
    year = row['year']
    state = row.get('state', '')
    
    if not state or state.lower() not in STATE_NAMES_SET:
        return None
    
    state_abbr = STATE_ABBR.get(state, '')
    measure_name = row.get('measure_name', '') or row.get('measure', '')
    description = row.get('description', '')
    yes_pct = row.get('yes_pct')
    no_pct = row.get('no_pct')
    
    # Determine outcome
    outcome_text = row.get('status', '') or row.get('result', '') or row.get('outcome', '')
    outcome_low = outcome_text.lower()
    
    if any(w in outcome_low for w in ['passed', 'approved', 'adopted']):
        passed = True
    elif any(w in outcome_low for w in ['failed', 'defeated', 'rejected']):
        passed = False
    elif yes_pct is not None:
        passed = yes_pct >= 50.0
    else:
        return None  # Can't determine from available data
    
    # If no percentages but we have outcome, use flags for 2022 format
    if yes_pct is None:
        return {
            'measure_id': f"{state_abbr}_{year}_{re.sub(r'[^a-zA-Z0-9]', '', measure_name)[:12] if measure_name else 'BM'}",
            'state': state_abbr, 'year': str(year),
            'election_date': f"{year}-11-08",
            'election_type': 'general',
            'measure_name': measure_name[:200],
            'wording': '', 'summary': description[:500],
            'topic': infer_topic(description, measure_name), 'subtopic': '',
            'passed': str(passed).upper(),
            'support_pct': '', 'oppose_pct': '', 'threshold': '', 'margin': '',
            'votes_for': '', 'votes_against': '', 'total_votes': '',
            'partisan_leans': '', 'campaign_contributions': '',
            'tags': f"{'passed' if passed else 'failed'};{year};{state_abbr}",
            'source_url': f"https://en.wikipedia.org/wiki/{year}_United_States_ballot_measures",
            'notes': f"Outcome: {outcome_text}. No vote percentages available.",
        }
    
    # 2024 format: has vote percentages
    no_pct_val = no_pct if no_pct is not None else round(100.0 - yes_pct, 2)
    threshold = 50.0
    margin = round(yes_pct - threshold, 2)
    
    clean_name = re.sub(r'[^a-zA-Z0-9]', '', measure_name)[:12] if measure_name else 'BM'
    measure_id = f"{state_abbr}_{year}_{clean_name}"
    
    # Election date
    date_str = row.get('date', '')
    election_date = ''
    if date_str:
        months_map = {'jan': '01', 'feb': '02', 'mar': '03', 'apr': '04', 'may': '05', 'jun': '06',
                      'jul': '07', 'aug': '08', 'sep': '09', 'oct': '10', 'nov': '11', 'dec': '12'}
        date_low = date_str.lower().strip()
        for abbr, num in months_map.items():
            if date_low.startswith(abbr):
                m = re.search(r'(\d+)', date_low)
                if m:
                    election_date = f"{year}-{num}-{int(m.group(1)):02d}"
                    break
    
    if not election_date:
        election_date = f"{year}-11-05"
    
    topic = infer_topic(description, measure_name)
    
    return {
        'measure_id': measure_id, 'state': state_abbr, 'year': str(year),
        'election_date': election_date, 'election_type': 'general',
        'measure_name': measure_name[:200],
        'wording': '', 'summary': description[:500],
        'topic': topic, 'subtopic': '',
        'passed': str(passed).upper(),
        'support_pct': f"{yes_pct:.2f}",
        'oppose_pct': f"{no_pct_val:.2f}",
        'threshold': f"{threshold:.1f}",
        'margin': f"{margin:.2f}",
        'votes_for': '', 'votes_against': '', 'total_votes': '',
        'partisan_leans': '', 'campaign_contributions': '',
        'tags': f"{topic};{year};{state_abbr};{'passed' if passed else 'failed'}",
        'source_url': f"https://en.wikipedia.org/wiki/{year}_United_States_ballot_measures",
        'notes': '',
    }

REF_FIELDS = [
    'measure_id', 'state', 'year', 'election_date', 'election_type',
    'measure_name', 'wording', 'summary', 'topic', 'subtopic',
    'passed', 'support_pct', 'oppose_pct', 'threshold', 'margin',
    'votes_for', 'votes_against', 'total_votes', 'partisan_leans',
    'campaign_contributions', 'tags', 'source_url', 'notes'
]

if __name__ == "__main__":
    years = [2024, 2022, 2020, 2018, 2016, 2014, 2012, 2010, 2008]
    all_refs = []
    seen_ids = set()
    
    for year in years:
        print(f"Scraping {year}... ", end='', flush=True)
        try:
            html = fetch_page(year)
            state_order = extract_state_sections(html)
            print(f"{len(state_order)} states found", end='', flush=True)
            
            if year == 2024:
                tables = re.findall(r'<table[^>]*class="[^"]*\bwikitable\b[^"]*"[^>]*>.*?</table>', html, re.DOTALL)
                raw_rows = []
                for t in tables:
                    raw_rows.extend(parse_2024_table(t, year))
            elif year == 2022:
                # For 2022, scan the full HTML to match each table to its state heading
                raw_rows = []
                # Find all wikitable tables with their positions in the page
                table_matches = list(re.finditer(
                    r'<table[^>]*class="[^"]*\bwikitable\b[^"]*"[^>]*>.*?</table>', html, re.DOTALL))
                
                # Find all state h2 positions
                state_positions = []
                for m in re.finditer(r'<h2[^>]*id="([A-Z][a-z]+(?:_[A-Z][a-z]+)*)">', html):
                    name = m.group(1).replace('_', ' ')
                    if name.lower() in STATE_NAMES_SET or name == 'District of Columbia':
                        state_positions.append((m.start(), name))
                
                # For each table, find its preceding state heading
                for table_match in table_matches:
                    table_pos = table_match.start()
                    table_html = table_match.group()
                    
                    # Find the state heading just before this table
                    state_for_table = ''
                    for sp, sn in reversed(state_positions):
                        if sp < table_pos:
                            state_for_table = sn
                            break
                    
                    if not state_for_table:
                        continue
                    
                    trs = re.findall(r'<tr>(.*?)</tr>', table_html, re.DOTALL)
                    if not trs:
                        continue
                    
                    headers = [re.sub(r'<[^>]+>', '', h).strip().lower() for h in 
                               re.findall(r'<th[^>]*>(.*?)</th>', trs[0], re.DOTALL)]
                    
                    if not any('result' in h for h in headers):
                        continue
                    
                    for tr in trs[1:]:
                        cells = re.findall(r'<t[dh][^>]*>(.*?)</t[dh]>', tr, re.DOTALL)
                        if len(cells) < 2:
                            continue
                        
                        clean = [re.sub(r'<[^>]+>', ' ', c).replace('&nbsp;', ' ').replace('&#160;', ' ')
                                .replace('\u2013', '-').replace('\u2014', '-') for c in cells]
                        clean = [re.sub(r'\[.*?\]', '', c).strip() for c in clean]
                        
                        row = {'year': year, 'state': state_for_table,
                               'measure': clean[0] if len(clean) > 0 else '',
                               'origin': clean[1] if len(clean) > 1 else '',
                               'description': re.sub(r'\s+', ' ', clean[2]).strip() if len(clean) > 2 else '',
                               'result': clean[3] if len(clean) > 3 else '',
                               'yes_pct': None}
                        raw_rows.append(row)
            else:
                raw_rows = parse_2020_earlier(html, year)
            
            print(f", {len(raw_rows)} raw rows", end='', flush=True)
            
            count = 0
            for r in raw_rows:
                ref = to_referendum(r)
                if ref and ref['measure_id'] not in seen_ids:
                    seen_ids.add(ref['measure_id'])
                    all_refs.append(ref)
                    count += 1
            
            print(f" → {count} new, {len(all_refs)} total")
            time.sleep(1.5)  # Rate limit
            
        except Exception as e:
            print(f"ERROR: {e}")
    
    print(f"\n=== RESULTS ===")
    print(f"Total measures: {len(all_refs)}")
    
    years_count = Counter(r['year'] for r in all_refs)
    print(f"By year: {dict(sorted(years_count.items()))}")
    
    topics = Counter(r['topic'] for r in all_refs)
    print(f"By topic: {dict(topics.most_common())}")
    
    # Write
    out_file = OUT / "referendums_new_wiki.csv"
    with open(out_file, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=REF_FIELDS)
        w.writeheader()
        w.writerows(all_refs)
    print(f"\nWritten: {out_file}")
