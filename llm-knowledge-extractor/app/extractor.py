# app/extractor.py
import re
from collections import Counter
from typing import List

STOPWORDS = {
    "the","and","a","an","in","on","with","for","of","to","is","are","that","this","it",
    "as","by","from","at","be","has","have","was","were","or","we","you","i","he","she","they"
}

def tokenize(text: str) -> List[str]:
    words = re.findall(r"\b[a-zA-Z0-9\-']+\b", text.lower())
    return words

def top_n_keywords(text: str, n: int = 3) -> List[str]:
    """
    Naive implementation to return the top N frequent candidate "nouns".
    We do not use LLM nor external NLP libs to satisfy the requirement.
    Heuristics:
      - tokenize
      - remove stopwords
      - prefer words longer than 2 chars and not numeric only
      - return the top N by frequency
    """
    words = tokenize(text)
    candidates = [w for w in words if w not in STOPWORDS and len(w) > 2 and not w.isdigit()]
    counts = Counter(candidates)
    top = [w for w,_ in counts.most_common(n)]
    return top
