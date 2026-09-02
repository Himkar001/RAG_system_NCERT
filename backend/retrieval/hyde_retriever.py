import os
from dotenv import load_dotenv
import google.generativeai as genai
from backend.vectorstore.chroma_store import load_vectorstore

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"), transport="rest")
model = genai.GenerativeModel("gemini-3.6-flash")

vectorstore = load_vectorstore()

def hyde_search(query, top_k=5):
    prompt = f"You are an NCERT Science textbook. Write a short paragraph (3-4 sentences) from the textbook that directly answers: {query}. Write ONLY the paragraph, no intro."
    try:
        response = model.generate_content(prompt)
        hypothetical_answer = response.text.strip()
    except Exception:
        # Fallback to the query itself if generation fails
        hypothetical_answer = query
        
    results = vectorstore.similarity_search_with_score(
        hypothetical_answer,
        k=top_k
    )

    formatted_results = []
    for doc, score in results:
        formatted_results.append({
            "text": doc.page_content,
            "page": doc.metadata.get("page", "Unknown"),
            "content_type": doc.metadata.get("content_type", "Unknown"),
            "score": float(score),
            "source": "hyde"
        })

    return formatted_results
