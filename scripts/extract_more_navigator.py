#!/usr/bin/env python3
"""Extract remaining Navigator battleground + special reports."""
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

added = 0

# === 1. Battleground Utility Costs ===
u = "https://navigatorresearch.org/battleground-views-on-utility-costs-and-data-centers/"
add(source_url=u, date='2026-03-12', topic='economy', issue_area='utility_costs',
    message_type='tracking_poll',
    wording='Say utility costs have gone up over the past year — highest of any cost category tested in the battleground',
    support_pct='84', sample_size='1500', methodology='text_to_web', population='likely_voters_2026', moe='2.5',
    tags='navigator;utility;costs;battleground',
    notes='From: Battleground Views On Utility Costs. 84% utility costs up (48% up a lot).')
added += 1

add(source_url=u, date='2026-03-12', topic='economy', issue_area='utility_costs',
    message_type='tracking_poll',
    wording='Blame utility companies for rising utility costs — battleground constituents',
    support_pct='37', sample_size='1500', methodology='text_to_web', population='likely_voters_2026', moe='2.5',
    tags='navigator;utility;blame;companies',
    notes='From: Battleground Utility Costs. 37% blame utility companies, 33% blame data centers/AI/crypto.')
added += 1

add(source_url=u, date='2026-03-12', topic='economy', issue_area='data_centers',
    message_type='tracking_poll',
    wording='Blame energy-intensive industries like data centers, AI, and crypto for rising utility costs',
    support_pct='33', sample_size='1500', methodology='text_to_web', population='likely_voters_2026', moe='2.5',
    tags='navigator;utility;data_centers;ai;crypto',
    notes='From: Battleground Utility Costs. 33% blame data centers/AI/crypto overall. 44% among those near data centers.')
added += 1

add(source_url=u, date='2026-03-12', topic='economy', issue_area='utility_costs',
    message_type='tracking_poll',
    wording='Believe Congress can do something to lower utility costs',
    support_pct='85', sample_size='1500', methodology='text_to_web', population='likely_voters_2026', moe='2.5',
    tags='navigator;utility;congress;action',
    notes='From: Battleground Utility Costs. 85% believe Congress can lower utility costs (49% say a great deal).')
added += 1

add(source_url=u, date='2026-03-12', topic='economy', issue_area='utility_company_favorability',
    message_type='tracking_poll',
    wording='Utility company net favorability — net -38 among battleground constituents',
    support_pct='25', oppose_pct='63', net_score='-38', effect_scale='net_favorability',
    sample_size='1500', methodology='text_to_web', population='likely_voters_2026', moe='2.5',
    tags='navigator;utility;favorability;companies',
    notes='From: Battleground Utility Costs. Utility companies -38 net. Energy companies -36 net. Tech companies -23 net.')
added += 1

# === 2. State of the Battleground ===
u2 = "https://navigatorresearch.org/state-of-the-battleground/"
add(source_url=u2, date='2026-02-23', topic='government', issue_area='congressional_approval',
    message_type='tracking_poll',
    wording='Congressional Democrats viewed unfavorably in the battleground',
    support_pct='', oppose_pct='63', net_score='-63',
    sample_size='1500', methodology='text_to_web', population='likely_voters_2026', moe='2.5',
    tags='navigator;democrats;favorability;battleground',
    notes='From: State of the Battleground. Both parties viewed overwhelmingly unfavorably.')
added += 1

add(source_url=u2, date='2026-02-23', topic='government', issue_area='gop_favorability',
    message_type='tracking_poll',
    wording='Congressional Republicans viewed unfavorably in the battleground — net -61',
    support_pct='', oppose_pct='61', net_score='-61',
    sample_size='1500', methodology='text_to_web', population='likely_voters_2026', moe='2.5',
    tags='navigator;republicans;favorability;battleground',
    notes='From: State of the Battleground. GOP incumbents underwater by 13 pts.')
added += 1

add(source_url=u2, date='2026-02-23', topic='government', issue_area='priorities',
    message_type='tracking_poll',
    wording='Rank government corruption as a top-two priority for Congress',
    support_pct='36', sample_size='1500', methodology='text_to_web', population='likely_voters_2026', moe='2.5',
    tags='navigator;corruption;priorities;battleground',
    notes='From: State of the Battleground. Corruption 36%, threats to democracy 33%.')
