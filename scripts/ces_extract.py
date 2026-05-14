#!/usr/bin/env python3
"""
Extract issue polling data from CES Common Content + Policy Preferences datasets.
Aggregates by year to create issue polling rows.
Output: data/processed/ces_extracted.csv
"""

import pandas as pd
import numpy as np
import pyreadstat
import os
import warnings
warnings.filterwarnings('ignore')

WORKDIR = '/home/agentbot/workspace/us-political-messaging-dataset'
COMMON_CONTENT = os.path.join(WORKDIR, 'data/raw/ces/cumulative_2006-2024.dta')
POLICY_PREFS = os.path.join(WORKDIR, 'data/raw/ces/cumulative_ces_policy_preferences.tab')
OUTPUT = os.path.join(WORKDIR, 'data/processed/ces_extracted.csv')

print("=" * 60)
print("CES Issue Polling Data Extraction")
print("=" * 60)

# ============================================================
# STEP 1: Read Common Content (selectively)
# ============================================================
print("\n[1/4] Reading Common Content (cumulative_2006-2024.dta)...")

# Columns we need from Common Content
cc_cols = ['year', 'case_id', 'weight', 'weight_cumulative',
           'approval_pres', 'approval_rep', 'approval_sen1', 'approval_sen2', 'approval_gov',
           'economy_retro', 'pid3', 'pid7', 'ideo5',
           'gender', 'race', 'educ', 'faminc', 'age', 'hispanic',
           'religion', 'newsint']

# Read with pyreadstat - use row_limit=0 for all rows, only select needed columns
df_cc, meta_cc = pyreadstat.read_dta(
    COMMON_CONTENT,
    encoding='latin1',
    usecols=cc_cols,
    row_limit=0
)

print(f"  Read {len(df_cc):,} rows with {len(df_cc.columns)} columns")
print(f"  Years: {sorted(df_cc['year'].unique())}")
print(f"  Memory: {df_cc.memory_usage(deep=True).sum() / 1e6:.1f} MB")

# ============================================================
# STEP 2: Read Policy Preferences
# ============================================================
print("\n[2/4] Reading Policy Preferences (cumulative_ces_policy_preferences.tab)...")

# Read in chunks to manage memory
chunks = []
for chunk in pd.read_csv(POLICY_PREFS, sep='\t', chunksize=100000):
    chunks.append(chunk)
df_policy = pd.concat(chunks, ignore_index=True)

policy_vars = [c for c in df_policy.columns if c not in ['year', 'case_id']]
print(f"  Read {len(df_policy):,} rows with {len(policy_vars)} policy variables")

# ============================================================
# STEP 3: Merge datasets on year and case_id (INNER JOIN)
# ============================================================
print("\n[3/4] Merging Common Content with Policy Preferences...")

# Ensure consistent types for merge
df_cc['year'] = df_cc['year'].astype(int)
df_cc['case_id'] = df_cc['case_id'].astype(int)
df_policy['year'] = df_policy['year'].astype(int)
df_policy['case_id'] = df_policy['case_id'].astype(int)

# Inner join
df_merged = df_cc.merge(df_policy, on=['year', 'case_id'], how='inner')
print(f"  Merged dataset: {len(df_merged):,} rows")

# ============================================================
# STEP 4: Calculate issue polling rows by year
# ============================================================
print("\n[4/4] Aggregating by year to create issue polling rows...")

results = []

years = sorted(df_merged['year'].unique())

