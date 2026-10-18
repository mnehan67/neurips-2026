#!/usr/bin/env python3
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
FRESH = ROOT / "results" / "fresh_c4_qwen3_8b_mistral7b"
TARGETS = {
    "Qwen3-8B": FRESH / "Qwen_Qwen3-8B__mlp__L14__r0.400" / "dose_curves.csv",
    "Mistral-7B": FRESH / "mistralai_Mistral-7B-v0.3__mlp__L12__r0.387" / "dose_curves.csv",
}
rows = []
for model, path in TARGETS.items():
    d = pd.read_csv(path)
    for lam in [0.10, 0.25, 0.50, 0.75, 1.00]:
        rho = d[["q_local", f"kl_{lam}"]].apply(np.log1p).corr(method="spearman").iloc[0, 1]
        rows.append({"model": model, "lambda": lam, "spearman_q_vs_kl": float(rho)})
observed = pd.DataFrame(rows)
expected = pd.read_csv(FRESH / "Q_VS_DOSE_CORRELATIONS.csv")
if not np.allclose(observed["spearman_q_vs_kl"], expected["spearman_q_vs_kl"], atol=1e-10, rtol=0):
    raise SystemExit("Dose-correlation mismatch")
print("Q-vs-dose audit passed.")
print(observed.to_string(index=False))
