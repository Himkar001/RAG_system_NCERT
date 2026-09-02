from backend.retrieval.query_analyzer import analyze_query
from backend.retrieval.hybrid_retriever import hybrid_search
from backend.retrieval.hyde_retriever import hyde_search

def route_query(query):
    analysis = analyze_query(query)
    intent = analysis.get("intent", "conceptual")
    confidence = analysis.get("confidence", 0.5)
    
    if confidence < 0.7:
        results = hybrid_search(query)
        return {"intent": "fallback_hybrid", "analysis": analysis, "results": results}
        
    if intent == "conceptual":
        results = hyde_search(query)
        return {"intent": "conceptual", "analysis": analysis, "results": results}
        
    elif intent in ["comparison", "definition"]:
        results = hybrid_search(query)
        return {"intent": intent, "analysis": analysis, "results": results}
        
    elif intent == "numerical":
        return {"route": "numerical", "analysis": analysis, "intent": "numerical"}
        
    elif intent == "equation":
        return {"route": "equation", "analysis": analysis, "intent": "equation"}
        
    elif intent == "image":
        return {"route": "image", "analysis": analysis, "intent": "image"}
        
    elif intent == "out_of_scope":
        return {"route": "out_of_scope", "analysis": analysis, "intent": "out_of_scope"}
        
    # Default fallback
    results = hybrid_search(query)
    return {"intent": intent, "analysis": analysis, "results": results}