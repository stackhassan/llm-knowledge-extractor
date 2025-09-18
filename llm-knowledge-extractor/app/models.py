# app/models.py
# (Optional Pydantic models if you want stricter typing in responses)
from pydantic import BaseModel
from typing import List, Optional

class AnalyzeResponse(BaseModel):
    id: int
    summary: str
    metadata: dict
    confidence: float
