#!/usr/bin/env python3
"""
Restore messages.csv with clean data from source documents + DFP Tested Message Wording sections.
Approach: quality over quantity. Use explicit message wording where available.
"""

import csv, re, sys
from pathlib import Path

BASE = Path(__file__).parent.parent
RAW = BASE / "data" / "raw"
PROC = BASE / "data" / "processed"

msg_fieldnames = [
    'message_id', 'source', 'source_url', 'date', 'topic', 'issue_area',
    'message_type', 'wording', 'support_pct', 'oppose_pct', 'net_score',
    'preference_effect', 'effect_scale', 'sample_size', 'methodology',
    'population', 'moe', 'tags', 'notes'
]

def write_msgs(rows, path):
    with open(path, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=msg_fieldnames)
        w.writeheader()
        w.writerows(rows)

# ====== PART 1: Blueprint (9) ======
blueprint_msgs = [
    {'message_id': 'BLP_20251205_001', 'source': 'Blueprint Research', 'source_url': 'https://blueprint-research.com/polling/dem-message-test-2-5/', 'date': '2025-12-05', 'topic': 'democracy', 'issue_area': 'vision', 'message_type': 'vision', 'wording': 'Fights—really fights—for all of us', 'preference_effect': '14', 'effect_scale': 'maxdiff', 'sample_size': '2572', 'methodology': 'online_panel', 'population': 'likely_voters', 'moe': '2.2', 'tags': 'maxdiff;vision;fight;all_of_us', 'notes': 'MaxDiff of 10 Democratic vision statements. #1 overall.'},
    {'message_id': 'BLP_20251205_002', 'source': 'Blueprint Research', 'source_url': 'https://blueprint-research.com/polling/dem-message-test-2-5/', 'date': '2025-12-05', 'topic': 'democracy', 'issue_area': 'vision', 'message_type': 'vision', 'wording': 'Make the fight to restore the American Dream the heart of our party', 'preference_effect': '12', 'effect_scale': 'maxdiff', 'sample_size': '2572', 'methodology': 'online_panel', 'population': 'likely_voters', 'moe': '2.2', 'tags': 'maxdiff;vision;american_dream', 'notes': 'MaxDiff of 10.'},
    {'message_id': 'BLP_20251205_003', 'source': 'Blueprint Research', 'source_url': 'https://blueprint-research.com/polling/dem-message-test-2-5/', 'date': '2025-12-05', 'topic': 'culture_war', 'issue_area': 'anti_woke', 'message_type': 'vision', 'wording': 'Anti-performative woke politics', 'preference_effect': '-11', 'effect_scale': 'maxdiff', 'sample_size': '2572', 'methodology': 'online_panel', 'population': 'likely_voters', 'moe': '2.2', 'tags': 'maxdiff;anti_woke;worst', 'notes': 'Worst performing message. -33 among Democrats.'},
    {'message_id': 'BLP_20240216_001', 'source': 'Blueprint Research', 'source_url': 'https://blueprint-research.com/polling/back-to-basics-3-6/', 'date': '2024-02-16', 'topic': 'social_security', 'issue_area': 'ssn_medicare', 'message_type': 'contrast', 'wording': 'Trump and Republicans are cutting Social Security and Medicare to pay for billionaire tax cuts', 'support_pct': '56', 'sample_size': '1383', 'methodology': 'online_panel', 'population': 'registered_voters', 'moe': '3.51', 'tags': 'ss_medicare;tax_cuts;billionaires;most_selected', 'notes': '56% selected as most effective anti-Trump message.'},
    {'message_id': 'BLP_20250924_001', 'source': 'Blueprint Research', 'source_url': 'https://blueprint-research.com/polling/build-a-dem-workshop/', 'date': '2025-09-24', 'topic': 'social_security', 'issue_area': 'ssn_medicare', 'message_type': 'policy_proposal', 'wording': 'Protecting Social Security and Medicare', 'preference_effect': '21', 'effect_scale': 'maxdiff', 'sample_size': '3028', 'methodology': 'online_panel', 'population': 'voters', 'moe': '2.1', 'tags': 'maxdiff;ss_medicare;top_issue', 'notes': 'Highest preference effect across ALL tested issues.'},
    {'message_id': 'BLP_20250924_002', 'source': 'Blueprint Research', 'source_url': 'https://blueprint-research.com/polling/build-a-dem-workshop/', 'date': '2025-09-24', 'topic': 'economy', 'issue_area': 'cost_of_living', 'message_type': 'policy_proposal', 'wording': 'Bringing down prices of food and goods', 'preference_effect': '20', 'effect_scale': 'maxdiff', 'sample_size': '3028', 'methodology': 'online_panel', 'population': 'voters', 'moe': '2.1', 'tags': 'maxdiff;cost_of_living;food_prices', 'notes': 'Second highest preference effect.'},
    {'message_id': 'BLP_20241108_001', 'source': 'Blueprint Research', 'source_url': 'https://blueprint-research.com/polling/why-trump-reasons-11-8/', 'date': '2024-11-08', 'topic': 'economy', 'issue_area': 'inflation', 'message_type': 'negative', 'wording': 'Inflation too high under Biden-Harris', 'preference_effect': '24', 'effect_scale': 'relative_importance', 'sample_size': '3262', 'methodology': 'online_panel', 'population': 'voters', 'tags': 'relative_importance;inflation;top_reason', 'notes': 'Highest relative importance for voting against Harris.'},
    {'message_id': 'BLP_20241108_002', 'source': 'Blueprint Research', 'source_url': 'https://blueprint-research.com/polling/why-trump-reasons-11-8/', 'date': '2024-11-08', 'topic': 'immigration', 'issue_area': 'border_security', 'message_type': 'negative', 'wording': 'Too many immigrants crossed the border under Biden-Harris', 'preference_effect': '23', 'effect_scale': 'relative_importance', 'sample_size': '3262', 'methodology': 'online_panel', 'population': 'voters', 'tags': 'relative_importance;immigration;border', 'notes': 'Second highest.'},
    {'message_id': 'BLP_20250924_004', 'source': 'Blueprint Research', 'source_url': 'https://blueprint-research.com/polling/authoritarian-test/', 'date': '2025-09-24', 'topic': 'democracy', 'issue_area': 'authoritarianism', 'message_type': 'negative', 'wording': 'Using executive orders to target political enemies', 'support_pct': '54', 'oppose_pct': '60', 'net_score': '-6', 'sample_size': '3028', 'methodology': 'online_panel', 'population': 'voters', 'moe': '2.1', 'tags': 'authoritarian;executive_orders;political_enemies', 'notes': '54% view as authoritarian. 60% oppose.'},
]
for r in blueprint_msgs:
    for col in msg_fieldnames:
        if col not in r:
            r[col] = r.get(col, '')

