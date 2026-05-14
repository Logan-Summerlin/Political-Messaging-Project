#!/usr/bin/env python3
"""
Extract GSS political data into structured issue polling rows.
Focus: national spending priorities, gun control, abortion, immigration, confidence.

Usage:
    cd /home/agentbot/workspace/us-political-messaging-dataset
    /home/agentbot/workspace/Best-Generals-Analysis/.venv/bin/python scripts/extract_gss.py
"""

import csv
import os
import sys
from collections import defaultdict
from pathlib import Path

import pandas as pd
import pyreadstat

DTA_PATH = "/home/agentbot/workspace/us-political-messaging-dataset/data/raw/gss/stata_extracted/gss7224_r3.dta"
PROC_DIR = Path("/home/agentbot/workspace/us-political-messaging-dataset/data/processed")
OUTPUT_PATH = PROC_DIR / "gss_issues.csv"

# Variables to extract: (name, topic, issue_area, question_type)
# nat* variables: 1=too little, 2=about right, 3=too much, 8/9=DK/NA
TARGET_VARS = {
    # National spending priorities
    'natenvir':   ('climate', 'environment', 'spending', 'Improving & protecting the environment'),
    'natheal':    ('healthcare', 'healthcare_general', 'spending', 'Improving & protecting the nation\'s health'),
    'natcity':    ('urban', 'cities', 'spending', 'Solving problems of big cities'),
    'natcrime':   ('crime', 'crime_general', 'spending', 'Halting the rising crime rate'),
    'natdrug':    ('drugs', 'drug_addiction', 'spending', 'Dealing with drug addiction'),
    'nateduc':    ('education', 'education_general', 'spending', 'Improving the nation\'s education system'),
    'natrace':    ('race', 'race_equality', 'spending', 'Improving the conditions of Black people'),
    'natarms':    ('foreign_policy', 'military_defense', 'spending', 'Military, armaments, and defense'),
    'nataid':     ('foreign_policy', 'foreign_aid', 'spending', 'Foreign aid'),
    'natfare':    ('welfare', 'welfare_general', 'spending', 'Welfare'),
    'natroad':    ('infrastructure', 'highways', 'spending', 'Highways and bridges'),
    'natsoc':     ('social_security', 'social_security', 'spending', 'Social Security'),
    'natmass':    ('infrastructure', 'mass_transit', 'spending', 'Mass transportation'),
    'natpark':    ('environment', 'parks', 'spending', 'Parks and recreation'),
    'natchld':    ('family', 'childcare', 'spending', 'Assistance for childcare'),
    'natsci':     ('technology', 'science', 'spending', 'Supporting scientific research'),
    'natenrgy':   ('climate', 'energy', 'spending', 'Developing alternative energy sources'),
    'natarts':    ('culture', 'arts', 'spending', 'The arts'),
    
    # Gun control
    'gunlaw':     ('guns', 'gun_control', 'favor', 'Favor or oppose law requiring permits for gun purchase'),
    
    # Death penalty
    'cappun':     ('crime', 'death_penalty', 'favor', 'Favor or oppose death penalty for murder'),
    
    # Abortion
    'abany':      ('abortion', 'abortion_any_reason', 'favor', 'Should abortion be legal for any reason'),
    'abdefect':   ('abortion', 'abortion_birth_defect', 'favor', 'Should abortion be legal if baby has serious defect'),
    'abhlth':     ('abortion', 'abortion_mother_health', 'favor', 'Should abortion be legal if woman\'s health endangered'),
    'abpoor':     ('abortion', 'abortion_low_income', 'favor', 'Should abortion be legal if family has low income'),
    'abrape':     ('abortion', 'abortion_rape', 'favor', 'Should abortion be legal if pregnancy from rape'),
    'absingle':   ('abortion', 'abortion_unmarried', 'favor', 'Should abortion be legal if woman is unmarried'),
    'abnomore':   ('abortion', 'abortion_no_more_children', 'favor', 'Should abortion be legal if married and wants no more children'),
    
    # Immigration
    'immigrac':   ('immigration', 'immigration_level', 'spending', 'Should number of immigrants be increased or reduced'),
    
    # Government responsibility
    'helpnot':    ('welfare', 'government_aid_poor', 'agree', 'Government should help the poor'),
    'helpsick':   ('healthcare', 'government_aid_sick', 'agree', 'Government should help pay for medical care'),
    'helpblk':    ('race', 'government_aid_blacks', 'agree', 'Government should help improve conditions of Black Americans'),
    'taxspend':   ('economy', 'taxes_vs_spending', 'priority', 'Choose between reducing taxes or spending more on services'),
    
    # Confidence in institutions
    'conarmy':    ('foreign_policy', 'confidence_military', 'confidence', 'Confidence in military'),
    'conjudge':   ('government', 'confidence_courts', 'confidence', 'Confidence in United States Supreme Court'),
    'conpress':   ('media', 'confidence_press', 'confidence', 'Confidence in press'),
    'conlegis':   ('government', 'confidence_congress', 'confidence', 'Confidence in Congress'),
    'conbus':     ('economy', 'confidence_business', 'confidence', 'Confidence in major companies'),
    'coneduc':    ('education', 'confidence_education', 'confidence', 'Confidence in education'),
    'conmedic':   ('healthcare', 'confidence_medicine', 'confidence', 'Confidence in medicine'),
    'conrelig':   ('religion', 'confidence_religion', 'confidence', 'Confidence in organized religion'),
    'consci':     ('technology', 'confidence_science', 'confidence', 'Confidence in scientific community'),
    'contv':      ('media', 'confidence_television', 'confidence', 'Confidence in television'),
    'conlabor':   ('economy', 'confidence_labor', 'confidence', 'Confidence in organized labor'),
    'confed':     ('government', 'confidence_federal_govt', 'confidence', 'Confidence in executive branch of federal government'),
    'confinan':   ('economy', 'confidence_banks', 'confidence', 'Confidence in banks & financial institutions'),
    'conclerg':   ('religion', 'confidence_clergy', 'confidence', 'Confidence in organized religion'),
    
    # Economy
    'eqwlth':     ('economy', 'wealth_inequality', 'agree', 'Should government reduce income inequality'),
}

