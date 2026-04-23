# Stage-2 RAG System — Crisp HLD (NCERT RAG)

## High-Level Architecture

```text
                 ┌─────────────────────┐
                 │     User Query      │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ Query Understanding │
                 │ - Intent Detection  │
                 │ - Query Rewrite     │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │   Retrieval Layer   │
                 └──────────┬──────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌────────────────┐ ┌────────────────┐ ┌────────────────┐
│ Dense Retrieval│ │ Sparse Retrieval│ │ Hybrid Retrieval│
│ (Embeddings)   │ │ (BM25/Keywords) │ │ Dense + Sparse  │
└────────┬───────┘ └────────┬────────┘ └────────┬───────┘
         │                  │                   │
         └──────────────────┴───────────────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │    Reranking Layer  │
                 │   (Top Relevant)    │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │   Context Builder   │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │         LLM         │
                 │   Answer Generator  │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │    Final Response   │
                 └─────────────────────┘
```

---

# Retrieval Types Included

### 1. Dense Retrieval

* Uses embeddings
* Finds semantic similarity
* Best for conceptual questions

### 2. Sparse Retrieval

* Uses keywords / BM25
* Best for exact term matching
* Useful for definitions and formulas

### 3. Hybrid Retrieval

* Combines Dense + Sparse
* Improves retrieval accuracy
* Recommended for Stage-2

### 4. Reranking

* Reorders retrieved chunks
* Selects highest-quality context
* Improves final answer quality

---

# Data Flow

```text
PDF → Chunking → Embeddings → Vector DB → Retrieval → Reranking → LLM
```

---

# Core Components

1. Data Processing
2. Vector Database
3. Retrieval Layer
4. Query Understanding
5. Reranker
6. Context Builder
7. LLM Response Generator
