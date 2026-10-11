"""Plot toxicity by molecular weight with a 14-record rolling mean."""

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

    plot_df = df.sort_values("MolWt")
    rolling_mean = plot_df["LD50"].rolling(14, center=True).mean()

    fig, ax = plt.subplots(figsize=(11, 3.6))
    ax.plot(plot_df["MolWt"], plot_df["LD50"], label="Compound LD50", lw=1)
    ax.plot(
        plot_df["MolWt"],
        rolling_mean,
        lw=2.5,
        color="black",
        label="14-compound rolling mean",
    )

    ax.set_xlabel("Molecular weight (MolWt)")
    ax.set_ylabel("LD50")
    ax.legend()
    ax.set_title("LD50 by molecular weight")
    plt.tight_layout()
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    output_path = FIGURE_DIR / "molecular_weight_trend.png"
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