for year in years:
    yr_data = df_merged[df_merged['year'] == year]
    n_total = len(yr_data)
    
    row = {
        'year': int(year),
        'n_respondents': n_total,
        'source': 'CES',
        'survey': 'Cooperative Election Study (CES) Common Content'
    }
    
    # ---- Demographics ----
    for dem_col, dem_name in [('gender', 'male'), ('race', 'white'), ('race', 'black'),
                               ('race', 'hispanic'), ('race', 'asian'),
                               ('educ', 'college_grad'), ('hispanic', 'hispanic_origin')]:
        pass  # Will handle below
    
    # Gender: % male
    male_pct = (yr_data['gender'] == 1).sum() / n_total * 100 if 'gender' in yr_data else np.nan
    row['pct_male'] = round(male_pct, 1) if not pd.isna(male_pct) else np.nan
    
    # Race categories
    if 'race' in yr_data:
        white = (yr_data['race'] == 1).sum()
        black = (yr_data['race'] == 2).sum()
        hisp = (yr_data['race'] == 3).sum()
        asian = (yr_data['race'] == 4).sum()
        total_race = white + black + hisp + asian
        row['pct_white'] = round(white / n_total * 100, 1) if n_total > 0 else np.nan
        row['pct_black'] = round(black / n_total * 100, 1) if n_total > 0 else np.nan
        row['pct_hispanic_race'] = round(hisp / n_total * 100, 1) if n_total > 0 else np.nan
        row['pct_asian'] = round(asian / n_total * 100, 1) if n_total > 0 else np.nan
    
    # Hispanic origin
    if 'hispanic' in yr_data:
        hisp_orig = (yr_data['hispanic'] == 1).sum()
        row['pct_hispanic_origin'] = round(hisp_orig / n_total * 100, 1) if n_total > 0 else np.nan
    
    # Education: college grad+ (4-Year or Post-Grad)
    if 'educ' in yr_data:
        college = ((yr_data['educ'] == 5) | (yr_data['educ'] == 6)).sum()
        row['pct_college_grad'] = round(college / n_total * 100, 1) if n_total > 0 else np.nan
    
    # ---- Party Identification ----
    if 'pid3' in yr_data:
        valid_pid = yr_data['pid3'].isin([1, 2, 3])
        if valid_pid.any():
            dem = (yr_data['pid3'] == 1).sum()
            rep = (yr_data['pid3'] == 2).sum()
            ind = (yr_data['pid3'] == 3).sum()
            total_pid = dem + rep + ind
            row['pct_democrat'] = round(dem / total_pid * 100, 1)
            row['pct_republican'] = round(rep / total_pid * 100, 1)
            row['pct_independent'] = round(ind / total_pid * 100, 1)
    
    # 7-point party ID
    if 'pid7' in yr_data:
        valid_pid7 = yr_data['pid7'].isin(range(1, 8))
        if valid_pid7.any():
            d_strong = (yr_data['pid7'] == 1).sum()
            d_notstrong = (yr_data['pid7'] == 2).sum()
            d_lean = (yr_data['pid7'] == 3).sum()
            ind = (yr_data['pid7'] == 4).sum()
            r_lean = (yr_data['pid7'] == 5).sum()
            r_notstrong = (yr_data['pid7'] == 6).sum()
            r_strong = (yr_data['pid7'] == 7).sum()
            total_pid7 = d_strong + d_notstrong + d_lean + ind + r_lean + r_notstrong + r_strong
            row['pct_strong_dem'] = round(d_strong / total_pid7 * 100, 1)
            row['pct_lean_dem'] = round((d_notstrong + d_lean) / total_pid7 * 100, 1)
            row['pct_pure_ind'] = round(ind / total_pid7 * 100, 1)
            row['pct_lean_rep'] = round((r_lean + r_notstrong) / total_pid7 * 100, 1)
            row['pct_strong_rep'] = round(r_strong / total_pid7 * 100, 1)
    
    # ---- Ideology ----
    if 'ideo5' in yr_data:
        valid_ideo = yr_data['ideo5'].isin(range(1, 6))
        if valid_ideo.any():
            liberal = (yr_data['ideo5'].isin([1, 2])).sum()
            moderate = (yr_data['ideo5'] == 3).sum()
            conservative = (yr_data['ideo5'].isin([4, 5])).sum()
            total_ideo = liberal + moderate + conservative
            row['pct_liberal'] = round(liberal / total_ideo * 100, 1)
            row['pct_moderate'] = round(moderate / total_ideo * 100, 1)
            row['pct_conservative'] = round(conservative / total_ideo * 100, 1)
            row['mean_ideo5'] = round(yr_data.loc[valid_ideo, 'ideo5'].mean(), 2)
    
    # ---- Presidential Approval ----
    if 'approval_pres' in yr_data:
        valid_ap = yr_data['approval_pres'].isin([1, 2, 3, 4])
        if valid_ap.any():
            approve = (yr_data['approval_pres'].isin([1, 2])).sum()
            disapprove = (yr_data['approval_pres'].isin([3, 4])).sum()
            strongly_approve = (yr_data['approval_pres'] == 1).sum()
            somewhat_approve = (yr_data['approval_pres'] == 2).sum()
            somewhat_disapprove = (yr_data['approval_pres'] == 3).sum()
            strongly_disapprove = (yr_data['approval_pres'] == 4).sum()
            total_ap = approve + disapprove
            row['pct_approve_pres'] = round(approve / total_ap * 100, 1) if total_ap > 0 else np.nan
            row['pct_disapprove_pres'] = round(disapprove / total_ap * 100, 1) if total_ap > 0 else np.nan
            row['pct_strongly_approve_pres'] = round(strongly_approve / total_ap * 100, 1) if total_ap > 0 else np.nan
            row['pct_somewhat_approve_pres'] = round(somewhat_approve / total_ap * 100, 1) if total_ap > 0 else np.nan
            row['pct_somewhat_disapprove_pres'] = round(somewhat_disapprove / total_ap * 100, 1) if total_ap > 0 else np.nan
            row['pct_strongly_disapprove_pres'] = round(strongly_disapprove / total_ap * 100, 1) if total_ap > 0 else np.nan
    
    # ---- Congressional Approval ----
    if 'approval_rep' in yr_data:
        valid_ar = yr_data['approval_rep'].isin([1, 2, 3, 4])
        if valid_ar.any():
            approve_rep = (yr_data['approval_rep'].isin([1, 2])).sum()
            disapprove_rep = (yr_data['approval_rep'].isin([3, 4])).sum()
            total_ar = approve_rep + disapprove_rep
            row['pct_approve_rep'] = round(approve_rep / total_ar * 100, 1) if total_ar > 0 else np.nan
            row['pct_disapprove_rep'] = round(disapprove_rep / total_ar * 100, 1) if total_ar > 0 else np.nan
    
    # ---- Economic Retrospective ----
    if 'economy_retro' in yr_data:
        valid_er = yr_data['economy_retro'].isin([1, 2, 3, 4, 5])
        if valid_er.any():
            much_better = (yr_data['economy_retro'] == 1).sum()
            somewhat_better = (yr_data['economy_retro'] == 2).sum()
            same = (yr_data['economy_retro'] == 3).sum()
            somewhat_worse = (yr_data['economy_retro'] == 4).sum()
            much_worse = (yr_data['economy_retro'] == 5).sum()
            total_er = much_better + somewhat_better + same + somewhat_worse + much_worse
            row['pct_economy_better'] = round((much_better + somewhat_better) / total_er * 100, 1) if total_er > 0 else np.nan
            row['pct_economy_same'] = round(same / total_er * 100, 1) if total_er > 0 else np.nan
            row['pct_economy_worse'] = round((somewhat_worse + much_worse) / total_er * 100, 1) if total_er > 0 else np.nan
            row['pct_economy_much_better'] = round(much_better / total_er * 100, 1) if total_er > 0 else np.nan
            row['pct_economy_much_worse'] = round(much_worse / total_er * 100, 1) if total_er > 0 else np.nan
    
    # ---- POLICY PREFERENCES ----
    # For each policy variable, calculate Support % (where 1=Support/Favor)
    for pv in policy_vars:
        if pv in yr_data:
            # Drop NaN for this variable in this year
            valid = yr_data[pv].notna()
            n_valid = valid.sum()
            
            if n_valid > 0:
                vals = yr_data.loc[valid, pv]
                
                # Determine variable type based on unique values
                unique_vals = sorted(vals.unique())
                
                # Binary variables (1=Support, 2=Oppose)
                if set(unique_vals).issubset({1.0, 2.0}):
                    support = (vals == 1.0).sum()
                    oppose = (vals == 2.0).sum()
                    total_so = support + oppose
                    if total_so > 0:
                        row[f'{pv}_pct_support'] = round(support / total_so * 100, 1)
                        row[f'{pv}_pct_oppose'] = round(oppose / total_so * 100, 1)
                        row[f'{pv}_n'] = n_valid
                
                # 4-point scale (abortion_scale)
                elif pv == 'abortion_scale' and set(unique_vals).issubset({1.0, 2.0, 3.0, 4.0}):
                    never = (vals == 1.0).sum()
                    rape_incest = (vals == 2.0).sum()
                    other_cases = (vals == 3.0).sum()
                    always = (vals == 4.0).sum()
                    total_ascale = never + rape_incest + other_cases + always
                    row[f'{pv}_pct_never_permit'] = round(never / total_ascale * 100, 1)
                    row[f'{pv}_pct_rape_incest'] = round(rape_incest / total_ascale * 100, 1)
                    row[f'{pv}_pct_other_cases'] = round(other_cases / total_ascale * 100, 1)
                    row[f'{pv}_pct_always_allow'] = round(always / total_ascale * 100, 1)
                    row[f'{pv}_mean'] = round(vals.mean(), 2)
                    row[f'{pv}_n'] = n_valid
                
                # 5-point scale (enviro_scale, gaymarriage_scale)
                elif pv in ['enviro_scale', 'gaymarriage_scale'] and max(unique_vals) <= 5:
                    for val in range(1, 6):
                        cnt = (vals == val).sum()
                        row[f'{pv}_pct_{int(val)}'] = round(cnt / n_valid * 100, 1)
                    row[f'{pv}_mean'] = round(vals.mean(), 2)
                    row[f'{pv}_n'] = n_valid
                
                # 3-point scale (guns_scale)
                elif pv == 'guns_scale':
                    for val in range(1, 4):
                        cnt = (vals == val).sum()
                        row[f'{pv}_pct_{int(val)}'] = round(cnt / n_valid * 100, 1)
                    row[f'{pv}_mean'] = round(vals.mean(), 2)
                    row[f'{pv}_n'] = n_valid
                
                # affirmativeaction (1-4 scale: support-oppose)
                elif pv == 'affirmativeaction' and set(unique_vals).issubset({1.0, 2.0, 3.0, 4.0}):
                    strongly_support = (vals == 1.0).sum()
                    somewhat_support = (vals == 2.0).sum()
                    somewhat_oppose = (vals == 3.0).sum()
                    strongly_oppose = (vals == 4.0).sum()
                    total_aa = strongly_support + somewhat_support + somewhat_oppose + strongly_oppose
                    row[f'{pv}_pct_strongly_support'] = round(strongly_support / total_aa * 100, 1)
                    row[f'{pv}_pct_somewhat_support'] = round(somewhat_support / total_aa * 100, 1)
                    row[f'{pv}_pct_somewhat_oppose'] = round(somewhat_oppose / total_aa * 100, 1)
                    row[f'{pv}_pct_strongly_oppose'] = round(strongly_oppose / total_aa * 100, 1)
                    row[f'{pv}_mean'] = round(vals.mean(), 2)
                    row[f'{pv}_n'] = n_valid
                
                # affirmativeaction_scale (1-7 scale)
                elif pv == 'affirmativeaction_scale':
                    row[f'{pv}_mean'] = round(vals.mean(), 2)
                    row[f'{pv}_n'] = n_valid
                    # Also record support (1-3) vs oppose (5-7)
                    support_aa = (vals.isin([1.0, 2.0, 3.0])).sum()
                    oppose_aa = (vals.isin([5.0, 6.0, 7.0])).sum()
                    mid_aa = (vals == 4.0).sum()
                    total_aas = support_aa + oppose_aa + mid_aa
                    if total_aas > 0:
                        row[f'{pv}_pct_support'] = round(support_aa / total_aas * 100, 1)
                        row[f'{pv}_pct_mid'] = round(mid_aa / total_aas * 100, 1)
                        row[f'{pv}_pct_oppose'] = round(oppose_aa / total_aas * 100, 1)
                
                # spending_cuts (1-4 categorical)
                elif pv in ['spending_cuts_most', 'spending_cuts_least']:
                    for val in range(1, 5):
                        cnt = (vals == val).sum()
                        row[f'{pv}_pct_{int(val)}'] = round(cnt / n_valid * 100, 1)
                    row[f'{pv}_n'] = n_valid
                
                # Slider variables (0-100): incometax_vs_salestax, spending_vs_tax
                elif pv in ['incometax_vs_salestax', 'spending_vs_tax']:
                    # Filter out special codes (>100 or weird values)
                    clean_vals = vals[(vals >= 0) & (vals <= 100)]
                    if len(clean_vals) > 0:
                        row[f'{pv}_mean'] = round(clean_vals.mean(), 1)
                        row[f'{pv}_median'] = round(clean_vals.median(), 1)
                        row[f'{pv}_n'] = len(clean_vals)
                
                # enviro_vs_jobs (1-6 scale)
                elif pv == 'enviro_vs_jobs':
                    for val in range(1, 7):
                        cnt = (vals == val).sum()
                        row[f'{pv}_pct_{int(val)}'] = round(cnt / n_valid * 100, 1)
                    row[f'{pv}_mean'] = round(vals.mean(), 2)
                    row[f'{pv}_n'] = n_valid
                
                # Binary with additional categories (gaymarriage_ban)
                elif pv in ['gaymarriage_ban', 'gaymarriage_legalize'] and set(unique_vals).issubset({1.0, 2.0}):
                    support = (vals == 1.0).sum()
                    oppose = (vals == 2.0).sum()
                    total_so = support + oppose
                    if total_so > 0:
                        row[f'{pv}_pct_support'] = round(support / total_so * 100, 1)
                        row[f'{pv}_pct_oppose'] = round(oppose / total_so * 100, 1)
                        row[f'{pv}_n'] = n_valid
                
                # Generic fallback for any other variable types
                else:
                    # Record as mean + distribution
                    row[f'{pv}_mean'] = round(vals.mean(), 2)
                    row[f'{pv}_n'] = n_valid
                    # Record top value categories
                    top_vals = vals.value_counts().head(5)
                    for val, cnt in top_vals.items():
                        row[f'{pv}_val_{int(val)}'] = round(cnt / n_valid * 100, 1)
    
    results.append(row)
    
    if (year - years[0]) % 2 == 0 or year == years[-1]:
        print(f"  Processed {year} ({n_total:,} respondents)")

