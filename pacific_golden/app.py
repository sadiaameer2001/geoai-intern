"""
Pacific Golden Plover — GeoAI Migration Chatbot
Streamlit App — Task 4 (Complete Redesign: Purpose-First Edition)
"""

import os, math, requests, warnings
import numpy as np
import pandas as pd
import folium
import streamlit as st
from folium.plugins import HeatMap, MiniMap
from groq import Groq
from dotenv import load_dotenv
from datetime import datetime
from streamlit.components.v1 import html as st_html

warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="Kōlea — Pacific Golden Plover GeoAI",
    page_icon="🐦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

PLOVER_SVG = """<svg viewBox="0 0 260 200" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:260px;">
  <defs>
    <radialGradient id="bg2" cx="50%" cy="80%" r="50%">
      <stop offset="0%" stop-color="#0d4a5a" stop-opacity="0.4"/>
      <stop offset="100%" stop-color="#000" stop-opacity="0"/>
    </radialGradient>
    <filter id="glow2"><feGaussianBlur stdDeviation="2.5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
    <filter id="shadow2"><feDropShadow dx="1" dy="3" stdDeviation="5" flood-color="#000" flood-opacity="0.5"/></filter>
  </defs>
  <ellipse cx="130" cy="182" rx="110" ry="14" fill="url(#bg2)"/>
  <ellipse cx="118" cy="108" rx="56" ry="38" fill="#5a3f08" transform="rotate(-6,118,108)"/>
  <ellipse cx="106" cy="94" rx="44" ry="28" fill="#8a6010" transform="rotate(-6,106,94)"/>
  <ellipse cx="90" cy="120" rx="16" ry="6" fill="#c8a030" transform="rotate(-14,90,120)"/>
  <ellipse cx="107" cy="125" rx="16" ry="6" fill="#b08820" transform="rotate(-8,107,125)"/>
  <ellipse cx="123" cy="128" rx="16" ry="6" fill="#986a10" transform="rotate(-3,123,128)"/>
  <ellipse cx="139" cy="126" rx="14" ry="5" fill="#7a5208" transform="rotate(2,139,126)"/>
  <ellipse cx="154" cy="121" rx="12" ry="5" fill="#5a3f08" transform="rotate(7,154,121)"/>
  <circle cx="95" cy="88" r="2.2" fill="#f0d060" opacity="0.85"/>
  <circle cx="108" cy="82" r="1.8" fill="#f0d060" opacity="0.75"/>
  <circle cx="120" cy="85" r="2.2" fill="#e8c840" opacity="0.8"/>
  <circle cx="134" cy="80" r="1.6" fill="#f0d060" opacity="0.65"/>
  <circle cx="145" cy="88" r="1.8" fill="#e0b830" opacity="0.6"/>
  <circle cx="103" cy="97" r="1.4" fill="#ffd840" opacity="0.7"/>
  <circle cx="116" cy="93" r="1.8" fill="#f0c830" opacity="0.65"/>
  <circle cx="130" cy="96" r="1.4" fill="#e8b820" opacity="0.6"/>
  <circle cx="144" cy="100" r="1.6" fill="#c8a020" opacity="0.55"/>
  <ellipse cx="122" cy="112" rx="40" ry="34" fill="#151008" filter="url(#shadow2)"/>
  <path d="M148 76 Q157 72 163 76 Q165 82 159 85 Q153 88 146 84Z" fill="#f0ece0" opacity="0.9"/>
  <circle cx="166" cy="73" r="23" fill="#181008" filter="url(#shadow2)"/>
  <circle cx="156" cy="64" r="1.8" fill="#c8a030" opacity="0.8"/>
  <circle cx="163" cy="60" r="1.4" fill="#b89020" opacity="0.7"/>
  <circle cx="173" cy="62" r="1.8" fill="#9a7010" opacity="0.65"/>
  <circle cx="179" cy="69" r="1.4" fill="#c0a028" opacity="0.6"/>
  <path d="M148 65 Q157 58 171 58 Q178 58 182 62 Q177 57 169 55 Q155 54 145 63Z" fill="#eeead8" opacity="0.88"/>
  <circle cx="175" cy="70" r="4.5" fill="#100d06"/>
  <circle cx="173" cy="68" r="1.1" fill="white" opacity="0.9"/>
  <path d="M187 73 L206 76 L187 79Z" fill="#252018"/>
  <path d="M187 73 L206 75 L205 76 L187 75Z" fill="#353028"/>
  <path d="M78 110 Q63 118 57 132 Q70 125 78 120Z" fill="#3a2a04"/>
  <line x1="128" y1="143" x2="123" y2="166" stroke="#7a7060" stroke-width="2.2" stroke-linecap="round"/>
  <line x1="139" y1="143" x2="134" y2="166" stroke="#7a7060" stroke-width="2.2" stroke-linecap="round"/>
  <line x1="123" y1="166" x2="113" y2="171" stroke="#7a7060" stroke-width="1.8" stroke-linecap="round"/>
  <line x1="123" y1="166" x2="123" y2="173" stroke="#7a7060" stroke-width="1.8" stroke-linecap="round"/>
  <line x1="123" y1="166" x2="132" y2="171" stroke="#7a7060" stroke-width="1.8" stroke-linecap="round"/>
  <line x1="134" y1="166" x2="124" y2="171" stroke="#7a7060" stroke-width="1.8" stroke-linecap="round"/>
  <line x1="134" y1="166" x2="134" y2="173" stroke="#7a7060" stroke-width="1.8" stroke-linecap="round"/>
  <line x1="134" y1="166" x2="143" y2="171" stroke="#7a7060" stroke-width="1.8" stroke-linecap="round"/>
  <path d="M10 20 Q130 -8 250 35" stroke="#c8a030" stroke-width="0.8" fill="none" stroke-dasharray="4,7" opacity="0.25"/>
  <circle cx="18" cy="18" r="1.5" fill="#ffd700" opacity="0.7" filter="url(#glow2)"/>
  <circle cx="36" cy="10" r="1" fill="#ffd700" opacity="0.5"/>
  <circle cx="235" cy="15" r="1.5" fill="#ffd700" opacity="0.65" filter="url(#glow2)"/>
  <circle cx="250" cy="28" r="1" fill="#ffd700" opacity="0.4"/>
</svg>"""

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;0,900;1,400&family=Outfit:wght@300;400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'Outfit', sans-serif; }
#MainMenu, footer, header { visibility: hidden; }
[data-testid="collapsedControl"] { display: none; }

