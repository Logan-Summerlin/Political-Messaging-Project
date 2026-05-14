#!/usr/bin/env python3
"""Add articles: gas prices, tariffs, regime change."""
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

# === 1. Americans Blame Trump for Rising Gas Prices ===
u1 = "https://navigatorresearch.org/americans-blame-trump-for-rising-gas-prices/"
add(source_url=u1, date='2026-04-08', topic='economy', issue_area='gas_prices',
    message_type='tracking_poll',
    wording='Say the cost of gas is going up — overwhelming majority feeling price increases',
    support_pct='87', sample_size='1000', methodology='online_panel', population='registered_voters', moe='3.1',
    tags='navigator;gas;prices;costs',
    notes='From: Americans Blame Trump for Rising Gas Prices. 87% say gas going up (60% up a lot). Field: Apr 2-6, 2026.')
add(source_url=u1, date='2026-04-08', topic='economy', issue_area='gas_prices',
    message_type='tracking_poll',
    wording='Disapprove of Trump handling of gas prices — net -37 among all Americans',
    support_pct='28', oppose_pct='65', net_score='-37', effect_scale='approval',
    sample_size='1000', methodology='online_panel', population='registered_voters', moe='3.1',
    tags='navigator;trump;gas_prices;approval',
    notes='From: Gas Prices article. Trump -37 on gas prices. Independents -57.')
add(source_url=u1, date='2026-04-08', topic='foreign_policy', issue_area='iran_war',
    message_type='tracking_poll',
    wording='Blame the war in Iran for rising gas prices — top cited driver',
    support_pct='71', sample_size='1000', methodology='online_panel', population='registered_voters', moe='3.1',
    tags='navigator;iran;war;gas_prices;blame',
    notes='From: Gas Prices article. 71% blame Iran war. 48% blame Trump/GOP. 36% blame oil companies.')
add(source_url=u1, date='2026-04-08', topic='politics', issue_area='party_trust',
    message_type='tracking_poll',
    wording='Trust Democratic Party more than Trump/GOP to handle gas prices — narrow Democratic advantage',
    support_pct='35', oppose_pct='31', net_score='+4', effect_scale='trust',
    sample_size='1000', methodology='online_panel', population='registered_voters', moe='3.1',
    tags='navigator;trust;gas_prices;democrats',
    notes='From: Gas Prices article. 35% trust Dems, 31% trust GOP. 27% trust neither. 52% of independents trust neither.')

# === 2. Year After Liberation Day: Tariffs ===
u2 = "https://navigatorresearch.org/a-year-after-liberation-day-americans-still-dislike-tariffs-and-want-their-money-back/"
add(source_url=u2, date='2026-04-01', topic='economy', issue_area='tariffs',
    message_type='tracking_poll',
    wording='Tariff favorability — only 30% favorable one year after Liberation Day, unchanged from April 2025',
    support_pct='30', sample_size='1000', methodology='online_panel', population='registered_voters', moe='3.1',
    tags='navigator;tariffs;favorability',
    notes='From: Year After Liberation Day. 30% favorable. Dems 7%, Inds 17%, Reps 55%. Field: Mar 12-16, 2026.')
add(source_url=u2, date='2026-04-01', topic='economy', issue_area='tariffs',
    message_type='tracking_poll',
    wording='Oppose Trump tariff plan — net -21 opposition',
    support_pct='36', oppose_pct='57', net_score='-21', effect_scale='support_oppose',
    sample_size='1000', methodology='online_panel', population='registered_voters', moe='3.1',
    tags='navigator;tariffs;opposition;trump',
    notes='From: Liberation Day article. 36% support, 57% oppose. Dems -81, Inds -42.')
add(source_url=u2, date='2026-04-01', topic='economy', issue_area='tariff_rebate',
    message_type='tracking_poll',
    wording='Support tariff rebate checks sent to consumers — bipartisan support for rebate',
    support_pct='', sample_size='1000', methodology='online_panel', population='registered_voters', moe='3.1',
    tags='navigator;tariffs;rebate;checks',
    notes='From: Liberation Day article. 75% Reps, 61% Dems, 56% Inds support rebate checks. 78% prefer consumer over business.')
