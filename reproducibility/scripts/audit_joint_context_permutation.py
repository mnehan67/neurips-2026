#!/usr/bin/env python3
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import spearmanr

ROOT = Path(__file__).resolve().parents[1]
FRESH = ROOT / "results" / "fresh_c4_qwen3_8b_mistral7b"
EXPECTED = pd.read_csv(FRESH / "JOINT_CONTEXT_PERMUTATION.csv")
RNG = np.random.default_rng(260825)

TARGETS = {
    "Qwen3-8B": FRESH / "Qwen_Qwen3-8B__mlp__L14__r0.400" / "pairs.csv",
    "Mistral-7B": FRESH / "mistralai_Mistral-7B-v0.3__mlp__L12__r0.387" / "pairs.csv",
}

def alternating_center(mat, n_iter=50):
    x = mat.copy().astype(float)
    mask = ~np.isnan(x)
    r = x.copy()
    for _ in range(n_iter):
        for i in range(r.shape[0]):
            m = mask[i]
            if m.any():
                r[i, m] -= np.nanmean(r[i, m])
        for j in range(r.shape[1]):
            m = mask[:, j]
            if m.any():
                r[m, j] -= np.nanmean(r[m, j])
    return r

rows = []
for model, path in TARGETS.items():
    df = pd.read_csv(path)
    n = 64
    k = np.full((n, n), np.nan)
    q = np.full((n, n), np.nan)
    for row in df.itertuples(index=False):
        k[int(row.host), int(row.donor)] = np.log1p(row.kl)
        q[int(row.host), int(row.donor)] = np.log1p(row.q_local)
    kr = alternating_center(k)
    qr = alternating_center(q)
    mask = ~np.isnan(kr) & ~np.isnan(qr)
    obs = float(spearmanr(kr[mask], qr[mask]).statistic)
    null = np.empty(5000)
    for b in range(len(null)):
        perm = RNG.permutation(n)
        qp = qr[np.ix_(perm, perm)]
        null[b] = spearmanr(kr[mask], qp[mask]).statistic
    p = (1 + int((null >= obs).sum())) / (len(null) + 1)
    rows.append({
        "model": model,
        "observed_pair_rho": obs,
        "n_permutations": len(null),
        "one_sided_p": p,
        "null_mean": float(null.mean()),
        "null_sd": float(null.std()),
        "null_max": float(null.max()),
    })

observed = pd.DataFrame(rows)
merged = observed.merge(EXPECTED, on="model", suffixes=("_obs", "_exp"))
for col in ["observed_pair_rho", "one_sided_p", "null_mean", "null_sd", "null_max"]:
    if not np.allclose(merged[f"{col}_obs"], merged[f"{col}_exp"], atol=1e-9, rtol=0):
        raise SystemExit(f"Mismatch in {col}")
if not np.array_equal(merged["n_permutations_obs"], merged["n_permutations_exp"]):
    raise SystemExit("Mismatch in n_permutations")
print("Joint context-role permutation audit passed.")
print(observed.to_string(index=False))
