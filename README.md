# LLM Knowledge Extractor

Welcome to the **LLM Knowledge Extractor** project.  
This repository contains a small prototype to analyze unstructured text using an LLM.  

👉 For details, see the following docs:

- [Description](DESCRIPTION.md)
- [Setup Instructions](SETUP.md)
- [Deliverables](DELIVERABLES.md)
- [Design Choices](DESIGN_CHOICES.md)
- [Trade-offs](TRADEOFFS.md)

# 📖 Description

A small prototype to analyze unstructured text using an LLM, producing:

- **1–2 sentence summary**
- **Structured metadata**: title, topics, sentiment, keywords
- **Confidence score**

Users can analyze text and search past analyses by topic or keyword.

# ⚙️ Setup

## 1. Create Virtual Environment
```bash
python -m venv venv
```
Activate Enviorment for windows
```bash
venv\Scripts\activate
```
Activate Enviorment for Mac
```bash
source venv/bin/activate
```

Install Dependencies
```bash
pip install -r requirements.txt
```
Run the App
```bash
uvicorn app.main:app --reload
```

# 📦 Deliverables

- **Setup and Run Instructions**  
(See [Setup](SETUP.md) for details.)

# ⚖️ Trade-offs

- **Time Constraints**: Due to the 2-hour timebox, advanced features like authentication, pagination, and Docker setup were not included.  
- **Sentiment Analysis**: Implemented a basic, rule-based approach instead of a sophisticated ML model.  
- **Error Handling**: Minimal — enough to catch empty input and mock API failures, but not fully production-grade.