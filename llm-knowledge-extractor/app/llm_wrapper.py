# app/llm_wrapper.py
import os
import re
from typing import Dict, Any
from datetime import datetime

# Optional: use openai if available and configured
try:
    import openai
    OPENAI_AVAILABLE = True
except Exception:
    OPENAI_AVAILABLE = False

# Basic word lists for simple sentiment heuristic
POSITIVE_WORDS = {"good", "great", "positive", "success", "happy", "improve", "benefit"}
NEGATIVE_WORDS = {"bad", "error", "fail", "negative", "problem", "loss", "worse"}

def _first_sentences(text: str, max_sentences: int = 2):
    # naive sentence split
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    return " ".join(sentences[:max_sentences]).strip()

def _naive_topics(text: str, n=3):
    # pick top distinct words (excluding stopwords) as topics (very naive)
    from collections import Counter
    import string
    stopwords = {
        "the","and","a","an","in","on","with","for","of","to","is","are","that","this","it"
    }
    words = re.findall(r"\b\w+\b", text.lower())
    words = [w.strip(string.punctuation) for w in words if w not in stopwords and len(w)>3]
    counts = Counter(words)
    return [t for t,_ in counts.most_common(n)]

def _naive_sentiment(text: str):
    t = text.lower()
    pos = sum(1 for w in POSITIVE_WORDS if w in t)
    neg = sum(1 for w in NEGATIVE_WORDS if w in t)
    if pos > neg: return "positive"
    if neg > pos: return "negative"
    return "neutral"

def generate_summary_and_metadata(text: str) -> Dict[str, Any]:
    """
    Tries to call an LLM (OpenAI) if api key present; otherwise returns a strong mock result.
    Returns a dict:
      { "summary": "...", "metadata": { "title":..., "topics":[...], "sentiment":..., "keywords":[...] }, "confidence": 0.8 }
    """
    api_key = os.getenv("OPENAI_API_KEY") or os.getenv("OPENAI_API")
    if api_key and OPENAI_AVAILABLE:
        try:
            openai.api_key = api_key
            prompt = (
                "You are a concise summarizer and extractor. "
                "Given the following TEXT, produce a short (1-2 sentence) summary, "
                "a title if present, 3 key topics as an array, and sentiment (positive/neutral/negative). "
                "Reply as JSON with keys: summary, title, topics, sentiment."
                f"\n\nTEXT:\n{text}\n\nJSON:"
            )
            resp = openai.Completion.create(
                model="text-davinci-003",
                prompt=prompt,
                max_tokens=256,
                temperature=0.2,
            )
            content = resp.choices[0].text.strip()
            # Try to extract JSON from content
            import json
            obj = None
            try:
                obj = json.loads(content)
            except Exception:
                # naive fallback: pick first sentence as summary and compute metadata
                obj = {
                    "summary": _first_sentences(text),
                    "title": None,
                    "topics": _naive_topics(text),
                    "sentiment": _naive_sentiment(text),
                }
            return {"summary": obj.get("summary"), "metadata": obj, "confidence": 0.85}
        except Exception as e:
            # propagate to caller to handle LLM failure gracefully
            raise RuntimeError(f"LLM call failed: {e}")
    else:
        # MOCK / fallback behavior (deterministic)
        summary = _first_sentences(text, max_sentences=2)
        title_guess = text.strip().splitlines()[0][:120]  # first line or trimmed
        topics = _naive_topics(text, n=3)
        sentiment = _naive_sentiment(text)
        metadata = {
            "title": title_guess,
            "topics": topics,
            "sentiment": sentiment,
        }
        # confidence: naive heuristic based on text length and topics present
        confidence = round(min(0.95, 0.4 + min(0.5, len(text) / 1000) + 0.05 * len(topics)), 2)
        return {"summary": summary, "metadata": metadata, "confidence": confidence}
