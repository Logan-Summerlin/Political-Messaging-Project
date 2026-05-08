# Political Message A/B Testing Organization Catalog

**Generated:** May 4, 2026
**Last updated:** May 7, 2026  
**Purpose:** Catalog all organizations that publish political message testing data with exact wording, support percentages, and preference scores — similar to Blueprint Research.

---

## Tier 1: HIGH VALUE — Publish exact message wording with support percentages, freely accessible

### 1. Navigator Research
- **URL:** https://navigatorresearch.org
- **Tag/Page:** https://navigatorresearch.org/research/message-guidance/
- **Type:** Progressive message testing cooperative
- **Lean:** Progressive/Democratic
- **Publishes exact message wording?** YES — Each report shows tested messages verbatim with favorability/oppose percentages
- **Gives preference scores?** YES — Bar charts showing % favorable, % unfavorable, net favorability for each tested message
- **Provides support percentages?** YES — Detailed toplines in PDF format with full cross-tabs
- **Freely accessible?** YES — All content free, no paywall
- **Data range:** ~2017 to present (8+ years of archives)
- **Content format:** HTML articles + PDF downloads (toplines + graph decks)
- **Cloudflare:** YES (server: cloudflare) — but accessible via curl with standard headers
- **Extractable?** YES — WordPress site with sitemap at /wp-sitemap-posts-post-1.xml; message guidance posts tagged with "message-guidance" taxonomy
- **Notable:** One of the most complete sources. Each post includes "Big Takeaways," tested message text, charts with percentages, and downloadable PDFs with full methodology and crosstabs.

### 2. Data for Progress
- **URL:** https://www.dataforprogress.org
- **Blog:** https://www.dataforprogress.org/blog
- **Type:** Progressive polling and research firm
- **Lean:** Progressive/Democratic
- **Publishes exact message wording?** YES — Many blog posts show specific message tests with wording
- **Gives preference scores?** YES — Often shows % support/% oppose and net scores
- **Provides support percentages?** YES — Includes charts with exact percentages
- **Freely accessible?** YES — All content free
- **Data range:** ~2018 to present (7+ years)
- **Content format:** Squarespace blog + downloadable PDFs/images
- **Cloudflare:** NO (Squarespace)
- **Extractable?** YES — Squarespace blog structured, RSS feed available
- **Notable:** Very active publisher. Does extensive policy polling and message testing across many topics. Also does state/district-level polling.

### 3. Echelon Insights
- **URL:** https://echeloninsights.com
- **Type:** Republican strategic research firm
- **Lean:** Conservative/Republican
- **Publishes exact message wording?** PARTIALLY — Publishes polling reports; some include tested language
- **Gives preference scores?** YES — Provides approval/favorability numbers
- **Provides support percentages?** YES
- **Freely accessible?** YES — Some reports publicly available
- **Data range:** ~2020 to present
- **Content format:** HubSpot site with blog and landing pages
- **Cloudflare:** YES — Has CF cookies but accessible
- **Extractable?** PARTIALLY — Public reports are available but less focused on A/B message testing than Navigator or DFP

---

## Tier 2: MODERATE VALUE — Some message testing published, variable format

### 4. YouGov (general)
- **URL:** https://yougov.com
- **US Politics:** https://today.yougov.com/topics/politics
- **YouGov Blue:** https://yougovblue.yougov.com (separate arm for progressive clients)
- **YouGov Red:** https://yougovred.yougov.com (separate arm for conservative clients)
- **Type:** International polling/data firm
- **Lean:** Neutral (YouGov Blue = progressive, YouGov Red = conservative)
- **Publishes exact message wording?** PARTIALLY — Trackers show approval/favorability but less focused on A/B message testing. YouGov Blue/Red produce client work that may include message tests but not always publicly shared
- **Gives preference scores?** YES — Extensive tracker data
- **Provides support percentages?** YES — Full survey results
- **Freely accessible?** YES — YouGov public data is free
- **Data range:** ~2015 to present (10+ years)
- **Content format:** Angular web app with public API
- **Cloudflare:** NO (Incapsula/Imperva)
- **Extractable?** PARTIALLY — Extensive tracker data but not specifically structured as A/B message tests

### 5. Ipsos Public Affairs
- **URL:** https://www.ipsos.com/en-us
- **News/Polls:** https://www.ipsos.com/en-us/news-polls
- **Type:** Global market research firm
- **Lean:** Neutral/Independent
- **Publishes exact message wording?** PARTIALLY — Publishes poll results and some message framing studies
- **Gives preference scores?** YES — Standard polling outputs
- **Provides support percentages?** YES
- **Freely accessible?** YES — Public reports available
- **Data range:** ~2000 to present (25+ years)
- **Content format:** Drupal-based website
- **Cloudflare:** YES — Has CF cookies
- **Extractable?** PARTIALLY — Has polling data but message testing is not a primary focus

