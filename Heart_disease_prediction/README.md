# ❤️ Heart Disease Prediction — GeoAI Edition
### Task 3 — Classification + Geospatial Risk Mapping

Predicts heart disease risk using clinical data AND geospatial features,
with an interactive risk map across 10 major Pakistan cities.

## What Makes This GeoAI?
- Dataset includes real Pakistan city coordinates
- Urban stress index per city as a geospatial feature
- Interactive Folium map showing heart disease risk by city
- Spatial clustering analysis of risk factors

## Models Used
| Model | Accuracy |
|-------|----------|
| Logistic Regression | See notebook |
| Decision Tree | See notebook |

## Files
| File | Description |
|------|-------------|
| `heart_disease_prediction.ipynb` | Main notebook |
| `heart_disease_pakistan.csv` | Dataset — 303 patients, 10 cities |

## How to Run
```
pip install pandas numpy matplotlib seaborn scikit-learn folium
```
Open notebook in VS Code and click **Run All**

## Evaluation Metrics
- Accuracy score
- Confusion Matrix
- ROC Curve + AUC score
- Feature Importance (clinical + geospatial)

## Cities Covered
Karachi, Lahore, Islamabad, Rawalpindi, Peshawar,
Quetta, Faisalabad, Multan, Hyderabad, Gujranwala

**Disclaimer:** For educational purposes only. Consult a licensed cardiologist for diagnosis.
