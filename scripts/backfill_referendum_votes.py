#!/usr/bin/env python3
"""
Backfill referendum vote data from Wikipedia HTML for 2020 and 2018.
Multi-strategy matching: direct, fuzzy, and position-based.
"""

import csv, re, urllib.request, time, shutil
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime

BASE = Path(__file__).parent.parent
PROCESSED = BASE / "data" / "processed"

HEADERS = {'User-Agent': 'USPoliticalMessaging/1.0 (research)'}

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

def fetch_page(year):
    url = f"https://en.wikipedia.org/wiki/{year}_United_States_ballot_measures"
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode('utf-8')

def parse_vote_cell(text):
    """Parse cell like '277,320 24.88%' → (votes, pct)."""
    text = text.replace('&nbsp;', ' ').replace('&#160;', ' ')
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    m = re.match(r'([\d,]+)\s+(\d+\.?\d*)%', text)
    if m:
        return int(m.group(1).replace(',', '')), float(m.group(2))
    m = re.match(r'(\d+\.?\d*)%', text)
    if m:
        return None, float(m.group(1))
    return None, None

def scrape_year(year):
    """Scrape 2020/2018 format: Origin|Status|Measure|Description|Date|Yes|No"""
    html = fetch_page(year)
    
    table_matches = list(re.finditer(
        r'<table[^>]*class="[^"]*\bwikitable\b[^"]*"[^>]*>.*?</table>', html, re.DOTALL))
    
    # Find h3 state headings (2020/2018 use h3, 2024 uses h2)
    state_positions = []
    for m in re.finditer(r'<h3[^>]*>(.*?)</h3>', html, re.DOTALL):
        inner = m.group(1)
        clean = re.sub(r'<[^>]+>', ' ', inner).strip()
        clean = re.sub(r'\s+', ' ', clean)
        if clean.lower() in STATE_NAMES_SET or clean == 'District of Columbia':
            state_positions.append((m.start(), clean))
    
    results = []
    for table_match in table_matches:
        table_pos = table_match.start()
        table_html = table_match.group()
        
        state_for_table = ''
        for sp, sn in reversed(state_positions):
            if sp < table_pos:
                state_for_table = sn
                break
        if not state_for_table:
            continue
        
        trs = re.findall(r'<tr>(.*?)</tr>', table_html, re.DOTALL)
        if len(trs) < 2:
            continue
        
        headers = [re.sub(r'<[^>]+>', '', h).strip().lower() for h in
                   re.findall(r'<th[^>]*>(.*?)</th>', trs[0], re.DOTALL)]
        
        is_yes_no_format = (len(headers) >= 7 and 'measure' in headers[2].lower() and 
                          any('yes' in h for h in headers))
        
        if not is_yes_no_format:
            continue
        
        for tr in trs[1:]:
            cells = re.findall(r'<t[dh][^>]*>(.*?)</t[dh]>', tr, re.DOTALL)
            if len(cells) < 7:
                continue
            
            clean = []
            for c in cells:
                c = re.sub(r'<[^>]+>', ' ', c).replace('&nbsp;', ' ').replace('&#160;', ' ')
                c = c.replace('\u2013', '-').replace('\u2014', '-')
                c = re.sub(r'\s+', ' ', c).strip()
                c = re.sub(r'\[.*?\]', '', c).strip()
                clean.append(c)
            
            measure_name = clean[2]
            description = clean[3]
            status = clean[1]
            
            yes_votes, yes_pct = parse_vote_cell(cells[5])
            no_votes, no_pct = parse_vote_cell(cells[6])
            if yes_pct is None and no_pct is None:
                continue
            
            outcome_low = status.lower()
            if any(w in outcome_low for w in ['passed', 'approved', 'adopted']):
                passed = True
            elif any(w in outcome_low for w in ['failed', 'defeated', 'rejected']):
                passed = False
            elif yes_pct is not None:
                passed = yes_pct >= 50.0
            else:
                passed = None
            
            no_pct_val = no_pct if no_pct is not None else round(100.0 - yes_pct, 2)
            threshold = 50.0
            margin = round(yes_pct - threshold, 2) if yes_pct is not None else None
            
            state_abbr = STATE_ABBR.get(state_for_table, '')
            
            results.append({
                'state': state_abbr,
                'year': str(year),
                'state_full': state_for_table,
                'measure_name_raw': measure_name,
                'description': description,
                'yes_pct': yes_pct,
                'no_pct': no_pct_val,
                'yes_votes': yes_votes,
                'no_votes': no_votes,
                'passed': passed,
                'status_text': status,
            })
    
    return results


