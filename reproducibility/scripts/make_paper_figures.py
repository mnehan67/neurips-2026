#!/usr/bin/env python3
"""Regenerate every data figure of the paper from the frozen public repository.

Reads CSV/JSON files directly from the frozen repository (ZIP or extracted
directory; no recomputation of model outputs) and writes vector PDFs sized for the NeurIPS
text block (5.5 in). Prints the statistics shown in each figure so they can be
checked against the manuscript.

Usage:
    python make_figures.py --repo <repository zip or directory> --out <figure dir>
"""
import argparse
import io
import json
import zipfile
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, LogNorm
import numpy as np
import pandas as pd
from scipy.stats import spearmanr

TEXTWIDTH = 5.5  # inches, NeurIPS text block

# Validated categorical order (blue, orange, aqua, yellow, magenta).
BLUE, ORANGE, AQUA, YELLOW, MAGENTA = "#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4"
INK, INK2, GRID = "#0b0b0b", "#52514e", "#d9d8d4"
MODEL_COLOR = {"Qwen3-8B": BLUE, "Mistral-7B": ORANGE}
MODEL_MARKER = {"Qwen3-8B": "o", "Mistral-7B": "s"}
SEQ_BLUE = LinearSegmentedColormap.from_list(
    "seq_blue", ["#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#256abf", "#184f95", "#0d366b"])

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "Times", "DejaVu Serif"],
    "mathtext.fontset": "stix",
    "font.size": 8,
    "axes.titlesize": 8.5,
    "axes.labelsize": 8,
    "xtick.labelsize": 7.5,
    "ytick.labelsize": 7.5,
    "legend.fontsize": 7.5,
    "axes.edgecolor": INK2,
    "axes.labelcolor": INK,
    "xtick.color": INK2,
    "ytick.color": INK2,
    "axes.linewidth": 0.6,
    "xtick.major.width": 0.6,
    "ytick.major.width": 0.6,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.02,
})

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


def _save(fig, path, **kw):
    """Save without a creation timestamp so reruns are byte-reproducible."""
    fig.savefig(path, metadata={"CreationDate": None, "ModDate": None}, **kw)


def style_axes(ax):
    ax.grid(True, color=GRID, linewidth=0.5)
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)


# ---------------------------------------------------------------------------
# Figure 2: crossed-receiver hexbin, bucket B2, primary depth
# ---------------------------------------------------------------------------
def fig_crossed_hexbin(repo, out):
    cases = [
        ("results/physical_crossing_v3/primary/qwen_b2_layer14_cross_receiver_physical.csv",
         "Qwen3-8B", 14),
        ("results/physical_crossing_v3/primary/mistral_b2_layer12_cross_receiver_physical.csv",
         "Mistral-7B", 12),
    ]
    floor = 1e-8  # display-only floor for numerical zeros, as in the original script
    data = []
    for rel, model, layer in cases:
        df = repo.csv(rel)
        df = df[df["receiver"] != df["origin_host"]].copy()  # alternative receivers only
        pooled = spearmanr(df["q_fisher"], df["kl_cross"]).statistic
        within = [spearmanr(g["q_fisher"], g["kl_cross"]).statistic for _, g in df.groupby("delta_id")]
        within = np.array([r for r in within if np.isfinite(r)])
        x = np.log10(np.maximum(df["q_fisher"].to_numpy(), floor))
        y = np.log10(np.maximum(df["kl_cross"].to_numpy(), floor))
        n_disp = df["delta_id"].nunique()
        data.append((model, layer, x, y, pooled, np.median(within), len(df), n_disp,
                     float(np.mean(within > 0))))
        print(f"[fig2] {model} L{layer} B2: n={len(df)} displacements={n_disp} pooled={pooled:.4f} "
              f"median_within={np.median(within):.4f} positive_frac={np.mean(within > 0):.4f}")

    lo = min(min(d[2].min(), d[3].min()) for d in data)
    hi = max(max(d[2].max(), d[3].max()) for d in data)
    fig, axes = plt.subplots(1, 2, figsize=(TEXTWIDTH, 2.1), sharey=False,
                             gridspec_kw={"wspace": 0.28})
    hbs = []
    for ax, (model, layer, x, y, pooled, med, n, nd, pos) in zip(axes, data):
        hb = ax.hexbin(x, y, gridsize=48, mincnt=1, cmap=SEQ_BLUE,
                       norm=LogNorm(vmin=1, vmax=400), linewidths=0.0, rasterized=True)
        hbs.append(hb)
        ax.set_title(f"{model} \N{EM DASH} Layer {layer}", color=INK, pad=13)
        ax.text(0.5, 1.015, f"median within-displacement $\\rho$ = {med:.3f}",
                transform=ax.transAxes, ha="center", va="bottom", fontsize=7, color=INK2)
        ax.set_xlabel(r"Receiver-local score $\log_{10} Q_{\mathrm{recv}}(r_k,\Delta u_d)$")
        style_axes(ax)
    axes[0].set_ylabel(r"Exact effect $\log_{10} K_{d,k}$")
    cb = fig.colorbar(hbs[-1], ax=axes, fraction=0.035, pad=0.02)
    cb.set_label("Interventions per hexagon", color=INK)
    cb.outline.set_linewidth(0.5)
    _save(fig, out / "fig2_crossed_hexbin.pdf", dpi=400)
    plt.close(fig)


