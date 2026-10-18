# Exact FP32 downstream-suffix JVP audit

Numerical audit of the finite-difference Fisher score used in the crossed experiments (paper Appendix D.12.2).

## What was run
- Notebook: `notebooks/kaggle_2xT4_exact_fp32_suffix_jvp_audit.ipynb` (Kaggle, 2x NVIDIA T4, 16 GB each).
- Models / layers: Qwen3-8B layer 14; Mistral-7B-v0.3 layer 12; 64-token contexts; seed 26091016.
- Cases: the first 16 displacements of the 96x8 control panel, each at receiver 0 (same host, donor, and
  receiver context IDs as `results/receiver_transformation_v1/{model}/displacements.csv` / `receivers.csv`).
- Natural states up to and including layer l (host/donor MLP outputs, receiver layer-l output) are produced
  with the FP16 model and cached. The downstream suffix (layers l+1..L, final norm, LM head) is evaluated in
  FP32 with TF32 disabled, split across the two GPUs.
- Exact JVP by automatic differentiation through the FP32 suffix; centered finite differences at eps=0.075
  and eps/2 and their Richardson combination on the same suffix.
- Runtime was not recorded.

## Files
- `*_FP32_suffix_exact_JVP.csv`, `ALL_MODELS_FP32_suffix_exact_JVP.csv`, `FP32_suffix_exact_JVP_summary.csv`,
  `AUDIT_METADATA.json`, `PAPER_READY_SUMMARY.txt` — notebook outputs.
- `FP16_VS_FP32_SUFFIX_SUMMARY.csv`, `FP16_VS_FP32_SUFFIX_PER_PAIR.csv` — written by
  `analysis/verify_fp32_suffix_jvp_audit.py`: context checks, recomputed FP32 summary, and the comparison of the
  FP16 finite-difference scores for the same 16 control-panel cases
  (`results/receiver_transformation_v1/{model}/finite_difference_richardson.csv`, computed with the estimator
  used in the crossed experiments) with the exact FP32 suffix scores. FP16 and FP32 metrics are kept in
  separate columns.

## What it establishes / does not establish
- FP32 centered differences at eps=0.075 reproduce exact FP32 suffix JVPs (median cosine 1.0000; Spearman 1.000
  between Fisher scores; median relative Q error 0.21% Qwen, 0.20% Mistral; max 0.82% / 0.37%): truncation
  error at this step is negligible on these directions.
- The FP16 scores for the same 16 cases agree less closely with the exact FP32 scores (Spearman 0.785 / 0.544;
  median relative difference 21.6% / 26.7%). On this audit panel, the pattern is consistent with
  finite-precision effects dominating the observed discrepancy rather than centered-difference truncation.
- It is not a full-model FP32 JVP (upstream states are FP16) and does not make the FP16 scores numerically
  exact. It varies displacement direction at a fixed receiver and does not reproduce the primary
  within-displacement receiver-ranking statistic.
