# LLM Knowledge Extractor (prototype)

## What it does
- Accepts a block of text and returns:
  - 1-2 sentence summary
  - structured metadata JSON (title, topics, sentiment)
  - keywords (3 most frequent nouns — implemented locally)
  - confidence score (naive heuristic)
- Stores each analysis in a SQLite DB.
- Provides endpoints:
  - POST /analyze
  - GET /search?topic=xyz or ?keyword=abc

## Setup (local)
1. Create & activate a virtual environment (recommended):
   ```
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # mac / linux:
   source venv/bin/activate
   ```
2. Install requirements:
   ```
   pip install -r requirements.txt
   ```
3. Run the app:
   ```
   uvicorn app.main:app --reload
   ```
   Server will start on http://127.0.0.1:8000

## Usage examples
Analyze text:
```
curl -X POST "http://127.0.0.1:8000/analyze" -H "Content-Type: application/json" -d '{"text":"OpenAI released a new model. It is very powerful and useful for many tasks. Research shows improvements."}'
```
Search:
```
curl "http://127.0.0.1:8000/search?topic=openai"
```

## Notes
- If you want to use a real OpenAI key, set environment variable `OPENAI_API_KEY`. If not set, the service uses a deterministic fallback.
- DB file `analyses.db` will be created in the working directory by default.

## Design choices (short)
FastAPI for quick API development, SQLite for light persistence, a pluggable LLM wrapper (mock or OpenAI), and a small local keyword extractor to satisfy the assignment requirement.
