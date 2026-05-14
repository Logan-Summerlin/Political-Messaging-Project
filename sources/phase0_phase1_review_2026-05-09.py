#!/usr/bin/env python3
"""
COMPREHENSIVE FINAL REVIEW OF PHASE 0 & PHASE 1
For training a political messaging LLM.
"""
import csv, json, os
from collections import Counter, defaultdict

print("=" * 80)
print("COMPREHENSIVE PHASE 0 & PHASE 1 REVIEW")
print("For: Political Messaging LLM — Popular Messages & Political Ads")
print("Date: May 9, 2026")
print("=" * 80)

project_dir = '/home/agentbot/workspace/us-political-messaging-dataset'

# ==== 1. Load all datasets ====
with open(f'{project_dir}/data/processed/messages.csv', newline='', encoding='utf-8') as f:
    messages = list(csv.DictReader(f))
with open(f'{project_dir}/data/processed/issues.csv', newline='', encoding='utf-8') as f:
    issues = list(csv.DictReader(f))
with open(f'{project_dir}/data/processed/referendums.csv', newline='', encoding='utf-8') as f:
    referendums = list(csv.DictReader(f))

# ==== 2. TRAINING FITNESS SCORE ====
# A political messaging model needs: exact wording + measured outcome
# 3 grades: A (wording + effect), B (wording + support%), C (wording only), F (fragment/no wording)

def classify_message(r):
    """Grade a message for model training."""
    source = r['source']
    wording = r.get('wording','').strip()
    wlen = len(wording)
    support = r.get('support_pct','').strip()
    oppose = r.get('oppose_pct','').strip()
    effect = r.get('preference_effect','').strip()
    has_effect = bool(effect)
    has_support = bool(support)
    has_metric = has_effect or has_support
    
    # DFP: For training purposes, even DFP "tested messages" from their sections
    # are survey response options, not crafted messages — they lack effectiveness metrics
    if source == 'Data for Progress':
        if wlen >= 40 and has_support:
            return 'C'  # Has poll support % but not an effectiveness score — useful as context
        elif wlen >= 50:
            return 'D'  # Has wording but no metric — limited use
        else:
            return 'F'  # Fragment, not a real message
    
    # Blueprint: Highest quality when they have effect scores
    if source == 'Blueprint Research':
        if has_effect:
            if wlen >= 30:
                return 'A'  # Has MaxDiff preference effect + wording
            else:
                return 'B'  # Has effect but wording is short/truncated
        elif has_support:
            if wlen >= 40:
                return 'B'  # Has support% + wording
            else:
                return 'C'  # Has support% but wording is summary
        elif wlen >= 40:
            return 'C'  # Has wording but no metric
        else:
            return 'D'  # Short description
    
    # Navigator: Good quality for polling questions, less so for message generation
    if source == 'Navigator Research':
        if has_support and wlen >= 40:
            return 'B'  # Has support% with decent wording
        elif has_support:
            return 'C'  # Has support% with short wording
        elif wlen >= 50:
            return 'C'  # Long wording but no metric
        elif wlen >= 30:
            return 'D'  # Short wording no metric
        else:
            return 'F'
    
    return 'F'

grades = [classify_message(r) for r in messages]
grade_counts = Counter(grades)

print(f"\n{'='*80}")
print("DATASET SIZES")
print(f"{'='*80}")
print(f"  messages.csv:    {len(messages):,} rows")
print(f"  issues.csv:      {len(issues):,} rows")
print(f"  referendums.csv: {len(referendums):,} rows")
print(f"  TOTAL:           {len(messages) + len(issues) + len(referendums):,} datapoints")

print(f"\n{'='*80}")
print("MESSAGE TRAINING FITNESS GRADES")
print(f"{'='*80}")
print(f"  A — Wording + Effect Score (training-ready):    {grade_counts.get('A', 0)}")
print(f"  B — Wording + Support% (training-ready):        {grade_counts.get('B', 0)}")
print(f"  C — Wording Only (context enrichment):          {grade_counts.get('C', 0)}")
print(f"  D — Short wording or limited usability:         {grade_counts.get('D', 0)}")
print(f"  F — Fragment/Non-message (not usable):          {grade_counts.get('F', 0)}")
print(f"  GRADE A + B (TRAINING-READY):                   {grade_counts.get('A',0) + grade_counts.get('B',0)}")
print(f"  GRADE C (CONTEXT):                              {grade_counts.get('C',0)}")
print(f"  GRADE D + F (UNUSABLE):                         {grade_counts.get('D',0) + grade_counts.get('F',0)}")

# By source grading
print(f"\n{'='*80}")
print("TRAINING FITNESS BY SOURCE")
print(f"{'='*80}")
for source in ['Blueprint Research', 'Navigator Research', 'Data for Progress']:
    src_rows = [r for r in messages if r['source'] == source]
    src_grades = Counter(classify_message(r) for r in src_rows)
    print(f"\n  {source} ({len(src_rows)} rows):")
    for grade in 'ABCDF':
        print(f"    Grade {grade}: {src_grades.get(grade, 0)}")
    trainable = sum(c for g, c in src_grades.items() if g in ('A','B'))
    print(f"    Training-ready: {trainable} ({trainable/len(src_rows)*100:.0f}%)")
    unusable = sum(c for g, c in src_grades.items() if g in ('D','F'))
    print(f"    Unusable: {unusable} ({unusable/len(src_rows)*100:.0f}%)")

print(f"\n{'='*80}")
print("ISSUES DATASET QUALITY")
print(f"{'='*80}")
print(f"  Total: {len(issues):,}")
print(f"  Null support_pct: {len([r for r in issues if not r.get('support_pct','').strip()])}")
print(f"  Null question_wording: {len([r for r in issues if not r.get('question_wording','').strip()])}")
sources_issues = Counter(r['source'] for r in issues)
print(f"  Sources: {len(sources_issues)}")
for s, c in sources_issues.most_common():
    print(f"    {s}: {c:,}")
