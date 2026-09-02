# High-Level Design (HLD) — Parishiksha NCERT AI Assistant

## 1. Executive Summary

**Parishiksha** is an advanced, production-grade Retrieval-Augmented Generation (RAG) system specifically engineered for Indian curriculum education (NCERT Class 9 Science). Unlike basic document search assistants, Parishiksha implements state-of-the-art information retrieval paradigms:
- **Parent-Child Semantic Chunking** (hierarchical context indexing).
- **Multi-Intent Intelligent Routing** (theory, definitions, equations, step-by-step physics calculations, diagram retrieval).
- **Hybrid Retrieval with Reciprocal Rank Fusion (RRF)** (BM25 sparse + MiniLM-L6 dense embeddings).
- **Hypothetical Document Embeddings (HyDE)** for conceptual and thematic queries.
- **Cross-Encoder Reranking** (`ms-marco-MiniLM-L-6-v2`) for precision relevance sorting.
- **Multimodal Visual Diagram Retrieval** across 278 high-resolution NCERT rendered pages.
- **Real-Time Token Streaming** via Server-Sent Events (SSE).
- **Persistent Session Memory** backed by SQLite.

---

## 2. End-to-End System Architecture

```
                                  +-----------------------------+
                                  |    Student / Client Web UI  |
                                  | (React + Vite + KaTeX math) |
                                  +--------------+--------------+
                                                 |
                       HTTP / SSE Stream         |  POST /ask/stream
                                                 v
+---------------------------------------------------------------------------------------------------+
|                                  FastAPI Backend Gateway (Port 8000)                              |
|                                                                                                   |
|   +--------------------------+       +----------------------------+       +-------------------+   |
|   |  Session Memory Manager  | <---> |    SQLite Session Store    |       | Structured Logger |   |
|   | (Query Context Resolver) |       | (conversations.db)         |       | (JSON App Logs)   |   |
|   +--------------------------+       +----------------------------+       +-------------------+   |
|                |                                                                                  |
|                v                                                                                  |
|   +-------------------------------------------------------------------------------------------+   |
|   |                                  LLM Query Analyzer & Router                              |   |
|   |                     (Intent Classification & Routing Confidence Engine)                   |   |
|   +-------------------------------------------------------------------------------------------+   |
|        |                  |                    |                   |                   |          |
|        | "image"          | "equation"         | "numerical"       | "conceptual"      | "hybrid" |
|        v                  v                    v                   v                   v          |
|  +-------------+    +-------------+     +--------------+     +-------------+    +---------------+ |
|  |   Diagram   |    |  Equation   |     | Numerical /  |     |    HyDE     |    |    Hybrid     | |
|  |   Search    |    |  Lookup DB  |     | Step Solver  |     |  Retriever  |    |   Retriever   | |
|  |  (278 pgs)  |    |  (Exact)    |     | (SymPy+LLM)  |     |  (Gemini)   |    |  (BM25 + Dense| |
|  +-------------+    +-------------+     +--------------+     +------+------+    |   + RRF + CE) | |
|        |                  |                    |                    |           +-------+-------+ |
|        |                  |                    |                    |                   |         |
|        +------------------+--------------------+--------------------+-------------------+         |
|                                                |                                                  |
|                                                v                                                  |
|                                 +------------------------------+                                  |
|                                 |    Context Prompt Builder    |                                  |
|                                 |  (Numbered Citation Blocks)  |                                  |
|                                 +--------------+---------------+                                  |
|                                                |                                                  |
|                                                v                                                  |
|                                 +------------------------------+                                  |
|                                 |   Gemini Generative Engine   |                                  |
|                                 | (Token-by-Token SSE Stream)  |                                  |
|                                 +------------------------------+                                  |
+------------------------------------------------+--------------------------------------------------+
                                                 |
                                                 v
                               +------------------------------------+
                               |     Response Payload:              |
                               |     - Streamed Answer Markdown     |
                               |     - Verified Source Citations    |
                               |     - Extracted Diagrams & Pages   |
                               |     - Detected Intent Badge        |
                               +------------------------------------+
```

