#!/usr/bin/env python3
"""Extract all data from UC Law SF Digital Commons repository pages."""
import re
import json
import os

OUTPUT_DIR = '/home/agentbot/workspace/us-political-messaging-dataset/data/raw/california'

def extract_propositions(filepath):
    """Extract propositions from the Propositions browse page."""
    with open(filepath) as f:
        content = f.read()
    
    # Find year sections and their positions
    year_matches = list(re.finditer(r'<h4 id="year_(\d{4})">', content))
    
    propositions = []
    
    # Find all items - each has a PDF link followed by an article link with pub info
    # Pattern: <p class="pdf"><a href="PDF_URL">...</a></p>
    #          <p class="article-listing"><a href="ARTICLE_URL">TITLE</a>
    #          <span class="index_pubinfo"><em>California Proposition N (YEAR)</em></span></p>
    
    pattern = (
        r'<p class="pdf"><a href="(https://repository\.uclawsf\.edu/cgi/viewcontent\.cgi\?article=(\d+)&amp;context=ca_ballot_props)"[^>]*>.*?</a></p>\s*'
        r'<p class="article-listing"><a href="(https://repository\.uclawsf\.edu/ca_ballot_props/(\d+))"[^>]*>(.*?)</a>\s*'
        r'<span class="index_pubinfo">\s*<em>(.*?)</em>\s*</span>\s*</p>'
    )
    
    items = re.findall(pattern, content, re.DOTALL)
    
    for pdf_url, article_num, article_url, article_id, title_html, pubinfo in items:
        title = ' '.join(re.sub(r'<[^>]+>', '', title_html).strip().split())
        pubinfo_clean = ' '.join(re.sub(r'<[^>]+>', '', pubinfo).strip().split())
        
        # Extract year and proposition number from pubinfo
        year_match = re.search(r'\((\d{4})\)', pubinfo_clean)
        year = year_match.group(1) if year_match else None
        
        prop_match = re.search(r'Proposition\s+(\d+[A-Z]?)', pubinfo_clean, re.IGNORECASE)
        prop_number = prop_match.group(1) if prop_match else None
        
        propositions.append({
            'type': 'proposition',
            'year': year,
            'proposition_number': prop_number,
            'title': title,
            'pubinfo': pubinfo_clean,
            'url': article_url,
            'pdf_url': pdf_url.replace('&amp;', '&'),
            'article_id': article_id
        })
    
    # Also check for Voter Information Guides mixed in (they also appear in Propositions)
    # Pattern: Voter Information Guide for YEAR, ELECTION_TYPE
    guide_pattern = (
        r'<p class="pdf"><a href="(https://repository\.uclawsf\.edu/cgi/viewcontent\.cgi\?article=(\d+)&amp;context=ca_ballot_props)"[^>]*>.*?</a></p>\s*'
        r'<p class="article-listing"><a href="(https://repository\.uclawsf\.edu/ca_ballot_props/(\d+))"[^>]*>(Voter Information Guide.*?)</a>'
    )
    guides = re.findall(guide_pattern, content, re.DOTALL)
    
    for pdf_url, article_num, article_url, article_id, title in guides:
        title_clean = ' '.join(title.strip().split())
        # Extract year from title
        year_match = re.search(r'(\d{4})', title_clean)
        year = year_match.group(1) if year_match else None
        
        propositions.append({
            'type': 'voter_guide',
            'year': year,
            'proposition_number': None,
            'title': title_clean,
            'pubinfo': '',
            'url': article_url,
            'pdf_url': pdf_url.replace('&amp;', '&'),
            'article_id': article_id
        })
    
    return propositions


