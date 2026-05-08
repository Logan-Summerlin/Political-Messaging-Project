# Polling Data Summary — May 4, 2026

This report summarizes polling data gathered from YouGov, Gallup, Ipsos, and the Roper Center via Google News RSS, direct site queries, and text-extraction APIs. Exact question wording and topline percentages are included where available.

---

## 1. IPSOS / REUTERS POLLS

### A. Reuters/Ipsos Poll — March 20–23, 2026
**Source:** Ipsos for Reuters | **Sample:** 1,272 US adults (probability-based KnowledgePanel®) | **MOE:** ±2.8 pp (95% CI)

**Question: "What do you think is the most important problem facing the U.S. today?" (open-ended)**
- Economy, unemployment and jobs: **16%** (top mention)
- War and foreign conflicts: **14%** (up from 1% in February 2026)
- Other issues cited but not broken out individually

**Question: "Do you approve or disapprove of the U.S. military strikes against Iran?"**
- Approve: **35%**
- Disapprove: **61%**

**Question: "Do you approve or disapprove of the way Donald Trump is handling his job as president?"**
- Overall approve: **36%** (down from 40–38% in prior weeks)
- Approve on handling cost of living: **25%**
- Disapprove on handling cost of living: **66%**

**Question: "Would you say the economy is ... ?"**
- Very/somewhat strong: **34%**
- Very/somewhat weak: **63%**

### B. Reuters/Ipsos Poll — Late March 2026
**Source:** Reuters, March 25-26 | Trump approval hits **36%** — new second-term low
- Driven by fuel price surges amid Iran conflict

### C. Post-ABC-Ipsos Poll — Early May 2026
**Source:** Washington Post / ABC News / Ipsos, released May 3, 2026
- Trump disapproval reaches **new high**
- **Two-thirds** of Americans say country is headed in wrong direction
- Specific question: "Do you think things in this country are going in the right direction, or are they off on the wrong track?"

### D. Ipsos — "Economy and Foreign Conflicts Now Public's Top Two Issue Concerns" (March 24, 2026)
- Americans view economy and war/foreign conflicts as the top two problems
- 14% cite war/foreign conflicts (up from 1% in February)
- 16% cite economy/unemployment/jobs

---

## 2. YOUGOV POLLS

### A. "Inflation is Americans' most important political issue — and one where Trump is particularly unpopular"
**Date:** April 7, 2026 | **Source:** today.yougov.com
- Inflation rated as the most important political issue among Americans
- Trump rated particularly unpopular on handling inflation
- *(Exact question wording and topline percentages were embedded in JavaScript-rendered Datawrapper charts and could not be fully extracted programmatically)*

### B. "Trump is losing support from Independents over Iran"
**Date:** March 17, 2026 | **Source:** yougov.com
- Trump losing Independent voter support over Iran conflict management

### C. "Majorities of Americans say wealth inequality is a problem and want government intervention"
**Date:** January 6, 2026 | **Source:** yougov.com
- Majority see wealth inequality as a serious problem
- Majority want government intervention

### D. "Most Americans support proof of citizenship to vote, but limiting use of mail-in ballots is more divisive"
**Date:** March 17, 2026 | **Source:** yougov.com
- Majority support proof of citizenship to vote
- Mail-in ballot limits more divisive

### E. "Nearly all Americans say the conflict with Iran is raising gas prices, but few expect Trump to back down"
**Date:** April 2026 | **Source:** yougov.com
- Nearly all Americans perceive Iran conflict raising gas prices
- Few expect Trump to change course

### F. "Today more Americans support than oppose abolishing ICE"
**Date:** January 25, 2026 | **Source:** yougov.com
- More Americans support than oppose abolishing ICE

### G. "The issues that Democrats and Republicans want their parties to focus on more"
**Date:** January 27, 2026 | **Source:** yougov.com
- Partisan divergence on priority issues

### H. "The U.S.'s war with Iran remains unpopular"
**Date:** April 7, 2026 | **Source:** yougov.com
- War with Iran remains broadly unpopular

---

## 3. GALLUP POLLS

