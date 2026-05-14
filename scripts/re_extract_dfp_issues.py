#!/usr/bin/env python3
"""
Re-extract DFP polling findings from raw chunk markdown.
Properly extracts narrative findings with context and corrected percentage handling.

Key improvements over original extraction:
1. Skips demographic percentages (age/race/gender breakdowns) as support_pct
2. Uses article title as topic context
3. Classifies question_type properly
4. Extracts sample size from metadata
5. Handles all 4 chunk formats
"""

import csv
import os
import re
from collections import Counter

BASE = '/home/agentbot/workspace/us-political-messaging-dataset'
RAW_DIR = os.path.join(BASE, 'data/raw/dataforprogress')
OUTPUT = os.path.join(BASE, 'data/processed/dfp_issues_repaired.csv')

# Demographic patterns to skip when extracting support percentages
DEMO_PATTERNS = [
    r'under the age of \d+ \((\d+)%\)',
    r'over the age of \d+ \((\d+)%\)',
    r'ages? \d+[-–]\d+ \((\d+)%\)',
    r'younger voters \((\d+)%\)',
    r'older voters \((\d+)%\)',
    r'(?:Black|white|Hispanic|Latino|Asian|AAPI|Native) (?:voters|Americans) \((\d+)%\)',
    r'(?:women|men) \((\d+)%\)',
    r'(?:college|non-college) (?:grads|educated) \((\d+)%\)',
    r'(?:rural|urban|suburban) (?:voters|residents) \((\d+)%\)',
    r'(?:Democrats|Republicans|Independents) \((\d+)%\)',
    r'(?:MAGA|non-MAGA) (?:Republicans|GOP) \((\d+)%\)',
]

# Keywords that indicate an actual support/oppose percentage
SUPPORT_KEYWORDS = [
    'support', 'oppose', 'favor', 'approve', 'agree', 'back',
    'disapprove', 'disagree', 'want', 'believe', 'think', 'say',
    'prefer', 'priority', 'important', 'concerned', 'likely to',
    'trust', 'confidence', 'rate', 'view',
]

def is_demographic_percentage(bullet_text):
    """Check if the percentage in this bullet is demographic, not support."""
    for pat in DEMO_PATTERNS:
        if re.search(pat, bullet_text):
            return True
    return False

def extract_primary_percentage(bullet_text):
    """Extract the most likely support/oppose percentage from a bullet.
    Returns (percentage, is_support_or_oppose) or (None, False)."""
    # Find all percentages in the bullet
    all_pcts = re.findall(r'(\d+)%', bullet_text)
    if not all_pcts:
        return None, False
    
    # Convert to ints
    pcts = [int(p) for p in all_pcts]
    
    # Check for demographic percentages
    demo_pcts = set()
    for pat in DEMO_PATTERNS:
        for m in re.finditer(pat, bullet_text):
            demo_pcts.add(int(m.group(1)))
    
    # Filter out demographic percentages
    non_demo = [p for p in pcts if p not in demo_pcts]
    
    if non_demo:
        return float(non_demo[0]), True
    
    # If all percentages are demographic, use the first one but mark as questionable
    return float(pcts[0]), False

def classify_finding_type(bullet_text):
    """Classify what kind of polling finding this is."""
    text_lower = bullet_text.lower()
    
    if 'support' in text_lower:
        if 'oppose' in text_lower:
            return 'support_oppose_pair'
        return 'support'
    elif 'oppose' in text_lower:
        return 'oppose'
    elif 'disapprove' in text_lower:
        return 'disapproval'
    elif 'approve' in text_lower:
        return 'approval'
    elif 'favor' in text_lower:
        return 'favorability'
    elif 'trust' in text_lower:
        return 'trust'
    elif 'concern' in text_lower:
        return 'concern'
    elif 'agree' in text_lower:
        return 'agreement'
    elif 'priority' in text_lower or 'important' in text_lower:
        return 'priority'
    elif 'likely' in text_lower:
        return 'likelihood'
    elif 'say' in text_lower or 'think' in text_lower or 'believe' in text_lower:
        return 'opinion'
    return 'polling_finding'

def infer_topic(title, bullet_text):
    """Infer topic from title and bullet text."""
    combined = (title + ' ' + bullet_text).lower()
    
    topic_map = [
        ('economy', ['economy', 'cost of living', 'inflation', 'jobs', 'prices', 'wages', 'tax', 'housing cost', 'affordability', 'groceries', 'gas price']),
        ('healthcare', ['health', 'medicare', 'medicaid', 'drug', 'pharma', 'prescription', 'hospital', 'insurance', 'MAHA', 'medical']),
        ('immigration', ['immigration', 'immigrant', 'border', 'ICE', 'deport', 'asylum', 'migrant']),
        ('climate', ['climate', 'clean energy', 'carbon', 'emissions', 'environment', 'pollution', 'fossil fuel', 'renewable']),
        ('foreign_policy', ['iran', 'china', 'israel', 'gaza', 'ukraine', 'war', 'military', 'foreign', 'nato', 'palestin', 'greenland']),
        ('democracy', ['democracy', 'voting', 'election', 'january 6', 'insurrection', 'impeach', 'supreme court', 'constitution']),
        ('guns', ['gun', 'firearm', 'assault weapon', 'background check']),
        ('abortion', ['abortion', 'reproductive', 'roe', 'pro-choice', 'pro-life']),
        ('technology', ['AI', 'artificial intelligence', 'tech', 'social media', 'data', 'privacy', 'electric vehicle', 'EV']),
        ('education', ['education', 'school', 'student', 'college', 'university']),
        ('crime', ['crime', 'police', 'prison', 'incarceration', 'criminal']),
        ('housing', ['housing', 'rent', 'homeless', 'homeowner', 'landlord']),
        ('labor', ['worker', 'union', 'strike', 'wage', 'overtime', 'paid leave', 'labor']),
        ('taxes', ['tax', 'IRS', 'revenue']),
        ('infrastructure', ['infrastructure', 'transit', 'highway', 'bridge', 'broadband']),
        ('government', ['government', 'congress', 'federal', 'state', 'regulation']),
        ('civil_rights', ['LGBTQ', 'transgender', 'discrimination', 'racism', 'equality', 'civil rights']),
        ('trade', ['trade', 'tariff', 'import', 'export']),
    ]
    
    for topic, keywords in topic_map:
        for kw in keywords:
            if kw in combined:
                return topic
    
    return 'other'

