# LLM Knowledge Extractor

## Description
A small prototype to analyze unstructured text using an LLM, producing:
- 1–2 sentence summary
- Structured metadata: title, topics, sentiment, keywords
- Confidence score

Users can analyze text and search past analyses by topic or keyword.

---

## Setup

1. Create virtual environment:

```bash
python -m venv venv
# Activate
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
Install dependencies:

pip install -r requirements.txt


Run the app:

uvicorn app.main:app --reload


Open browser at: http://127.0.0.1:8000/