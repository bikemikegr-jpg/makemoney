# Personal AI — Minimal Prototype

This project is a starting point for a Personal AI assistant using embeddings + retrieval + a language model.

Features
- Ingest local text files into a Chroma vector store
- Chat endpoint that uses retrieval-augmented generation (RAG)
- Simple Streamlit UI for chat

Requirements
- Python 3.10+
- An OpenAI API key (or configure a local LLM backend)

Quickstart
1. Create a virtualenv:
   python -m venv .venv && source .venv/bin/activate
2. Install dependencies:
   pip install -r requirements.txt
3. Create `.env` from `.env.example` and add your OPENAI_API_KEY.
4. Ingest files:
   python ingest.py --path ./data
5. Run API:
   uvicorn app:app --reload --port 8000
6. Run UI (optional):
   streamlit run streamlit_app.py

Notes
- To use a local model replace `OpenAI` calls with your chosen inference endpoint or local runner.
- For production, secure your API and encrypt vector store files.
