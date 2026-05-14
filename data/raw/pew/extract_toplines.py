#!/usr/bin/env python3
"""
Pew Research PDF topline extractor - v2
More robust parsing using line-by-line state machine.
"""

import fitz
import re
import csv
import os

PDF_DIR = "/home/agentbot/workspace/us-political-messaging-dataset/data/raw/pew"
OUTPUT_CSV = os.path.join(PDF_DIR, "pew_toplines_extracted.csv")

PDF_META = {
    "2011_typology_topline.pdf": {
        "source_url": "http://assets.pewresearch.org/wp-content/uploads/sites/5/2011/05/Political-Typology-Topline.pdf",
        "date": "2011-03-01",
        "sample_size": 3029,
        "methodology": "phone",
        "population": "adults",
        "tags": "political_typology;2011",
    },
    "2014_polarization_topline.pdf": {
        "source_url": "https://assets.pewresearch.org/wp-content/uploads/sites/5/2014/06/2014-Polarization-Topline-for-Release.pdf",
        "date": "2014-02-26",
        "sample_size": 10013,
        "methodology": "phone",
        "population": "adults",
        "tags": "political_polarization;typology;2014",
    },
    "2017_typology_topline.pdf": {
        "source_url": "https://www.people-press.org/wp-content/uploads/sites/4/2017/10/10-24-2017-typology-toplines-for-release.pdf",
        "date": "2017-07-09",
        "sample_size": 5009,
        "methodology": "phone",
        "population": "adults",
        "tags": "political_typology;2017",
    },
    "2021_typology_topline.pdf": {
        "source_url": "https://www.pewresearch.org/wp-content/uploads/sites/20/2021/11/PP_2021.11.09_political-typology_TOPLINE.pdf",
        "date": "2021-06-27",
        "sample_size": 10606,
        "methodology": "online_panel",
        "population": "adults",
        "tags": "political_typology;2021",
    },
    "2014_typology_appendix_topline.pdf": {
        "source_url": "https://assets.pewresearch.org/wp-content/uploads/sites/5/2014/06/APPENDIX-4-Typology-Topline-for-Release.pdf",
        "date": "2014-03-01",
        "sample_size": 10013,
        "methodology": "phone",
        "population": "adults",
        "tags": "political_typology;appendix;2014",
    },
}


def extract_all_text(pdf_path):
    doc = fitz.open(pdf_path)
    full_text = ""
    for page in doc:
        full_text += page.get_text() + "\n"
    doc.close()
    return full_text


MONTH_NAMES = r'(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)'
DATE_LINE_RE = re.compile(
    MONTH_NAMES + r'\s+\d+[-\u2013]' + MONTH_NAMES + r'?\s*\d*,?\s+\d{4}'
)

# Lines that indicate we're NOT in question wording anymore
TABLE_INDICATORS = [
    re.compile(r'^(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d+'),
    re.compile(r'^\s*Approv'),
    re.compile(r'^\s*Disapp'),
    re.compile(r'^\s*Favor'),
    re.compile(r'^\s*Unfav'),
    re.compile(r'^\s*Satis'),
    re.compile(r'^\s*Dis\s*$'),
    re.compile(r'^\s*\(VOL\.\)'),
    re.compile(r'^\s*Total\s'),
    re.compile(r'^\s*Very\s'),
    re.compile(r'^\s*Mostly\s'),
    re.compile(r'^\s*Never\s'),
    re.compile(r'^\s*----'),
    re.compile(r'^\s*DK/Ref'),
    re.compile(r'^\s*Can\'t'),
    re.compile(r'^\s*Net\s'),
    re.compile(r'^\s*Strongly'),
    re.compile(r'^\s*Not so'),
    re.compile(r'^\s*Some\s'),
    re.compile(r'^\s*Not\s'),
    re.compile(r'^\s*Hardly'),
    re.compile(r'^\s*Protect'),
    re.compile(r'^\s*Control'),
    re.compile(r'^\s*Other\s'),
]


def is_table_line(line):
    """Check if a line is likely part of the results table rather than question wording."""
    stripped = line.strip()
    if not stripped:
        return False
    for pattern in TABLE_INDICATORS:
        if pattern.match(stripped):
            return True
    # Check if it starts with a percentage-like number followed by answer text
    if re.match(r'^\s*\d{1,3}\s', stripped):
        return True
    # Check if it's a survey date pattern
    if DATE_LINE_RE.match(stripped):
        return True
    return False


