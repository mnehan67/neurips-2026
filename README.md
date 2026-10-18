# Transformer MLP Transplants Depend on the Receiving State

NeurIPS 2026 Workshops — NewInML & MusIML

Muhammed Nehan — Ajman University

Project page: https://mnehan67.github.io/neurips-2026/

## Overview

Activation patching and steering move internal updates between forward passes and often treat a moved update as
if it carried a portable effect. We test this with a crossed-receiver design: a natural transformer MLP
displacement is computed once, frozen, and added unchanged to many natural receiver states of Qwen3-8B and
Mistral-7B. The same displacement has strongly receiver-dependent next-token effects, which an established
receiver-local Fisher score ranks (median within-displacement Spearman 0.858–0.928). The receiver also changes
the direction of the downstream causal effect, and receiver-specific maps predict part of that transformation
for held-out displacements.

## Code and reproducibility

[`reproducibility/`](reproducibility/) contains:

- the experiment notebooks (crossed-receiver runs, control panel and receiver maps, ordinary transplants,
  Pythia replication, exact FP32 downstream-suffix JVP audit);
- CPU verification scripts and the figure-generation script;
- lightweight frozen CSV/JSON outputs behind the headline results.

Start with [`reproducibility/README.md`](reproducibility/README.md).

Larger frozen artifacts and the original experiment snapshot:
https://anonymous.4open.science/r/newinml-7402/

## Repository structure

```
index.html, static/          project page (GitHub Pages)
reproducibility/
  README.md                  how to verify and reproduce the results
  requirements.txt           CPU verification environment
  requirements-gpu.txt       model-level notebook environment
  scripts/                   audits, derived statistics, figure generation, JVP-audit verification
  notebooks/                 final experiment notebooks
  results/                   lightweight frozen outputs
LICENSE                      MIT license for the research code
LICENSE-SITE.md              license of the project-page source (adapted from Nerfies)
CITATION.cff                 citation metadata
```
