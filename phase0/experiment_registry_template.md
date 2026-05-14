# Experiment Registry Template

## Purpose
Track each fine-tuning run, data snapshot, and evaluation cycle. Every experiment gets a unique ID and permanent record.

## Experiment ID Format
```
EXP_<YYYYMMDD>_<##>
```

## Registry Entry Template

```yaml
experiment_id: EXP_20260508_01
date: 2026-05-08
status: planned | running | completed | failed

## Data Snapshot
data_version: v1.0.0
data_freeze_date: 2026-05-08
train_rows: <count>
eval_rows: <count>
data_notes: <sources used, filters applied>

## Model
base_model: <model name, e.g., llama-3-8b>
fine_tuning_method: sft | dpo | ppo | grpo
checkpoint_path: <path>
hyperparameters:
  learning_rate: <float>
  batch_size: <int>
  epochs: <int>
  lora_rank: <int>
  lora_alpha: <float>
  warmup_steps: <int>
  seed: <int>

## Task Configuration
task_format: <e.g., message_generation, popularity_prediction>
input_format: <audience_profile + issue_context + goal>
output_format: <generated_message | popularity_score>
training_signal: <e.g., preference_effect, support_pct, binary_win>

## Evaluation Results
eval_metrics:
  popularity_correlation: <float>
  relevance_score: <float>
  safety_violation_rate: <float>
  readability_score: <float>
  toxicity_score: <float>
  policy_alignment_score: <float>

## Swarm Evaluation (Phase 3+)
swarm_calibration_correlation: <float>
swarm_stability_variance: <float>
subgroup_fairness: <dict>

## Artifacts
model_registry_path: <wandb/hf link>
dataset_snapshot_url: <path>
eval_results_path: <path>

## Notes
notes: <free text about what was learned, issues, anomalies>
```

## Storage
- Registry stored in `experiments/` directory as individual YAML files
- Alternatively, stored as a CSV tracking table: `experiments/registry.csv`
- For later phases, integrate with Weights & Biases or MLflow
