from backend.retrieval.hybrid_retriever import hybrid_search
from backend.retrieval.semantic_retriever import semantic_search

def classify_query(query):

    query_lower = query.lower()
    if "=" in query or "formula" in query_lower:

        return "equation"
    elif any(word in query_lower for word in [

        "diagram",
        "image",
        "figure",
        "draw"

    ]):

        return "image"
    elif any(word in query_lower for word in [

        "calculate",
        "solve",
        "find value",
        "numerical"

    ]):

        return "numerical"
    elif any(word in query_lower for word in [

        "why",
        "how",
        "explain",
        "reason"

    ]):

        return "semantic"
    else:

        return "hybrid"
    
def route_query(query):

    route = classify_query(query)

    if route == "semantic":

        return semantic_search(query)

    elif route == "hybrid":

        return hybrid_search(query)

    elif route == "equation":

        return {

            "route": "equation"
        }

    elif route == "numerical":

        return {

            "route": "numerical"
        }

    elif route == "image":

        return {

            "route": "image"
        }