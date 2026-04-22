# 📘 NCERT RAG Study Assistant

A retrieval-based AI study assistant built using Retrieval-Augmented Generation (RAG) concepts over NCERT Science chapters.

This project focuses on building a complete end-to-end pipeline:

* PDF extraction
* Text cleaning
* Tokenizer-aware chunking
* Retrieval system (BM25)
* Backend API
* Frontend chatbot UI
* Future semantic retrieval + LLM response generation

---

# 🚀 Project Goal

Build an intelligent study assistant capable of answering questions from NCERT chapters by retrieving relevant textbook content.

Example:

**User Query:**

> What is Newton’s First Law of Motion?

**System Flow:**

1. Retrieve relevant chunks from NCERT text
2. Pass retrieved context to an LLM
3. Generate grounded answer

---

# 🧠 Current Chapter Used

### Chapter:

**Force and Laws of Motion**

Source:

* NCERT Science textbook

---

# 🏗️ Project Architecture

```text
PDF
↓
Text Extraction
↓
Cleaning
↓
Tokenizer-Based Chunking
↓
Chunks JSON
↓
BM25 Retrieval
↓
Backend API
↓
Frontend Chatbot
↓
LLM Response Generation
```

---

# 📂 Project Structure

```text
retrieval-study-assistant/
│
├── data/
│   ├── raw/
│   │   └── force_laws_motion.pdf
│   │
│   └── processed/
│       ├── cleaned_text.txt
│       └── chunks.json
│
├── notebooks/
│   └── rag_pipeline.ipynb
│
├── backend/
│   ├── main.py
│   └── utils.py
│
├── frontend/
│   └── (React App)
│
├── src/
│   └── reusable logic
│
├── outputs/
│
├── README.md
├── hld.md
├── requirements.txt
└── .gitignore
```

---

# 🔬 Stage 1 — Corpus Engineering

Completed:

### ✔ PDF Extraction

* Used `pdfplumber`
* Extracted raw text from NCERT PDF

### ✔ Cleaning

Removed:

* page markers
* repeated uppercase noise
* figure artifacts
* spacing inconsistencies

### ✔ Chunking

Implemented:

* transformer tokenizer-based chunking
* chunk overlap
* metadata creation

---

# 🧩 Chunking Strategy

### Tokenizer Used

* BERT Tokenizer (`bert-base-uncased`)

### Chunk Parameters

| Parameter  | Value                    |
| ---------- | ------------------------ |
| Chunk Size | 350 tokens               |
| Overlap    | 60 tokens                |
| Method     | Transformer Tokenization |

---

# 🧠 Why Tokenizer-Based Chunking?

Instead of splitting text by words, chunking is performed using transformer tokens.

Benefits:

* Better alignment with LLM context windows
* Improved retrieval stability
* Better handling of scientific text
* More consistent chunk boundaries

---

# 🔍 Tokenizer Comparison Study

Compared:

1. BERT Tokenizer (WordPiece)
2. GPT-2 Tokenizer (BPE)
3. T5 Tokenizer (SentencePiece)

Comparison criteria:

* token count
* decimal handling
* scientific terminology splitting
* chunk compatibility

### Result

BERT WordPiece tokenizer performed best for:

* educational text
* lexical retrieval
* scientific terminology

---

# 📦 Saved Outputs

Generated files:

### `cleaned_text.txt`

Stores cleaned chapter text.

### `chunks.json`

Stores retrieval-ready tokenized chunks.

Example chunk format:

```json
{
  "id": 0,
  "text": "chunk text",
  "chapter": "Force and Laws of Motion",
  "token_count": 350
}
```

---

# 🧠 Retrieval Strategy

Planned retrieval pipeline:

### Stage 2

* BM25 Retrieval

### Stage 3

* Semantic Retrieval (Embeddings)

### Stage 4

* Hybrid Retrieval

```text
BM25 + Dense Vector Search
```

---

# 🛠️ Tech Stack

### Libraries

* pdfplumber
* transformers
* torch
* rank_bm25
* json
* regex

### Backend

* Python
* FastAPI (planned)

### Frontend

* React (planned)

### Retrieval

* BM25
* Tokenizer-aware chunks

---

# 📈 Current Progress

### Completed

* [x] Project setup
* [x] HLD structure
* [x] PDF extraction
* [x] Cleaning pipeline
* [x] Transformer chunking
* [x] Tokenizer comparison
* [x] Chunk storage
* [x] BM25 retrieval engine
* [x] Retrieval evaluation
* [x] Gemini-powered answer generation
* [x] End-to-end RAG prototype

### Current Prototype Features

The current prototype supports:

* Asking questions from NCERT chapter content
* Retrieval of relevant chunks using BM25
* Grounded prompting using retrieved context
* Gemini-based answer generation
* Interactive notebook-based Q&A workflow

### Prototype Workflow

```text
User Question
↓
Query Preprocessing
↓
BM25 Retrieval
↓
Top Relevant Chunks
↓
Prompt Construction
↓
Gemini Generation
↓
Final Answer
```

### Upcoming

* [ ] FastAPI backend
* [ ] Frontend chatbot
* [ ] API integration
* [ ] Multi-chapter ingestion
* [ ] Semantic retrieval (embeddings)
* [ ] Hybrid retrieval
* [ ] Evaluation metrics

---

# 🎯 Future Improvements

* Semantic embeddings
* Hybrid search
* Query intent routing
* Chapter expansion
* Multi-chapter retrieval
* Citation grounding
* Answer confidence scoring

---

# 🧠 Learning Objectives

This project demonstrates:

* Retrieval-Augmented Generation fundamentals
* Corpus engineering
* Tokenizer-aware chunking
* Retrieval system design
* Educational chatbot architecture
* End-to-end AI system design




