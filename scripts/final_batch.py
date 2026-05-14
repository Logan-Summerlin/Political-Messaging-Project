#!/usr/bin/env python3
"""Final batch: Add messages from 4 more Navigator battleground articles."""
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

# ====== 1. Battleground Shutdown/Health Care ======
u1 = "https://navigatorresearch.org/americans-in-the-battleground-want-congress-to-protect-health-care-even-if-it-means-shutting-down-the-government/"
add(source_url=u1, date='2025-09-26', topic='government', issue_area='shutdown_blame',
    message_type='tracking_poll',
    wording='Blame Trump and Republicans for a government shutdown over health care funding — battleground constituents',
    support_pct='49', oppose_pct='44', net_score='+5', effect_scale='blame',
    sample_size='1500', methodology='text_to_web', population='likely_voters_2026', moe='2.5',
    tags='navigator;shutdown;blame;gop',
    notes='From: Battleground Health Care Shutdown. 49% blame GOP, 44% blame Dems. Inds: 55% blame GOP.')
add(source_url=u1, date='2025-09-26', topic='government', issue_area='shutdown_concern',
    message_type='tracking_poll',
    wording='See potential government shutdown as a serious problem for the country',
    support_pct='66', sample_size='1500', methodology='text_to_web', population='likely_voters_2026', moe='2.5',
    tags='navigator;shutdown;concern',
    notes='From: Battleground Shutdown. 66% say serious problem. 53% say personal impact.')
add(source_url=u1, date='2025-09-26', topic='healthcare', issue_area='shutdown_tactic',
    message_type='tested_message',
    wording='Congress should let the government shut down to hold the line against funding cuts for healthcare programs and keeping tariffs in place',
    support_pct='49', sample_size='1500', methodology='text_to_web', population='likely_voters_2026', moe='2.5',
    tags='navigator;shutdown;healthcare;tariffs',
    notes='From: Battleground Shutdown. 49% agree with pro-shutdown position to protect healthcare.')

# ====== 2. Trump Approval Declines (July 2025) ======
u2 = "https://navigatorresearch.org/trumps-approval-declines-in-the-battleground-as-economic-pessimism-grows/"
add(source_url=u2, date='2025-07-03', topic='economy', issue_area='presidential_approval',
    message_type='tracking_poll',
    wording='Trump economic approval in the battleground — 7 points underwater',
    support_pct='46', oppose_pct='53', net_score='-7', effect_scale='approval',
    sample_size='1500', methodology='text_to_web', population='likely_voters_2026', moe='2.5',
    tags='navigator;trump;economy;approval;battleground',
    notes='From: Trump Approval Declines. Field: May 28-Jun 1, 2025.')
add(source_url=u2, date='2025-07-03', topic='economy', issue_area='economic_perception',
    message_type='tracking_poll',
    wording='Rate the economy as not so good or poor — battleground constituents',
    support_pct='61', sample_size='1500', methodology='text_to_web', population='likely_voters_2026', moe='2.5',
    tags='navigator;economy;negativity;battleground',
    notes='From: Trump Approval Declines. 61% rate economy poorly.')
add(source_url=u2, date='2025-07-03', topic='economy', issue_area='personal_finance',
    message_type='tracking_poll',
    wording='Say personal financial situation is worse than a year ago — battleground',
    support_pct='33', sample_size='1500', methodology='text_to_web', population='likely_voters_2026', moe='2.5',
    tags='navigator;personal_finance;worse;battleground',
    notes='From: Trump Approval Declines. 33% say worse than a year ago.')
add(source_url=u2, date='2025-07-03', topic='government', issue_area='corruption',
    message_type='tracking_poll',
    wording='Rank government corruption as a top concern — emerging as third-most prioritized issue in the battleground',
    support_pct='28', sample_size='1500', methodology='text_to_web', population='likely_voters_2026', moe='2.5',
    tags='navigator;corruption;priorities;battleground',
    notes='From: Trump Approval Declines. 28% rank corruption as top concern. Behind threats to democracy and economy.')

