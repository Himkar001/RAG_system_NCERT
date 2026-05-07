# Stage 2 README — NCERT Smart Assistant

You can create a new file:

```text id="7h2jgl"
README_STAGE2.md
```

and paste this content.

---

# NCERT Smart Assistant — Stage 2

## Overview

Stage 2 focuses on transforming the initial NCERT RAG prototype into a more intelligent and modular AI tutoring system.

The system now supports:

* Semantic retrieval
* Hybrid retrieval
* Equation handling
* Numerical problem routing
* Image retrieval
* Memory handling
* FastAPI backend
* React frontend interface

This stage establishes the backend and frontend architecture required for scaling the project into a complete NCERT AI tutor.

---

# Stage 1 vs Stage 2

## Stage 1 (Prototype)

The Stage 1 prototype included:

* PDF extraction using `pdfplumber`
* Text cleaning
* BERT tokenizer-based chunking
* BM25 retrieval
* Gemini-based answer generation

### Limitations

* Weak semantic understanding
* Poor handling of equations
* No numerical solving
* No image retrieval
* No memory
* Large chunk retrieval noise
* Basic notebook-only implementation

---

## Stage 2 Goals

Stage 2 was designed to solve these limitations by introducing:

* Modular backend architecture
* Intelligent query routing
* Semantic retrieval
* Hybrid retrieval
* Equation and numerical handlers
* Image retrieval pipeline
* Frontend chat interface
* API-based interaction

---

# Project Architecture

```text id="l2y6yk"
User Query
    ↓
Frontend (React)
    ↓
FastAPI Backend
    ↓
Query Router
    ↓
┌─────────────────────┐
│ Retrieval Handlers  │
├─────────────────────┤
│ BM25 Retrieval      │
│ Semantic Retrieval  │
│ Hybrid Retrieval    │
│ Equation Handler    │
│ Numerical Handler   │
│ Image Handler       │
│ Memory Handler      │
└─────────────────────┘
    ↓
Prompt Builder
    ↓
Gemini API
    ↓
Frontend Response
```

---

# Features Implemented

## 1. Semantic Retrieval

Implemented semantic search using transformer embeddings.

### Goal

Improve retrieval for conceptually similar queries.

### Example

```text id="2thupx"
Query:
"Why does an object resist change?"

Traditional BM25:
May fail to retrieve "inertia"

Semantic Retrieval:
Correctly retrieves inertia-related chunks
```

---

## 2. Hybrid Retrieval

Combined:

* BM25 keyword retrieval
* Semantic similarity retrieval

### Goal

Improve both precision and recall.

---

## 3. Equation Handler

Implemented routing and handling for equation-related queries.

### Examples

```text id="y9jzfc"
Explain F = ma
Explain v = u + at
Equation for momentum
```

---

## 4. Numerical Handler

Implemented basic numerical problem solving.

### Examples

```text id="d0db1n"
Find force when mass = 5kg and acceleration = 2m/s²
```

---

## 5. Image Retrieval

Implemented OCR-based image retrieval system.

### Pipeline

* Extract rendered PDF pages
* OCR text extraction
* Metadata generation
* Query-image matching

---

## 6. Memory Handling

Implemented short-term conversational memory.

### Goal

Enable context-aware conversations.

---

## 7. FastAPI Backend

Built modular backend using FastAPI.

### Features

* Query routing
* API endpoints
* CORS support
* Static file serving
* Modular architecture

---

## 8. React Frontend

Built frontend chat interface using React + Vite.

### Features

* ChatGPT-style interface
* Sidebar chats
* Markdown rendering
* Loading states
* Chat memory
* API integration

---

# Current Folder Structure

```text id="7i1f24"
RAG_system_NCERT/
│
├── backend/
│   ├── api/
│   ├── handlers/
│   ├── retrieval/
│   ├── vectorstore/
│   ├── app.py
│
├── frontend/
│   ├── src/
│   ├── public/
│
├── data/
│   ├── raw/
│   ├── processed/
│   │   ├── rendered_pages/
│   │   ├── image_metadata.json
│
├── notebooks/
│
├── outputs/
│
├── requirements.txt
│
└── README_STAGE2.md
```

---

# Current Known Issues

The following issues are intentionally deferred to Stage 3:

* Image rendering issues
* Undefined equation response fields
* Numerical parsing limitations
* Momentum solver limitations
* Query routing edge cases
* Gemini API quota handling
* UI refinements
* Full-book scaling
* Deployment pipeline

---

# Stage 3 Goals

Stage 3 will focus on:

## 1. Full NCERT Book Scaling

* Multiple chapters
* Complete textbook ingestion
* Better metadata handling

---

## 2. Numerical Solver Improvements

* Automatic variable extraction
* Advanced formula routing
* Step-by-step solutions

---

## 3. Image System Improvements

* Proper frontend image rendering
* Diagram-specific retrieval
* Better OCR matching

---

## 4. UI Improvements

* Premium UI design
* Animations
* Better responsiveness
* Improved chat experience

---

## 5. Gemini Stability

* Retry mechanisms
* Fallback responses
* Reduced API dependency

---

## 6. Deployment

### Frontend

* Vercel deployment

### Backend

* Render / Railway deployment

---

# Technologies Used

## Backend

* FastAPI
* LangChain
* SentenceTransformers
* BM25
* ChromaDB
* Gemini API

---

## Frontend

* React
* Vite
* SCSS
* ReactMarkdown

---

## NLP / Retrieval

* Semantic embeddings
* Hybrid retrieval
* OCR-based image retrieval

---

# Current Status

```text id="m1yzut"
Stage 1 → Completed
Stage 2 → Completed (Core Architecture)
Stage 3 → Planned
```

---

# Author

Himkar Vashistha

BTech Data Science Engineering
PG in Agentic AI & AIML Engineering — IIT Gandhinagar