# ============================================================
# Create final DataFrame and save
# ============================================================
df_out = pd.DataFrame(results)

# Sort columns logically
col_order = ['year', 'n_respondents', 'source', 'survey']
# Demographics
dem_cols = [c for c in df_out.columns if c.startswith('pct_') and any(d in c for d in ['male', 'white', 'black', 'hispanic', 'asian', 'college'])]
# Party/ideology
pid_cols = [c for c in df_out.columns if c.startswith('pct_dem') or c.startswith('pct_rep') or c.startswith('pct_ind') or 
            c.startswith('pct_strong_dem') or c.startswith('pct_lean_dem') or c.startswith('pct_pure') or
            c.startswith('pct_lean_rep') or c.startswith('pct_strong_rep') or
            c.startswith('pct_liberal') or c.startswith('pct_moderate') or c.startswith('pct_conservative') or
            c.startswith('mean_ideo')]
# Approval
approval_cols = [c for c in df_out.columns if 'approve' in c or 'disapprove' in c]
# Economy
econ_cols = [c for c in df_out.columns if c.startswith('pct_economy')]
# Policy vars (everything else)
policy_cols = [c for c in df_out.columns if c not in col_order + dem_cols + pid_cols + approval_cols + econ_cols]

ordered = col_order + sorted(dem_cols) + sorted(pid_cols) + sorted(approval_cols) + sorted(econ_cols) + sorted(policy_cols)
df_out = df_out[ordered]

# Save
os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
df_out.to_csv(OUTPUT, index=False)

print(f"\n{'=' * 60}")
print(f"EXTRACTION COMPLETE")
print(f"{'=' * 60}")
print(f"Output: {OUTPUT}")
print(f"Years: {df_out['year'].min()} - {df_out['year'].max()}")
print(f"Rows: {len(df_out)}")
print(f"Columns: {len(df_out.columns)}")
print(f"\nColumn summary:")
for c in df_out.columns:
    print(f"  {c}")
