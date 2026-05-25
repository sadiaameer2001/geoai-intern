# 🤖 RAG Chatbot — Task 4

## Retrieval-Augmented Generation with FEMA Flood Documents

This task builds a RAG (Retrieval-Augmented Generation) chatbot that answers questions about FEMA flood risk management documents. Users can ask natural language questions and receive answers grounded in the uploaded PDF documents.

---

## 📌 Pipeline Overview

1. **Load PDF Documents** — FEMA risk map and urban flooding guidance PDFs
2. **Chunk & Embed** — Split documents into chunks and generate embeddings
3. **Vector Store** — Store embeddings in FAISS for fast similarity search
4. **RAG Chain** — Retrieve relevant chunks and generate answers using an LLM
5. **Chatbot Interface** — Streamlit web app for interactive Q&A

---

## 🗂️ Files

| File | Description |
|------|-------------|
| `Task4_RAG_Chatbot_FIXED.ipynb` | Main Jupyter notebook |
| `app.py` | Streamlit chatbot web application |
| `.gitignore` | Excludes `.env` and API keys |
| `Data/` | FEMA source PDF documents |
| `vectorstore/index.faiss` | FAISS vector index (prebuilt) |
| `vectorstore/index.pkl` | Vector store metadata |

---

## 📄 Source Documents

| Document | Description |
|----------|-------------|
| `fema_risk-map-phase-1-factsheet.pdf` | FEMA Risk MAP Phase 1 |
| `fema_risk-map-phase-2-factsheet.pdf` | FEMA Risk MAP Phase 2 |
| `fema_risk-map-phase-3-factsheet.pdf` | FEMA Risk MAP Phase 3 |
| `fema_risk-map-phase-4-factsheet.pdf` | FEMA Risk MAP Phase 4 |
| `fema_urban_flooding_guidance.pdf` | Urban Flooding Guidance for Homeowners & Renters |

---

## ⚙️ Setup & Installation

```bash
pip install langchain openai faiss-cpu pypdf streamlit python-dotenv
```

### API Key Setup

Create a `.env` file in the Task4 folder (already in `.gitignore`):

```
OPENAI_API_KEY=your_key_here
```

> ⚠️ Never commit your `.env` file or API key to GitHub.

---

## 🚀 Running the Chatbot

```bash
streamlit run app.py
```

Then open `http://localhost:8501` in your browser.

---

## 🤖 Architecture

```
User Question
     ↓
Embedding Model
     ↓
FAISS Vector Search → Top-k Relevant Chunks
     ↓
LLM (GPT) + Retrieved Context
     ↓
Grounded Answer
```

| Component | Tool |
|-----------|------|
| Document Loader | LangChain PyPDFLoader |
| Text Splitting | LangChain RecursiveCharacterTextSplitter |
| Embeddings | OpenAI Embeddings |
| Vector Store | FAISS |
| LLM | OpenAI GPT |
| Interface | Streamlit |

---

## 💡 What is RAG?

RAG (Retrieval-Augmented Generation) combines a **retrieval system** (finds relevant document chunks) with a **generative model** (produces answers). This means the chatbot answers are grounded in actual document content rather than hallucinated — making it accurate and trustworthy for domain-specific Q&A.

---

## 🔧 Requirements

- Python 3.8+
- langchain
- openai
- faiss-cpu
- pypdf
- streamlit
- python-dotenv
