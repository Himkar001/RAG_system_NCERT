import os
import json
from dotenv import load_dotenv
import google.generativeai as genai
from backend.retrieval.hybrid_retriever import hybrid_search

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"), transport="rest")
model = genai.GenerativeModel("gemini-3.6-flash")

def expand_query(query):
    prompt = f"Generate 3 alternative phrasings of this NCERT Science question. Return ONLY a JSON array of 3 strings, no explanation: {query}"
    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        if text.startswith("```json"):
            text = text[7:-3]
        elif text.startswith("```"):
            text = text[3:-3]
        variants = json.loads(text.strip())
        if not isinstance(variants, list):
            raise ValueError("Not a list")
        
        results = [query] + [str(v) for v in variants[:3]]
        return results
    except Exception:
        return [query]

def multi_query_search(query, top_k=5):
    queries = expand_query(query)
    all_results = []
    
    for q in queries:
        # We fetch more internally to ensure enough for deduplication
        results = hybrid_search(q, top_k=top_k)
        all_results.extend(results)
        
    # Deduplicate by text[:150]
    seen = set()
    deduped = []
    
    # Sort by score ascending (assuming lower is better in Chroma, but standard score behavior depends on distance metric)
    # RRF will make higher score better. Let's assume higher score is better for hybrid_search now.
    all_results.sort(key=lambda x: x["score"], reverse=True)
    
    for res in all_results:
        key = res["text"][:150]
        if key not in seen:
            seen.add(key)
            deduped.append(res)
            
    return deduped[:top_k]
