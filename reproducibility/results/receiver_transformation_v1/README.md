# Receiver-transformation and final control-panel results

This directory contains the public frozen outputs for the final 96-displacement × 8-receiver experiments in Qwen3-8B (layer 14) and Mistral-7B-v0.3 (layer 12).

## Per-model files

- `predictor_summary.csv` — pooled, median within-displacement, positive-fraction, and residual-rank correlations for Fisher and alternative predictors.
- `control_panel_rows.csv` — row-level 96×8 physical interventions used by the stronger-baseline analysis.
- `layerwise_causal_trajectories.csv` — original-host vs receiver causal-effect fidelity/gain/rewrite across downstream layers.
- `receiver_map_benchmark.csv` — held-out map results by downstream layer and receiver.
- `receiver_map_summary.csv` — compact layer × method averages used by the paper figure.
- `receiver_map_clustered_se.csv` — curve means and standard errors computed across the 24 held-out displacement units after averaging receivers.
- `final_layer_bootstrap.csv` — displacement-clustered bootstrap comparison of receiver-specific vs global/wrong/identity/gain baselines.
- `finite_difference_richardson.csv` — epsilon-halving and Richardson numerical audit.
- `train_test_split.csv` — frozen 72/24 displacement split.
- `displacements.csv`, `receivers.csv` — intervention metadata.
- `receiver_map_per_case.csv` — available for Mistral because the final replication notebook saved per-test-displacement scores directly.

The large Qwen hidden-state mmap arrays are intentionally not included because individual files exceed ordinary Git hosting limits. The public artifact retains the row-level control data, layerwise trajectories, map summaries/benchmarks, bootstrap output, and clustered-SE table needed to reproduce the reported paper statistics and figures.

## Headline final-layer values

| Model | Receiver-specific | Global | Wrong receiver | Receiver − global |
|---|---:|---:|---:|---:|
| Qwen3-8B | 0.316 | 0.086 | -0.023 | +0.230 [0.205, 0.256] |
| Mistral-7B | 0.241 | 0.109 | 0.028 | +0.132 [0.108, 0.155] |

The reported improvement is directional cosine prediction. Normalized vector-reconstruction error improves less, so the paper interprets the result as a reusable receiver-specific **component**, not a complete transformation law.
