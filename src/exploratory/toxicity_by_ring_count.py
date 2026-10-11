"""Compare mean, spread and individual toxicity values by ring count."""

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

    # Compare a summary plot, a spread plot, and the individual observations.
    fig, axes = plt.subplots(1, 3, figsize=(14, 3.5))

    df["ring_group"] = pd.cut(
        df["RingCount"],
        bins=[-1, 0, 1, 2, 3, 4, np.inf],
        labels=["0", "1", "2", "3", "4", "5+"],
    )

    sns.barplot(data=df, x="ring_group", y="LD50", errorbar=None, ax=axes[0])
    axes[0].set_title("Mean LD50 by ring count")
    axes[0].set_xlabel("Number of rings")
    axes[0].set_ylabel("LD50")

    sns.boxplot(data=df, x="ring_group", y="LD50", ax=axes[1])
    axes[1].set_title("LD50 spread by ring count")
    axes[1].set_xlabel("Number of rings")
    axes[1].set_ylabel("LD50")

    np.random.seed(42)
    sns.stripplot(data=df, x="ring_group", y="LD50", alpha=0.5, ax=axes[2])
    axes[2].set_title("Individual LD50 values by ring count")
    axes[2].set_xlabel("Number of rings")
    axes[2].set_ylabel("LD50")

    plt.tight_layout()
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    output_path = FIGURE_DIR / "toxicity_by_ring_count.png"
    fig.savefig(output_path, dpi=150, bbox_inches="tight", facecolor="white")
    print(f"Saved {output_path}")
    if show:
        plt.show()
    else:
        plt.close(fig)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--no-show", action="store_true", help="Save the plot without opening a window.")
    args = parser.parse_args()
    if args.no_show:
        plt.switch_backend("Agg")
    main(show=not args.no_show)
