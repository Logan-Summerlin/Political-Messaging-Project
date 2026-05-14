#!/usr/bin/env python3
"""
Normalize Wikipedia ballot measures (2008-2020) into referendums.csv schema.
v3: Fixed measure_name to strip state prefix, better IDs, added NV Question 6 context handling.
"""

import csv
import re
import os
import sys
from collections import defaultdict
from itertools import islice

# State name -> abbreviation mapping (sorted by name length desc for greedy matching)
STATE_NAME_TO_ABBR = dict(
    sorted([
        ('Alabama', 'AL'), ('Alaska', 'AK'), ('Arizona', 'AZ'), ('Arkansas', 'AR'),
        ('California', 'CA'), ('Colorado', 'CO'), ('Connecticut', 'CT'), ('Delaware', 'DE'),
        ('Florida', 'FL'), ('Georgia', 'GA'), ('Hawaii', 'HI'), ('Idaho', 'ID'),
        ('Illinois', 'IL'), ('Indiana', 'IN'), ('Iowa', 'IA'), ('Kansas', 'KS'),
        ('Kentucky', 'KY'), ('Louisiana', 'LA'), ('Maine', 'ME'), ('Maryland', 'MD'),
        ('Massachusetts', 'MA'), ('Michigan', 'MI'), ('Minnesota', 'MN'), ('Mississippi', 'MS'),
        ('Missouri', 'MO'), ('Montana', 'MT'), ('Nebraska', 'NE'), ('Nevada', 'NV'),
        ('New Hampshire', 'NH'), ('New Jersey', 'NJ'), ('New Mexico', 'NM'), ('New York', 'NY'),
        ('North Carolina', 'NC'), ('North Dakota', 'ND'), ('Ohio', 'OH'), ('Oklahoma', 'OK'),
        ('Oregon', 'OR'), ('Pennsylvania', 'PA'), ('Rhode Island', 'RI'), ('South Carolina', 'SC'),
        ('South Dakota', 'SD'), ('Tennessee', 'TN'), ('Texas', 'TX'), ('Utah', 'UT'),
        ('Vermont', 'VT'), ('Virginia', 'VA'), ('Washington', 'WA'), ('West Virginia', 'WV'),
        ('Wisconsin', 'WI'), ('Wyoming', 'WY'),
    ], key=lambda x: -len(x[0]))
)

STATE_ABBREVS = set(STATE_NAME_TO_ABBR.values())

# Topic keywords
TOPIC_KEYWORDS = {
    'abortion': ['abortion', 'reproductive', 'pro-life', 'pro-choice', 'fetal', 'unborn'],
    'drugs': ['marijuana', 'cannabis', 'recreational marijuana', 'medical marijuana', 'opioid'],
    'minimum_wage': ['minimum wage', 'hourly wage', 'living wage', 'increase the minimum wage', '$15', '$11', '$12'],
    'voting_rights': ['voter id', 'voter registration', 'redistricting', 'gerrymandering', 'absentee voting', 
                      'campaign contribution', 'campaign finance', 'non-citizen voting', 'felon voting',
                      'top-two', 'top-four', 'top-five', 'partisan primary', 'photo id', 'photo identification',
                      'identification to vote', 'voting'],
    'civil_rights': ['same-sex marriage', 'gay marriage', 'marriage license', 'affirmative action',
                     'non-discrimination', 'civil union', 'lgbt', 'marriage'],
    'guns': ['gun', 'firearm', 'background check', 'assault weapon', 'second amendment', 'weapon'],
    'healthcare': ['healthcare', 'health care', 'medicaid', 'medicare', 'health insurance', 
                   'mental health', 'hospital', 'homeless', 'medical treatment'],
    'education': ['education', 'school', 'teacher', 'student', 'college', 'university', 
                  'scholarship', 'tuition', 'vocational', 'public school', 'lottery fund'],
    'environment': ['renewable energy', 'solar', 'wind', 'environment', 'conservation', 
                    'clean energy', 'climate', 'emission', 'coastal protection', 'renewable'],
    'taxes': ['sales tax', 'property tax', 'income tax', 'tax exemption', 'tax increase', 
              'tax cut', 'tax credit', 'bond', 'bond measure', 'taxpayer', 'levy', 'revenue'],
    'crime': ['felony', 'prison', 'sentencing', 'parole', 'death penalty', 'capital punishment',
              'police', 'law enforcement', 'criminal', 'offender', 'rehabilitation', 'incarceration'],
    'government': ['term limit', 'legislature', 'legislative', 'judicial', 'judge', 'pension',
                   'retirement', 'recall', 'ethics', 'transparency', 'salary', 'compensation',
                   'daylight saving', 'lockbox', 'budget', 'governor recall'],
    'gambling': ['casino', 'gambling', 'lottery', 'betting', 'dog racing', 'horse racing', 'parimutuel'],
    'labor': ['union', 'collective bargaining', 'right to work', 'paid sick leave'],
    'housing': ['housing', 'rent', 'rental', 'landlord', 'tenant', 'zoning', 'property'],
    'immigration': ['sanctuary', 'immigrant', 'immigration', 'alien', 'border'],
    'transportation': ['transportation', 'transit', 'highway', 'road', 'bridge', 'rail'],
    'animals': ['animal', 'animal cruelty', 'puppy', 'livestock', 'factory farm'],
    'alcohol': ['alcohol', 'liquor', 'beer', 'wine', 'drinking'],
}

