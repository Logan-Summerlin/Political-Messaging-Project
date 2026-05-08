#!/usr/bin/env python3
import csv
import datetime as dt
from pathlib import Path
import xml.etree.ElementTree as ET

BASE = Path(__file__).resolve().parent.parent
RAW = BASE / 'data' / 'raw'
PROC = BASE / 'data' / 'processed'

YEARS = [2008,2010,2012,2014,2016,2018,2020,2022,2024]

def read_csv(path):
    with open(path, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def validate_raw_coverage():
    missing = [y for y in YEARS if not (RAW / f'wiki_ballot_{y}.html').exists()]
    return missing

def normalized_year_counts():
    rows = read_csv(PROC / 'referendums.csv')
    counts = {str(y):0 for y in YEARS}
    for r in rows:
        y = r.get('year','')
        if y in counts:
            counts[y]+=1
    return counts

def schema_consistency():
    a = set(read_csv(RAW / 'wikipedia_ballot_measures.csv')[0].keys())
    b = set(read_csv(RAW / 'wikipedia_ballot_measures_complete.csv')[0].keys())
    return a,b

def feed_urls_from_xml(path):
    root = ET.parse(path).getroot()
    urls=[]
    for item in root.findall('.//item'):
        link = item.findtext('link')
        if link:
            urls.append(link.strip())
    return urls

def feed_diff(source_name, feed_urls):
    rows = read_csv(PROC / 'messages.csv')
    current = {r['source_url'] for r in rows if r.get('source')==source_name and r.get('source_url')}
    return sorted([u for u in feed_urls if u not in current])

def staleness_report(source_name, feed_urls):
    rows = read_csv(PROC / 'messages.csv') + read_csv(PROC / 'issues.csv')
    src_dates = []
    for r in rows:
        if r.get('source')==source_name and r.get('date'):
            try: src_dates.append(dt.date.fromisoformat(r['date']))
            except: pass
    max_data = max(src_dates) if src_dates else None
    # feed date fallback from url slug unsupported; use rss pubDate not stored in local artifacts
    return max_data

if __name__ == '__main__':
    miss = validate_raw_coverage()
    print('Raw coverage missing years:', miss if miss else 'none')
    print('Normalized referendum counts by year:', normalized_year_counts())
    s1,s2 = schema_consistency()
    print('Raw schema A:', sorted(s1))
    print('Raw schema B:', sorted(s2))
    dfp_feed = feed_urls_from_xml(RAW / 'dataforprogress' / 'rss_feed.xml')
    nav_feed = feed_urls_from_xml(RAW / 'navigator' / 'navigator_feed.xml') if (RAW / 'navigator' / 'navigator_feed.xml').exists() else []
    print('DFP feed URLs missing from messages.csv:', len(feed_diff('Data for Progress', dfp_feed)))
    if nav_feed:
        print('Navigator feed URLs missing from messages.csv:', len(feed_diff('Navigator Research', nav_feed)))
    print('Staleness max date - DFP:', staleness_report('Data for Progress', dfp_feed))
    print('Staleness max date - Navigator:', staleness_report('Navigator Research', nav_feed))
    print('Staleness max date - Gallup:', staleness_report('Gallup', []))