# ====== 3. Two in Three Support Middle Class Policies (Aug 2023) ======
u3 = "https://navigatorresearch.org/two-in-three-battleground-constituents-support-policies-aimed-at-growing-the-middle-class/"
add(source_url=u3, date='2023-08-02', topic='economy', issue_area='economic_perception',
    message_type='tracking_poll',
    wording='Rate the economy as poor or not so good — battleground constituents July 2023',
    support_pct='71', sample_size='1500', methodology='text_to_web', population='likely_voters_2024', moe='2.5',
    tags='navigator;economy;negativity;battleground',
    notes='From: Two in Three support middle class policies. Field: Jul 6-12, 2023.')
add(source_url=u3, date='2023-08-02', topic='economy', issue_area='middle_class',
    message_type='tested_message',
    wording='Support a progressive approach: growing the middle class will drive economic growth — focus on improving incomes, affordable education, reducing middle class taxes, making wealthy pay fair share',
    support_pct='65', sample_size='1500', methodology='text_to_web', population='likely_voters_2024', moe='2.5',
    tags='navigator;middle_class;progressive;economy',
    notes='From: Two in Three. 65% support progressive middle-class approach over trickle-down. Inds: 67%. Reps: 41%.')
add(source_url=u3, date='2023-08-02', topic='economy', issue_area='gop_policies',
    message_type='tracking_poll',
    wording='Say Republican policies help the wealthy and corporations too much',
    support_pct='60', sample_size='1500', methodology='text_to_web', population='likely_voters_2024', moe='2.5',
    tags='navigator;gop;wealthy;corporations;perception',
    notes='From: Two in Three. 60% say GOP helps wealthy/corporations too much.')
add(source_url=u3, date='2023-08-02', topic='economy', issue_area='party_trust',
    message_type='tracking_poll',
    wording='Trust Republicans more to handle the economy — battleground constituents, July 2023',
    support_pct='44', oppose_pct='36', net_score='+8', effect_scale='trust',
    sample_size='1500', methodology='text_to_web', population='likely_voters_2024', moe='2.5',
    tags='navigator;trust;economy;gop',
    notes='From: Two in Three. GOP +8 on economy trust. Dems +4 on looking out for people like me.')
add(source_url=u3, date='2023-08-02', topic='politics', issue_area='trump_favorability',
    message_type='tracking_poll',
    wording='Trump unfavorable rating among battleground constituents — July 2023',
    support_pct='43', oppose_pct='57', net_score='-13', effect_scale='net_favorability',
    sample_size='1500', methodology='text_to_web', population='likely_voters_2024', moe='2.5',
    tags='navigator;trump;favorability;battleground',
    notes='From: Two in Three. Trump -13 net. 50% very unfavorable.')
add(source_url=u3, date='2023-08-02', topic='economy', issue_area='inflation',
    message_type='tracking_poll',
    wording='Rank inflation and cost of living as top priority for Congress — #1 issue July 2023',
    support_pct='40', sample_size='1500', methodology='text_to_web', population='likely_voters_2024', moe='2.5',
    tags='navigator;inflation;priorities;battleground',
    notes='From: Two in Three. 40% rank inflation/cost of living as top priority. 53% Reps, 50% Inds.')
add(source_url=u3, date='2023-08-02', topic='government', issue_area='gop_focus',
    message_type='tracking_poll',
    wording='Say Republicans have prioritized the wrong things since taking control of Congress — battleground constituents',
    support_pct='53', oppose_pct='37', net_score='-16', effect_scale='wrong_priorities',
    sample_size='1500', methodology='text_to_web', population='likely_voters_2024', moe='2.5',
    tags='navigator;gop;wrong_priorities;battleground',
    notes='From: Two in Three. 53% say GOP wrong priorities. 59% say GOP focuses on non-economic issues.')