add(source_url=u2, date='2026-04-01', topic='economy', issue_area='tariff_message',
    message_type='tested_message',
    wording='The tariffs raised costs for Americans by thousands of dollars a year, and therefore Americans should get a rebate from the money that was collected — most persuasive pro-rebate message',
    support_pct='65', sample_size='1000', methodology='online_panel', population='registered_voters', moe='3.1',
    tags='navigator;tariffs;rebate;message_test',
    notes='From: Liberation Day article. Cost-focused message scored 65%. Outperformed conservative message by 30 points.')
add(source_url=u2, date='2026-04-01', topic='economy', issue_area='tariff_message',
    message_type='tested_message',
    wording='The Supreme Court ruled recent tariffs illegal and therefore Americans should get a rebate from the money that was stolen from them — legal argument for tariff rebates',
    support_pct='57', sample_size='1000', methodology='online_panel', population='registered_voters', moe='3.1',
    tags='navigator;tariffs;rebate;legal',
    notes='From: Liberation Day article. Legal message scored 57%. Outperformed conservative message by 14 points.')
add(source_url=u2, date='2026-04-01', topic='economy', issue_area='tariff_message',
    message_type='tested_message',
    wording='The tariffs worked to bring in billions of dollars to the United States and now Americans should share in the success of this policy — least persuasive message tested',
    support_pct='35', sample_size='1000', methodology='online_panel', population='registered_voters', moe='3.1',
    tags='navigator;tariffs;rebate;conservative',
    notes='From: Liberation Day article. Conservative success message scored only 35%, least persuasive.')

# === 3. Americans Don't Want Regime Change Wars ===
u3 = "https://navigatorresearch.org/americans-dont-want-regime-change-wars/"
add(source_url=u3, date='2026-03-02', topic='foreign_policy', issue_area='military_force',
    message_type='tracking_poll',
    wording='Say the U.S. should be cautious about using military force abroad — especially for regime change — and focus on domestic priorities',
    support_pct='77', sample_size='1000', methodology='online_panel', population='registered_voters', moe='3.1',
    tags='navigator;military;regime_change;cautious',
    notes='From: Americans Don\'t Want Regime Change Wars. 77% cautious approach. 80% of independents. Field: Feb 19-22, 2026.')
add(source_url=u3, date='2026-03-02', topic='foreign_policy', issue_area='iran_war',
    message_type='tracking_poll',
    wording='Opposed a military strike against Iran before the U.S. operation — near majority opposition',
    support_pct='34', oppose_pct='48', net_score='-14', effect_scale='support_oppose',
    sample_size='1000', methodology='online_panel', population='registered_voters', moe='3.1',
    tags='navigator;iran;military_strike;opposition',
    notes='From: Regime Change Wars article. 34% support, 48% oppose, 19% unsure. Pre-strike polling.')
add(source_url=u3, date='2026-03-02', topic='foreign_policy', issue_area='regime_change',
    message_type='tracking_poll',
    wording='Oppose using U.S. military for regime change — high across all party lines including 64% of Republicans',
    support_pct='', oppose_pct='', net_score='',
    sample_size='1000', methodology='online_panel', population='registered_voters', moe='3.1',
    tags='navigator;regime_change;opposition;bipartisan',
    notes='From: Regime Change Wars. 88% Dems, 83% Inds, 64% Reps, 55% MAGA oppose regime change wars.')
add(source_url=u3, date='2026-03-02', topic='economy', issue_area='priorities_mismatch',
    message_type='tracking_poll',
    wording='Say Trump and Republicans are focused on immigration (73%) and foreign conflicts (47%) — not on what voters prioritize (63% want inflation focus)',
    support_pct='73', sample_size='1000', methodology='online_panel', population='registered_voters', moe='3.1',
    tags='navigator;priorities;mismatch;trump',
    notes='From: Regime Change Wars article. 73% see GOP focused on immigration. Only 25% on inflation.')

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