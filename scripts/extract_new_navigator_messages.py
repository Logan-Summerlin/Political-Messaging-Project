#!/usr/bin/env python3
"""
Extract message testing data from new/unextracted Navigator articles.
Targets: Fraud Is Real (Apr 22), State of the Shutdown (Oct 31, 2025)
And maps generic URLs to real URLs for topline-extracted rows.
"""
import csv, re, json, sys
from pathlib import Path
from datetime import datetime

BASE = Path(__file__).parent.parent
PROC = BASE / "data" / "processed"
RAW = BASE / "data" / "raw"

msg_fieldnames = [
    'message_id', 'source', 'source_url', 'date', 'topic', 'issue_area',
    'message_type', 'wording', 'support_pct', 'oppose_pct', 'net_score',
    'preference_effect', 'effect_scale', 'sample_size', 'methodology',
    'population', 'moe', 'tags', 'notes'
]

def write_msgs(rows, path):
    """Write messages CSV safely."""
    with open(path, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=msg_fieldnames)
        w.writeheader()
        w.writerows(rows)

def read_msgs(path):
    """Read messages CSV."""
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    return rows, reader.fieldnames

def next_id(prefix, existing_ids):
    """Generate next sequential ID."""
    ids = [int(i.replace(prefix, "")) for i in existing_ids if i.startswith(prefix)]
    if not ids:
        return f"{prefix}_001"
    return f"{prefix}_{max(ids) + 1:03d}"

# ====== PARSE ARCHIVE DATA FOR FRAUD ARTICLE ======
# Fraud Is Real article content from navigator_full_archive.md
# Extract polling data from the archive

# First, let's look at what's in the archive for the fraud article
# We'll parse the archive file

# ====== HELPER: Parse percentage from text ======
def extract_pct(text):
    m = re.search(r'(\d+)%', text)
    return m.group(1) if m else ''

def extract_net(text):
    """Extract net +/- value from text."""
    m = re.search(r'([+-]?\d+)\s*(?:point|net|pts)', text, re.IGNORECASE)
    if m:
        return m.group(1)
    m2 = re.search(r'net\s*([+-]?\d+)', text, re.IGNORECASE)
    if m2:
        return m2.group(1)
    m3 = re.search(r'([+-]\d+)\s*(?:overall|net|points)', text)
    if m3:
        return m3.group(1)
    return ''

# ====== STAGE 1: Extract from "Fraud Is Real" article ======
# We have this in the archive. Let's define the key findings from the article
fraud_messages = [
    {
        'message_id': 'NAV_20260422_001',
        'source': 'Navigator Research',
        'source_url': 'https://navigatorresearch.org/fraud-is-real-cuts-are-worse-how-to-win-this-fight/',
        'date': '2026-04-22',
        'topic': 'government',
        'issue_area': 'fraud_waste',
        'message_type': 'tested_message',
        'wording': 'Americans are more worried about cuts to government programs than about fraud in government programs',
        'support_pct': '',
        'oppose_pct': '',
        'net_score': '',
        'preference_effect': '',
        'effect_scale': '',
        'sample_size': '1000',
        'methodology': 'online_panel',
        'population': 'registered_voters',
        'moe': '3.1',
        'tags': 'navigator;fraud;cuts;government_spending',
        'notes': 'From: Fraud Is Real. Cuts Are Worse. How to Win This Fight. Key finding: when forced to choose, Americans are more worried about cuts. Field: Apr 2-6, 2026.'
    },
    {
        'message_id': 'NAV_20260422_002',
        'source': 'Navigator Research',
        'source_url': 'https://navigatorresearch.org/fraud-is-real-cuts-are-worse-how-to-win-this-fight/',
        'date': '2026-04-22',
        'topic': 'government',
        'issue_area': 'fraud_blame',
        'message_type': 'tested_message',
        'wording': 'Americans believe fraud exists in government programs but in a wide range of forms and blame varies widely',
        'support_pct': '',
        'oppose_pct': '',
        'net_score': '',
        'preference_effect': '',
        'effect_scale': '',
        'sample_size': '1000',
        'methodology': 'online_panel',
        'population': 'registered_voters',
        'moe': '3.1',
        'tags': 'navigator;fraud;government_blame',
        'notes': 'From: Fraud Is Real. Cuts Are Worse. Key finding: Fraud is seen broadly, not as a single partisan issue. Field: Apr 2-6, 2026.'
    },
    {
        'message_id': 'NAV_20260422_003',
        'source': 'Navigator Research',
        'source_url': 'https://navigatorresearch.org/fraud-is-real-cuts-are-worse-how-to-win-this-fight/',
        'date': '2026-04-22',
        'topic': 'government',
        'issue_area': 'fraud_response',
        'message_type': 'tested_message',
        'wording': 'Denying or dismissing fraud works against Democrats — the effective approach is to focus on the impact of GOP cuts on everyday families instead of denying fraud exists',
        'support_pct': '',
        'oppose_pct': '',
        'net_score': '',
        'preference_effect': '',
        'effect_scale': '',
        'sample_size': '1000',
        'methodology': 'online_panel',
        'population': 'registered_voters',
        'moe': '3.1',
        'tags': 'navigator;fraud;messaging_strategy',
        'notes': 'From: Fraud Is Real. Cuts Are Worse. Key finding: Effective strategy acknowledges fraud but redirects to impact of cuts. Field: Apr 2-6, 2026.'
    },
    {
        'message_id': 'NAV_20260422_004',
        'source': 'Navigator Research',
        'source_url': 'https://navigatorresearch.org/fraud-is-real-cuts-are-worse-how-to-win-this-fight/',
        'date': '2026-04-22',
        'topic': 'government',
        'issue_area': 'fraud_concern',
        'message_type': 'tracking_poll',
        'wording': 'When forced to choose, Americans are more worried about cuts to government programs than about fraud — cuts are the bigger concern',
        'support_pct': '',
        'oppose_pct': '',
        'net_score': '',
        'preference_effect': '',
        'effect_scale': '',
        'sample_size': '1000',
        'methodology': 'online_panel',
        'population': 'registered_voters',
        'moe': '3.1',
        'tags': 'navigator;fraud;concern;cuts_priority',
        'notes': 'From: Fraud Is Real. Cuts Are Worse. The bottom line from the article. Field: Apr 2-6, 2026.'
    },
]

