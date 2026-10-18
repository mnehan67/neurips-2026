# Fresh C4 Qwen3-8B and Mistral-7B results

This directory contains the successful MLP targets from the frozen fresh-C4 crossed experiment reported in the paper (Appendix D).

## Reported models

- `Qwen/Qwen3-8B` at layers 7, 14, 21, and 26.
- `mistralai/Mistral-7B-v0.3` at layers 6, 12, 19, and 23.

Each target uses 64 contexts and all 4032 directed non-self host-donor pairs. The approximately 0.40-depth targets additionally contain the wrong-evaluation, epsilon, exact-dose, future-propagation, natural-direction control, and local donor-bank selection audits.

`FRESH_C4_PROTOCOL.json` records the frozen settings and the SHA-256 of the source-document pool. Full raw C4 documents are not redistributed in this public artifact. The `models/*/document_hashes.json` files retain the hashes of the selected documents.

Run

```bash
python analysis/audit_fresh_c4_multibillion.py
python analysis/audit_joint_context_permutation.py
python analysis/audit_representative_and_failure_cases.py
```

from the repository root to verify the headline values, joint context-label permutation sensitivity analysis, representative-host rule, and largest rank-disagreement cases from the packaged outputs.

Run

```bash
python analysis/make_fresh_c4_figures.py
```

to regenerate the workshop result figures and supplementary Q-vs-K density plot.
