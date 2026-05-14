#!/usr/bin/env python3
"""Add MAHA policies + shutdown change articles."""
import csv, re
from pathlib import Path
from collections import Counter

BASE = Path(__file__).parent.parent
PROC = BASE / "data" / "processed"

msg_fieldnames = [
    'message_id', 'source', 'source_url', 'date', 'topic', 'issue_area',
    'message_type', 'wording', 'support_pct', 'oppose_pct', 'net_score',
    'preference_effect', 'effect_scale', 'sample_size', 'methodology',
    'population', 'moe', 'tags', 'notes'
]

with open(PROC / 'messages.csv', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    existing = list(reader)
existing_ids = set(r['message_id'] for r in existing)

nav_nums = []
for r in existing:
    m = re.search(r'NAV_(\d+)', r['message_id'])
    if m: nav_nums.append(int(m.group(1)))
next_nav = max(nav_nums) + 1 if nav_nums else 100

def add(**kw):
    global next_nav
    kw['message_id'] = f"NAV_{next_nav:04d}"
    next_nav += 1
    kw['source'] = 'Navigator Research'
    row = {k: '' for k in msg_fieldnames}
    row.update(kw)
    existing.append(row)
    existing_ids.add(row['message_id'])

# === 1. MAHA Policies and Messages ===
u1 = "https://navigatorresearch.org/maha-the-policies-and-messages/"
add(source_url=u1, date='2025-09-25', topic='healthcare', issue_area='vaccines',
    message_type='tracking_poll',
    wording='Oppose changing childhood vaccine mandates in Florida — including 54% of MAHA curious',
    support_pct='63', sample_size='1000', methodology='online_panel', population='registered_voters', moe='3.1',
    tags='navigator;vaccines;mandates;maha',
    notes='From: MAHA Policies and Messages. 63% oppose Florida changes. Inds 60% oppose.')
add(source_url=u1, date='2025-09-25', topic='healthcare', issue_area='vaccines',
    message_type='tracking_poll',
    wording='Measles vaccine favorability — net +66 overall, net +49 among MAHA curious',
    support_pct='', net_score='+66', effect_scale='net_favorability',
    sample_size='1000', methodology='online_panel', population='registered_voters', moe='3.1',
    tags='navigator;measles;vaccine;favorability',
    notes='From: MAHA Policies. Measles vaccine +66 net. Anti-vaccine movement -41 net overall.')
add(source_url=u1, date='2025-09-25', topic='healthcare', issue_area='vaccines',
    message_type='tracking_poll',
    wording='Identify as pro-vaccine — 68% overall vs 20% anti-vaccine and 12% neither',
    support_pct='68', oppose_pct='20', net_score='+48', effect_scale='identification',
    sample_size='1000', methodology='online_panel', population='registered_voters', moe='3.1',
    tags='navigator;vaccine;pro_vaccine;identification',
    notes='From: MAHA Policies. 68% pro-vaccine. COVID vaccine only +11 net.')
add(source_url=u1, date='2025-09-25', topic='healthcare', issue_area='public_health',
    message_type='tracking_poll',
    wording='Support banning artificial food dyes from all foods — broad bipartisan health/wellness policy',
    support_pct='', sample_size='1000', methodology='online_panel', population='registered_voters', moe='3.1',
    tags='navigator;food_dyes;public_health;bipartisan',
    notes='From: MAHA Policies. Broad bipartisan support for health/wellness policies: preventative care, exercise, removing processed foods from schools.')
add(source_url=u1, date='2025-09-25', topic='healthcare', issue_area='public_health',
    message_type='tracking_poll',
    wording='Support banning forever chemicals (PFAS) from drinking water — broad bipartisan support',
    support_pct='', sample_size='1000', methodology='online_panel', population='registered_voters', moe='3.1',
    tags='navigator;pfas;water;public_health',
    notes='From: MAHA Policies. Also: decrease pesticides, medical research funding, preventative care coverage.')
add(source_url=u1, date='2025-09-25', topic='healthcare', issue_area='maha_messaging',
    message_type='tested_message',
    wording='Our health care system is broken, but the answer is not to cut medical research, take away healthy school meal options from kids, or limit vaccines. Instead we should be cracking down on special interest influence in our government and putting science and facts ahead of politics',
    support_pct='60', sample_size='1000', methodology='online_panel', population='registered_voters', moe='3.1',
    tags='navigator;maha;messaging;progressive',
    notes='From: MAHA Policies. Most persuasive progressive response (60% agreed). Persuasive across MAHA curious and Independents.')
add(source_url=u1, date='2025-09-25', topic='healthcare', issue_area='maha_messaging',
    message_type='tested_message',
    wording='Republicans are cutting crucial health and wellness programs. They have cut Medicaid, taken away free healthy school meal options from kids, and made massive cuts to lifesaving research into diseases like cancer and Alzheimer\'s. None of this makes America healthier',
    support_pct='49', sample_size='1000', methodology='online_panel', population='registered_voters', moe='3.1',
    tags='navigator;gop;cuts;healthcare',
    notes='From: MAHA Policies. Best hit on GOP policies - 49% found convincing.')

# === 2. How Americans Views of the Shutdown Changed ===
u2 = "https://navigatorresearch.org/how-americans-views-of-the-shutdown-changed/"
add(source_url=u2, date='2025-11-12', topic='government', issue_area='shutdown_blame',
    message_type='tracking_poll',
    wording='Blame Trump and Republicans for the government shutdown — consistent across six weeks',
    support_pct='48', oppose_pct='34', net_score='+14', effect_scale='blame',
    sample_size='1000', methodology='online_panel', population='registered_voters', moe='3.1',
    tags='navigator;shutdown;blame;gop',
    notes='From: How Views of Shutdown Changed. 48% blame GOP, 34% blame Dems. Field: Nov 6-9, 2025.')
add(source_url=u2, date='2025-11-12', topic='government', issue_area='shutdown_awareness',
    message_type='tracking_poll',
    wording='Heard about the government shutdown — 87% awareness, up 47 points from before it began',
    support_pct='87', sample_size='1000', methodology='online_panel', population='registered_voters', moe='3.1',
    tags='navigator;shutdown;awareness',
    notes='From: How Views of Shutdown Changed. 87% heard (57% a lot). 85% concerned.')
add(source_url=u2, date='2025-11-12', topic='government', issue_area='shutdown_impact',
    message_type='tracking_poll',
    wording='Believe the shutdown is bad for the country — up 17 points to 85% during six-week shutdown',
    support_pct='85', sample_size='1000', methodology='online_panel', population='registered_voters', moe='3.1',
    tags='navigator;shutdown;impact;country',
    notes='From: How Views of Shutdown Changed. 85% say bad for country (up from 68%). 65% say bad personally (up from 42%).')
add(source_url=u2, date='2025-11-12', topic='government', issue_area='trump_approval',
    message_type='tracking_poll',
    wording='Trump overall job approval during shutdown — net -18, down 8 points from before shutdown',
    support_pct='', net_score='-18', effect_scale='approval',
    sample_size='1000', methodology='online_panel', population='registered_voters', moe='3.1',
    tags='navigator;trump;approval;shutdown',
    notes='From: How Views of Shutdown Changed. Overall approval -8 pts during shutdown. Economic approval -6 pts.')
add(source_url=u2, date='2025-11-12', topic='economy', issue_area='healthcare_costs',
    message_type='tracking_poll',
    wording='Say cost of healthcare is going up — up 13 points since July during shutdown period',
    support_pct='73', sample_size='1000', methodology='online_panel', population='registered_voters', moe='3.1',
    tags='navigator;healthcare;costs;shutdown',
    notes='From: How Views of Shutdown Changed. 73% say healthcare costs up (+13 pts since July). 49-pt margin say premiums up.')
add(source_url=u2, date='2025-11-12', topic='government', issue_area='wasteful_spending',
    message_type='tracking_poll',
    wording='Say Trump excessive spending on White House ballroom, gold fixtures, and private jets is inappropriate while millions lack food assistance',
    support_pct='69', sample_size='1000', methodology='online_panel', population='registered_voters', moe='3.1',
    tags='navigator;wasteful_spending;trump;inappropriate',
    notes='From: How Views of Shutdown Changed. 69% say inappropriate.')
add(source_url=u2, date='2025-11-12', topic='economy', issue_area='snap',
    message_type='tracking_poll',
    wording='Blame Trump and Republicans for SNAP funding lapse (food stamps during shutdown)',
    support_pct='52', oppose_pct='32', net_score='+20', effect_scale='blame',
    sample_size='1000', methodology='online_panel', population='registered_voters', moe='3.1',
    tags='navigator;snap;food_stamps;shutdown',
    notes='From: How Views of Shutdown Changed. 52% blame GOP for SNAP lapse vs 32% blame Dems.')
add(source_url=u2, date='2025-11-12', topic='healthcare', issue_area='healthcare_costs',
    message_type='tracking_poll',
    wording='Blame Trump and Republicans for healthcare premium increases — 26-point margin over Democrats',
    support_pct='47', oppose_pct='21', net_score='+26', effect_scale='blame',
    sample_size='1000', methodology='online_panel', population='registered_voters', moe='3.1',
    tags='navigator;healthcare;premiums;blame',
    notes='From: How Views of Shutdown Changed. 47% blame GOP for premium increases vs 21% blame Dems.')

print(f"Total: {len(existing)}")

with open(PROC / 'messages.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=msg_fieldnames)
    writer.writeheader()
    writer.writerows(existing)

sources = Counter(r['source'] for r in existing)
has_m = sum(1 for r in existing if r.get('support_pct','').strip() or r.get('preference_effect','').strip() or r.get('net_score','').strip())
print(f"With metrics: {has_m}")
for s,c in sources.most_common():
    sm = sum(1 for r in existing if r['source']==s and (r.get('support_pct','').strip() or r.get('preference_effect','').strip() or r.get('net_score','').strip()))
    print(f"  {s}: {c} ({sm} with metrics)")
print(f"\nGap to 500: {500 - len(existing)}")