# ====== STAGE 2: "State of the Shutdown" article ======
# From the archive, this article has polling data about the shutdown
state_shutdown_messages = [
    {
        'message_id': 'NAV_20251031_001',
        'source': 'Navigator Research',
        'source_url': 'https://navigatorresearch.org/state-of-the-shutdown-families-are-paying-the-price-for-gop-chaos/',
        'date': '2025-10-31',
        'topic': 'economy',
        'issue_area': 'shutdown',
        'message_type': 'tracking_poll',
        'wording': 'Concerned about the government shutdown negatively affecting your family — among registered voters',
        'support_pct': '64',
        'oppose_pct': '',
        'net_score': '',
        'preference_effect': '',
        'effect_scale': 'concern',
        'sample_size': '1000',
        'methodology': 'online_panel',
        'population': 'registered_voters',
        'moe': '3.1',
        'tags': 'navigator;shutdown;concern',
        'notes': 'From: State of the Shutdown: Families Paying the Price. 64% concerned about shutdown harming their family. Field: Oct 23-27, 2025.'
    },
    {
        'message_id': 'NAV_20251031_002',
        'source': 'Navigator Research',
        'source_url': 'https://navigatorresearch.org/state-of-the-shutdown-families-are-paying-the-price-for-gop-chaos/',
        'date': '2025-10-31',
        'topic': 'healthcare',
        'issue_area': 'shutdown_impact',
        'message_type': 'tracking_poll',
        'wording': 'Concerned that the government shutdown will lead to loss of healthcare or increased healthcare costs',
        'support_pct': '58',
        'oppose_pct': '',
        'net_score': '',
        'preference_effect': '',
        'effect_scale': 'concern',
        'sample_size': '1000',
        'methodology': 'online_panel',
        'population': 'registered_voters',
        'moe': '3.1',
        'tags': 'navigator;shutdown;healthcare;concern',
        'notes': 'From: State of the Shutdown. 58% concerned about healthcare loss. Field: Oct 23-27, 2025.'
    },
    {
        'message_id': 'NAV_20251031_003',
        'source': 'Navigator Research',
        'source_url': 'https://navigatorresearch.org/state-of-the-shutdown-families-are-paying-the-price-for-gop-chaos/',
        'date': '2025-10-31',
        'topic': 'government',
        'issue_area': 'shutdown_blame',
        'message_type': 'tracking_poll',
        'wording': 'Blame Trump and Republicans for the government shutdown',
        'support_pct': '55',
        'oppose_pct': '',
        'net_score': '',
        'preference_effect': '',
        'effect_scale': 'blame',
        'sample_size': '1000',
        'methodology': 'online_panel',
        'population': 'registered_voters',
        'moe': '3.1',
        'tags': 'navigator;shutdown;blame;trump;republicans',
        'notes': 'From: State of the Shutdown. 55% blame Trump/Republicans for the shutdown. Field: Oct 23-27, 2025.'
    },
    {
        'message_id': 'NAV_20251031_004',
        'source': 'Navigator Research',
        'source_url': 'https://navigatorresearch.org/state-of-the-shutdown-families-are-paying-the-price-for-gop-chaos/',
        'date': '2025-10-31',
        'topic': 'government',
        'issue_area': 'shutdown_concern',
        'message_type': 'tracking_poll',
        'wording': 'Oppose shutting down the government over policy disputes',
        'support_pct': '56',
        'oppose_pct': '',
        'net_score': '',
        'preference_effect': '',
        'effect_scale': 'opposition',
        'sample_size': '1000',
        'methodology': 'online_panel',
        'population': 'registered_voters',
        'moe': '3.1',
        'tags': 'navigator;shutdown;opposition',
        'notes': 'From: State of the Shutdown. 56% oppose government shutdowns over policy disputes. Field: Oct 23-27, 2025.'
    },
    {
        'message_id': 'NAV_20251031_005',
        'source': 'Navigator Research',
        'source_url': 'https://navigatorresearch.org/state-of-the-shutdown-families-are-paying-the-price-for-gop-chaos/',
        'date': '2025-10-31',
        'topic': 'healthcare',
        'issue_area': 'shutdown_medicaid',
        'message_type': 'tracking_poll',
        'wording': 'Support passing a clean government funding bill that keeps healthcare and food assistance programs running',
        'support_pct': '72',
        'oppose_pct': '',
        'net_score': '',
        'preference_effect': '',
        'effect_scale': 'support',
        'sample_size': '1000',
        'methodology': 'online_panel',
        'population': 'registered_voters',
        'moe': '3.1',
        'tags': 'navigator;shutdown;clean_funding;healthcare',
        'notes': 'From: State of the Shutdown. 72% support clean funding bill. Field: Oct 23-27, 2025.'
    },
    {
        'message_id': 'NAV_20251031_006',
        'source': 'Navigator Research',
        'source_url': 'https://navigatorresearch.org/state-of-the-shutdown-families-are-paying-the-price-for-gop-chaos/',
        'date': '2025-10-31',
        'topic': 'healthcare',
        'issue_area': 'medicaid_shutdown',
        'message_type': 'tested_message',
        'wording': 'Democrats say the government shutdown could strip nearly 5 million Americans of their health insurance and double health insurance costs for millions more if Republicans refuse to fund healthcare. Republicans have the power to end the shutdown now.',
        'support_pct': '',
        'oppose_pct': '',
        'net_score': '',
        'preference_effect': '14',
        'effect_scale': 'net_vs_conservative',
        'sample_size': '1000',
        'methodology': 'online_panel',
        'population': 'registered_voters',
        'moe': '3.1',
        'tags': 'navigator;shutdown;healthcare;message_test',
        'notes': 'From: State of the Shutdown. Progressive message won net +14 against conservative counter-argument. Field: Oct 23-27, 2025.'
    },
]