# ---------------------------------------------------------------------------
# Figure 3: held-out receiver-map generalization (+/- 1 SE over 24 held-out displacements)
# ---------------------------------------------------------------------------
METHODS = [  # (key, label, color, marker, linestyle, linewidth)
    ("receiver_map", "Receiver-specific map", BLUE, "o", "-", 1.8),
    ("global_map", "Global map", ORANGE, "s", "-", 1.2),
    ("wrong_receiver_map", "Wrong-receiver map", AQUA, "^", "--", 1.2),
    ("identity", "Identity", YELLOW, "D", ":", 1.2),
    ("gain_only", "Gain only", MAGENTA, "v", "-.", 1.2),
]


def fig_receiver_maps(repo, out):
    cases = [("qwen3_8b", "Qwen3-8B", 14), ("mistral_7b", "Mistral-7B", 12)]
    fig, axes = plt.subplots(1, 2, figsize=(TEXTWIDTH, 2.05), sharey=True)
    for ax, (key, model, layer) in zip(axes, cases):
        d = repo.csv(f"results/receiver_transformation_v1/{key}/receiver_map_clustered_se.csv")
        for mkey, label, color, marker, ls, lw in METHODS:
            g = d[d["method"] == mkey].sort_values("downstream_layer")
            x, y, se = g["downstream_layer"].to_numpy(), g["mean_cosine"].to_numpy(), g["se"].to_numpy()
            ax.fill_between(x, y - se, y + se, color=color, alpha=0.18, linewidth=0)
            ax.plot(x, y, color=color, linestyle=ls, linewidth=lw, marker=marker, markersize=3.2,
                    markevery=3, label=label)
            print(f"[fig3] {model} {mkey}: final layer {int(x[-1])} mean={y[-1]:.4f} se={se[-1]:.4f}")
        ax.axhline(0, color=INK2, linewidth=0.6)
        ax.set_title(f"{model} \N{EM DASH} Layer {layer}", color=INK)
        ax.set_xlabel("Downstream layer $m$")
        style_axes(ax)
    axes[0].set_ylabel("Held-out cosine prediction")
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=5, frameon=False,
               bbox_to_anchor=(0.5, -0.06), handlelength=2.2, columnspacing=1.1)
    fig.tight_layout(rect=(0, 0.07, 1, 1))
    _save(fig, out / "fig3_receiver_maps.pdf")
    plt.close(fig)


# ---------------------------------------------------------------------------
# Appendix figures
# ---------------------------------------------------------------------------
def fig_dose(repo, out):
    q = repo.csv("results/fresh_c4_qwen3_8b_mistral7b/Q_VS_DOSE_CORRELATIONS.csv")
    fig, ax = plt.subplots(figsize=(3.3, 2.2))
    for model in ["Qwen3-8B", "Mistral-7B"]:
        d = q[q["model"] == model].sort_values("lambda")
        ax.plot(d["lambda"], d["spearman_q_vs_kl"], color=MODEL_COLOR[model],
                marker=MODEL_MARKER[model], markersize=3.5, markeredgecolor="white", markeredgewidth=0.5, linewidth=1.5, label=model)
        print(f"[dose] {model}: " + ", ".join(f"{a:.2f}:{b:.4f}" for a, b in zip(d['lambda'], d['spearman_q_vs_kl'])))
    ax.set_xlabel(r"Intervention dose $\lambda$")
    ax.set_ylabel(r"Spearman $\rho(Q_{\mathrm{recv}}, K_\lambda)$")
    ax.set_xticks(sorted(q["lambda"].unique()))
    ax.set_ylim(0.80, 1.00)
    ax.legend(frameon=False, loc="lower left")
    style_axes(ax)
    _save(fig, out / "figD_dose.pdf")
    plt.close(fig)


