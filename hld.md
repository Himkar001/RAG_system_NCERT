# 📘 High-Level Design (HLD)

## Retrieval-Ready Study Assistant (NCERT Science)

---

## 1. 🎯 Objective

Design and implement a **grounded question-answering system** over NCERT Class 9 Science content that:

* Retrieves relevant textbook context
* Generates answers strictly from retrieved content
* Refuses to answer when information is not present

The system prioritizes **accuracy, grounding, and reliability** over open-ended generation.

---

## 2. 🧠 System Overview

The system follows a **Retrieval-Augmented Generation (RAG)** pipeline:

1. Extract and preprocess NCERT textbook data
2. Split text into meaningful chunks
3. Retrieve relevant chunks using lexical search
4. Generate answers using an LLM constrained by context
5. Evaluate performance using a structured dataset

---

## 3. 🏗️ Architecture

```
NCERT PDF
   ↓
Text Extraction (pdfplumber / PyMuPDF)
   ↓
Text Cleaning & Structuring
   ↓
Chunking (size + overlap)
   ↓
Chunk Store (with metadata)
   ↓
User Query
   ↓
BM25 Retriever
   ↓
Top-K Chunks
   ↓
LLM (Gemini/OpenAI) + Grounding Prompt
   ↓
Final Answer (Grounded)
```

---

## 4. 🔧 Core Components

### 4.1 Corpus Processing

* Extract raw text from PDFs
* Clean noisy formatting
* Segment into:

  * Concept paragraphs
  * Worked examples
  * Questions

---

### 4.2 Tokenization & Chunking

* Compare tokenizers (BERT, GPT, T5)
* Define chunk size and overlap
* Preserve semantic units (avoid splitting examples/solutions)

---

### 4.3 Retrieval Layer

* Use **BM25 (rank_bm25)**
* Retrieve top-k relevant chunks for a query
* Each chunk contains metadata:

  * Chapter
  * Section
  * Content type

---

### 4.4 Generation Layer

* Use LLM API (Gemini/OpenAI)
* Apply grounding prompt:

  * Answer only from context
  * Refuse if answer not present
  * Avoid hallucination

---

### 4.5 Answer Pipeline

```
Query → Retrieve → Provide Context → Generate → Return Answer
```

---

### 4.6 Evaluation Framework

* Create evaluation dataset (15–20 questions):

  * Direct questions
  * Paraphrased questions
  * Out-of-scope queries

* Metrics:

  * Correctness
  * Grounding
  * Refusal appropriateness

---

## 5. 📊 Data Flow

1. PDF → Extracted text
2. Text → Cleaned structured data
3. Structured data → Chunks
4. Chunks → Indexed (BM25)
5. Query → Top-k chunks
6. Chunks + prompt → LLM
7. LLM → Final answer

---

## 6. ⚙️ Tech Stack

| Component      | Tool                 |
| -------------- | -------------------- |
| PDF Extraction | pdfplumber / PyMuPDF |
| Tokenization   | HuggingFace          |
| Retrieval      | BM25 (rank_bm25)     |
| LLM            | Gemini / OpenAI API  |
| Language       | Python               |
| Environment    | Jupyter / Colab      |

---

## 7. ⚠️ Design Considerations

* Chunk size vs context tradeoff
* Retrieval quality impacts answer correctness
* Prompt design controls hallucination
* Evaluation must reflect real user queries

---

## 8. 🚧 Constraints

* CPU-only setup
* Small corpus (1–2 chapters)
* No vector database (this phase)
* API-based LLM

---

## 9. 📈 Future Improvements

* Dense retrieval (embeddings)
* Hybrid search (BM25 + semantic)
* Reranking models
* Multilingual support (Hindi-English)
* UI-based chatbot

---

## 10. ✅ Success Criteria

* ≥10 correct answers out of 15–20
* Correct refusal for out-of-scope queries
* Answers grounded in retrieved content
* Clear failure analysis

---

