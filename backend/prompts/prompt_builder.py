def fuse_context(results):

    context_blocks = []

    for item in results:

        text = item.get("text", "")

        context_blocks.append(text)

    return "\n\n".join(context_blocks)

def build_prompt(query, retrieved_results):

    context = fuse_context(retrieved_results)

    prompt = f"""
You are an NCERT Science Tutor.

You must answer ONLY using the provided NCERT context.

If answer is missing, say:
"I could not find this in NCERT context."

Context:
{context}

Question:
{query}

Instructions:
- Explain clearly
- Use simple NCERT language
- Stay grounded to textbook
- Do not hallucinate
"""

    return prompt
