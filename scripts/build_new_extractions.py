#!/usr/bin/env python3
"""
Build comprehensive new_extracted_messages.csv with all missing Blueprint
and Navigator Research message testing data.
"""
import csv
import os

rows = []

# ============================================
# PART 1: BLUEPRINT RESEARCH (new extractions)
# ============================================

# --- Article 1: Dem Message Test 2-5 (Feb 5, 2026) ---
# URL: /polling/dem-message-test-2-5/
# Existing: BLP_20251205_001 (Fights for all +14), BLP_20251205_002 (American Dream +12), BLP_20251205_003 (Anti-woke -11)
url1 = 'https://blueprint-research.com/polling/dem-message-test-2-5/'
rows.append({
    'message_id': 'BLP_20251205_004',
    'source': 'Blueprint Research',
    'source_url': url1,
    'date': '2025-12-05',
    'topic': 'economy',
    'issue_area': 'cost_of_living',
    'message_type': 'vision',
    'wording': 'Laser-focus on making life affordable and expanding the social safety net',
    'support_pct': '', 'oppose_pct': '', 'net_score': '',
    'preference_effect': '17', 'effect_scale': 'maxdiff',
    'sample_size': '2572', 'methodology': 'online_panel', 'population': 'likely_voters', 'moe': '2.2',
    'tags': 'blueprint;vision;affordability;safety_net',
    'notes': "MaxDiff of 10 Democratic vision statements. Democrats' 2nd most preferred statement."
})
rows.append({
    'message_id': 'BLP_20251205_005',
    'source': 'Blueprint Research',
    'source_url': url1,
    'date': '2025-12-05',
    'topic': 'democracy',
    'issue_area': 'governance',
    'message_type': 'vision',
    'wording': 'A government that is every bit as ambitious as our adversaries',
    'support_pct': '', 'oppose_pct': '', 'net_score': '',
    'preference_effect': '12', 'effect_scale': 'maxdiff',
    'sample_size': '2572', 'methodology': 'online_panel', 'population': 'likely_voters', 'moe': '2.2',
    'tags': 'blueprint;vision;ambition;governance',
    'notes': "MaxDiff of 10 Democratic vision statements. +12 among Democrats."
})
rows.append({
    'message_id': 'BLP_20251205_006',
    'source': 'Blueprint Research',
    'source_url': url1,
    'date': '2025-12-05',
    'topic': 'democracy',
    'issue_area': 'oligarchy',
    'message_type': 'vision',
    'wording': 'Calling out oligarchy',
    'support_pct': '', 'oppose_pct': '', 'net_score': '-6',
    'preference_effect': '3', 'effect_scale': 'maxdiff',
    'sample_size': '2572', 'methodology': 'online_panel', 'population': 'likely_voters', 'moe': '2.2',
    'tags': 'blueprint;vision;oligarchy',
    'notes': "MaxDiff of 10. +3 Democrats, -4 independents, -6 overall."
})
rows.append({
    'message_id': 'BLP_20251205_007',
    'source': 'Blueprint Research',
    'source_url': url1,
    'date': '2025-12-05',
    'topic': 'economy',
    'issue_area': 'aspirational',
    'message_type': 'vision',
    'wording': '"Get rich" language with no named antagonist',
    'support_pct': '', 'oppose_pct': '', 'net_score': '-16',
    'preference_effect': '-16', 'effect_scale': 'maxdiff',
    'sample_size': '2572', 'methodology': 'online_panel', 'population': 'likely_voters', 'moe': '2.2',
    'tags': 'blueprint;vision;worst;get_rich',
    'notes': "Worst performing message. -33 among Democrats."
})

# --- Article 6: Interview Testing (Sep 19, 2024) ---
url6 = 'https://blueprint-research.com/polling/interview-test-9-19/'
clip_data = [
    ('BLP_20240919_001', 'Appoint a Republican to cabinet', '2.1', '65% positive, 57% know more'),
    ('BLP_20240919_002', 'Biden dropping out perspective', '1.9', '63% positive, 57% know more'),
    ('BLP_20240919_003', 'Border/immigration answer on CNN', '1.6', '62% positive, 58% know more'),
    ('BLP_20240919_004', 'Opportunity economy vision (6ABC)', '1.5', '64% positive, 58% know more'),
    ('BLP_20240919_005', '"More in common than separates us"', '1.5', '61% positive, 57% know more'),
    ('BLP_20240919_006', 'Fracking/energy answer', '1.4', '59% positive, 58% know more'),
]
for mid, clip, effect, note in clip_data:
    rows.append({
        'message_id': mid,
        'source': 'Blueprint Research',
        'source_url': url6,
        'date': '2024-09-19',
        'topic': 'politics',
        'issue_area': 'kamala_harris',
        'message_type': 'clip_test',
        'wording': f'Harris video clip: {clip}',
        'support_pct': '', 'oppose_pct': '', 'net_score': '',
        'preference_effect': effect, 'effect_scale': 'preference_shift_pts',
        'sample_size': '', 'methodology': 'online_panel', 'population': 'voters', 'moe': '',
        'tags': 'blueprint;harris;clip_test;interview',
        'notes': f'Harris support effect in pts. {note}'
    })

# --- Article 7: Oprah/MSNBC Interview (Oct 7, 2024) ---
url7 = 'https://blueprint-research.com/polling/harris-interviews-test-10-7/'
rows.append({
    'message_id': 'BLP_20241007_001',
    'source': 'Blueprint Research',
    'source_url': url7,
    'date': '2024-10-07',
    'topic': 'economy',
    'issue_area': 'manufacturing',
    'message_type': 'clip_test',
    'wording': 'Harris on US Steel/Nippon manufacturing response: supporting American manufacturing and workers',
    'support_pct': '', 'oppose_pct': '', 'net_score': '',
    'preference_effect': '2.1', 'effect_scale': 'preference_shift_pts',
    'sample_size': '5764', 'methodology': 'online_panel', 'population': 'voters', 'moe': '',
    'tags': 'blueprint;harris;manufacturing;steel',
    'notes': '+2.1 support effect, 66% positive, 64% favorable among 5,764 voters.'
})
rows.append({
    'message_id': 'BLP_20241007_002',
    'source': 'Blueprint Research',
    'source_url': url7,
    'date': '2024-10-07',
    'topic': 'economy',
    'issue_area': 'opportunity_economy',
    'message_type': 'clip_test',
    'wording': 'Harris opportunity economy vision message',
    'support_pct': '', 'oppose_pct': '', 'net_score': '',
    'preference_effect': '2.1', 'effect_scale': 'preference_shift_pts',
    'sample_size': '5764', 'methodology': 'online_panel', 'population': 'voters', 'moe': '',
    'tags': 'blueprint;harris;opportunity_economy',
    'notes': '+2.1 support effect, +2.8 favorability effect, 64% positive.'
})

# --- Article 8: Go Your Own Way (Oct 2, 2024) ---
url8 = 'https://blueprint-research.com/polling/biden-distance-10-2-message-test/'
rows.append({
    'message_id': 'BLP_20241002_001',
    'source': 'Blueprint Research',
    'source_url': url8,
    'date': '2024-10-02',
    'topic': 'economy',
    'issue_area': 'corporate_greed',
    'message_type': 'contrast',
    'wording': "I'm not happy with what greedy corporate giants got away with. Joe Biden needed to get economy back on track...companies took advantage...As president, I will be tougher on unethical businesses than Joe Biden was.",
    'support_pct': '', 'oppose_pct': '', 'net_score': '',
    'preference_effect': '', 'effect_scale': '',
    'sample_size': '', 'methodology': 'online_panel', 'population': 'voters', 'moe': '',
    'tags': 'blueprint;harris;corporate_greed;biden_distance',
    'notes': 'Best distancing message from Biden on corporate greed.'
})
rows.append({
    'message_id': 'BLP_20241002_002',
    'source': 'Blueprint Research',
    'source_url': url8,
    'date': '2024-10-02',
    'topic': 'immigration',
    'issue_area': 'border_security',
    'message_type': 'contrast',
    'wording': "I want to take a different approach to Biden on immigration...from my background as a prosecutor...we need to be really enforcing our laws at the border.",
    'support_pct': '', 'oppose_pct': '', 'net_score': '',
    'preference_effect': '', 'effect_scale': '',
    'sample_size': '', 'methodology': 'online_panel', 'population': 'voters', 'moe': '',
    'tags': 'blueprint;harris;immigration;biden_distance',
    'notes': 'Best distancing message from Biden on immigration.'
})
rows.append({
    'message_id': 'BLP_20241002_003',
    'source': 'Blueprint Research',
    'source_url': url8,
    'date': '2024-10-02',
    'topic': 'politics',
    'issue_area': 'gaffe',
    'message_type': 'negative',
    'wording': '"Not a thing comes to mind" (The View) - Harris asked what she would do differently from Biden',
    'support_pct': '', 'oppose_pct': '', 'net_score': '-21',
    'preference_effect': '-21', 'effect_scale': 'drag_points',
    'sample_size': '', 'methodology': 'online_panel', 'population': 'voters', 'moe': '',
    'tags': 'blueprint;harris;worst;gaffe;the_view',
    'notes': 'Worst tested -21 point drag overall, -26 among independents.'
})

