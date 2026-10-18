#!/usr/bin/env python3
"""Verify the exact FP32 downstream-suffix JVP audit and compare it with the frozen FP16 audit.

Inputs (each may be a ZIP or a directory):
  --audit  the six audit outputs (FP32_SUFFIX_EXACT_JVP_AUDIT_RESULTS.zip, or
           results/fp32_suffix_jvp_audit/ inside the repository);
  --repo   the frozen repository (for results/receiver_transformation_v1/{model}/...).
Checks that the 16 pairs use the same host/donor/receiver contexts as the frozen
control panel, recomputes the audit summary from per-pair rows, and joins the
FP32 suffix scores with the original FP16 finite-difference scores by model + pair_id.
FP16 and FP32 metrics are kept in separate columns.

Usage: python verify_jvp_audit.py --audit <zip|dir> [--repo <zip|dir>] [--out <dir>]
"""
import argparse
import io
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

MODELS = ["qwen3_8b", "mistral_7b"]


class Source:
    def __init__(self, path, anchor):
        self.path = Path(path)
        if self.path.is_dir():
            self.z = None
            self.prefix = ""
        else:
            self.z = zipfile.ZipFile(self.path)
            hits = [n for n in self.z.namelist() if n.endswith(anchor)]
            if not hits:
                raise SystemExit(f"{anchor} not found in {self.path}")
            self.prefix = hits[0][: -len(anchor)]

    def csv(self, rel):
        data = (self.path / rel).read_bytes() if self.z is None else self.z.read(self.prefix + rel)
        return pd.read_csv(io.BytesIO(data))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--audit", required=True)
    ap.add_argument("--repo", default=".")
    ap.add_argument("--out", default=None, help="optional directory for comparison CSVs")
    a = ap.parse_args()
    audit = Source(a.audit, "FP32_suffix_exact_JVP_summary.csv")
    repo = Source(a.repo, "results/physical_crossing_v3/summary/config.json")
    summary = audit.csv("FP32_suffix_exact_JVP_summary.csv")
    per_pair, rows = [], []
    for m in MODELS:
        x = audit.csv(f"{m}_FP32_suffix_exact_JVP.csv")
        base = f"results/receiver_transformation_v1/{m}/"
        disp, recv = repo.csv(base + "displacements.csv"), repo.csv(base + "receivers.csv")
        fd16 = repo.csv(base + "finite_difference_richardson.csv")

        # 1. Context identity with the frozen control panel.
        j = x.merge(disp, left_on="pair_id", right_on="displacement_id", suffixes=("", "_frozen"))
        same_host = bool((j.host_context_id == j.host_context_id_frozen).all())
        same_donor = bool((j.donor_context_id == j.donor_context_id_frozen).all())
        r0 = recv.loc[recv.receiver_id == 0, "receiver_context_id"].item()
        same_recv = bool((x.receiver_context_id == r0).all())
        f = fd16.sort_values("pair_id")
        same_rows = bool(list(f.pair_id) == list(range(16)) and (f.displacement_id == f.pair_id).all()
                         and (f.receiver_id == 0).all())
        print(f"[{m}] N={len(x)} hosts match={same_host} donors match={same_donor} "
              f"receiver0 match={same_recv} frozen FP16 rows = displacements 0-15 @ receiver 0: {same_rows}")

        # 2. Recompute the FP32 summary from per-pair rows.
        s = summary[summary.model == m].iloc[0]
        rec = {
            "median_cos_fd075_exact": x.cos_fd075_exact.median(),
            "median_rel_qerr_fd075": x.rel_qerr_fd075.median(),
            "median_rel_qerr_half": x.rel_qerr_half.median(),
            "median_rel_qerr_rich": x.rel_qerr_rich.median(),
            "rho_Qfd075_Qexact": spearmanr(x.q_fd075, x.q_exact).statistic,
        }
        for k, v in rec.items():
            print(f"    {k}: summary={s[k]:.7f} recomputed={v:.7f}")

        # 3. Original FP16 finite-difference score vs exact FP32 suffix score.
        k = x.merge(fd16, on=["model", "pair_id"])
        rel16 = (k.Fisher_eps - k.q_exact).abs() / k.q_exact.abs()
        rel16r = (k.Fisher_richardson - k.q_exact).abs() / k.q_exact.abs()
        row = {
            "model": m, "N": len(k),
            "contexts_match_frozen_panel": same_host and same_donor and same_recv and same_rows,
            "fp32_fd075_vs_jvp32_median_cosine": round(float(x.cos_fd075_exact.median()), 7),
            "fp32_fd075_vs_jvp32_min_cosine": round(float(x.cos_fd075_exact.min()), 7),
            "fp32_fd075_vs_jvp32_spearman_Q": round(float(rec["rho_Qfd075_Qexact"]), 6),
            "fp32_fd075_vs_jvp32_median_rel_Q_error": round(float(rec["median_rel_qerr_fd075"]), 6),
            "fp32_fd075_vs_jvp32_max_rel_Q_error": round(float(x.rel_qerr_fd075.max()), 6),
            "fp32_half_vs_jvp32_median_rel_Q_error": round(float(rec["median_rel_qerr_half"]), 6),
            "fp32_richardson_vs_jvp32_median_rel_Q_error": round(float(rec["median_rel_qerr_rich"]), 6),
            "fp16_fd075_vs_jvp32_spearman_Q": round(float(spearmanr(k.Fisher_eps, k.q_exact).statistic), 6),
            "fp16_fd075_vs_jvp32_median_rel_Q_difference": round(float(rel16.median()), 6),
            "fp16_richardson_vs_jvp32_spearman_Q": round(float(spearmanr(k.Fisher_richardson, k.q_exact).statistic), 6),
            "fp16_richardson_vs_jvp32_median_rel_Q_difference": round(float(rel16r.median()), 6),
            "max_abs_delta_norm_difference_vs_frozen_panel": round(float(np.max(np.abs(j.delta_norm - j.delta_norm_frozen))), 6),
        }
        rows.append(row)
        for key in [c for c in row if c.startswith("fp16")] + ["fp32_fd075_vs_jvp32_max_rel_Q_error"]:
            print(f"    {key}: {row[key]}")
        pp = k[["model", "pair_id", "host_context_id", "donor_context_id", "receiver_context_id",
                "q_exact", "q_fd075", "Fisher_eps", "Fisher_richardson"]].rename(columns={
                    "q_exact": "Q_JVP32_suffix", "q_fd075": "Q_FD32_eps075_suffix",
                    "Fisher_eps": "Q_FD16_eps075_frozen", "Fisher_richardson": "Q_FD16_richardson_frozen"})
        pp["rel_diff_FD16_vs_JVP32"] = rel16.values
        per_pair.append(pp)

    if a.out:
        out = Path(a.out)
        out.mkdir(parents=True, exist_ok=True)
        pd.DataFrame(rows).to_csv(out / "FP16_VS_FP32_SUFFIX_SUMMARY.csv", index=False, lineterminator="\n")
        pd.concat(per_pair).to_csv(out / "FP16_VS_FP32_SUFFIX_PER_PAIR.csv", index=False, lineterminator="\n")
        print(f"wrote {out / 'FP16_VS_FP32_SUFFIX_SUMMARY.csv'} and FP16_VS_FP32_SUFFIX_PER_PAIR.csv")


if __name__ == "__main__":
    main()
