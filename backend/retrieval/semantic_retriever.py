from backend.vectorstore.chroma_store import load_vectorstore


vectorstore = load_vectorstore()


def semantic_search(query, top_k=5):

    results = vectorstore.similarity_search_with_score(
        query,
        k=top_k
    )

    formatted_results = []

    for doc, score in results:

        formatted_results.append({

            "text": doc.page_content,
            "page": doc.metadata.get("page"),
            "content_type": doc.metadata.get("content_type"),
            "score": float(score),
            "source": "semantic"
        })

    return formatted_results