# --- Article 9: Closing Arguments (Oct 16, 2024) ---
url9 = 'https://blueprint-research.com/polling/trump-closing-argument-10-16/'
rows.append({
    'message_id': 'BLP_20241016_001',
    'source': 'Blueprint Research',
    'source_url': url9,
    'date': '2024-10-16',
    'topic': 'democracy',
    'issue_area': 'trump_cabinet',
    'message_type': 'negative',
    'wording': "Nearly half of Donald Trump's cabinet have refused to endorse him...when Trump learned his supporters were threatening to kill his own VP, he said 'so what'...",
    'support_pct': '', 'oppose_pct': '', 'net_score': '',
    'preference_effect': '12', 'effect_scale': 'preference_effect',
    'sample_size': '2993', 'methodology': 'online_panel', 'population': 'voters', 'moe': '',
    'tags': 'blueprint;closing_argument;trump;cabinet;endorsements',
    'notes': 'Republican endorsements message. +12 overall, +14 independents. Sample: 2,993 voters.'
})
rows.append({
    'message_id': 'BLP_20241016_002',
    'source': 'Blueprint Research',
    'source_url': url9,
    'date': '2024-10-16',
    'topic': 'abortion',
    'issue_area': 'roe_v_wade',
    'message_type': 'negative',
    'wording': "Donald Trump appointed the judges who overturned Roe vs. Wade. Since then, Trump abortion bans in 22 states and women are dying...",
    'support_pct': '', 'oppose_pct': '', 'net_score': '',
    'preference_effect': '10', 'effect_scale': 'preference_effect',
    'sample_size': '2993', 'methodology': 'online_panel', 'population': 'voters', 'moe': '',
    'tags': 'blueprint;closing_argument;abortion;roe',
    'notes': 'Roe v. Wade message. +10 overall, +12 independents.'
})

# --- Article 10: Back to Basics (Mar 6, 2024) ---
url10 = 'https://blueprint-research.com/polling/back-to-basics-3-6/'
rows.append({
    'message_id': 'BLP_20240306_001',
    'source': 'Blueprint Research',
    'source_url': url10,
    'date': '2024-03-06',
    'topic': 'immigration',
    'issue_area': 'remain_in_mexico',
    'message_type': 'contrast',
    'wording': 'Remain in Mexico policy reinstated by Trump — voters prefer alternative approach',
    'support_pct': '72', 'oppose_pct': '', 'net_score': '',
    'preference_effect': '22', 'effect_scale': 'boost',
    'sample_size': '1383', 'methodology': 'online_panel', 'population': 'registered_voters', 'moe': '3.51',
    'tags': 'blueprint;immigration;remain_in_mexico;border',
    'notes': '72% preferred alternative to Remain in Mexico. +22 boost. From Back to Basics poll.'
})
rows.append({
    'message_id': 'BLP_20240306_002',
    'source': 'Blueprint Research',
    'source_url': url10,
    'date': '2024-03-06',
    'topic': 'healthcare',
    'issue_area': 'trump_healthcare',
    'message_type': 'negative',
    'wording': 'Trump healthcare net approval',
    'support_pct': '', 'oppose_pct': '', 'net_score': '-10',
    'preference_effect': '', 'effect_scale': 'net_approval',
    'sample_size': '1383', 'methodology': 'online_panel', 'population': 'registered_voters', 'moe': '3.51',
    'tags': 'blueprint;healthcare;trump;net_approval',
    'notes': 'Trump healthcare net approval: -10. Also inflation: -10, corruption: -4.'
})
rows.append({
    'message_id': 'BLP_20240306_003',
    'source': 'Blueprint Research',
    'source_url': url10,
    'date': '2024-03-06',
    'topic': 'economy',
    'issue_area': 'food_prices',
    'message_type': 'contrast',
    'wording': 'Social Security, Medicare threats and food prices messages outperform broad democracy attacks',
    'support_pct': '', 'oppose_pct': '', 'net_score': '',
    'preference_effect': '', 'effect_scale': '',
    'sample_size': '1383', 'methodology': 'online_panel', 'population': 'registered_voters', 'moe': '3.51',
    'tags': 'blueprint;ss_medicare;food_prices;messaging',
    'notes': 'SS/Medicare threats and food prices messages outperform broad democracy attacks.'
})

# --- Article 11: Why America Chose Trump (Nov 8, 2024) ---
# Already extracted: BLP_20241108_001 (Inflation +24), BLP_20241108_002 (Immigration +23)
url11 = 'https://blueprint-research.com/polling/why-trump-reasons-11-8/'
rows.append({
    'message_id': 'BLP_20241108_003',
    'source': 'Blueprint Research',
    'source_url': url11,
    'date': '2024-11-08',
    'topic': 'culture_war',
    'issue_area': 'cultural_issues',
    'message_type': 'negative',
    'wording': 'Harris focused on cultural issues, not the middle class',
    'support_pct': '', 'oppose_pct': '', 'net_score': '',
    'preference_effect': '17', 'effect_scale': 'relative_importance',
    'sample_size': '3262', 'methodology': 'online_panel', 'population': 'voters', 'moe': '',
    'tags': 'blueprint;why_trump;cultural_issues;middle_class',
    'notes': 'Relative importance for not voting for Harris. #3 reason.'
})
rows.append({
    'message_id': 'BLP_20241108_004',
    'source': 'Blueprint Research',
    'source_url': url11,
    'date': '2024-11-08',
    'topic': 'economy',
    'issue_area': 'debt',
    'message_type': 'negative',
    'wording': 'Debt rose too much under Biden-Harris',
    'support_pct': '', 'oppose_pct': '', 'net_score': '',
    'preference_effect': '13', 'effect_scale': 'relative_importance',
    'sample_size': '3262', 'methodology': 'online_panel', 'population': 'voters', 'moe': '',
    'tags': 'blueprint;why_trump;debt;deficit',
    'notes': 'Relative importance for not voting for Harris. #4 reason.'
})
rows.append({
    'message_id': 'BLP_20241108_005',
    'source': 'Blueprint Research',
    'source_url': url11,
    'date': '2024-11-08',
    'topic': 'politics',
    'issue_area': 'biden_similarity',
    'message_type': 'negative',
    'wording': 'Harris too similar to Biden',
    'support_pct': '', 'oppose_pct': '', 'net_score': '',
    'preference_effect': '12', 'effect_scale': 'relative_importance',
    'sample_size': '3262', 'methodology': 'online_panel', 'population': 'voters', 'moe': '',
    'tags': 'blueprint;why_trump;biden;similarity',
    'notes': 'Relative importance for not voting for Harris. #5 reason.'
})
# Swing voter breakdown
rows.append({
    'message_id': 'BLP_20241108_006',
    'source': 'Blueprint Research',
    'source_url': url11,
    'date': '2024-11-08',
    'topic': 'culture_war',
    'issue_area': 'cultural_issues',
    'message_type': 'negative',
    'wording': 'Cultural issues (swing voters who chose Trump)',
    'support_pct': '', 'oppose_pct': '', 'net_score': '',
    'preference_effect': '28', 'effect_scale': 'relative_importance',
    'sample_size': '3262', 'methodology': 'online_panel', 'population': 'voters', 'moe': '',
    'tags': 'blueprint;swing_voters;cultural_issues',
    'notes': 'Swing voters who chose Trump. Cultural issues ranked #1 at +28 relative importance.'
})
rows.append({
    'message_id': 'BLP_20241108_007',
    'source': 'Blueprint Research',
    'source_url': url11,
    'date': '2024-11-08',
    'topic': 'economy',
    'issue_area': 'inflation',
    'message_type': 'negative',
    'wording': 'Inflation (swing voters who chose Trump)',
    'support_pct': '', 'oppose_pct': '', 'net_score': '',
    'preference_effect': '23', 'effect_scale': 'relative_importance',
    'sample_size': '3262', 'methodology': 'online_panel', 'population': 'voters', 'moe': '',
    'tags': 'blueprint;swing_voters;inflation',
    'notes': 'Swing voters who chose Trump. Inflation at +23 relative importance.'
})
# Negative reasons (lowest ranking)
rows.append({
    'message_id': 'BLP_20241108_008',
    'source': 'Blueprint Research',
    'source_url': url11,
    'date': '2024-11-08',
    'topic': 'politics',
    'issue_area': 'biden_similarity',
    'message_type': 'positive',
    'wording': 'Harris not similar enough to Biden',
    'support_pct': '', 'oppose_pct': '', 'net_score': '',
    'preference_effect': '-24', 'effect_scale': 'relative_importance',
    'sample_size': '3262', 'methodology': 'online_panel', 'population': 'voters', 'moe': '',
    'tags': 'blueprint;why_trump;negative_reason',
    'notes': 'Lowest ranking negative reason for voting against Harris. -24 relative importance.'
})
rows.append({
    'message_id': 'BLP_20241108_009',
    'source': 'Blueprint Research',
    'source_url': url11,
    'date': '2024-11-08',
    'topic': 'politics',
    'issue_area': 'ideology',
    'message_type': 'positive',
    'wording': 'Harris too conservative',
    'support_pct': '', 'oppose_pct': '', 'net_score': '',
    'preference_effect': '-27', 'effect_scale': 'relative_importance',
    'sample_size': '3262', 'methodology': 'online_panel', 'population': 'voters', 'moe': '',
    'tags': 'blueprint;why_trump;negative_reason',
    'notes': 'Lowest ranking. -27 relative importance.'
})
rows.append({
    'message_id': 'BLP_20241108_010',
    'source': 'Blueprint Research',
    'source_url': url11,
    'date': '2024-11-08',
    'topic': 'foreign_policy',
    'issue_area': 'israel',
    'message_type': 'positive',
    'wording': 'Harris too pro-Israel',
    'support_pct': '', 'oppose_pct': '', 'net_score': '',
    'preference_effect': '-22', 'effect_scale': 'relative_importance',
    'sample_size': '3262', 'methodology': 'online_panel', 'population': 'voters', 'moe': '',
    'tags': 'blueprint;why_trump;israel;negative_reason',
    'notes': 'Lowest ranking. -22 relative importance.'
})

