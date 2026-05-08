#!/usr/bin/env python3
"""
Parse DFP raw chunks into structured messages.csv and issues.csv rows.

Processes chunk1–chunk4 from data/raw/dataforprogress/ and extracts:
  - Issue polling rows (any bullet point with a percentage)
  - Message test rows (from "Tested Message Wording" sections in chunk2)

Output: data/processed/dfp_new_messages.csv and dfp_new_issues.csv
Ready for deduplication against existing data.
"""

import csv, re, sys
from pathlib import Path
from collections import Counter
from datetime import datetime

RAW_DIR = Path(__file__).parent.parent / "data" / "raw" / "dataforprogress"
OUT_DIR = Path(__file__).parent.parent / "data" / "processed"

# Topic keyword map — inferred from article title
TOPIC_KEYWORDS = {
    "economy": ["economy", "economic", "inflation", "cost of living", "prices", "jobs", "wages", "recession", "gdp", "stimulus"],
    "healthcare": ["healthcare", "health care", "medicare", "medicaid", "insurance", "prescription", "drugs", "hospital", "doctor"],
    "immigration": ["immigra", "border", "asylum", "deport", "visa", "migrant", "refugee", "citizenship", "ice"],
    "climate": ["climate", "environment", "green", "emissions", "carbon", "energy", "solar", "wind", "fossil", "renewable", "clean energy"],
    "foreign_policy": ["foreign", "iran", "china", "russia", "ukraine", "nato", "israel", "gaza", "palestine", "defense", "military", "war", "sanctions"],
    "democracy": ["democracy", "voting", "election", "vote", "gerrymander", "rights", "freedom", "constitution", "congress", "senate"],
    "abortion": ["abortion", "reproductive", "pro-choice", "pro-life", "roe"],
    "guns": ["gun", "firearm", "second amendment", "shooting", "weapon"],
    "crime": ["crime", "police", "criminal", "justice", "prison", "safety"],
    "education": ["education", "school", "student", "college", "university", "teacher"],
    "taxes": ["tax", "irs", "tax cut", "tax credit"],
    "social_security": ["social security", "ssn", "retirement", "pension"],
    "technology": ["tech", "ai", "artificial intelligence", "social media", "internet", "data", "privacy", "algorithm"],
    "housing": ["housing", "rent", "homeowner", "mortgage", "homeless", "affordable housing"],
    "trade": ["trade", "tariff", "import", "export"],
    "civil_rights": ["civil rights", "lgbt", "trans", "gay", "equality", "discrimination", "racial"],
    "drugs": ["drug", "marijuana", "cannabis", "opioid", "addiction"],
    "corruption": ["corruption", "ethics", "lobby", "campaign finance"],
}

def infer_topic(title, url=""):
    """Infer topic from title text using keyword matching."""
    text = (title + " " + url).lower()
    for topic, keywords in TOPIC_KEYWORDS.items():
        for kw in keywords:
            if kw in text:
                return topic
    return "general"


def extract_pct(text):
    """Extract first percentage from text."""
    match = re.search(r'(\d+)%', text)
    return float(match.group(1)) if match else None


def extract_sample_size(text):
    """Extract sample size like 'Sample size: 1167' or 'n=1250'."""
    m = re.search(r'[Ss]ample size[:\s]*(\d[\d,]*)', text)
    if m:
        return int(m.group(1).replace(',', ''))
    m = re.search(r'[Nn]\s*=\s*(\d[\d,]*)', text)
    if m:
        return int(m.group(1).replace(',', ''))
    return None


