#!/usr/bin/env python3
"""
Build the Gallup MIP extracted CSV from raw Datawrapper CSV files.

Schema: poll_id, source, source_url, date, question_type, question_wording,
        topic, issue_area, support_pct, oppose_pct, net, sample_size,
        methodology, population, moe, tags
"""

import csv
import os
import re
from datetime import datetime

RAW_DIR = "/home/agentbot/workspace/us-political-messaging-dataset/data/raw/gallup"
OUTPUT_FILE = os.path.join(RAW_DIR, "gallup_mip_extracted.csv")

SOURCE = "Gallup"
SOURCE_URL = "https://news.gallup.com/poll/1675/most-important-problem.aspx"
QUESTION_WORDING = "What do you think is the most important problem facing this country today? [Open-ended]"
SAMPLE_SIZE = 1000
METHODOLOGY = "phone"
POPULATION = "adults"
MOE = 4.0

# Standardized topic mappings
TOPIC_MAP = {
    "ECONOMIC PROBLEMS (NET)": "economy",
    "Economy in general": "economy",
    "High cost of living/Inflation": "economy",
    "Inflation": "economy",
    "Foreign Trade/Trade deficit": "economy",
    "Federal budget deficit/Federal debt": "economy",
    "Unemployment/Jobs": "economy",
    "Lack of money": "economy",
    "Gap between rich and poor": "economy",
    "Taxes": "economy",
    "Wage issues": "economy",
    "Fuel/Oil prices": "economy",
    "Corporate corruption": "economy",
    "Recession": "economy",
    "NON-ECONOMIC PROBLEMS (NET)": "government",
    "The government/Poor leadership": "government",
    "Immigration": "immigration",
    "Race relations/Racism": "race",
    "Unifying the country": "government",
    "Judicial system/Courts/Laws": "government",
    "Abortion": "abortion",
    "Crime/Violence": "crime",
    "Environment/Pollution/Climate change": "climate",
    "Poverty/Hunger/Homelessness": "economy",
    "Ethics/moral/religious/family decline": "society",
    "Education": "education",
    "Guns/Gun control": "guns",
    "Healthcare": "healthcare",
    "Lack of respect for each other": "society",
    "Elections/Election reform/Democracy": "government",
    "Elections/Election reform": "government",
    "School shootings": "guns",
    "Energy/Lack of energy sources": "energy",
    "Coronavirus/Diseases": "healthcare",
    "The media": "government",
    "Drugs": "crime",
    "National security": "foreign_policy",
    "Foreign policy/Foreign aid/Focus overseas": "foreign_policy",
    "Situation with Russia": "foreign_policy",
    "Situation with China": "foreign_policy",
    "Lack of military defense": "foreign_policy",
    "Care for the elderly/Medicare": "healthcare",
    "Welfare": "economy",
    "Wars/War (nonspecific)/Fear of war": "foreign_policy",
    "International issues, problems ": "foreign_policy",
    "International issues, problems": "foreign_policy",
    "Terrorism": "foreign_policy",
    "Infrastructure": "economy",
    "Police brutality": "crime",
    "Children's behavior/Way they are raised": "society",
    "Children's behavior/The way they are raised": "society",
    "Children's needs": "society",
    "Situation in Afghanistan": "foreign_policy",
    "Advancement of computers/technology": "technology",
    "Social Security": "economy",
    "Cancer/diseases/viruses": "healthcare",
    "LGBTQ rights": "society",
    "War in the Middle East": "foreign_policy",
    "Natural disaster response": "government",
    "Other non-economic": "other",
    "No opinion": "other",
}

