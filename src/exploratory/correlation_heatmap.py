"""Plot Pearson correlations between numeric molecular descriptors and LD50."""

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

    numeric_data = df.select_dtypes("number")
    corr = numeric_data.corr(method="pearson")

    # A heatmap makes positive and negative relationships easier to scan.
    fig = plt.figure(figsize=(18, 16))
    sns.heatmap(corr, annot=False, cmap="vlag", center=0,
                vmin=-1, vmax=1, square=True, cbar_kws={"label": "Pearson correlation"})
    plt.xticks(rotation=45, ha="right", fontsize=9)
    plt.yticks(rotation=0, fontsize=9)
    plt.title("Pearson correlation matrix")
    plt.tight_layout()
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    output_path = FIGURE_DIR / "correlation_heatmap.png"
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
