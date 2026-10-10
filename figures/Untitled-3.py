# Import libraries and give them short, conventional aliases.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Use a consistent style for all charts in this notebook.
sns.set_theme(style="whitegrid")

df = pd.read_csv("C:\\Users\\abadj\\Downloads\\ld50_cleaned.csv")
df.head(3)

# Build Anscombe's quartet as one table.
x = [10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5]
ys = {
    "I":   (x, [8.04, 6.95, 7.58, 8.81, 8.33, 9.96, 7.24, 4.26, 10.84, 4.82, 5.68]),
    "II":  (x, [9.14, 8.14, 8.74, 8.77, 9.26, 8.10, 6.13, 3.10, 9.13, 7.26, 4.74]),
    "III": (x, [7.46, 6.77, 12.74, 7.11, 7.81, 8.84, 6.08, 5.39, 8.15, 6.42, 5.73]),
    "IV":  ([8] * 7 + [19] + [8] * 3,
            [6.58, 5.76, 7.71, 8.84, 8.47, 7.04, 5.25, 12.50, 5.56, 7.91, 6.89]),
}
anscombe = pd.DataFrame(
    [(name, xi, yi) for name, (xs, yv) in ys.items() for xi, yi in zip(xs, yv)],
    columns=["dataset", "x", "y"],
)

# Calculate the same summaries that make the four datasets look similar.
summary = anscombe.groupby("dataset").agg(
    x_mean=("x", "mean"), y_mean=("y", "mean"),
    x_var=("x", "var"), y_var=("y", "var"),
)
summary["r"] = anscombe.groupby("dataset")[["x", "y"]].corr().xs("x", level=1)["y"]
print(summary.round(2))

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

sns.stripplot(data=df, x="ring_group", y="LD50", alpha=0.5, ax=axes[2])
axes[2].set_title("Individual LD50 values by ring count")
axes[2].set_xlabel("Number of rings")
axes[2].set_ylabel("LD50")

plt.tight_layout()
plt.show()