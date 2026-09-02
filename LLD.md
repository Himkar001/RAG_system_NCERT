# Low-Level Design (LLD) — Parishiksha NCERT AI Assistant

## 1. Module Hierarchy & Directory Structure

```
RAG_system_NCERT/
├── backend/
│   ├── api/
│   │   ├── routes.py            # Standard POST /ask endpoint (batch)
│   │   └── stream_routes.py     # POST /ask/stream SSE streaming endpoint
│   ├── database/
│   │   ├── __init__.py
│   │   └── session_store.py     # SQLite persistence layer (sessions table)
│   ├── handlers/
│   │   ├── memory_handler.py    # Conversation state & query resolution
│   │   ├── equation_handler.py  # Structured equation lookup
│   │   ├── numerical_handler.py # Physics variable extraction & routing
│   │   ├── step_solver.py       # Step-by-step LaTeX solution generator
│   │   └── image_handler.py     # Semantic diagram search across rendered pages
│   ├── prompts/
│   │   └── prompt_builder.py    # Numbered citation context formatter
│   ├── retrieval/
│   │   ├── query_analyzer.py    # Intent classifier using Gemini
│   │   ├── query_expander.py    # Multi-query variant generator
│   │   ├── router.py            # Dynamic intent-based dispatcher
│   │   ├── hyde_retriever.py    # Hypothetical Document Embeddings
│   │   ├── hybrid_retriever.py  # BM25 + Dense RRF fusion retriever
│   │   ├── bm25_retriever.py    # Sparse rank-bm25 index search
│   │   ├── semantic_retriever.py# Dense MiniLM-L6 vector search
│   │   └── reranker.py          # Cross-Encoder (ms-marco-MiniLM-L-6-v2)
│   ├── vectorstore/
│   │   └── chroma_store.py      # ChromaDB singleton provider
│   ├── config.py                # Pydantic Settings configuration
│   ├── logging_config.py        # Structured JSON logger
│   └── app.py                   # FastAPI initialization & static routes
├── src/
│   ├── ingestion/
│   │   ├── pdf_extractor.py     # PyMuPDF textbook text extractor
│   │   ├── render_pages.py      # 150 DPI page renderer & diagram flagger
│   │   └── ingest_pipeline.py   # End-to-end vector indexing script
│   ├── chunking/
│   │   └── semantic_chunker.py  # Parent-child hierarchical chunker
│   └── evaluation/
│       ├── eval_dataset.json    # 30-question gold standard test set
│       ├── ragas_evaluator.py   # Faithfulness & Relevancy metric evaluator
│       └── run_eval.py          # CLI evaluation runner
└── frontend/
    └── src/
        ├── components/
        │   ├── DiagramCard.jsx  # Collapsible NCERT page image preview
        │   ├── IntentBadge.jsx  # Color-coded intent pill
        │   ├── SourceCard.jsx   # Collapsible citation card
        │   ├── StreamingMessage.jsx # KaTeX markdown streaming renderer
        │   ├── SessionList.jsx  # Multi-conversation sidebar
        │   └── MathBlock.jsx    # Inline & block math renderer
        ├── App.jsx              # Main UI controller with SSE consumer
        └── App.css              # Custom Parishiksha theme styling
```

---

## 2. Database Schemas

### 2.1 SQLite Schema (`conversations.db`)
```sql
CREATE TABLE IF NOT EXISTS sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    query TEXT NOT NULL,
    answer TEXT NOT NULL,
    timestamp TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_session_id ON sessions (session_id);
```

### 2.2 ChromaDB Collections Schema
1. **Collection `langchain` (Child Chunks)**:
   - `id`: `doc_ch{chapter_num}_p{page}_c{chunk_idx}`
   - `embedding`: Vector dimension 384 (`all-MiniLM-L6-v2`)
   - `metadata`:
     ```json
     {
       "page": 115,
       "chapter": "iesc109",
       "content_type": "paragraph",
       "parent_id": "parent_iesc109_p115_0",
       "chunk_type": "child"
     }
     ```
2. **Collection `parents` (Parent Chunks)**:
   - `id`: `parent_iesc109_p115_{idx}`
   - `embedding`: Vector dimension 384
   - `metadata`:
     ```json
     {
       "page": 115,
       "chapter": "iesc109",
       "content_type": "section",
       "chunk_type": "parent"
     }
     ```

---

## 3. Data Flow & Algorithmic Details

### 3.1 Reciprocal Rank Fusion (RRF) Algorithm
For a query $q$ executed against $M$ retrieval candidate lists $L_1, L_2, \dots, L_M$:
$$RRF(d) = \sum_{m=1}^{M} \frac{1}{k + r_m(d)}$$
Where:
- $k = 60$ (constant mitigating outlier dominance).
- $r_m(d)$ is the 0-indexed rank of document $d$ in retriever list $L_m$.

```python
def rrf_fusion(results_lists: list[list[dict]], top_k: int = 15) -> list[dict]:
    scores = {}
    doc_map = {}
    for results in results_lists:
        for rank, item in enumerate(results):
            key = item["text"][:150]
            if key not in doc_map:
                doc_map[key] = item
                scores[key] = 0.0
            scores[key] += 1.0 / (60.0 + rank + 1.0)
    sorted_keys = sorted(scores.keys(), key=lambda k: scores[k], reverse=True)
    return [doc_map[k] for k in sorted_keys[:top_k]]
```

### 3.2 Parent-Child Chunking Strategy
- **Parent Chunker**: `RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=150)`
- **Child Chunker**: `RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)`
- Each child preserves a foreign-key link to its parent's unique UUID. Retrieval performs vector search on child chunks to avoid dilution, and context building feeds the parent chunk for complete pedagogical clarity.

### 3.3 Dynamic Intent Dispatcher
```python
def route_query(query: str) -> dict:
    analysis = analyze_query(query)
    intent = analysis.get("intent", "conceptual")
    confidence = analysis.get("confidence", 0.5)

    if confidence < 0.7:
        return {"intent": "fallback_hybrid", "results": hybrid_search(query), "analysis": analysis}
    if intent == "conceptual":
        return {"intent": "conceptual", "results": hyde_search(query), "analysis": analysis}
    elif intent in ["comparison", "definition"]:
        return {"intent": intent, "results": hybrid_search(query), "analysis": analysis}
    elif intent in ["numerical", "equation", "image", "out_of_scope"]:
        return {"route": intent, "intent": intent, "analysis": analysis}
    return {"intent": intent, "results": hybrid_search(query), "analysis": analysis}
```

---

## 4. Error Handling, Resilience & Rate Limiting

- **REST Transport Configuration**: All Gemini clients explicitly set `transport="rest"` to eliminate Windows gRPC port stalls and DNS delays.
- **Exponential Backoff**: Calls to Gemini generative APIs are wrapped with retry logic ($t = 3 \times (\text{attempt} + 1)$ seconds) across 3 attempts.
- **Graceful Degradation**: If HyDE generation encounters an error, the retriever transparently falls back to direct semantic search on the raw query text.
