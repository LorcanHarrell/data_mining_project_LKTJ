# Hydrogen-Bond Acceptors and Acute Toxicity

**Research question:** Is an increased number of hydrogen-bond acceptors associated with greater acute toxicity in organic compounds?

**H0:** There is no significant association between hydrogen-bond acceptor count and acute toxicity.

**H1:** Compounds with more hydrogen-bond acceptors have significantly higher -log10(LD50 in mol/kg) values and are therefore more acutely toxic.

The dataset's `LD50` column is already expressed as **-log10(LD50 in mol/kg)**. Higher scores indicate greater acute oral toxicity in rats. Do not apply another logarithmic transformation.

## Data and cleaning

- **Provenance:** ChemIDplus -> EPA TEST -> `data/raw/ld50-smiles-descriptors-dataset.csv`.
- **Raw data:** 7,397 records and 28 columns.
- **Cleaned data:** `data/processed/ld50_cleaned.csv`, containing 7,388 records and all 28 columns.
- Cleaning removed 1 record with missing `LD50` and 8 exact duplicate rows. No records were missing `NumHAcceptors`.
- The remaining 47 repeated SMILES values and extreme observations were retained. Repeated SMILES are not automatically duplicate records.
- The notebook checks that `LD50` and `NumHAcceptors` are finite numeric values and that acceptor counts are non-negative whole numbers.

The cleaning workflow is implemented in [`notebooks/01_data_exploration.ipynb`](notebooks/01_data_exploration.ipynb).

## Project structure

```text
data/
  raw/ld50-smiles-descriptors-dataset.csv   Original dataset
  processed/ld50_cleaned.csv               Cleaned dataset
notebooks/
  01_data_exploration.ipynb                Exploration, cleaning and initial statistics
src/
  data_visualisation.py                   Six selected project graphs
  exploratory/                            Additional exploratory scripts
  data_cleaning.py                         Placeholder; cleaning is in the notebook
  statistical_analysis.py                  Placeholder for standalone analysis
  machine_learning.py                      Placeholder for future modelling
figures/
  *.png                                   Six selected project graphs
  exploratory/*.png                       Additional exploratory figures
results/                                  Reserved for analysis tables and model outputs
requirements.txt                          Python dependencies
```

Python scripts belong in `src/`; generated chart images belong in `figures/`. Keep original data in `data/raw/` and cleaned data in `data/processed/`.

## Setup in VS Code

Open the project folder in VS Code. Run these commands in a PowerShell terminal from the project root:

```powershell
# Create the environment only if .venv does not already exist.
python -m venv .venv

# Install the project dependencies.
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Use **Python: Select Interpreter** in VS Code to select `.venv\Scripts\python.exe`. When opening the notebook, select the same environment as its kernel. These commands use the environment directly, so PowerShell activation is optional.

The dependencies include pandas, NumPy, Matplotlib, SciPy, seaborn, scikit-learn and Jupyter. Seaborn is used by the additional exploratory plots; scikit-learn is included for planned modelling.

## Reproduce the work

### 1. Explore and clean the data

Open `notebooks/01_data_exploration.ipynb` and run its cells in order. It reads the raw CSV and saves the cleaned CSV to `data/processed/ld50_cleaned.csv`. The cleaned CSV is already included in the repository.

### 2. Generate the six selected project graphs

```powershell
.\.venv\Scripts\python.exe src/data_visualisation.py
```

This saves all six images to `figures/` and displays them. To save images without opening plot windows:

```powershell
.\.venv\Scripts\python.exe src/data_visualisation.py --no-show
```

| Output in `figures/` | Contents |
| --- | --- |
| [ld50_hist.png](figures/ld50_hist.png) | LD50 distribution with density curve, mean and median |
| [hba_counts_linear.png](figures/hba_counts_linear.png) | Hydrogen-bond acceptor frequencies on a linear count axis |
| [01_hba_toxicity_scatter.png](figures/01_hba_toxicity_scatter.png) | Acceptor count versus toxicity, with jitter and group medians |
| [02_hba_toxicity_boxplots.png](figures/02_hba_toxicity_boxplots.png) | Toxicity by acceptor count, with group sample sizes |
| [molecular_weight_toxicity.png](figures/molecular_weight_toxicity.png) | Molecular weight versus toxicity with a fitted line |
| [03_hba_adjusted_association.png](figures/03_hba_adjusted_association.png) | HBA coefficient and 95% confidence interval before and after adjustment |

The final graph compares an HBA-only linear model with a model adjusted for molecular weight (`MolWt`) and lipophilicity (`MolLogP`). Both use the same **7,378 complete records**, excluding 10 records with missing model variables. Confidence intervals account for repeated identical SMILES using clustered standard errors. These are exploratory associations and do not establish causation.

### 3. Run additional exploratory scripts

These scripts are in `src/exploratory/`. Each plotting script saves a PNG with the same base name in `figures/exploratory/` and supports `--no-show`.

| Script | Purpose |
| --- | --- |
| [molecular_weight_trend.py](src/exploratory/molecular_weight_trend.py) | Molecular weight and toxicity with a 14-record rolling mean |
| [ld50_distributions.py](src/exploratory/ld50_distributions.py) | Histogram, box plot, violin plot and ECDF of LD50 |
| [toxicity_by_ring_count.py](src/exploratory/toxicity_by_ring_count.py) | Mean toxicity, box plots and individual records by ring count |
| [molecular_weight_by_ring_count.py](src/exploratory/molecular_weight_by_ring_count.py) | Overall and ring-group molecular-weight/toxicity relationships |
| [ring_count_distribution.py](src/exploratory/ring_count_distribution.py) | Ring-count frequencies as pie and bar charts |
| [correlation_heatmap.py](src/exploratory/correlation_heatmap.py) | Pearson correlation matrix for numeric columns |
| [dataset_overview.py](src/exploratory/dataset_overview.py) | Prints actual dimensions, missing values, duplicates and descriptive statistics; no image |

Examples:

```powershell
.\.venv\Scripts\python.exe src/exploratory/ld50_distributions.py --no-show
.\.venv\Scripts\python.exe src/exploratory/dataset_overview.py
```

All scripts resolve input and output paths from their own location, so they do not depend on a particular user's Downloads folder. Running a plotting script again replaces its corresponding PNG files.

## Current progress and remaining work

- [x] Select the dataset and define the research question.
- [x] Explore, validate and clean the data.
- [x] Visualise LD50 and hydrogen-bond acceptor distributions.
- [x] Create the six selected project graphs and additional exploratory plots.
- [x] Add exploratory unadjusted and adjusted HBA association plots.
- [x] Initial statistical analysis: completed Spearman correlation between `NumHAcceptors` and `LD50`, with sample size and interpretation in the exploration notebook.
- [ ] Complete remaining model diagnostics and sensitivity checks.
- [ ] Implement a supporting machine-learning model.
- [ ] Interpret the full results and write the final conclusion.

`src/data_cleaning.py`, `src/statistical_analysis.py` and `src/machine_learning.py` are documented placeholders, not runnable analysis workflows. Cleaning and the initial Spearman test currently live in the notebook, and the exploratory HBA regressions live in `src/data_visualisation.py`.