# --- Article 12: Authoritarian Test (Nov 10, 2025) ---
url12 = 'https://blueprint-research.com/polling/authoritarian-test/'
# Already extracted: BLP_20250924_004 (Exec orders political enemies 54%/60%) - wrong date, but already exists
auth_actions = [
    ('BLP_20251110_001', 'Firing BLS director over jobs data', '50', '59', '50% view as authoritarian, 59% oppose'),
    ('BLP_20251110_002', 'Deploying National Guard to cities', '50', '', '50% view as authoritarian'),
    ('BLP_20251110_003', 'Firing Jan 6 prosecutors', '49', '60', '49% view as authoritarian, 60% oppose'),
    ('BLP_20251110_004', 'FBI raid on John Bolton', '49', '', '49% view as authoritarian'),
    ('BLP_20251110_005', 'Masked ICE raids without badge or warrant', '49', '60', '49% view as authoritarian, 60% oppose'),
    ('BLP_20251110_006', 'FCC pulling NBC/ABC licenses', '49', '62', '49% view as authoritarian, 62% oppose'),
    ('BLP_20251110_007', 'DOGE/grant manipulation', '48', '', '48% view as authoritarian'),
    ('BLP_20251110_008', 'Pardoning Jan 6 rioters and punishing investigators', '48', '60', '48% view as authoritarian, 60% oppose'),
    ('BLP_20251110_009', 'Threatening Chris Christie', '48', '62', '48% view as authoritarian, 62% oppose'),
    ('BLP_20251110_010', 'Self-dealing/enrichment by Trump', '42', '64', '42% view as authoritarian, 64% oppose (highest opposition)'),
]
for mid, action, auth_pct, oppose_pct, note in auth_actions:
    rows.append({
        'message_id': mid,
        'source': 'Blueprint Research',
        'source_url': url12,
        'date': '2025-11-10',
        'topic': 'democracy',
        'issue_area': 'authoritarianism',
        'message_type': 'negative',
        'wording': f'Trump action: {action}',
        'support_pct': auth_pct if auth_pct else '',
        'oppose_pct': oppose_pct if oppose_pct else '',
        'net_score': '',
        'preference_effect': '', 'effect_scale': 'authoritarian_perception',
        'sample_size': '3028', 'methodology': 'online_panel', 'population': 'voters', 'moe': '2.1',
        'tags': f'blueprint;authoritarian;trump',
        'notes': note + '. 25 Trump actions tested.'
    })

# --- Article 13: View Alternate Universe (Oct 15, 2024) ---
url13 = 'https://blueprint-research.com/polling/distance-biden-ads-message-test-10-15/'
rows.append({
    'message_id': 'BLP_20241015_001',
    'source': 'Blueprint Research',
    'source_url': url13,
    'date': '2024-10-15',
    'topic': 'healthcare',
    'issue_area': 'medicare_at_home',
    'message_type': 'positive',
    'wording': 'Expand Medicare to cover at-home care for seniors',
    'support_pct': '', 'oppose_pct': '', 'net_score': '',
    'preference_effect': '10', 'effect_scale': 'preference_effect',
    'sample_size': '', 'methodology': 'online_panel', 'population': 'voters', 'moe': '',
    'tags': 'blueprint;medicare;at_home_care;seniors',
    'notes': 'Best distancing message. +10 overall, +10 independents.'
})
rows.append({
    'message_id': 'BLP_20241015_002',
    'source': 'Blueprint Research',
    'source_url': url13,
    'date': '2024-10-15',
    'topic': 'economy',
    'issue_area': 'price_gouging',
    'message_type': 'positive',
    'wording': 'Corporate price-gouging crackdown',
    'support_pct': '', 'oppose_pct': '', 'net_score': '',
    'preference_effect': '7', 'effect_scale': 'preference_effect',
    'sample_size': '', 'methodology': 'online_panel', 'population': 'voters', 'moe': '',
    'tags': 'blueprint;price_gouging;corporate',
    'notes': '+7 overall, +15 independents.'
})

# --- Article 14: Positive Beats Negative - Harris Ads (Aug 30, 2024) ---
url14 = 'https://blueprint-research.com/polling/ads-test-harris-8-30/'
rows.append({
    'message_id': 'BLP_20240830_001',
    'source': 'Blueprint Research',
    'source_url': url14,
    'date': '2024-08-30',
    'topic': 'abortion',
    'issue_area': 'abortion_contrast',
    'message_type': 'contrast',
    'wording': 'Abortion contrast ad: Harris vs. Trump on abortion rights',
    'support_pct': '', 'oppose_pct': '', 'net_score': '',
    'preference_effect': '3.5', 'effect_scale': 'preference_effect',
    'sample_size': '', 'methodology': 'online_panel', 'population': 'voters', 'moe': '',
    'tags': 'blueprint;ads;abortion;contrast',
    'notes': 'Best ad. +3.5 overall, +9.2 independents.'
})
rows.append({
    'message_id': 'BLP_20240830_002',
    'source': 'Blueprint Research',
    'source_url': url14,
    'date': '2024-08-30',
    'topic': 'healthcare',
    'issue_area': 'harris_healthcare',
    'message_type': 'positive',
    'wording': 'Positive Harris healthcare ad',
    'support_pct': '', 'oppose_pct': '', 'net_score': '',
    'preference_effect': '3.4', 'effect_scale': 'preference_effect',
    'sample_size': '', 'methodology': 'online_panel', 'population': 'voters', 'moe': '',
    'tags': 'blueprint;ads;healthcare;harris',
    'notes': '+3.4 overall preference effect.'
})
rows.append({
    'message_id': 'BLP_20240830_003',
    'source': 'Blueprint Research',
    'source_url': url14,
    'date': '2024-08-30',
    'topic': 'abortion',
    'issue_area': 'harris_abortion',
    'message_type': 'positive',
    'wording': 'Positive Harris abortion ad',
    'support_pct': '', 'oppose_pct': '', 'net_score': '',
    'preference_effect': '3.4', 'effect_scale': 'preference_effect',
    'sample_size': '', 'methodology': 'online_panel', 'population': 'voters', 'moe': '',
    'tags': 'blueprint;ads;abortion;harris',
    'notes': '+3.4 overall preference effect.'
})
rows.append({
    'message_id': 'BLP_20240830_004',
    'source': 'Blueprint Research',
    'source_url': url14,
    'date': '2024-08-30',
    'topic': 'healthcare',
    'issue_area': 'healthcare_contrast',
    'message_type': 'contrast',
    'wording': 'Healthcare contrast ad (Harris vs. Trump on healthcare)',
    'support_pct': '', 'oppose_pct': '', 'net_score': '',
    'preference_effect': '10.7', 'effect_scale': 'preference_effect',
    'sample_size': '', 'methodology': 'online_panel', 'population': 'independents', 'moe': '',
    'tags': 'blueprint;ads;healthcare;independents',
    'notes': 'Among independents: +10.7 preference effect.'
})
rows.append({
    'message_id': 'BLP_20240830_005',
    'source': 'Blueprint Research',
    'source_url': url14,
    'date': '2024-08-30',
    'topic': 'abortion',
    'issue_area': 'harris_abortion',
    'message_type': 'positive',
    'wording': 'Harris abortion ad (independents)',
    'support_pct': '', 'oppose_pct': '', 'net_score': '',
    'preference_effect': '10.3', 'effect_scale': 'preference_effect',
    'sample_size': '', 'methodology': 'online_panel', 'population': 'independents', 'moe': '',
    'tags': 'blueprint;ads;abortion;independents',
    'notes': 'Among independents: +10.3 preference effect.'
})
rows.append({
    'message_id': 'BLP_20240830_006',
    'source': 'Blueprint Research',
    'source_url': url14,
    'date': '2024-08-30',
    'topic': 'economy',
    'issue_area': 'tax_cuts',
    'message_type': 'negative',
    'wording': 'Trump tax cuts lead to healthcare cuts',
    'support_pct': '', 'oppose_pct': '', 'net_score': '',
    'preference_effect': '1.3', 'effect_scale': 'preference_effect',
    'sample_size': '', 'methodology': 'online_panel', 'population': 'voters', 'moe': '',
    'tags': 'blueprint;ads;tax_cuts;healthcare;lowest',
    'notes': 'Lowest performing ad. +1.3 preference effect.'
})
rows.append({
    'message_id': 'BLP_20240830_007',
    'source': 'Blueprint Research',
    'source_url': url14,
    'date': '2024-08-30',
    'topic': 'abortion',
    'issue_area': 'trump_anti_choice',
    'message_type': 'negative',
    'wording': 'Trump anti-choice agenda ad',
    'support_pct': '', 'oppose_pct': '', 'net_score': '',
    'preference_effect': '1.5', 'effect_scale': 'preference_effect',
    'sample_size': '', 'methodology': 'online_panel', 'population': 'voters', 'moe': '',
    'tags': 'blueprint;ads;abortion;trump;lowest',
    'notes': 'Lowest performing. +1.5 preference effect.'
})

