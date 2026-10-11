"""Compare ring-count frequencies as a pie chart and a bar chart."""

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

    ring_counts = pd.cut(
        df["RingCount"].dropna(),
        bins=[-1, 0, 1, 2, 3, 4, np.inf],
        labels=["0", "1", "2", "3", "4", "5+"],
    )
    counts = ring_counts.value_counts(sort=False)
    labels = [f"{ring_count} rings" for ring_count in counts.index]

    # Compare compound counts as shares and as bar lengths.
    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    axes[0].pie(counts.to_numpy(), labels=labels, autopct="%1.1f%%")
    axes[0].set_title("Share of compounds by ring count")

    axes[1].barh(labels[::-1], counts.to_numpy()[::-1])
    axes[1].set_xlabel("Number of compounds")
    axes[1].set_title("Compound count by ring count")

    plt.tight_layout()
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    output_path = FIGURE_DIR / "ring_count_distribution.png"
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
