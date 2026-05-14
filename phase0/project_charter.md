# Project Charter — Political Messaging Dataset, Fine-Tuning & Simulated Electorate Evaluation

## 1. Executive Summary

**Project Title:** US Political Messaging & Simulated Electorate Evaluation System

**Objective:** Build an end-to-end system that (1) aggregates high-quality datasets on US political issue polling, message testing, and referendum outcomes, (2) fine-tunes a language model to generate politically effective messages, and (3) evaluates messages using a simulated electorate of demographic persona LLM swarms calibrated to real-world outcomes.

**Owner:** Logan

**Timeline:** 20–30 weeks total (Phase 0–4)

---

## 2. Success Metrics

### Dataset KPIs
| Metric | Target | Measurement |
|--------|--------|-------------|
| Issue polling coverage | 6,000+ rows, 1972–2026 | Row count, year range |
| Message testing coverage | 600+ rows, 2018–2026 | Row count, source diversity |
| Ballot measure coverage | 500+ rows, 2008–2025 | Row count, state coverage |
| State coverage (ballot measures) | 25+ states | Unique states in referendums.csv |
| Topic diversity | 20+ topics per table | Unique topic values |
| Provenance completeness | 100% rows with source + date | Non-null source + date fields |
| Duplicate rate | < 1% | Duplicate detection pass |
| Source diversity | 8+ independent sources | Unique source organizations |

### Model KPIs *(for Phase 2+)*
- Popularity prediction correlation ≥ 0.5 vs held-out outcomes
- Safety violation rate < 1%
- Message quality rubric scores above baseline

### Swarm KPIs *(for Phase 3+)*
- Calibration correlation ≥ 0.6 with known message-test results
- Run-to-run stability variance < 0.05
- Fairness parity across demographic subgroups

---

## 3. Scope

### In Scope
- US electorate issue polling (national and state-level)
- US political message A/B testing with exact wording and measured outcomes
- US statewide ballot measures and referendums
- Data extraction from publicly accessible web sources, RSS feeds, PDFs, and academic datasets
- Fine-tuning language models on politically-relevant text generation
- Simulated electorate evaluation using LLM persona swarms
- Automated quality validation and data provenance tracking

### Out of Scope (Phase 0–1)
- Live deployment for real-time persuasion
- Individual-level voter data or microtargeting
- Non-US political data
- Paid/subscription data sources
- Social media scraped content without structured polling methodology

---

## 4. Deliverables by Phase

### Phase 0 — Program Setup
- [x] Repository conventions and directory structure
- [x] Data schemas (messages, issues, referendums)
- [ ] Project charter with success metrics ✅
- [ ] Data versioning rules
- [ ] Experiment registry template
- [ ] Risk register
- [ ] Compliance checklist

### Phase 1 — Data Compilation & Harmonization
- [ ] Unified dataset v1.0
- [ ] Source inventory with licensing
- [ ] Ingestion pipelines for all sources
- [ ] Normalized taxonomies
- [ ] Entity resolution (canonical IDs)
- [ ] Data quality report
- [ ] Provenance manifest

### Phase 2 — Baseline Modeling & Fine-Tuning Pipeline *(future)*
### Phase 3 — Simulated Electorate Framework *(future)*
### Phase 4 — Iterative Optimization Loop *(future)*

---

## 5. Governance

### Roles
- **Data Engineering:** Ingestion, normalization, quality validation
- **Applied ML:** Fine-tuning, optimization loops, evaluation
- **Political Science/Survey Methods:** Taxonomy validity, measurement quality
- **Governance:** Compliance, risk monitoring, ethical review

### Decision Rights
- Schema changes require documented rationale and impact assessment
- Adding new data sources requires licensing check
- Any model output intended for external use requires human review

### Communication
- Status updates delivered via session summaries
- Dataset snapshots versioned and documented
- Quality issues tracked in data quality reports