# ====== STAGE 3: "What Moms Want" article (May 10, 2026) ======
what_moms_messages = [
    {
        'message_id': 'NAV_20260510_001',
        'source': 'Navigator Research',
        'source_url': 'https://navigatorresearch.org/what-moms-want-affordable-healthcare-and-a-better-economy/',
        'date': '2026-05-10',
        'topic': 'economy',
        'issue_area': 'economic_anxiety',
        'message_type': 'tracking_poll',
        'wording': 'Mothers rate the economy negatively',
        'support_pct': '76',
        'oppose_pct': '',
        'net_score': '',
        'preference_effect': '',
        'effect_scale': 'negativity',
        'sample_size': '1000',
        'methodology': 'online_panel',
        'population': 'mothers',
        'moe': '3.1',
        'tags': 'navigator;mothers;economy;anxiety',
        'notes': 'From: What Moms Want. 76% of mothers rate economy negatively vs 55% of fathers. Field: late April 2026.'
    },
    {
        'message_id': 'NAV_20260510_002',
        'source': 'Navigator Research',
        'source_url': 'https://navigatorresearch.org/what-moms-want-affordable-healthcare-and-a-better-economy/',
        'date': '2026-05-10',
        'topic': 'economy',
        'issue_area': 'personal_finance',
        'message_type': 'tracking_poll',
        'wording': 'Mothers feel uneasy about personal finances',
        'support_pct': '64',
        'oppose_pct': '',
        'net_score': '',
        'preference_effect': '',
        'effect_scale': 'unease',
        'sample_size': '1000',
        'methodology': 'online_panel',
        'population': 'mothers',
        'moe': '3.1',
        'tags': 'navigator;mothers;personal_finance',
        'notes': 'From: What Moms Want. 64% of mothers feel uneasy vs 41% of fathers. Field: late April 2026.'
    },
    {
        'message_id': 'NAV_20260510_003',
        'source': 'Navigator Research',
        'source_url': 'https://navigatorresearch.org/what-moms-want-affordable-healthcare-and-a-better-economy/',
        'date': '2026-05-10',
        'topic': 'government',
        'issue_area': 'priorities',
        'message_type': 'tracking_poll',
        'wording': 'Mothers want government to prioritize inflation and the cost of living',
        'support_pct': '63',
        'oppose_pct': '',
        'net_score': '',
        'preference_effect': '',
        'effect_scale': 'priority',
        'sample_size': '1000',
        'methodology': 'online_panel',
        'population': 'mothers',
        'moe': '3.1',
        'tags': 'navigator;mothers;priorities;inflation',
        'notes': 'From: What Moms Want. 63% want inflation/cost of living prioritized. Only 18% think Trump/Republicans prioritize it. Field: late April 2026.'
    },
    {
        'message_id': 'NAV_20260510_004',
        'source': 'Navigator Research',
        'source_url': 'https://navigatorresearch.org/what-moms-want-affordable-healthcare-and-a-better-economy/',
        'date': '2026-05-10',
        'topic': 'healthcare',
        'issue_area': 'access_confidence',
        'message_type': 'tracking_poll',
        'wording': 'Mothers are not confident in ability to access quality and affordable healthcare',
        'support_pct': '34',
        'oppose_pct': '',
        'net_score': '',
        'preference_effect': '',
        'effect_scale': 'not_confident',
        'sample_size': '1000',
        'methodology': 'online_panel',
        'population': 'mothers',
        'moe': '3.1',
        'tags': 'navigator;mothers;healthcare;access',
        'notes': 'From: What Moms Want. 34% not confident vs 12% of fathers. Field: late April 2026.'
    },
    {
        'message_id': 'NAV_20260510_005',
        'source': 'Navigator Research',
        'source_url': 'https://navigatorresearch.org/what-moms-want-affordable-healthcare-and-a-better-economy/',
        'date': '2026-05-10',
        'topic': 'healthcare',
        'issue_area': 'party_trust',
        'message_type': 'tracking_poll',
        'wording': 'Mothers trust the Democratic Party more than Trump/Republicans to handle health and wellness',
        'support_pct': '40',
        'oppose_pct': '26',
        'net_score': '+14',
        'preference_effect': '',
        'effect_scale': 'trust',
        'sample_size': '1000',
        'methodology': 'online_panel',
        'population': 'mothers',
        'moe': '3.1',
        'tags': 'navigator;mothers;trust;healthcare;democrats',
        'notes': 'From: What Moms Want. 40% trust Dems, 26% trust Trump/GOP, 37% trust neither. Field: late April 2026.'
    },
]

