from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.handlers.equation_handler import equation_lookup
from backend.handlers.numerical_handler import numerical_router
from backend.handlers.image_handler import image_search
from backend.retrieval.router import route_query
from backend.prompts.prompt_builder import build_prompt
from backend.handlers.memory_handler import (
    resolve_query,
    save_to_memory
)

import os
from dotenv import load_dotenv
import google.generativeai as genai


# -----------------------------
# Gemini Setup
# -----------------------------
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY, transport="rest")

model = genai.GenerativeModel("gemini-3.6-flash")


# -----------------------------
# Router
# -----------------------------
router = APIRouter()


# -----------------------------
# Request Schema
# -----------------------------
class QueryRequest(BaseModel):
    query: str
    session_id: str = "default"


# -----------------------------
# Ask Endpoint
# -----------------------------
@router.post("/ask")
def ask_question(request: QueryRequest):
    try:
        query = request.query
        session_id = request.session_id

        resolved_query = resolve_query(query, session_id)
        route_output = route_query(resolved_query)
        
        intent = route_output.get("intent", "unknown")
        
        if "route" in route_output:
            route_type = route_output["route"]

            if route_type == "equation":
                result = equation_lookup(query)
                answer = result
                sources = []
            elif route_type == "numerical":
                result = numerical_router(query)
                answer = result
                sources = []
            elif route_type == "image":
                result = image_search(query)
                if "error" in result:
                    answer = f"Sorry, I couldn't find a relevant diagram: {result['error']}"
                    image_results = []
                else:
                    primary = result["primary"]
                    answer = (
                        f"Here is the most relevant diagram from **{primary['chapter']}** "
                        f"(Page {primary['page']}):\n\n"
                        f"_{primary['ocr_preview']}..._"
                    )
                    image_results = result.get("results", [])
                save_to_memory(session_id, query, answer)
                return {
                    "query": query,
                    "answer": answer,
                    "sources": [],
                    "intent": intent,
                    "session_id": session_id,
                    "image_results": image_results
                }
            elif route_type == "out_of_scope":
                answer = "I'm an NCERT Science Tutor. I can only answer questions related to the NCERT Science syllabus."
                sources = []
            else:
                answer = "Unknown route type."
                sources = []
                
            save_to_memory(session_id, query, answer)
            return {
                "query": query,
                "answer": answer,
                "sources": sources,
                "intent": intent,
                "session_id": session_id,
                "image_results": []
            }

        # Otherwise, we have context results to use with LLM
        retrieved_results = route_output.get("results", [])
        prompt, sources = build_prompt(resolved_query, retrieved_results)
        
        import time
        answer = None
        last_error = None
        for attempt in range(3):
            try:
                response = model.generate_content(prompt)
                answer = response.text
                break
            except Exception as e:
                last_error = e
                if attempt < 2:
                    time.sleep(3 * (attempt + 1))  # 3s, 6s backoff
        if answer is None:
            answer = f"The AI model is temporarily unavailable (rate limit). Please wait a few seconds and try again. Error: {str(last_error)}"

        save_to_memory(session_id, query, answer)

        return {
            "query": query,
            "answer": answer,
            "sources": sources,
            "intent": intent,
            "session_id": session_id,
            "image_results": []
        }
        
    except Exception as e:
        return {
            "query": request.query,
            "answer": f"An error occurred processing your request: {str(e)}",
            "sources": [],
            "intent": "error",
            "session_id": request.session_id
        }
