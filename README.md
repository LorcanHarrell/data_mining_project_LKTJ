# Hydrogen-Bond Acceptors and Acute Toxicity

**Research question:** Is an increased number of hydrogen-bond acceptors associated with greater acute toxicity in organic compounds?

**H₀:** There is no significant association between the number of hydrogen-bond acceptors and acute toxicity.

**H₁:** Compounds with more hydrogen-bond acceptors have significantly higher −log₁₀(LD₅₀ mol/kg) values and are therefore more acutely toxic.

**Dataset:** Organic-compound records with names, SMILES, and molecular descriptors, with `NumHAcceptors` (hydrogen-bond acceptor count) and `LD50` (−log₁₀(LD₅₀ mol/kg), where higher values indicate greater acute toxicity) as the main variables.

**Provenance:** ChemIDplus → EPA TEST → current dataset (`ld50-smiles-descriptors-dataset.csv`).

## Current Progress

- `notebooks/01_data_exploration.ipynb` loads and inspects the dataset, completes cleaning, validates numeric target values and non-negative whole-number acceptor counts, and inspects extreme values.
- The cleaned dataset is saved to `data/processed/ld50_cleaned.csv` with 7,388 rows: 1 row missing `LD50` and 8 exact duplicate rows were removed. Other records sharing SMILES and extreme values were retained; `LD50` was not transformed.

## Roadmap

- [x] Select dataset and define research question
- [x] Load and inspect the dataset
- [x] Identify `LD50` and `NumHAcceptors` as the main variables
- [x] Check missing values and summary statistics
- [x] Clean and prepare the data
- [ ] Visualise LD50 and hydrogen-bond acceptor distributions
- [ ] Test the relationship between `NumHAcceptors` and `LD50`
- [ ] Perform statistical hypothesis testing
- [ ] Investigate other molecular properties that may influence the relationship
- [ ] Apply a machine-learning model as supporting analysis
- [ ] Interpret results and draw a final conclusion
