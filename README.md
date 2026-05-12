# 🚀 SHL Conversational Assessment Recommendation Agent

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi)
![FAISS](https://img.shields.io/badge/FAISS-Vector_Search-orange?style=for-the-badge)
![BM25](https://img.shields.io/badge/BM25-Hybrid_Retrieval-red?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)

### Intelligent conversational assessment recommendation backend for SHL catalog exploration

</div>

---

# ✨ Overview

The **SHL Conversational Assessment Recommendation Agent** is a retrieval-driven recommendation backend designed to help recruiters and hiring teams discover relevant SHL assessments efficiently through natural language queries.

The system combines:

- Semantic retrieval
- Hybrid search
- Context-aware recommendation refinement
- Conversational memory
- Intelligent reranking
- Explainable recommendations

to improve assessment discovery and recommendation quality.

---

# 🎯 Problem Statement

Recruiters and hiring teams often face challenges while:

- Searching through large assessment catalogs
- Matching assessments to job roles accurately
- Refining hiring requirements conversationally
- Discovering relevant assessments quickly

This project addresses these challenges using a retrieval-oriented recommendation pipeline.

---

# 🔥 Key Features

## ✅ Conversational Recommendation Workflow

Supports multi-turn conversations with contextual recommendation refinement.

---

## ✅ Hybrid Retrieval Architecture

Combines:

- FAISS semantic vector search
- BM25 lexical retrieval

for improved recommendation quality and Recall@10 performance.

---

## ✅ Query Expansion

Enhances user queries using domain-aware keyword expansion strategies.

---

## ✅ Intelligent Reranking

Post-retrieval reranking improves recommendation precision for technical and business-oriented roles.

---

## ✅ Explainable Recommendations

Every recommendation includes contextual reasoning.

---

## ✅ Context-Aware Retrieval

Conversation history is used to refine future recommendations.

---

## ✅ Off-topic Guardrails

Handles unrelated queries gracefully.

---

## ✅ Vague Query Clarification

Prompts users for additional hiring context before recommending assessments.

---

## ✅ FastAPI Backend

Clean modular backend architecture with scalable service separation.

---

## ✅ Swagger Documentation

Interactive API documentation through FastAPI OpenAPI support.

---

# 🏗️ System Architecture

```text
User Query
    ↓
Conversation Memory
    ↓
Query Expansion
    ↓
Hybrid Retrieval
(FAISS + BM25)
    ↓
Intelligent Reranking
    ↓
Explainable Recommendations
    ↓
FastAPI Response
```

---

# 🧠 Retrieval Pipeline

## 1️⃣ Catalog Scraping

The SHL product catalog is dynamically scraped using Selenium.

Collected information includes:

- Assessment names
- URLs
- Metadata
- Assessment attributes

---

## 2️⃣ Embedding Generation

Assessment descriptions are converted into dense vector embeddings using:

```python
sentence-transformers/all-MiniLM-L6-v2
```

---

## 3️⃣ Semantic Search

FAISS is used for fast vector similarity search across assessment embeddings.

---

## 4️⃣ Lexical Retrieval

BM25 improves exact keyword matching and technical retrieval precision.

---

## 5️⃣ Hybrid Retrieval

Semantic and lexical retrieval results are merged for improved retrieval stability.

---

## 6️⃣ Reranking

Results are reranked using domain-aware heuristics for improved recommendation quality.

---

## 7️⃣ Context Handling

Conversation history is used to refine retrieval for follow-up queries.

---

# 🛠️ Tech Stack

| Category | Technology |
|---|---|
| Backend Framework | FastAPI |
| Language | Python 3.11 |
| Semantic Search | FAISS |
| Lexical Retrieval | BM25 |
| Embeddings | Sentence Transformers |
| Web Scraping | Selenium |
| API Documentation | Swagger / OpenAPI |
| Deployment | Railway |

---

# 📂 Project Structure

```text
shl-assessment-agent/
│
├── app/
│   ├── routes/
│   ├── services/
│   ├── models/
│   ├── prompts/
│   └── utils/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── embeddings/
│
├── evaluation/
├── scripts/
├── tests/
│
├── README.md
├── requirements.txt
├── Procfile
├── startup.sh
└── runtime.txt
```

---

# ⚙️ Installation & Setup

## 1️⃣ Clone Repository

```bash
git clone <YOUR_GITHUB_REPO>
cd SHL-Assignment
```

---

## 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

---

## 3️⃣ Activate Environment

### Windows

```bash
venv\Scripts\activate
```

### Mac/Linux

```bash
source venv/bin/activate
```

---

## 4️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Running The Application

## Start FastAPI Server

```bash
python -m uvicorn app.main:app --reload
```

---

# 📘 API Documentation

After starting the server:

```text
http://127.0.0.1:8000/docs
```

---

# 🧪 Sample Requests

## 🔹 Java Backend Hiring

```json
{
  "session_id": "java_user",
  "query": "Need assessments for Java backend developers"
}
```

---

## 🔹 Leadership Hiring

```json
{
  "session_id": "manager_user",
  "query": "Need leadership and managerial assessments for senior team leads"
}
```

---

## 🔹 Sales Hiring

```json
{
  "session_id": "sales_user",
  "query": "Need customer-facing sales and communication assessments"
}
```

---

# 📊 Example Response

```json
{
  "response": "For the ongoing conversation, I identified 10 relevant SHL assessments using context-aware hybrid retrieval and intelligent reranking.",
  "recommendations": [
    {
      "name": "Java 8 (New)",
      "url": "https://www.shl.com/",
      "attributes": [
        "Knowledge & Skills"
      ],
      "reason": "Recommended because it evaluates Java programming and backend development skills."
    }
  ]
}
```

---

# 🧪 Evaluation-Oriented Features

The system includes features focused on robust conversational evaluation:

- Schema-compliant responses
- Catalog-only recommendations
- Turn-cap enforcement
- Off-topic refusal handling
- Vague-query clarification
- Context-aware retrieval refinement
- Explainable recommendation generation

---

# 🛡️ Behavioral Handling

The assistant:

- Refuses unrelated queries
- Avoids hallucinated recommendations
- Requests clarification for vague hiring requests
- Maintains bounded conversational memory

---

# 🚀 Deployment

The application is designed for deployment on:

- Railway
- Render
- Docker-based environments

## Railway Start Command

```bash
web: bash startup.sh
```

---

# 📈 Future Improvements

- Metadata-aware filtering
- Persistent conversation memory
- Frontend dashboard
- Analytics support
- Assessment comparison workflow
- Role-based recommendation templates

---

# 📚 References

## FastAPI

https://fastapi.tiangolo.com/

---

## FAISS

https://github.com/facebookresearch/faiss

---

## Sentence Transformers

https://www.sbert.net/

---

## BM25 Ranking

https://pypi.org/project/rank-bm25/

---

## Selenium

https://www.selenium.dev/

---

# 👨‍💻 Author

### Sourabh Alimchandani

AI/ML Enthusiast • Cybersecurity Enthusiast • Prompt Engineer • Backend Developer


---

# ⭐ Final Notes

This project was built with a focus on:

- Retrieval engineering
- Scalable backend architecture
- Conversational recommendation workflows
- Production-oriented API design

The goal was to build a robust conversational assessment recommendation platform capable of handling realistic hiring-oriented recommendation workflows.

---

<div align="center">

### 🚀 FastAPI • FAISS • BM25 • Retrieval Engineering

</div>