# Reproducing the paper

**Transformer MLP Transplants Depend on the Receiving State**
Muhammed Nehan, Ajman University. NeurIPS 2026 Workshops (NewInML and MusIML).

This directory contains the public code and lightweight frozen outputs used to verify the paper's principal
results. The verification scripts run on CPU from the frozen outputs below; no model download or GPU is needed.
The notebooks regenerate the outputs from the models (GPU required).

## Quick verification

```bash
cd reproducibility
python -m pip install -r requirements.txt

python scripts/audit_final_public_results.py          # crossed-receiver statistics, rank-KL decomposition,
                                                      # receiver-map summaries, dose curve
python scripts/verify_fp32_suffix_jvp_audit.py --audit results/fp32_suffix_jvp_audit
python scripts/derived_stats.py                       # spread of one displacement's effect across receivers
python scripts/audit_joint_context_permutation.py     # host–donor permutation test (64x63 matrices)
python scripts/make_paper_figures.py --out figures    # regenerates every data figure of the paper
```

`audit_final_public_results.py` recomputes and prints the primary within-displacement correlations
(Qwen3-8B 0.871 / 0.872 / 0.858; Mistral-7B 0.911 / 0.928 / 0.928) and the residual-rank correlations from the
row-level crossed tables. The rank-KL decomposition, the receiver-map summaries (final-layer held-out cosine
0.316 vs 0.086 global in Qwen3-8B, 0.241 vs 0.109 in Mistral-7B), and the dose correlations are compared with
the frozen tables, and the script stops with an error on any mismatch.

## Environment

- **Verification (CPU):** `requirements.txt` (pandas 2.2.3, numpy 2.3.5, scipy 1.17.0, scikit-learn 1.8.0,
  matplotlib 3.10.8).
- **Model-level notebooks (GPU):** `requirements-gpu.txt` (torch ≥ 2.5, transformers ≥ 4.55, accelerate,
  datasets). The large-model runs used Kaggle with two NVIDIA T4 GPUs (16 GB each), FP16 weights, and
  Accelerate sharding. Model revisions are listed in `MODEL_REVISIONS.md`; model and data licenses are in
  `THIRD_PARTY_NOTICES.md`.

## Experiments

| Experiment | Notebook | Frozen outputs |
|---|---|---|
| Crossed-receiver test, Qwen3-8B (layer 14) and Mistral-7B-v0.3 (layer 12): buckets B1–B3, B1 at four depths | `notebooks/KAGGLE_T4X2_receiver_causal_replication_V3.ipynb` | `results/physical_crossing_v3/` |
| 96×8 control panel: alternative predictors, equal-norm control, causal footprints, held-out receiver maps | `notebooks/qwen_receiver_transformation_kaggle_t4x2.ipynb`, `notebooks/mistral_receiver_transformation_kaggle_t4x2.ipynb` | `results/receiver_transformation_v1/` |
| Ordinary 64×63 transplant matrices: host–donor residual, wrong-state diagnostic, dose, teacher-forced continuation | `notebooks/reproduce_fresh_c4_qwen_mistral.ipynb` | `results/fresh_c4_qwen3_8b_mistral7b/` (primary depths) |
| Pythia-70M ordinary-transplant replication (six independently pretrained runs) | `notebooks/reproduce_pythia_confirmatory.ipynb` | `results/pythia_six_run/` |
| Exact FP32 downstream-suffix JVP audit (16 control-panel cases per model) | `notebooks/kaggle_2xT4_exact_fp32_suffix_jvp_audit.ipynb` | `results/fp32_suffix_jvp_audit/` |
| Spread of one displacement's effect across receivers | `scripts/derived_stats.py` | `results/derived/` |

Configurations and splits are stored next to their outputs: for example `results/physical_crossing_v3/summary/config.json`,
`results/receiver_transformation_v1/*/config.json` and `train_test_split.csv`, and
`results/fresh_c4_qwen3_8b_mistral7b/FRESH_C4_PROTOCOL.json`.

## Frozen outputs

`results/` holds only the CSV, JSON, and text outputs needed to verify the headline results and regenerate
the figures. For the Qwen3-8B control panel, the frozen bootstrap and standard-error summaries are included,
but per-held-out-displacement map scores are not available (they are included for Mistral-7B).

## Larger artifact

Larger frozen artifacts and the original experiment snapshot are hosted separately:
https://anonymous.4open.science/r/newinml-7402/

That snapshot includes, for example, the 65,280-pair Mistral ordinary-transplant matrix, the ordinary matrices
at all four depths, and the frozen Pythia token-ID inputs. This GitHub repository provides the final public
code, verification scripts, and lightweight outputs, including the final control-panel and numerical-audit
results.

## Scope

- The Pythia-70M result is an ordinary-transplant replication, not a crossed-receiver replication.
- The numerical audit is an exact FP32 downstream-suffix JVP: natural states come from the FP16 pipeline and
  only the downstream suffix is recomputed in FP32. It is not a full-model FP32 JVP, and it varies the
  displacement direction at one fixed receiver rather than replicating the receiver-ranking statistic.
- Teacher-forced continuation is not free generation.
- The study is diagnostic; it proposes no steering method.
