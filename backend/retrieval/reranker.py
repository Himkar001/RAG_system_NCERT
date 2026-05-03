from sentence_transformers import CrossEncoder


reranker_model = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)


def rerank_results(query, candidates, top_k=5):

    pairs = []

    for item in candidates:

        pairs.append((query, item["text"]))

    scores = reranker_model.predict(pairs)

    for i, score in enumerate(scores):

        candidates[i]["rerank_score"] = float(score)

    candidates = sorted(
        candidates,
        key=lambda x: x["rerank_score"],
        reverse=True
    )

    return candidates[:top_k]