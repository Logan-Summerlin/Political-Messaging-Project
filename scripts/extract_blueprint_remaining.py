#!/usr/bin/env python3
"""
Extract remaining Blueprint articles from the source doc into messages.csv.
Also standardize a few short wording labels.
"""
import csv, re
from pathlib import Path

BASE = Path(__file__).parent.parent
PROC = BASE / "data" / "processed"
BLUEPRINT_SRC = BASE / "sources" / "blueprint_message_testing_data.md"

msg_fieldnames = [
    'message_id', 'source', 'source_url', 'date', 'topic', 'issue_area',
    'message_type', 'wording', 'support_pct', 'oppose_pct', 'net_score',
    'preference_effect', 'effect_scale', 'sample_size', 'methodology',
    'population', 'moe', 'tags', 'notes'
]

# Read existing
with open(PROC / 'messages.csv', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    existing = list(reader)
existing_ids = set(r['message_id'] for r in existing)
blp_existing = [r for r in existing if r['source'] == 'Blueprint Research']

# Get max BLP ID number
blp_nums = set()
for r in blp_existing:
    mid = r['message_id']
    try:
        parts = mid.split('_')
        blp_nums.add(int(parts[2]))
    except:
        pass
next_num = max(blp_nums) + 1 if blp_nums else 1

def add_message(rows, existing_ids, **kwargs):
    """Add a row if unique by URL + wording prefix."""
    mid = kwargs.get('message_id', '')
    if mid in existing_ids:
        return False
    row = {k: '' for k in msg_fieldnames}
    row.update(kwargs)
    rows.append(row)
    existing_ids.add(mid)
    return True

# ====== Blueprint articles to extract from source doc ======
# Each article from the source doc that's NOT in CSV

# 1. Defining Harris: The Case For Positive Messaging (Aug 8, 2024)
# URL: /polling/harris-poll-positive-message-8-8/
article_url = "https://blueprint-research.com/polling/harris-poll-positive-message-8-8/"
add_message(existing, existing_ids,
    message_id=f'BLP_{next_num:04d}', source='Blueprint Research',
    source_url=article_url, date='2024-08-08', topic='politics',
    issue_area='harris_messaging', message_type='positive',
    wording='Minds made up about Trump — 71% say nothing could change their opinion about Trump',
    support_pct='71', tags='blueprint;harris;trump;positive',
    notes='From: Defining Harris: The Case For Positive Messaging. 71% minds made up about Trump vs 57% about Harris.')
next_num += 1

add_message(existing, existing_ids,
    message_id=f'BLP_{next_num:04d}', source='Blueprint Research',
    source_url=article_url, date='2024-08-08', topic='politics',
    issue_area='harris_messaging', message_type='positive',
    wording='Only 20% of voters are open to changing their mind about Harris — higher potential than Trump for persuasion',
    support_pct='20', tags='blueprint;harris;persuasion',
    notes='From: Defining Harris: The Case For Positive Messaging. 20% open to changing mind about Harris.')
next_num += 1

add_message(existing, existing_ids,
    message_id=f'BLP_{next_num:04d}', source='Blueprint Research',
    source_url=article_url, date='2024-08-08', topic='economy',
    issue_area='inflation', message_type='negative',
    wording='23% of voters associate Harris with inflation — less than Trump on the same issue',
    support_pct='23', tags='blueprint;harris;inflation;perception',
    notes='From: Defining Harris. 23% associate Harris with inflation.')
next_num += 1

# 2. Campaign Like It's 2008 (Sep 4, 2024)
# URL: /polling/obama-broad-messaging-9-5/
article_url2 = "https://blueprint-research.com/polling/obama-broad-messaging-9-5/"
add_message(existing, existing_ids,
    message_id=f'BLP_{next_num:04d}', source='Blueprint Research',
    source_url=article_url2, date='2024-09-04', topic='economy',
    issue_area='economic_approval', message_type='tracking_poll',
    wording='Obama economic policies net approval',
    support_pct='53', oppose_pct='39', net_score='+14',
    preference_effect='14', effect_scale='net_approval',
    tags='blueprint;obama;economy;approval;positive',
    notes='From: Campaign Like It\'s 2008. Obama +14, Harris +4, Biden -4, Trump -4.')
next_num += 1

add_message(existing, existing_ids,
    message_id=f'BLP_{next_num:04d}', source='Blueprint Research',
    source_url=article_url2, date='2024-09-04', topic='economy',
    issue_area='economic_approval', message_type='tracking_poll',
    wording='Harris economic policies net approval — slightly positive among voters',
    support_pct='46', oppose_pct='42', net_score='+4',
    preference_effect='4', effect_scale='net_approval',
    tags='blueprint;harris;economy;approval',
    notes='From: Campaign Like It\'s 2008. Harris +4 net.')
next_num += 1

add_message(existing, existing_ids,
    message_id=f'BLP_{next_num:04d}', source='Blueprint Research',
    source_url=article_url2, date='2024-09-04', topic='economy',
    issue_area='messaging_style', message_type='positive',
    wording='General/sweeping policy promises are more persuasive than detailed or data-heavy messaging when discussing economic policy',
    tags='blueprint;messaging;style;broad',
    notes='From: Campaign Like It\'s 2008. Broad policy promises outperform detailed/dense messaging.')
next_num += 1

# 3. Debate Snap Poll and Message Test (Sep 11, 2024)
# URL: /polling/debate-test-9-11/
article_url3 = "https://blueprint-research.com/polling/debate-test-9-11/"
add_message(existing, existing_ids,
    message_id=f'BLP_{next_num:04d}', source='Blueprint Research',
    source_url=article_url3, date='2024-09-11', topic='politics',
    issue_area='debate_perception', message_type='tracking_poll',
    wording='Harris won the debate according to viewers',
    support_pct='56', tags='blueprint;debate;harris;win',
    notes='From: Debate Snap Poll. 56% said Harris won (50% independents). 31% said Trump won.')
next_num += 1

add_message(existing, existing_ids,
    message_id=f'BLP_{next_num:04d}', source='Blueprint Research',
    source_url=article_url3, date='2024-09-11', topic='politics',
    issue_area='debate_effect', message_type='tracking_poll',
    wording='45% more likely to support Harris after debate (37% independents)',
    support_pct='45', tags='blueprint;debate;harris;support_shift',
    notes='From: Debate Snap Poll. 45% more likely to support Harris after debate.')
next_num += 1

add_message(existing, existing_ids,
    message_id=f'BLP_{next_num:04d}', source='Blueprint Research',
    source_url=article_url3, date='2024-09-11', topic='politics',
    issue_area='biden_similarity', message_type='tracking_poll',
    wording='47% see Harris administration as continuation of Biden — a messaging vulnerability',
    support_pct='47', tags='blueprint;harris;biden;similarity',
    notes='From: Debate Snap Poll. 47% see Harris as continuation of Biden.')
next_num += 1

# 4. The Case For More Kamala: Interview Testing (Sep 19, 2024) 
# Already partially extracted with clip_test rows. Let me add the ones not in CSV yet.
# BLP_20240919_001 through _006 are already in the CSV from the earlier extraction.
# These represent 6 rows already in the CSV.

# 5. Change Election, Kitchen Table Mandate (Nov 25, 2024)
# URL: /polling/post-mortem-3-nov-25/
article_url5 = "https://blueprint-research.com/polling/post-mortem-3-nov-25/"
add_message(existing, existing_ids,
    message_id=f'BLP_{next_num:04d}', source='Blueprint Research',
    source_url=article_url5, date='2024-11-25', topic='economy',
    issue_area='inflation', message_type='tracking_poll',
    wording='46% want Democrats to focus on inflation/prices as their top priority (52% swing voters)',
    support_pct='46', tags='blueprint;priorities;inflation;swing',
    notes='From: Change Election, Kitchen Table Mandate. 46% want Dems focus on inflation.')
next_num += 1

add_message(existing, existing_ids,
    message_id=f'BLP_{next_num:04d}', source='Blueprint Research',
    source_url=article_url5, date='2024-11-25', topic='immigration',
    issue_area='border_security', message_type='tracking_poll',
    wording='24% want Democrats to focus on immigration (31% swing voters)',
    support_pct='24', tags='blueprint;priorities;immigration',
    notes='From: Change Election. 24% want Dems focus on immigration (31% swing).')
next_num += 1

add_message(existing, existing_ids,
    message_id=f'BLP_{next_num:04d}', source='Blueprint Research',
    source_url=article_url5, date='2024-11-25', topic='economy',
    issue_area='deficit', message_type='tracking_poll',
    wording='71% favor deficit reduction even with spending cuts (only 12% support deficit spending)',
    support_pct='71', tags='blueprint;deficit;spending',
    notes='From: Change Election. 71% favor deficit reduction even with cuts.')
next_num += 1

add_message(existing, existing_ids,
    message_id=f'BLP_{next_num:04d}', source='Blueprint Research',
    source_url=article_url5, date='2024-11-25', topic='politics',
    issue_area='party_perception', message_type='tracking_poll',
    wording='Republicans seen as party of elites (+13 margin over Democrats)',
    preference_effect='13', effect_scale='party_perception_margin',
    tags='blueprint;party_perception;elites;republicans',
    notes='From: Change Election. Republicans seen as elites by +13 margin.')
next_num += 1

add_message(existing, existing_ids,
    message_id=f'BLP_{next_num:04d}', source='Blueprint Research',
    source_url=article_url5, date='2024-11-25', topic='politics',
    issue_area='party_perception', message_type='tracking_poll',
    wording='Democrats seen as establishment (+9 margin over Republicans)',
    preference_effect='9', effect_scale='party_perception_margin',
    tags='blueprint;party_perception;establishment;democrats',
    notes='From: Change Election. Democrats seen as establishment by +9 margin.')
next_num += 1

add_message(existing, existing_ids,
    message_id=f'BLP_{next_num:04d}', source='Blueprint Research',
    source_url=article_url5, date='2024-11-25', topic='politics',
    issue_area='vote_motivation', message_type='tracking_poll',
    wording='Dissatisfaction with Biden-Harris (33%) vs Trump proposals (32%) as primary vote driver among swing voters: 49% dissatisfaction vs 39% proposals',
    support_pct='33', tags='blueprint;swing;motivation;biden;harris',
    notes='From: Change Election. Dissatisfaction drove swing voters more than Trump proposals.')
next_num += 1

# 6. John Kelly Vs. The Economy (Oct 28, 2024)
# URL: /polling/swing-state-kelly-10-28/
article_url6 = "https://blueprint-research.com/polling/swing-state-kelly-10-28/"
add_message(existing, existing_ids,
    message_id=f'BLP_{next_num:04d}', source='Blueprint Research',
    source_url=article_url6, date='2024-10-28', topic='politics',
    issue_area='kelly_comments', message_type='tracking_poll',
    wording='57% of swing state voters heard John Kelly comments about Trump calling him a dictator',
    support_pct='57', sample_size='3623', methodology='online_panel',
    population='swing_state_voters',
    tags='blueprint;kelly;trump;dictator;swing_state',
    notes='From: John Kelly Vs. The Economy. 57% heard Kelly comments about Trump/dictators.')
next_num += 1

add_message(existing, existing_ids,
    message_id=f'BLP_{next_num:04d}', source='Blueprint Research',
    source_url=article_url6, date='2024-10-28', topic='politics',
    issue_area='kelly_comments', message_type='tracking_poll',
    wording='47% say John Kelly comments about Trump are a good reason to vote against Trump (36% very good reason)',
    support_pct='47', sample_size='3623', methodology='online_panel',
    population='swing_state_voters',
    tags='blueprint;kelly;trump;voting_reason',
    notes='From: John Kelly Vs. The Economy. 47% say good reason to vote against Trump.')
next_num += 1

add_message(existing, existing_ids,
    message_id=f'BLP_{next_num:04d}', source='Blueprint Research',
    source_url=article_url6, date='2024-10-28', topic='politics',
    issue_area='kelly_comments', message_type='tracking_poll',
    wording='41% of swing state swing voters say Kelly comments are a good reason to vote against Trump (vs 29% bad reason)',
    support_pct='41', sample_size='3623', methodology='online_panel',
    population='swing_state_swing_voters',
    tags='blueprint;kelly;swing;trump',
    notes='From: John Kelly Vs. The Economy. Among swing voters in swing states: 41% good reason.')
next_num += 1

# 7. Swing State Decision Points (Oct 29, 2024)
# URL: /polling/swing-state-decision-points-10-29/
article_url7 = "https://blueprint-research.com/polling/swing-state-decision-points-10-29/"
add_message(existing, existing_ids,
    message_id=f'BLP_{next_num:04d}', source='Blueprint Research',
    source_url=article_url7, date='2024-10-29', topic='abortion',
    issue_area='pro_choice', message_type='tracking_poll',
    wording='Swing state swing voters are pro-choice by a +24 margin',
    net_score='+24', tags='blueprint;abortion;swing;pro_choice',
    notes='From: Swing State Decision Points. Pro-choice +24 among swing state swing voters.')
next_num += 1

add_message(existing, existing_ids,
    message_id=f'BLP_{next_num:04d}', source='Blueprint Research',
    source_url=article_url7, date='2024-10-29', topic='economy',
    issue_area='cost_of_living', message_type='tracking_poll',
    wording='67% of swing state voters say lower prices are a top priority',
    support_pct='67', tags='blueprint;prices;priority;swing',
    notes='From: Swing State Decision Points. 67% prioritize lower prices.')
next_num += 1

add_message(existing, existing_ids,
    message_id=f'BLP_{next_num:04d}', source='Blueprint Research',
    source_url=article_url7, date='2024-10-29', topic='politics',
    issue_area='candidate_perception', message_type='tracking_poll',
    wording='Harris +10 on \'represent all Americans\' over Trump among swing state voters',
    preference_effect='10', effect_scale='candidate_perception_margin',
    tags='blueprint;harris;represent;swing',
    notes='From: Swing State Decision Points. Harris +10 on representing all Americans.')
next_num += 1

# 8. Obama-Trump-Harris Voter (Oct 31, 2024)
# URL: /polling/swing-state-issues-10-31/
article_url8 = "https://blueprint-research.com/polling/swing-state-issues-10-31/"
add_message(existing, existing_ids,
    message_id=f'BLP_{next_num:04d}', source='Blueprint Research',
    source_url=article_url8, date='2024-10-31', topic='politics',
    issue_area='candidate_favorability', message_type='tracking_poll',
    wording='Harris +7 favorability over Trump with swing state swing voters',
    preference_effect='7', effect_scale='net_favorability',
    tags='blueprint;harris;trump;favorability;swing',
    notes='From: Obama-Trump-Harris Voter. Harris +7 over Trump with swing swing voters.')
next_num += 1

add_message(existing, existing_ids,
    message_id=f'BLP_{next_num:04d}', source='Blueprint Research',
    source_url=article_url8, date='2024-10-31', topic='politics',
    issue_area='candidate_favorability', message_type='tracking_poll',
    wording='Obama favorability with swing state swing voters: +16 net approval (Biden: -45)',
    preference_effect='16', effect_scale='net_favorability',
    tags='blueprint;obama;biden;favorability;swing',
    notes='From: Obama-Trump-Harris Voter. Obama +16, Biden -45 with swing swing voters.')
next_num += 1

add_message(existing, existing_ids,
    message_id=f'BLP_{next_num:04d}', source='Blueprint Research',
    source_url=article_url8, date='2024-10-31', topic='economy',
    issue_area='price_gouging', message_type='tracking_poll',
    wording='Grocery prices crackdown — +57 net personal benefit rating among swing state voters',
    net_score='+57', tags='blueprint;price_gouching;groceries;swing',
    notes='From: Obama-Trump-Harris Voter. +57 net benefit for grocery price crackdown.')
next_num += 1

add_message(existing, existing_ids,
    message_id=f'BLP_{next_num:04d}', source='Blueprint Research',
    source_url=article_url8, date='2024-10-31', topic='healthcare',
    issue_area='drug_prices', message_type='tracking_poll',
    wording='Prescription drug costs crackdown — +41 net personal benefit among swing state voters',
    net_score='+41', tags='blueprint;prescription_drugs;swing',
    notes='From: Obama-Trump-Harris Voter. +41 net benefit for prescription drug cost crackdown.')
next_num += 1

add_message(existing, existing_ids,
    message_id=f'BLP_{next_num:04d}', source='Blueprint Research',
    source_url=article_url8, date='2024-10-31', topic='politics',
    issue_area='misinformation', message_type='tracking_poll',
    wording='Only 27% of swing state swing voters believe Harris defunds police; 19% believe she would ban private insurance; 28% believe she supports Medicare for All',
    support_pct='27', tags='blueprint;misinformation;harris;policy',
    notes='From: Obama-Trump-Harris Voter. Most swing voters don\'t believe negative claims about Harris.')
next_num += 1

add_message(existing, existing_ids,
    message_id=f'BLP_{next_num:04d}', source='Blueprint Research',
    source_url=article_url8, date='2024-10-31', topic='abortion',
    issue_area='choice', message_type='tracking_poll',
    wording='Pro-choice sentiment among swing state swing voters: 55% to 29% (+26 margin)',
    net_score='+26', tags='blueprint;abortion;choice;swing',
    notes='From: Obama-Trump-Harris Voter. Pro-choice +26 among swing swing voters.')
next_num += 1

# 9. Rust Belt to Sun Belt (Sep 9, 2024)
# URL: /polling/swing-state-9-9/
article_url9 = "https://blueprint-research.com/polling/swing-state-9-9/"
add_message(existing, existing_ids,
    message_id=f'BLP_{next_num:04d}', source='Blueprint Research',
    source_url=article_url9, date='2024-09-09', topic='economy',
    issue_area='tax_cuts', message_type='positive',
    wording='Cutting taxes for middle class — most compelling reason to vote for Harris among swing state voters',
    tags='blueprint;harris;tax_cuts;middle_class;top_issue',
    notes='From: Rust Belt to Sun Belt. Top compelling reason to vote for Harris.')
next_num += 1

add_message(existing, existing_ids,
    message_id=f'BLP_{next_num:04d}', source='Blueprint Research',
    source_url=article_url9, date='2024-09-09', topic='crime',
    issue_area='drug_smuggling', message_type='positive',
    wording='Cracking down on crime and drug smuggling — compelling reason to vote for Harris among swing state voters',
    tags='blueprint;harris;crime;drug_smuggling',
    notes='From: Rust Belt to Sun Belt. Compelling reason to vote for Harris.')
next_num += 1

add_message(existing, existing_ids,
    message_id=f'BLP_{next_num:04d}', source='Blueprint Research',
    source_url=article_url9, date='2024-09-09', topic='economy',
    issue_area='price_gouging', message_type='positive',
    wording='Going after price gougers and hidden fees — compelling reason to vote for Harris',
    tags='blueprint;harris;price_gouging;hidden_fees',
    notes='From: Rust Belt to Sun Belt. Compelling reason to vote for Harris.')
next_num += 1

add_message(existing, existing_ids,
    message_id=f'BLP_{next_num:04d}', source='Blueprint Research',
    source_url=article_url9, date='2024-09-09', topic='economy',
    issue_area='housing', message_type='positive',
    wording='Building new homes and addressing housing supply — compelling reason to vote for Harris',
    tags='blueprint;harris;housing;construction',
    notes='From: Rust Belt to Sun Belt. Compelling reason to vote for Harris.')
next_num += 1

add_message(existing, existing_ids,
    message_id=f'BLP_{next_num:04d}', source='Blueprint Research',
    source_url=article_url9, date='2024-09-09', topic='politics',
    issue_area='candidate_comparison', message_type='tracking_poll',
    wording='Harris leads independents on every issue except border security, immigration, and oil/gas production',
    tags='blueprint;harris;independents;issues',
    notes='From: Rust Belt to Sun Belt. Harris leads independents on most issues.')
next_num += 1

# 10. Meat and Potatoes (Sep 25, 2024)
# URL: /polling/man-survey-9-25/
article_url10 = "https://blueprint-research.com/polling/man-survey-9-25/"
add_message(existing, existing_ids,
    message_id=f'BLP_{next_num:04d}', source='Blueprint Research',
    source_url=article_url10, date='2024-09-25', topic='economy',
    issue_area='men_issues', message_type='tracking_poll',
    wording='Men rank economy as top issue at 78% — followed by SS/Medicare, taxes, and national security',
    support_pct='78', tags='blueprint;men;economy;priorities',
    notes='From: Meat and Potatoes. Men top issues: Economy 78%, SS/Medicare, taxes, national security.')
next_num += 1

add_message(existing, existing_ids,
    message_id=f'BLP_{next_num:04d}', source='Blueprint Research',
    source_url=article_url10, date='2024-09-25', topic='politics',
    issue_area='party_perception', message_type='tracking_poll',
    wording='55% of men say Democrats have moved too far left (+24 net margin)',
    support_pct='55', net_score='+24', tags='blueprint;men;democrats;ideology',
    notes='From: Meat and Potatoes. 55% say Dems moved too far left. Lowest trust: crypto, transgender, feminism.')
next_num += 1

add_message(existing, existing_ids,
    message_id=f'BLP_{next_num:04d}', source='Blueprint Research',
    source_url=article_url10, date='2024-09-25', topic='politics',
    issue_area='trust_comparison', message_type='tracking_poll',
    wording='Men trust Harris on abortion, climate, environment, and transgender issues. Men trust Trump on inflation, regulations, national security, foreign policy, and immigration.',
    tags='blueprint;men;trust;harris;trump',
    notes='From: Meat and Potatoes. Trust split: Harris on social issues, Trump on economic/national security.')
next_num += 1

# 11. How to Become Do-Something Democrats (Oct 23, 2025)
# URL: /polling/do-something-dems-10-15/
article_url11 = "https://blueprint-research.com/polling/do-something-dems-10-15/"
add_message(existing, existing_ids,
    message_id=f'BLP_{next_num:04d}', source='Blueprint Research',
    source_url=article_url11, date='2025-10-23', topic='economy',
    issue_area='blame', message_type='tracking_poll',
    wording='49% blame Republicans for rising prices, 37% blame Democrats',
    support_pct='49', tags='blueprint;blame;prices;republicans',
    notes='From: How to Become Do-Something Democrats. 49% blame GOP for rising prices.')
next_num += 1

add_message(existing, existing_ids,
    message_id=f'BLP_{next_num:04d}', source='Blueprint Research',
    source_url=article_url11, date='2025-10-23', topic='government',
    issue_area='epstein', message_type='tracking_poll',
    wording='76% want DOJ to release Epstein files — top non-economic policy preference',
    support_pct='76', tags='blueprint;epstein;transparency',
    notes='From: Do-Something Democrats. 76% want Epstein files released.')
next_num += 1

add_message(existing, existing_ids,
    message_id=f'BLP_{next_num:04d}', source='Blueprint Research',
    source_url=article_url11, date='2025-10-23', topic='politics',
    issue_area='preferred_action', message_type='ranking',
    wording='Most preferred Democratic action: Protecting healthcare as party\'s top priority',
    tags='blueprint;democrats;healthcare;priority',
    notes='From: Do-Something Democrats. #1 most preferred Democratic action.')
next_num += 1

add_message(existing, existing_ids,
    message_id=f'BLP_{next_num:04d}', source='Blueprint Research',
    source_url=article_url11, date='2025-10-23', topic='economy',
    issue_area='price_gouging', message_type='ranking',
    wording='Most preferred hypothetical Democratic policy: Cracking down on grocery price-gouging',
    tags='blueprint;democrats;policy;price_gouging',
    notes='From: Do-Something Democrats. #1 most preferred hypothetical Democratic policy.')
next_num += 1

add_message(existing, existing_ids,
    message_id=f'BLP_{next_num:04d}', source='Blueprint Research',
    source_url=article_url11, date='2025-10-23', topic='economy',
    issue_area='drug_prices', message_type='ranking',
    wording='Second most preferred policy: Cracking down on pharmaceutical overcharging',
    tags='blueprint;pharma;drug_prices;policy',
    notes='From: Do-Something Democrats. #2 preferred policy.')
next_num += 1

add_message(existing, existing_ids,
    message_id=f'BLP_{next_num:04d}', source='Blueprint Research',
    source_url=article_url11, date='2025-10-23', topic='social_issues',
    issue_area='social_media_children', message_type='ranking',
    wording='Third most preferred policy: Crack down on social media harmful content for children',
    tags='blueprint;social_media;children;policy',
    notes='From: Do-Something Democrats. #3 preferred policy.')
next_num += 1

# Expand short Blueprint wordings
for r in existing:
    mid = r['message_id']
    w = r['wording'].strip()
    
    expansions = {
        'BLP_20251205_006': 'Calling out oligarchy and concentrated corporate power — testing "call out oligarchy" as a Democratic vision message',
        'BLP_20251114_005': 'Billionaire background — voters strongly dislike a billionaire background as a candidate biography trait',
        'BLP_20251114_007': 'Podcaster background — performs poorly as a candidate biography trait among voters',
        'BLP_20241108_005': 'Harris too similar to Joe Biden — a reason voters gave for not supporting her over Trump',
        'BLP_20241108_009': 'Harris too conservative — a low-ranked reason voters gave for not supporting her',
        'BLP_20241108_010': 'Harris too pro-Israel — a low-ranked reason voters gave for not supporting her',
        'BLP_20240830_002': 'Positive Harris healthcare ad — tested ad messaging showing Harris\'s healthcare plans and vision',
        'BLP_20240830_003': 'Positive Harris abortion ad — tested ad messaging on abortion rights featuring Harris\'s position',
        'BLP_20240830_007': 'Trump anti-choice agenda ad — tested ad warning about Trump\'s abortion record and anti-choice agenda',
        'BLP_20240320_002': 'Elon Musk favorability — tested public opinion on Elon Musk\'s overall favorability rating',
    }
    
    if mid in expansions and len(w) < 30:
        r['wording'] = expansions[mid]
        print(f"Expanded {mid}: '{w}' → '{expansions[mid][:60]}...'")

# Write
with open(PROC / 'messages.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=msg_fieldnames)
    writer.writeheader()
    writer.writerows(existing)

from collections import Counter
sources = Counter(r['source'] for r in existing)
print(f"\nFinal: {len(existing)} rows")
for s,c in sources.most_common():
    print(f"  {s}: {c}")
    
# Count with metrics
has_m = sum(1 for r in existing if r.get('support_pct','').strip() or r.get('preference_effect','').strip() or r.get('net_score','').strip())
print(f"With metrics: {has_m}")
