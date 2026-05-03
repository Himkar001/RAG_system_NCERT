import re
equation_db = {
    "v = u + at": {
        "name": "First Equation of Motion",
        "formula": "v = u + at",
        "variables": {
            "v": "Final Velocity",
            "u": "Initial Velocity",
            "a": "Acceleration",
            "t": "Time"
        },
        "description": "Calculates the final velocity of an object after accelerating for a certain time."
  },

    "f = ma": {
        "name": "Newton Second Law",
        "formula": "F = ma",
        "topic": "Force and Motion",
        "variables": {
            "F": "Force",
            "m": "Mass",
            "a": "Acceleration"
        },
        "description": "Force equals mass multiplied by acceleration."
    },

    "p = mv": {
        "name": "Momentum",
        "formula": "p = mv",
        "topic": "Momentum",
        "variables": {
            "p": "Momentum",
            "m": "Mass",
            "v": "Velocity"
        },
        "description": "Momentum is the product of mass and velocity."
    },

    "f = (mv-u)/t": {
        "name": "Rate of Change of Momentum",
        "formula": "F = (mv-u)/t",
        "topic": "Newton Second Law",
        "variables": {
            "m": "Mass",
            "v": "Final Velocity",
            "u": "Initial Momentum Component",
            "t": "Time"
        },
        "description": "Force equals rate of change of momentum."
    },

    "impulse = force × time": {
        "name": "Impulse",
        "formula": "Impulse = Force × Time",
        "topic": "Impulse and Momentum",
        "variables": {
            "Force": "Applied Force",
            "Time": "Duration"
        },
        "description": "Impulse equals force applied over time."
    },

    "impulse = change in momentum": {
        "name": "Impulse-Momentum Relation",
        "formula": "Impulse = Δp",
        "topic": "Momentum",
        "variables": {
            "Δp": "Change in Momentum"
        },
        "description": "Impulse is equal to change in momentum."
    },

    "momentum = mass × velocity": {
        "name": "Momentum Formula",
        "formula": "Momentum = Mass × Velocity",
        "topic": "Momentum",
        "variables": {
            "Mass": "Object Mass",
            "Velocity": "Object Velocity"
        },
        "description": "Defines momentum of an object."
    }
}

def extract_equation(query):

    query = query.lower()

    patterns = [

        r"[a-z]\s*=\s*[a-z]+",
        r"[a-z]\s*=\s*[a-z]\s*[\+\-\*/]\s*[a-z]+"
    ]

    for pattern in patterns:

        match = re.search(pattern, query)

        if match:

            return match.group()

    return None

def equation_lookup(query):

    equation = extract_equation(query)

    if equation is None:

        return {

            "error": "No equation detected"
        }

    equation = equation.replace(" ", "")
    for key in equation_db:

        if key.replace(" ", "") == equation:

            return equation_db[key]

    return {

        "error": "Equation not found"
    }