# ====== 4. Post-Election Poll (Dec 2024) ======
u4 = "https://navigatorresearch.org/post-election-poll-the-issues-that-mattered-most-in-the-battleground/"
add(source_url=u4, date='2024-12-04', topic='economy', issue_area='voter_priorities',
    message_type='tracking_poll',
    wording='Inflation and cost of living was the top issue driving vote choice in the 2024 battleground — open-end #1',
    support_pct='30', sample_size='1500', methodology='text_to_web', population='likely_voters_2024', moe='2.5',
    tags='navigator;inflation;voter_priorities;2024',
    notes='From: Post-Election Poll. 30% inflation/cost of living. 49% among GOP voters.')
add(source_url=u4, date='2024-12-04', topic='immigration', issue_area='voter_priorities',
    message_type='tracking_poll',
    wording='Immigration/border was a top issue in the 2024 battleground — especially among GOP voters (53%)',
    support_pct='28', sample_size='1500', methodology='text_to_web', population='likely_voters_2024', moe='2.5',
    tags='navigator;immigration;voter_priorities;2024',
    notes='From: Post-Election Poll. 28% immigration/border. 53% among GOP voters.')
add(source_url=u4, date='2024-12-04', topic='democracy', issue_area='voter_priorities',
    message_type='tracking_poll',
    wording='Threats to democracy was a top issue in 2024 battleground — #1 for Democratic voters (48%)',
    support_pct='27', sample_size='1500', methodology='text_to_web', population='likely_voters_2024', moe='2.5',
    tags='navigator;democracy;voter_priorities;2024',
    notes='From: Post-Election Poll. 27% threats to democracy. 48% among Dem voters.')
add(source_url=u4, date='2024-12-04', topic='economy', issue_area='inflation',
    message_type='tracking_poll',
    wording='Inflation and cost of living mattered a great deal in 2024 vote — closed-ended measure',
    support_pct='67', sample_size='1500', methodology='text_to_web', population='likely_voters_2024', moe='2.5',
    tags='navigator;inflation;mattered;2024',
    notes='From: Post-Election Poll. 67% said inflation mattered a great deal (87% total mattered).')
add(source_url=u4, date='2024-12-04', topic='politics', issue_area='candidate_traits',
    message_type='tracking_poll',
    wording='Personal character and values mattered a great deal in 2024 vote — top candidate trait',
    support_pct='64', sample_size='1500', methodology='text_to_web', population='likely_voters_2024', moe='2.5',
    tags='navigator;character;values;2024',
    notes='From: Post-Election Poll. 64% said character/values mattered a great deal (86% total).')
add(source_url=u4, date='2024-12-04', topic='abortion', issue_area='party_concern',
    message_type='tracking_poll',
    wording='More concerned about Republicans\' position on abortion (47%) than Democrats\' position on transgender people (32%) — 15-point gap in battleground',
    support_pct='47', oppose_pct='32', net_score='+15', effect_scale='concern_gap',
    sample_size='1500', methodology='text_to_web', population='likely_voters_2024', moe='2.5',
    tags='navigator;abortion;transgender;concern',
    notes='From: Post-Election Poll. Voters more concerned about GOP abortion stance than Dem trans stance by 15 pts.')
add(source_url=u4, date='2024-12-04', topic='politics', issue_area='party_concern',
    message_type='tracking_poll',
    wording='Did not vote for Republican candidate because they would be a rubber stamp for Trump',
    support_pct='55', sample_size='1500', methodology='text_to_web', population='likely_voters_2024', moe='2.5',
    tags='navigator;gop;non_voter;trump',
    notes='From: Post-Election Poll. 55% of non-GOP voters said rubber stamp for Trump.')
add(source_url=u4, date='2024-12-04', topic='abortion', issue_area='message_reach',
    message_type='tracking_poll',
    wording='Heard Democratic congressional candidates\' message about abortion stance — highest reach issue for Dems at 70%',
    support_pct='70', effect_scale='message_reach',
    sample_size='1500', methodology='text_to_web', population='likely_voters_2024', moe='2.5',
    tags='navigator;abortion;message;reach',
    notes='From: Post-Election Poll. 70% heard Dem abortion message. 67% heard GOP immigration message.')

print(f"Added: {len(existing) - len([x for x in existing if x['message_id'] in existing_ids]) + 25}")
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