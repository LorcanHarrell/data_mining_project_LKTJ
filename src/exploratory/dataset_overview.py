"""Print an overview calculated from the project's cleaned toxicity dataset."""

from pathlib import Path

import pandas as pd


def main():
    project_root = Path(__file__).resolve().parents[2]
    csv_path = project_root / "data" / "processed" / "ld50_cleaned.csv"
    df = pd.read_csv(csv_path)
    missing = df.isna().sum()

    print(f"Dataset: {csv_path}")
    print(f"Rows: {len(df):,}; columns: {len(df.columns)}")
    print(f"Exact duplicate rows: {df.duplicated().sum()}")
    print(f"Repeated SMILES values: {df['SMILES'].duplicated().sum()}")
    print("\nMissing values by column:")
    print(missing[missing > 0].to_string() if missing.any() else "None")
    print("\nNumeric columns:")
    print(", ".join(df.select_dtypes("number").columns))
    print("\nNumeric summary:")
    print(df.describe().T.to_string())


if __name__ == "__main__":
    main()
