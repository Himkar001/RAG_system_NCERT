from backend.retrieval.semantic_retriever import semantic_search
from backend.retrieval.bm25_retriever import bm25_search
from backend.retrieval.reranker import rerank_results

def hybrid_search(query, top_k=5):

    bm25_results = bm25_search(query, top_k=10)

    semantic_results = semantic_search(query, top_k=10)

    combined_results = bm25_results + semantic_results

    unique_results = {}

    for item in combined_results:

        key = item["text"][:150]

        if key not in unique_results:

            unique_results[key] = item

    candidate_chunks = list(unique_results.values())  
    
    final_results = rerank_results(
        query,
        candidate_chunks,
        top_k=top_k
    )

    return final_results
