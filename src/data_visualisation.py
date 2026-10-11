"""
Create the six selected graphs for the hydrogen-bond acceptor project.

Run: python src/data_visualisation.py
Use --no-show to save the figures without opening plot windows.
Requires: pandas, numpy, matplotlib, scipy.

LD50 is already -log10(LD50 in mol/kg).
Higher scores mean greater acute oral toxicity in rats.
"""

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats


def fit_hba_association(model_data, predictors, cluster_codes):
    """HBA coefficient and 95% interval, grouping repeated identical SMILES."""
    x = np.column_stack([
        np.ones(len(model_data)),
        model_data[predictors],
    ])
    y = model_data["LD50"].to_numpy()
    n, k = x.shape

    beta, _, rank, _ = np.linalg.lstsq(x, y, rcond=None)
    if rank != k or n <= k:
        raise ValueError("The regression needs independent predictors and n > k.")

    residuals = y - x @ beta
    bread = np.linalg.inv(x.T @ x)
    number_of_clusters = int(cluster_codes.max() + 1)
    if number_of_clusters < 2:
        raise ValueError("At least two SMILES groups are required.")

    cluster_scores = np.zeros((number_of_clusters, k))
    np.add.at(cluster_scores, cluster_codes, x * residuals[:, None])

    correction = (
        number_of_clusters / (number_of_clusters - 1)
        * (n - 1) / (n - k)
    )
    covariance = (
        correction * bread
        @ (cluster_scores.T @ cluster_scores)
        @ bread
    )

    hba_index = 1 + predictors.index("NumHAcceptors")
    coefficient = beta[hba_index]
    standard_error = np.sqrt(covariance[hba_index, hba_index])
    margin = stats.t.ppf(0.975, number_of_clusters - 1) * standard_error
    return coefficient, coefficient - margin, coefficient + margin