# ====== PART 2: Navigator (3 hardcoded + parse archive) ======
nav_msgs = [
    {'message_id': 'NAV_20260216_001', 'source': 'Navigator Research', 'source_url': 'https://navigatorresearch.org/special-battleground-report-on-food-and-health-part-ii-messages/', 'date': '2026-02-16', 'topic': 'healthcare', 'issue_area': 'food_safety', 'message_type': 'negative', 'wording': 'Trump and Republicans are hurting American children...', 'support_pct': '64', 'sample_size': '1500', 'methodology': 'online_panel', 'population': 'likely_voters', 'moe': '2.5', 'tags': 'food_safety;children;snap', 'notes': '64% concerned.'},
    {'message_id': 'NAV_20260216_002', 'source': 'Navigator Research', 'source_url': 'https://navigatorresearch.org/special-battleground-report-on-food-and-health-part-ii-messages/', 'date': '2026-02-16', 'topic': 'economy', 'issue_area': 'food_prices', 'message_type': 'negative', 'wording': 'Trump and Republicans allowed food companies to take advantage of inflation to raise prices.', 'support_pct': '68', 'sample_size': '1500', 'methodology': 'online_panel', 'population': 'likely_voters', 'moe': '2.5', 'tags': 'price_gouging;food_prices', 'notes': '68% concerned.'},
    {'message_id': 'NAV_20260319_001', 'source': 'Navigator Research', 'source_url': 'https://navigatorresearch.org/the-more-americans-learn-about-the-save-act-the-less-they-like-it/', 'date': '2026-03-19', 'topic': 'voting_rights', 'issue_area': 'voter_id', 'message_type': 'rebuttal', 'wording': 'The SAVE Act would require a passport or birth certificate to register to vote...', 'support_pct': '52', 'sample_size': '1500', 'methodology': 'online_panel', 'population': 'likely_voters', 'moe': '2.5', 'tags': 'save_act;voter_suppression', 'notes': '52% convincing. Flipped support from +11 to -2 net.'},
]
for r in nav_msgs:
    for col in msg_fieldnames:
        if col not in r:
            r[col] = r.get(col, '')

