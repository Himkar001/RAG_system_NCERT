"""
image_handler.py — Upgraded diagram search using semantic similarity.

Finds the most relevant NCERT page image for a given query by:
1. Semantic scoring using sentence embeddings (cosine similarity)
2. Falls back to keyword overlap if embedding model unavailable
3. Prefers pages flagged has_diagram=True
4. Returns image URL path and page metadata
"""

import json
import os
import numpy as np

IMAGE_METADATA_PATH = "data/processed/image_metadata.json"

# --- Lazy-load sentence transformer for semantic search ---
_embed_model = None

def _get_embed_model():
    global _embed_model
    if _embed_model is None:
        try:
            from sentence_transformers import SentenceTransformer
            _embed_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        except Exception:
            _embed_model = None
    return _embed_model


def _cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    denom = (np.linalg.norm(a) * np.linalg.norm(b))
    if denom == 0:
        return 0.0
    return float(np.dot(a, b) / denom)


def load_image_metadata():
    if not os.path.exists(IMAGE_METADATA_PATH):
        return []
    with open(IMAGE_METADATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def _keyword_score(query: str, ocr_text: str) -> float:
    """Simple word-overlap score as fallback."""
    query_words = set(query.lower().split())
    ocr_words = set(ocr_text.lower().split())
    if not query_words:
        return 0.0
    return len(query_words & ocr_words) / len(query_words)


def image_search(query: str, top_k: int = 3):
    """
    Search for the most relevant page image(s) for a query.
    Returns a dict with:
      - results: list of top_k matches [{image_url, page, chapter, score, has_diagram}]
      - primary: the single best match
    """
    metadata = load_image_metadata()
    if not metadata:
        return {"error": "No image metadata found. Run src/ingestion/render_pages.py first."}

    # Filter to only pages that likely have diagrams for diagram queries
    diagram_keywords = ["diagram", "figure", "image", "draw", "show", "illustration",
                        "picture", "sketch", "label", "structure"]
    is_diagram_query = any(kw in query.lower() for kw in diagram_keywords)

    # Try semantic scoring
    model = _get_embed_model()
    scored = []

    if model is not None:
        query_emb = model.encode(query, convert_to_numpy=True)
        # Batch encode all OCR texts (cache-friendly)
        ocr_texts = [m.get("ocr_text", "") for m in metadata]
        # Encode in one shot for speed
        try:
            doc_embs = model.encode(ocr_texts, convert_to_numpy=True, batch_size=64, show_progress_bar=False)
            for i, m in enumerate(metadata):
                sem_score = _cosine_similarity(query_emb, doc_embs[i])
                # Boost pages that are flagged as having diagrams
                diagram_boost = 0.05 if m.get("has_diagram", False) else 0.0
                scored.append((sem_score + diagram_boost, m))
        except Exception:
            # Fall back to keyword
            for m in metadata:
                score = _keyword_score(query, m.get("ocr_text", ""))
                scored.append((score, m))
    else:
        # Keyword fallback
        for m in metadata:
            score = _keyword_score(query, m.get("ocr_text", ""))
            scored.append((score, m))

    # Sort by score descending
    scored.sort(key=lambda x: x[0], reverse=True)

    # Build results — prefer diagram pages if this is a diagram query
    if is_diagram_query:
        diagram_results = [(s, m) for s, m in scored if m.get("has_diagram", False)]
        non_diagram = [(s, m) for s, m in scored if not m.get("has_diagram", False)]
        ranked = diagram_results + non_diagram
    else:
        ranked = scored

    top = ranked[:top_k]

    if not top or top[0][0] <= 0.05:
        return {"error": "No relevant diagram found for this query."}

    def make_result(score, m):
        filename = m.get("image_filename") or os.path.basename(m.get("image_path", ""))
        return {
            "image_url": f"images/{filename}",
            "page": m.get("page"),
            "chapter": m.get("chapter", ""),
            "pdf_name": m.get("pdf_name", ""),
            "has_diagram": m.get("has_diagram", False),
            "score": round(score, 4),
            "ocr_preview": m.get("ocr_text", "")[:150]
        }

    results = [make_result(s, m) for s, m in top]
    return {
        "primary": results[0],
        "results": results
    }