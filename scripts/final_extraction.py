#!/usr/bin/env python3
"""
Final extraction: Add Navigator articles and remaining DFP data.
"""
import csv, re
from pathlib import Path
from collections import Counter

BASE = Path(__file__).parent.parent
PROC = BASE / "data" / "processed"
DFP_NEW = PROC / "dfp_new_messages.csv"
CHUNK1 = BASE / "data" / "raw" / "dataforprogress" / "chunk1_polling_data.md"

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
print(f"Starting: {len(existing)} rows")

# Get next NAV ID number
import re
nav_nums = []
for r in existing:
    if r['message_id'].startswith('NAV_'):
        m = re.search(r'NAV_(\d+)', r['message_id'])
        if m:
            nav_nums.append(int(m.group(1)))
next_nav = max(nav_nums) + 1 if nav_nums else 100

def add_nav(**kw):
    global next_nav
    mid = f"NAV_{next_nav:04d}"
    next_nav += 1
    if mid in existing_ids:
        next_nav += 1
        mid = f"NAV_{next_nav:04d}"
    kw['message_id'] = mid
    kw['source'] = 'Navigator Research'
    row = {k: '' for k in msg_fieldnames}
    row.update(kw)
    existing.append(row)
    existing_ids.add(mid)
    return mid

added = 0

# ====== 1. Trump Regretters article ======
u = "https://navigatorresearch.org/one-in-five-trump-2024-voters-regret-their-vote/"
add_nav(source_url=u, date='2026-04-23', topic='politics', issue_area='trump_voter_regret',
    message_type='tracking_poll', 
    wording='One in five Trump 2024 voters regret their vote — consistent across recent Navigator surveys',
    support_pct='20', sample_size='1000', methodology='online_panel', population='registered_voters', moe='3.1',
    tags='navigator;trump;regret;voter',
    notes='From: One in Five Trump 2024 Voters Regret Their Vote. Field: Apr 2-6, 2026. Global Strategy Group.')
added += 1

add_nav(source_url=u, date='2026-04-23', topic='economy', issue_area='tariffs',
    message_type='tracking_poll',
    wording='Trump 2024 voters who regret their vote view tariffs unfavorably by a net -31 margin',
    support_pct='30', oppose_pct='61', net_score='-31', effect_scale='net_favorability',
    sample_size='1000', methodology='online_panel', population='registered_voters', moe='3.1',
    tags='navigator;trump;regret;tariffs',
    notes='From: Trump Regretters article. Regretters: 30% favorable, 61% unfavorable. Non-regretters: 62% favorable.')
added += 1

add_nav(source_url=u, date='2026-04-23', topic='immigration', issue_area='ice',
    message_type='tracking_poll',
    wording='Trump 2024 voters who regret their vote view ICE unfavorably by a net -24 margin',
    support_pct='34', oppose_pct='58', net_score='-24', effect_scale='net_favorability',
    sample_size='1000', methodology='online_panel', population='registered_voters', moe='3.1',
    tags='navigator;trump;regret;ice',
    notes='From: Trump Regretters article. Regretters: 34% favorable, 58% unfavorable.')
added += 1

add_nav(source_url=u, date='2026-04-23', topic='economy', issue_area='economic_perception',
    message_type='tracking_poll',
    wording='Trump 2024 voters who regret their vote rate the economy as poor or not so good',
    support_pct='64', effect_scale='negativity',
    sample_size='1000', methodology='online_panel', population='registered_voters', moe='3.1',
    tags='navigator;trump;regret;economy',
    notes='From: Trump Regretters article. 64% rate economy poor/not so good.')
added += 1

# ====== 2. Americans Struggle to Keep Up with Rising Costs ======
u2 = "https://navigatorresearch.org/americans-struggle-to-keep-up-with-rising-costs/"
add_nav(source_url=u2, date='2026-04-16', topic='economy', issue_area='economic_approval',
    message_type='tracking_poll',
    wording='Trump economy approval — approve or disapprove of Trump handling of the economy',
    support_pct='40', oppose_pct='59', net_score='-19', effect_scale='approval',
    sample_size='1000', methodology='online_panel', population='registered_voters', moe='3.1',
    tags='navigator;trump;economy;approval',
    notes='From: Americans Struggle to Keep Up. Trump economic approval at historical low. Net -19.')
added += 1

add_nav(source_url=u2, date='2026-04-16', topic='economy', issue_area='economic_perception',
    message_type='tracking_poll',
    wording='Rate the state of the U.S. economy as poor or not so good',
    support_pct='68', oppose_pct='31', net_score='-37', effect_scale='negativity',
    sample_size='1000', methodology='online_panel', population='registered_voters', moe='3.1',
    tags='navigator;economy;negativity',
    notes='From: Americans Struggle to Keep Up. 68% negative vs 31% positive on economy.')