def clean_wording(text):
    """Clean up question wording."""
    text = re.sub(r'\s+', ' ', text).strip()
    # Remove interviewer instructions in brackets
    text = re.sub(r'\[(INTERVIEWERS?|IF NECESSARY|READ|DO NOT|PROBE).*?\]', '', text, flags=re.DOTALL)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def parse_phone_survey(text, pdf_name):
    """
    Parse phone survey topline format used in 2011, 2014, 2017.
    
    Structure:
    - Lines starting with "ASK ALL" or "ASK IF" start a question block
    - Question code on "Q.X" line
    - Question wording follows until table data begins
    - Table data has date lines and percentage values
    """
    lines = text.split('\n')
    
    # First, identify all question block boundaries
    question_starts = []
    for i, line in enumerate(lines):
        stripped = line.strip()
        if re.match(r'^ASK\s+(ALL|IF)', stripped, re.IGNORECASE):
            question_starts.append(i)
        elif re.match(r'^Q\.\s*[A-Z0-9]', stripped) and i > 0:
            # Check if previous line is empty or ASK-related
            prev = lines[i-1].strip() if i > 0 else ""
            if not prev or re.match(r'^ASK\s+(ALL|IF)', prev, re.IGNORECASE):
                question_starts.append(i)
    
    # Also find "NO QUESTION" markers as boundaries
    no_question_starts = set()
    for i, line in enumerate(lines):
        if re.match(r'^NO QUESTION', line.strip()):
            no_question_starts.add(i)
    
    # Find "HELD FOR FUTURE" and "PREVIOUSLY RELEASED" as boundaries
    skip_starts = set()
    for i, line in enumerate(lines):
        if 'HELD FOR FUTURE RELEASE' in line or 'PREVIOUSLY RELEASED' in line:
            skip_starts.add(i)
    
    # Group lines into blocks
    # Each block starts at a question start and ends at the next question start (or end of file)
    
    results = []
    
    for idx, start in enumerate(question_starts):
        end = question_starts[idx + 1] if idx + 1 < len(question_starts) else len(lines)
        
        # Extract block content
        block_lines = []
        for j in range(start, end):
            l = lines[j]
            stripped = l.strip()
            # Skip empty lines, page numbers, headers
            if not stripped:
                continue
            if re.match(r'^\d+$', stripped) and len(stripped) < 5 and int(stripped) < 200:
                continue
            if stripped in ['www.pewresearch.org', 'www.people-press.org', 'PEW RESEARCH CENTER']:
                continue
            if 'PEW RESEARCH CENTER' in stripped and len(stripped) < 60:
                continue
            block_lines.append(stripped)
        
        if not block_lines:
            continue
        
        block_text = '\n'.join(block_lines)
        
        # Skip junk blocks
        first = block_lines[0]
        if re.match(r'^NO QUESTION', first):
            continue
        if 'HELD FOR FUTURE RELEASE' in block_text or 'PREVIOUSLY RELEASED' in block_text:
            continue
        if 'ADDITIONAL QUESTION' in first:
            continue
        if 'NOT CODED YET' in first:
            continue
        if 'RANDOMIZE' in first and len(first) < 30:
            continue
        
        # Parse the block to extract question id, wording, and data
        q_id = ""
        q_wording_parts = []
        table_data = []
        in_wording = True
        
        for bi, bline in enumerate(block_lines):
            # Check if this is a table line
            if in_wording:
                # Question ID
                if re.match(r'^Q\.', bline):
                    q_id = bline
                    continue
                if re.match(r'^ASK\s+(ALL|IF)', bline, re.IGNORECASE):
                    # Don't include this in wording
                    continue
                
                # Check for transition to table
                # A line that looks like a column header or data
                if is_table_line(bline) and len(q_wording_parts) > 1:
                    in_wording = False
                    table_data.append(bline)
                else:
                    q_wording_parts.append(bline)
            else:
                table_data.append(bline)
        
        # Also check: if wording is very short and table data doesn't look right,
        # try to find the real wording by looking at more lines
        q_wording = ' '.join(q_wording_parts)
        q_wording = clean_wording(q_wording)
        
        if not q_wording or len(q_wording) < 10:
            continue
        if len(q_wording) > 1500:
            q_wording = q_wording[:1500] + "..."
        
        # Extract percentages from table data
        support_pct, oppose_pct = extract_pct_phone(table_data, q_wording)
        
        if support_pct is None:
            # Try harder - scan the whole block
            support_pct, oppose_pct = extract_pct_scan(block_text, q_wording)
        
        if support_pct is not None:
            results.append({
                'q_id': q_id,
                'q_wording': q_wording,
                'support_pct': support_pct,
                'oppose_pct': oppose_pct,
                'net': support_pct - oppose_pct,
                'table_data': table_data,
            })
    
    return results


