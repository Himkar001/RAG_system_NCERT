from fastapi import APIRouter
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

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")


# -----------------------------
# Router
# -----------------------------
router = APIRouter()


# -----------------------------
# Request Schema
# -----------------------------
class QueryRequest(BaseModel):
    query: str


# -----------------------------
# Ask Endpoint
# -----------------------------
@router.post("/ask")
def ask_question(request: QueryRequest):

    query = request.query

    resolved_query = resolve_query(query)
    route_output = route_query(resolved_query)
    if isinstance(route_output, dict) and "route" in route_output:
        route_type = route_output["route"]

        if route_type == "equation":

            result = equation_lookup(query)

            return {
                "query": query,
                "answer": result
            }

        elif route_type == "numerical":

            result = numerical_solver(query)

            return {
                "query": query,
                "answer": result
            }

        elif route_type == "image":

            result = image_search(query)

            return {
                "query": query,
                "answer": result
            }
    prompt = build_prompt(
        resolved_query,
        route_output
        )
    response = model.generate_content(prompt)

    answer = response.text

    save_to_memory(query, answer)

    return {
        "query": query,
        "answer": answer
    }