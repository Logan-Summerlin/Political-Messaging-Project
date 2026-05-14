#!/usr/bin/env python3
"""Add immigration article + Trump C- Grade article."""
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

# === 1. Americans Fed Up With Cruel Immigration Policies ===
u1 = "https://navigatorresearch.org/americans-are-fed-up-with-cruel-immigration-policies/"
add(source_url=u1, date='2026-03-11', topic='immigration', issue_area='ice',
    message_type='tracking_poll',
    wording='Americans are unfavorable toward ICE — highest unfavorability since Trump took office this term',
    support_pct='60', sample_size='1000', methodology='online_panel', population='registered_voters', moe='3.1',
    tags='navigator;ice;unfavorable',
    notes='From: Americans Fed Up With Cruel Immigration Policies. Field: Feb 19-22, 2026.')
add(source_url=u1, date='2026-03-11', topic='immigration', issue_area='ice',
    message_type='tracking_poll',
    wording='Say ICE has been too aggressive in its approach — three in five Americans',
    support_pct='62', sample_size='1000', methodology='online_panel', population='registered_voters', moe='3.1',
    tags='navigator;ice;aggression',
    notes='From: Immigration article. 62% say too aggressive. 22% right balance. 11% not aggressive enough.')
add(source_url=u1, date='2026-03-11', topic='immigration', issue_area='ice_funding',
    message_type='tracking_poll',
    wording='Support Congress withholding funding from ICE until it changes its approach — even if that means shutting down DHS',
    support_pct='58', sample_size='1000', methodology='online_panel', population='registered_voters', moe='3.1',
    tags='navigator;ice;funding;congress',
    notes='From: Immigration article. 58% support withholding funding (65% of independents).')
add(source_url=u1, date='2026-03-11', topic='immigration', issue_area='trump_approval',
    message_type='tracking_poll',
    wording='Disapprove of Trump handling of immigration — net approval fell from -3 to -17 since June 2025',
    support_pct='40', oppose_pct='57', net_score='-17', effect_scale='approval',
    sample_size='1000', methodology='online_panel', population='registered_voters', moe='3.1',
    tags='navigator;trump;immigration;approval',
    notes='From: Immigration article. Trump immigration approval -17 net (was -3 in June 2025).')
add(source_url=u1, date='2026-03-11', topic='immigration', issue_area='mass_deportation',
    message_type='tracking_poll',
    wording='Oppose Trump mass deportation plan — net support fell from +10 to -14 since Jan 2025',
    support_pct='40', oppose_pct='54', net_score='-14', effect_scale='support_oppose',
    sample_size='1000', methodology='online_panel', population='registered_voters', moe='3.1',
    tags='navigator;mass_deportation;opposition',
    notes='From: Immigration article. Mass deportation plan net +10 in Jan 2025 → -14 in Feb 2026.')
add(source_url=u1, date='2026-03-11', topic='immigration', issue_area='priorities_mismatch',
    message_type='tracking_poll',
    wording='Say Trump/Republicans are focused on immigration (71%) — but only 31% list it as a top-five priority. Top priorities are inflation (56%) and jobs (46%)',
    support_pct='71', sample_size='1000', methodology='online_panel', population='registered_voters', moe='3.1',
    tags='navigator;priorities;immigration;mismatch',
    notes='From: Immigration article. 71% see GOP focused on immigration. Only 21% see them focused on inflation.')
add(source_url=u1, date='2026-03-11', topic='immigration', issue_area='migrant_concern',
    message_type='tracking_poll',
    wording='Concerned about dire conditions in migrant detention centers (contaminated food, measles, deaths) — highest concern among immigration stories tested',
    support_pct='68', sample_size='1000', methodology='online_panel', population='registered_voters', moe='3.1',
    tags='navigator;migrant;detention;concern',
    notes='From: Immigration article. 68% concerned about detention conditions. 54% heard about ICE detention of child.')

# === 2. One Year In: Trump C- Grade ===
u2 = "https://navigatorresearch.org/one-year-in-americans-give-trump-a-c-grade/"
add(source_url=u2, date='2026-01-20', topic='politics', issue_area='presidential_grade',
    message_type='tracking_poll',
    wording='Americans give Trump a C- (1.78 GPA) average overall for his second term — 36% give an F',
    support_pct='', sample_size='1000', methodology='online_panel', population='registered_voters', moe='3.1',
    tags='navigator;trump;grade;approval',
    notes='From: One Year In: Trump C- Grade. Overall GPA 1.78. Economy GPA 1.88. Field: Jan 8-12, 2026.')
add(source_url=u2, date='2026-01-20', topic='economy', issue_area='cost_increases',
    message_type='tracking_poll',
    wording='Say cost of living has increased as a result of Trump second term policies',
    support_pct='80', sample_size='1000', methodology='online_panel', population='registered_voters', moe='3.1',
    tags='navigator;cost_of_living;trump;policies',
    notes='From: Trump C- Grade article. 80% say cost of living up. 79% say grocery costs up.')
add(source_url=u2, date='2026-01-20', topic='economy', issue_area='cost_increases',
    message_type='tracking_poll',
    wording='Say grocery costs have increased as a result of Trump second term policies',
    support_pct='79', sample_size='1000', methodology='online_panel', population='registered_voters', moe='3.1',
    tags='navigator;groceries;costs;trump',
    notes='From: Trump C- Grade article. 79% say grocery costs up. 69% utility costs up. 69% housing costs up.')
add(source_url=u2, date='2026-01-20', topic='politics', issue_area='political_division',
    message_type='tracking_poll',
    wording='Say political division has gotten worse during first year of Trump second term — nearly two-thirds agree',
    support_pct='65', sample_size='1000', methodology='online_panel', population='registered_voters', moe='3.1',
    tags='navigator;division;politics;trump',
    notes='From: Trump C- Grade. 65% say political division worse (47% say a lot worse).')
add(source_url=u2, date='2026-01-20', topic='economy', issue_area='tariffs',
    message_type='tracking_poll',
    wording='Rank tariffs as one of the top two policies most associated with Trump second term — 48% top two, 64% top three',
    support_pct='48', sample_size='1000', methodology='online_panel', population='registered_voters', moe='3.1',
    tags='navigator;tariffs;association;trump',
    notes='From: Trump C- Grade article. 48% top two. 38% SNAP/Medicaid cuts top two.')
add(source_url=u2, date='2026-01-20', topic='economy', issue_area='tariffs',
    message_type='tracking_poll',
    wording='Cite tariffs as the #1 policy driving cost increases — 33% rank first, 55% rank in top three',
    support_pct='33', sample_size='1000', methodology='online_panel', population='registered_voters', moe='3.1',
    tags='navigator;tariffs;cost_driver',
    notes='From: Trump C- Grade article. 33% say tariffs #1 for cost increases. Cuts to Medicaid/SNAP #2 (40% top three).')

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