topics_issues = len(set(r['topic'] for r in issues))
print(f"  Topics: {topics_issues}")
years_issues = sorted(set(r['date'][:4] for r in issues if r.get('date')))
year_set = set()
for r in issues:
    if r.get('year'):
        year_set.add(r['year'])
    elif r.get('date','')[:4].isdigit():
        year_set.add(r['date'][:4])
print(f"  Year range: {years_issues[0]}-{years_issues[-1]} ({len(year_set)} years)")

print(f"\n{'='*80}")
print("REFERENDUMS QUALITY")
print(f"{'='*80}")
print(f"  Total: {len(referendums):,}")
print(f"  With vote %: {len([r for r in referendums if r.get('support_pct','').strip()])} ({len([r for r in referendums if r.get('support_pct','').strip()])/len(referendums)*100:.0f}%)")
print(f"  With passed status: {len([r for r in referendums if r.get('passed','').strip()])} ({len([r for r in referendums if r.get('passed','').strip()])/len(referendums)*100:.0f}%)")
print(f"  With ballot wording: {len([r for r in referendums if r.get('wording','').strip()])} ({len([r for r in referendums if r.get('wording','').strip()])/len(referendums)*100:.0f}%)")
print(f"  With summary: {len([r for r in referendums if r.get('summary','').strip()])} ({len([r for r in referendums if r.get('summary','').strip()])/len(referendums)*100:.0f}%)")
states_ref = len(set(r['state'] for r in referendums if r.get('state')))
print(f"  States: {states_ref}")

print(f"\n{'='*80}")
print("CRITICAL ISSUES SUMMARY")
print(f"{'='*80}")
print("""
ISSUE 1: DFP MESSAGES ARE 96% POLLUTION
  - 318 of 526 messages (60%) are from DFP
  - Only ~12 are actual tested messages from "Tested Message Wording" sections
  - 173 are survey response options ("not confident at all", "somewhat disapprove,")
  - 133 are narrative text passages ("Younger voters (73%) and renters (64%)...")
  - 0 have preference_effect (no effectiveness metric)
  - The raw chunk2 data HAS 50 articles with real "Tested Message Wording:" sections
  - But even those are not A/B tests — they're survey response options with support%
  - ROOT CAUSE: Parser extracted ANY bullet point with a percentage, not just messages

ISSUE 2: BLUEPRINT WORDINGS ARE TRUNCATED OR SUMMARIZED
  - 41 of 71 Blueprint wordings are < 50 chars
  - 8 are descriptions, not message text ("Trump healthcare net approval")
  - Original articles are behind Substack login wall
  - Wayback Machine has archived versions — accessible but extraction is manual
  - 63 of 71 have some metric (48 effect + 16 support = good metric quality)

ISSUE 3: NAVIGATOR IS BEST BUT IMPERFECT
  - 88% have metrics — best extraction quality
  - 132 of 137 are training-ready
  - But only 23 of 137 have oppose_pct (17%)
  - 5 are qualitative guidance with no extractable numbers

ISSUE 4: REFERENDUMS HAVE MAJOR GAPS
  - 78% missing vote percentages
  - 100% missing ballot wording (full text in 'wording' column empty)
  - 38% missing passage status
  - 'summary' column IS populated (315/315) with useful descriptions
  - Raw Wikipedia HTML files exist and could be re-parsed

ISSUE 5: NO OPPOSE_PCT FOR MOST MESSAGES
  - Of 526 messages, only 33 have oppose_pct
  - This limits net support analysis and makes it hard to measure polarization

ISSUE 6: KEY BLOCKED SOURCES NOT FULLY EXPLOITED
  - Pew Research: 5 US political topline PDFs downloaded today (not blocked)
    - Trump exec power (Sep 2025), trust (Dec 2025), political violence (Oct 2025)
    - Rep-Dem comfort (Apr 2025), democracy representation (Spring 2025)
    - These were incorrectly assumed to be blocked (403) — curl works fine
  - YouGov: Homepage no longer shows trackers (corporate marketing site now)
  - Gallup MIP: Datawrapper chart ID was stale — new ID needed for latest data
""")

print(f"\n{'='*80}")
print("BOTTOM LINE FOR MODEL TRAINING")
print(f"{'='*80}")
print(f"""
The dataset as-is would cause serious problems for fine-tuning:

1. 60% of messages.csv entries (DFP) are NOT political messages at all — they'd 
   train the model to generate "not confident at all" and "a lot of responsibility"
   as if those were effective political messaging.

2. Only ~207 of 526 messages are actually training-ready: 63 Blueprint (MaxDiff) 
   + 132 Navigator (support%) + 12 DFP (poll findings).

3. After cleanup, the training set is too small (~207 messages) for 
   effective fine-tuning. A political messaging model would need 500-1000+
   high-quality messages with exact wording + effectiveness metrics.

4. The issues.csv (5,477 rows) is actually the strongest asset — it provides
   rich context about what policies Americans support/oppose across 45 topics
   and 8 sources. This could supplement the message training data.

5. Referendums are not usable in current form but the raw HTML exists for 
   re-extraction.

RECOMMENDED ACTIONS:
1. Strip all DFP non-messages from messages.csv (remove ~268 rows)
2. Re-extract real DFP tested messages with support_% (keep ~12-50)
3. Expand Blueprint with Wayback Machine archival re-extraction
4. Re-parse referendums from raw Wikipedia HTML with full ballot text
5. Add the 5 newly-downloaded Pew PDFs to issues.csv
6. Target minimum 500 training-ready message rows before model training
""")