ISSUE_AREA_MAP = {
    "ECONOMIC PROBLEMS (NET)": "economy_general",
    "Economy in general": "economy_general",
    "High cost of living/Inflation": "inflation",
    "Inflation": "inflation",
    "Foreign Trade/Trade deficit": "trade",
    "Federal budget deficit/Federal debt": "budget_deficit",
    "Unemployment/Jobs": "unemployment",
    "Lack of money": "poverty",
    "Gap between rich and poor": "inequality",
    "Taxes": "taxes",
    "Wage issues": "wages",
    "Fuel/Oil prices": "energy_prices",
    "Corporate corruption": "corruption",
    "Recession": "recession",
    "NON-ECONOMIC PROBLEMS (NET)": "government_general",
    "The government/Poor leadership": "government_leadership",
    "Immigration": "immigration_general",
    "Race relations/Racism": "race_relations",
    "Unifying the country": "national_unity",
    "Judicial system/Courts/Laws": "judicial_system",
    "Abortion": "abortion_general",
    "Crime/Violence": "crime_violence",
    "Environment/Pollution/Climate change": "climate_change",
    "Poverty/Hunger/Homelessness": "poverty_homelessness",
    "Ethics/moral/religious/family decline": "moral_decline",
    "Education": "education_general",
    "Guns/Gun control": "gun_control",
    "Healthcare": "healthcare_general",
    "Lack of respect for each other": "social_respect",
    "Elections/Election reform/Democracy": "election_reform",
    "Elections/Election reform": "election_reform",
    "School shootings": "school_shootings",
    "Energy/Lack of energy sources": "energy_sources",
    "Coronavirus/Diseases": "coronavirus",
    "The media": "media",
    "Drugs": "drugs",
    "National security": "national_security",
    "Foreign policy/Foreign aid/Focus overseas": "foreign_policy",
    "Situation with Russia": "russia",
    "Situation with China": "china",
    "Lack of military defense": "military_defense",
    "Care for the elderly/Medicare": "elderly_care",
    "Welfare": "welfare",
    "Wars/War (nonspecific)/Fear of war": "war_fear",
    "International issues, problems ": "international_issues",
    "International issues, problems": "international_issues",
    "Terrorism": "terrorism",
    "Infrastructure": "infrastructure",
    "Police brutality": "police_brutality",
    "Children's behavior/Way they are raised": "children_behavior",
    "Children's behavior/The way they are raised": "children_behavior",
    "Children's needs": "children_needs",
    "Situation in Afghanistan": "afghanistan",
    "Advancement of computers/technology": "technology_advancement",
    "Social Security": "social_security",
    "Cancer/diseases/viruses": "diseases",
    "LGBTQ rights": "lgbtq_rights",
    "War in the Middle East": "middle_east_war",
    "Natural disaster response": "natural_disasters",
    "Other non-economic": "other",
    "No opinion": "no_opinion",
}


def parse_month_year(text):
    """Parse various month/year formats to YYYY-MM-DD (first of month)."""
    text = text.strip().replace("'", "")
    # Handle formats like "Aug 2022", "Jan-2023", "23-Nov", "25-May", "Nov/Dec-2022"
    
    # "Nov/Dec-2022" -> use Nov
    if "/" in text and "-" in text:
        parts = text.split("/")
        text = parts[0] + text.split("-")[-1] if "-" in text else parts[0]
    
    # Format: "25-May" or "23-Nov" (YY-Mon)
    m = re.match(r'^(\d{2})-([A-Za-z]{3})$', text)
    if m:
        year = int(m.group(1)) + 2000
        month_abbr = m.group(2)
        return f"{year}-{month_number(month_abbr):02d}-01"
    
    # Format: "Feb-2023" (Mon-YYYY)
    m = re.match(r'^([A-Za-z]{3})-(\d{4})$', text)
    if m:
        return f"{m.group(2)}-{month_number(m.group(1)):02d}-01"
    
    # Format: "Aug 2022" (Mon YYYY)
    m = re.match(r'^([A-Za-z]{3,9})\s+(\d{4})$', text)
    if m:
        return f"{m.group(2)}-{month_number(m.group(1)):02d}-01"
    
    # Format: "Jan 1 2001" (Mon DD YYYY) - from economy mentions
    m = re.match(r'^([A-Za-z]{3,9})\s+(\d{1,2})\s+(\d{4})$', text)
    if m:
        month = month_number(m.group(1))
        day = int(m.group(2))
        year = int(m.group(3))
        return f"{year}-{month:02d}-{day:02d}"
    
    # Try a generic approach for "Nov/Dec-2022"
    m = re.match(r'^([A-Za-z]+)/([A-Za-z]+)-(\d{4})$', text)
    if m:
        return f"{m.group(3)}-{month_number(m.group(1)):02d}-01"
    
    return None


MONTHS = {
    'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,
    'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12,
    'january': 1, 'february': 2, 'march': 3, 'april': 4, 'june': 6,
    'july': 7, 'august': 8, 'september': 9, 'october': 10, 'november': 11, 'december': 12
}

def month_number(abbr):
    return MONTHS.get(abbr.lower()[:3], 1)


def parse_support(val):
    """Parse support percentage value."""
    val = val.strip().replace('%', '').replace(',', '').strip()
    if val in ('', '*', '--', '-'):
        return None
    try:
        f = float(val)
        if f > 100:
            return None  # totals
        return f
    except ValueError:
        return None


