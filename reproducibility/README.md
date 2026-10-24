# Reproducing the crossed-receiver study

Paper: **Transformer MLP Transplants Depend on the Receiving State** (Muhammed Nehan; NeurIPS 2026 NewInML & MusIML Workshops).

This directory includes GPU experiment notebooks, frozen output tables, and independent CPU audits. **CPU verification** checks the released outputs without downloading models. **Full experiment regeneration** requires GPU resources, model checkpoints, and the documented datasets.

## Quick verification (CPU; no model downloads)

From the `reproducibility/` directory:

```bash
python -m pip install -r requirements.txt
python scripts/audit_final_public_results.py
python scripts/verify_fp32_suffix_jvp_audit.py --audit results/fp32_suffix_jvp_audit
python scripts/check_website_assets.py
python scripts/make_paper_figures.py --repo . --out figures
```

`audit_final_public_results.py` runs four components: physical crossing, rank-KL variance decomposition, receiver transformations, **and the new crossed stress tests**. Individual tests can also be run directly (for example `python scripts/audit_crossed_stress_tests.py`). The `figures/` output directory is ignored by Git; do not commit compiled paper PDFs or generated figure files when they can be regenerated.

## Which experiment produced which result?

| Experiment | Frozen results | Source notebook / script |
| --- | --- | --- |
| Fixed MLP update crossed with natural receivers, Qwen3-8B and Mistral-7B, B1/B2/B3 | `results/physical_crossing_v3/` | `notebooks/KAGGLE_T4X2_receiver_causal_replication_V3.ipynb` |
| Attribution/geometry baselines, downstream footprints, receiver-specific rank-16 maps, and 72/24 split | `results/receiver_transformation_v1/` | `notebooks/qwen_receiver_transformation_kaggle_t4x2.ipynb`, `notebooks/mistral_receiver_transformation_kaggle_t4x2.ipynb` |
| Crossed FP32 downstream-suffix stress tests on 16 B1 displacements × 15 alternative receivers/model | `results/crossed_stress_tests_v1/` | `notebooks/kaggle_2xT4_crossed_reviewer_stress_tests.ipynb` and `scripts/audit_crossed_stress_tests.py` |
| Corrected held-out receiver-only fragility and residual association (72 train / 24 held-out displacements) | `results/crossed_stress_tests_v1/corrected_fragility/` | Frozen outputs and `scripts/audit_crossed_stress_tests.py` |
| Additional FP32-suffix JVP numerical comparison | `results/fp32_suffix_jvp_audit/` | `notebooks/kaggle_2xT4_exact_fp32_suffix_jvp_audit.ipynb`, `scripts/verify_fp32_suffix_jvp_audit.py` |
| Ordinary host–donor transplants, alternatives, teacher-forced continuation | `results/fresh_c4_qwen3_8b_mistral7b/` | `notebooks/reproduce_fresh_c4_qwen_mistral.ipynb` |
| Pythia-70M ordinary-transplant replication across six pretrained runs | `results/pythia_six_run/` | `notebooks/reproduce_pythia_confirmatory.ipynb` |
| KL effect-spread summary | `results/derived/` | `scripts/derived_stats.py` |

## Key numerical summaries

- Fixed displacement, 31 alternative receivers (buckets B2/B3): median max/min exact-KL ratios exceed **1,000×**; these are *within-update extrema*, not typical randomly sampled receiver pairs. Raw numbers are in `results/derived/crossed_receiver_effect_spread.csv`.
- Fisher ranking, median within-displacement Spearman (B1/B2/B3): **Qwen: 0.871/0.872/0.858; Mistral: 0.911/0.928/0.928**. Three disjoint data buckets in each model are not six independent model trainings.
- Exact FP32 downstream-suffix JVP versus **original frozen full-dose KL**: **0.884 (Qwen), 0.930 (Mistral)**. The newer crossed-stress CSVs also contain comparisons with *FP32-recomputed downstream-suffix full-dose KL*; consult the exact metric names to distinguish them.
- FP16 versus exact-FP32 Fisher **receiver rankings**: **0.977 / 0.988**. At 0.1× intervention dose versus full-dose KL rank: **0.900 / 0.938**.
- Corrected held-out receiver-only fragility: **0.595 / 0.845**; Fisher: **0.738 / 0.893**. Bootstrap intervals for the paired Fisher-minus-fragility advantage include zero. Pooled held-out residual Fisher–KL association: **0.379 / 0.489**.
- Final-layer held-out cosine of receiver-specific maps: **0.316 / 0.241**, compared with global maps **0.086 / 0.109**. The maps use previously observed receivers and unseen displacements.

## Figures

```bash
python scripts/make_paper_figures.py --repo . --out figures
```

The generated PDFs include `fig2_crossed_hexbin.pdf`, `fig3_receiver_maps.pdf`, the dose/teacher-forcing/trajectory plots, and `figD_within_displacement_receiver_ranks.pdf` (**supplementary Figure 5**). Figure 5 uses the first three **fixed displacement IDs 0, 1, 2** from bucket B2 for each model, selected by ID (not performance), ranks 31 *alternative* receivers by local Fisher and exact KL, and excludes the original host anchor. Its six per-displacement Spearman correlations are computed directly from the frozen CSVs. The website's PNG is rendered from the camera-ready Figure 5 PDF supplied with the final paper source.

## Numerical provenance and limitations

- Large-model runs used Qwen3-8B and Mistral-7B-v0.3 with frozen FP16 weights. Inputs are deterministic 64-token C4 validation contexts assigned to disjoint buckets; primary sites are layers 14 and 12.
- The FP32 audits recompute a downstream suffix from **FP16-cached natural prefix states**. They validate local directional responses and crossed receiver ordering; they are not a full-model FP32 rerun. The exact experimental controls and fields are in `results/crossed_stress_tests_v1/README.md` and each model's `RUN_METADATA.json`.
- `corrected_fragility/HELDOUT_FRAGILITY_CORRECTED_SUMMARY.csv` supersedes an earlier cache-collided notebook fragility summary. The latter is deliberately **not** included in this release.
- The PCA/5-NN naturality proxy is descriptive and does **not** prove activation manifold membership. Teacher-forced continuation is **not** free generation. No new steering algorithm is proposed.
- The paper's rank-16 receiver maps are trained for a fixed set of receivers on 72 updates and tested on 24 held-out updates. They do not demonstrate transfer to unseen receivers.

## Environment and licenses

CPU dependency versions are pinned in `requirements.txt`. GPU setup requires `requirements-gpu.txt`, compatible PyTorch/Transformers, and the model checkpoints, dataset, and hardware documented by the notebooks. Model revisions and third-party notices are in `MODEL_REVISIONS.md` and `THIRD_PARTY_NOTICES.md`.