def extract_date(s):
    """Parse various date formats to YYYY-MM-DD."""
    s = s.strip()
    # Already ISO
    if re.match(r'^\d{4}-\d{2}-\d{2}$', s):
        return s
    # "August 18, 2022"
    for fmt in ["%B %d, %Y", "%B %d %Y", "%b %d, %Y", "%m/%d/%Y"]:
        try:
            return datetime.strptime(s, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return s  # return as-is if can't parse


def clean_bullet(text):
    """Clean a bullet point: strip leading dash, whitespace, quotes."""
    text = text.strip()
    if text.startswith("- "):
        text = text[2:]
    if text.startswith('"') and text.endswith('"'):
        text = text[1:-1]
    if text.startswith('“') and text.endswith('”'):
        text = text[1:-1]
    return text.strip()


def parse_chunk1(text):
    """Parse chunk1: ## Article N format with ### Polling Findings."""
    articles = []
    # Split by article markers
    parts = re.split(r'## Article \d+\n', text)
    for part in parts[1:]:  # skip header
        article = parse_common_article(part)
        if article:
            articles.append(article)
    return articles


def parse_chunk2(text):
    """Parse chunk2: ## {Title} format with **Tested Message Wording:** and **Polling Data & Findings:**"""
    articles = []
    lines = text.split('\n')
    
    # Find ## headers that start articles (after the intro)
    i = 0
    # Skip past the intro header
    while i < len(lines) and not lines[i].startswith('## '):
        i += 1
    if i < len(lines):
        i += 1  # skip first ## (the main header)
    
    current_article = None
    current_section = None
    msg_wording_bullets = []
    polling_bullets = []
    
    while i < len(lines):
        line = lines[i]
        
        if line.startswith('## '):
            # Save previous article
            if current_article:
                current_article['msg_wording'] = msg_wording_bullets
                current_article['polling_bullets'] = polling_bullets
                articles.append(current_article)
            
            # Start new article
            title = line[3:].strip()
            current_article = {'title': title, 'url': '', 'date': '', 'sample_size': None}
            msg_wording_bullets = []
            polling_bullets = []
            current_section = None
            
        elif line.strip().startswith('**URL:**') and current_article:
            current_article['url'] = line.split(':', 1)[1].strip().replace('**', '').strip()
            
        elif line.strip().startswith('**Date:**') and current_article:
            current_article['date'] = extract_date(line.split(':', 1)[1].strip().replace('**', '').strip())
            
        elif line.strip().startswith('**Tested Message Wording:**'):
            current_section = 'message'
            
        elif line.strip().startswith('**Polling Data & Findings:**'):
            current_section = 'polling'
            
        elif line.strip().startswith('- ') and current_article:
            bullet = clean_bullet(line)
            if bullet:
                if current_section == 'message':
                    msg_wording_bullets.append(bullet)
                elif current_section == 'polling':
                    polling_bullets.append(bullet)
        
        i += 1
    
    # Save last article
    if current_article:
        current_article['msg_wording'] = msg_wording_bullets
        current_article['polling_bullets'] = polling_bullets
        articles.append(current_article)
    
    return articles


def parse_chunk3(text):
    """Parse chunk3: ## N. {Title} format with **Polling Findings:**"""
    articles = []
    lines = text.split('\n')
    
    i = 0
    while i < len(lines) and not lines[i].startswith('## '):
        i += 1
    if i < len(lines):
        i += 1  # skip main header
    
    current_article = None
    current_section = None
    polling_bullets = []
    
    while i < len(lines):
        line = lines[i]
        
        if line.startswith('## ') and not line.startswith('###'):
            if current_article:
                current_article['polling_bullets'] = polling_bullets
                articles.append(current_article)
            
            # Strip the "N. " prefix from title
            title = re.sub(r'^\d+\.\s*', '', line[3:]).strip()
            current_article = {'title': title, 'url': '', 'date': '', 'sample_size': None}
            polling_bullets = []
            current_section = None
            
        elif line.strip().startswith('**URL:**') and current_article:
            current_article['url'] = line.split(':', 1)[1].strip().replace('**', '').strip()
            
        elif line.strip().startswith('**Date:**') and current_article:
            current_article['date'] = extract_date(line.split(':', 1)[1].strip().replace('**', '').strip())
            
        elif line.strip().startswith('**Polling Findings:**'):
            current_section = 'polling'
            
        elif line.strip().startswith('- ') and current_article:
            bullet = clean_bullet(line)
            if bullet and current_section == 'polling':
                polling_bullets.append(bullet)
        
        i += 1
    
    if current_article:
        current_article['polling_bullets'] = polling_bullets
        articles.append(current_article)
    
    return articles


def parse_chunk4(text):
    """Parse chunk4: ## {Title} format with - **URL** and - **Date** format."""
    articles = []
    lines = text.split('\n')
    
    i = 0
    while i < len(lines) and not lines[i].startswith('## '):
        i += 1
    if i < len(lines):
        i += 1
    
    current_article = None
    current_section = None
    polling_bullets = []
    
    while i < len(lines):
        line = lines[i]
        
        if line.startswith('## ') and not line.startswith('###'):
            if current_article:
                current_article['polling_bullets'] = polling_bullets
                articles.append(current_article)
            
            title = line[3:].strip()
            current_article = {'title': title, 'url': '', 'date': '', 'sample_size': None}
            polling_bullets = []
            current_section = None
            
        elif line.strip().startswith('- **URL**') and current_article:
            url_match = re.search(r'\(https?://[^\)]+\)', line)
            if url_match:
                current_article['url'] = url_match.group(0)[1:-1]
            
        elif line.strip().startswith('- **Date**') and current_article:
            date_match = re.search(r'\*\*Date\*\*:\s*(.*)', line)
            if date_match:
                current_article['date'] = extract_date(date_match.group(1).strip())
            
        elif line.strip().startswith('**Polling Findings:**'):
            current_section = 'polling'
            
        elif line.strip().startswith('- ') and current_article:
            bullet = clean_bullet(line)
            if bullet and current_section == 'polling':
                polling_bullets.append(bullet)
        
        i += 1
    
    if current_article:
        current_article['polling_bullets'] = polling_bullets
        articles.append(current_article)
    
    return articles


def parse_common_article(part):
    """Parse an article section shared across formats (title, url, date, bullets)."""
    lines = part.split('\n')
    article = {'title': '', 'url': '', 'date': '', 'sample_size': None, 'bullets': []}
    
    for line in lines:
        if line.startswith('**Title:**'):
            article['title'] = line.split(':', 1)[1].strip().replace('**', '').strip()
        elif line.startswith('**URL:**'):
            article['url'] = line.split(':', 1)[1].strip().replace('**', '').strip()
        elif line.startswith('**Date:**'):
            article['date'] = extract_date(line.split(':', 1)[1].strip().replace('**', '').strip())
        elif line.strip().startswith('- Sample size:'):
            article['sample_size'] = extract_sample_size(line)
        elif line.strip().startswith('- ') and not line.strip().startswith('- Sample'):
            bullet = clean_bullet(line)
            if bullet:
                article['bullets'].append(bullet)
    
    if article['title'] or article['url']:
        return article
    return None


def bullet_to_issue_row(article, bullet_text, idx):
    """Convert a polling finding bullet to an issues.csv row."""
    pct = extract_pct(bullet_text)
    if pct is None:
        return None
    
    # Clip long bullet text
    wording = bullet_text[:500]
    if len(bullet_text) > 500:
        wording += "..."
    
    topic = infer_topic(article.get('title', ''), article.get('url', ''))
    
    return {
        'poll_id': f"DFP_{article.get('date', 'unknown').replace('-', '')[:8]}_{idx:04d}",
        'source': 'Data for Progress',
        'source_url': article.get('url', ''),
        'date': article.get('date', ''),
        'question_type': 'polling',
        'question_wording': wording,
        'topic': topic,
        'issue_area': '',
        'support_pct': str(pct),
        'oppose_pct': '',
        'net': '',
        'sample_size': str(article.get('sample_size', '')) if article.get('sample_size') else '',
        'methodology': 'online_panel',
        'population': 'voters',
        'moe': '',
        'tags': f"dfp;{topic}",
        'notes': f"From: {article.get('title', '')}" if article.get('title') else '',
    }


def bullet_to_message_row(article, bullet_text, idx):
    """Convert a message test bullet to a messages.csv row."""
    pct = extract_pct(bullet_text)
    topic = infer_topic(article.get('title', ''), article.get('url', ''))
    
    return {
        'message_id': f"DFP_{article.get('date', 'unknown').replace('-', '')[:8]}_{idx:04d}",
        'source': 'Data for Progress',
        'source_url': article.get('url', ''),
        'date': article.get('date', ''),
        'topic': topic,
        'issue_area': '',
        'message_type': 'tested_message',
        'wording': bullet_text[:1000],
        'support_pct': str(pct) if pct else '',
        'oppose_pct': '',
        'net_score': '',
        'preference_effect': '',
        'effect_scale': '',
        'sample_size': str(article.get('sample_size', '')) if article.get('sample_size') else '',
        'methodology': 'online_panel',
        'population': 'voters',
        'moe': '',
        'tags': f"dfp;{topic}",
        'notes': f"From: {article.get('title', '')}" if article.get('title') else '',
    }


def process():
    issue_rows = []
    msg_rows = []
    article_count = 0
    bullet_count = 0
    msg_source_count = 0
    
    # Chunk 1
    with open(RAW_DIR / "chunk1_polling_data.md", encoding='utf-8') as f:
        articles = parse_chunk1(f.read())
    article_count += len(articles)
    for art in articles:
        for i, bullet in enumerate(art.get('bullets', [])):
            row = bullet_to_issue_row(art, bullet, len(issue_rows))
            if row:
                issue_rows.append(row)
            bullet_count += 1
    
    # Chunk 2
    with open(RAW_DIR / "chunk2_polling_data.md", encoding='utf-8') as f:
        articles2 = parse_chunk2(f.read())
    article_count += len(articles2)
    for art in articles2:
        # Tested Message Wording → messages
        for i, wording in enumerate(art.get('msg_wording', [])):
            row = bullet_to_message_row(art, wording, len(msg_rows))
            if row:
                msg_rows.append(row)
                msg_source_count += 1
        # Polling Data → issues
        for i, bullet in enumerate(art.get('polling_bullets', [])):
            row = bullet_to_issue_row(art, bullet, len(issue_rows))
            if row:
                issue_rows.append(row)
            bullet_count += 1
    
    # Chunk 3
    with open(RAW_DIR / "chunk3_polling_data.md", encoding='utf-8') as f:
        articles3 = parse_chunk3(f.read())
    article_count += len(articles3)
    for art in articles3:
        for i, bullet in enumerate(art.get('polling_bullets', [])):
            row = bullet_to_issue_row(art, bullet, len(issue_rows))
            if row:
                issue_rows.append(row)
            bullet_count += 1
    
    # Chunk 4
    with open(RAW_DIR / "chunk4_polling_data.md", encoding='utf-8') as f:
        articles4 = parse_chunk4(f.read())
    article_count += len(articles4)
    for art in articles4:
        for i, bullet in enumerate(art.get('polling_bullets', [])):
            row = bullet_to_issue_row(art, bullet, len(issue_rows))
            if row:
                issue_rows.append(row)
            bullet_count += 1
    
    print(f"Processed {article_count} articles across 4 chunks")
    print(f"Total bullet points: {bullet_count}")
    print(f"Issue rows extracted (with percentages): {len(issue_rows)}")
    print(f"Message rows extracted: {len(msg_rows)}")
    
    # Write outputs
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    
    issue_fields = ['poll_id', 'source', 'source_url', 'date', 'question_type', 'question_wording',
                    'topic', 'issue_area', 'support_pct', 'oppose_pct', 'net', 'sample_size',
                    'methodology', 'population', 'moe', 'tags', 'notes']
    
    msg_fields = ['message_id', 'source', 'source_url', 'date', 'topic', 'issue_area', 'message_type',
                  'wording', 'support_pct', 'oppose_pct', 'net_score', 'preference_effect', 'effect_scale',
                  'sample_size', 'methodology', 'population', 'moe', 'tags', 'notes']
    
    with open(OUT_DIR / "dfp_new_issues.csv", 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=issue_fields)
        writer.writeheader()
        writer.writerows(issue_rows)
    
    with open(OUT_DIR / "dfp_new_messages.csv", 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=msg_fields)
        writer.writeheader()
        writer.writerows(msg_rows)
    
    print(f"\nWritten to:")
    print(f"  data/processed/dfp_new_issues.csv ({len(issue_rows)} rows)")
    print(f"  data/processed/dfp_new_messages.csv ({len(msg_rows)} rows)")


if __name__ == "__main__":
    process()