def process_mip_table(filepath):
    """Process a single MIP table CSV and return rows."""
    rows = []
    base_name = os.path.basename(filepath)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.strip().split('\n')
    if len(lines) < 2:
        return rows
    
    # Parse header
    header = lines[0].split(',')
    if len(header) < 2:
        return rows
    
    # Extract month columns from header (skip first column which is issue name)
    month_cols = []
    for col in header[1:]:
        col = col.strip().strip('"')
        if col and col != '%':
            parsed = parse_month_year(col)
            if parsed:
                month_cols.append(parsed)
    
    if not month_cols:
        return rows
    
    # Process data rows
    for line in lines[2:]:  # skip header and % row
        if not line.strip():
            continue
        parts = line.split(',')
        if len(parts) < 2:
            continue
        
        issue = parts[0].strip().strip('"').replace('<b>', '').replace('</b>', '').strip()
        
        # Skip totals rows
        if issue == 'Total' or issue.startswith('Total'):
            continue
        
        topic = TOPIC_MAP.get(issue, 'other')
        issue_area = ISSUE_AREA_MAP.get(issue, 'other')
        
        # Determine the month range from this version
        for i, date_str in enumerate(month_cols):
            if i + 1 < len(parts):
                val = parts[i + 1].strip().strip('"')
                support = parse_support(val)
                if support is not None:
                    rows.append({
                        'date': date_str,
                        'topic': topic,
                        'issue_area': issue_area,
                        'issue_name': issue,
                        'support_pct': support,
                    })
    
    return rows


def process_economy_mentions(filepath):
    """Process economy mentions data."""
    rows = []
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.strip().split('\n')
    for line in lines[1:]:  # skip header
        if not line.strip():
            continue
        parts = line.split(',')
        if len(parts) < 2:
            continue
        
        date_str = parts[0].strip()
        date = parse_month_year(date_str)
        if not date:
            continue
        
        support = parse_support(parts[1].strip())
        if support is not None:
            rows.append({
                'date': date,
                'topic': 'economy',
                'issue_area': 'economy_general',
                'issue_name': 'Economy in general',
                'support_pct': support,
            })
    
    return rows


def main():
    all_rows = []
    poll_counter = {}
    
    # Process economy mentions (monthly, 2001-2026)
    economy_file = os.path.join(RAW_DIR, "economy_mentions_mip.csv")
    if os.path.exists(economy_file):
        rows = process_economy_mentions(economy_file)
        print(f"Economy mentions: {len(rows)} rows")
        all_rows.extend(rows)
    
    # Process MIP table versions (detailed breakdowns)
    for ver in [2, 3, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 66]:
        filepath = os.path.join(RAW_DIR, f"mip_table_v{ver}.csv")
        if os.path.exists(filepath):
            rows = process_mip_table(filepath)
            print(f"MIP table v{ver}: {len(rows)} rows")
            all_rows.extend(rows)
    
    # Deduplicate by (date, issue_area, support_pct)
    seen = set()
    deduped = []
    for row in all_rows:
        key = (row['date'], row['issue_area'], row['support_pct'])
        if key not in seen:
            seen.add(key)
            deduped.append(row)
    
    print(f"\nTotal rows after dedup: {len(deduped)}")
    
    # Sort by date
    deduped.sort(key=lambda r: r['date'])
    
    # Write output CSV
    fieldnames = [
        'poll_id', 'source', 'source_url', 'date', 'question_type',
        'question_wording', 'topic', 'issue_area', 'support_pct',
        'oppose_pct', 'net', 'sample_size', 'methodology', 'population',
        'moe', 'tags'
    ]
    
    with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for i, row in enumerate(deduped):
            # Generate poll_id
            date_clean = row['date'].replace('-', '')
            poll_id = f"GALLUP_{date_clean}_{i+1:03d}"
            
            tags = f"most_important_problem;{row['topic']};{row['issue_area']}"
            
            writer.writerow({
                'poll_id': poll_id,
                'source': SOURCE,
                'source_url': SOURCE_URL,
                'date': row['date'],
                'question_type': 'most_important_problem',
                'question_wording': QUESTION_WORDING,
                'topic': row['topic'],
                'issue_area': row['issue_area'],
                'support_pct': row['support_pct'],
                'oppose_pct': '',
                'net': '',
                'sample_size': SAMPLE_SIZE,
                'methodology': METHODOLOGY,
                'population': POPULATION,
                'moe': MOE,
                'tags': tags,
            })
    
    print(f"\nWritten to: {OUTPUT_FILE}")
    
    # Print some stats
    dates = set(r['date'] for r in deduped)
    print(f"Date range: {min(dates)} to {max(dates)}")
    print(f"Unique dates: {len(dates)}")
    
    topics = set(r['topic'] for r in deduped)
    print(f"Topics: {sorted(topics)}")
    
    # Count by year
    years = {}
    for r in deduped:
        y = r['date'][:4]
        years[y] = years.get(y, 0) + 1
    for y in sorted(years.keys()):
        print(f"  {y}: {years[y]} rows")


if __name__ == "__main__":
    main()
