# app/db.py
import sqlite3
from dataclasses import dataclass
from typing import List, Optional
import json
import os
from datetime import datetime

DB_PATH = os.getenv("LKE_DB", "analyses.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS analyses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT,
        summary TEXT,
        metadata TEXT,
        topics TEXT,
        keywords TEXT,
        created_at TEXT
    )
    """)
    conn.commit()
    conn.close()


@dataclass
class AnalysisRecord:
    text: str
    summary: str
    metadata: str
    topics: str
    keywords: str

def save_analysis(record: AnalysisRecord) -> int:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    created_at = datetime.utcnow().isoformat()
    c.execute("""
    INSERT INTO analyses (text, summary, metadata, topics, keywords, created_at)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (record.text, record.summary, record.metadata, record.topics, record.keywords, created_at))
    conn.commit()
    rowid = c.lastrowid
    conn.close()
    return rowid

def search_analyses(topic: Optional[str] = None, keyword: Optional[str] = None) -> List[dict]:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, text, summary, metadata, topics, keywords, created_at FROM analyses")
    rows = c.fetchall()
    results = []

    for r in rows:
        topics_list = json.loads(r[4]) if r[4] else []
        keywords_list = json.loads(r[5]) if r[5] else []

        # Filter by topic if provided
        if topic and not any(topic.lower() in t.lower() for t in topics_list):
            continue

        # Filter by keyword if provided
        if keyword and not any(keyword.lower() in k.lower() for k in keywords_list):
            continue

        results.append({
            "id": r[0],
            "text": r[1],
            "summary": r[2],
            "metadata": json.loads(r[3]) if r[3] else {},
            "topics": topics_list,
            "keywords": keywords_list,
            "created_at": r[6],
        })

    conn.close()
    return results

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    query = "SELECT id, text, summary, metadata, topics, keywords, created_at FROM analyses WHERE 1=1"
    params = []
    if topic:
        query += " AND topics LIKE ?"
        params.append(f"%{topic}%")
    if keyword:
        query += " AND keywords LIKE ?"
        params.append(f"%{keyword}%")
    c.execute(query, params)
    rows = c.fetchall()
    results = []
    for r in rows:
        results.append({
            "id": r[0],
            "text": r[1],
            "summary": r[2],
            "metadata": json.loads(r[3]) if r[3] else {},
            "topics": json.loads(r[4]) if r[4] else [],
            "keywords": json.loads(r[5]) if r[5] else [],
            "created_at": r[6],
        })
    conn.close()
    return results
