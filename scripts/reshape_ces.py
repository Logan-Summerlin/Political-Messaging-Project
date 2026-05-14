#!/usr/bin/env python3
"""
Reshape CES wide-format data (16 rows, 100+ columns) into issues.csv long format.
One row per issue per year.
Uses only standard library (csv module).

Usage: python3 reshape_ces.py
"""

import csv
import os
import sys

INPUT = "/home/agentbot/workspace/us-political-messaging-dataset/data/processed/ces_extracted.csv"
OUTPUT = "/home/agentbot/workspace/us-political-messaging-dataset/data/processed/ces_reshaped.csv"

SOURCE_URL = "https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/II2DB6"

# Column groups that have support/oppose pairs
# Each: (topic, base_column_prefix, question_wording)
ISSUE_PAIRS = [
    ("abortion", "abortion_20weeks", "Ban abortion after 20 weeks"),
    ("abortion", "abortion_always", "Abortion should be always available"),
    ("abortion", "abortion_conditional", "Abortion should be conditional/limited"),
    ("abortion", "abortion_coverage", "Government insurance should cover abortion"),
    ("abortion", "abortion_expenditures", "Government should fund abortion expenditures"),
    ("abortion", "abortion_prohibition", "Constitutional amendment to prohibit abortion"),
    ("affirmative_action", "affirmativeaction_scale", "Support for affirmative action programs"),
    ("environment", "enviro_airwateracts", "Support stricter air and water quality laws"),
    ("environment", "enviro_carbon", "Support limits on carbon emissions"),
    ("environment", "enviro_mpg_raise", "Support raising fuel efficiency standards"),
    ("environment", "enviro_renewable", "Support requiring renewable energy"),
    ("gay_marriage", "gaymarriage_ban", "Constitutional amendment banning gay marriage"),
    ("gay_marriage", "gaymarriage_legalize", "Support legalizing gay marriage"),
    ("guns", "guns_assaultban", "Ban assault weapons"),
    ("guns", "guns_bgchecks", "Require background checks for gun purchases"),
    ("guns", "guns_names", "Keep gun ownership public record/names"),
    ("guns", "guns_permits", "Require permit for gun purchase"),
    ("healthcare", "healthcare_aca", "Support the Affordable Care Act"),
    ("healthcare", "healthcare_acamandate", "Support ACA individual mandate"),
    ("healthcare", "healthcare_medicare", "Support government health insurance/Medicare for All"),
    ("healthcare", "healthcare_medicareage", "Support lowering Medicare eligibility age"),
    ("immigration", "immig_border", "Increase border security"),
    ("immigration", "immig_deport", "Deport undocumented immigrants"),
    ("immigration", "immig_employer", "Penalize employers hiring undocumented workers"),
    ("immigration", "immig_legalize", "Legalize undocumented immigrants"),
    ("immigration", "immig_police", "Allow police to question immigration status"),
    ("immigration", "immig_reduce", "Reduce legal immigration levels"),
    ("immigration", "immig_report", "Require reporting of undocumented immigrants"),
    ("immigration", "immig_services", "Deny social services to undocumented immigrants"),
    ("immigration", "immig_wall", "Build a border wall with Mexico"),
    ("foreign_policy", "military_democracy", "Use military to promote democracy abroad"),
    ("foreign_policy", "military_genocide", "Use military to stop genocide"),
    ("foreign_policy", "military_helpun", "Use military to help UN peacekeeping"),
    ("foreign_policy", "military_oil", "Use military to secure oil supplies"),
    ("foreign_policy", "military_protectallies", "Use military to protect allies"),
    ("foreign_policy", "military_terroristcamp", "Use military against terrorist camps"),
    ("trade", "trade_canmex_except", "Support trade with Canada/Mexico except for certain goods"),
    ("trade", "trade_canmex_include", "Support trade including all goods with Canada/Mexico"),
    ("trade", "trade_china", "Support free trade with China"),
]

# Single pct_* columns (standalone values, no oppose pair)
# Each: (topic, col_name, question_wording, question_type, issue_area)
SINGLE_ISSUES = [
    ("approval", "pct_approve_pres", "Approve of president's job performance", "approval", "presidential_approval"),
    ("approval", "pct_disapprove_pres", "Disapprove of president's job performance", "approval", "presidential_approval"),
    ("approval", "pct_somewhat_approve_pres", "Somewhat approve of president's job performance", "approval", "presidential_approval"),
    ("approval", "pct_somewhat_disapprove_pres", "Somewhat disapprove of president's job performance", "approval", "presidential_approval"),
    ("approval", "pct_strongly_approve_pres", "Strongly approve of president's job performance", "approval", "presidential_approval"),
    ("approval", "pct_strongly_disapprove_pres", "Strongly disapprove of president's job performance", "approval", "presidential_approval"),
    ("economy", "pct_economy_better", "Economy is better than last year", "priority", "economy_general"),
    ("economy", "pct_economy_worse", "Economy is worse than last year", "priority", "economy_general"),
    ("economy", "pct_economy_much_better", "Economy is much better than last year", "priority", "economy_general"),
    ("economy", "pct_economy_much_worse", "Economy is much worse than last year", "priority", "economy_general"),
    ("economy", "pct_economy_same", "Economy is about the same as last year", "priority", "economy_general"),
]


def parse_float(val):
    """Try to parse a string as float. Return None if not possible."""
    if val is None:
        return None
    val = val.strip()
    if not val:
        return None
    try:
        return float(val)
    except (ValueError, TypeError):
        return None


