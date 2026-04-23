# Stage 2 Project Plan — Advanced NCERT Intelligent Study Assistant

---

# 📌 Why Stage 2 Exists

Stage 1 successfully created a working Retrieval-Augmented Generation (RAG) prototype.

Stage 1 proved that:

* textbook content can be extracted from NCERT PDFs
* chunks can be created using tokenizer-aware chunking
* BM25 retrieval can fetch relevant sections
* Gemini can generate grounded answers using retrieved chunks

However, Stage 1 has limitations.

---

# ✅ What Was Achieved in Stage 1

### Architecture

```text
User Query
↓
BM25 Retrieval
↓
Chunk Retrieval
↓
Prompt Builder
↓
Gemini
↓
Answer
```

---

## Stage 1 Components

### 1. PDF Extraction

Used:

* `pdfplumber`

Purpose:

* convert NCERT textbook into raw text

---

### 2. Cleaning Pipeline

Purpose:

* remove PDF noise
* remove formatting artifacts
* normalize extracted text

---

### 3. Tokenizer-Based Chunking

Used:

* BERT tokenizer

Purpose:

* create retrieval-ready text chunks
* preserve transformer-compatible chunk sizes

---

### 4. BM25 Retrieval

Used:

* BM25 lexical retrieval

Purpose:

* retrieve chunks using exact keywords

---

### 5. Gemini Grounded Answer Generation

Purpose:

* answer questions using retrieved context

---

# ⚠️ Why Stage 1 Needs Improvement

Stage 1 works well for:

* direct textbook definitions
* exact chapter terminology
* keyword-heavy questions

However, Stage 1 struggles with:

* semantic understanding
* paraphrased questions
* equations
* numerical problems
* diagrams/images
* contextual conversation memory

---

# Example — Stage 1 Limitation

Question:

> Why does an object resist change?

Textbook chunk:

> Inertia is the tendency of an object to resist change.

Problem:

BM25 may fail because query does not contain exact keyword “inertia”.

---

# 🚀 Stage 2 Goal

Build an intelligent educational assistant capable of:

* semantic understanding
* equation handling
* image understanding
* contextual tutoring
* hybrid retrieval

---

# 🧠 Stage 2 Architecture

```text
User Query
↓
Intent Detection
↓
Retriever Router
├── BM25 Retrieval
├── Semantic Retrieval
├── Equation Retrieval
├── Image Retrieval
└── Context Memory
↓
Context Fusion
↓
Prompt Builder
↓
Gemini
↓
Grounded Educational Answer
```

---

# 🔍 Retrieval Algorithms Used in Stage 2

---

# 1️⃣ BM25 Retrieval

Algorithm:

* BM25

Purpose:

* keyword matching
* direct concept lookup
* textbook terminology retrieval

---

## Example

Query:

> What is inertia?

BM25 retrieves:

> inertia is the tendency of an object to resist change

---

## Why Keep BM25?

BM25 is still valuable because:

* fast
* interpretable
* strong for definitions
* reliable for textbook vocabulary

---

# 2️⃣ Semantic Retrieval

Algorithm:

* dense embeddings
* cosine similarity

Model:

* Sentence Transformers
* all-MiniLM-L6-v2

---

## Purpose

Retrieve based on meaning.

---

## Example

Query:

> Why does an object resist motion?

Chunk:

> Inertia is the tendency of an object to resist change.

Semantic retrieval can match conceptual similarity.

---

## Why Needed?

BM25 only understands exact keywords.

Semantic retrieval understands:

* concepts
* paraphrases
* meaning

---

# 3️⃣ Hybrid Retrieval

Algorithm:

* score fusion
* weighted ranking

Formula:

```text
Final Score =
BM25 Score + Semantic Score
```

---

## Purpose

Combine:

* keyword precision
* semantic meaning

---

## Example

Query:

> Explain why motion changes

Hybrid retrieval combines:

* motion-related keywords
* conceptual understanding

---

## Improvement Over Stage 1

Hybrid retrieval improves:

* recall
* ranking quality
* ambiguous question handling

---

# 4️⃣ Equation Retrieval

Algorithm:

* regex
* symbol matching
* formula detection

---

## Purpose

Handle formulas and science equations.

---

## Example

Query:

> Explain F = ma

System detects equation.

Retrieves:

* Newton’s second law section
* formula explanation

---

## Why Needed?

BM25 cannot understand formula structure.

---

# 5️⃣ Numerical Problem Retrieval

Algorithm:

* intent detection
* equation mapping

---

## Example

Query:

> Find acceleration if velocity changes from 10 to 20 in 5 seconds

Pipeline:

```text
Numerical Detection
↓
Acceleration Formula Mapping
↓
Relevant Context
```

---

## Why Needed?

Educational systems must solve textbook problems.

---

# 6️⃣ Image Retrieval

Algorithm:

* image metadata retrieval
* caption matching
* OCR

---

## Purpose

Handle diagrams and figures.

---

## Example

Query:

> Explain inclined plane diagram

System retrieves:

* extracted image
* surrounding chapter context
* visual explanation

---

## Why Needed?

NCERT contains:

* diagrams
* experiments
* visual explanations

---

# 7️⃣ Contextual Memory Retrieval

Algorithm:

* previous conversation retrieval

---

## Example

User:

> What is inertia?

Follow-up:

> Give another example.

System understands:

> example of inertia

---

## Why Needed?

Stage 1 answers independently.

Stage 2 becomes conversational.

---

# 📈 Stage 1 vs Stage 2

| Capability             | Stage 1 | Stage 2  |
| ---------------------- | ------- | -------- |
| BM25 Retrieval         | ✅       | ✅        |
| Semantic Search        | ❌       | ✅        |
| Hybrid Retrieval       | ❌       | ✅        |
| Equation Understanding | ❌       | ✅        |
| Image Understanding    | ❌       | ✅        |
| Memory Context         | ❌       | ✅        |
| Numerical Solving      | ❌       | ✅        |
| Educational Tutoring   | Basic   | Advanced |

---

# 🚀 How Model Improves After Stage 2

---

## Stage 1

Query:

> Why does an object resist change?

Result:

* may fail due to missing keyword

---

## Stage 2

Semantic retrieval detects:

* inertia meaning

Result:

* accurate answer

---

## Stage 1

Query:

> Explain F = ma

Result:

* weak formula understanding

---

## Stage 2

Equation routing detects formula.

Result:

* formula explanation
* symbol breakdown
* chapter grounding

---

## Stage 1

Query:

> Explain this figure

Result:

* impossible

---

## Stage 2

Image retrieval explains diagrams.

---

# 🎯 Stage 2 End Goal

Build an intelligent NCERT educational assistant capable of:

* understanding meaning
* solving equations
* explaining diagrams
* remembering context
* improving retrieval quality
* delivering grounded educational explanations

---

# 🧠 Stage 2 Philosophy

Stage 1 built:

> Retrieval + Generation

Stage 2 builds:

> Intelligent Retrieval Orchestration + Multimodal Educational Reasoning

---

# 📌 Final Goal

Transform project from:

```text
RAG chatbot
```

into:

```text
Intelligent NCERT Science Tutor
```