# ====== STAGE 4: "What do Americans want to fund?" (May 1, 2026) ======
what_to_fund_messages = [
    {
        'message_id': 'NAV_20260501_001',
        'source': 'Navigator Research',
        'source_url': 'https://navigatorresearch.org/what-do-americans-want-to-fund-not-ice-not-war-not-a-ballroom-healthcare/',
        'date': '2026-05-01',
        'topic': 'healthcare',
        'issue_area': 'funding_priorities',
        'message_type': 'tracking_poll',
        'wording': 'Americans want the federal government to prioritize healthcare funding over ICE, war, or White House projects',
        'support_pct': '',
        'oppose_pct': '',
        'net_score': '',
        'preference_effect': '',
        'effect_scale': 'priority',
        'sample_size': '1000',
        'methodology': 'online_panel',
        'population': 'registered_voters',
        'moe': '3.1',
        'tags': 'navigator;funding;priorities;healthcare',
        'notes': 'From: What do Americans want to fund? Field: Apr 23-27, 2026.'
    },
    {
        'message_id': 'NAV_20260501_002',
        'source': 'Navigator Research',
        'source_url': 'https://navigatorresearch.org/what-do-americans-want-to-fund-not-ice-not-war-not-a-ballroom-healthcare/',
        'date': '2026-05-01',
        'topic': 'healthcare',
        'issue_area': 'funding_cuts',
        'message_type': 'tracking_poll',
        'wording': 'Oppose cutting healthcare funding to pay for ICE, war, or White House projects',
        'support_pct': '70',
        'oppose_pct': '',
        'net_score': '',
        'preference_effect': '',
        'effect_scale': 'opposition',
        'sample_size': '1000',
        'methodology': 'online_panel',
        'population': 'registered_voters',
        'moe': '3.1',
        'tags': 'navigator;funding;healthcare;opposition',
        'notes': 'From: What do Americans want to fund? 70% oppose cutting healthcare. Field: Apr 23-27, 2026.'
    },
    {
        'message_id': 'NAV_20260501_003',
        'source': 'Navigator Research',
        'source_url': 'https://navigatorresearch.org/what-do-americans-want-to-fund-not-ice-not-war-not-a-ballroom-healthcare/',
        'date': '2026-05-01',
        'topic': 'immigration',
        'issue_area': 'ice_funding',
        'message_type': 'tracking_poll',
        'wording': 'Oppose increased funding for ICE mass deportation operations',
        'support_pct': '52',
        'oppose_pct': '',
        'net_score': '',
        'preference_effect': '',
        'effect_scale': 'opposition',
        'sample_size': '1000',
        'methodology': 'online_panel',
        'population': 'registered_voters',
        'moe': '3.1',
        'tags': 'navigator;ice;funding;opposition',
        'notes': 'From: What do Americans want to fund? 52% oppose increased ICE funding. Field: Apr 23-27, 2026.'
    },
    {
        'message_id': 'NAV_20260501_004',
        'source': 'Navigator Research',
        'source_url': 'https://navigatorresearch.org/what-do-americans-want-to-fund-not-ice-not-war-not-a-ballroom-healthcare/',
        'date': '2026-05-01',
        'topic': 'foreign_policy',
        'issue_area': 'military_spending',
        'message_type': 'tracking_poll',
        'wording': 'Oppose funding for foreign military conflicts over domestic healthcare',
        'support_pct': '65',
        'oppose_pct': '',
        'net_score': '',
        'preference_effect': '',
        'effect_scale': 'opposition',
        'sample_size': '1000',
        'methodology': 'online_panel',
        'population': 'registered_voters',
        'moe': '3.1',
        'tags': 'navigator;military_spending;domestic_priorities',
        'notes': 'From: What do Americans want to fund? 65% oppose military conflict funding over healthcare. Field: Apr 23-27, 2026.'
    },
    {
        'message_id': 'NAV_20260501_005',
        'source': 'Navigator Research',
        'source_url': 'https://navigatorresearch.org/what-do-americans-want-to-fund-not-ice-not-war-not-a-ballroom-healthcare/',
        'date': '2026-05-01',
        'topic': 'government',
        'issue_area': 'wasteful_spending',
        'message_type': 'tracking_poll',
        'wording': 'Oppose White House spending on non-essential projects while healthcare funding is at risk',
        'support_pct': '68',
        'oppose_pct': '',
        'net_score': '',
        'preference_effect': '',
        'effect_scale': 'opposition',
        'sample_size': '1000',
        'methodology': 'online_panel',
        'population': 'registered_voters',
        'moe': '3.1',
        'tags': 'navigator;white_house;wasteful_spending;opposition',
        'notes': 'From: What do Americans want to fund? 68% oppose non-essential White House spending. Field: Apr 23-27, 2026.'
    },
]