def create_all_plots(csv_path, fig_dir, show=True):
    # Shared setup: load the data once.
    clean_df = pd.read_csv(csv_path)
    fig_dir = Path(fig_dir)
    fig_dir.mkdir(parents=True, exist_ok=True)

    plt.rcParams["figure.figsize"] = (8, 5)
    plt.rcParams["axes.grid"] = True
    plt.rcParams["grid.alpha"] = 0.3

    data = clean_df[["LD50", "NumHAcceptors"]].apply(
        pd.to_numeric, errors="raise"
    )
    if data.empty or not np.isfinite(data.to_numpy()).all():
        raise ValueError("LD50 and acceptor counts must be finite numeric values.")
    if (
        (data["NumHAcceptors"] < 0).any()
        or (data["NumHAcceptors"] % 1 != 0).any()
    ):
        raise ValueError("Acceptor counts must be non-negative integers.")

    ld50 = data["LD50"]  # Already transformed: do not log again.
    hba = data["NumHAcceptors"].astype(int)
    data["NumHAcceptors"] = hba

    y_label = "Acute oral-rat toxicity\n−log₁₀(LD₅₀ in mol/kg)"
    y_limits = (ld50.min() - 0.25, ld50.max() + 0.4)
    figures = []

    def save_figure(fig, filename, bottom=0):
        fig.tight_layout(rect=(0, bottom, 1, 1))
        fig.savefig(fig_dir / filename, dpi=300, facecolor="white")
        figures.append(fig)

    def style_relationship(ax, grid_axis="y"):
        ax.grid(False)
        ax.set_axisbelow(True)
        ax.grid(axis=grid_axis, color="#DCE2E8", linewidth=0.7)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    # GRAPH 1: LD50 distribution.
    fig, ax = plt.subplots()
    ax.hist(
        ld50, bins=40, density=True,
        color="steelblue", edgecolor="white", alpha=0.7
    )
    kde = stats.gaussian_kde(ld50)
    x = np.linspace(ld50.min(), ld50.max(), 300)
    ax.plot(x, kde(x), color="firebrick", lw=2, label="KDE")
    ax.axvline(
        ld50.mean(), color="k", ls="--",
        label=f"mean = {ld50.mean():.2f}"
    )
    ax.axvline(
        ld50.median(), color="green", ls=":", lw=2,
        label=f"median = {ld50.median():.2f}"
    )
    ax.set_xlabel("Transformed LD50 (-log10(LD50 in mol/kg))")
    ax.set_ylabel("Density")
    ax.set_title("LD50 distribution")
    ax.legend()
    save_figure(fig, "ld50_hist.png")

    # GRAPH 2: Acceptor count distribution, with a linear count axis.
    frequencies = hba.value_counts().reindex(
        range(hba.max() + 1), fill_value=0
    )
    fig, ax = plt.subplots()
    ax.bar(
        frequencies.index, frequencies.values,
        color="darkorange", edgecolor="white"
    )
    ax.axvline(
        hba.median(), color="k", ls="--",
        label=f"median = {hba.median():.0f}"
    )
    ax.set_xlabel("H-bond acceptors")
    ax.set_ylabel("Number of compound records")
    ax.set_yscale("linear")
    ax.set_title("Hydrogen-bond acceptor count distribution")
    ax.legend()
    save_figure(fig, "hba_counts_linear.png")

    # Group summaries used by graphs 3 and 4.
    groups = data.groupby("NumHAcceptors", sort=True)["LD50"]
    summary = groups.agg(["count", "median"])
    counts = summary.index.to_numpy()
    values = [groups.get_group(count).to_numpy() for count in counts]
    rng = np.random.default_rng(42)

    # GRAPH 3: Acceptor count against toxicity.
    fig, ax = plt.subplots(figsize=(12, 6.5))
    jitter = rng.uniform(-0.18, 0.18, size=len(data))
    ax.scatter(
        hba + jitter, ld50,
        s=16, alpha=0.22, color="#3977AC", edgecolors="none",
        label="Compound records", rasterized=True
    )
    # Diamonds are group medians, not a fitted regression line.
    medians = summary.loc[summary["count"] >= 5]
    ax.scatter(
        medians.index, medians["median"],
        s=48, marker="D", color="#202B36",
        edgecolors="white", linewidths=0.5,
        label="Group median (n >= 5)", zorder=3
    )
    ax.set_title(
        "Hydrogen-bond acceptors and acute toxicity", fontsize=17, pad=15
    )
    ax.set_xlabel("Hydrogen-bond acceptors per compound", fontsize=11)
    ax.set_ylabel(y_label, fontsize=11)
    ax.set_xlim(counts.min() - 0.7, counts.max() + 0.7)
    ax.set_ylim(y_limits)
    ax.legend(loc="upper right", frameon=False)
    style_relationship(ax)
    fig.text(
        0.10, 0.04,
        f"All {len(data):,} records retained. Horizontal jitter is for visibility only. "
        "Higher score = greater toxicity.",
        fontsize=9, color="#46515C"
    )
    save_figure(fig, "01_hba_toxicity_scatter.png", bottom=0.09)

    # GRAPH 4: Toxicity box plots by acceptor count, with sample sizes.
    fig, ax = plt.subplots(figsize=(14, 6.8))
    positions = np.arange(1, len(counts) + 1)
    enough_data = summary["count"].to_numpy() >= 5
    ax.boxplot(
        [value for value, keep in zip(values, enough_data) if keep],
        positions=positions[enough_data],
        widths=0.6, patch_artist=True, showfliers=True, whis=1.5,
        boxprops={"facecolor": "#BCD3E6", "edgecolor": "#3977AC"},
        medianprops={"color": "#202B36", "linewidth": 1.8},
        whiskerprops={"color": "#3977AC"},
        capprops={"color": "#3977AC"},
        flierprops={
            "marker": "o", "markersize": 3, "alpha": 0.35,
            "markerfacecolor": "#3977AC", "markeredgecolor": "none"
        }
    )
    # Show individual orange points when a group has fewer than 5 records.
    for position, value, keep in zip(positions, values, enough_data):
        if not keep:
            ax.scatter(
                position + rng.uniform(-0.08, 0.08, len(value)), value,
                s=35, color="#C26725", edgecolors="white",
                linewidths=0.4, zorder=3
            )

    ax.set_xticks(positions)
    ax.set_xticklabels(
        [f"{count}\nn={len(value):,}" for count, value in zip(counts, values)],
        fontsize=8
    )
    ax.set_xlim(0.4, len(counts) + 0.6)
    ax.set_ylim(y_limits)
    ax.set_title(
        "Toxicity by hydrogen-bond acceptor count", fontsize=17, pad=15
    )
    ax.set_xlabel(
        "Hydrogen-bond acceptors per compound; n = group sample size", fontsize=11
    )
    ax.set_ylabel(y_label, fontsize=11)
    style_relationship(ax)
    fig.text(
        0.09, 0.04,
        "Boxes: middle 50%; dark line: median; whiskers: up to 1.5×IQR. "
        "Orange points: groups with n < 5. All records retained.",
        fontsize=9, color="#46515C"
    )
    save_figure(fig, "02_hba_toxicity_boxplots.png", bottom=0.09)

    # GRAPH 5: Molecular weight against toxicity.
    mw_data = (
        clean_df[["MolWt", "LD50"]]
        .apply(pd.to_numeric, errors="raise")
        .dropna()
    )
    molecular_weight = mw_data["MolWt"]
    toxicity = mw_data["LD50"]
    fit = stats.linregress(molecular_weight, toxicity)
    x_line = np.linspace(molecular_weight.min(), molecular_weight.max(), 300)
    y_line = fit.intercept + fit.slope * x_line

    fig, ax = plt.subplots()
    ax.scatter(
        molecular_weight, toxicity,
        s=16, alpha=0.22, color="steelblue", edgecolors="none",
        label="Compound records"
    )
    ax.plot(
        x_line, y_line, color="black", lw=2, label="Fitted straight line"
    )
    ax.set_xlabel("Molecular weight (g/mol)")
    ax.set_ylabel("Transformed LD50 (-log10(LD50 in mol/kg))")
    ax.set_title(
        f"Molecular weight against toxicity (Pearson r = {fit.rvalue:.2f})"
    )
    ax.legend()
    save_figure(fig, "molecular_weight_toxicity.png")

    # GRAPH 6: HBA association before and after adjustment.
    model_data = (
        clean_df[["LD50", "NumHAcceptors", "MolWt", "MolLogP"]]
        .apply(pd.to_numeric, errors="raise")
        .dropna()
    )
    if model_data.empty or not np.isfinite(model_data.to_numpy()).all():
        raise ValueError("The model needs complete, finite numeric values.")

    smiles = clean_df.loc[model_data.index, "SMILES"]
    if smiles.isna().any():
        raise ValueError("SMILES are required to group repeated records.")
    cluster_codes, _ = pd.factorize(smiles, sort=True)

    # Both models use the SAME complete records.
    model_definitions = [
        ("Unadjusted\nHBA only", ["NumHAcceptors"], "#3977AC"),
        (
            "Adjusted\nHBA + molecular weight + logP",
            ["NumHAcceptors", "MolWt", "MolLogP"], "#C26725"
        ),
    ]
    fig, ax = plt.subplots(figsize=(11.5, 5.5))
    rows = [1, 0]
    intervals = []
    for (label, predictors, color), row in zip(model_definitions, rows):
        coefficient, lower, upper = fit_hba_association(
            model_data, predictors, cluster_codes
        )
        intervals.extend([lower, upper])
        ax.errorbar(
            coefficient, row,
            xerr=[[coefficient - lower], [upper - coefficient]],
            fmt="o", color=color, markersize=9, capsize=6, elinewidth=2.5
        )
        ax.annotate(
            f"{coefficient:.3f} (95% CI: {lower:.3f} to {upper:.3f})",
            xy=(coefficient, row), xytext=(0, 17),
            textcoords="offset points", ha="center", fontsize=10, color=color
        )

    xmin = min(0, min(intervals))
    xmax = max(0, max(intervals))
    padding = max((xmax - xmin) * 0.35, 0.01)
    ax.set_xlim(xmin - padding, xmax + padding)
    ax.set_ylim(-0.6, 1.6)
    ax.axvline(0, color="#78828C", linestyle="--", linewidth=1.2)
    ax.set_yticks(rows)
    ax.set_yticklabels([item[0] for item in model_definitions], fontsize=11)
    ax.set_title(
        "Hydrogen-bond acceptor association before and after adjustment",
        fontsize=15, pad=17
    )
    ax.set_xlabel(
        "Change in −log₁₀(LD₅₀ in mol/kg)\nper additional hydrogen-bond acceptor",
        fontsize=11
    )
    style_relationship(ax, grid_axis="x")
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)
    fig.text(
        0.05, 0.065,
        f"Both models: {len(model_data):,} complete records; "
        f"{len(clean_df) - len(model_data)} excluded for missing model variables.\n"
        "95% confidence intervals account for repeated identical SMILES. "
        "Exploratory linear-model associations; no causal interpretation.",
        fontsize=8.5, color="#46515C"
    )
    save_figure(fig, "03_hba_adjusted_association.png", bottom=0.15)

    # Display all six graphs together, or close them for a non-display run.
    if show:
        plt.show()
    else:
        for fig in figures:
            plt.close(fig)

    return figures


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--no-show", action="store_true",
        help="Save all six figures without opening plot windows.",
    )
    args = parser.parse_args()
    if args.no_show:
        plt.switch_backend("Agg")
    project_root = Path(__file__).resolve().parent.parent
    csv_path = project_root / "data" / "processed" / "ld50_cleaned.csv"
    fig_dir = project_root / "figures"
    create_all_plots(csv_path, fig_dir, show=not args.no_show)
    print(f"Saved six project figures to {fig_dir}")


if __name__ == "__main__":
    main()
