# California Ballot Measure Data Sources
**Extracted:** May 4, 2026

## UC Law San Francisco — CA Ballot Propositions (repository.uclawsf.edu/ca_ballot_props)
- **Articles found:** 110 proposition articles, 110 initiative articles
- **Coverage:** 1911-2020
- **Content:** Full ballot language (titles + summaries), sample PDFs of voter pamphlets
- **Access:** Digital Commons platform, fully scrapeable
- **Each article URL:** `https://repository.uclawsf.edu/ca_ballot_props/{ID}`
- **Example IDs:** 1379 (2020 Primary guide), 1380-1392 (2020 propositions), 1370 (children's health bonds)
- **Initiatives:** `https://repository.uclawsf.edu/ca_ballot_inits/{ID}`

## California Secretary of State (sos.ca.gov)
- **Ballot measures portal:** `sos.ca.gov/elections/ballot-measures/` (60 KB, accessible)
- **Election results:** `sos.ca.gov/elections/prior-elections/statewide-election-results/` (71 KB, accessible)
- **Historical resources:** `sos.ca.gov/elections/ballot-measures/resources-and-historical-information/`
- **Format:** Direct HTML, no bot protection
- **Coverage:** Statewide results 1990+, ballot measures 1911+

## Extraction Notes
- UC Law SF: Digital Commons uses pagination, each article landing page has PDF download link
- CA SoS: Direct HTML, standard table formatting on results pages
- Both sources are freely accessible with no Cloudflare/WAF
