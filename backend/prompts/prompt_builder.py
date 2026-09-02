def extract_sources(retrieved_results):
    sources = []
    for i, item in enumerate(retrieved_results, 1):
        text = item.get("text", "")
        preview = text[:100] + "..." if len(text) > 100 else text
        sources.append({
            "index": i,
            "page": item.get("page", "Unknown"),
            "content_type": item.get("content_type", "Unknown"),
            "preview": preview
        })
    return sources

def build_prompt(query, retrieved_results):
    context_blocks = []
    
    for i, item in enumerate(retrieved_results, 1):
        text = item.get("text", "")
        page = item.get("page", "Unknown")
        c_type = item.get("content_type", "Unknown")
        
        block = f"[{i}] Page {page} | Type: {c_type}\n{text}"
        context_blocks.append(block)

    context = "\n\n".join(context_blocks)
    
    prompt = f"""
You are an NCERT Science Tutor.

You must answer ONLY using the provided NCERT context.
If answer is missing, say:
"I could not find this in NCERT context."

Please cite sources by number using the format [1] or [2].

Context:
{context}

Question:
{query}

Instructions:
- Explain clearly
- Use simple NCERT language
- Stay grounded to textbook
- Do not hallucinate
- Cite sources like [1] or [2]
"""
    sources = extract_sources(retrieved_results)
    return prompt, sources
