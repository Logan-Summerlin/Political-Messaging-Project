# Compliance Checklist — Data Usage & Governance

## Source Data Compliance

### Check for each data source:
- [ ] Source URL documented and accessible
- [ ] Content is publicly available and freely accessible
- [ ] Terms of service checked for data collection restrictions
- [ ] No paywall or authentication required
- [ ] No login-gated content being accessed programmatically
- [ ] Attribution maintained in dataset (source field)
- [ ] Extraction date documented

### Sources Verified (Phase 0–1)
| Source | Public? | ToS Checked? | Attribution? | Status |
|--------|---------|-------------|-------------|--------|
| Blueprint Research | ✅ Free | ✅ No restrictions | source_url field | Verified |
| Navigator Research | ✅ Free | ✅ No restrictions | source_url field | Verified |
| Data for Progress | ✅ Free | ✅ No restrictions | source_url field | Verified |
| Gallup | ✅ Free (MIP data) | ✅ Public data | source_url field | Verified |
| General Social Survey | ✅ Free download | ✅ NORC open data | source & source_url | Verified |
| Pew Research Center | ✅ Free PDFs | ✅ Public data | source_url field | Verified |
| AP-NORC | ✅ Free | ✅ Public data | source_url field | Verified |
| YouGov | ✅ Free public trackers | ✅ Public data | source_url field | Verified |
| Ipsos | ✅ Free reports | ✅ Public data | source_url field | Verified |
| Wikipedia | ✅ Open access | ✅ CC license | source_url field | Verified |

## Use Case Governance

### Restrictions
- [ ] System outputs are for research and measurement only
- [ ] No real-time political persuasion without additional policy/legal review
- [ ] No individual-level targeting or microtargeting
- [ ] No generation of deceptive or manipulative content
- [ ] Human review required before any external use of model outputs

### Safety Gates (to be implemented in Phase 2+)
- [ ] Content filter for hate speech, violence, disinformation
- [ ] Red-team suite for adversarial prompt attacks
- [ ] Hard-block list for prohibited topics
- [ ] Escalation workflow for flagged content

## Reproducibility Requirements

### Each dataset snapshot must include:
- [ ] Provenance manifest with source URLs and extraction dates
- [ ] Pipeline script(s) used to generate the snapshot
- [ ] Validation report with quality checks
- [ ] Schema frozen at time of snapshot

### Each model training run must include:
- [ ] Data snapshot version used
- [ ] Full hyperparameter configuration
- [ ] Training and evaluation code version
- [ ] Evaluation results with test set

## Sign-off

| Role | Name | Date |
|------|------|------|
| Project Owner | Logan | |
| Ethics Review | (TBD) | |

*To be signed at Phase 0 completion and re-signed at each major phase gate.*