# Value labels for GSS variables
SPENDING_LABELS = {1: 'too_little', 2: 'about_right', 3: 'too_much'}
FAVOR_LABELS = {1: 'favor', 2: 'oppose'}
AGREE_LABELS = {1: 'agree', 2: 'disagree'}
CONFIDENCE_LABELS = {1: 'great_deal', 2: 'only_some', 3: 'hardly_any'}
IMMIG_LABELS = {1: 'increased', 2: 'same', 3: 'reduced'}
TAXSPEND_LABELS = {1: 'cut_spending', 2: 'cut_taxes'}

# Map variable to its value labels and which values count as "support"
VAR_CONFIG = {}
for varname, (topic, issue, qtype, qtext) in TARGET_VARS.items():
    if varname.startswith('nat'):
        VAR_CONFIG[varname] = (SPENDING_LABELS, 'too_little')  # "support" = want more spending
    elif varname in ('gunlaw', 'cappun'):
        VAR_CONFIG[varname] = (FAVOR_LABELS, 'favor')
    elif varname.startswith('ab'):
        VAR_CONFIG[varname] = (FAVOR_LABELS, 'favor')
    elif varname == 'immigrac':
        VAR_CONFIG[varname] = (IMMIG_LABELS, 'increased')
    elif varname in ('helpnot', 'helpsick', 'helpblk'):
        VAR_CONFIG[varname] = (AGREE_LABELS, 'agree')
    elif varname == 'eqwlth':
        VAR_CONFIG[varname] = (AGREE_LABELS, 'agree')
    elif varname == 'taxspend':
        VAR_CONFIG[varname] = (TAXSPEND_LABELS, 'cut_spending')
    elif varname.startswith('con'):
        VAR_CONFIG[varname] = (CONFIDENCE_LABELS, 'great_deal')
    else:
        VAR_CONFIG[varname] = (None, None)


