# tests/test_extractor.py
from app.extractor import top_n_keywords

def test_top_keywords_simple():
    text = "Python is great. Python programming and data science use Python a lot."
    kws = top_n_keywords(text, n=3)
    assert "python" in kws