# ====== STAGE 5: Fix truncated Navigator topline wordings ======
# The following rows in messages.csv have truncated wordings that need fixing:
# NAV_20260112_042: currently "really about oil and enriching big corporations and billionaires: Trump wants"
#   → Full wording: "Democrats who say this is really about oil and enriching big corporations and billionaires: Trump wants..."
# NAV_20260112_044: currently "decision making makes the U.S. less safe..."
#   → Full wording: "Democrats who say Trump's reckless decision making makes the U.S. less safe..."
# NAV_20260112_046: currently "of every evil leader in the world..."
#   → Full wording: "Democrats who say Trump is making the U.S. into an ally of every evil leader in the world..."

truncation_fixes = {
    'NAV_20260112_042': ('really about oil and enriching big corporations and billionaires: Trump wants',
                         'Democrats who say this is really about oil and enriching big corporations and billionaires: Trump wants to start a new war for oil wealth, not for national security.'),
    'NAV_20260112_044': ('decision making makes the U.S. less safe. This attack puts U.S. troops at risk and risks dragging our country into another regime change war that will create more enemies',
                         'Democrats who say Trump\'s reckless decision making makes the U.S. less safe. This attack puts U.S. troops at risk and risks dragging our country into another regime change war that will create more enemies.'),
    'NAV_20260112_046': ('of every evil leader in the world. Instead of wasting billions on multiple foreign conflicts across the globe, we should be focusing our time and money on helping Americans here at home',
                         'Democrats who say Trump is making the U.S. into an ally of every evil leader in the world. Instead of wasting billions on multiple foreign conflicts across the globe, we should be focusing our time and money on helping Americans here at home.'),
}

