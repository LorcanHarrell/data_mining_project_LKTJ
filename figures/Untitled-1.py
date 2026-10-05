# Import libraries and give them short, conventional aliases.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Use a consistent style for all charts in this notebook.
sns.set_theme(style="whitegrid")

df = pd.read_csv("C:\\Users\\abadj\\Downloads\\ld50_cleaned.csv")
df.head(3)

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
plt.show()