---

## 3. Ingestion & Indexing Pipeline Architecture

```
[ NCERT Class 9 Science PDFs (13 Chapters) ]
                    |
                    v
    +-------------------------------+
    |   PyMuPDF (fitz) Extractor    |
    | - Header / Footer Sanitizer   |
    | - Page Number Normalizer      |
    +---------------+---------------+
                    |
          +---------+---------+
          |                   |
          v                   v
+-------------------+   +----------------------------------------------------+
| 150 DPI Renderer  |   | Parent-Child Semantic Chunker                      |
| (PNG Page Images) |   | - Parent Chunks: ~400 tokens (Rich LLM context)    |
+---------+---------+   | - Child Chunks:  ~100 tokens (Precise match)       |
          |             +-------------------------+--------------------------+
          v                                       |
+-------------------+                             v
| Image Metadata DB |           +-----------------------------------+
| (OCR Text Proxy & |           | SentenceTransformer MiniLM-L6-v2  |
| Diagram Flagging) |           +-----------------+-----------------+
+-------------------+                             |
                                                  v
                               +-------------------------------------+
                               | ChromaDB Persistent Vector Database |
                               | - Collection 'langchain' (Children) |
                               | - Collection 'parents' (Parents)    |
                               +-------------------------------------+
```

---

## 4. Key Subsystem Specifications

### 4.1 Query Understanding & Multi-Intent Router
- **Intent Classifier**: Utilizes `gemini-flash-latest` with structured JSON output formatting.
- **Supported Classifications**:
  - `conceptual`: General syllabus concepts requiring semantic synthesis.
  - `definition`: Terminology or glossary questions.
  - `comparison`: Differentiating two entities (e.g., Mass vs Weight).
  - `numerical`: Physics calculation problems with numeric parameters.
  - `equation`: Formula requests (e.g., $F = ma$).
  - `image`: Diagram, visual setup, or apparatus figure requests.
  - `out_of_scope`: Queries unrelated to NCERT Science.

### 4.2 Multi-Stage Retrieval Engine
1. **HyDE (Hypothetical Document Embeddings)**:
   - For conceptual inquiries, the LLM first creates a hypothetical textbook excerpt.
   - Vector similarity search is executed on the hypothetical passage rather than the raw user query, dramatically increasing semantic overlap with textbook formulations.
2. **Hybrid RRF Fusion**:
   - Sparse lexical search (BM25) and dense semantic embedding search (MiniLM-L6-v2) run concurrently.
   - Reciprocal Rank Fusion ($RRF = \sum \frac{1}{60 + \text{rank}}$) merges disparate candidate lists into an unified ranking.
3. **Cross-Encoder Reranker**:
   - Top-15 candidates are evaluated by `cross-encoder/ms-marco-MiniLM-L-6-v2` to produce deep contextual relevance scores for the top-5 final context windows.

### 4.3 Multimodal Diagram Visualizer
- Pre-renders 278 high-resolution textbook pages.
- Evaluates query semantic similarity against OCR text profiles.
- Boosts pages flagged with active diagram keywords (`fig.`, `diagram`, `apparatus`, `setup`).
- Serves images over static route `/images/{filename}` with interactive client-side gallery preview.

### 4.4 Session Memory Store
- SQLite database (`backend/database/conversations.db`) storing full turn history per session ID.
- Resolves follow-up ambiguities (e.g., *"What is its unit?"* $\rightarrow$ *"What is the unit of force?"*).

---

## 5. Non-Functional Requirements & Design Principles

| Parameter | Specification | Implementation Strategy |
|---|---|---|
| **Latency** | First token < 1.5s | SSE Streaming + Singleton Model Caching + REST transport |
| **Accuracy** | High faithfulness | Numbered source citation constraints in prompt |
| **Portability** | OS-agnostic deployment | Docker + Docker Compose with Nginx reverse proxy |
| **Reliability** | Zero crash on rate limit | 3-stage exponential backoff retry mechanism |
| **Modularity** | Decoupled layers | Clean separation between ingestion, retrieval, handler, and API |
