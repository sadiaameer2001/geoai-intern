# 🌍 GeoAI News Classifier — Task 1

## NLP Pipeline + GIS Visualization

This task builds an end-to-end pipeline that classifies news headlines by topic using a zero-shot BERT model, extracts geographic location mentions using NER, geocodes them, and visualizes topic density on an interactive world map.

---

## 📌 Pipeline Overview

1. **Load AG News Dataset** — 120,000 headlines from Hugging Face (sampled to 200)
2. **Topic Classification** — Zero-shot classification using `facebook/bart-large-mnli`
3. **Location Extraction** — Named Entity Recognition (NER) using spaCy
4. **Geocoding** — Convert location names to lat/lon using GeoPy + Nominatim
5. **GIS Visualization** — Interactive world maps using Folium and Plotly

---

## 🗂️ Files

| File | Description |
|------|-------------|
| `geoai_news_classifier.ipynb` | Main Jupyter notebook with full pipeline |
| `news_topic_map.html` | Interactive topic marker map (Folium) |
| `news_heatmap.html` | News density heatmap by location (Folium) |
| `news_bubble_map.html` | Topic bubble map (Plotly) |

---

## ⚙️ Setup & Installation

```bash
pip install transformers datasets spacy geopy folium plotly torch
python -m spacy download en_core_web_sm
```

> ⚠️ First run downloads the BART-large-MNLI model (~1.6GB). Subsequent runs use cache.

---

## 🤖 Model Details

| Component | Tool/Model |
|-----------|-----------|
| Topic Classification | `facebook/bart-large-mnli` (Zero-Shot) |
| NER | `spaCy en_core_web_sm` |
| Geocoding | GeoPy + Nominatim (OpenStreetMap) |
| Visualization | Folium, Plotly Express |

### Topic Labels
- 🌐 World News & Politics
- ⚽ Sports & Athletics
- 💼 Business & Finance
- 🔬 Science & Technology

---

## 📊 Output

- **Zero-shot accuracy** evaluated against AG News ground-truth labels
- **Confusion matrix** heatmap across 4 topics
- **Confidence score** distribution per topic
- **Interactive maps**: marker clusters, heatmaps, bubble maps

---

## 📍 NER Entity Types Used

| Entity | Meaning |
|--------|---------|
| `GPE` | Countries, cities, states |
| `LOC` | Non-GPE locations (mountains, rivers, regions) |

---

## 💡 Key Design Choice

Zero-shot classification is used intentionally — it demonstrates that BERT can classify news **without any labeled training examples**, making it more generalizable and showcasing the power of pretrained language models.

---

## 🔧 Requirements

- Python 3.8+
- transformers
- datasets
- spacy
- geopy
- folium
- plotly
- torch
- pandas
- scikit-learn
