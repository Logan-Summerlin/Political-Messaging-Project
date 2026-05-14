#!/usr/bin/env python3
"""Add Greenland + Holidays costs articles."""
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

# === 1. Americans Don't Want Greenland ===
u1 = "https://navigatorresearch.org/americans-dont-want-greenland-they-just-want-lower-costs/"
add(source_url=u1, date='2026-01-15', topic='foreign_policy', issue_area='greenland',
    message_type='tracking_poll',
    wording='Oppose US taking control of Greenland — opposed 57% to 23%',
    support_pct='23', oppose_pct='57', net_score='-34', effect_scale='support_oppose',
    sample_size='1000', methodology='online_panel', population='registered_voters', moe='3.1',
    tags='navigator;greenland;opposition;trump',
    notes='From: Don\'t Want Greenland article. 57% oppose, 23% support. Non-MAGA Republicans oppose by 34 pts. Field: Jan 8-12, 2026.')
add(source_url=u1, date='2026-01-15', topic='foreign_policy', issue_area='venezuela',
    message_type='tracking_poll',
    wording='Oppose the US taking control and running Venezuela — majority oppose running the country',
    support_pct='37', oppose_pct='53', net_score='-16', effect_scale='support_oppose',
    sample_size='1000', methodology='online_panel', population='registered_voters', moe='3.1',
    tags='navigator;venezuela;military_operation;opposition',
    notes='From: Greenland article. 43%-43% split on operation. 53% oppose running the country.')
add(source_url=u1, date='2026-01-15', topic='foreign_policy', issue_area='military_force',
    message_type='tracking_poll',
    wording='Agree US should be cautious about using military force abroad and instead focus priorities at home',
    support_pct='72', sample_size='1000', methodology='online_panel', population='registered_voters', moe='3.1',
    tags='navigator;military;cautious;priorities',
    notes='From: Greenland article. 72% agree US cautious. 28% disagree. Same split even with toppling dictators context.')
add(source_url=u1, date='2026-01-15', topic='immigration', issue_area='ice',
    message_type='tracking_poll',
    wording='ICE net favorability — dropped from -8 to -20 after Renee Good shooting',
    support_pct='37', oppose_pct='57', net_score='-20', effect_scale='net_favorability',
    sample_size='1000', methodology='online_panel', population='registered_voters', moe='3.1',
    tags='navigator;ice;favorability;decline',
    notes='From: Greenland article. ICE -20 net. Was -8 in summer 2025. 59% say too aggressive (up from 52%).')
add(source_url=u1, date='2026-01-15', topic='economy', issue_area='priorities_mismatch',
    message_type='tracking_poll',
    wording='Say Trump and Republicans are focused on immigration and border (62%) — but only 27% say it should be a priority. Cost of living should be top focus (54-56% across parties)',
    support_pct='62', sample_size='1000', methodology='online_panel', population='registered_voters', moe='3.1',
    tags='navigator;priorities;immigration;mismatch',
    notes='From: Greenland article. 62% see GOP focused on immigration. 45% see them focused on Venezuela (only 5% priority).')

# === 2. Holiday Costs ===
u2 = "https://navigatorresearch.org/in-time-for-the-holidays-americans-say-costs-are-going-up-on-everything/"
add(source_url=u2, date='2025-12-11', topic='economy', issue_area='grocery_prices',
    message_type='tracking_poll',
    wording='Say grocery costs are going up — overwhelming majority feel rising costs across categories',
    support_pct='78', sample_size='1000', methodology='online_panel', population='registered_voters', moe='3.1',
    tags='navigator;groceries;costs',
    notes='From: Holiday Costs article. 78% groceries up. 74% housing up. 74% utilities up. 72% healthcare up. Field: Dec 4-8, 2025.')
add(source_url=u2, date='2025-12-11', topic='economy', issue_area='economic_perception',
    message_type='tracking_poll',
    wording='Rate the economy negatively — 67% say not so good or poor',
    support_pct='67', sample_size='1000', methodology='online_panel', population='registered_voters', moe='3.1',
    tags='navigator;economy;negativity',
    notes='From: Holiday Costs. 67% rate economy negatively. 55% uneasy about personal finances.')
add(source_url=u2, date='2025-12-11', topic='economy', issue_area='inflation',
    message_type='tracking_poll',
    wording='Say President and Congress should focus on inflation and cost of living as top issue — 57% near its high',
    support_pct='57', sample_size='1000', methodology='online_panel', population='registered_voters', moe='3.1',
    tags='navigator;inflation;priorities',
    notes='From: Holiday Costs. 57% say inflation/cost of living should be top focus (near high of 62%).')
add(source_url=u2, date='2025-12-11', topic='economy', issue_area='financial_behavior',
    message_type='tracking_poll',
    wording='Unable to save as much as desired due to rising costs during holiday season',
    support_pct='51', sample_size='1000', methodology='online_panel', population='registered_voters', moe='3.1',
    tags='navigator;savings;financial_strain',
    notes='From: Holiday Costs. 51% unable to save. 49% stopped dining out. 47% cut back on gifts.')
add(source_url=u2, date='2025-12-11', topic='economy', issue_area='blame',
    message_type='tracking_poll',
    wording='Blame Trump and Republicans in Congress more than Democrats for rising costs — 21-point margin',
    support_pct='', net_score='+21', effect_scale='blame_margin',
    sample_size='1000', methodology='online_panel', population='registered_voters', moe='3.1',
    tags='navigator;blame;trump;gop;costs',
    notes='From: Holiday Costs. GOP blamed more by 21-pt margin on costs. Health premiums: GOP +22 net.')

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