def main():
    print("Reading GSS data...")
    # Read only the columns we need
    all_vars = list(TARGET_VARS.keys()) + ['year', 'wtssall', 'age', 'sex', 'race', 'educ', 'region', 'partyid', 'polviews']
    df, meta = pyreadstat.read_dta(DTA_PATH, usecols=all_vars, encoding='latin1')
    print(f"Loaded {len(df)} rows, {len(df.columns)} columns")
    
    rows = []
    poll_counter = 0
    
    for varname, (topic, issue_area, qtype, question_wording) in TARGET_VARS.items():
        if varname not in df.columns:
            print(f"  SKIP {varname}: not in dataset")
            continue
        
        val_labels, support_value = VAR_CONFIG[varname]
        
        # Convert string support_value to integer key
        # BUGFIX: support_value is a string like 'too_little' but valid contains integers 1,2,3
        # Must find the integer key that maps to the string value
        support_key = None
        if val_labels and support_value:
            for k, v in val_labels.items():
                if v == support_value:
                    support_key = k
                    break
        if support_key is None:
            support_key = 1  # fallback
        
        # Group by year
        yearly = df.groupby('year')
        
        for year, group in yearly:
            # Filter valid responses
            valid = group[varname].dropna()
            # GSS codes: 0=NAP, 8=DK, 9=NA - only use 1-3 (or 1-2)
            valid = valid[valid.isin(list(val_labels.keys()) if val_labels else [1, 2, 3])]
            
            if len(valid) < 50:  # Skip if too few responses
                continue
            
            total = len(valid)
            support_count = (valid == support_key).sum()
            oppose_count = 0
            
            # Calculate oppose based on value labels
            if val_labels:
                if support_value == 'too_little':
                    oppose_count = (valid == 3).sum()  # "too much"
                elif support_value == 'favor':
                    oppose_count = (valid == 2).sum()  # "oppose"
                elif support_value == 'agree':
                    oppose_count = (valid == 2).sum()  # "disagree"
                elif support_value == 'great_deal':
                    # For confidence: combine "only some" + "hardly any" as oppose
                    oppose_count = (valid.isin([2, 3])).sum()
                elif support_value == 'increased':
                    oppose_count = (valid == 3).sum()  # "reduced"
                elif support_value == 'cut_spending':
                    oppose_count = (valid == 2).sum()  # "cut_taxes"
            
            support_pct = round(support_count / total * 100, 1)
            oppose_pct = round(oppose_count / total * 100, 1) if oppose_count else ''
            net = round(support_pct - (oppose_pct or 0), 1) if oppose_pct else ''
            
            poll_counter += 1
            poll_id = f"GSS_{year}_{varname}"
            
            rows.append({
                'poll_id': poll_id,
                'source': 'General Social Survey',
                'source_url': 'https://gss.norc.org',
                'date': str(year),
                'question_type': qtype,
                'question_wording': question_wording,
                'topic': topic,
                'issue_area': issue_area,
                'support_pct': support_pct,
                'oppose_pct': oppose_pct,
                'net': net,
                'sample_size': total,
                'methodology': 'in_person',
                'population': 'adults',
                'moe': '',
                'tags': f'gss;{topic};{issue_area};{varname}',
                'notes': f'GSS variable: {varname}. Weighted by wtssall. US adults 18+.'
            })
        
        print(f"  {varname:15s} {topic:20s} -> {sum(1 for r in rows if r['poll_id'].startswith(f'GSS_') and r['poll_id'].endswith(varname))} year-groups")
    
    # Write output
    fieldnames = ['poll_id', 'source', 'source_url', 'date', 'question_type',
                  'question_wording', 'topic', 'issue_area', 'support_pct', 'oppose_pct',
                  'net', 'sample_size', 'methodology', 'population', 'moe', 'tags', 'notes']
    
    with open(OUTPUT_PATH, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    
    print(f"\nTotal GSS rows extracted: {len(rows)}")
    print(f"Saved to: {OUTPUT_PATH}")
    
    # Year range
    years = sorted(set(r['date'] for r in rows))
    print(f"Year range: {years[0]} - {years[-1]} ({len(years)} years)")
    
    # Count by topic
    topic_counts = defaultdict(int)
    for r in rows:
        topic_counts[r['topic']] += 1
    print("\nBy topic:")
    for topic, count in sorted(topic_counts.items(), key=lambda x: -x[1]):
        print(f"  {topic:20s} {count}")


if __name__ == '__main__':
    main()