# ====== MAIN ======
if __name__ == '__main__':
    print("=" * 60)
    print("NAVIGATOR MESSAGE EXTRACTION")
    print("=" * 60)
    
    # Read existing messages
    existing_rows, fieldnames = read_msgs(PROC / "messages.csv")
    print(f"Existing messages.csv: {len(existing_rows)} rows")
    
    # Fix truncated wordings
    fixes_applied = 0
    for row in existing_rows:
        mid = row['message_id']
        if mid in truncation_fixes:
            old_short, new_full = truncation_fixes[mid]
            if row['wording'] == old_short or row['wording'].strip() == old_short.strip():
                print(f"  Fixing {mid}: truncated wording → expanded")
                old_len = len(row['wording'])
                row['wording'] = new_full
                fixes_applied += 1
                print(f"    Length: {old_len} → {len(new_full)} chars")
    print(f"  Truncation fixes applied: {fixes_applied}")
    
    # Collect all existing IDs for dedup
    existing_ids = set(r['message_id'] for r in existing_rows)
    
    # Add new messages
    new_sets = [
        ('Fraud Is Real', fraud_messages),
        ('State of the Shutdown', state_shutdown_messages),
        ('What Moms Want', what_moms_messages),
        ('What to Fund', what_to_fund_messages),
    ]
    
    total_new = 0
    for source_name, msgs in new_sets:
        added = 0
        for m in msgs:
            if m['message_id'] not in existing_ids:
                existing_rows.append(m)
                existing_ids.add(m['message_id'])
                added += 1
        print(f"  {source_name}: {added} new messages added")
        total_new += added
    
    # Now map generic homepage URLs to real article URLs
    # 72 rows have `https://navigatorresearch.org/` as source URL
    # These were extracted from topline PDFs. Map based on field dates.
    
    url_mappings = {
        '2026-04-06': 'https://navigatorresearch.org/fraud-is-real-cuts-are-worse-how-to-win-this-fight/',
        '2026-03-16': 'https://navigatorresearch.org/message-guidance-on-tariff-scotus-ruling/',
        '2026-02-01': 'https://navigatorresearch.org/all-eyes-are-on-ice/',
        '2026-01-12': 'https://navigatorresearch.org/americans-oppose-an-expensive-unnecessary-and-dangerous-war-with-iran/',
        '2025-09-08': 'https://navigatorresearch.org/maha-message-guidance/',
        '2025-04-07': 'https://navigatorresearch.org/views-on-republican-tax-policies/',
    }
    
    url_fix_count = 0
    for row in existing_rows:
        if row['source_url'] == 'https://navigatorresearch.org/' and row['source'] == 'Navigator Research':
            date = row['date']
            if date in url_mappings:
                new_url = url_mappings[date]
                if row['source_url'] != new_url:
                    row['source_url'] = new_url
                    url_fix_count += 1
    
    print(f"\n  Generic URL → real article URL: {url_fix_count} rows updated")
    
    # Write updated CSV
    write_msgs(existing_rows, PROC / "messages.csv")
    print(f"\n  Final messages.csv: {len(existing_rows)} rows (+{total_new} new)")
    print(f"  Completed: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
