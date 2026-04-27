# 🏠 House Price Prediction with Location Features
### Task 6 — GeoAI / Machine Learning

Predicts house prices using both standard property features AND geospatial location features — making this a genuine GeoAI project.

---

## Objective
Build a regression model to predict house prices using property features such as size, bedrooms, and most importantly — geospatial location data like distance to city center, schools, and parks.

---

## Dataset
- **Source:** Synthetic dataset based on Rawalpindi/Islamabad area
- **Size:** 500 houses
- **File:** `housing_data.csv`

| Column | Description |
|--------|-------------|
| `price` | House price in PKR |
| `bedrooms` | Number of bedrooms |
| `bathrooms` | Number of bathrooms |
| `area_sqft` | House area in square feet |
| `house_age_years` | Age of the house |
| `latitude` | GPS latitude coordinate |
| `longitude` | GPS longitude coordinate |
| `dist_to_center_km` | Distance to city center (km) |
| `dist_to_school_km` | Distance to nearest school (km) |
| `dist_to_park_km` | Distance to nearest park (km) |
| `neighborhood` | Neighborhood name |

---

## What Makes This GeoAI?
- Uses real GPS coordinates (latitude, longitude)
- Distance to city center as a geospatial feature
- Distance to schools and parks as location features
- Neighborhood encoded as a spatial category
- Price prediction directly influenced by spatial proximity

---

## Models Applied
| Model | Type |
|-------|------|
| Linear Regression | Simple baseline model |
| Gradient Boosting | Advanced ensemble model |

---

## Key Results & Findings
- Gradient Boosting outperforms Linear Regression
- `area_sqft` is the strongest predictor of price
- Geospatial features (distance to center, school, park) significantly affect price
- Neighborhood category has strong spatial influence on price

---

## Evaluation Metrics
- R² Score
- Mean Absolute Error (MAE)
- Actual vs Predicted price plots
- Feature importance chart (geospatial features highlighted)

---

## How to Run

**Step 1:** Install libraries
```
pip install pandas numpy scikit-learn matplotlib seaborn
```

**Step 2:** Open in VS Code
```
house_price_prediction.ipynb
```

**Step 3:** Click **Run All**

---

## Graphs Generated
- Price distribution histogram
- Distance to center vs price scatter plot
- Average price by neighborhood
- Correlation heatmap
- Actual vs Predicted (both models)
- Model R² comparison
- Feature importance chart

---

## Skills Demonstrated
- Regression modeling (Linear Regression + Gradient Boosting)
- Geospatial feature engineering
- Feature scaling and selection
- Model evaluation (MAE, R²)
- Real estate + GeoAI data understanding