TOPIC_PRIORITY = [
    'abortion', 'guns', 'drugs', 'minimum_wage', 'voting_rights', 'civil_rights',
    'healthcare', 'education', 'environment', 'taxes', 'crime', 'government',
    'housing', 'gambling', 'labor', 'immigration', 'transportation', 'animals', 'alcohol'
]


def strip_type_prefix(text):
    t = text
    t = re.sub(
        r'^(Legislatively-referred|Citizen-initiated|Initiated|Indirect initiated|Indirect)\s+'
        r'(constitutional\s+)?(amendment|state\s+statute|bond\s+act|state\s+statue)\s*:\s*'
        r'(?:\d{4}\s+)?',
        '', t, flags=re.IGNORECASE
    )
    return t


def strip_state_from_name(name, state):
    """Remove state name prefix from a measure name like 'California Proposition 14' -> 'Proposition 14'"""
    for state_name, abbr in STATE_NAME_TO_ABBR.items():
        if abbr == state:
            # Remove "StateName " prefix (e.g., "California Proposition 14" -> "Proposition 14")
            pattern = r'^' + re.escape(state_name) + r'\s+'
            name = re.sub(pattern, '', name)
            break
    return name


def find_state_in_text(text):
    """Extract state abbreviation from text."""
    if not text:
        return None
    
    for state_name, abbr in STATE_NAME_TO_ABBR.items():
        if re.search(r'\b' + re.escape(state_name) + r'\b', text):
            return abbr
    
    for abbr in STATE_ABBREVS:
        if re.search(r'\b(' + re.escape(abbr) + r')\s+(Proposition|Amendment|Question|Measure|Initiative|Issue|Ballot|State\s+Question|Public\s+Question)', text):
            return abbr
        if re.search(r'(in|of|for)\s+' + re.escape(abbr) + r'\b', text, re.IGNORECASE):
            return abbr
    
    m = re.search(r',\s*([A-Z]{2})\b', text)
    if m and m.group(1) in STATE_ABBREVS:
        return m.group(1)
    
    m = re.search(r'\(([A-Z]{2})\)', text)
    if m and m.group(1) in STATE_ABBREVS:
        return m.group(1)
    
    return None


def extract_state(measure_name, full_text, year):
    state = find_state_in_text(measure_name)
    if state:
        return state
    state = find_state_in_text(full_text)
    if state:
        return state
    if 'County' in measure_name or 'County' in full_text:
        if 'Los Angeles' in measure_name or 'Los Angeles' in full_text:
            return 'CA'
    return None


def determine_outcome(measure_name, full_text, outcome_field):
    outcome = outcome_field.strip().lower() if outcome_field else ''
    if outcome in ('passed', 'pass', 'yes'):
        return 'TRUE'
    elif outcome in ('failed', 'fail', 'no'):
        return 'FALSE'
    ft_lower = full_text.lower()
    if re.search(r'\bpassed\b', ft_lower):
        return 'TRUE'
    if re.search(r'\bfailed\b', ft_lower):
        return 'FALSE'
    if re.search(r'this (measure|amendment|proposition|initiative)\s+passed', ft_lower):
        return 'TRUE'
    if re.search(r'this (measure|amendment|proposition|initiative)\s+failed', ft_lower):
        return 'FALSE'
    return None


