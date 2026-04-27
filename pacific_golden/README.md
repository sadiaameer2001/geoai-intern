🐦 Pacific Golden Plover — GeoAI Migration Chatbot
Task 4 — Prompt Engineering Based Chatbot with Spatial Component
A GeoAI chatbot that answers questions about the Pacific Golden Plover (Kōlea) migration — combining AI prompt engineering with real geospatial data, live eBird sightings, and an interactive migration map.

Objective
Build a chatbot using an LLM that answers questions through prompt engineering — adapted to GeoAI by focusing on the Pacific Golden Plover migration from Alaska to Hawaii, integrating real spatial data and an interactive map.

Tools Used
ToolPurposeGroq API (Llama 3)Free LLM powering the chatboteBird APIReal live bird sighting recordsFoliumInteractive migration mapStreamlitWeb-based chat interfaceHaversine FormulaReal GPS distance calculationpython-dotenvSecure API key management

What Makes This GeoAI?

Real eBird sighting records pulled live from API (Hawaii + Alaska)
GEE-style habitat data per location (NDVI, temperature, elevation, suitability score)
Haversine formula calculates real distances between GPS coordinates
Interactive map with satellite imagery + heatmap + clickable habitat popups
AI chatbot system prompt contains real spatial coordinates and habitat data


Files
FileDescriptionpacific_golden_plover_chatbot.ipynbStep-by-step Jupyter notebookapp.pyStreamlit web interface.env.exampleTemplate for API keys

API Keys Required
Create a .env file with:
GROQ_API_KEY=gsk_your_groq_key_here
EBIRD_API_KEY=your_ebird_key_here

Groq key: console.groq.com (free)
eBird key: ebird.org/api/keygen (free)


How to Run
Install libraries:
pip install groq python-dotenv folium requests pandas numpy matplotlib streamlit
Run Streamlit app:
streamlit run app.py
Or run notebook:
Open pacific_golden_plover_chatbot.ipynb → Click Run All

App Features
FeatureDescription💬 Chat TabAsk any question about Kōlea migration🗺️ Map TabSatellite + heatmap migration map📊 Data TabHabitat data tables + distance calculator🔄 eBird ButtonFetch live sighting data🛡️ Safety FilterBlocks harmful wildlife questions

Prompt Engineering
The system prompt includes:

Expert GeoAI ornithologist persona
Real coordinates of all breeding and wintering sites
NDVI, temperature, elevation, habitat suitability per location
Live eBird sighting counts
Migration facts (distance, duration, navigation methods)


Example Questions

"When do Kōlea arrive in Hawaii?"
"Which breeding site has the highest NDVI score?"
"How do they navigate 4,400 km across the Pacific?"
"Compare habitat conditions between Alaska and Hawaii"
"What is their conservation status?"


Key Migration Facts

Species: Pluvialis fulva — Pacific Golden Plover
Breeding: Arctic Alaska (May–July)
Wintering: Hawaiian Islands (August–April)
Distance: ~4,400 km non-stop across the Pacific Ocean
Duration: ~3–4 days continuous flight


Skills Demonstrated

Prompt design and engineering
Using LLM APIs (Groq — Llama 3)
Real API integration (eBird)
Geospatial data visualization (Folium)
Safety handling in chatbot responses
Streamlit web app development
Secure API key management (.env)


⚠️ Disclaimer: For educational purposes only. Consult a certified ornithologist for professional wildlife advice