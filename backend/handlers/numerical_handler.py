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

def extract_numbers(query):

    numbers = re.findall(r"\d+\.?\d*", query)

    return [float(n) for n in numbers]

def detect_numerical_type(query):

    query_lower = query.lower()

    for eq_name, eq_info in numerical_equations.items():

        for keyword in eq_info["keywords"]:

            if keyword in query_lower:

                return eq_name

    return None

def solve_force(mass, acceleration):

    force = mass * acceleration

    return {
        "formula": "F = ma",
        "result": f"Force = {force} N"
    }


def solve_momentum(mass, velocity):

    momentum = mass * velocity

    return {
        "formula": "p = mv",
        "result": f"Momentum = {momentum} kg·m/s"
    }


def solve_velocity(initial_velocity, acceleration, time):

    final_velocity = initial_velocity + (acceleration * time)

    return {
        "formula": "v = u + at",
        "result": f"Final Velocity = {final_velocity} m/s"
    }


def solve_impulse(force, time):

    impulse = force * time

    return {
        "formula": "Impulse = Force × Time",
        "result": f"Impulse = {impulse} Ns"
    }


def solve_impulse_momentum(initial_momentum, final_momentum):

    impulse = final_momentum - initial_momentum

    return {
        "formula": "Impulse = Change in Momentum",
        "result": f"Impulse = {impulse} kg·m/s"
    }


def solve_rate_of_change(mass, initial_velocity, final_velocity, time):

    force = mass * (final_velocity - initial_velocity) / time

    return {
        "formula": "F = (mv - mu)/t",
        "result": f"Force = {force} N"
    }

def numerical_router(query):

    equation_type = detect_numerical_type(query)

    if equation_type is None:
        return "No matching numerical equation found"

    values = extract_numbers(query)

    try:

        if equation_type == "force":

            return solve_force(values[0], values[1])

        elif equation_type == "momentum":

            return solve_momentum(values[0], values[1])

        elif equation_type == "velocity":

            return solve_velocity(values[0], values[1], values[2])

        elif equation_type == "impulse_force_time":

            return solve_impulse(values[0], values[1])

        elif equation_type == "impulse_momentum":

            return solve_impulse_momentum(values[0], values[1])

        elif equation_type == "rate_of_change_of_momentum":

            return solve_rate_of_change(values[0], values[1], values[2], values[3])
        
    except:

        return "Not enough numerical values found in query"