# Parse archive for more Navigator messages
nav_file = RAW / "navigator" / "navigator_full_archive.md"
if nav_file.exists():
    with open(nav_file, encoding='utf-8') as f:
        text = f.read()
    
    articles = re.split(r'## \d+\.\s+', text)
    seen_urls = set(r['source_url'] for r in nav_msgs)
    
    for article in articles[1:]:
        lines = article.split('\n')
        title = lines[0].strip() if lines else ''
        
        # Extract URL
        url = ''
        for line in lines:
            for m in re.finditer(r'(https?://navigatorresearch\.org[^\s\)"]+)', line):
                url = m.group(1).rstrip(')')
                break
            if url:
                break
        if not url or url in seen_urls:
            continue
        
        # Extract date
        date = ''
        m = re.search(r'(\d{4}-\d{2}-\d{2})', article[:500])
        if m:
            date = m.group(1)
        
        # Extract sample
        sample = ''
        m = re.search(r'Sample[:\s]*(\d[\d,]*)', article)
        if m:
            sample = m.group(1).replace(',', '')
        
        # Find messages (bullets with quotes or percentages)
        bullets = []
        for line in lines:
            s = line.strip()
            if s.startswith('-') and ('%' in s or s.startswith('- "') or any(k in s.lower() for k in ['message', 'argument', 'focus group', 'framing'])):
                s = s.lstrip('- ').strip('" \u201c\u201d')
                if len(s) > 30:
                    bullets.append(s)
        
        # Infer topic
        topic = 'general'
        low = (title + ' ' + article[:500]).lower()
        for kw, t in [('food', 'healthcare'), ('health', 'healthcare'), ('immigration', 'immigration'),
                       ('tariff', 'economy'), ('tax', 'economy'), ('save', 'voting_rights'),
                       ('iran', 'foreign_policy'), ('budget', 'economy'), ('doge', 'government'),
                       ('musk', 'technology'), ('ice', 'immigration'), ('abortion', 'abortion'),
                       ('guns', 'guns'), ('climate', 'climate')]:
            if kw in low:
                topic = t
                break
        
        for i, bullet in enumerate(bullets):
            pct = ''
            m = re.search(r'(\d+)%', bullet)
            if m:
                pct = m.group(1)
            row = {'message_id': f"NAV_{date[:8].replace('-', '')}_{i+1:03d}", 'source': 'Navigator Research',
                   'source_url': url, 'date': date, 'topic': topic, 'message_type': 'tested_message',
                   'wording': bullet[:500], 'support_pct': pct, 'sample_size': sample,
                   'methodology': 'online_panel', 'population': 'likely_voters',
                   'tags': f'navigator;{topic}', 'notes': f'From: {title[:80]}'}
            for col in msg_fieldnames:
                if col not in row:
                    row[col] = row.get(col, '')
            nav_msgs.append(row)
            seen_urls.add(url)

print(f"Navigator messages: {len(nav_msgs)}")

