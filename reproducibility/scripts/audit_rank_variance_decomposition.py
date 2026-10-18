#!/usr/bin/env python3
"""Recompute the descriptive rank-KL additive decomposition used in Appendix D.2.

For each crossed matrix, rank-transform exact KL and compare:
  * displacement-only group means,
  * receiver-only group means,
  * additive displacement + receiver effects via alternating demeaning.

The remaining fraction is called *non-additive residual variation*. With one
observation per displacement-receiver cell it is not separately identified as a
pure interaction variance component.
"""
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import rankdata

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "results" / "physical_crossing_v3" / "primary"
OUT = ROOT / "results" / "receiver_transformation_v1" / "summary" / "rank_KL_variance_decomposition_recomputed.csv"

FILES = [
    ("Mistral-7B", "B1", "mistral_b1_layer12_cross_receiver_physical.csv"),
    ("Mistral-7B", "B2", "mistral_b2_layer12_cross_receiver_physical.csv"),
    ("Mistral-7B", "B3", "mistral_b3_layer12_cross_receiver_physical.csv"),
    ("Qwen3-8B", "B1", "qwen_b1_layer14_cross_receiver_physical.csv"),
    ("Qwen3-8B", "B2", "qwen_b2_layer14_cross_receiver_physical.csv"),
    ("Qwen3-8B", "B3", "qwen_b3_layer14_cross_receiver_physical.csv"),
]

def centered_rank(x):
    y = rankdata(np.asarray(x, float), method="average")
    return y - y.mean()

def group_prediction(y, groups):
    gvals, inv = np.unique(groups, return_inverse=True)
    sums = np.bincount(inv, weights=y, minlength=len(gvals))
    cnt = np.bincount(inv, minlength=len(gvals)).astype(float)
    means = sums / np.maximum(cnt, 1)
    return means[inv]

def additive_residual(y, a, b, max_iter=500, tol=1e-12):
    _, ai = np.unique(a, return_inverse=True)
    _, bi = np.unique(b, return_inverse=True)
    na, nb = ai.max()+1, bi.max()+1
    ac = np.bincount(ai, minlength=na).astype(float)
    bc = np.bincount(bi, minlength=nb).astype(float)
    res = y.copy()
    iterations = 0
    for iterations in range(1, max_iter+1):
        am = np.bincount(ai, weights=res, minlength=na) / np.maximum(ac, 1)
        res -= am[ai]
        bm = np.bincount(bi, weights=res, minlength=nb) / np.maximum(bc, 1)
        res -= bm[bi]
        if max(np.max(np.abs(am)), np.max(np.abs(bm))) < tol:
            break
    return res, iterations

def r2_from_residual(y, residual):
    tss = float(np.dot(y, y))
    rss = float(np.dot(residual, residual))
    return 1.0 - rss / tss

rows=[]
for model,bucket,name in FILES:
    d=pd.read_csv(DATA/name)
    y=centered_rank(d["kl_cross"])
    pred_d=group_prediction(y,d["delta_id"].to_numpy())
    pred_r=group_prediction(y,d["receiver"].to_numpy())
    r2_d=1-float(np.dot(y-pred_d,y-pred_d))/float(np.dot(y,y))
    r2_r=1-float(np.dot(y-pred_r,y-pred_r))/float(np.dot(y,y))
    resid,it=additive_residual(y,d["delta_id"].to_numpy(),d["receiver"].to_numpy())
    r2_add=r2_from_residual(y,resid)
    rows.append(dict(
        model=model,bucket=bucket,N=len(d),
        displacement_only_R2=r2_d,receiver_only_R2=r2_r,additive_R2=r2_add,
        residual_nonadditive=1-r2_add,
        unique_displacement=r2_add-r2_r,
        unique_receiver=r2_add-r2_d,
        shared_overlap=r2_d+r2_r-r2_add,
        iterations=it,
    ))
out=pd.DataFrame(rows)
out.to_csv(OUT,index=False)
print(out.to_string(index=False,float_format=lambda x:f"{x:.6f}"))
print(f"\nWrote {OUT.relative_to(ROOT)}")

# Compare against the frozen release table when present.
frozen=ROOT/"results"/"receiver_transformation_v1"/"summary"/"rank_KL_variance_decomposition.csv"
if frozen.exists():
    ref=pd.read_csv(frozen)
    numeric=[c for c in ref.columns if c not in {"model","bucket"}]
    merged=ref.merge(out,on=["model","bucket"],suffixes=("_ref","_new"))
    maxdiff=0.0
    for c in numeric:
        if c == "iterations":
            continue
        maxdiff=max(maxdiff,float(np.max(np.abs(merged[c+"_ref"]-merged[c+"_new"]))))
    print(f"Max absolute difference from frozen table: {maxdiff:.3e}")
    if maxdiff > 1e-8:
        raise SystemExit("Variance-decomposition recomputation does not match frozen release table")
