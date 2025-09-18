# from fastapi import FastAPI
# from pydantic import BaseModel
# from typing import Optional, List
# import json
# from app.llm_wrapper import generate_summary_and_metadata
# from app.db import init_db, save_analysis, search_analyses, AnalysisRecord
# from app.extractor import top_n_keywords

# app = FastAPI(title="LLM Knowledge Extractor")
# init_db()  # create tables if not exists

# class AnalyzeRequest(BaseModel):
#     text: str

# @app.get("/")
# def root():
#     return {"message": "LLM Knowledge Extractor API is running 🚀"}

# @app.post("/analyze", response_model=dict)
# async def analyze(req: AnalyzeRequest):
#     text = (req.text or "").strip()
#     if not text:
#         return {"error": "Empty input provided."}

#     try:
#         llm_result = generate_summary_and_metadata(text)
#     except Exception as e:
#         return {"error": "LLM call failed", "details": str(e)}

#     keywords = top_n_keywords(text, n=3)
#     metadata = llm_result.get("metadata", {})
#     metadata["keywords"] = keywords

#     confidence = llm_result.get("confidence", None)
#     if confidence is None:
#         confidence = round(0.5 + 0.1 * len([k for k in keywords if k]), 2)
#         llm_result["confidence"] = confidence

#     record = AnalysisRecord(
#         text=text,
#         summary=llm_result.get("summary", ""),
#         metadata=json.dumps(metadata),
#         topics=json.dumps(metadata.get("topics", [])),
#         keywords=json.dumps(keywords),
#     )
#     saved = save_analysis(record)
#     response = {
#         "id": saved,
#         "summary": llm_result.get("summary"),
#         "metadata": metadata,
#         "confidence": llm_result.get("confidence"),
#     }
#     return response

# @app.get("/search", response_model=List[dict])
# async def search(topic: Optional[str] = None, keyword: Optional[str] = None):
#     results = search_analyses(topic=topic, keyword=keyword)
#     return results

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from app.llm_wrapper import generate_summary_and_metadata
from app.db import init_db, save_analysis, search_analyses, AnalysisRecord
from app.extractor import top_n_keywords
import json

app = FastAPI(title="LLM Knowledge Extractor")
init_db()

# Templates setup
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/ui/analyze", response_class=HTMLResponse)
async def analyze_ui(request: Request, text: str = Form(...)):
    if not text.strip():
        return templates.TemplateResponse("index.html", {"request": request, "error": "Empty input!"})

    try:
        llm_result = generate_summary_and_metadata(text)
    except Exception as e:
        return templates.TemplateResponse("index.html", {"request": request, "error": f"LLM failed: {e}"})

    keywords = top_n_keywords(text, n=3)
    metadata = llm_result.get("metadata", {})
    metadata["keywords"] = keywords
    confidence = llm_result.get("confidence", round(0.5 + 0.1 * len(keywords), 2))

    record = AnalysisRecord(
        text=text,
        summary=llm_result.get("summary", ""),
        metadata=json.dumps(metadata),
        topics=json.dumps(metadata.get("topics", [])),
        keywords=json.dumps(keywords),
    )
    save_analysis(record)

    return templates.TemplateResponse("index.html", {
        "request": request,
        "summary": llm_result.get("summary"),
        "metadata": metadata,
        "confidence": confidence,
    })


@app.post("/ui/search", response_class=HTMLResponse)
async def search_ui(request: Request, topic: str = Form(""), keyword: str = Form("")):
    results = search_analyses(topic=topic or None, keyword=keyword or None)
    return templates.TemplateResponse("index.html", {"request": request, "results": results})