def safe_int(val):
    """Try to parse as int. Return None if not possible."""
    if val is None:
        return None
    val = val.strip()
    if not val:
        return None
    try:
        return int(float(val))
    except (ValueError, TypeError):
        return None


def build_index_map(headers):
    """Build a mapping from column name to column index."""
    return {h.strip(): i for i, h in enumerate(headers)}


def main():
    # Read the CSV
    with open(INPUT, 'r', newline='') as f:
        reader = csv.reader(f)
        all_rows = list(reader)
    
    if not all_rows:
        print("ERROR: Empty CSV file")
        sys.exit(1)
    
    headers = [h.strip() for h in all_rows[0]]
    print(f"Total columns: {len(headers)}")
    
    idx = build_index_map(headers)
    
    # Get indices of key columns
    year_idx = idx.get('year')
    n_respondents_idx = idx.get('n_respondents')
    
    if year_idx is None or n_respondents_idx is None:
        print("ERROR: Missing required columns 'year' and 'n_respondents'")
        sys.exit(1)
    
    rows_out = []
    
    for data_row in all_rows[1:]:
        if len(data_row) < len(headers):
            # Pad short rows
            data_row = data_row + [''] * (len(headers) - len(data_row))
        
        year_val = data_row[year_idx].strip()
        n_resp = safe_int(data_row[n_respondents_idx]) or 0
        
        # Process support/oppose pairs
        for topic, base_col, question_wording in ISSUE_PAIRS:
            support_col = f"{base_col}_pct_support"
            oppose_col = f"{base_col}_pct_oppose"
            n_col = f"{base_col}_n"
            
            s_idx = idx.get(support_col)
            o_idx = idx.get(oppose_col)
            n_idx = idx.get(n_col)
            
            if s_idx is None and o_idx is None:
                continue
            
            support_val = parse_float(data_row[s_idx]) if s_idx is not None else None
            oppose_val = parse_float(data_row[o_idx]) if o_idx is not None else None
            
            if support_val is None and oppose_val is None:
                continue
            
            # Get question-specific sample size or fallback
            sample_size = n_resp
            if n_idx is not None:
                ns = safe_int(data_row[n_idx])
                if ns is not None and ns > 0:
                    sample_size = ns
            
            # Calculate net
            net = None
            if support_val is not None and oppose_val is not None:
                net = round(support_val - oppose_val, 1)
            
            poll_id = f"CES_{year_val}_{base_col}"
            tags = f"ces;{year_val};{topic}"
            notes = f"CES variable: {base_col}. US adults 18+."
            
            rows_out.append({
                "poll_id": poll_id,
                "source": "CES (Cooperative Election Study)",
                "source_url": SOURCE_URL,
                "date": year_val,
                "question_type": "favor",
                "question_wording": question_wording,
                "topic": topic,
                "issue_area": "",
                "support_pct": support_val,
                "oppose_pct": oppose_val,
                "net": net,
                "sample_size": sample_size,
                "methodology": "online_panel",
                "population": "US adults",
                "moe": "",
                "tags": tags,
                "notes": notes,
            })
        
        # Process single pct columns
        for topic, col_name, question_wording, qtype, issue_area in SINGLE_ISSUES:
            c_idx = idx.get(col_name)
            if c_idx is None:
                continue
            
            val = parse_float(data_row[c_idx])
            if val is None:
                continue
            
            short_name = col_name.replace('pct_', '')
            poll_id = f"CES_{year_val}_{short_name}"
            tags = f"ces;{year_val};{topic}"
            notes = f"CES variable: {col_name}. US adults 18+."
            
            rows_out.append({
                "poll_id": poll_id,
                "source": "CES (Cooperative Election Study)",
                "source_url": SOURCE_URL,
                "date": year_val,
                "question_type": qtype,
                "question_wording": question_wording,
                "topic": topic,
                "issue_area": issue_area,
                "support_pct": val,
                "oppose_pct": None,
                "net": None,
                "sample_size": n_resp,
                "methodology": "online_panel",
                "population": "US adults",
                "moe": "",
                "tags": tags,
                "notes": notes,
            })
    
    if not rows_out:
        print("ERROR: No rows generated!")
        sys.exit(1)
    
    # Sort by date, then topic, then poll_id
    rows_out.sort(key=lambda r: (r['date'], r['topic'], r['poll_id']))
    
    # Write output
    fieldnames = [
        "poll_id", "source", "source_url", "date", "question_type",
        "question_wording", "topic", "issue_area", "support_pct", "oppose_pct",
        "net", "sample_size", "methodology", "population", "moe", "tags", "notes"
    ]
    
    with open(OUTPUT, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows_out)
    
    # Compute some stats
    topics_covered = sorted(set(r['topic'] for r in rows_out))
    years_covered = sorted(set(r['date'] for r in rows_out))
    
    print(f"\nCreated {len(rows_out)} rows in {OUTPUT}")
    print(f"Topics covered ({len(topics_covered)}): {topics_covered}")
    print(f"Years covered ({len(years_covered)}): {years_covered}")
    print(f"\nFirst 5 rows:")
    for r in rows_out[:5]:
        print(f"  {r['poll_id']}: topic={r['topic']}, support={r['support_pct']}, oppose={r['oppose_pct']}")
    print(f"\nLast 5 rows:")
    for r in rows_out[-5:]:
        print(f"  {r['poll_id']}: topic={r['topic']}, support={r['support_pct']}, oppose={r['oppose_pct']}")


if __name__ == "__main__":
    main()
