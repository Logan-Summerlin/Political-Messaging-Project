# US Ballot Measure / Referendum Data Source Catalog
**Generated:** May 4, 2026
**Purpose:** Catalog all sources for US ballot measure/referendum language and results — what they provide and how to access them.

---

## Tier 1: ✅ WORK — Readily extractable, best value

### 1. Wikipedia (MediaWiki API)
**Status:** ✅ EXCELLENT — Best freely accessible multi-state source
- **Ballot language?** Summaries/titles (not full legal text)
- **Vote results?** ✅ Yes — yes/no % and raw counts in HTML tables
- **Access:** `en.wikipedia.org/w/api.php?action=parse&page=2024_United_States_ballot_measures&prop=text&format=json`
- **Years:** ~2004–present (yearly pages)
- **States:** All 50
- **Cost:** Free
- **Rate limit:** ~200 req/min

### 2. California Secretary of State (sos.ca.gov)
**Status:** ✅ EXCELLENT — Best single-state source
- **Ballot language?** ✅ Full text in Voter Information Guides
- **Vote results?** ✅ Yes — results since 1990
- **Access:** Direct scrape, no bot protection
- **URL:** `sos.ca.gov/elections/prior-elections/statewide-election-results`
- **Years:** 1911–present
- **Cost:** Free

### 3. UC Law San Francisco (repository.uclawsf.edu/ca_ballots)
**Status:** ✅ EXCELLENT — Best for historical CA ballot language
- **Ballot language?** ✅ Full text PDFs of all propositions, initiatives, and voter pamphlets
- **Vote results?** ⚠️ Some records
- **Access:** Digital Commons/bepress platform, RSS feeds, scrapeable
- **URL:** `repository.uclawsf.edu/ca_ballot_props/`
- **Years:** 1911–2020 (near-complete)
- **Cost:** Free

### 4. Colorado Secretary of State (sos.state.co.us)
**Status:** ✅ GOOD — Working single-state source
- **Access:** Direct scrape at `sos.state.co.us/pubs/elections/Results/Abstract/20XX/`
- **Years:** 1990s–present

### 5. Google Civic Information API
**Status:** ⚠️ Current/upcoming elections only (no historical results)
- **Ballot language?** ✅ Full text of upcoming measures (referendumTitle, referendumSubtitle, referendumText, yesVoteDescription, noVoteDescription)
- **Vote results?** ❌ No (pre-election only)
- **Access:** `civicinfo.googleapis.com/v2/elections` — free API key
- **Best for:** Getting upcoming ballot measure text programmatically

---

## Tier 2: ⚠️ PARTIAL — Accessible but limited

### 6. Ballotpedia (ballotpedia.org)
**Status:** ❌ WAF-blocked for programmatic access
- **Best source** for full ballot language, vote %, campaign finance, analysis
- Programmatic access requires headless browser (Playwright + stealth plugin)
- **RSS feed works:** `news.ballotpedia.org/feed/` (news articles, not structured data)
- **Years:** Full historical | **States:** All 50

### 7. NCSL (ncsl.org)
**Status:** ❌ Cloudflare-blocked
- Excellent human-usable database with summaries and analysis
- Requires headless browser

### 8. OpenSecrets / FollowTheMoney (opensecrets.org)
**Status:** ❌ Cloudflare-blocked
- Campaign finance data for ballot measure campaigns
- Would be useful if accessible

---

## Tier 3: ❌ BLOCKED OR DEFUNCT

| Source | Status | Notes |
|--------|--------|-------|
| Arizona SoS (azsos.gov) | ❌ Cloudflare 403 | |
| Florida DoS (dos.fl.gov) | ❌ 404 on results page | |
| I&R Institute (iandrinstitute.org) | ❌ Empty/defunct | |
| ProCon.org | ❌ Redirects to Britannica (CF) | |
| Vote Smart (votesmart.org) | ❌ 403 blocked | |
| OpenStates (openstates.org) | ⚠️ No ballot endpoint | Good for bills only |

---

## Recommended Extraction Strategy

**Priority 1:** Wikipedia API → nationwide summary data (titles, outcomes, vote splits). All states, multiple years, free, structured HTML tables.

**Priority 2:** UC Law SF + CA SoS → California full-text ballot language. Best single-state archive with 1911-2020 coverage.

**Priority 3:** State election sites that work (CO SoS, others TBD) for individual state deep dives.

**Priority 4:** Google Civic API → upcoming ballot measure text. Free, structured, multi-state.

**Priority 5 (if needed):** Ballotpedia + NCSL via headless browser agent-browser for comprehensive coverage.

---

## How to Extract Wikipedia Ballot Data

```bash
# Get a year's ballot measures
curl -s "https://en.wikipedia.org/w/api.php?action=parse&page=2024_United_States_ballot_measures&prop=text&format=json" | \
  python3 -c "
import sys, json, re, html as _html
data = json.load(sys.stdin)
text = data['parse']['text']['*']
# Tables contain state, measure name, subject, yes%, no%, outcome
tables = re.findall(r'<table[^>]*class=\"wikitable[^\"]*\"[^>]*>.*?</table>', text, re.DOTALL)
print(f'Found {len(tables)} tables')
for t in tables[:3]:
    rows = re.findall(r'<tr>(.*?)</tr>', t, re.DOTALL)
    for r in rows[:5]:
        cells = re.findall(r'<t[dh][^>]*>(.*?)</t[dh]>', r, re.DOTALL)
        clean = [_html.unescape(re.sub(r'<[^>]+>', '', c)).strip()[:40] for c in cells]
        print(' | '.join(clean))
"
```