def fig_teacher_forced(repo, out):
    cases = [("Qwen_Qwen3-8B__mlp__L14__r0.400", "Qwen3-8B"),
             ("mistralai_Mistral-7B-v0.3__mlp__L12__r0.387", "Mistral-7B")]
    hs = [1, 4, 8, 16, 32]
    fig, ax = plt.subplots(figsize=(3.3, 2.2))
    for folder, model in cases:
        s = repo.json(f"results/fresh_c4_qwen3_8b_mistral7b/{folder}/summary.json")
        vals = [s[f"future_rho_h{h}"] for h in hs]
        ax.plot(hs, vals, color=MODEL_COLOR[model], marker=MODEL_MARKER[model], markersize=3.5, markeredgecolor="white", markeredgewidth=0.5,
                linewidth=1.5, label=model)
        print(f"[teacher-forced] {model}: " + ", ".join(f"h{h}:{v:.4f}" for h, v in zip(hs, vals)))
    ax.set_xscale("log", base=2)
    ax.set_xticks(hs)
    ax.set_xticklabels([str(h) for h in hs])
    ax.set_xlabel("Teacher-forced positions $h$ (log scale)")
    ax.set_ylabel(r"Spearman $\rho$ with cumulative KL")
    ax.set_ylim(0.5, 1.0)
    ax.legend(frameon=False, loc="lower left")
    style_axes(ax)
    _save(fig, out / "figD_teacher_forced.pdf")
    plt.close(fig)


def fig_trajectories(repo, out):
    cases = [("qwen3_8b", "Qwen3-8B", 14), ("mistral_7b", "Mistral-7B", 12)]
    fig, axes = plt.subplots(1, 2, figsize=(TEXTWIDTH, 2.2))
    for key, model, layer in cases:
        t = repo.csv(f"results/receiver_transformation_v1/{key}/layerwise_causal_trajectories.csv")
        g = t.groupby("downstream_layer").agg(fid=("fidelity", "median"), gain=("gain", "median"),
                                              n=("fidelity", "size")).reset_index()
        off = g["downstream_layer"] - layer
        for ax, col in zip(axes, ["fid", "gain"]):
            ax.plot(off, g[col], color=MODEL_COLOR[model], linewidth=1.6,
                    linestyle="-" if model == "Qwen3-8B" else "--", label=f"{model} (layer {layer})")
        print(f"[trajectory] {model}: rows/layer={int(g['n'].iloc[0])} final layer {int(g['downstream_layer'].iloc[-1])} "
              f"median fidelity={g['fid'].iloc[-1]:.4f} median gain={g['gain'].iloc[-1]:.4f}")
    axes[0].set_ylabel("Median directional fidelity $F^{(m)}$")
    axes[1].set_ylabel("Median gain $A^{(m)}$")
    for ax in axes:
        ax.set_xlabel(r"Layers after the intervention, $m-\ell$")
        ax.axhline(0, color=INK2, linewidth=0.6)
        style_axes(ax)
    axes[0].legend(frameon=False, loc="upper right")
    fig.tight_layout()
    _save(fig, out / "figD_trajectories.pdf")
    plt.close(fig)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".", type=Path)
    ap.add_argument("--out", required=True, type=Path)
    a = ap.parse_args()
    a.out.mkdir(parents=True, exist_ok=True)
    repo = Repo(a.repo)
    fig_crossed_hexbin(repo, a.out)
    fig_receiver_maps(repo, a.out)
    fig_dose(repo, a.out)
    fig_teacher_forced(repo, a.out)
    fig_trajectories(repo, a.out)


if __name__ == "__main__":
    main()
