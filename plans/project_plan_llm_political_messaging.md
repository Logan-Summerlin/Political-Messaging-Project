# Project Plan: Political Messaging Dataset, Fine-Tuning, and Simulated Electorate Evaluation

## 1) Objective and Scope

### Objective
Build an end-to-end system that:
1. Aggregates high-quality datasets on political issues, policy preferences, message testing, and statewide referendum outcomes.
2. Fine-tunes a language model to generate political messages/ads aligned with voter popularity signals.
3. Evaluates generated messages using a simulated electorate made of demographic persona LLM swarms.
4. Iteratively improves model outputs via repeated train → generate → evaluate cycles.

### Scope Boundaries
- Focus on U.S. electorate and U.S. statewide referendums.
- Build for research and measurement; do not deploy for real-time persuasion without additional policy/legal review.
- Prioritize traceability, reproducibility, and bias/fairness instrumentation from day one.

---

## 2) Guiding Principles

- **Data provenance first:** every record must have source metadata and date coverage.
- **Causal humility:** treat outputs as predictive/correlative, not causal truth.
- **Evaluation over intuition:** message quality is based on measured outcomes.
- **Safety and governance:** include abuse-prevention, compliance, and red-team checks as required gates.
- **Reproducibility:** all pipelines are deterministic, versioned, and rerunnable.

---

## 3) Phase Roadmap

## Phase 0 — Program Setup (1–2 weeks)

### Goals
- Establish repository conventions, data contracts, experiment tracking, and governance requirements.

### Deliverables
- Project charter with success metrics.
- Data schemas and versioning rules (issues/messages/referendums).
- Experiment registry template (model version, data snapshot, hyperparameters, eval results).
- Risk register (ethical, legal, technical).

### Exit Criteria
- Team alignment on acceptance criteria for each phase.
- Signed-off compliance checklist for data usage.

---

## Phase 1 — Data Compilation & Harmonization (4–8 weeks)

### Goals
- Build a unified dataset of:
  - Issue polling / policy preferences
  - Political message testing outcomes
  - Statewide referendum metadata + vote outcomes

### Workstreams
1. **Source Inventory & Licensing**
   - Catalog all sources, coverage windows, geography, sample frames, and usage rights.
2. **Ingestion Pipelines**
   - Implement extractors/parsers for structured and unstructured sources.
3. **Normalization**
   - Standardize variables: issue taxonomy, geography, date formats, demographic keys, polling methodology.
4. **Entity Resolution**
   - Canonical IDs for issues, messages, elections, and jurisdictions.
5. **Quality & Auditing**
   - Missingness checks, duplicate detection, source disagreement flags, outlier review.

### Required Dataset Fields (minimum)
- **Issues table:** issue_id, issue_label, state/national scope, date, sample descriptors, support/oppose/priority metrics.
- **Messages table:** message_id, issue_id, treatment text, delivery channel, audience attributes, pre/post or test/control lift metrics, favorability/intent outcomes.
- **Referendums table:** referendum_id, state, year, issue mapping, ballot text summary, yes/no vote share, turnout, partisan baseline context.

### Exit Criteria
- Data quality report published with thresholds met.
- Versioned dataset snapshot (`v1.0`) with provenance manifest.

---

## Phase 2 — Baseline Modeling & Fine-Tuning Pipeline (3–6 weeks)

### Goals
- Stand up a robust training pipeline and baseline fine-tuned model for message generation.

### Workstreams
1. **Task Formulation**
   - Define input/output format: e.g., `(audience profile + issue context + goal) -> message`.
2. **Labeling Strategy**
   - Convert popularity outcomes to training signals (e.g., scalar reward bins or preference pairs).
3. **Training Data Construction**
   - Build supervised fine-tuning set with quality filters and leakage prevention.
4. **Model Training**
   - Train baseline SFT model; track hyperparameters and checkpoints.
5. **Offline Evaluation**
   - Automatic metrics: relevance, readability, policy alignment, toxicity/safety, and estimated popularity score.

### Exit Criteria
- Reproducible fine-tuning run completed.
- Baseline model exceeds predefined quality/safety thresholds.

---

## Phase 3 — Simulated Electorate (LLM Swarm) Framework (4–6 weeks)

### Goals
- Build a panel of persona LLM evaluators that represent U.S. demographic/political subgroups and score generated messages.

### Design
- Segment electorate into demographic cells (e.g., age × race/ethnicity × gender × education × region × partisan ID).
- Instantiate multiple evaluator agents per cell (e.g., 10 per subgroup as proposed).
- Weight each subgroup by real U.S. population and (optionally) turnout propensity.

### Workstreams
1. **Persona Specification**
   - Define controlled persona templates from public demographic distributions.
