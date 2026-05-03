conversation_memory = []

def save_to_memory(query, answer):

    conversation_memory.append({

        "query": query,
        "answer": answer
    })

def get_last_context():

    if len(conversation_memory) == 0:

        return None

    return conversation_memory[-1]

def is_followup_query(query):

    query_lower = query.lower()

    followup_keywords = [

        "explain more",
        "tell more",
        "continue",
        "give another example",
        "simplify",
        "why",
        "how"
    ]

    return any(word in query_lower for word in followup_keywords)

def resolve_query(query):

    if is_followup_query(query):

        previous = get_last_context()

        if previous:

            combined_query = f"""
Previous Question:
{previous['query']}

Previous Answer:
{previous['answer']}

Followup Question:
{query}
"""

            return combined_query

    return query