added += 1

add(source_url=u2, date='2026-02-23', topic='democracy', issue_area='threats',
    message_type='tracking_poll',
    wording='Rank threats to democracy as a top-two priority for Congress',
    support_pct='33', sample_size='1500', methodology='text_to_web', population='likely_voters_2026', moe='2.5',
    tags='navigator;democracy;priorities;battleground',
    notes='From: State of the Battleground. 33% rank threats to democracy as top-two priority.')
added += 1

add(source_url=u2, date='2026-02-23', topic='economy', issue_area='inflation',
    message_type='tracking_poll',
    wording='Rank inflation and cost of living as top-two priority — #1 issue for battleground voters',
    support_pct='29', sample_size='1500', methodology='text_to_web', population='likely_voters_2026', moe='2.5',
    tags='navigator;inflation;priorities;battleground;top_issue',
    notes='From: State of the Battleground. Inflation/cost of living #1.')
added += 1

add(source_url=u2, date='2026-02-23', topic='government', issue_area='gop_focus',
    message_type='tracking_poll',
    wording='Say Republicans in Congress are focused on immigration — a misalignment with voter priorities (only 9% rank it top)',
    support_pct='59', sample_size='1500', methodology='text_to_web', population='likely_voters_2026', moe='2.5',
    tags='navigator;gop;immigration;focus;misalignment',
    notes='From: State of the Battleground. 59% say GOP focused on immigration. Only 9% rank it top issue.')
added += 1

add(source_url=u2, date='2026-02-23', topic='economy', issue_area='wrong_focus',
    message_type='tracking_poll',
    wording='Say Trump and Republicans are focused on the wrong things — by an 18-point margin',
    support_pct='57', oppose_pct='39', net_score='-18', effect_scale='wrong_direction',
    sample_size='1500', methodology='text_to_web', population='likely_voters_2026', moe='2.5',
    tags='navigator;trump;gop;wrong_focus',
    notes='From: State of the Battleground. 57% wrong things vs 39% right things.')
added += 1

add(source_url=u2, date='2026-02-23', topic='economy', issue_area='trust_comparison',
    message_type='tracking_poll',
    wording='Trust Democrats more than Republicans to lower costs for working families — Democrats hold +8 advantage',
    support_pct='', net_score='+8', effect_scale='trust_advantage',
    sample_size='1500', methodology='text_to_web', population='likely_voters_2026', moe='2.5',
    tags='navigator;trust;democrats;costs',
    notes='From: State of the Battleground. Democrats +8 on lowering costs, +8 on healthcare, +23 on wealthy paying share.')
added += 1

add(source_url=u2, date='2026-02-23', topic='politics', issue_area='party_perception',
    message_type='tracking_poll',
    wording='Say elitist describes Democrats well — 53% of battleground constituents',
    support_pct='53', sample_size='1500', methodology='text_to_web', population='likely_voters_2026', moe='2.5',
    tags='navigator;democrats;elitist;perception',
    notes='From: State of the Battleground. 53% say elitist describes Dems well. Only 37% say cares about people like me.')
added += 1

add(source_url=u2, date='2026-02-23', topic='government', issue_area='presidential_approval',
    message_type='tracking_poll',
    wording='Trump unfavorable rating among battleground constituents',
    support_pct='', oppose_pct='54', net_score='-54',
    sample_size='1500', methodology='text_to_web', population='likely_voters_2026', moe='2.5',
    tags='navigator;trump;favorability;battleground',
    notes='From: State of the Battleground. Trump 54% unfavorable. Independents: 51% unfavorable.')
added += 1

# === 3. Abortion/Contraception (2024) ===
u3 = "https://navigatorresearch.org/a-majority-of-battleground-constituents-support-congress-taking-action-to-protect-access-to-contraception-and-abortion/"
add(source_url=u3, date='2024-06-28', topic='abortion', issue_area='contraception',
    message_type='tracking_poll',
    wording='Support Congress passing a law protecting access to contraception nationwide — overwhelming bipartisan support',
    support_pct='', net_score='+50', sample_size='1600', methodology='text_to_web',
    population='likely_voters_2024', moe='2.5',
    tags='navigator;contraception;abortion;battleground',
    notes='From: Abortion/Contraception access poll. 92% Dems, 65% Inds, 52% Reps support. 71% in both Dem and GOP districts.')