def infer_topic(measure_name, full_text):
    text = strip_type_prefix(measure_name + ' ' + full_text).lower()
    text = re.sub(r'^\d{4}\s+', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    scores = {}
    for topic, keywords in TOPIC_KEYWORDS.items():
        score = sum(text.count(kw.lower()) for kw in keywords)
        if score > 0:
            scores[topic] = score
    if not scores:
        return 'government'
    max_score = max(scores.values())
    top_topics = [t for t, s in scores.items() if s == max_score]
    if len(top_topics) == 1:
        return top_topics[0]
    for t in TOPIC_PRIORITY:
        if t in top_topics:
            return t
    return top_topics[0]


def clean_measure_name(measure_name, state):
    """Clean up measure_name: strip type prefixes, year, and state name."""
    text = measure_name.strip()
    text = strip_type_prefix(text)
    text = re.sub(r'^\d{4}\s+', '', text)
    text = re.sub(r'\s*\[\s*\d+\s*\]', '', text)
    text = re.sub(r'\s*\.\s*This\s+(measure|amendment|proposition|initiative)\s+(passed|failed)\..*$', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\s+', ' ', text).strip().rstrip(',').strip()
    text = strip_state_from_name(text, state)
    return text


def extract_summary(measure_name, full_text, state):
    """Extract meaningful summary."""
    ft_clean = full_text.strip()
    ft_clean = strip_type_prefix(ft_clean)
    ft_clean = re.sub(r'^\d{4}\s+', '', ft_clean)
    
    # Remove state prefix from summary too
    ft_clean = strip_state_from_name(ft_clean, state)
    
    ft_clean = re.sub(r'\s*\.\s*This\s+(measure|amendment|proposition|initiative)\s+(passed|failed|Passed|Failed)\s*\..*$', '', ft_clean)
    ft_clean = re.sub(r'\s*\[\s*\d+\s*\]', '', ft_clean)
    ft_clean = re.sub(r'\s+', ' ', ft_clean).strip().rstrip(',').strip()
    return ft_clean


def get_measure_id_short(measure_name):
    """Extract short identifier from measure name for use in measure_id."""
    short = measure_name.strip()
    short = re.sub(r'^(Proposition|Amendment|Question|Measure|Initiative|Issue|Public Question|Ballot Measure|State Question)\s+', '', short)
    short = re.sub(r'\s*\[\s*\d+\s*\]', '', short)
    # Take only alphanumeric characters
    short = re.sub(r'[^a-zA-Z0-9]', '', short)
    if not short:
        short = 'M'
    return short[:12]


def is_summary_row(measure_name):
    patterns = [
        r'\d+\s+ballot measures?\s+(were|was|were balloted)',
        r'ballot measures?\s+in\s+the\s+United\s+States',
        r'ballot measures?\s+were\s+balloted',
        r'^One measure was balloted',
        r'^Two measures were balloted',
        r'^\d+ ballot measures were balloted',
    ]
    return any(re.search(p, measure_name, re.IGNORECASE) for p in patterns)


def normalize_for_dedup(name):
    n = name.lower().strip()
    n = re.sub(r'\s*\[\s*\d+\s*\]', '', n)
    n = re.sub(r'^\d{4}\s+', '', n)
    n = strip_type_prefix(n)
    n = re.sub(r'[,\s]+', ' ', n).strip()
    n = re.sub(r'\s*\.\s*(this\s+(measure|amendment|proposition|initiative)\s+(passed|failed).*)?$', '', n)
    return n


def get_measure_numbers(name):
    return set(re.findall(r'\b(\d+|[A-Z])\b', name))


class StateContextTracker:
    """Track state context across rows for rows where state isn't explicitly mentioned."""
    def __init__(self):
        self.last_state_by_year = {}
    
    def get_context_state(self, year, measure_name, full_text):
        """Get the likely state based on context from previous rows."""
        return self.last_state_by_year.get(year)
    
    def set_context_state(self, year, state):
        if state:
            self.last_state_by_year[year] = state


def main():
    base_dir = '/home/agentbot/workspace/us-political-messaging-dataset'
    input_path = os.path.join(base_dir, 'data/raw/wikipedia_ballot_measures_complete.csv')
    existing_path = os.path.join(base_dir, 'data/processed/referendums.csv')
    backup_path = os.path.join(base_dir, 'data/processed/referendums.csv.bak')
    output_path = os.path.join(base_dir, 'data/processed/ballot_2008_2020_normalized.csv')
    
    # Backup existing
    if os.path.exists(existing_path):
        import shutil
        shutil.copy2(existing_path, backup_path)
        print(f"Backed up: referendums.csv → referendums.csv.bak")
    
    # Build existing records index
    existing_ids = set()
    existing_norm_map = defaultdict(set)  # (state, year) -> set of normalized names
    
    if os.path.exists(existing_path):
        with open(existing_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                mid = row['measure_id'].strip()
                state = row['state'].strip()
                year = row['year'].strip()
                mn = row['measure_name'].strip()
                existing_ids.add(mid)
                
                mn_norm = normalize_for_dedup(mn)
                existing_norm_map[(state, year)].add(mn_norm)
                # Also index by numbers
                nums = get_measure_numbers(mn_norm)
                existing_norm_map[(state, year, '__nums__')].add(frozenset(nums))
    
    print(f"Loaded {len(existing_ids)} existing measure_ids")
    
    # Read all Wikipedia rows first (for context-based state inference)
    all_wiki_rows = []
    with open(input_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            all_wiki_rows.append(row)
    
    # Pre-compute state context: scan rows sequentially, tracking the most recent
    # state seen for each year as we go
    last_state_by_year = {}
    row_state_hints = [None] * len(all_wiki_rows)
    for i, row in enumerate(all_wiki_rows):
        yr = row['year'].strip()
        mn = row['measure_name'].strip()
        ft = row['full_text'].strip()
        state = extract_state(mn, ft, yr)
        if state:
            last_state_by_year[yr] = state
        row_state_hints[i] = last_state_by_year.get(yr)
    
    # Process rows with sequential context tracking
    new_rows = []
    summary_count = 0
    dup_count = 0
    skip_state_count = 0
    context_state_count = 0
    
    current_state_by_year = {}
    
    for i, row in enumerate(all_wiki_rows):
        year = row['year'].strip()
        measure_name = row['measure_name'].strip()
        outcome_field = row['outcome'].strip() if row.get('outcome') else ''
        full_text = row['full_text'].strip() if row.get('full_text') else ''
        
        if not year or not measure_name:
            continue
        
        if is_summary_row(measure_name):
            summary_count += 1
            continue
        
        # Extract state - first check explicit, then context
        state = extract_state(measure_name, full_text, year)
        if state:
            current_state_by_year[year] = state
        else:
            # Use context: last known state for this year
            state = current_state_by_year.get(year)
            if state:
                context_state_count += 1
        
        if not state:
            skip_state_count += 1
            continue
        
        # Clean up measure name (without state prefix)
        display_name = clean_measure_name(measure_name, state)
        if not display_name:
            display_name = measure_name.strip()
        
        # Dedup check
        mn_norm = normalize_for_dedup(display_name)
        nums_new = get_measure_numbers(mn_norm)
        
        is_duplicate = False
        existing_in_year_state = existing_norm_map.get((state, year), set())
        
        if mn_norm in existing_in_year_state:
            is_duplicate = True
        
        if not is_duplicate and nums_new:
            existing_nums = existing_norm_map.get((state, year, '__nums__'), set())
            if frozenset(nums_new) in existing_nums:
                # Double-check: does an existing name share this set?
                for ex_name in existing_in_year_state:
                    if get_measure_numbers(ex_name) == nums_new:
                        is_duplicate = True
                        break
        
        if not is_duplicate:
            for ex_name in existing_in_year_state:
                if mn_norm in ex_name or ex_name in mn_norm:
                    is_duplicate = True
                    break
        
        if is_duplicate:
            dup_count += 1
            continue
        
        # Determine outcome
        passed = determine_outcome(measure_name, full_text, outcome_field)
        
        # Infer topic
        topic = infer_topic(measure_name, full_text)
        
        # Extract summary
        summary = extract_summary(measure_name, full_text, state)
        
        # Create measure_id
        short = get_measure_id_short(display_name)
        base_id = f"{state}_{year}_{short}"
        mid = base_id
        counter = 2
        while mid in existing_ids:
            mid = f"{state}_{year}_{short}{counter}"
            counter += 1
        existing_ids.add(mid)
        
        # Determine election date
        election_date = f"{year}-11-03"
        text_lower = (measure_name + ' ' + full_text).lower()
        if 'june' in text_lower:
            election_date = f"{year}-06-30"
        elif 'july' in text_lower:
            election_date = f"{year}-07-14"
        elif 'august' in text_lower or 'aug' in text_lower:
            election_date = f"{year}-08-06"
        
        # Build tags
        tags_parts = [topic, year, state]
        if passed == 'TRUE':
            tags_parts.append('passed')
        elif passed == 'FALSE':
            tags_parts.append('failed')
        else:
            tags_parts.append('unknown')
        tags = ';'.join(tags_parts)
        
        source_url = f"https://en.wikipedia.org/wiki/{year}_United_States_ballot_measures"
        
        notes_parts = []
        if passed is None:
            notes_parts.append("Outcome: unknown.")
        notes_parts.append("No vote percentages available.")
        if not full_text or full_text.strip() == measure_name.strip():
            notes_parts.append("No description available.")
        notes = ' '.join(notes_parts)
        
        normalized = {
            'measure_id': mid,
            'state': state,
            'year': year,
            'election_date': election_date,
            'election_type': 'general',
            'measure_name': display_name,
            'wording': '',
            'summary': summary,
            'topic': topic,
            'subtopic': '',
            'passed': passed if passed else '',
            'support_pct': '',
            'oppose_pct': '',
            'threshold': '50.0',
            'margin': '',
            'votes_for': '',
            'votes_against': '',
            'total_votes': '',
            'partisan_leans': '',
            'campaign_contributions': '',
            'tags': tags,
            'source_url': source_url,
            'notes': notes,
        }
        
        new_rows.append(normalized)
    
    print(f"\nResults:")
    print(f"  Summary rows skipped: {summary_count}")
    print(f"  Duplicates: {dup_count}")
    print(f"  No state found: {skip_state_count}")
    print(f"  Context-inferred state: {context_state_count}")
    print(f"  NEW rows: {len(new_rows)}")
    
    # Write output
    fieldnames = [
        'measure_id', 'state', 'year', 'election_date', 'election_type',
        'measure_name', 'wording', 'summary', 'topic', 'subtopic',
        'passed', 'support_pct', 'oppose_pct', 'threshold', 'margin',
        'votes_for', 'votes_against', 'total_votes', 'partisan_leans',
        'campaign_contributions', 'tags', 'source_url', 'notes'
    ]
    
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in new_rows:
            writer.writerow(row)
    
    print(f"\nOutput: {os.path.basename(output_path)} ({len(new_rows)} rows)")
    
    # Summary
    year_counts = defaultdict(int)
    state_counts = defaultdict(int)
    for row in new_rows:
        year_counts[row['year']] += 1
        state_counts[row['state']] += 1
    
    print("\nNew rows by year:")
    for y in sorted(year_counts):
        print(f"  {y}: {year_counts[y]}")
    
    print("\nNew rows by state (top 10):")
    for s in sorted(state_counts, key=lambda x: -state_counts[x])[:10]:
        print(f"  {s}: {state_counts[s]}")
    
    desc_rows = [r for r in new_rows if len(r['summary']) > 40 and r['summary'] != r['measure_name']]
    print(f"\nRows with enriched descriptions ({len(desc_rows)}):")
    for r in desc_rows:
        print(f"  [{r['year']}] {r['state']} | {r['measure_name'][:50]:50s} | {r['topic']:15s} | passed={r['passed']:5s} | {r['summary'][:80]}")


if __name__ == '__main__':
    main()