def parse_articles_from_chunk(chunk_text):
    """Parse articles from a chunk, returning list of dicts."""
    articles = []
    
    # Split by article headers
    sections = re.split(r'\n## Article \d+\n', chunk_text)
    # First section is header, skip it
    
    for section in sections[1:]:
        # Clean up trailing separators
        section = re.sub(r'\n---\s*$', '', section).strip()
        if not section:
            continue
        
        # Extract metadata
        title_m = re.search(r'\*\*Title:\*\*\s*(.+?)(?:\n|$)', section)
        url_m = re.search(r'\*\*URL:\*\*\s*(.+?)(?:\n|$)', section)
        date_m = re.search(r'\*\*Date:\*\*\s*(.+?)(?:\n|$)', section)
        
        if not title_m or not url_m or not date_m:
            continue
        
        title = title_m.group(1).strip()
        url = url_m.group(1).strip()
        date = date_m.group(1).strip()
        
        # Extract findings
        findings_start = section.find('### Polling Findings')
        if findings_start < 0:
            continue
        
        findings_text = section[findings_start:]
        
        # Extract bullets
        bullets = re.findall(r'^- (.+)$', findings_text, re.MULTILINE)
        
        # Get sample size
        sample_size = None
        for b in bullets:
            sm = re.search(r'(?:Sample size|sample size|n\s*=\s*|N\s*=\s*)\s*:?\s*([\d,]+)', b)
            if sm:
                sample_size = int(sm.group(1).replace(',', ''))
                break
        
        articles.append({
            'title': title,
            'url': url,
            'date': date,
            'sample_size': sample_size,
            'bullets': bullets,
        })
    
    return articles

def main():
    all_articles = []
    
    # Parse all 4 chunks
    for chunk_name in ['chunk1_polling_data.md', 'chunk2_polling_data.md', 
                       'chunk3_polling_data.md', 'chunk4_polling_data.md']:
        chunk_path = os.path.join(RAW_DIR, chunk_name)
        if not os.path.exists(chunk_path):
            print(f"SKIP {chunk_name}: not found")
            continue
        
        with open(chunk_path) as f:
            text = f.read()
        
        articles = parse_articles_from_chunk(text)
        print(f"{chunk_name}: {len(articles)} articles")
        all_articles.extend(articles)
    
    print(f"\nTotal articles: {len(all_articles)}")
    
    # Build issue rows
    rows = []
    poll_counter = 0
    skipped_demo = 0
    skipped_sample = 0
    skipped_no_pct = 0
    
    for art in all_articles:
        for bullet in art['bullets']:
            # Skip sample size bullets
            if re.match(r'^[Ss]ample size', bullet):
                skipped_sample += 1
                continue
            
            # Skip bullets without percentages
            if '%' not in bullet and not re.search(r'\d+ percent', bullet):
                skipped_no_pct += 1
                continue
            
            # Extract primary percentage
            pct, is_clean = extract_primary_percentage(bullet)
            if pct is None:
                skipped_no_pct += 1
                continue
            
            # Skip purely demographic findings
            if is_demographic_percentage(bullet) and not is_clean:
                skipped_demo += 1
                continue
            
            finding_type = classify_finding_type(bullet)
            topic = infer_topic(art['title'], bullet)
            
            poll_counter += 1
            poll_id = f"DFP_{art['date'].replace('-', '')}_{poll_counter:04d}"
            
            rows.append({
                'poll_id': poll_id,
                'source': 'Data for Progress',
                'source_url': art['url'],
                'date': art['date'],
                'question_type': finding_type,
                'question_wording': bullet.strip(),
                'topic': topic,
                'issue_area': '',
                'support_pct': str(pct),
                'oppose_pct': '',
                'net': '',
                'sample_size': str(art['sample_size']) if art['sample_size'] else '',
                'methodology': 'online_panel',
                'population': 'voters',
                'moe': '',
                'tags': f'dfp;{topic};{finding_type}',
                'notes': f'Article: {art["title"]}. Narrative polling finding.'
            })
    
    # Write output
    fieldnames = ['poll_id', 'source', 'source_url', 'date', 'question_type',
                  'question_wording', 'topic', 'issue_area', 'support_pct', 'oppose_pct',
                  'net', 'sample_size', 'methodology', 'population', 'moe', 'tags', 'notes']
    
    with open(OUTPUT, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    
    print(f"\n=== RESULTS ===")
    print(f"Total findings extracted: {len(rows)}")
    print(f"Skipped (demographic): {skipped_demo}")
    print(f"Skipped (sample size): {skipped_sample}")
    print(f"Skipped (no percentage): {skipped_no_pct}")
    
    # Topic distribution
    topics = Counter(r['topic'] for r in rows)
    print(f"\nTopics: {len(topics)}")
    for t, c in topics.most_common(20):
        print(f"  {t}: {c}")
    
    print(f"\nSaved to: {OUTPUT}")

if __name__ == '__main__':
    main()
