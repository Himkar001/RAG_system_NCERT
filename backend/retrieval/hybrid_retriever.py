from backend.retrieval.semantic_retriever import semantic_search
from backend.retrieval.bm25_retriever import bm25_search
from backend.retrieval.reranker import rerank_results

def rrf_fusion(results_lists, top_k=5):
    # RRF formula: for each document d, score = sum(1 / (60 + rank))
    scores = {}
    doc_map = {}
    
    for results in results_lists:
        for rank, item in enumerate(results):
            # Using text[:150] as the unique key to match items
            key = item["text"][:150]
            if key not in doc_map:
                doc_map[key] = item
                scores[key] = 0.0
            scores[key] += 1.0 / (60.0 + rank + 1.0)
            
    # Sort by RRF score descending
    sorted_keys = sorted(scores.keys(), key=lambda k: scores[k], reverse=True)
    
    fused = []
    for k in sorted_keys:
        item = doc_map[k].copy()
        item["score"] = scores[k]  # replace score with RRF score
        fused.append(item)
        
    return fused[:top_k]

def hybrid_search(query, top_k=5):
    bm25_results = bm25_search(query, top_k=15)
    semantic_results = semantic_search(query, top_k=15)
    
    fused_results = rrf_fusion([bm25_results, semantic_results], top_k=15)
    
    final_results = rerank_results(
        query,
        fused_results,
        top_k=top_k
    )

    return final_results
