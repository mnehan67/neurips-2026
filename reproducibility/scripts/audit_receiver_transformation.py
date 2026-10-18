#!/usr/bin/env python3
"""Verify final control-panel and held-out receiver-map values from frozen outputs."""
from pathlib import Path
import pandas as pd
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/"results"/"receiver_transformation_v1"

EXPECTED={
    "qwen3_8b": dict(final_layer=35, receiver=0.316284, global_=0.086007, wrong=-0.023295),
    "mistral_7b": dict(final_layer=31, receiver=0.241280, global_=0.109253, wrong=0.028082),
}

for model in ["qwen3_8b","mistral_7b"]:
    folder=BASE/model
    pred=pd.read_csv(folder/"predictor_summary.csv")
    maps=pd.read_csv(folder/"receiver_map_summary.csv")
    e=EXPECTED[model]
    last=maps[maps["downstream_layer"].eq(e["final_layer"])].set_index("method")
    vals={
        "receiver":float(last.loc["receiver_map","mean_cosine"]),
        "global":float(last.loc["global_map","mean_cosine"]),
        "wrong":float(last.loc["wrong_receiver_map","mean_cosine"]),
    }
    for key,ref in [("receiver",e["receiver"]),("global",e["global_"]),("wrong",e["wrong"])]:
        if abs(vals[key]-ref)>5e-6:
            raise SystemExit(f"{model}: {key} mismatch: {vals[key]} vs {ref}")

    fisher=pred[pred["predictor"].eq("Fisher")].iloc[0]
    atp=pred[pred["predictor"].eq("AtP_toplogp")].iloc[0]
    rel=pred[pred["predictor"].eq("relative_norm")].iloc[0]
    print(f"\n{model}")
    print(f"  Fisher median within-delta rho : {fisher['median_within_displacement_spearman']:.6f}")
    print(f"  AtP-top median within-delta rho: {atp['median_within_displacement_spearman']:.6f}")
    print(f"  rel-norm median within-delta rho: {rel['median_within_displacement_spearman']:.6f}")
    print(f"  final receiver-map cosine      : {vals['receiver']:.6f}")
    print(f"  final global-map cosine        : {vals['global']:.6f}")
    print(f"  final wrong-receiver cosine    : {vals['wrong']:.6f}")

    boot=pd.read_csv(folder/"final_layer_bootstrap.csv")
    print("  final-layer bootstrap:")
    if model=="qwen3_8b":
        for _,r in boot.iterrows():
            print(f"    {r['comparison']}: {r['mean_difference']:.6f} [{r['ci95_low']:.6f}, {r['ci95_high']:.6f}]")
    else:
        for _,r in boot.iterrows():
            print(f"    {r['comparison']}: {r['mean']:.6f} [{r['lo']:.6f}, {r['hi']:.6f}]")

print("\nReceiver-transformation frozen-output audit passed.")