:root {
    --gold:        #d4a820;
    --gold-bright: #f0c832;
    --gold-dim:    #7a5f10;
    --ocean-dark:  #060f14;
    --ocean-deep:  #0a2030;
    --ocean-mid:   #0d3a50;
    --teal:        #2a90a8;
    --sand:        #c8b888;
    --warm:        #ede4c8;
    --text:        #d8cfa8;
    --muted:       #687860;
}

.stApp {
    background:
        radial-gradient(ellipse 80% 50% at 10% 90%, rgba(13,58,80,0.5) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 90% 10%, rgba(212,168,32,0.06) 0%, transparent 55%),
        linear-gradient(150deg, #060f14 0%, #0a1a10 55%, #0e0a04 100%);
    color: var(--text);
    min-height: 100vh;
}

/* HERO */
.hero {
    display: flex; align-items: center; gap: 40px;
    padding: 40px 48px 32px 48px; position: relative;
    overflow: hidden; border-bottom: 1px solid rgba(212,168,32,0.12);
}
.hero::before {
    content: ''; position: absolute; inset: 0;
    background: radial-gradient(ellipse 70% 100% at 80% 50%, rgba(13,58,80,0.3) 0%, transparent 70%);
    pointer-events: none;
}
.hero-text { flex: 1; position: relative; z-index: 1; }
.hero-bird {
    width: 240px; flex-shrink: 0; position: relative; z-index: 1;
    animation: birdFloat 5s ease-in-out infinite;
    filter: drop-shadow(0 8px 32px rgba(212,168,32,0.25));
}
@keyframes birdFloat {
    0%,100% { transform: translateY(0) rotate(-1deg); }
    50%      { transform: translateY(-8px) rotate(1deg); }
}
.hero-eyebrow {
    font-size: 0.68rem; font-weight: 600; letter-spacing: 0.3em;
    text-transform: uppercase; color: var(--teal); margin-bottom: 10px;
}
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 3.2rem; font-weight: 900; line-height: 1.0;
    background: linear-gradient(135deg, #f0c832 0%, #d4a820 45%, #c8b888 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text; margin-bottom: 6px;
}
.hero-kolea {
    font-family: 'Playfair Display', serif;
    font-size: 1.05rem; font-style: italic; color: var(--sand); margin-bottom: 16px;
}
.hero-desc {
    font-size: 0.97rem; line-height: 1.78; color: var(--text);
    max-width: 580px; margin-bottom: 22px;
}
.hero-desc strong { color: var(--gold); font-weight: 600; }
.journey-strip { display: flex; gap: 26px; flex-wrap: wrap; }
.journey-stat { display: flex; flex-direction: column;
    border-left: 2px solid rgba(212,168,32,0.4); padding-left: 12px; }
.j-val { font-family: 'Playfair Display', serif; font-size: 1.35rem;
    font-weight: 700; color: var(--gold-bright); line-height: 1.1; }
.j-lbl { font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.14em;
    color: var(--muted); margin-top: 2px; }

/* PURPOSE CARDS */
.purpose-grid {
    display: grid; grid-template-columns: repeat(3, 1fr);
    gap: 16px; padding: 26px 48px; border-bottom: 1px solid rgba(212,168,32,0.1);
}
.purpose-card {
    background: rgba(13,58,80,0.22);
    border: 1px solid rgba(212,168,32,0.15);
    border-radius: 16px; padding: 22px 20px; position: relative; overflow: hidden;
    transition: border-color 0.25s, transform 0.25s, box-shadow 0.25s;
}
.purpose-card::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, transparent, var(--gold), transparent);
    opacity: 0; transition: opacity 0.25s;
}
.purpose-card:hover { border-color: rgba(212,168,32,0.4); transform: translateY(-3px);
    box-shadow: 0 12px 40px rgba(0,0,0,0.3); }
.purpose-card:hover::before { opacity: 1; }
.pc-icon { font-size: 2rem; margin-bottom: 12px; display: block; }
.pc-title { font-family: 'Playfair Display', serif; font-size: 1.05rem;
    color: var(--gold); margin-bottom: 8px; font-weight: 700; }