def extract_pct_phone(table_lines, q_wording):
    """Extract percentages from phone survey table data."""
    # Join table lines and look for the first date + numbers pattern
    text = ' '.join(table_lines)
    
    # Find numbers that follow a date pattern
    # Pattern: "Feb 22-Mar 1, 2011 51 39 10"
    date_num_pattern = re.compile(
        MONTH_NAMES + r'\s+\d+[-\u2013](?:\d+,?\s+)?' + MONTH_NAMES + r'?\s*\d*,?\s+\d{4}\s+(\d{1,3})'
    )
    matches = date_num_pattern.findall(text)
    
    if matches:
        # matches is a list of tuples due to MONTH_NAMES capturing group
        first_val = int(matches[0][-1]) if isinstance(matches[0], tuple) else int(matches[0])
        # Now find the second number after the first date
        first_date_match = re.search(
            MONTH_NAMES + r'\s+\d+[-\u2013](?:\d+,?\s+)?' + MONTH_NAMES + r'?\s*\d*,?\s+\d{4}',
            text
        )
        if first_date_match:
            after_date = text[first_date_match.end():]
            nums = re.findall(r'\b(\d{1,3})\b', after_date)
            nums = [int(n) for n in nums if int(n) <= 100]
            if len(nums) >= 2:
                return (nums[0], nums[1])
            elif len(nums) >= 1:
                return (first_val, nums[0])
    
    # Try simpler approach: find all numbers that appear after month-date patterns
    all_dates = re.finditer(
        MONTH_NAMES + r'\s+\d+[-\u2013](?:\d+,?\s+)?' + MONTH_NAMES + r'?\s*\d*,?\s+\d{4}',
        text
    )
    
    for date_match in all_dates:
        start = date_match.start()
        # Get the next ~50 chars
        snippet = text[start:start+80]
        nums = re.findall(r'\b(\d{1,3})\b', snippet)
        nums = [int(n) for n in nums if int(n) <= 100]
        if len(nums) >= 3:
            return (nums[0], nums[1])
    
    return (None, None)