# --- Article 15: Harris Unburdened (Jul 24, 2024) ---
url15 = 'https://blueprint-research.com/polling/harris-poll-message-test-7-24/'
rows.append({
    'message_id': 'BLP_20240724_001',
    'source': 'Blueprint Research',
    'source_url': url15,
    'date': '2024-07-24',
    'topic': 'economy',
    'issue_area': 'populist_economic',
    'message_type': 'positive',
    'wording': 'Populist economic message: deficit reduction, all-of-above energy, prosecute price-gouging, Medicare drug negotiation',
    'support_pct': '61', 'oppose_pct': '', 'net_score': '',
    'preference_effect': '', 'effect_scale': '',
    'sample_size': '', 'methodology': 'online_panel', 'population': 'voters', 'moe': '',
    'tags': 'blueprint;harris;populist;economic',
    'notes': 'Most compelling of 15 tested pro-Harris messages. 61% overall, 61% independents, 61% all age/gender groups, 64% non-college, 63% Republicans.'
})

# --- Article 17: Mad Libs Candidate / Build a Dem Workshop (Nov 14, 2025) ---
url17 = 'https://blueprint-research.com/polling/build-a-dem-workshop/'
# Already extracted: BLP_20250924_001 (SS/Medicare +21), BLP_20250924_002 (Food prices +20)
rows.append({
    'message_id': 'BLP_20251114_001',
    'source': 'Blueprint Research',
    'source_url': url17,
    'date': '2025-11-14',
    'topic': 'politics',
    'issue_area': 'candidate_bio',
    'message_type': 'positive',
    'wording': 'Working-class background (ideal Democrat bio trait)',
    'support_pct': '', 'oppose_pct': '', 'net_score': '',
    'preference_effect': '8', 'effect_scale': 'preference_effect',
    'sample_size': '3028', 'methodology': 'online_panel', 'population': 'voters', 'moe': '2.1',
    'tags': 'blueprint;candidate_bio;working_class',
    'notes': 'Ideal Democrat bio traits. Working-class +8, Veteran +8, Middle-class +8.'
})
rows.append({
    'message_id': 'BLP_20251114_002',
    'source': 'Blueprint Research',
    'source_url': url17,
    'date': '2025-11-14',
    'topic': 'politics',
    'issue_area': 'candidate_bio',
    'message_type': 'positive',
    'wording': 'Guided by science, evidence, and facts',
    'support_pct': '', 'oppose_pct': '', 'net_score': '',
    'preference_effect': '7', 'effect_scale': 'preference_effect',
    'sample_size': '3028', 'methodology': 'online_panel', 'population': 'voters', 'moe': '2.1',
    'tags': 'blueprint;candidate_bio;science',
    'notes': 'Ideal Democrat bio trait. +7 preference effect.'
})
rows.append({
    'message_id': 'BLP_20251114_003',
    'source': 'Blueprint Research',
    'source_url': url17,
    'date': '2025-11-14',
    'topic': 'economy',
    'issue_area': 'cost_of_living',
    'message_type': 'positive',
    'wording': 'Bringing down prices of food and goods',
    'support_pct': '', 'oppose_pct': '', 'net_score': '',
    'preference_effect': '20', 'effect_scale': 'preference_effect',
    'sample_size': '3028', 'methodology': 'online_panel', 'population': 'voters', 'moe': '2.1',
    'tags': 'blueprint;cost_of_living;food_prices',
    'notes': '+20 overall, +18 independents, +23 Democrats. Top issue priority.'
})
rows.append({
    'message_id': 'BLP_20251114_004',
    'source': 'Blueprint Research',
    'source_url': url17,
    'date': '2025-11-14',
    'topic': 'politics',
    'issue_area': 'candidate_bio',
    'message_type': 'positive',
    'wording': "Perfect candidate combined: Working-class veteran guided by science and facts, created jobs in private sector, believes in finding common ground. Running on protecting SS/Medicare, bringing down prices, making healthcare affordable.",
    'support_pct': '', 'oppose_pct': '', 'net_score': '',
    'preference_effect': '35', 'effect_scale': 'combined_preference',
    'sample_size': '3028', 'methodology': 'online_panel', 'population': 'voters', 'moe': '2.1',
    'tags': 'blueprint;candidate_bio;perfect_candidate',
    'notes': 'Combined preference effect of +35 for the perfect Democrat candidate.'
})
rows.append({
    'message_id': 'BLP_20251114_005',
    'source': 'Blueprint Research',
    'source_url': url17,
    'date': '2025-11-14',
    'topic': 'politics',
    'issue_area': 'candidate_bio',
    'message_type': 'negative',
    'wording': 'Billionaire background',
    'support_pct': '', 'oppose_pct': '', 'net_score': '',
    'preference_effect': '-11', 'effect_scale': 'preference_effect',
    'sample_size': '3028', 'methodology': 'online_panel', 'population': 'voters', 'moe': '2.1',
    'tags': 'blueprint;candidate_bio;billionaire;negative',
    'notes': 'What hurts a Democrat candidate. -11 overall, -18 Democrats.'
})
rows.append({
    'message_id': 'BLP_20251114_006',
    'source': 'Blueprint Research',
    'source_url': url17,
    'date': '2025-11-14',
    'topic': 'politics',
    'issue_area': 'candidate_bio',
    'message_type': 'negative',
    'wording': 'Socialist label',
    'support_pct': '', 'oppose_pct': '', 'net_score': '',
    'preference_effect': '-11', 'effect_scale': 'preference_effect',
    'sample_size': '3028', 'methodology': 'online_panel', 'population': 'voters', 'moe': '2.1',
    'tags': 'blueprint;candidate_bio;socialist;negative',
    'notes': '-11 overall, -9 independents.'
})
rows.append({
    'message_id': 'BLP_20251114_007',
    'source': 'Blueprint Research',
    'source_url': url17,
    'date': '2025-11-14',
    'topic': 'politics',
    'issue_area': 'candidate_bio',
    'message_type': 'negative',
    'wording': 'Podcaster background',
    'support_pct': '', 'oppose_pct': '', 'net_score': '',
    'preference_effect': '-9', 'effect_scale': 'preference_effect',
    'sample_size': '3028', 'methodology': 'online_panel', 'population': 'voters', 'moe': '2.1',
    'tags': 'blueprint;candidate_bio;podcaster;negative',
    'notes': '-9 preference effect.'
})

# --- Article 18: Haley Voters Part 2 (Oct 9-10, 2024) ---
url18_1 = 'https://blueprint-research.com/polling/haley-voters-10-9/'
url18_2 = 'https://blueprint-research.com/polling/haley-voters-10-10/'
rows.append({
    'message_id': 'BLP_20241009_001',
    'source': 'Blueprint Research',
    'source_url': url18_1,
    'date': '2024-10-09',
    'topic': 'economy',
    'issue_area': 'price_gouging',
    'message_type': 'policy',
    'wording': 'Law banning excessive grocery prices',
    'support_pct': '70', 'oppose_pct': '9', 'net_score': '+61',
    'preference_effect': '', 'effect_scale': '',
    'sample_size': '', 'methodology': 'online_panel', 'population': 'haley_voters', 'moe': '',
    'tags': 'blueprint;haley_voters;price_gouching;grocery',
    'notes': '70% support among Haley voters. Net +61. Part 2.'
})
rows.append({
    'message_id': 'BLP_20241009_002',
    'source': 'Blueprint Research',
    'source_url': url18_1,
    'date': '2024-10-09',
    'topic': 'social_security',
    'issue_area': 'ss_medicare',
    'message_type': 'positive',
    'wording': 'Harris message on protecting Social Security',
    'support_pct': '', 'oppose_pct': '', 'net_score': '',
    'preference_effect': '30', 'effect_scale': 'boost',
    'sample_size': '', 'methodology': 'online_panel', 'population': 'haley_voters', 'moe': '',
    'tags': 'blueprint;haley_voters;social_security;harris_boost',
    'notes': '+30 boost for Harris among Haley voters on protecting Social Security.'
})
rows.append({
    'message_id': 'BLP_20241009_003',
    'source': 'Blueprint Research',
    'source_url': url18_2,
    'date': '2024-10-10',
    'topic': 'social_security',
    'issue_area': 'ss_medicare_vs_tax_cuts',
    'message_type': 'contrast',
    'wording': 'Protecting Social Security and Medicare from Trump tax cuts',
    'support_pct': '', 'oppose_pct': '', 'net_score': '',
    'preference_effect': '21', 'effect_scale': 'boost',
    'sample_size': '', 'methodology': 'online_panel', 'population': 'haley_voters', 'moe': '',
    'tags': 'blueprint;haley_voters;ss_medicare;tax_cuts',
    'notes': 'Top message: +21 boost for Harris among Haley voters.'
})

