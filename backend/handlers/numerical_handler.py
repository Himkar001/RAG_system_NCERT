import re
numerical_equations = {

    "force": {
        "formula": "F = ma",
        "variables": ["mass", "acceleration"],
        "keywords": ["force", "newton", "push"],
        "solver": "solve_force"
    },

    "momentum": {
        "formula": "p = mv",
        "variables": ["mass", "velocity"],
        "keywords": ["momentum"],
        "solver": "solve_momentum"
    },

    "velocity": {
        "formula": "v = u + at",
        "variables": ["initial_velocity", "acceleration", "time"],
        "keywords": ["velocity", "speed", "final velocity"],
        "solver": "solve_velocity"
    },

    "impulse_force_time": {
        "formula": "Impulse = Force × Time",
        "variables": ["force", "time"],
        "keywords": ["impulse"],
        "solver": "solve_impulse"
    },

    "impulse_momentum": {
        "formula": "Impulse = Change in Momentum",
        "variables": ["initial_momentum", "final_momentum"],
        "keywords": ["change in momentum"],
        "solver": "solve_impulse_momentum"
    },

    "rate_of_change_of_momentum": {
        "formula": "F = (mv - mu)/t",
        "variables": ["mass", "initial_velocity", "final_velocity", "time"],
        "keywords": ["rate of change of momentum"],
        "solver": "solve_rate_of_change"
    },

}

import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from backend.handlers.step_solver import solve_step_by_step

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY, transport="rest")
model = genai.GenerativeModel("gemini-3.6-flash")

def extract_variables_llm(query):
    prompt = f"""
Extract the physical quantities and their values from the following physics problem.
Return ONLY a valid JSON dictionary where keys are variable names (e.g. mass, initial_velocity, time) and values are the numerical values (as floats).
Do not include units in the values, just the numbers.
Query: "{query}"
"""
    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.endswith("```"):
            text = text[:-3]
        return json.loads(text.strip())
    except Exception as e:
        print("Error extracting variables:", e)
        return {}

def detect_numerical_type(query):
    query_lower = query.lower()
    for eq_name, eq_info in numerical_equations.items():
        for keyword in eq_info["keywords"]:
            if keyword in query_lower:
                return eq_name
    return None

def numerical_router(query):
    equation_type = detect_numerical_type(query)
    if equation_type is None:
        return "No matching numerical equation found"
    
    variables_dict = extract_variables_llm(query)
    if not variables_dict:
        return "Not enough numerical values found in query"
        
    return solve_step_by_step(query, equation_type, variables_dict)
