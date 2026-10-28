# Course Demand & Faculty Allocation Engine

This project provides an end-to-end synthetic data generator and validation suite for forecasting course demand and allocating faculty under strict capacity, skills, and workload constraints.

## Project Structure
- `src/config.py`: Controls scale parameters and the deterministic random seed (`20261022`).
- `src/generator.py`: Generates all 11 Master, Rule, and Transaction tables, injects edge cases, and exports to CSV.
- `src/validator.py`: Tests the generated output for Primary Key uniqueness, Foreign Key integrity, and domain Enum rules.
- `DATA_DICTIONARY.md`: The complete schema rules for the 11 entities.
- `SOURCE_MANIFEST.json`: Lawful provenance declaring 100% synthetic generation.

## Reproducibility
This project uses a locked numpy random seed (`20261022`). Running the generator twice will produce mathematically identical files and row counts, satisfying the reproducibility requirement.

## How to Run

**1. Set up the environment**
```bash
conda create -n env python=3.10 -y
conda activate env
pip install pandas numpy
```
**2. Generate the Data
```
python src/generator.py
```
(This will populate the /output folder with 12 CSV files, including ground_truth.csv which contains the injected edge case labels).

**3. Run the Validator
```
python src/validator.py
```