### 6. NORC at University of Chicago (AmeriSpeak)
- **URL:** https://www.norc.org
- **Type:** Academic research organization
- **Lean:** Nonpartisan/Academic
- **Publishes exact message wording?** PARTIALLY — Conducts academic experiments with message treatments but results are in academic papers, not always formatted as A/B comparisons with percentages
- **Gives preference scores?** YES — Academic papers include statistical results
- **Provides support percentages?** YES
- **Freely accessible?** PARTIALLY — Many papers behind paywalls; some public reports
- **Data range:** ~1940s to present (long-standing institution)
- **Content format:** Custom CMS
- **Cloudflare:** NO
- **Extractable?** LIMITED — Not structured for easy bulk extraction

### 7. Harvard Kennedy School / Shorenstein Center
- **URL:** https://shorensteincenter.org
- **Type:** Academic research center
- **Lean:** Nonpartisan/Academic
- **Publishes exact message wording?** PARTIALLY — Academic studies on media/politics, some with message experiments
- **Gives preference scores?** YES — Standard academic publishing
- **Provides support percentages?** YES
- **Freely accessible?** YES — Most reports publicly available
- **Data range:** ~2000 to present
- **Content format:** WordPress
- **Cloudflare:** NO (Harvard infrastructure)
- **Extractable?** LIMITED — Academic papers not structured for message test extraction

---

## Tier 3: LIMITED VALUE — Polling firms that do message testing but DON'T publish full details publicly

### 8. Lake Research Partners
- **URL:** https://www.lakeresearch.com
- **Type:** Democratic polling firm
- **Lean:** Democratic
- **Publishes exact message wording?** NO — Website is a corporate brochure, does not publish message testing results
- **Gives preference scores?** NO (on public site)
- **Provides support percentages?** NO
- **Freely accessible?** Only general information
- **Data range:** N/A for public data
- **Content format:** Duda website
- **Cloudflare:** NO
- **Extractable?** NO — No public polling content

### 9. The Tarrance Group
- **URL:** https://www.tarrance.com
- **Type:** Republican polling firm
- **Lean:** Republican
- **Publishes exact message wording?** NO — Corporate site with case studies but no published message testing
- **Gives preference scores?** NO (on public site)
- **Provides support percentages?** NO
- **Freely accessible?** Only general information
- **Data range:** N/A for public data
- **Cloudflare:** NO (WordPress)
- **Extractable?** NO — No public polling content published

### 10. GS Strategy Group
- **URL:** https://www.gsstrategygroup.com
- **Type:** Republican polling and strategy firm
- **Lean:** Republican
- **Publishes exact message wording?** NO — Corporate site, no published message testing
- **Freely accessible?** Only general information
- **Cloudflare:** NO
- **Extractable?** NO — No public polling data

### 11. Public Opinion Strategies
- **URL:** https://www.publicopinionstrategies.com (SSL error — cert issue)
- **Type:** Republican polling firm
- **Lean:** Republican
- **Publishes exact message wording?** NO — Corporate site
- **Freely accessible?** Limited
- **Extractable?** NO — SSL error encountered

### 12. Penn Schoen Berland (PSB Insights)
- **URL:** https://www.psbinsights.com
- **Type:** Corporate/Comms message testing firm
- **Lean:** Neutral/Corporate
- **Publishes exact message wording?** NO — Corporate site, does not publish client message testing
- **Freely accessible?** Only general information
- **Cloudflare:** YES (HubSpot)
- **Extractable?** NO — No public message testing data

---

## Tier 4: DEFUNCT/INACCESSIBLE — Former message testing orgs no longer accessible

### 13. Winning Message / The Opportunity Project
- **Former URL:** https://winningmessage.org (DNS does not resolve)
- **Type:** Progressive message testing cooperative
- **Status:** DEFUNCT — Domain unresolvable; Wikipedia search yields no relevant results
- **Notes:** Was a cooperative of progressive organizations pooling resources for message testing. No longer appears to be active at this domain.

### 14. Equis Research
- **Former URL:** https://equisresearch.com
- **Current URL:** https://www.equisresearch.com (parked/sedo)
- **Type:** Latino voter message testing
- **Status:** DEFUNCT — Domain appears to have expired. equisresearch.com returns 522 (Cloudflare timeout), www.equisresearch.com shows a parked domain
- **Notes:** Was active during 2020-2022 election cycles focusing on Latino voter messaging. Wikipedia has a page but the site is no longer active.

---

## Tier 5: ADVOCACY/ORGANIZING — Message testing is internal, not published publicly