added += 1

add_nav(source_url=u2, date='2026-04-16', topic='economy', issue_area='personal_finance',
    message_type='tracking_poll',
    wording='Feel uneasy about personal financial situation',
    support_pct='58', oppose_pct='39', net_score='-19', effect_scale='unease',
    sample_size='1000', methodology='online_panel', population='registered_voters', moe='3.1',
    tags='navigator;personal_finance;unease',
    notes='From: Americans Struggle to Keep Up. 58% uneasy, 39% confident. Women: 63% uneasy.')
added += 1

add_nav(source_url=u2, date='2026-04-16', topic='economy', issue_area='direction',
    message_type='tracking_poll',
    wording='Say country will be worse off a year from now — economic pessimism about the future',
    support_pct='55', effect_scale='pessimism',
    sample_size='1000', methodology='online_panel', population='registered_voters', moe='3.1',
    tags='navigator;direction;pessimism',
    notes='From: Americans Struggle to Keep Up. 55% say Trump focused on wrong things. 43% say worse off next year.')
added += 1

add_nav(source_url=u2, date='2026-04-16', topic='economy', issue_area='cost_of_living',
    message_type='tracking_poll',
    wording='Say gas prices are going up — perception of rising costs across categories',
    support_pct='90', effect_scale='perception',
    sample_size='1000', methodology='online_panel', population='registered_voters', moe='3.1',
    tags='navigator;costs;gas;prices',
    notes='From: Americans Struggle to Keep Up. 9-in-10 feel gas prices up, 8-in-10 feel costs generally up.')
added += 1

add_nav(source_url=u2, date='2026-04-16', topic='economy', issue_area='coping_strategies',
    message_type='tracking_poll',
    wording='Cutting back on spending by going out less and staying home more to cope with rising costs',
    support_pct='52', effect_scale='behavior_change',
    sample_size='1000', methodology='online_panel', population='registered_voters', moe='3.1',
    tags='navigator;costs;spending;behavior',
    notes='From: Americans Struggle to Keep Up. 52% stay home more, 41% use coupons, 29% cancel subscriptions.')
added += 1

# ====== 3. Battleground Grocery Costs ======
u3 = "https://navigatorresearch.org/feeling-the-pressure-of-rising-grocery-costs-battleground-voters-lay-the-blame-on-trump-and-republicans-in-congress/"
add_nav(source_url=u3, date='2025-10-03', topic='economy', issue_area='tariffs',
    message_type='tracking_poll',
    wording='Believe tariffs have increased costs — battleground voters on tariff impact',
    support_pct='69', sample_size='1500', methodology='text_to_web', population='likely_voters_2026', moe='2.5',
    tags='navigator;tariffs;costs;battleground',
    notes='From: Feeling the Pressure of Rising Grocery Costs. Field: Sep 18-21, 2025. Impact Research.')
added += 1

add_nav(source_url=u3, date='2025-10-03', topic='economy', issue_area='tariffs',
    message_type='tracking_poll',
    wording='Say President Trump\'s policies are making costs go up — battleground voters',
    support_pct='54', sample_size='1500', methodology='text_to_web', population='likely_voters_2026', moe='2.5',
    tags='navigator;trump;costs;policies',
    notes='From: Feeling the Pressure. 54% say Trump policies making costs go up (including 60% of independents).')
added += 1

add_nav(source_url=u3, date='2025-10-03', topic='economy', issue_area='tariffs',
    message_type='tracking_poll',
    wording='Believe the worst of cost increases is yet to come — pessimistic about future costs',
    support_pct='50', sample_size='1500', methodology='text_to_web', population='likely_voters_2026', moe='2.5',
    tags='navigator;costs;future;pessimism;tariffs',
    notes='From: Feeling the Pressure. 50% believe worst is yet to come (52% of persuadables).')
added += 1

add_nav(source_url=u3, date='2025-10-03', topic='economy', issue_area='grocery_prices',
    message_type='tracking_poll',
    wording='Say cost of groceries has increased the most as a result of tariffs',
    support_pct='54', sample_size='1500', methodology='text_to_web', population='likely_voters_2026', moe='2.5',
    tags='navigator;groceries;tariffs;costs',
    notes='From: Feeling the Pressure. 54% say groceries increased most due to tariffs. 87% say groceries matter most to budget.')
added += 1