### A. "Government Still Leads as Nation's Top Problem"
**Date:** March 3, 2026 | **Source:** news.gallup.com/poll
- **Question:** "What do you think is the most important problem facing this country today?" (open-ended)
- Government/Poor leadership cited as the top problem
- *(Gallup uses JavaScript-rendered content; topline percentages could not be extracted programmatically. The article is accessible only with JS enabled.)*

### B. "Healthcare Reclaims Top Spot Among U.S. Domestic Worries"
**Date:** March 31, 2026 | **Source:** news.gallup.com/poll
- Healthcare reclaims the #1 spot among domestic worries

### C. "The World's Most Important Problem: What People Need Leaders to Hear in 2026"
**Date:** February 4, 2026 | **Source:** www.gallup.com
- Global survey: Economic concerns dominate worldwide
- But in the U.S., different problems (government, healthcare) top the list
- **Question:** "What do you think is the most important problem facing the world today?"

### D. "Disapproval of Congress Ties Record High at 86%"
**Date:** April 22, 2026 | **Source:** news.gallup.com/poll
- Congress disapproval: **86%** (ties record high)
- Congress approval: **15%**

### E. "Americans' Economic Confidence Drops in April"
**Date:** April 23, 2026 | **Source:** news.gallup.com/poll
- **Gallup Economic Confidence Index** declined in April 2026

### F. "Affordability Still Dominates Americans' Financial Worries"
**Date:** April 28, 2026 | **Source:** news.gallup.com/poll
- Cost of living/affordability remains the top financial worry

### G. "Americans Predict Challenging 2026 Across 13 Dimensions"
**Date:** January 5, 2026 | **Source:** news.gallup.com/poll
- Americans predict a challenging year across 13 dimensions

### H. "Top U.S. Foreign Policy Priority: National Security"
**Date:** March 5, 2026 | **Source:** news.gallup.com/poll
- National security ranked as top foreign policy priority

### I. "The Economy is the World's Most Important Problem, but not America's"
**Date:** February 4, 2026 | **Source:** Axios (citing Gallup)
- Gallup's global survey: economy is #1 problem worldwide
- But in the U.S., government/leadership is the top-cited problem

### J. "Americans' Views on the Nation's Global Image and Power"
**Date:** March 5, 2026 | **Source:** news.gallup.com/poll
- Americans' views on U.S. global standing

---

## 4. ROPER CENTER iPOLL

**URL:** https://ropercenter.cornell.edu/ipoll
- Fully JavaScript-rendered single-page application (React-based)
- Requires authentication/subscription for full access to question-level data
- Could not extract data programmatically without a browser rendering engine
- The Roper Center archives polling data from over 100 organizations, including Gallup, YouGov, Ipsos, and Pew
- Public-facing homepage loads but data requires institutional login or individual subscription

---

## 5. METHODOLOGY NOTES

- **Gallup** site (news.gallup.com) is fully JavaScript-rendered; direct HTML extraction returns only navigation/shell content. Data is loaded client-side.
- **YouGov** (today.yougov.com) is an Angular SPA; article content is loaded via API calls after page render. Textise proxy showed URL redirects between article slugs.
- **Ipsos** (ipsos.com) had the most accessible content — article text was embedded in server-rendered HTML.
- **Roper Center** (ropercenter.cornell.edu/ipoll) is a React SPA requiring institutional login for data.
- **Google News RSS** was effective for discovering relevant polling articles and identifying their sources/dates.

## 6. KEY THEMATIC FINDINGS

| Theme | Source | Finding |
|-------|--------|---------|
| Most Important Problem | Ipsos (Mar 2026) | Economy (16%), War/conflicts (14%) |
| Most Important Problem | Gallup (Mar 2026) | Government/leadership leads |
| Most Important Problem | YouGov (Apr 2026) | Inflation #1 |
| Trump Approval | Ipsos (Mar-May 2026) | 36% overall, trending down |
| Trump on Cost of Living | Ipsos (Mar 2026) | 25% approve, 66% disapprove |
| Iran Military Strikes | Ipsos (Mar 2026) | 35% approve, 61% disapprove |
| Economy Strength | Ipsos (Mar 2026) | 34% strong, 63% weak |
| Congress Approval | Gallup (Apr 2026) | 15% approve, 86% disapprove |
| Wrong Direction | Ipsos/Post/ABC (May 2026) | 2/3 say wrong direction |
