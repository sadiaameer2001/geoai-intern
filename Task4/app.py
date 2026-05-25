import streamlit as st
from streamlit_folium import st_folium
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from pathlib import Path
from dotenv import load_dotenv
import spacy
from geopy.geocoders import Nominatim
import folium
import os
import warnings
warnings.filterwarnings('ignore')

# ── Paths ──────────────────────────────────────────────────────────
BASE_DIR         = Path(r'D:\OneDrive - National University of Sciences & Technology\internship\geoai\LangChain RAG Chatbot')
VECTORSTORE_PATH = BASE_DIR / 'vectorstore'
ENV_PATH         = BASE_DIR / '.env'

load_dotenv(dotenv_path=ENV_PATH)

# ── Page config ────────────────────────────────────────────────────
st.set_page_config(
    page_title="Geo-Aware RAG Chatbot",
    page_icon="🗺️",
    layout="wide"
)

st.title("🗺️ Geo-Aware RAG Chatbot")
st.caption("Powered by LangChain · Groq LLaMA3 · FEMA Flood Documents · GIS Location Mapping")
st.divider()

# ── Load models (cached) ───────────────────────────────────────────
@st.cache_resource
def load_nlp():
    return spacy.load('en_core_web_sm')

@st.cache_resource
def load_chain():
    embeddings = HuggingFaceEmbeddings(
        model_name='all-MiniLM-L6-v2',
        model_kwargs={'device': 'cpu'}
    )
    vectorstore = FAISS.load_local(
        str(VECTORSTORE_PATH),
        embeddings,
        allow_dangerous_deserialization=True
    )
    retriever = vectorstore.as_retriever(search_kwargs={'k': 4})

    llm = ChatGroq(
        model_name='llama-3.3-70b-versatile',
        api_key=os.getenv('GROQ_API_KEY'),
        temperature=0.2
    )

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    prompt = PromptTemplate.from_template("""
You are a helpful assistant that answers questions about flood zones, FEMA programs, and city geography.
Use the following context to answer the question. If you don't know, say so.

Context:
{context}

Question: {question}

Answer:""")

    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain

# ── GIS helpers ────────────────────────────────────────────────────
geolocator = Nominatim(user_agent='geo_rag_chatbot_v1')

def extract_locations(text, nlp):
    doc = nlp(text)
    return list({ent.text for ent in doc.ents if ent.label_ in ['GPE', 'LOC', 'FAC']})

def geocode_locations(names):
    results = []
    for name in names:
        try:
            loc = geolocator.geocode(name, timeout=5)
            if loc:
                results.append({
                    'name': name,
                    'lat': loc.latitude,
                    'lon': loc.longitude
                })
        except:
            pass
    return results

def build_map(locations):
    if not locations:
        return None
    center = [locations[0]['lat'], locations[0]['lon']]
    m = folium.Map(location=center, zoom_start=4, tiles='CartoDB positron')
    for loc in locations:
        folium.Marker(
            location=[loc['lat'], loc['lon']],
            popup=folium.Popup(f"<b>{loc['name']}</b>", max_width=200),
            tooltip=loc['name'],
            icon=folium.Icon(color='blue', icon='info-sign')
        ).add_to(m)
    return m

# ── Load resources ─────────────────────────────────────────────────
with st.spinner('Loading AI models...'):
    try:
        nlp   = load_nlp()
        chain = load_chain()
        st.success('✅ Models loaded! Ask me anything about flood zones, FEMA, or US cities.')
    except Exception as e:
        st.error(f'❌ Error loading models: {e}')
        st.info('Make sure you ran the ingestion notebook first (Step 3).')
        st.stop()

# ── Suggested questions ────────────────────────────────────────────
st.subheader("💡 Try asking:")
example_questions = [
    "What is the FEMA Risk MAP program?",
    "What happens during the flood map discovery phase?",
    "What are flood risk zones in urban areas?",
    "How does FEMA notify communities about new flood maps?",
    "What is the National Flood Insurance Program?",
]
cols = st.columns(len(example_questions))
for i, (col, q) in enumerate(zip(cols, example_questions)):
    if col.button(q, key=f'q{i}', use_container_width=True):
        st.session_state['prefill'] = q

# ── Chat history ───────────────────────────────────────────────────
if 'history' not in st.session_state:
    st.session_state['history'] = []

# ── Input ──────────────────────────────────────────────────────────
prefill = st.session_state.pop('prefill', '')
query   = st.text_input(
    "Ask a question:",
    value=prefill,
    placeholder="e.g. What are the flood-risk zones near downtown Chicago?",
    key='query_input'
)

if query:
    with st.spinner('Thinking...'):
        answer = chain.invoke(query)

    st.session_state['history'].append({'q': query, 'a': answer})

    col1, col2 = st.columns([1, 1], gap='large')

    with col1:
        st.subheader("💬 Answer")
        st.write(answer)

    with col2:
        st.subheader("📍 GIS Map")
        locs   = extract_locations(answer, nlp)
        coords = geocode_locations(locs)

        if coords:
            st.caption(f"Locations detected: **{', '.join([c['name'] for c in coords])}**")
            fmap = build_map(coords)
            st_folium(fmap, width=550, height=400, returned_objects=[])
        else:
            st.info("No specific locations detected in this answer.")
            m = folium.Map(location=[39, -98], zoom_start=4, tiles='CartoDB positron')
            st_folium(m, width=550, height=400, returned_objects=[])

# ── Chat history display ───────────────────────────────────────────
if len(st.session_state['history']) > 1:
    st.divider()
    st.subheader("🕘 Previous Questions")
    for item in reversed(st.session_state['history'][:-1]):
        with st.expander(f"❓ {item['q']}"):
            st.write(item['a'])