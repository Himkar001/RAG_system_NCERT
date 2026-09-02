from backend.database.session_store import save_turn, get_history

def save_to_memory(session_id, query, answer):
    save_turn(session_id, query, answer)

def is_followup_query(query):
    query_lower = query.lower()
    followup_keywords = [
        "explain more",
        "tell more",
        "continue",
        "give another example",
        "simplify",
        "why",
        "how",
        "what about",
        "can you",
        "please",
        "more details",
        "give me"
    ]
    return any(word in query_lower for word in followup_keywords)

def resolve_query(query, session_id):
    if is_followup_query(query):
        history = get_history(session_id, last_n=3)
        if history:
            context = ""
            for turn in history:
                context += f"Previous Question:\n{turn['query']}\n\nPrevious Answer:\n{turn['answer']}\n\n"
            
            combined_query = context + f"Followup Question:\n{query}\n"
            return combined_query
    return query