def extract_measure_key(name):
    """Extract the core identifier from a measure name.
    'Amendment 1' → ('amendment', '1')
    'I-190' → ('i', '190') → also try ('initiative', '190')
    'LR-130' → ('lr', '130') → also try ('legislative referendum', '130')
    """
    n = name.lower().strip()
    n = re.sub(r'[^a-z0-9\s]', ' ', n)  # Replace hyphens with spaces
    n = re.sub(r'\s+', ' ', n).strip()
    
    # Pattern: type_word followed by identifier (may be at end of string)
    # The identifier can be digits, a letter, or an alphanumeric code
    # e.g. "initiative 190", "Amendment A", "Proposition 3", "I-190" → "i 190"
    m = re.search(r'(amendment|proposition|question|measure|initiative|issue|referendum|i|lr|ci|c|r)\s+(\S+)', n)
    if m:
        raw_type = m.group(1)
        ident = m.group(2)
        # Map abbreviations
        type_map = {
            'i': 'initiative', 'lr': 'legislative referendum', 
            'ci': 'initiative', 'c': 'constitutional amendment',
            'r': 'referendum',
        }
        mapped_type = type_map.get(raw_type, raw_type)
        return mapped_type, ident
    
    # If the name only has "initiative" or similar at the very end, try to find the number before it
    m = re.search(r'(\d+|[a-z])\s*(?:initiative|amendment|proposition|question|measure|issue|referendum)\s*$', n)
    if m:
        # Find which type word was used
        type_match = re.search(r'(initiative|amendment|proposition|question|measure|issue|referendum)\s*$', n)
        if type_match:
            return type_match.group(1), m.group(1)
    
    return None, None


def measure_keys_match(k1_type, k1_num, k2_type, k2_num):
    """Check if two measure keys match, handling aliases."""
    if k1_type == k2_type and k1_num == k2_num:
        return True
    
    # Type aliases
    type_aliases = {
        'amendment': ['amendment', 'constitutional amendment'],
        'proposition': ['proposition', 'prop', 'proposal'],
        'initiative': ['initiative', 'i', 'initiated measure'],
        'measure': ['measure', 'ballot measure'],
        'question': ['question', 'public question', 'constitutional convention question'],
        'referendum': ['referendum', 'r', 'legislative referendum'],
    }
    
    for canonical, aliases in type_aliases.items():
        if (k1_type in aliases or k1_type == canonical) and (k2_type in aliases or k2_type == canonical):
            if k1_num == k2_num:
                return True
    
    return False