2. **Evaluator Prompting Protocol**
   - Standard rubric: clarity, trust, agreement, motivation, shareability, backlash risk.
3. **Aggregation Engine**
   - Weighted scoring across subgroups and uncertainty intervals.
4. **Calibration**
   - Compare swarm judgments vs known historical message-test outcomes.

### Exit Criteria
- Swarm scores show meaningful correlation with held-out real-world outcomes.
- Stability checks pass across reruns (low variance under fixed seeds/settings).

---

## Phase 4 — Iterative Optimization Loop (4–8 weeks, ongoing)

### Goals
- Close the loop by using simulated electorate feedback to improve generator performance.

### Loop Structure
1. Generate candidate messages from fine-tuned model.
2. Score via electorate swarm and safety filters.
3. Select top/contrastive candidates.
4. Build preference data and retrain (SFT + preference optimization/RL-style objective).
5. Re-evaluate on held-out historical benchmarks and swarm panel.

### MLOps Requirements
- Automated pipelines (orchestration + scheduled runs).
- Model registry with promotion gates.
- Drift monitoring (issue salience shifts, distribution shifts by election cycle).

### Exit Criteria
- Demonstrated improvement over baseline across multiple cycles.
- No regression on safety/governance gates.

---

## 4) Cross-Cutting Streams

### A) Governance, Ethics, and Legal
- Data rights verification, source terms tracking.
- Policy review for political persuasion use-cases.
- Protected-class sensitivity and disparate impact checks.
- Human review requirement before any external use.

### B) Safety and Abuse Prevention
- Filters for manipulative, hateful, or deceptive content.
- Red-team suite for adversarial prompt attacks.
- Hard-block list and escalation workflow.

### C) Experimentation and Analytics
- A/B harness for controlled comparisons.
- Confidence intervals for performance deltas.
- Dashboarding by subgroup performance and fairness metrics.

---

## 5) Suggested Team Structure

- **Data Engineering:** ingestion, normalization, data quality.
- **Applied ML:** fine-tuning, optimization loops, eval science.
- **Political Science/Survey Methods:** taxonomy validity, measurement quality.
- **Policy/Legal/Ethics:** governance gates and compliance.
- **MLOps:** automation, deployment controls, reproducibility.

---

## 6) Milestones and Timeline (Example 20–30 week plan)

- **M1 (Week 2):** Program setup complete.
- **M2 (Week 8):** Dataset `v1.0` complete and audited.
- **M3 (Week 14):** Baseline fine-tuned generator validated.
- **M4 (Week 20):** Simulated electorate calibrated and stable.
- **M5 (Week 24+):** First full optimization cycle complete; measurable gains.
- **M6 (Week 30):** Multi-cycle robustness and governance sign-off.

---

## 7) KPIs / Success Metrics

### Data KPIs
- Coverage (% of states/years/issues represented).
- Provenance completeness (% rows with source + timestamp).
- Quality thresholds (missingness, duplicate rate, disagreement flags).

### Model KPIs
- Popularity prediction correlation vs held-out outcomes.
- Message quality rubric scores (clarity/trust/persuasion proxies).
- Safety violation rate and false positive rate.

### Swarm KPIs
- Calibration correlation with known polling/message-test results.
- Run-to-run stability variance.
- Fairness parity across demographic subgroups.

---

## 8) Risks and Mitigations

- **Risk:** synthetic evaluator bias diverges from real voters.
  - **Mitigation:** continuous calibration to real message-test and polling data.
- **Risk:** data leakage / overfitting to historical campaigns.
  - **Mitigation:** strict temporal splits and provenance-aware train/test boundaries.
- **Risk:** ethical misuse.
  - **Mitigation:** governance gating, human-in-the-loop approval, restricted access.
- **Risk:** rapid opinion shifts invalidate model.
  - **Mitigation:** rolling retraining with recency weighting and drift alerts.

---

## 9) Immediate Next 14 Days (Action Plan)

1. Finalize unified schema and controlled vocabularies.
2. Lock source inventory and legal usage status.
3. Implement ingestion for top-priority sources and publish first QA report.
4. Draft baseline training spec (task format + label engineering).
5. Prototype 3–5 electorate subgroup personas and scoring rubric.
6. Define phase gates and dashboard skeleton.

---

## 10) Definition of Done (Project Level)

Project is considered successful when:
1. A versioned, auditable dataset supports issue/message/referendum analysis.
2. Fine-tuned model reliably generates high-quality political messages with measurable popularity gains on benchmarks.
3. Simulated electorate framework is calibrated to historical outcomes and stable under reruns.
4. Iterative retraining loop shows sustained improvements without safety/compliance regressions.
