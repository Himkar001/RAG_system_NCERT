import json
import asyncio
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from backend.handlers.equation_handler import equation_lookup
from backend.handlers.numerical_handler import numerical_router
from backend.handlers.image_handler import image_search
from backend.retrieval.router import route_query
from backend.prompts.prompt_builder import build_prompt
from backend.handlers.memory_handler import resolve_query, save_to_memory

import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY, transport="rest")
model = genai.GenerativeModel("gemini-3.6-flash")

stream_router = APIRouter()

class QueryRequest(BaseModel):
    query: str
    session_id: str = "default"

@stream_router.post("/ask/stream")
async def ask_question_stream(request: QueryRequest):
    query = request.query
    session_id = request.session_id

    async def event_generator():
        try:
            resolved_query = resolve_query(query, session_id)
            route_output = route_query(resolved_query)
            
            if "route" in route_output:
                route_type = route_output["route"]
                sources = []
                image_results = []
                intent = route_output.get("analysis", {}).get("intent", route_type)

                if route_type == "equation":
                    answer = str(equation_lookup(query))
                elif route_type == "numerical":
                    answer = str(numerical_router(query))
                elif route_type == "image":
                    result = image_search(query)
                    if "error" in result:
                        answer = f"Sorry, I couldn't find a relevant diagram: {result['error']}"
                    else:
                        primary = result["primary"]
                        answer = (
                            f"Here is the most relevant diagram from **{primary['chapter']}** "
                            f"(Page {primary['page']}):\n\n"
                            f"_{primary['ocr_preview']}..._"
                        )
                        image_results = result.get("results", [])
                elif route_type == "out_of_scope":
                    answer = "I'm an NCERT Science Tutor. I can only answer questions related to the NCERT Science syllabus."
                else:
                    answer = "Unknown route type."
                
                save_to_memory(session_id, query, answer)
                
                # Yield tokens for static answers
                for token in answer.split(" "):
                    chunk_data = json.dumps({"token": token + " "})
                    yield f"data: {chunk_data}\n\n"
                    await asyncio.sleep(0.01)
                
                yield f"data: {json.dumps({'done': True, 'sources': sources, 'intent': intent, 'image_results': image_results})}\n\n"
                return

            # Otherwise, use LLM
            retrieved_results = route_output.get("results", [])
            prompt, sources = build_prompt(resolved_query, retrieved_results)
            
            import time
            full_answer = ""
            streamed = False
            for attempt in range(3):
                try:
                    response = model.generate_content(prompt, stream=True)
                    for chunk in response:
                        text_chunk = chunk.text
                        full_answer += text_chunk
                        chunk_data = json.dumps({"token": text_chunk})
                        yield f"data: {chunk_data}\n\n"
                    streamed = True
                    break
                except Exception as e:
                    if attempt < 2:
                        wait_msg = f" (retrying in {3*(attempt+1)}s...)"
                        yield f"data: {json.dumps({'token': wait_msg})}\n\n"
                        await asyncio.sleep(3 * (attempt + 1))
                    else:
                        err = "The AI model is temporarily busy. Please try again in a moment."
                        full_answer += err
                        yield f"data: {json.dumps({'token': err})}\n\n"

            intent = route_output.get("intent", "conceptual")
            save_to_memory(session_id, query, full_answer)
            yield f"data: {json.dumps({'done': True, 'sources': sources, 'intent': intent, 'image_results': []})}\n\n"
            
        except Exception as e:
            error_data = json.dumps({"token": f"Error: {str(e)}"})
            yield f"data: {error_data}\n\n"
            yield f"data: {json.dumps({'done': True})}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")