def scrape_and_backfill(year):
    """Scrape Wikipedia and merge into referendums."""
    scraped = scrape_year(year)
    print(f"  {year}: {len(scraped)} measures found on Wikipedia")
    
    # Load current referendums
    path = PROCESSED / "referendums.csv"
    with open(path, newline='', encoding='utf-8') as f:
        current = list(csv.DictReader(f))
    
    backfilled = 0
    new_rows = 0
    
    # Group scraped by state
    scraped_by_state = defaultdict(list)
    for s in scraped:
        scraped_by_state[s['state']].append(s)
    
    # For each existing row, try to find a match
    for existing in current:
        if existing['year'] != str(year):
            continue
        
        st = existing['state']
        existing_name = existing.get('measure_name', '')
        
        # Skip if already has data
        if existing.get('support_pct', '').strip():
            continue
        
        wiki_measures = scraped_by_state.get(st, [])
        if not wiki_measures:
            continue
        
        # Strategy 1: extract key terms from existing measure name
        e_type, e_num = extract_measure_key(existing_name)
        
        best_match = None
        
        for wm in wiki_measures:
            w_type, w_num = extract_measure_key(wm['measure_name_raw'])
            
            if e_type and w_type and e_num and w_num:
                if measure_keys_match(e_type, e_num, w_type, w_num):
                    best_match = wm
                    break
        
        # Strategy 2: if no match by type, try matching by count within state
        if not best_match:
            # Group existing rows for this state that need backfill
            existing_for_state = [r for r in current if r['state'] == st and r['year'] == str(year) and not r.get('support_pct', '').strip()]
            if len(existing_for_state) == 1 and len(wiki_measures) == 1:
                best_match = wiki_measures[0]
        
        if best_match and best_match not in [None, False]:
            existing['support_pct'] = f"{best_match['yes_pct']:.2f}"
            existing['oppose_pct'] = f"{best_match['no_pct']:.2f}"
            existing['threshold'] = "50.0"
            existing['margin'] = f"{best_match['yes_pct'] - 50.0:.2f}"
            existing['passed'] = str(best_match['passed']).upper() if best_match['passed'] is not None else ''
            existing['votes_for'] = str(best_match['yes_votes']) if best_match['yes_votes'] else ''
            existing['votes_against'] = str(best_match['no_votes']) if best_match['no_votes'] else ''
            existing['notes'] = existing.get('notes', '') + f" Backfilled from Wikipedia ({best_match['measure_name_raw'][:80]})." if not existing.get('notes', '') else ''
            
            # Update measure_id if needed
            clean_id = re.sub(r'[^a-zA-Z0-9]', '', best_match['measure_name_raw'])[:12] if best_match['measure_name_raw'] else 'BM'
            existing['measure_id'] = f"{st}_{year}_{clean_id}"
            
            # Update other fields
            existing['summary'] = best_match['description'][:500]
            existing['election_date'] = f"{year}-11-05"
            existing['tags'] = f"{existing.get('topic', 'government')};{year};{st};{'passed' if best_match['passed'] else 'failed'}"
            
            backfilled += 1
            print(f"    ✓ {st}: '{existing_name}' → '{best_match['measure_name_raw'][:50]}' ({best_match['yes_pct']:.1f}%)")
            
            # Remove matched wiki measure from pool
            wiki_measures.remove(best_match)
    
    # Add any remaining unmatched wiki measures as new rows
    for st, wms in scraped_by_state.items():
        for wm in wms:
            existing_states = set(r['state'] for r in current if r['year'] == str(year))
            if st not in existing_states:
                # New state for this year — add it
                clean_id = re.sub(r'[^a-zA-Z0-9]', '', wm['measure_name_raw'])[:12] if wm['measure_name_raw'] else 'BM'
                measure_id = f"{st}_{year}_{clean_id}"
                
                topic_map = {
                    'abortion': ['abortion', 'fetal', 'reproductive'],
                    'taxes': ['tax', 'bond', 'levy'],
                    'voting_rights': ['voting', 'election', 'voter', 'ballot'],
                    'drugs': ['marijuana', 'cannabis', 'drug', 'psilocybin'],
                    'crime': ['crime', 'criminal', 'penalty', 'sentencing', 'prison'],
                    'guns': ['gun', 'firearm', 'weapon'],
                    'education': ['education', 'school', 'student', 'teacher'],
                    'healthcare': ['health', 'medicaid', 'hospital'],
                    'minimum_wage': ['minimum wage', 'wage', 'hourly', 'paid leave'],
                    'environment': ['environment', 'energy', 'conservation', 'wildlife', 'park', 'water'],
                    'civil_rights': ['civil rights', 'discrimination', 'equality', 'lgbt', 'marriage', 'slavery'],
                    'immigration': ['immigra', 'border', 'citizenship'],
                    'housing': ['housing', 'rent', 'homeless', 'zoning'],
                    'gambling': ['gambling', 'casino', 'lottery', 'betting'],
                    'government': ['government', 'legislature', 'constitutional', 'term limits', 'initiative', 'referendum'],
                }
                desc_lower = (wm['description'] + ' ' + wm['measure_name_raw']).lower()
                topic = 'government'
                for t, kws in topic_map.items():
                    if any(kw in desc_lower for kw in kws):
                        topic = t
                        break
                
                new_row = {
                    'measure_id': measure_id,
                    'state': st,
                    'year': str(year),
                    'election_date': f"{year}-11-05",
                    'election_type': 'general',
                    'measure_name': wm['measure_name_raw'][:200],
                    'wording': '',
                    'summary': wm['description'][:500],
                    'topic': topic,
                    'subtopic': '',
                    'passed': str(wm['passed']).upper() if wm['passed'] is not None else '',
                    'support_pct': f"{wm['yes_pct']:.2f}",
                    'oppose_pct': f"{wm['no_pct']:.2f}",
                    'threshold': "50.0",
                    'margin': f"{wm['yes_pct'] - 50.0:.2f}",
                    'votes_for': str(wm['yes_votes']) if wm['yes_votes'] else '',
                    'votes_against': str(wm['no_votes']) if wm['no_votes'] else '',
                    'total_votes': '',
                    'partisan_leans': '',
                    'campaign_contributions': '',
                    'tags': f"{topic};{year};{st};{'passed' if wm['passed'] else 'failed'}",
                    'source_url': f"https://en.wikipedia.org/wiki/{year}_United_States_ballot_measures",
                    'notes': '',
                }
                current.append(new_row)
                new_rows += 1
                print(f"    + NEW {st}: '{wm['measure_name_raw'][:50]}' ({wm['yes_pct']:.1f}%)")
    
    return current, backfilled, new_rows


