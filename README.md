# Transformer MLP Transplants Depend on the Receiving State

**Muhammed Nehan Â· Ajman University**
**NeurIPS 2026 Workshops Â· NewInML + MusIML**

[Project website](https://mnehan67.github.io/neurips-2026/) & [MusIML paper](https://openreview.net/forum?id=tEGkJ4J3o7) & [Reproducibility guide](reproducibility/README.md)

## What the paper finds

We take the difference between two naturally occurring transformer MLP outputs, freeze that vector, and add it unchanged to many alternative receiver contexts in Qwen3-8B and Mistral-7B. Across 31 alternative receivers, the median ratio between a fixed displacement's largest and smallest effects on the native next-token distribution (forward KL divergence) exceeds 1,000-fold. A standard receiver-local Fisher quadratic ranks these effects with median within-displacement Spearman correlations of **0.858â€“0.928** across three disjoint data buckets in each model. Exact FP32 *downstream-suffix* JVP audits, alternative-explanation controls, lower-dose tests, and downstream causal-footprint analyses further characterize the dependence.

The experiment isolates **where the same update matters most**; it does not propose a new Fisher metric, a semantic decoding of MLP updates, or a new steering algorithm.

## Repository layout

| Path | Purpose |
| --- | --- |
| `index.html`, `static/css/`, `static/js/`, `static/images/` | Hosted project page, interactive receiver visualizer, and figures |
| `reproducibility/README.md` | Run instructions, frozen output layout, scope of claims |
| `reproducibility/notebooks/` | GPU research notebooks, including final crossed stress-test reproduction |
| `reproducibility/scripts/` | CPU verification and figure-generation scripts |
| `reproducibility/results/` | Published lightweight frozen CSV/JSON outputs |
| `CITATION.cff` | Citation metadata (MusIML paper as preferred reference) |

The site is intentionally static: no build system is required. GitHub Pages serves `index.html` from the repository root. To preview locally, run `python -m http.server 8000` in the repository root and open `http://localhost:8000/`.

## Verify the paper from frozen data

```bash
cd reproducibility
python -m pip install -r requirements.txt
python scripts/audit_final_public_results.py
python scripts/verify_fp32_suffix_jvp_audit.py --audit results/fp32_suffix_jvp_audit
python scripts/check_website_assets.py
python scripts/make_paper_figures.py --repo . --out figures
```

The audit suite now includes the **crossed stress tests and corrected held-out fragility outputs**. The figure script also regenerates the individual fixed-displacement receiver rank panels from B2 (Figure 5 in the supplementary appendix). For more detail see [the reproducibility README](reproducibility/README.md).

## Scope and limitations

- **Next-token behavior:** The main response metric is forward KL of the native versus intervened next-token distributions, not a benchmark of semantic steering success.
- **FP32 audit:** The numerical stress test runs the downstream suffix in FP32 starting from states cached by the FP16 prefix; it is not a full-model FP32 reproduction.
- **Receiver-specific maps:** These generalize to held-out *displacements for already observed receivers*, not to novel receivers.
- **Receiver-only baseline:** It is strong, particularly in Mistral; the bootstrap interval for Fisher's held-out advantage over this baseline crosses zero. The residual association nevertheless remains positive.
- **Lower dose:** Strong agreement of receiver ordering at 0.1Ã— does not establish that crossed activations lie on the natural manifold.

## Licensing

Research scripts and notebooks: [MIT](LICENSE). Website source: [CC BY-SA 4.0; adapted from Nerfies](LICENSE-SITE.md). Model, dataset, and third-party notices are in [`reproducibility/THIRD_PARTY_NOTICES.md`](reproducibility/THIRD_PARTY_NOTICES.md). The frozen experimental outputs and research figures are not relicensed by the code license.
