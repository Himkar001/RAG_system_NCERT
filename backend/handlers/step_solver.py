import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY, transport="rest")

model = genai.GenerativeModel("gemini-3.6-flash")

def solve_step_by_step(query, equation_type, variables_dict):
    prompt = f"""
You are a helpful physics and math tutor. The user asked: "{query}"
We identified the equation type as: "{equation_type}"
The variables extracted from the query are: {variables_dict}

Please provide a formatted markdown step-by-step solution to this problem.
Include:
1. Given values (with units if known).
2. The formula used.
3. Step-by-step substitution and calculation.
4. Final answer with units.
"""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating step-by-step solution: {str(e)}"
