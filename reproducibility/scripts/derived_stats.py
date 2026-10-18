#!/usr/bin/env python3
"""Descriptive statistics derived from frozen crossed-receiver outputs.

Reads only the frozen repository (ZIP or extracted directory) and reports, for every
crossed bucket, how much the exact KL of one frozen displacement varies across its
alternative receivers (the spread statistic of the paper's Section 5.2 and Table 7).

Usage: python derived_stats.py [--repo <repository zip or directory>] [--out <csv>]
"""
import argparse
import io
import json
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

FILES = [
    ("Qwen3-8B", b, f"results/physical_crossing_v3/primary/qwen_b{b}_layer14_cross_receiver_physical.csv")
    for b in (1, 2, 3)
] + [
    ("Mistral-7B", b, f"results/physical_crossing_v3/primary/mistral_b{b}_layer12_cross_receiver_physical.csv")
    for b in (1, 2, 3)
]


class Repo:
    """Read frozen outputs from the repository ZIP or from an extracted repository directory."""

    ANCHOR = "results/physical_crossing_v3/summary/config.json"

    def __init__(self, path):
        self.path = Path(path)
        if self.path.is_dir():
            if not (self.path / self.ANCHOR).exists():
                raise SystemExit(f"Not the repository: {self.ANCHOR} missing under {self.path}")
            self.z = None
        else:
            self.z = zipfile.ZipFile(self.path)
            anchor = [n for n in self.z.namelist() if n.endswith(self.ANCHOR)]
            if not anchor:
                raise SystemExit("Not the repository zip: physical_crossing_v3 missing")
            self.prefix = anchor[0][: -len(self.ANCHOR)]

    def read(self, rel):
        if self.z is None:
            return (self.path / rel).read_bytes()
        return self.z.read(self.prefix + rel)

    def csv(self, rel):
        return pd.read_csv(io.BytesIO(self.read(rel)))

    def json(self, rel):
        return json.loads(self.read(rel).decode("utf-8"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".")
    ap.add_argument("--out", default=None, help="optional CSV path")
    a = ap.parse_args()
    repo = Repo(a.repo)
    rows = []
    for model, b, rel in FILES:
        df = repo.csv(rel)
        df = df[df["receiver"] != df["origin_host"]]  # alternative receivers only
        floor = 1e-12  # guard against exact zeros
        spread = df.groupby("delta_id")["kl_cross"].agg(
            lambda s: np.log10(max(s.max(), floor) / max(s.min(), floor)))
        per = df.groupby("delta_id").size()
        rows.append({"model": model, "bucket": f"B{b}", "n_displacements": spread.size,
                     "alt_receivers_per_displacement": int(per.median()),
                     "median_log10_max_over_min_KL": round(float(spread.median()), 6),
                     "fraction_displacements_ratio_ge_100": round(float((spread >= 2).mean()), 6)})
    out = pd.DataFrame(rows)
    print(out.to_csv(index=False), end="")
    if a.out:
        out.to_csv(a.out, index=False, lineterminator="\n")


if __name__ == "__main__":
    main()