# --- Article 20: Trump is New Joe Biden (Jan 21, 2026) ---
url20 = 'https://blueprint-research.com/polling/trump-economy-1-21/'
rows.append({
    'message_id': 'BLP_20260121_001',
    'source': 'Blueprint Research',
    'source_url': url20,
    'date': '2026-01-21',
    'topic': 'economy',
    'issue_area': 'affordability',
    'message_type': 'negative',
    'wording': 'Trump calls affordability a "fake narrative" or "con job"',
    'support_pct': '', 'oppose_pct': '', 'net_score': '',
    'preference_effect': '', 'effect_scale': 'net_concern',
    'sample_size': '', 'methodology': 'online_panel', 'population': 'voters', 'moe': '',
    'tags': 'blueprint;trump;economy;affordability;concern',
    'notes': 'Highest net concern. +12 Republicans, +33 independents.'
})
rows.append({
    'message_id': 'BLP_20260121_002',
    'source': 'Blueprint Research',
    'source_url': url20,
    'date': '2026-01-21',
    'topic': 'economy',
    'issue_area': 'regional_disparity',
    'message_type': 'negative',
    'wording': 'Bessent cites CEA study to suggest moving to red states',
    'support_pct': '', 'oppose_pct': '', 'net_score': '',
    'preference_effect': '', 'effect_scale': 'net_concern',
    'sample_size': '', 'methodology': 'online_panel', 'population': 'voters', 'moe': '',
    'tags': 'blueprint;trump;economy;bessent;red_states',
    'notes': '+27 overall, +27 independents net concern.'
})
rows.append({
    'message_id': 'BLP_20260121_003',
    'source': 'Blueprint Research',
    'source_url': url20,
    'date': '2026-01-21',
    'topic': 'economy',
    'issue_area': 'affordability',
    'message_type': 'negative',
    'wording': 'Trump says affordability is much better under his administration',
    'support_pct': '', 'oppose_pct': '', 'net_score': '',
    'preference_effect': '', 'effect_scale': 'net_concern',
    'sample_size': '', 'methodology': 'online_panel', 'population': 'independents', 'moe': '',
    'tags': 'blueprint;trump;economy;affordability;independents',
    'notes': '+27 net concern among independents.'
})

# --- Article 21: Trump-Musk Vulnerabilities (Mar 20, 2024) ---
url21 = 'https://blueprint-research.com/polling/trump-musk-vulnerabilities-3-20/'
rows.append({
    'message_id': 'BLP_20240320_001',
    'source': 'Blueprint Research',
    'source_url': url21,
    'date': '2024-03-20',
    'topic': 'politics',
    'issue_area': 'trump_approval',
    'message_type': 'tracking_poll',
    'wording': 'Trump job approval',
    'support_pct': '45', 'oppose_pct': '51', 'net_score': '-6',
    'preference_effect': '', 'effect_scale': 'net_approval',
    'sample_size': '', 'methodology': 'online_panel', 'population': 'voters', 'moe': '',
    'tags': 'blueprint;trump;approval;job_performance',
    'notes': 'Trump job approval: 45% approve, 51% disapprove. Net -6.'
})
rows.append({
    'message_id': 'BLP_20240320_002',
    'source': 'Blueprint Research',
    'source_url': url21,
    'date': '2024-03-20',
    'topic': 'politics',
    'issue_area': 'musk_favorability',
    'message_type': 'tracking_poll',
    'wording': 'Elon Musk favorability',
    'support_pct': '', 'oppose_pct': '', 'net_score': '-16',
    'preference_effect': '', 'effect_scale': 'net_favorability',
    'sample_size': '', 'methodology': 'online_panel', 'population': 'voters', 'moe': '',
    'tags': 'blueprint;musk;favorability',
    'notes': 'Musk net favorability: -16.'
})
rows.append({
    'message_id': 'BLP_20240320_003',
    'source': 'Blueprint Research',
    'source_url': url21,
    'date': '2024-03-20',
    'topic': 'politics',
    'issue_area': 'musk_admin_role',
    'message_type': 'tracking_poll',
    'wording': 'Elon Musk role in Trump administration approval',
    'support_pct': '38', 'oppose_pct': '56', 'net_score': '-18',
    'preference_effect': '', 'effect_scale': 'net_approval',
    'sample_size': '', 'methodology': 'online_panel', 'population': 'voters', 'moe': '',
    'tags': 'blueprint;musk;admin_role;approval',
    'notes': '38% approve, 56% disapprove of Musk role in administration. Net -18. Dems -82, Inds -28, Reps +55.'
})

# =============================================
# PART 2: NAVIGATOR RESEARCH (new extractions)
# =============================================

# --- Navigator: All Eyes Are On ICE (Feb 5, 2026) ---
nav_url_ice = 'https://navigatorresearch.org/all-eyes-are-on-ice/'
rows.append({
    'message_id': 'NAV_20260205_001',
    'source': 'Navigator Research',
    'source_url': nav_url_ice,
    'date': '2026-02-05',
    'topic': 'immigration',
    'issue_area': 'ice_deployment',
    'message_type': 'tracking_poll',
    'wording': 'Oppose the way Trump has deployed ICE',
    'support_pct': '', 'oppose_pct': '59', 'net_score': '',
    'preference_effect': '', 'effect_scale': 'opposition',
    'sample_size': '1000', 'methodology': 'online_panel', 'population': 'registered_voters', 'moe': '3.1',
    'tags': 'navigator;immigration;ice;deployment',
    'notes': 'All Eyes Are On ICE. Field: Jan 29 - Feb 1, 2026. 59% oppose ICE deployment.'
})
rows.append({
    'message_id': 'NAV_20260205_002',
    'source': 'Navigator Research',
    'source_url': nav_url_ice,
    'date': '2026-02-05',
    'topic': 'immigration',
    'issue_area': 'mass_deportation',
    'message_type': 'tracking_poll',
    'wording': 'Disapprove of Trump mass deportation plan',
    'support_pct': '', 'oppose_pct': '52', 'net_score': '',
    'preference_effect': '', 'effect_scale': 'disapproval',
    'sample_size': '1000', 'methodology': 'online_panel', 'population': 'registered_voters', 'moe': '3.1',
    'tags': 'navigator;immigration;mass_deportation;trump',
    'notes': '52% disapprove. In Jan 2025, 51% approved of the plan.'
})
rows.append({
    'message_id': 'NAV_20260205_003',
    'source': 'Navigator Research',
    'source_url': nav_url_ice,
    'date': '2026-02-05',
    'topic': 'immigration',
    'issue_area': 'balanced_approach',
    'message_type': 'tested_message',
    'wording': 'Support balanced approach on immigration: focus on fixing broken system rather than mass deportations',
    'support_pct': '66', 'oppose_pct': '25', 'net_score': '+41',
    'preference_effect': '', 'effect_scale': '',
    'sample_size': '1000', 'methodology': 'online_panel', 'population': 'registered_voters', 'moe': '3.1',
    'tags': 'navigator;immigration;balanced_approach',
    'notes': '66% support balanced approach. 25% support strict enforcement/mass deportations. Includes 48% of 2024 Trump voters.'
})
rows.append({
    'message_id': 'NAV_20260205_004',
    'source': 'Navigator Research',
    'source_url': nav_url_ice,
    'date': '2026-02-05',
    'topic': 'immigration',
    'issue_area': 'ice_violence',
    'message_type': 'tested_message',
    'wording': 'Worried that ICE agents will act violently due to lack of training',
    'support_pct': '65', 'oppose_pct': '', 'net_score': '',
    'preference_effect': '', 'effect_scale': 'concern',
    'sample_size': '1000', 'methodology': 'online_panel', 'population': 'registered_voters', 'moe': '3.1',
    'tags': 'navigator;immigration;ice_violence;concern',
    'notes': '65% worried (50% extremely worried). Inds 71%, Black 85%.'
})
rows.append({
    'message_id': 'NAV_20260205_005',
    'source': 'Navigator Research',
    'source_url': nav_url_ice,
    'date': '2026-02-05',
    'topic': 'immigration',
    'issue_area': 'ice_targeting',
    'message_type': 'tested_message',
    'wording': 'Worried ICE is targeting people based on appearance',
    'support_pct': '62', 'oppose_pct': '', 'net_score': '',
    'preference_effect': '', 'effect_scale': 'concern',
    'sample_size': '1000', 'methodology': 'online_panel', 'population': 'registered_voters', 'moe': '3.1',
    'tags': 'navigator;immigration;ice_targeting;concern',
    'notes': '62% worried (48% extremely).'
})
rows.append({
    'message_id': 'NAV_20260205_006',
    'source': 'Navigator Research',
    'source_url': nav_url_ice,
    'date': '2026-02-05',
    'topic': 'immigration',
    'issue_area': 'ice_family_separation',
    'message_type': 'tested_message',
    'wording': 'Worried ICE is detaining children and separating families',
    'support_pct': '63', 'oppose_pct': '', 'net_score': '',
    'preference_effect': '', 'effect_scale': 'concern',
    'sample_size': '1000', 'methodology': 'online_panel', 'population': 'registered_voters', 'moe': '3.1',
    'tags': 'navigator;immigration;family_separation;concern',
    'notes': '63% worried (47% extremely).'
})
rows.append({
    'message_id': 'NAV_20260205_007',
    'source': 'Navigator Research',
    'source_url': nav_url_ice,
    'date': '2026-02-05',
    'topic': 'immigration',
    'issue_area': 'ice_targeting_citizens',
    'message_type': 'tested_message',
    'wording': 'Worried ICE is targeting citizens and lawful residents',
    'support_pct': '60', 'oppose_pct': '', 'net_score': '',
    'preference_effect': '', 'effect_scale': 'concern',
    'sample_size': '1000', 'methodology': 'online_panel', 'population': 'registered_voters', 'moe': '3.1',
    'tags': 'navigator;immigration;ice_citizens;concern',
    'notes': '60% worried (46% extremely).'
})
rows.append({
    'message_id': 'NAV_20260205_008',
    'source': 'Navigator Research',
    'source_url': nav_url_ice,
    'date': '2026-02-05',
    'topic': 'immigration',
    'issue_area': 'ice_targeting_community',
    'message_type': 'tested_message',
    'wording': 'Worried ICE is targeting residents in your community',
    'support_pct': '58', 'oppose_pct': '', 'net_score': '',
    'preference_effect': '', 'effect_scale': 'concern',
    'sample_size': '1000', 'methodology': 'online_panel', 'population': 'registered_voters', 'moe': '3.1',
    'tags': 'navigator;immigration;ice_community;concern',
    'notes': '58% worried (44% extremely).'
})
# ICE message frames
ice_frames = [
    ('NAV_20260205_009', 'ICE should be going after violent criminals, but instead is being far too aggressive and broad in its approach.', 'Too aggressive and broad frame'),
    ('NAV_20260205_010', 'We are spending billions of dollars on ICE to terrorize our communities while cutting billions from things that help Americans get by, like health care and food assistance in Medicaid and SNAP.', 'Waste of money frame'),
    ('NAV_20260205_011', 'ICE is acting like a secret police force in a dictatorship that is completely loyal to Trump: masked agents are terrorizing communities and killing citizens.', 'Secret police force frame'),
    ('NAV_20260205_012', 'ICE is tearing families apart, detaining and zip-tying children and separating U.S. citizen children from their families.', 'Tearing families apart frame'),
    ('NAV_20260205_013', 'ICE is supposed to be making our communities safer, but they are making us less safe.', 'Makes communities less safe frame'),
]
for mid, wording, note in ice_frames:
    rows.append({
        'message_id': mid,
        'source': 'Navigator Research',
        'source_url': nav_url_ice,
        'date': '2026-02-05',
        'topic': 'immigration',
        'issue_area': 'ice_messaging',
        'message_type': 'tested_message',
        'wording': wording,
        'support_pct': '', 'oppose_pct': '', 'net_score': '',
        'preference_effect': '', 'effect_scale': '',
        'sample_size': '1000', 'methodology': 'online_panel', 'population': 'registered_voters', 'moe': '3.1',
        'tags': 'navigator;immigration;ice;message_frame',
        'notes': f'Top-testing message frame: {note}. Field: Jan 29 - Feb 1, 2026.'
    })