add_nav(source_url=u3, date='2025-10-03', topic='economy', issue_area='blame',
    message_type='tracking_poll',
    wording='Blame Donald Trump for price increases from tariffs — battleground voter attribution',
    support_pct='43', sample_size='1500', methodology='text_to_web', population='likely_voters_2026', moe='2.5',
    tags='navigator;blame;trump;tariffs',
    notes='From: Feeling the Pressure. 43% blame Trump alone, 35% blame Trump/GOP equally, 20% blame GOP exclusively.')
added += 1

add_nav(source_url=u3, date='2025-10-03', topic='economy', issue_area='gop_blame',
    message_type='tracking_poll',
    wording='View congressional Republicans as extremely responsible for tariffs after learning they voted to support them three times',
    support_pct='52', sample_size='1500', methodology='text_to_web', population='likely_voters_2026', moe='2.5',
    tags='navigator;gop;tariffs;responsibility',
    notes='From: Feeling the Pressure. After learning GOP voted 3 times for tariffs, 52% say extremely responsible.')
added += 1

# ====== 4. Tariffs, Tax Cuts & Trouble for Republicans ======
u4 = "https://navigatorresearch.org/tariffs-tax-cuts-trouble-for-republicans/"
add_nav(source_url=u4, date='2026-03-05', topic='economy', issue_area='gop_approval',
    message_type='tracking_poll',
    wording='Disapprove of Republican incumbents handling of the economy in battleground districts — dropped from net 0 to net -16 in one year',
    support_pct='31', oppose_pct='47', net_score='-16', effect_scale='approval',
    sample_size='1500', methodology='text_to_web', population='likely_voters_2026', moe='2.5',
    tags='navigator;gop;economy;approval;battleground',
    notes='From: Tariffs, Tax Cuts & Trouble. GOP incumbent economic approval collapsed from 0 to -16. Field: Feb 3-9, 2026.')
added += 1

add_nav(source_url=u4, date='2026-03-05', topic='economy', issue_area='cost_increases',
    message_type='tracking_poll',
    wording='Say costs have gone up over the past year — battleground constituents',
    support_pct='75', sample_size='1500', methodology='text_to_web', population='likely_voters_2026', moe='2.5',
    tags='navigator;costs;increases;battleground',
    notes='From: Tariffs, Tax Cuts article. 75% say costs up (53% up a lot). 98% Democrats, 71% independents, 52% Republicans.')
added += 1

add_nav(source_url=u4, date='2026-03-05', topic='economy', issue_area='tariffs',
    message_type='tracking_poll',
    wording='Cite tariffs as main reason for costs increasing over the past year — open-end response top answer',
    support_pct='33', sample_size='1500', methodology='text_to_web', population='likely_voters_2026', moe='2.5',
    tags='navigator;tariffs;cost_driver',
    notes='From: Tariffs, Tax Cuts article. 33% cite tariffs (open-end), 20% cite inflation. Independents: 27% cite tariffs.')
added += 1

add_nav(source_url=u4, date='2026-03-05', topic='economy', issue_area='tariffs',
    message_type='tracking_poll',
    wording='Believe Trump/GOP tariffs on imports have led to costs going up',
    support_pct='72', sample_size='1500', methodology='text_to_web', population='likely_voters_2026', moe='2.5',
    tags='navigator;tariffs;cost_increase;trump',
    notes='From: Tariffs, Tax Cuts article. 72% say tariffs caused costs up (53% up a lot).')
added += 1

add_nav(source_url=u4, date='2026-03-05', topic='economy', issue_area='gop_policies',
    message_type='tracking_poll',
    wording='Say ending ACA tax credits would increase costs — one of several GOP policies linked to higher costs',
    support_pct='60', sample_size='1500', methodology='text_to_web', population='likely_voters_2026', moe='2.5',
    tags='navigator;aca;tax_credits;costs',
    notes='From: Tariffs, Tax Cuts article. 60% say ending ACA credits increases costs.')
added += 1

add_nav(source_url=u4, date='2026-03-05', topic='economy', issue_area='gop_policies',
    message_type='tracking_poll',
    wording='Say tax bill benefiting the ultra wealthy increases costs',
    support_pct='54', sample_size='1500', methodology='text_to_web', population='likely_voters_2026', moe='2.5',
    tags='navigator;tax_bill;wealthy;costs',
    notes='From: Tariffs, Tax Cuts article. 54% say GOP tax bill benefiting wealthy increases costs.')
added += 1

add_nav(source_url=u4, date='2026-03-05', topic='healthcare', issue_area='medicaid',
    message_type='tracking_poll',
    wording='Say cutting Medicaid funding increases costs',
    support_pct='53', sample_size='1500', methodology='text_to_web', population='likely_voters_2026', moe='2.5',
    tags='navigator;medicaid;cuts;costs',
    notes='From: Tariffs, Tax Cuts article. 53% say cutting Medicaid increases costs.')