### 15. American Principles Project
- **URL:** https://americanprinciplesproject.org
- **Type:** Conservative advocacy/policy organization
- **Lean:** Conservative/Republican
- **Publishes exact message wording?** NO — Publishes press releases and policy papers, not message testing data
- **Freely accessible?** Yes for general content
- **Cloudflare:** YES
- **Extractable?** NO — No message testing content

### 16. HIT Strategies
- **URL:** https://www.hitstrategies.com
- **Type:** Research firm focused on Black voters
- **Lean:** Democratic/progressive
- **Publishes exact message wording?** PARTIALLY — Site is Wix-based, has research publications tab
- **Gives preference scores?** YES (some reports)
- **Freely accessible?** Some reports available
- **Cloudflare:** NO (Wix)
- **Extractable?** LIMITED — Site is JS-heavy (Wix) but may have some public PDFs

### 17. Voto Latino
- **URL:** https://votolatino.org
- **Type:** Latino voter registration/organizing
- **Lean:** Democratic
- **Publishes exact message wording?** NO — Voter registration and advocacy org, not a message testing publisher
- **Cloudflare:** NO (WordPress running Cloudflare-like protection)
- **Extractable?** NO

### 18. Mi Familia Vota
- **URL:** https://www.mifamiliavota.org
- **Type:** Latino civic engagement
- **Lean:** Democratic
- **Publishes exact message wording?** NO — Advocacy/organizing organization
- **Cloudflare:** NO (WordPress)
- **Extractable?** NO

---

## Summary Table

| # | Source | URL | Exact Wording? | % Scores? | Free? | Years | CF? | Extractable? |
|---|--------|-----|:---:|:---:|:---:|:---:|:---:|:---:|
| 1 | **Navigator Research** | navigatorresearch.org | YES | YES | YES | 2017+ | YES | YES |
| 2 | **Data for Progress** | dataforprogress.org | YES | YES | YES | 2018+ | NO | YES |
| 3 | **Echelon Insights** | echeloninsights.com | Partial | YES | YES | 2020+ | YES | Partial |
| 4 | **YouGov** | yougov.com | Partial | YES | YES | 2015+ | NO¹ | Partial |
| 5 | **Ipsos** | ipsos.com | Partial | YES | YES | 2000+ | YES | Partial |
| 6 | **NORC** | norc.org | Partial | YES | Partial | Long | NO | Limited |
| 7 | **HKS/Shorenstein** | shorensteincenter.org | Partial | YES | YES | 2000+ | NO | Limited |
| 8 | **Lake Research** | lakeresearch.com | NO | NO | NO | — | NO | NO |
| 9 | **Tarrance Group** | tarrance.com | NO | NO | NO | — | NO | NO |
| 10 | **GS Strategy Grp** | gsstrategygroup.com | NO | NO | NO | — | NO | NO |
| 11 | **POS** | publicopinionstrategies.com | NO | NO | NO | — | NO | SSL Err |
| 12 | **PSB Insights** | psbinsights.com | NO | NO | NO | — | YES | NO |
| 13 | **Winning Message** | winningmessage.org | DEFUNCT | — | — | — | — | — |
| 14 | **Equis Research** | equisresearch.com | DEFUNCT | — | — | — | — | — |
| 15 | **APP** | americanprinciplesproject.org | NO | NO | NO | — | YES | NO |
| 16 | **HIT Strategies** | hitstrategies.com | Partial | Partial | Partial | ~2020+ | NO | Limited |
| 17 | **Voto Latino** | votolatino.org | NO | NO | NO | — | Partial | NO |
| 18 | **Mi Familia Vota** | mifamiliavota.org | NO | NO | NO | — | NO | NO |

¹ YouGov uses Incapsula/Imperva — similar to Cloudflare but different WAF.

---

## Recommended Extraction Targets (Priority Order)

**PRIORITY 1 — Readily extractable, high value:**
1. **Navigator Research** — 22 articles identified, 13 with structured poll data. 53 rows extracted with support/oppose percentages. WordPress RSS feed available at /feed/.
2. **Data for Progress** — 500+ blog posts with polling and message tests. Squarespace RSS feed available. No Cloudflare.

**PRIORITY 2 — Moderate value, some extraction needed:**
3. **Echelon Insights** — Blog/reports with polling data. HubSpot hosted, some tests public.
4. **YouGov** — Massive tracker data, but A/B message testing is not their primary format.
5. **Ipsos** — Polling archives, message framing studies scattered.

**PRIORITY 3 — Limited/no public message data:**
6-18: Various firms that either don't publish message tests, are defunct, or require special access.

---

## Methodology Notes
- All URLs were checked via HTTP(S) requests on May 4, 2026
- Cloudflare detection via server headers and cf-ray/cf-cookies
- "Exact wording" means the source publishes the verbatim text of tested message frames
- "Preference scores" means the source shows which message "won" with comparative percentages
- Status "DEFUNCT" means the domain is unresolvable or returns no actual content