.pc-desc { font-size: 0.82rem; color: var(--text); line-height: 1.65; }

/* MAIN AREA */
.main-content { padding: 22px 48px 40px 48px; }

/* TABS */
[data-testid="stTabs"] [role="tablist"] {
    border-bottom: 1px solid rgba(212,168,32,0.15) !important; gap: 0; margin-bottom: 24px;
}
[data-testid="stTabs"] [role="tab"] {
    font-family: 'Outfit', sans-serif !important; font-size: 0.78rem !important;
    font-weight: 600 !important; letter-spacing: 0.12em !important;
    text-transform: uppercase !important; color: var(--muted) !important;
    border: none !important; background: transparent !important;
    padding: 12px 24px !important; border-radius: 0 !important;
    transition: color 0.2s !important;
}
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    color: var(--gold-bright) !important;
    border-bottom: 2px solid var(--gold-bright) !important;
}

/* SECTION HEADER */
.sec-hdr {
    font-family: 'Playfair Display', serif; font-size: 1.32rem;
    color: var(--gold-bright); margin-bottom: 18px;
    display: flex; align-items: center; gap: 10px;
}
.sec-hdr::after { content: ''; flex: 1; height: 1px;
    background: linear-gradient(90deg, rgba(212,168,32,0.3), transparent); }

/* CHAT */
.chat-wrap { max-height: 440px; overflow-y: auto; padding: 4px 2px;
    scrollbar-width: thin; scrollbar-color: rgba(212,168,32,0.25) transparent; }
.chat-user {
    background: linear-gradient(135deg, rgba(13,58,80,0.7), rgba(26,96,128,0.5));
    border: 1px solid rgba(42,144,168,0.3); border-radius: 18px 18px 4px 18px;
    padding: 13px 17px; margin: 10px 0; margin-left: 10%;
    color: var(--warm); font-size: 0.91rem; line-height: 1.65;
}
.chat-bot {
    background: rgba(8,20,12,0.7);
    border: 1px solid rgba(212,168,32,0.18); border-left: 3px solid var(--gold);
    border-radius: 4px 18px 18px 18px;
    padding: 13px 17px; margin: 10px 0; margin-right: 4%;
    color: var(--text); font-size: 0.91rem; line-height: 1.75;
}
.chat-lbl { font-size: 0.63rem; font-weight: 600; letter-spacing: 0.16em;
    text-transform: uppercase; margin-bottom: 4px; }
.lbl-u { color: var(--teal); text-align: right; }
.lbl-b { color: var(--gold-dim); }
.empty-state { text-align:center; padding: 50px 16px; }
.empty-icon { font-size: 3rem; display:block; margin-bottom: 14px;
    animation: pulse2 3s ease-in-out infinite; }
@keyframes pulse2 { 0%,100%{opacity:.5;transform:scale(1)} 50%{opacity:1;transform:scale(1.06)} }
.empty-title { font-family:'Playfair Display',serif; font-size:1.1rem;
    color:var(--sand); margin-bottom:8px; }
.empty-hints { font-size:0.77rem; color:var(--muted); line-height:1.85; }

/* STAT CARDS */
.s-card {
    background: rgba(13,58,80,0.22); border: 1px solid rgba(212,168,32,0.18);
    border-radius: 14px; padding: 18px 14px; text-align: center;
    position: relative; overflow: hidden; transition: transform 0.2s, border-color 0.2s;
}
.s-card::before { content:''; position:absolute; top:0;left:0;right:0; height:2px;
    background:linear-gradient(90deg,transparent,var(--gold),transparent); }