# ====== PART 3: DFP Tested Message Wording sections only ======
sys.path.insert(0, str(BASE / "scripts"))
from parse_dfp_chunks import parse_chunk1, parse_chunk2, parse_chunk3, parse_chunk4, bullet_to_message_row

dfp_msgs = []
seen_dfp = set()

def looks_like_message_test(text):
    low = text.lower()
    cues = ['message', 'argument', 'convinc', 'persua', 'more likely', 'less likely', 'support after', 'oppose after']
    return any(c in low for c in cues)

dfp_files = [
    ("chunk1_polling_data.md", parse_chunk1, "bullets"),
    ("chunk2_polling_data.md", parse_chunk2, "msg_wording"),
    ("chunk3_polling_data.md", parse_chunk3, "polling_bullets"),
    ("chunk4_polling_data.md", parse_chunk4, "polling_bullets"),
]

for filename, parser, field in dfp_files:
    fp = RAW / "dataforprogress" / filename
    if not fp.exists():
        continue
    with open(fp, encoding='utf-8') as f:
        articles = parser(f.read())

    for art in articles:
        candidates = art.get(field, [])
        for wording in candidates:
            w = wording.strip().strip('" \u201c\u201d')
            if len(w) < 10:
                continue
            if field != "msg_wording" and not looks_like_message_test(w):
                continue
            
            row = bullet_to_message_row(art, w, len(dfp_msgs))
            if not row:
                continue
            
            row['wording'] = w
            key = (art.get('url', ''), w[:80])
            if key in seen_dfp:
                continue
            seen_dfp.add(key)
            
            # Map topics from title
            title = art.get('title', '')
            topic = 'general'
            low = (title + ' ' + w).lower()
            for kw, t in [('immigra', 'immigration'), ('border', 'immigration'), ('iran', 'foreign_policy'),
                           ('israel', 'foreign_policy'), ('gaza', 'foreign_policy'), ('china', 'foreign_policy'),
                           ('climate', 'climate'), ('environment', 'climate'), ('energy', 'climate'),
                           ('health', 'healthcare'), ('medicare', 'healthcare'), ('drug', 'healthcare'),
                           ('economy', 'economy'), ('inflation', 'economy'), ('price', 'economy'),
                           ('housing', 'housing'), ('gun', 'guns'), ('abortion', 'abortion'),
                           ('democracy', 'democracy'), ('voting', 'democracy'), ('vote', 'democracy'),
                           ('tech', 'technology'), ('ai', 'technology'), ('social media', 'technology'),
                           ('tax', 'taxes'), ('crime', 'crime')]:
                if kw in low:
                    topic = t
                    break
            row['topic'] = topic
            row['tags'] = f"dfp;{topic}"
            
            for col in msg_fieldnames:
                if col not in row:
                    row[col] = row.get(col, '')
            
            dfp_msgs.append(row)

print(f"DFP messages (Tested Message Wording only): {len(dfp_msgs)}")

# Assign clean IDs
for i, r in enumerate(dfp_msgs):
    r['message_id'] = f"DFP_{100+i:04d}"

# ====== PART 4: Combine ======
all_msgs = blueprint_msgs + nav_msgs + dfp_msgs
print(f"\n=== FINAL ===")
print(f"  Blueprint:  {len(blueprint_msgs)}")
print(f"  Navigator:  {len(nav_msgs)}")
print(f"  DFP:        {len(dfp_msgs)}")
print(f"  Total:      {len(all_msgs)}")

write_msgs(all_msgs, PROC / "messages.csv")

# Verify
with open(PROC / "messages.csv") as f:
    count = sum(1 for _ in f) - 1
print(f"Verified: {count} data rows in messages.csv")

# Quick quality check
sources = set(r['source'] for r in all_msgs)
topics = {}
for r in all_msgs:
    t = r['topic']
    topics[t] = topics.get(t, 0) + 1
print(f"Sources: {sources}")
print(f"Topics: {dict(sorted(topics.items(), key=lambda x: -x[1]))}")