def main():
    print("=" * 60)
    print("BACKFILL: Referendum Vote Data from Wikipedia")
    print("=" * 60)
    
    total_backfilled = 0
    total_new = 0
    
    for year in [2020, 2018]:
        print(f"\n--- {year} ---")
        try:
            current, backfilled, new_rows = scrape_and_backfill(year)
            total_backfilled += backfilled
            total_new += new_rows
            time.sleep(1.5)
            
            # Write after each year
            if backfilled > 0 or new_rows > 0:
                path = PROCESSED / "referendums.csv"
                
                # Backup
                ts = datetime.now().strftime('%Y%m%d_%H%M%S')
                shutil.copy(path, PROCESSED / f"referendums.csv.bak.{ts}")
                
                with open(path, 'w', newline='', encoding='utf-8') as f:
                    REF_FIELDS = [
                        'measure_id', 'state', 'year', 'election_date', 'election_type',
                        'measure_name', 'wording', 'summary', 'topic', 'subtopic',
                        'passed', 'support_pct', 'oppose_pct', 'threshold', 'margin',
                        'votes_for', 'votes_against', 'total_votes', 'partisan_leans',
                        'campaign_contributions', 'tags', 'source_url', 'notes'
                    ]
                    writer = csv.DictWriter(f, fieldnames=REF_FIELDS)
                    writer.writeheader()
                    writer.writerows(current)
        except Exception as e:
            import traceback
            print(f"  ERROR on {year}: {e}")
            traceback.print_exc()
    
    print(f"\n{'='*60}")
    print(f"Total backfilled: {total_backfilled}")
    print(f"Total new rows: {total_new}")
    
    # Final summary
    with open(PROCESSED / "referendums.csv", newline='', encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
    total = len(rows)
    support_missing = sum(1 for r in rows if not r.get('support_pct', '').strip())
    passed_missing = sum(1 for r in rows if not r.get('passed', '').strip())
    print(f"\nFinal state: {total} rows")
    print(f"Missing support_pct: {support_missing} ({support_missing/total*100:.1f}%)")
    print(f"Missing passed: {passed_missing} ({passed_missing/total*100:.1f}%)")
    years = Counter(r['year'] for r in rows)
    for year in sorted(years.keys()):
        yr = [r for r in rows if r['year'] == year]
        miss = sum(1 for r in yr if not r.get('support_pct', '').strip())
        print(f"  {year}: {len(yr)} rows, {miss} missing support_pct ({miss/len(yr)*100:.0f}%)")

if __name__ == "__main__":
    main()