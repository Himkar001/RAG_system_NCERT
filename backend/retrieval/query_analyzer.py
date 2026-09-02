import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"), transport="rest")
model = genai.GenerativeModel("gemini-3.6-flash")

def analyze_query(query):
    prompt = f"""
    Analyze the following NCERT Science query and classify its intent into one of these categories:
    [conceptual, numerical, equation, image, comparison, definition, out_of_scope]
    
    Return a JSON object with the following fields:
    - intent (string)
    - confidence (float between 0 and 1)
    - requires_math (boolean, true if intent is numerical or equation)
    - is_definition (boolean, true if intent is definition)
    - keywords (list of strings, key terms extracted from the query)
    
    Return ONLY valid JSON, no explanation or formatting blocks.
    
    Query: {query}
    """
    
    default_response = {
        "intent": "conceptual",
        "confidence": 0.5,
        "requires_math": False,
        "is_definition": False,
        "keywords": []
    }
    
    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        if text.startswith("```json"):
            text = text[7:-3]
        elif text.startswith("```"):
            text = text[3:-3]
            
        analysis = json.loads(text.strip())
        
        # Ensure it has all keys
        for k in default_response:
            if k not in analysis:
                analysis[k] = default_response[k]
                
        return analysis
        
    except Exception:
        return default_response
