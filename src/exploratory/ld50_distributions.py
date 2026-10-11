"""Compare histogram, box, violin and ECDF views of LD50."""

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CSV_PATH = PROJECT_ROOT / "data" / "processed" / "ld50_cleaned.csv"
FIGURE_DIR = PROJECT_ROOT / "figures" / "exploratory"


def main(show=True):
    sns.set_theme(style="whitegrid")
    df = pd.read_csv(CSV_PATH)

    # Compare four ways to show the distribution of one numeric column.
    fig, axes = plt.subplots(1, 4, figsize=(15, 3.2))

    sns.histplot(data=df, x="LD50", bins=25, ax=axes[0])
    axes[0].set_title("LD50 distribution")
    axes[0].set_xlabel("LD50")
    axes[0].set_ylabel("Number of compounds")

    sns.boxplot(data=df, y="LD50", ax=axes[1])
    axes[1].set_title("LD50 box plot")
    axes[1].set_ylabel("LD50")

    sns.violinplot(data=df, y="LD50", ax=axes[2])
    axes[2].set_title("LD50 violin plot")
    axes[2].set_ylabel("LD50")

    sns.ecdfplot(data=df, x="LD50", ax=axes[3])
    axes[3].set_title("LD50 ECDF")
    axes[3].set_xlabel("LD50")
    axes[3].set_ylabel("Cumulative proportion")

    plt.tight_layout()
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    output_path = FIGURE_DIR / "ld50_distributions.png"
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