# --- Navigator: Government Shutdown Week 3 (Oct 23, 2025) ---
nav_url_gs3 = 'https://navigatorresearch.org/government-shutdown-week-3-message-guidance/'
rows.append({
    'message_id': 'NAV_20251023_001',
    'source': 'Navigator Research',
    'source_url': nav_url_gs3,
    'date': '2025-10-23',
    'topic': 'government',
    'issue_area': 'shutdown_process',
    'message_type': 'tested_message',
    'wording': 'Trump and Republicans in Congress have the power to end the shutdown. Trump and Republicans are in full control of the federal government, including the White House and Congress, and are responsible for getting the government back up and running.',
    'support_pct': '', 'oppose_pct': '', 'net_score': '+16',
    'preference_effect': '16', 'effect_scale': 'agreement_margin',
    'sample_size': '1000', 'methodology': 'online_panel', 'population': 'registered_voters', 'moe': '3.1',
    'tags': 'navigator;shutdown;process_message',
    'notes': 'Process message about government control. Net +16 agreement margin.'
})
rows.append({
    'message_id': 'NAV_20251023_002',
    'source': 'Navigator Research',
    'source_url': nav_url_gs3,
    'date': '2025-10-23',
    'topic': 'healthcare',
    'issue_area': 'shutdown_impact',
    'message_type': 'tested_message',
    'wording': 'Trump and Republicans in Congress have the power to end the shutdown. The shutdown would end today if Republicans would agree to a compromise that would prevent health insurance costs from going up for millions of Americans.',
    'support_pct': '', 'oppose_pct': '', 'net_score': '+26',
    'preference_effect': '26', 'effect_scale': 'agreement_margin',
    'sample_size': '1000', 'methodology': 'online_panel', 'population': 'registered_voters', 'moe': '3.1',
    'tags': 'navigator;shutdown;healthcare;impact_message',
    'notes': 'Impact message about health care. Net +26 agreement margin (+48 among soft partisans). Recommended message.'
})
rows.append({
    'message_id': 'NAV_20251023_003',
    'source': 'Navigator Research',
    'source_url': nav_url_gs3,
    'date': '2025-10-23',
    'topic': 'healthcare',
    'issue_area': 'health_subsidies',
    'message_type': 'tracking_poll',
    'wording': 'Support extending health care subsidies',
    'support_pct': '73', 'oppose_pct': '16', 'net_score': '+57',
    'preference_effect': '', 'effect_scale': '',
    'sample_size': '1000', 'methodology': 'online_panel', 'population': 'registered_voters', 'moe': '3.1',
    'tags': 'navigator;healthcare;subsidies',
    'notes': '73% support extending health care subsidies. Broad bipartisan support.'
})

# --- Navigator: Government Shutdown Week 4 (Oct 30, 2025) ---
nav_url_gs4 = 'https://navigatorresearch.org/government-shutdown-week-4-message-guidance/'
rows.append({
    'message_id': 'NAV_20251030_001',
    'source': 'Navigator Research',
    'source_url': nav_url_gs4,
    'date': '2025-10-30',
    'topic': 'economy',
    'issue_area': 'wasteful_spending',
    'message_type': 'tracking_poll',
    'wording': 'Oppose $170 million on private jets for Secretary Kristi Noem',
    'support_pct': '', 'oppose_pct': '76', 'net_score': '',
    'preference_effect': '', 'effect_scale': 'opposition',
    'sample_size': '1000', 'methodology': 'online_panel', 'population': 'registered_voters', 'moe': '3.1',
    'tags': 'navigator;wasteful_spending;noem;jets',
    'notes': '76% oppose (62% strongly). Field: Oct 23-27, 2025.'
})
rows.append({
    'message_id': 'NAV_20251030_002',
    'source': 'Navigator Research',
    'source_url': nav_url_gs4,
    'date': '2025-10-30',
    'topic': 'economy',
    'issue_area': 'wasteful_spending',
    'message_type': 'tracking_poll',
    'wording': 'Oppose White House ballroom project',
    'support_pct': '', 'oppose_pct': '70', 'net_score': '',
    'preference_effect': '', 'effect_scale': 'opposition',
    'sample_size': '1000', 'methodology': 'online_panel', 'population': 'registered_voters', 'moe': '3.1',
    'tags': 'navigator;wasteful_spending;ballroom',
    'notes': '70% oppose (59% strongly).'
})
rows.append({
    'message_id': 'NAV_20251030_003',
    'source': 'Navigator Research',
    'source_url': nav_url_gs4,
    'date': '2025-10-30',
    'topic': 'economy',
    'issue_area': 'tax_cuts',
    'message_type': 'tracking_poll',
    'wording': 'Oppose new tax cuts for billionaires',
    'support_pct': '', 'oppose_pct': '72', 'net_score': '',
    'preference_effect': '', 'effect_scale': 'opposition',
    'sample_size': '1000', 'methodology': 'online_panel', 'population': 'registered_voters', 'moe': '3.1',
    'tags': 'navigator;tax_cuts;billionaires',
    'notes': '72% oppose (59% strongly).'
})
rows.append({
    'message_id': 'NAV_20251030_004',
    'source': 'Navigator Research',
    'source_url': nav_url_gs4,
    'date': '2025-10-30',
    'topic': 'foreign_policy',
    'issue_area': 'argentina_bailout',
    'message_type': 'tracking_poll',
    'wording': 'Oppose bailing out Argentina economy',
    'support_pct': '', 'oppose_pct': '76', 'net_score': '',
    'preference_effect': '', 'effect_scale': 'opposition',
    'sample_size': '1000', 'methodology': 'online_panel', 'population': 'registered_voters', 'moe': '3.1',
    'tags': 'navigator;argentina;bailout;wasteful_spending',
    'notes': '76% oppose (57% strongly). Wedge issue within GOP (66% of Republicans oppose). 38% of independents most concerned.'
})
rows.append({
    'message_id': 'NAV_20251030_005',
    'source': 'Navigator Research',
    'source_url': nav_url_gs4,
    'date': '2025-10-30',
    'topic': 'government',
    'issue_area': 'shutdown_frame',
    'message_type': 'tested_message',
    'wording': "We're spending money on those items, while millions of Americans do not receive their paychecks and some will not receive back pay, and thousands will lose their jobs permanently",
    'support_pct': '', 'oppose_pct': '', 'net_score': '',
    'preference_effect': '35', 'effect_scale': 'frame_agreement',
    'sample_size': '1000', 'methodology': 'online_panel', 'population': 'registered_voters', 'moe': '3.1',
    'tags': 'navigator;shutdown;frame;paychecks',
    'notes': 'Frame A. 35% agree. Ties wasteful spending to lost paychecks and jobs.'
})
rows.append({
    'message_id': 'NAV_20251030_006',
    'source': 'Navigator Research',
    'source_url': nav_url_gs4,
    'date': '2025-10-30',
    'topic': 'healthcare',
    'issue_area': 'shutdown_healthcare',
    'message_type': 'tested_message',
    'wording': "We're spending money on those items, while millions of Americans will lose their health care completely and millions more will see their health care costs double",
    'support_pct': '', 'oppose_pct': '', 'net_score': '',
    'preference_effect': '33', 'effect_scale': 'frame_agreement',
    'sample_size': '1000', 'methodology': 'online_panel', 'population': 'registered_voters', 'moe': '3.1',
    'tags': 'navigator;shutdown;frame;healthcare',
    'notes': 'Frame B. 33% agree. Ties wasteful spending to healthcare loss.'
})
rows.append({
    'message_id': 'NAV_20251030_007',
    'source': 'Navigator Research',
    'source_url': nav_url_gs4,
    'date': '2025-10-30',
    'topic': 'government',
    'issue_area': 'shutdown_combined',
    'message_type': 'tested_message',
    'wording': 'Trump and Republicans are spending money on everything except what benefits American families. In the last few weeks, they have announced the spending of $40 billion on a bailout of Argentina, $170 million on two private jets for Secretary of Homeland Security Kristi Noem, and $300 million to build a White House ballroom. At the same time, they are keeping the government shut down because they refuse to help Americans with rising health care costs, and instead could strip nearly 5 million of their health insurance and double the cost of health insurance for millions more.',
    'support_pct': '', 'oppose_pct': '', 'net_score': '',
    'preference_effect': '', 'effect_scale': 'most_effective',
    'sample_size': '1000', 'methodology': 'online_panel', 'population': 'registered_voters', 'moe': '3.1',
    'tags': 'navigator;shutdown;combined_message',
    'notes': 'Most effective combined message tying wasteful spending to shutdown consequences.'
})
rows.append({
    'message_id': 'NAV_20251030_008',
    'source': 'Navigator Research',
    'source_url': nav_url_gs4,
    'date': '2025-10-30',
    'topic': 'government',
    'issue_area': 'progressive_message',
    'message_type': 'tested_message',
    'wording': 'Trump and Republicans are spending billions on foreign aid and conflicts, including a $40 billion bailout of Argentina... Meanwhile, Trump and Republicans are doing nothing for us at home - keeping the government shut down and pushing to strip health care from millions of Americans...',
    'support_pct': '', 'oppose_pct': '', 'net_score': '+14',
    'preference_effect': '14', 'effect_scale': 'net_vs_conservative',
    'sample_size': '1000', 'methodology': 'online_panel', 'population': 'registered_voters', 'moe': '3.1',
    'tags': 'navigator;shutdown;progressive;message_test',
    'notes': 'Progressive message 1. Won net +14 against conservative argument.'
})
rows.append({
    'message_id': 'NAV_20251030_009',
    'source': 'Navigator Research',
    'source_url': nav_url_gs4,
    'date': '2025-10-30',
    'topic': 'healthcare',
    'issue_area': 'shutdown_healthcare_costs',
    'message_type': 'tested_message',
    'wording': "Trump and Republicans' budget would more than double health care costs for 22 million Americans. Democrats say health care costs have already been skyrocketing, and so they are doing everything they can to stop health care costs from rising even more...",
    'support_pct': '', 'oppose_pct': '', 'net_score': '+14',
    'preference_effect': '14', 'effect_scale': 'net_vs_conservative',
    'sample_size': '1000', 'methodology': 'online_panel', 'population': 'registered_voters', 'moe': '3.1',
    'tags': 'navigator;shutdown;healthcare_costs;progressive',
    'notes': 'Progressive message 2. Won net +14 against conservative argument.'
})