def extract_pct_scan(block_text, q_wording):
    """Fallback: scan entire block for percentage data."""
    # Find a line with a date pattern followed by 2-3 numbers within 80 chars
    lines = block_text.split('\n')
    for line in lines:
        if DATE_LINE_RE.match(line.strip()):
            nums = re.findall(r'\b(\d{1,3})\b', line)
            nums = [int(n) for n in nums if int(n) <= 100]
            if len(nums) >= 3:
                return (nums[0], nums[1])
    
    # Look for any block of numbers near a date
    for i, line in enumerate(lines):
        if re.search(r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d+', line):
            # Check this line and next few for numbers
            all_nums = []
            for j in range(i, min(i + 10, len(lines))):
                nums = re.findall(r'\b(\d{1,3})\b', lines[j])
                for n in nums:
                    v = int(n)
                    if v <= 100:
                        all_nums.append(v)
            if len(all_nums) >= 2:
                return (all_nums[0], all_nums[1])
    
    return (None, None)


def parse_atp_survey(text, pdf_name):
    """Parse ATP format (2021)."""
    lines = text.split('\n')
    
    # Find all variable names (all caps, standalone)
    # Then figure out question blocks
    results = []
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Check for variable name
        if re.match(r'^[A-Z][A-Z_0-9]{3,20}$', line):
            var_name = line
            i += 1
            
            # Gather question wording and table
            q_wording_parts = []
            table_lines = []
            in_wording = True
            
            while i < len(lines):
                cur = lines[i].strip()
                
                # Stop conditions
                if not cur:
                    i += 1
                    continue
                
                # Check for next variable
                if re.match(r'^[A-Z][A-Z_0-9]{3,20}$', cur) and cur != var_name:
                    # But don't stop for NOTES, ASK ALL, etc
                    if not re.match(r'^(NOTE|ASK|ALL)', cur):
                        break
                
                # Stop for section markers
                if 'ADDITIONAL QUESTION' in cur or 'ADDITIONAL QUESTIONS' in cur:
                    break
                if re.match(r'^NO QUESTION', cur):
                    break
                
                if in_wording:
                    # Check transition to table
                    if re.match(r'^\d+\s', cur) and len(cur) < 15:
                        in_wording = False
                        table_lines.append(cur)
                        i += 1
                        continue
                    if DATE_LINE_RE.match(cur):
                        in_wording = False
                        table_lines.append(cur)
                        i += 1
                        continue
                    if re.match(r'^Rating of|^[A-Z][a-z]+\s+\d+-\d+', cur):
                        in_wording = False
                        i += 1
                        continue
                    
                    q_wording_parts.append(cur)
                    i += 1
                else:
                    table_lines.append(cur)
                    i += 1
            
            q_wording = ' '.join(q_wording_parts)
            q_wording = clean_wording(q_wording)
            
            if not q_wording or len(q_wording) < 10:
                continue
            if len(q_wording) > 1500:
                q_wording = q_wording[:1500] + "..."
            
            # Extract percentages
            support_pct, oppose_pct = extract_pct_atp(table_lines, q_wording)
            
            if support_pct is None:
                continue
            
            results.append({
                'q_id': var_name,
                'q_wording': q_wording,
                'support_pct': support_pct,
                'oppose_pct': oppose_pct,
                'net': support_pct - oppose_pct,
                'table_data': table_lines,
            })
        
        i += 1
    
    return results


def extract_pct_atp(table_lines, q_wording):
    """Extract percentages from ATP table data."""
    text = '\n'.join(table_lines)
    
    # Look for the first data row (current survey date)
    # Pattern: "Jun 14-27, 2021" followed by percentages
    for line in table_lines:
        if DATE_LINE_RE.match(line):
            nums = re.findall(r'\b(\d{1,3})\b', line)
            nums = [int(n) for n in nums if int(n) <= 100]
            if len(nums) >= 2:
                return (nums[0], nums[1])
    
    # Also look for "Jul 8-18, 2021" (wave 92)
    for line in table_lines:
        if re.search(r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d+', line):
            nums = re.findall(r'\b(\d{1,3})\b', line)
            nums = [int(n) for n in nums if int(n) <= 100]
            if len(nums) >= 2:
                return (nums[0], nums[1])
    
    # Also look for lines starting with numbers (percentage data)
    for line in table_lines:
        if re.match(r'^\d{1,3}\b', line.strip()):
            nums = re.findall(r'\b(\d{1,3})\b', line)
            nums = [int(n) for n in nums if int(n) <= 100]
            if len(nums) >= 2:
                return (nums[0], nums[1])
    
    return (None, None)


def classify_topic(qw):
    qt = qw.lower()
    if any(w in qt for w in ['economy', 'economic', 'jobs', 'unemployment', 'stock market', 'inflation', 'cost of living', 'financial', 'recession', 'budget deficit', 'national debt', 'economic issues']):
        return 'economy'
    if any(w in qt for w in ['health care', 'healthcare', 'medicare', 'medicaid', 'affordable care', 'obamacare', 'health insurance']):
        return 'healthcare'
    if any(w in qt for w in ['immigrant', 'immigration', 'border', 'undocumented', 'migrant', 'deport', 'legal immigrants', 'illegal']):
        return 'immigration'
    if any(w in qt for w in ['gun', 'firearm', 'second amendment', 'gun control', 'gun rights', 'gun ownership']):
        return 'gun_policy'
    if any(w in qt for w in ['climate', 'environment', 'global warming', 'clean energy', 'pollution', 'renewable', 'protect the environment']):
        return 'climate_environment'
    if any(w in qt for w in ['abortion', 'pro-choice', 'pro-life', 'roe', 'reproductive']):
        return 'abortion'
    if any(w in qt for w in ['racial', 'race', 'discrimination', 'black', 'equality', 'racism', 'diversity', 'ethnic']):
        return 'race_equality'
    if any(w in qt for w in ['foreign policy', 'defense', 'military', 'national security', 'terrorism', 'war', 'china', 'russia', 'ukraine', 'iran', 'isis', 'afghanistan', 'iraq', 'syria', 'nato', 'world affairs', 'foreign']):
        return 'foreign_policy'
    if any(w in qt for w in ['crime', 'criminal', 'policing', 'police', 'violence', 'safety', 'justice system', 'prison', 'convicted']):
        return 'crime_policing'
    if any(w in qt for w in ['education', 'school', 'student', 'college', 'university', 'student loans']):
        return 'education'
    if any(w in qt for w in ['tax', 'taxes', 'taxation']):
        return 'taxes'
    if any(w in qt for w in ['government', 'trust', 'regulation', 'role of government', 'government is', 'government should', 'government aid', 'welfare', 'social security', 'food stamps', 'unemployment benefits', 'poor', 'aid to']):
        return 'government_role'
    if any(w in qt for w in ['gay', 'lesbian', 'lgbt', 'same-sex', 'same sex', 'transgender', 'marriage equality', 'homosexual']):
        return 'lgbt_rights'
    if any(w in qt for w in ['religion', 'religious', 'church', 'bible', 'god', 'faith', 'christian', 'prayer', 'pray']):
        return 'religion'
    if any(w in qt for w in ['republican party', 'democratic party', 'feelings toward', 'thermometer', 'opinion of the republican', 'opinion of the democratic', 'republicans', 'democrats']):
        return 'political_parties'
    if any(w in qt for w in ['satisfied', 'satisfaction', 'things are going', 'right track', 'country today']):
        return 'general_outlook'
    if any(w in qt for w in ['approve', 'disapprove', 'handling his job', 'handling her job']):
        if any(w in qt for w in ['president', 'obama', 'trump', 'biden', 'george w. bush', 'clinton']):
            return 'presidential_approval'
        if any(w in qt for w in ['congress', 'supreme court']):
            return 'institutional_approval'
        return 'approval'
    if any(w in qt for w in ['values', 'moral', 'honesty', 'ethics', 'hard work', 'success', 'individual', 'responsibility', 'good and evil']):
        return 'values'
    if any(w in qt for w in ['media', 'news', 'press', 'journalist', 'newspaper', 'television news', 'social media', 'watch the national']):
        return 'media'
    if any(w in qt for w in ['most important', 'priority', 'biggest problem']):
        return 'priorities'
    if any(w in qt for w in ['compromise', 'selling out', 'politics today', 'voting']):
        return 'political_engagement'
    return 'general_politics'


def classify_issue_area(topic, qw):
    qt = qw.lower()
    if topic == 'economy':
        if any(w in qt for w in ['condition', 'state of', 'doing well', 'good shape', 'excellent', 'poor']):
            return 'economic_conditions'
        if any(w in qt for w in ['jobs', 'employment', 'unemployment']):
            return 'jobs'
        if any(w in qt for w in ['inflation', 'prices', 'cost of living', 'costs']):
            return 'inflation_costs'
        if any(w in qt for w in ['personal finance', 'financial situation', 'recession affected']):
            return 'personal_finances'
        if 'deficit' in qt or 'debt' in qt:
            return 'budget_deficit'
        return 'economy_general'
    if topic == 'healthcare':
        if 'cost' in qt:
            return 'cost'
        if any(w in qt for w in ['aca', 'obamacare', 'affordable care act']):
            return 'aca'
        if any(w in qt for w in ['single payer', 'health insurance']):
            return 'health_insurance'
        return 'healthcare_general'
    if topic == 'government_role':
        if any(w in qt for w in ['trust', 'confidence']):
            return 'trust_in_government'
        if any(w in qt for w in ['regulation', 'regulate']):
            return 'regulation'
        if any(w in qt for w in ['welfare', 'aid to poor', 'food stamps', 'poor people', 'poor do']):
            return 'social_safety_net'
        if any(w in qt for w in ['social security']):
            return 'social_security'
        if any(w in qt for w in ['wasteful', 'efficient', 'run the government']):
            return 'government_efficiency'
        if any(w in qt for w in ['too much', 'too powerful', 'doing too many', 'smaller government', 'bigger government']):
            return 'role_of_government'
        if any(w in qt for w in ['responsibility of the federal government']):
            return 'federal_responsibility'
        return 'government_general'
    if topic == 'political_parties':
        if 'thermometer' in qt or 'feelings toward' in qt:
            return 'party_affect'
        if any(w in qt for w in ['opinion of', 'view of', 'favorable', 'unfavorable']):
            return 'party_favorability'
        if 'difference' in qt:
            return 'party_differentiation'
        return 'parties_general'
    if topic == 'presidential_approval':
        return 'presidential_approval'
    if topic == 'general_outlook':
        return 'right_track_wrong_track'
    if topic == 'immigration':
        if 'legal' in qt:
            return 'legal_immigration'
        if 'illegal' in qt or 'undocumented' in qt:
            return 'illegal_immigration'
        return 'immigration_general'
    if topic == 'foreign_policy':
        if any(w in qt for w in ['china', 'russia', 'ukraine']):
            return 'great_power_relations'
        if any(w in qt for w in ['terrorism', 'isis']):
            return 'terrorism'
        if any(w in qt for w in ['iran', 'iraq', 'afghanistan']):
            return 'middle_east'
        return 'foreign_policy_general'
    if topic == 'values':
        if 'good' in qt and 'evil' in qt:
            return 'moral_absolutes'
        return 'political_values'
    if topic == 'lgbt_rights':
        if 'same-sex' in qt or 'same sex' in qt or 'gay' in qt:
            return 'same_sex_marriage'
        if 'transgender' in qt:
            return 'transgender_rights'
        return 'lgbt_rights_general'
    return topic


def extract_question_type(qw):
    qt = qw.lower()
    if 'approve' in qt and 'disapprove' in qt:
        return 'approval'
    if 'satisfied' in qt and 'dissatisfied' in qt:
        return 'right_track_wrong_track'
    if 'favor' in qt and 'oppose' in qt:
        return 'favor'
    if any(w in qt for w in ['important', 'priority', 'most important problem', 'biggest problem']):
        return 'priority'
    if 'concern' in qt or 'worry' in qt or 'worried' in qt:
        return 'concern'
    if 'agree' in qt or 'statement comes closer' in qt:
        return 'agree'
    if 'favorable' in qt and 'unfavorable' in qt:
        return 'favor'
    if 'thermometer' in qt or 'feelings toward' in qt:
        return 'favor'
    if any(w in qt for w in ['opinion of', 'view of', 'rating of']):
        return 'favor'
    if 'how much' in qt and 'problem' in qt:
        return 'concern'
    if any(w in qt for w in ['good thing', 'bad thing', 'good or bad']):
        return 'favor'
    if any(w in qt for w in ['would you rather', 'rather have']):
        return 'favor'
    return 'agree'


def parse_file(pdf_name):
    pdf_path = os.path.join(PDF_DIR, pdf_name)
    if not os.path.exists(pdf_path):
        print(f"  WARNING: {pdf_path} not found")
        return []
    
    meta = PDF_META[pdf_name]
    text = extract_all_text(pdf_path)
    
    # Detect format
    if 'AMERICAN TRENDS PANEL' in text:
        print(f"  Detected ATP format")
        questions = parse_atp_survey(text, pdf_name)
    else:
        print(f"  Detected phone survey format")
        questions = parse_phone_survey(text, pdf_name)
    
    print(f"  Found {len(questions)} questions with percentages")
    
    rows = []
    poll_counter = 1
    
    for q in questions:
        topic = classify_topic(q['q_wording'])
        issue_area = classify_issue_area(topic, q['q_wording'])
        qtype = extract_question_type(q['q_wording'])
        
        date_str = meta['date']
        poll_id = f"PEW_{date_str.replace('-', '')}_{poll_counter:03d}"
        moe = '1.5' if meta['methodology'] == 'online_panel' else ''
        
        rows.append({
            'poll_id': poll_id,
            'source': 'Pew Research Center',
            'source_url': meta['source_url'],
            'date': date_str,
            'question_type': qtype,
            'question_wording': q['q_wording'],
            'topic': topic,
            'issue_area': issue_area,
            'support_pct': q['support_pct'],
            'oppose_pct': q['oppose_pct'],
            'net': q['net'],
            'sample_size': meta['sample_size'],
            'methodology': meta['methodology'],
            'population': meta['population'],
            'moe': moe,
            'tags': meta['tags'],
            'data_quality': 'structured_poll',
        })
        poll_counter += 1
    
    return rows


def main():
    all_rows = []
    
    for pdf_name in sorted(PDF_META.keys()):
        print(f"\nProcessing {pdf_name}...")
        rows = parse_file(pdf_name)
        print(f"  Extracted {len(rows)} rows")
        all_rows.extend(rows)
    
    fieldnames = [
        'poll_id', 'source', 'source_url', 'date', 'question_type',
        'question_wording', 'topic', 'issue_area', 'support_pct', 'oppose_pct',
        'net', 'sample_size', 'methodology', 'population', 'moe', 'tags',
        'data_quality'
    ]
    
    os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)
    with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_rows)
    
    print(f"\n{'='*60}")
    print(f"TOTAL: {len(all_rows)} rows written to {OUTPUT_CSV}")
    print(f"{'='*60}")
    
    from collections import Counter
    sources = Counter(r['source_url'] for r in all_rows)
    for pdf_name in sorted(PDF_META.keys()):
        url = PDF_META[pdf_name]['source_url']
        count = sources.get(url, 0)
        print(f"  {pdf_name}: {count} questions")


if __name__ == '__main__':
    main()
