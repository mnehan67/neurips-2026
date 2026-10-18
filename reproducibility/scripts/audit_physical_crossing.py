#!/usr/bin/env python3
"""Recompute the direct physical crossed-receiver headline numbers.

This script is CPU-only. It verifies:
  * pooled Fisher / q_p2 rank correlations,
  * per-displacement alternative-receiver rank correlations,
  * post-hoc rank residual association after fixed-displacement + receiver effects.

The post-hoc fixed-effect analysis is intentionally labeled as such in the paper.
"""
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import rankdata, spearmanr

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "results" / "physical_crossing_v3" / "primary"
OUT = ROOT / "results" / "physical_crossing_v3" / "summary" / "PHYSICAL_CROSSING_PRIMARY_RECOMPUTED.csv"

FILES = [
    ("mistral", 1, 12, "mistral_b1_layer12_cross_receiver_physical.csv"),
    ("mistral", 2, 12, "mistral_b2_layer12_cross_receiver_physical.csv"),
    ("mistral", 3, 12, "mistral_b3_layer12_cross_receiver_physical.csv"),
    ("qwen", 1, 14, "qwen_b1_layer14_cross_receiver_physical.csv"),
    ("qwen", 2, 14, "qwen_b2_layer14_cross_receiver_physical.csv"),
    ("qwen", 3, 14, "qwen_b3_layer14_cross_receiver_physical.csv"),
]


def two_way_residual_rank(df, value_col, max_iter=200, tol=1e-12):
    """Rank-transform then project out additive delta_id and receiver effects."""
    r = rankdata(df[value_col].to_numpy(float), method="average")
    r = r - r.mean()
    sd = r.std()
    if sd > 0:
        r = r / sd

    d_raw = df["delta_id"].to_numpy(int)
    k_raw = df["receiver"].to_numpy(int)
    _, d = np.unique(d_raw, return_inverse=True)
    _, k = np.unique(k_raw, return_inverse=True)
    nd, nk = d.max() + 1, k.max() + 1
    dc = np.bincount(d, minlength=nd).astype(float)
    kc = np.bincount(k, minlength=nk).astype(float)
    res = r.copy()
    for _ in range(max_iter):
        dm = np.bincount(d, weights=res, minlength=nd) / np.maximum(dc, 1)
        res -= dm[d]
        km = np.bincount(k, weights=res, minlength=nk) / np.maximum(kc, 1)
        res -= km[k]
        if max(np.max(np.abs(dm)), np.max(np.abs(km))) < tol:
            break
    return res


def per_delta_alt_rhos(df, pred):
    vals = []
    positive = 0
    for _, x in df.groupby("delta_id", sort=True):
        # The first receiver recorded for each displacement is its origin host.
        # Use the explicit origin_host column rather than relying on row order.
        alt = x[x["receiver"].astype(int) != x["origin_host"].astype(int)]
        if len(alt) < 4:
            continue
        rho = spearmanr(alt[pred], alt["kl_cross"]).statistic
        if np.isfinite(rho):
            vals.append(float(rho))
            positive += int(rho > 0)
    return np.asarray(vals), positive / max(len(vals), 1)


rows = []
for model, bucket, layer, name in FILES:
    df = pd.read_csv(DATA / name)
    needed = {"delta_id", "origin_host", "receiver", "kl_cross", "q_fisher", "q_p2"}
    missing = needed - set(df.columns)
    if missing:
        raise RuntimeError(f"{name}: missing columns {sorted(missing)}")

    row = {"model": model, "bucket": bucket, "layer": layer, "n_rows": len(df)}
    for pred in ("q_fisher", "q_p2"):
        rho = spearmanr(df[pred], df["kl_cross"]).statistic
        vals, pos = per_delta_alt_rhos(df, pred)
        yp = two_way_residual_rank(df, pred)
        yk = two_way_residual_rank(df, "kl_cross")
        resid = float(np.corrcoef(yp, yk)[0, 1])
        row[f"{pred}_pooled_rho"] = float(rho)
        row[f"{pred}_median_alt_rho"] = float(np.median(vals))
        row[f"{pred}_mean_alt_rho"] = float(np.mean(vals))
        row[f"{pred}_positive_delta_fraction"] = float(pos)
        row[f"{pred}_rank_resid_rho"] = resid
    rows.append(row)

out = pd.DataFrame(rows)
out.to_csv(OUT, index=False)
pd.set_option("display.max_columns", None)
print(out.to_string(index=False, float_format=lambda x: f"{x:.6f}"))
print(f"\nWrote {OUT.relative_to(ROOT)}")