# --- Navigator: Tariff SCOTUS Ruling (Feb 20, 2026) ---
nav_url_tariff = 'https://navigatorresearch.org/message-guidance-on-tariff-scotus-ruling/'
rows.append({
    'message_id': 'NAV_20260220_001',
    'source': 'Navigator Research',
    'source_url': nav_url_tariff,
    'date': '2026-02-20',
    'topic': 'economy',
    'issue_area': 'tariffs',
    'message_type': 'tracking_poll',
    'wording': 'Tariff favorability — unfavorable',
    'support_pct': '30', 'oppose_pct': '60', 'net_score': '-30',
    'preference_effect': '', 'effect_scale': 'net_favorability',
    'sample_size': '1000', 'methodology': 'online_panel', 'population': 'registered_voters', 'moe': '3.1',
    'tags': 'navigator;tariffs;favorability',
    'notes': 'Tariffs 30 points underwater. Field: Jan 8-12, 2026.'
})
rows.append({
    'message_id': 'NAV_20260220_002',
    'source': 'Navigator Research',
    'source_url': nav_url_tariff,
    'date': '2026-02-20',
    'topic': 'economy',
    'issue_area': 'tariffs',
    'message_type': 'tracking_poll',
    'wording': 'Oppose Trump tariff plan',
    'support_pct': '', 'oppose_pct': '55', 'net_score': '',
    'preference_effect': '', 'effect_scale': 'opposition',
    'sample_size': '1000', 'methodology': 'online_panel', 'population': 'registered_voters', 'moe': '3.1',
    'tags': 'navigator;tariffs;trump_plan',
    'notes': '55% oppose Trump tariff plan. 38% support. 88% of Dems, 55% of Inds oppose.'
})
rows.append({
    'message_id': 'NAV_20260220_003',
    'source': 'Navigator Research',
    'source_url': nav_url_tariff,
    'date': '2026-02-20',
    'topic': 'economy',
    'issue_area': 'tariffs',
    'message_type': 'tracking_poll',
    'wording': 'Say tariffs increased their costs',
    'support_pct': '69', 'oppose_pct': '10', 'net_score': '',
    'preference_effect': '', 'effect_scale': 'perception',
    'sample_size': '1000', 'methodology': 'online_panel', 'population': 'registered_voters', 'moe': '3.1',
    'tags': 'navigator;tariffs;cost_impact',
    'notes': '69% say tariffs increased costs. Only 10% say costs went down. 52% of Republicans agree costs increased.'
})
rows.append({
    'message_id': 'NAV_20260220_004',
    'source': 'Navigator Research',
    'source_url': nav_url_tariff,
    'date': '2026-02-20',
    'topic': 'economy',
    'issue_area': 'inflation',
    'message_type': 'tracking_poll',
    'wording': 'Disapprove of Trump handling of inflation and cost of living',
    'support_pct': '37', 'oppose_pct': '58', 'net_score': '-21',
    'preference_effect': '', 'effect_scale': 'approval',
    'sample_size': '1000', 'methodology': 'online_panel', 'population': 'registered_voters', 'moe': '3.1',
    'tags': 'navigator;economy;inflation;trump_approval',
    'notes': '58% disapprove, 37% approve of Trump handling of inflation/cost of living.'
})

# --- Navigator: Views on Republican Tax Policies (Apr 14, 2026) ---
nav_url_tax = 'https://navigatorresearch.org/views-on-republican-tax-policies/'
rows.append({
    'message_id': 'NAV_20260414_001',
    'source': 'Navigator Research',
    'source_url': nav_url_tax,
    'date': '2026-04-14',
    'topic': 'economy',
    'issue_area': 'tax_policy',
    'message_type': 'tracking_poll',
    'wording': 'Republican tax law favorability',
    'support_pct': '36', 'oppose_pct': '49', 'net_score': '-13',
    'preference_effect': '', 'effect_scale': 'net_favorability',
    'sample_size': '1000', 'methodology': 'online_panel', 'population': 'registered_voters', 'moe': '3.1',
    'tags': 'navigator;tax;gop_tax_law',
    'notes': 'Republican tax law remains net -13 unfavorable. Field: Apr 2-6, 2026.'
})
rows.append({
    'message_id': 'NAV_20260414_002',
    'source': 'Navigator Research',
    'source_url': nav_url_tax,
    'date': '2026-04-14',
    'topic': 'economy',
    'issue_area': 'tax_trust',
    'message_type': 'tracking_poll',
    'wording': 'Trust Democrats vs. Republicans on taxes (tied at 34%)',
    'support_pct': '34', 'oppose_pct': '34', 'net_score': '0',
    'preference_effect': '', 'effect_scale': 'trust',
    'sample_size': '1000', 'methodology': 'online_panel', 'population': 'registered_voters', 'moe': '3.1',
    'tags': 'navigator;tax;trust;democrats;republicans',
    'notes': 'Trust on taxes: Democrats 34%, Trump/Republicans 34%. Republicans lost 6-pt advantage from Jan 2026. 24% trust neither.'
})
rows.append({
    'message_id': 'NAV_20260414_003',
    'source': 'Navigator Research',
    'source_url': nav_url_tax,
    'date': '2026-04-14',
    'topic': 'economy',
    'issue_area': 'tax_policy',
    'message_type': 'tracking_poll',
    'wording': 'Tax law does not benefit the middle class',
    'support_pct': '48', 'oppose_pct': '28', 'net_score': '+20',
    'preference_effect': '', 'effect_scale': 'agreement',
    'sample_size': '1000', 'methodology': 'online_panel', 'population': 'registered_voters', 'moe': '3.1',
    'tags': 'navigator;tax;middle_class',
    'notes': '48% agree tax law does not benefit middle class. 24% say "don\'t know enough to say."'
})
rows.append({
    'message_id': 'NAV_20260414_004',
    'source': 'Navigator Research',
    'source_url': nav_url_tax,
    'date': '2026-04-14',
    'topic': 'economy',
    'issue_area': 'tax_policy',
    'message_type': 'tracking_poll',
    'wording': 'Costs of tax law outweigh benefits',
    'support_pct': '44', 'oppose_pct': '31', 'net_score': '+13',
    'preference_effect': '', 'effect_scale': 'agreement',
    'sample_size': '1000', 'methodology': 'online_panel', 'population': 'registered_voters', 'moe': '3.1',
    'tags': 'navigator;tax;costs_vs_benefits',
    'notes': '44% agree costs outweigh benefits.'
})
rows.append({
    'message_id': 'NAV_20260414_005',
    'source': 'Navigator Research',
    'source_url': nav_url_tax,
    'date': '2026-04-14',
    'topic': 'economy',
    'issue_area': 'tax_policy',
    'message_type': 'rebuttal',
    'wording': 'Democrats say the One Big Beautiful Bill cuts programs people depend on, like Medicaid and SNAP, to pay for tax cuts for billionaires and big corporations, leaving millions unable to put food on the table or afford health care.',
    'support_pct': '', 'oppose_pct': '', 'net_score': '',
    'preference_effect': '', 'effect_scale': '',
    'sample_size': '1000', 'methodology': 'online_panel', 'population': 'registered_voters', 'moe': '3.1',
    'tags': 'navigator;tax;medicaid;snap;billionaires;rebuttal',
    'notes': 'Most effective rebuttal message against Republican tax law.'
})
rows.append({
    'message_id': 'NAV_20260414_006',
    'source': 'Navigator Research',
    'source_url': nav_url_tax,
    'date': '2026-04-14',
    'topic': 'economy',
    'issue_area': 'tariffs',
    'message_type': 'rebuttal',
    'wording': 'Democrats say because of Trump and Republicans, the average American could pay thousands more this year in costs because of tariffs and increased gas prices, which would wipe out any possible savings from the One Big Beautiful Bill.',
    'support_pct': '', 'oppose_pct': '', 'net_score': '',
    'preference_effect': '', 'effect_scale': '',
    'sample_size': '1000', 'methodology': 'online_panel', 'population': 'registered_voters', 'moe': '3.1',
    'tags': 'navigator;tax;tariffs;gas_prices;rebuttal',
    'notes': 'Still effective rebuttal: tariffs and gas prices wipe out tax savings.'
})