.s-card:hover { transform:translateY(-2px); border-color:rgba(212,168,32,0.4); }
.s-val { font-family:'Playfair Display',serif; font-size:1.8rem; font-weight:700;
    background:linear-gradient(135deg,#f0c832,#d4a820);
    -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text; }
.s-lbl { font-size:0.65rem; text-transform:uppercase; letter-spacing:0.14em;
    color:var(--muted); margin-top:5px; }

/* INPUT */
.stTextInput input {
    background: rgba(8,28,42,0.7) !important; border: 1px solid rgba(212,168,32,0.25) !important;
    border-radius: 14px !important; color: var(--warm) !important;
    font-family: 'Outfit', sans-serif !important; padding: 13px 18px !important;
}
.stTextInput input:focus {
    border-color: var(--gold) !important; box-shadow: 0 0 0 3px rgba(212,168,32,0.1) !important;
}
.stTextInput input::placeholder { color: var(--muted) !important; }

/* BUTTONS */
.stButton button {
    background: rgba(13,58,80,0.5) !important; color: var(--sand) !important;
    border: 1px solid rgba(42,144,168,0.3) !important; border-radius: 10px !important;
    font-family: 'Outfit', sans-serif !important; font-weight: 500 !important;
    font-size: 0.8rem !important; transition: all 0.22s !important;
}
.stButton button:hover {
    background: rgba(74,55,8,0.7) !important; color: var(--gold-bright) !important;
    border-color: var(--gold) !important;
    box-shadow: 0 4px 20px rgba(212,168,32,0.15) !important;
    transform: translateY(-1px) !important;
}

.tag { display:inline-block; background:rgba(13,58,80,0.5);
    border:1px solid rgba(42,144,168,0.3); border-radius:20px;
    padding:3px 11px; font-size:0.7rem; color:var(--teal); margin:2px; }
.warn { background:rgba(180,90,0,0.1); border:1px solid rgba(180,90,0,0.25);
    border-radius:10px; padding:10px 14px; font-size:0.77rem; color:#c07820;
    margin-top:14px; line-height:1.6; }
.info-box { background:rgba(13,58,80,0.2); border:1px solid rgba(212,168,32,0.15);
    border-radius:12px; padding:16px 20px; margin-bottom:20px;
    font-size:0.87rem; color:#c8b888; line-height:1.75; }

hr { border-color: rgba(212,168,32,0.1) !important; }
[data-testid="stDataFrame"] { border:1px solid rgba(212,168,32,0.15) !important;
    border-radius:12px !important; overflow:hidden !important; }
</style>
""", unsafe_allow_html=True)

# ── LOAD KEYS & DATA ──────────────────────────────────────────
load_dotenv()
GROQ_API_KEY  = os.getenv('GROQ_API_KEY')
EBIRD_API_KEY = os.getenv('EBIRD_API_KEY')

BREEDING_SITES = [
    {'name': 'Seward Peninsula, Alaska',      'lat': 64.50, 'lon': -165.40, 'season': 'May–Jul', 'habitat': 'Arctic tundra',    'pop_estimate': 5000},
    {'name': 'Yukon-Kuskokwim Delta, Alaska', 'lat': 61.50, 'lon': -165.00, 'season': 'May–Jul', 'habitat': 'Coastal wetlands', 'pop_estimate': 8000},
    {'name': 'Nome, Alaska',                  'lat': 64.50, 'lon': -165.41, 'season': 'Jun–Jul', 'habitat': 'Tundra grassland', 'pop_estimate': 3000},
    {'name': 'Kotzebue, Alaska',              'lat': 66.90, 'lon': -162.60, 'season': 'May–Jul', 'habitat': 'Arctic shrubland', 'pop_estimate': 2000},
]
WINTERING_SITES = [
    {'name': 'Oahu, Hawaii',       'lat': 21.30, 'lon': -157.85, 'season': 'Aug–Apr', 'habitat': 'Urban grassland',   'pop_estimate': 12000},
    {'name': 'Maui, Hawaii',       'lat': 20.80, 'lon': -156.33, 'season': 'Aug–Apr', 'habitat': 'Coastal wetlands',  'pop_estimate':  6000},
    {'name': 'Big Island, Hawaii', 'lat': 19.59, 'lon': -155.43, 'season': 'Aug–Apr', 'habitat': 'Open grassland',    'pop_estimate':  4000},
    {'name': 'Kauai, Hawaii',      'lat': 22.00, 'lon': -159.50, 'season': 'Aug–Apr', 'habitat': 'Agricultural land', 'pop_estimate':  3000},
    {'name': 'Midway Atoll',       'lat': 28.21, 'lon': -177.37, 'season': 'Aug–Apr', 'habitat': 'Atoll grassland',   'pop_estimate':  1500},
]
ROUTE_POINTS = [
    {'name': 'Departure — Alaska',  'lat': 63.00, 'lon': -165.00},
    {'name': 'Pacific Day 2',       'lat': 52.00, 'lon': -168.00},
    {'name': 'Pacific Midpoint',    'lat': 42.00, 'lon': -170.00},
    {'name': 'Pacific Day 4',       'lat': 32.00, 'lon': -168.00},
    {'name': 'Arrival — Hawaii',    'lat': 21.50, 'lon': -157.50},
]

def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    a = math.sin((lat2-lat1)/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin((lon2-lon1)/2)**2
    km = R * 2 * math.asin(math.sqrt(a))
    return round(km), round(km * 0.621371)

@st.cache_data
def generate_habitat_data():
    np.random.seed(42)
    records = []
    for site in BREEDING_SITES:
        records.append({'site_name': site['name'], 'latitude': site['lat'], 'longitude': site['lon'],
            'season': site['season'], 'habitat_type': site['habitat'],
            'ndvi': round(np.random.uniform(0.25, 0.55), 3),
            'mean_temp_c': round(np.random.uniform(4, 14), 1),
            'elevation_m': int(np.random.randint(10, 300)),
            'pop_estimate': site['pop_estimate'],
            'habitat_suitability': round(min(1.0, np.random.uniform(0.25, 0.55) * 1.3), 2),
            'site_type': 'breeding'})
    for site in WINTERING_SITES:
        records.append({'site_name': site['name'], 'latitude': site['lat'], 'longitude': site['lon'],
            'season': site['season'], 'habitat_type': site['habitat'],
            'ndvi': round(np.random.uniform(0.40, 0.80), 3),
            'mean_temp_c': round(np.random.uniform(22, 29), 1),
            'elevation_m': int(np.random.randint(5, 150)),
            'pop_estimate': site['pop_estimate'],
            'habitat_suitability': round(min(1.0, np.random.uniform(0.40, 0.80) * 1.3), 2),
            'site_type': 'wintering'})
    return pd.DataFrame(records)

@st.cache_data(ttl=3600)
def fetch_ebird_sightings():
    results = {'hawaii': [], 'alaska': []}
    if not EBIRD_API_KEY:
        return results
    headers = {'X-eBirdApiToken': EBIRD_API_KEY}
    for region, key in [('US-HI', 'hawaii'), ('US-AK', 'alaska')]:
        try:
            r = requests.get(f'https://api.ebird.org/v2/data/obs/{region}/recent', headers=headers,
                params={'speciesCode': 'pagplo', 'maxResults': 100, 'includeProvisional': True}, timeout=10)
            if r.status_code == 200:
                results[key] = [o for o in r.json() if o.get('lat') and o.get('lng')]
        except: pass
    return results

def build_map(habitat_df, ebird_data):
    m = folium.Map(location=[43.0, -165.0], zoom_start=3, tiles=None)
    folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='Esri', name='Satellite View', overlay=False, control=True).add_to(m)
    folium.TileLayer(tiles='CartoDB dark_matter', name='Dark Map', overlay=False, control=True).add_to(m)

    all_s = ebird_data['hawaii'] + ebird_data['alaska']
    if all_s:
        hg = folium.FeatureGroup(name='Live eBird Sightings')
        HeatMap([[o['lat'], o['lng'], float(o.get('howMany', 1))] for o in all_s],
            min_opacity=0.4, radius=22, blur=16,
            gradient={'0.2':'blue','0.5':'lime','0.8':'orange','1.0':'red'}).add_to(hg)
        hg.add_to(m)

    bg = folium.FeatureGroup(name='Breeding Grounds (Alaska)')
    for _, s in habitat_df[habitat_df['site_type'] == 'breeding'].iterrows():
        folium.CircleMarker([s['latitude'], s['longitude']], radius=13,
            color='#d4a820', fill=True, fill_color='#d4a820', fill_opacity=0.88,
            tooltip=f"BREEDING: {s['site_name']}",
            popup=folium.Popup(
                f"<div style='font-family:Georgia;width:230px;background:#0a1408;color:#d8cfa8;padding:14px;border-radius:10px;border:1px solid rgba(212,168,32,0.3);'>"
                f"<div style='color:#d4a820;font-size:10px;letter-spacing:1.5px;font-weight:bold;margin-bottom:6px;'>BREEDING SITE · ALASKA</div>"
                f"<div style='font-size:15px;font-weight:bold;margin-bottom:10px;'>{s['site_name']}</div>"
                f"<div style='font-size:11px;line-height:1.8;'>"
                f"📅 Season: <b>{s['season']}</b><br>🌿 Habitat: {s['habitat_type']}<br>"
                f"🌱 NDVI: <b>{s['ndvi']}</b> &nbsp; 🌡️ Temp: <b>{s['mean_temp_c']}°C</b><br>"
                f"⛰️ Elevation: {s['elevation_m']}m<br>"
                f"🐦 Population: <b>~{s['pop_estimate']:,} birds</b><br>"
                f"✅ Suitability score: <b>{s['habitat_suitability']}/1.0</b></div></div>", max_width=260)
        ).add_to(bg)
    bg.add_to(m)

    wg = folium.FeatureGroup(name='Wintering Grounds (Hawaii)')
    for _, s in habitat_df[habitat_df['site_type'] == 'wintering'].iterrows():
        folium.CircleMarker([s['latitude'], s['longitude']], radius=13,
            color='#2a90a8', fill=True, fill_color='#2a90a8', fill_opacity=0.88,
            tooltip=f"WINTERING: {s['site_name']}",
            popup=folium.Popup(
                f"<div style='font-family:Georgia;width:230px;background:#060f14;color:#d8cfa8;padding:14px;border-radius:10px;border:1px solid rgba(42,144,168,0.3);'>"
                f"<div style='color:#2a90a8;font-size:10px;letter-spacing:1.5px;font-weight:bold;margin-bottom:6px;'>WINTERING SITE · HAWAII</div>"
                f"<div style='font-size:15px;font-weight:bold;margin-bottom:10px;'>{s['site_name']}</div>"
                f"<div style='font-size:11px;line-height:1.8;'>"
                f"📅 Season: <b>{s['season']}</b><br>🌿 Habitat: {s['habitat_type']}<br>"
                f"🌱 NDVI: <b>{s['ndvi']}</b> &nbsp; 🌡️ Temp: <b>{s['mean_temp_c']}°C</b><br>"
                f"⛰️ Elevation: {s['elevation_m']}m<br>"
                f"🐦 Population: <b>~{s['pop_estimate']:,} birds</b><br>"
                f"✅ Suitability score: <b>{s['habitat_suitability']}/1.0</b></div></div>", max_width=260)
        ).add_to(wg)
    wg.add_to(m)

    rg = folium.FeatureGroup(name='Non-Stop Migration Route')
    folium.PolyLine([[p['lat'], p['lon']] for p in ROUTE_POINTS],
        color='#d4a820', weight=3, opacity=0.9, dash_array='10').add_to(rg)
    for pt in ROUTE_POINTS:
        folium.CircleMarker([pt['lat'], pt['lon']], radius=5,
            color='#d4a820', fill=True, fill_color='#f0c832',
            tooltip=pt['name']).add_to(rg)
    rg.add_to(m)

    km, miles = haversine(64.0, -165.0, 21.0, -157.0)
    folium.Marker([42.0, -174.0], icon=folium.DivIcon(html=
        f"""<div style='background:rgba(6,15,20,0.93);color:#d4a820;padding:9px 14px;
        border-radius:12px;border:1px solid rgba(212,168,32,0.5);font-family:Georgia;
        text-align:center;white-space:nowrap;box-shadow:0 4px 24px rgba(0,0,0,0.5);'>
        Non-stop Pacific flight<br><b style='font-size:15px;'>{km:,} km &nbsp;|&nbsp; {miles:,} mi</b><br>
        <span style='font-size:9px;color:#a09060;'>3–4 days · no rest · no food</span></div>"""),
        tooltip='Migration Distance').add_to(m)

    m.get_root().html.add_child(folium.Element(
        f"""<div style='position:fixed;top:10px;left:50%;transform:translateX(-50%);
        background:rgba(6,15,20,0.94);color:#d4a820;padding:10px 26px;
        border-radius:12px;border:1px solid rgba(212,168,32,0.4);font-family:Georgia;
        font-size:14px;font-weight:bold;z-index:9999;text-align:center;'>
        Pacific Golden Plover — Alaska to Hawaii Migration<br>
        <span style='font-size:9px;color:#6a8060;letter-spacing:0.1em;'>
        CLICK MARKERS FOR HABITAT DATA · TOGGLE LAYERS TOP-RIGHT</span></div>"""))

    m.get_root().html.add_child(folium.Element(
        """<div style='position:fixed;bottom:40px;left:14px;background:rgba(6,15,20,0.92);
        color:#c8b888;padding:14px 18px;border-radius:12px;
        border:1px solid rgba(212,168,32,0.22);font-family:Arial;
        font-size:11px;z-index:9999;line-height:2.2;'>
        <b style='color:#d4a820;letter-spacing:0.1em;font-size:10px;'>MAP LEGEND</b><br>
        <span style='color:#d4a820;font-size:14px;'>●</span> Breeding grounds (Alaska)<br>
        <span style='color:#2a90a8;font-size:14px;'>●</span> Wintering grounds (Hawaii)<br>
        <span style='color:#d4a820;'>— —</span> Non-stop migration route<br>
        <span style='color:#ff9900;'>▓</span> Live eBird sightings heatmap</div>"""))

    MiniMap(toggle_display=True, position='bottomright').add_to(m)
    folium.LayerControl(collapsed=False).add_to(m)
    return m._repr_html_()

def is_safe(q):
    blocked = ['how to hunt','how to kill','how to trap','shoot bird','poison','harm animal']
    return not any(kw in q.lower() for kw in blocked)

# ── SESSION STATE ─────────────────────────────────────────────
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'habitat_df' not in st.session_state:
    st.session_state.habitat_df = generate_habitat_data()
if 'ebird_data' not in st.session_state:
    st.session_state.ebird_data = {'hawaii': [], 'alaska': []}

habitat_df = st.session_state.habitat_df

# ══════════════════════════════════════════════════════
# HERO
# ══════════════════════════════════════════════════════
st.markdown(f"""
<div class="hero">
  <div class="hero-text">
    <div class="hero-eyebrow">GeoAI Wildlife Research Platform · Task 4</div>
    <div class="hero-title">Pacific Golden<br>Plover</div>
    <div class="hero-kolea">Pluvialis fulva &nbsp;·&nbsp; Kōlea (Hawaiian name)</div>
    <div class="hero-desc">
      One of nature's most extraordinary feats: a small shorebird that flies 
      <strong>4,400 km non-stop across the open Pacific Ocean</strong> — 
      from Arctic Alaska to Hawaii — with no rest, no food, and no landmarks to guide it.
      This platform uses <strong>AI chat</strong>, <strong>live eBird tracking</strong>, 
      and <strong>satellite habitat analysis</strong> to explore and understand this migration.
    </div>
    <div class="journey-strip">
      <div class="journey-stat"><div class="j-val">4,400 km</div><div class="j-lbl">Over open ocean</div></div>
      <div class="journey-stat"><div class="j-val">3–4 days</div><div class="j-lbl">No rest, no stop</div></div>
      <div class="journey-stat"><div class="j-val">2× weight</div><div class="j-lbl">Fat stored pre-flight</div></div>
      <div class="journey-stat"><div class="j-val">9 sites</div><div class="j-lbl">Tracked by GeoAI</div></div>
    </div>
  </div>
  <div class="hero-bird">{PLOVER_SVG}</div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
# PURPOSE CARDS — what each tab does
# ══════════════════════════════════════════════════════
st.markdown("""
<div class="purpose-grid">
  <div class="purpose-card">
    <span class="pc-icon">💬</span>
    <div class="pc-title">Chat with an AI Ornithologist</div>
    <div class="pc-desc">
      Ask questions in plain English about the Kōlea's biology, navigation, 
      breeding sites, and habitat quality scores. The AI answers using 
      real satellite data from all 9 tracked locations.
    </div>
  </div>
  <div class="purpose-card">
    <span class="pc-icon">🗺️</span>
    <div class="pc-title">See the Migration on a Map</div>
    <div class="pc-desc">
      An interactive map shows the exact Alaska breeding grounds, 
      Hawaiian wintering islands, and the transoceanic flight path.
      Load real-time eBird sightings as a live heat map overlay.
    </div>
  </div>
  <div class="purpose-card">
    <span class="pc-icon">📡</span>
    <div class="pc-title">Analyse Habitat Quality</div>
    <div class="pc-desc">
      Browse satellite data for each site — vegetation index (NDVI), 
      temperature, elevation, and suitability scores. 
      Calculate the exact flight distance between any two sites.
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════════════
st.markdown('<div class="main-content">', unsafe_allow_html=True)
tab1, tab2, tab3 = st.tabs(["💬  Chat with GeoAI", "🗺️  Migration Map", "📊  Habitat Data"])

# ── TAB 1: CHAT ───────────────────────────────────────
with tab1:
    col_chat, col_side = st.columns([3, 1])

    with col_chat:
        st.markdown('<div class="sec-hdr">Ask the GeoAI Ornithologist</div>', unsafe_allow_html=True)

        chat_html = '<div class="chat-wrap">'
        if not st.session_state.messages:
            chat_html += """
            <div class="empty-state">
              <span class="empty-icon">🐦</span>
              <div class="empty-title">Ask me anything about the Kōlea</div>
              <div class="empty-hints">
                How do they navigate 4,400 km with no landmarks?<br>
                Which Alaska site has the best breeding habitat?<br>
                Why do they double their weight before flying?<br>
                What does the NDVI score mean for Oahu?
              </div>
            </div>"""
        else:
            for msg in st.session_state.messages:
                if msg['role'] == 'user':
                    chat_html += f'<div class="chat-lbl lbl-u">You</div><div class="chat-user">{msg["content"]}</div>'
                else:
                    chat_html += f'<div class="chat-lbl lbl-b">🐦 GeoAI Ornithologist</div><div class="chat-bot">{msg["content"]}</div>'
        chat_html += '</div>'
        st.markdown(chat_html, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        with st.form('chat_form', clear_on_submit=True):
            user_input = st.text_input("q",
                placeholder="e.g. How do they navigate across the Pacific Ocean?",
                label_visibility="collapsed")
            submitted = st.form_submit_button("Send →")

        if submitted and user_input.strip():
            question = user_input.strip()
            if not is_safe(question):
                st.session_state.messages += [
                    {'role': 'user', 'content': question},
                    {'role': 'assistant', 'content': '⚠️ I only support Pacific Golden Plover conservation, not harm to wildlife.'}
                ]
            else:
                ctx = '\n'.join([
                    f"  - {r['site_name']}: {r['latitude']}N {abs(r['longitude'])}W | "
                    f"NDVI={r['ndvi']} | Temp={r['mean_temp_c']}C | Suitability={r['habitat_suitability']} | Pop~{r['pop_estimate']:,}"
                    for _, r in habitat_df.iterrows()])
                n_eb = len(st.session_state.ebird_data['hawaii']) + len(st.session_state.ebird_data['alaska'])
                system_prompt = f"""You are a GeoAI ornithologist specialising in the Pacific Golden Plover (Pluvialis fulva), called Kōlea in Hawaii.

HABITAT DATA (satellite-derived):
{ctx}

eBird live sightings loaded: {n_eb}

KEY MIGRATION FACTS:
- Non-stop flight: Alaska to Hawaii, ~4,400 km, ~3-4 days, no rest, no food
- Departure: late July–August each year
- Navigation: uses Earth's magnetic field, stars at night, and sun compass by day
- Pre-migration: doubles body weight with fat reserves (from ~95g to ~190g)
- Breeds in Arctic Alaska tundra (May–July). Winters in Hawaiian Islands (Aug–April)
- Conservation status: Least Concern (IUCN)
- Remarkable: returns to exact same Hawaiian lawn or garden each year

Always be clear, warm, and scientifically accurate. Include coordinates and habitat scores when relevant.
Today: {datetime.now().strftime('%B %d, %Y')}"""

                history = [{'role': m['role'], 'content': m['content']} for m in st.session_state.messages[-10:]]
                try:
                    client = Groq(api_key=GROQ_API_KEY)
                    resp = client.chat.completions.create(
                        model='llama-3.1-8b-instant',
                        messages=[{'role': 'system', 'content': system_prompt}] + history + [{'role': 'user', 'content': question}],
                        temperature=0.7, max_tokens=700)
                    answer = resp.choices[0].message.content
                except Exception as e:
                    answer = f"⚠️ Groq API error: {e}"

                st.session_state.messages += [
                    {'role': 'user', 'content': question},
                    {'role': 'assistant', 'content': answer}
                ]
            st.rerun()

    with col_side:
        st.markdown('<div style="font-family:Playfair Display,serif;font-size:1rem;color:#d4a820;margin-bottom:8px;">Try asking</div>', unsafe_allow_html=True)
        for s in [
            "When do Kōlea arrive in Hawaii?",
            "Which site has highest NDVI?",
            "How do they navigate the Pacific?",
            "How fast do they fly?",
            "Conservation status?",
            "Distance Nome to Oahu?",
            "Why do they double weight?",
        ]:
            st.button(s, key=s, use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 Load Live eBird Data", use_container_width=True):
            with st.spinner("Fetching..."):
                st.session_state.ebird_data = fetch_ebird_sightings()
            total = len(st.session_state.ebird_data['hawaii']) + len(st.session_state.ebird_data['alaska'])
            st.success(f"✅ {total} real sightings loaded")
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
        st.markdown('<div class="warn">⚠️ Educational use only. Consult an ornithologist for professional wildlife advice.</div>', unsafe_allow_html=True)

# ── TAB 2: MAP ────────────────────────────────────────
with tab2:
    st.markdown('<div class="sec-hdr">Alaska → Hawaii Migration Map</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box">
    <b style="color:#d4a820;">📍 How to read this map:</b><br>
    <b style="color:#d4a820;">🟡 Gold dots</b> = Breeding grounds in Arctic Alaska where Kōlea nest each summer (May–Jul).<br>
    <b style="color:#2a90a8;">🔵 Teal dots</b> = Hawaiian wintering islands where they spend 8 months (Aug–Apr).<br>
    <b>Dashed gold line</b> = Their actual non-stop flight path over the open Pacific — no islands, no stops.<br>
    <b>Click any dot</b> to see full habitat data for that site.
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    km, miles = haversine(64.0, -165.0, 21.0, -157.0)
    ebird_total = len(st.session_state.ebird_data['hawaii']) + len(st.session_state.ebird_data['alaska'])
    with c1:
        st.markdown(f'<div class="s-card"><div class="s-val">{km:,} km</div><div class="s-lbl">Non-stop flight distance</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="s-card"><div class="s-val">{ebird_total}</div><div class="s-lbl">Live eBird sightings</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="s-card"><div class="s-val">{len(habitat_df)}</div><div class="s-lbl">Habitat sites tracked</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    with st.spinner("Rendering map..."):
        st_html(build_map(habitat_df, st.session_state.ebird_data), height=560)

# ── TAB 3: HABITAT DATA ───────────────────────────────
with tab3:
    st.markdown('<div class="sec-hdr">Satellite Habitat Analysis</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box">
    <b style="color:#d4a820;">🛰️ What this data means:</b> &nbsp;
    <b>NDVI</b> (0–1) measures vegetation greenness from satellite imagery — higher means richer, greener habitat.
    <b>Suitability</b> (0–1) is a composite score combining NDVI, temperature, and elevation.
    <b>Population</b> is the estimated number of Kōlea using each site per season.
    </div>
    """, unsafe_allow_html=True)

    col_b, col_w = st.columns(2)
    with col_b:
        st.markdown("#### 🟡 Breeding Grounds — Alaska (May–July)")
        b_df = habitat_df[habitat_df['site_type']=='breeding'][
            ['site_name','ndvi','mean_temp_c','elevation_m','habitat_suitability','pop_estimate']].copy()
        b_df.columns = ['Site','NDVI','Temp °C','Elev m','Suitability','Population']
        st.dataframe(b_df, use_container_width=True, hide_index=True)
    with col_w:
        st.markdown("#### 🔵 Wintering Grounds — Hawaii (Aug–April)")
        w_df = habitat_df[habitat_df['site_type']=='wintering'][
            ['site_name','ndvi','mean_temp_c','elevation_m','habitat_suitability','pop_estimate']].copy()
        w_df.columns = ['Site','NDVI','Temp °C','Elev m','Suitability','Population']
        st.dataframe(w_df, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.markdown("#### 📏 Flight Distance Calculator")
    st.markdown('<div style="font-size:0.82rem;color:#687860;margin-bottom:14px;">Pick any Alaska site and any Hawaii island to calculate the exact migration distance between them.</div>', unsafe_allow_html=True)
    dc1, dc2 = st.columns(2)
    with dc1:
        site1 = st.selectbox("From — Alaska breeding site", [s['name'] for s in BREEDING_SITES])
    with dc2:
        site2 = st.selectbox("To — Hawaii wintering site", [s['name'] for s in WINTERING_SITES])
    all_sites = BREEDING_SITES + WINTERING_SITES
    s1 = next(s for s in all_sites if s['name'] == site1)
    s2 = next(s for s in all_sites if s['name'] == site2)
    km2, miles2 = haversine(s1['lat'], s1['lon'], s2['lat'], s2['lon'])
    st.markdown(f"""
    <div class='s-card' style='margin-top:14px;'>
      <div style='font-size:0.77rem;color:#687860;margin-bottom:8px;'>{site1} &nbsp;→&nbsp; {site2}</div>
      <div class='s-val'>{km2:,} km &nbsp;·&nbsp; {miles2:,} miles</div>
      <div class='s-lbl'>Over open Pacific Ocean · Non-stop · No landmarks</div>
    </div>""", unsafe_allow_html=True)

    if len(st.session_state.ebird_data['hawaii']) > 0:
        st.markdown("---")
        st.markdown("#### 🐦 Recent eBird Sightings — Hawaii")
        ebird_records = [{'Location': o.get('locName','Unknown'), 'Date': o.get('obsDt','Unknown'),
            'Count': o.get('howMany',1), 'Region': 'Hawaii'}
            for o in st.session_state.ebird_data['hawaii'][:10]]
        if ebird_records:
            st.dataframe(pd.DataFrame(ebird_records), use_container_width=True, hide_index=True)

st.markdown('</div>', unsafe_allow_html=True)