added += 1

add(source_url=u3, date='2024-06-28', topic='abortion', issue_area='abortion_access',
    message_type='tracking_poll',
    wording='Support Congress passing a law protecting access to abortion nationwide and protecting physicians who provide abortions',
    support_pct='59', sample_size='1600', methodology='text_to_web', population='likely_voters_2024', moe='2.5',
    tags='navigator;abortion;access;congress',
    notes='From: Abortion/Contraception access. 59% support nationwide abortion protection. Women: 66%. Men: 51%.')
added += 1

add(source_url=u3, date='2024-06-28', topic='abortion', issue_area='abortion_future',
    message_type='tracking_poll',
    wording='Believe Republicans will pass more restrictions on abortion nationwide if they win the next election',
    support_pct='60', sample_size='1600', methodology='text_to_web', population='likely_voters_2024', moe='2.5',
    tags='navigator;abortion;gop;restrictions',
    notes='From: Abortion/Contraception access. 60% believe GOP will pass more restrictions. 95% Dems, 46% Inds, 57% Reps.')
added += 1

# === 4. Health Care Battleground ===
u4 = "https://navigatorresearch.org/views-on-health-care-in-the-battleground-and-beyond/"
add(source_url=u4, date='2026-03-09', topic='healthcare', issue_area='healthcare_costs',
    message_type='tracking_poll',
    wording='Say health care costs have gone up over the past year — battleground constituents',
    support_pct='80', sample_size='1500', methodology='text_to_web', population='likely_voters_2026', moe='2.5',
    tags='navigator;healthcare;costs;battleground',
    notes='From: Views on Health Care in Battleground. Field Feb 3-9, 2026. 80% say health costs up.')
added += 1

add(source_url=u4, date='2026-03-09', topic='healthcare', issue_area='congress_action',
    message_type='tracking_poll',
    wording='Believe Congress has power to lower health care costs — highest of any cost category',
    support_pct='91', sample_size='1500', methodology='text_to_web', population='likely_voters_2026', moe='2.5',
    tags='navigator;healthcare;congress;action',
    notes='From: Views on Health Care in Battleground. 91% believe Congress can lower health costs (74% say a great deal).')
added += 1

# === 5. Special Report: Who Americans Trust ===
u5 = "https://navigatorresearch.org/special-report-who-do-americans-trust/"
add(source_url=u5, date='2026-04-28', topic='politics', issue_area='party_trust',
    message_type='tracking_poll',
    wording='Trust the Democratic Party more than Republicans to handle health care — Democrats maintain advantage',
    support_pct='44', sample_size='1000', methodology='online_panel', population='registered_voters', moe='3.1',
    tags='navigator;trust;healthcare;democrats',
    notes='From: Who Do Americans Trust special report. 44% trust Dems on health care, 19% trust neither.')
added += 1

add(source_url=u5, date='2026-04-28', topic='politics', issue_area='party_trust',
    message_type='tracking_poll',
    wording='Trust Republicans more on getting things done — GOP holds narrow advantage',
    support_pct='41', oppose_pct='31', net_score='+10', effect_scale='trust_comparison',
    sample_size='1000', methodology='online_panel', population='registered_voters', moe='3.1',
    tags='navigator;trust;getting_things_done;gop',
    notes='From: Who Do Americans Trust. 41% R vs 31% D. 23% trust neither.')
added += 1

# === 6. Americans Oppose Prediction Markets ===
u6 = "https://navigatorresearch.org/americans-oppose-unfair-prediction-markets/"
add(source_url=u6, date='2026-04-20', topic='government', issue_area='prediction_markets',
    message_type='tracking_poll',
    wording='Oppose unfair prediction markets usage for political betting — even if few are following them',
    support_pct='', sample_size='1000', methodology='online_panel', population='registered_voters', moe='3.1',
    tags='navigator;prediction_markets;gambling;opposition',
    notes='From: Americans Oppose Unfair Prediction Markets. Field: Apr 2-6, 2026.')
added += 1

print(f"Added: {added}")
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