# --- Navigator: Perceptions of Trump's War Against Iran (Mar 18, 2026) ---
nav_url_iran = 'https://navigatorresearch.org/perceptions-and-concerns-about-trumps-war-against-iran/'
rows.append({
    'message_id': 'NAV_20260318_001',
    'source': 'Navigator Research',
    'source_url': nav_url_iran,
    'date': '2026-03-18',
    'topic': 'foreign_policy',
    'issue_area': 'iran_war',
    'message_type': 'tracking_poll',
    'wording': 'Support vs. oppose US military operation against Iran',
    'support_pct': '40', 'oppose_pct': '49', 'net_score': '-9',
    'preference_effect': '', 'effect_scale': 'support_oppose',
    'sample_size': '1000', 'methodology': 'online_panel', 'population': 'registered_voters', 'moe': '3.1',
    'tags': 'navigator;iran;war;opposition',
    'notes': 'Opposition leads by 9 pts. Field: Mar 12-16, 2026. 74% of Dems oppose, 52% of Inds oppose.'
})
rows.append({
    'message_id': 'NAV_20260318_002',
    'source': 'Navigator Research',
    'source_url': nav_url_iran,
    'date': '2026-03-18',
    'topic': 'foreign_policy',
    'issue_area': 'iran_war',
    'message_type': 'tracking_poll',
    'wording': 'Trump does not have clear timeline or goals for Iran operation',
    'support_pct': '53', 'oppose_pct': '', 'net_score': '',
    'preference_effect': '', 'effect_scale': 'agreement',
    'sample_size': '1000', 'methodology': 'online_panel', 'population': 'registered_voters', 'moe': '3.1',
    'tags': 'navigator;iran;trump;timeline',
    'notes': '53% believe Trump has no clear timeline or goals.'
})
rows.append({
    'message_id': 'NAV_20260318_003',
    'source': 'Navigator Research',
    'source_url': nav_url_iran,
    'date': '2026-03-18',
    'topic': 'foreign_policy',
    'issue_area': 'iran_war',
    'message_type': 'tracking_poll',
    'wording': 'Concerned the US will get bogged down in prolonged conflict with Iran',
    'support_pct': '67', 'oppose_pct': '', 'net_score': '',
    'preference_effect': '', 'effect_scale': 'concern',
    'sample_size': '1000', 'methodology': 'online_panel', 'population': 'registered_voters', 'moe': '3.1',
    'tags': 'navigator;iran;prolonged_conflict;concern',
    'notes': '67% concerned about prolonged conflict.'
})
rows.append({
    'message_id': 'NAV_20260318_004',
    'source': 'Navigator Research',
    'source_url': nav_url_iran,
    'date': '2026-03-18',
    'topic': 'foreign_policy',
    'issue_area': 'iran_war',
    'message_type': 'tracking_poll',
    'wording': 'Think Iran conflict will last months or longer',
    'support_pct': '53', 'oppose_pct': '', 'net_score': '',
    'preference_effect': '', 'effect_scale': 'expectation',
    'sample_size': '1000', 'methodology': 'online_panel', 'population': 'registered_voters', 'moe': '3.1',
    'tags': 'navigator;iran;duration;expectation',
    'notes': '53% think months or longer. 30% say a year or longer.'
})
rows.append({
    'message_id': 'NAV_20260318_005',
    'source': 'Navigator Research',
    'source_url': nav_url_iran,
    'date': '2026-03-18',
    'topic': 'foreign_policy',
    'issue_area': 'iran_war',
    'message_type': 'tracking_poll',
    'wording': 'Say Iran operation has made the world less safe',
    'support_pct': '46', 'oppose_pct': '28', 'net_score': '',
    'preference_effect': '', 'effect_scale': 'perception',
    'sample_size': '1000', 'methodology': 'online_panel', 'population': 'registered_voters', 'moe': '3.1',
    'tags': 'navigator;iran;safety',
    'notes': '46% say world is less safe. 28% say safer.'
})
rows.append({
    'message_id': 'NAV_20260318_006',
    'source': 'Navigator Research',
    'source_url': nav_url_iran,
    'date': '2026-03-18',
    'topic': 'foreign_policy',
    'issue_area': 'iran_funding',
    'message_type': 'tracking_poll',
    'wording': 'Oppose providing additional $50 billion in Iran war funding',
    'support_pct': '34', 'oppose_pct': '54', 'net_score': '-20',
    'preference_effect': '', 'effect_scale': 'opposition',
    'sample_size': '1000', 'methodology': 'online_panel', 'population': 'registered_voters', 'moe': '3.1',
    'tags': 'navigator;iran;funding;opposition',
    'notes': '54% oppose additional $50 billion in funding.'
})
rows.append({
    'message_id': 'NAV_20260318_007',
    'source': 'Navigator Research',
    'source_url': nav_url_iran,
    'date': '2026-03-18',
    'topic': 'foreign_policy',
    'issue_area': 'iran_war',
    'message_type': 'tracking_poll',
    'wording': 'Want Trump and Congress to prioritize inflation and cost of living over foreign conflicts',
    'support_pct': '58', 'oppose_pct': '', 'net_score': '',
    'preference_effect': '', 'effect_scale': 'priority',
    'sample_size': '1000', 'methodology': 'online_panel', 'population': 'registered_voters', 'moe': '3.1',
    'tags': 'navigator;inflation;priorities;iran',
    'notes': '58% want inflation/cost of living prioritized. Perceive Trump focused on immigration (64%) and foreign conflicts (54%).'
})

# --- Navigator: MAHA Message Guidance (Sep 25, 2025) ---
nav_url_maha = 'https://navigatorresearch.org/maha-message-guidance/'
rows.append({
    'message_id': 'NAV_20250925_001',
    'source': 'Navigator Research',
    'source_url': nav_url_maha,
    'date': '2025-09-25',
    'topic': 'healthcare',
    'issue_area': 'maha',
    'message_type': 'tested_message',
    'wording': 'Our health care system is broken, but the answer is not to cut medical research, take away healthy school meal options from kids, or limit vaccines. Instead we should be cracking down on special interest influence in our government and putting science and facts ahead of politics.',
    'support_pct': '', 'oppose_pct': '', 'net_score': '',
    'preference_effect': '', 'effect_scale': '',
    'sample_size': '1000', 'methodology': 'online_panel', 'population': 'registered_voters', 'moe': '3.1',
    'tags': 'navigator;healthcare;maha;message_framework',
    'notes': 'Recommended message framework targeting MAHA movement. Persuasive across Dems, Inds, non-MAGA Reps, MAHA-curious. Field: Sep 4-8, 2025.'
})

# Write CSV
output_path = '/home/agentbot/workspace/us-political-messaging-dataset/data/processed/new_extracted_messages.csv'
fieldnames = [
    'message_id', 'source', 'source_url', 'date', 'topic', 'issue_area',
    'message_type', 'wording', 'support_pct', 'oppose_pct', 'net_score',
    'preference_effect', 'effect_scale', 'sample_size', 'methodology',
    'population', 'moe', 'tags', 'notes'
]

with open(output_path, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for row in rows:
        writer.writerow(row)

print(f"✅ Wrote {len(rows)} rows to {output_path}")
print(f"\nBreakdown by source:")
blueprint = sum(1 for r in rows if r['source'] == 'Blueprint Research')
navigator = sum(1 for r in rows if r['source'] == 'Navigator Research')
print(f"  Blueprint Research: {blueprint}")
print(f"  Navigator Research: {navigator}")
print(f"  Total: {len(rows)}")