added += 1

print(f"New Navigator articles added: {added}")

# ====== 5. Clean DFP messages from dfp_new_messages.csv ======
# Only add DFP messages that are genuine (at least 30 chars, not fragment-like)
FRAGMENT_PATTERNS = [
    r'^[Oo]f the choices', r'^[Ii]n the voting booth', r'^the cost of ',
    r'^jobs and the economy', r'^somewhat of a problem', r'^already have enough',
    r'^responsible investing', r'^not (at all|confident|very|too)',
    r'^only a little', r'^a violent insurrection', r'^while \d+ percent',
    r'^in U\.S\. communities', r'^held in prisons', r'^87,000 IRS',
    r'^medically necessary\.$', r'^unfairly raise prices', r'^the Biden administration',
    r'^low political interest', r'^next big climate', r'^I\'?m concerned',
    r'^Environmental, Social', r'^Don\'?t Say Gay', r'^I often feel',
    r'^Congress is dysfunctional', r'^protecting tenants', r'^manufacturing renaissance',
    r'^new license to discriminate', r'^compromise, waive', r'^nonignorable',
    r'^free from controlled', r'^a lot of responsibility', r'^bear some',
    r'^somewhat disapprove', r'^marketplace of ideas', r'^joint employer',
    r'^a great deal of blame', r'^not at all important', r'^moderate republicans',
    r'^good-paying union', r'^mild and manageable',
    r'^which doesn\'?t require', r'^of the proposal',
]

def is_fragment(w):
    w = w.strip().strip('"').strip("'")
    if len(w) < 30:
        return True
    for pat in FRAGMENT_PATTERNS:
        if re.match(pat, w, re.IGNORECASE):
            return True
    if w.lower().startswith(('which ', 'what ', 'how ', 'do you ', 'would you ', 'when asked', 'a majority ', 'we find ')):
        return True
    return False

def clean_w(w):
    w = w.strip()
    w = re.sub(r'^["\u201c\u201d]\s*', '', w)
    w = re.sub(r'\s*["\u201d]+$', '', w)
    if w:
        w = w[0].upper() + w[1:]
    return w.strip()

dfp_added = 0
with open(DFP_NEW, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for r in reader:
        w = clean_w(r['wording'])
        if is_fragment(w):
            continue
        mid = r['message_id'].strip()
        if mid in existing_ids:
            continue
        row = {k: '' for k in msg_fieldnames}
        row['message_id'] = mid
        row['source'] = 'Data for Progress'
        row['source_url'] = r.get('source_url', '')
        row['date'] = r.get('date', '')
        row['message_type'] = 'tested_message'
        row['wording'] = w
        row['tags'] = 'dfp;message_test'
        topic_map = [
            ('grocery', 'economy'), ('price', 'economy'), ('cost', 'economy'),
            ('tax', 'economy'), ('gaza', 'foreign_policy'), ('israel', 'foreign_policy'),
            ('ceasefire', 'foreign_policy'), ('hostage', 'foreign_policy'),
            ('gun', 'crime'), ('health', 'healthcare'), ('medicare', 'healthcare'),
            ('abortion', 'healthcare'), ('lgbtq', 'social_issues'), ('gay', 'social_issues'),
            ('marijuana', 'social_issues'), ('corporation', 'economy'),
            ('ceo', 'economy'), ('energy', 'environment'), ('climate', 'environment'),
            ('immigration', 'immigration'), ('border', 'immigration'),
            ('irs', 'economy'), ('republican', 'government'), ('democrat', 'government'),
        ]
        for kw, topic in topic_map:
            if kw in w.lower():
                row['topic'] = topic
                break
        if not row['topic']:
            row['topic'] = 'general'
        existing.append(row)
        existing_ids.add(mid)
        dfp_added += 1

print(f"Clean DFP messages added: {dfp_added}")

# Write final CSV
with open(PROC / 'messages.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=msg_fieldnames)
    writer.writeheader()
    writer.writerows(existing)

sources = Counter(r['source'] for r in existing)
has_m = sum(1 for r in existing if r.get('support_pct','').strip() or r.get('preference_effect','').strip() or r.get('net_score','').strip())
print(f"\nFinal: {len(existing)} rows")
print(f"With metrics: {has_m}")
for s,c in sources.most_common():
    sm = sum(1 for r in existing if r['source']==s and (r.get('support_pct','').strip() or r.get('preference_effect','').strip() or r.get('net_score','').strip()))
    print(f"  {s}: {c} ({sm} with metrics)")
print(f"\nGap to 500: {500 - len(existing)}")