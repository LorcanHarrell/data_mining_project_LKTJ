"""Compare molecular-weight/toxicity associations across ring groups."""

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CSV_PATH = PROJECT_ROOT / "data" / "processed" / "ld50_cleaned.csv"
FIGURE_DIR = PROJECT_ROOT / "figures" / "exploratory"


def main(show=True):
    sns.set_theme(style="whitegrid")
    df = pd.read_csv(CSV_PATH)

    sub = df.dropna(subset=["MolWt", "LD50", "RingCount"]).copy()
    sub["ring_group"] = pd.cut(
        sub["RingCount"],
        bins=[-1, 0, 1, 2, 3, 4, np.inf],
        labels=["0", "1", "2", "3", "4", "5+"],
    )

    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))

    # Left: the overall relationship across all compounds.
    sns.regplot(data=sub, x="MolWt", y="LD50",
                seed=42, scatter_kws={"alpha": 0.6}, line_kws={"color": "black"}, ax=axes[0])
    axes[0].set_xlabel("Molecular weight (MolWt)")
    axes[0].set_ylabel("LD50")
    axes[0].set_title(f"All compounds (Pearson r = {sub['MolWt'].corr(sub['LD50']):.2f})")

    # Right: draw one fitted line for each ring-count group.
    ring_groups = ["0", "1", "2", "3", "4", "5+"]
    palette = sns.color_palette("colorblind", n_colors=len(ring_groups))
    for ring_group, group in sub.groupby("ring_group", observed=True):
        color = palette[ring_groups.index(ring_group)]
        sns.regplot(
            data=group,
            seed=42,
            x="MolWt",
            y="LD50",
            scatter_kws={"alpha": 0.3, "s": 18},
            label=f"{ring_group} rings",
            color=color,
            ax=axes[1],
        )
    axes[1].legend(title="Number of rings")
    axes[1].set_xlabel("Molecular weight (MolWt)")
    axes[1].set_ylabel("LD50")
    axes[1].set_title("LD50 by molecular weight and ring count")

    plt.tight_layout()
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    output_path = FIGURE_DIR / "molecular_weight_by_ring_count.png"
    fig.savefig(output_path, dpi=150, bbox_inches="tight", facecolor="white")
    print(f"Saved {output_path}")
    if show:
        plt.show()
    else:
        plt.close(fig)

    print("Overall Pearson r:", round(sub["MolWt"].corr(sub["LD50"]), 3))
    for ring_group, group in sub.groupby("ring_group", observed=True):
        print(f"{ring_group:>2} rings:", round(group["MolWt"].corr(group["LD50"]), 3))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--no-show", action="store_true", help="Save the plot without opening a window.")
    args = parser.parse_args()
    if args.no_show:
        plt.switch_backend("Agg")
    main(show=not args.no_show)