def extract_initiatives(filepath):
    """Extract initiatives from the Initiatives browse page."""
    with open(filepath) as f:
        content = f.read()
    
    initiatives = []
    
    # Digital Commons uses different structure for initiatives
    # Look for article listings with initiative titles
    
    # Find all items in the page
    items = re.findall(
        r'<p class="article-listing"><a href="(https://repository\.uclawsf\.edu/ca_ballot_inits/(\d+))"[^>]*>(.*?)</a>\s*'
        r'<span class="index_pubinfo">\s*<em>(.*?)</em>\s*</span>\s*</p>',
        content, re.DOTALL
    )
    
    for article_url, article_id, title_html, pubinfo in items:
        title = ' '.join(re.sub(r'<[^>]+>', '', title_html).strip().split())
        pubinfo_clean = ' '.join(re.sub(r'<[^>]+>', '', pubinfo).strip().split())
        
        year_match = re.search(r'\((\d{4})\)', pubinfo_clean)
        year = year_match.group(1) if year_match else None
        
        # Find PDF link - search backwards in content for PDF link before this article
        pos = content.find(article_url)
        preceding = content[max(0, pos-500):pos]
        pdf_match = re.search(r'href="(https://repository\.uclawsf\.edu/cgi/viewcontent\.cgi\?article=\d+&amp;context=ca_ballot_inits)"', preceding)
        pdf_url = pdf_match.group(1).replace('&amp;', '&') if pdf_match else None
        
        initiatives.append({
            'type': 'initiative',
            'year': year,
            'title': title,
            'pubinfo': pubinfo_clean,
            'url': article_url,
            'pdf_url': pdf_url,
            'article_id': article_id
        })
    
    return initiatives


def extract_pamphlets(filepath):
    """Extract pamphlets from the Pamphlets browse page."""
    with open(filepath) as f:
        content = f.read()
    
    pamphlets = []
    
    items = re.findall(
        r'<p class="pdf"><a href="(https://repository\.uclawsf\.edu/cgi/viewcontent\.cgi\?article=(\d+)&amp;context=ca_ballot_props)"[^>]*>.*?</a></p>\s*'
        r'<p class="article-listing"><a href="(https://repository\.uclawsf\.edu/ca_ballot_props/(\d+))"[^>]*>(.*?)</a>',
        content, re.DOTALL
    )
    
    for pdf_url, article_num, article_url, article_id, title_html in items:
        title = ' '.join(re.sub(r'<[^>]+>', '', title_html).strip().split())
        
        year_match = re.search(r'(\d{4})', title)
        year = year_match.group(1) if year_match else None
        
        pamphlets.append({
            'type': 'pamphlet',
            'year': year,
            'title': title,
            'url': article_url,
            'pdf_url': pdf_url.replace('&amp;', '&'),
            'article_id': article_id
        })
    
    return pamphlets


def get_year_counts(items):
    """Get count of items by year."""
    from collections import Counter
    years = [i.get('year') for i in items if i.get('year')]
    return Counter(years)


# Main execution
if __name__ == '__main__':
    # Extract propositions
    props = extract_propositions(os.path.join(OUTPUT_DIR, 'uclaw_browse.html'))
    print(f"Propositions extracted: {len(props)}")
    for p in props:
        print(f"  {p['year']}: Prop {p.get('proposition_number','?')} - {p['title'][:60]}")
    
    # Extract initiatives
    inits = extract_initiatives(os.path.join(OUTPUT_DIR, 'uclaw_inits.html'))
    print(f"\nInitiatives extracted: {len(inits)}")
    for i in inits[:5]:
        print(f"  {i['year']}: {i['title'][:60]}")
    if len(inits) > 5:
        print(f"  ... and {len(inits)-5} more")
    
    # Extract pamphlets
    pamphlets = extract_pamphlets(os.path.join(OUTPUT_DIR, 'uclaw_pamphlets.html'))
    print(f"\nPamphlets extracted: {len(pamphlets)}")
    for p in pamphlets[:5]:
        print(f"  {p['year']}: {p['title'][:60]}")
    if len(pamphlets) > 5:
        print(f"  ... and {len(pamphlets)-5} more")
    
    # Save all data
    data = {
        'propositions': props,
        'initiatives': inits,
        'pamphlets': pamphlets
    }
    with open(os.path.join(OUTPUT_DIR, 'uclaw_all_data.json'), 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"\nYear distribution - Propositions:")
    for y, c in sorted(get_year_counts(props).items()):
        print(f"  {y}: {c}")
    
    print(f"\nYear distribution - Pamphlets:")
    for y, c in sorted(get_year_counts(pamphlets).items()):
        print(f"  {y}: {c}")
    
    print(f"\nSaved to uclaw_all_data.json")
