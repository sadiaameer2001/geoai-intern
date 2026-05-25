# Telco Customer Churn Prediction with GIS Analysis

A machine learning project that predicts customer churn for a telecom company and visualizes churn patterns geographically across US states using GIS techniques.

---

## Project Overview

This notebook combines classic churn prediction ML with geospatial analysis. Since the Telco dataset contains no geographic data, US states are randomly assigned to customers — a standard demonstration technique — and then state-level Census data (population density, urban ratio) is used as additional ML features. The result is both a predictive model and an interactive choropleth map showing churn rates by state.

---

## Project Structure

```
Task 2/
├── data/
│   ├── WA_Fn-UseC_-Telco-Customer-Churn.xlsx   # Source dataset
│   └── us_states.geojson                        # US state boundaries
├── Task2_Churn_GIS.ipynb                        # Main notebook
├── eda_plots.png                                # Auto-saved EDA figures
└── README.md
```

---

## Dataset

**Source:** IBM Watson Telco Customer Churn dataset
**Size:** ~7,043 customers, 21 features
**Target:** `Churn` — whether the customer left (Yes/No → 1/0)

**Key features used:**
- Demographics: `gender`, `SeniorCitizen`, `Partner`, `Dependents`
- Services: `PhoneService`, `InternetService`, `StreamingTV`, `TechSupport`, etc.
- Account: `Contract`, `PaymentMethod`, `MonthlyCharges`, `TotalCharges`, `tenure`
- GIS (engineered): `state`, `latitude`, `longitude`, `pop_density`, `urban_ratio`, `log_pop_density`, `is_urban_market`

---

## Setup & Requirements

### Install dependencies (Cell 1 in notebook)
```bash
pip install pandas numpy scikit-learn geopandas folium matplotlib seaborn joblib openpyxl
```

Or run Cell 1 in the notebook — it auto-installs all packages.

### Python version
Python 3.8+ recommended.

---

## How to Run

1. Clone or download this project folder.
2. Place the data files in the `data/` subdirectory (see structure above).
3. Open `Task2_Churn_GIS.ipynb` in Jupyter.
4. Update the `DATA_DIR` path in **Cell 4** to match your local setup:

```python
DATA_DIR = pathlib.Path(r'YOUR\PATH\TO\Task 2\data')
```

5. Run all cells top to bottom (`Kernel → Restart & Run All`).

---

## Notebook Walkthrough

| Cell | Purpose |
|------|---------|
| 1 | Install packages |
| 2 | Import libraries |
| 3 | Define GIS state data (lat/lon, pop density, urban ratio for all 50 states) |
| 4 | Load dataset from Excel/CSV |
| 5 | Data cleaning — fix `TotalCharges`, encode churn target |
| 6 | GIS feature engineering — assign states, add geographic features |
| 7 | Exploratory Data Analysis — 6-panel plot saved as `eda_plots.png` |
| 8 | Define features, train/test split (80/20, stratified) |
| 9 | Build scikit-learn preprocessing pipeline |
| 10–13 | Train models (Logistic Regression + Random Forest with GridSearchCV) |
| 14 | Evaluate models — accuracy, F1, ROC-AUC, confusion matrix |
| 15 | **Interactive choropleth map** — Folium map of churn rate by state |
| 16+ | Feature importance, final insights |

---

## Models Used

### Logistic Regression
- Baseline linear model
- Preprocessed via `ColumnTransformer` (StandardScaler + OneHotEncoder)

### Random Forest Classifier
- Tuned with `GridSearchCV` + `StratifiedKFold`
- Captures non-linear relationships
- Provides feature importances

---

## GIS Features

State-level data sourced from the US Census Bureau / World Population Review:

| Feature | Description |
|---------|-------------|
| `latitude` / `longitude` | State centroid coordinates |
| `pop_density` | Population per square mile |
| `urban_ratio` | Fraction of population living in urban areas |
| `is_urban_market` | Binary flag: `urban_ratio > 0.80` |
| `log_pop_density` | Log-transformed population density |

---

## Known Issue & Fix — Cell 15 (Choropleth Map)

Folium may throw a `ValueError: Cannot render objects with any missing geometries` when passing a `WindowsPath` object directly. Fix by loading the GeoJSON manually:

```python
import json

with open(GEOJSON_FILE, 'r', encoding='utf-8') as f:
    geojson_data = json.load(f)

choropleth = folium.Choropleth(
    geo_data = geojson_data,   # pass dict, not path
    ...
)
```

---

## Output

- `eda_plots.png` — 6-panel EDA visualization
- Interactive Folium map rendered inline in the notebook showing churn rate per US state (gray = no data)
- Model evaluation metrics printed to cell output

---

## Author

Developed as part of a GeoAI internship at the National University of Sciences & Technology (NUST).
