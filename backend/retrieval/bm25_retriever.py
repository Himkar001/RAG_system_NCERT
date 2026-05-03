import json
import re
from rank_bm25 import BM25Okapi


CHUNK_PATH = "data/processed/wk10_chunks.json"


def preprocess(text):

    text = text.lower()

    text = re.sub(r"[^a-zA-Z0-9 ]", "", text)

    return text.split()


def load_chunks():

    with open(CHUNK_PATH, "r", encoding="utf-8") as f:

        chunks = json.load(f)

    return chunks


chunks = load_chunks()


bm25_corpus = []

for chunk in chunks:

    tokens = preprocess(chunk["text"])

    bm25_corpus.append(tokens)


bm25 = BM25Okapi(bm25_corpus)

def bm25_search(query, top_k=5):

    query_tokens = preprocess(query)

    scores = bm25.get_scores(query_tokens)

    ranked_indices = sorted(
        range(len(scores)),
        key=lambda i: scores[i],
        reverse=True
    )[:top_k]

    results = []

    for idx in ranked_indices:

        results.append({

            "text": chunks[idx]["text"],
            "page": chunks[idx]["page"],
            "content_type": chunks[idx]["content_type"],
            "score": float(scores[idx]),
            "source": "bm25"
        })

    return results