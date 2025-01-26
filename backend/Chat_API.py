import re
from openai import OpenAI

# Default value for user query
user_query = "A circular loop of radius R = 0.1m and resistance Rloop = 2.o ohm is placed in a time-varying magnetic field B(t) = 0.01t^2 T where t is in seconds. 1. Deerive an expression for the induced EMF in the loop. 2. Find the current indued in the loop at t= 5s"

# Map to convert ^# to its subscript equivalent
subscript_map = {
    "-30": "₋³⁰", "-29": "₋²⁹", "-28": "₋²⁸", "-27": "₋²⁷", "-26": "₋²⁶", "-25": "₋²⁵",
    "-24": "₋²⁴", "-23": "₋²³", "-22": "₋²²", "-21": "₋²¹", "-20": "₋²⁰", "-19": "₋¹⁹",
    "-18": "₋¹⁸", "-17": "₋¹⁷", "-16": "₋¹⁶", "-15": "₋¹⁵", "-14": "₋¹⁴", "-13": "₋¹³",
    "-12": "₋¹²", "-11": "₋¹¹", "-10": "₋¹⁰", "-9": "₋⁹", "-8": "₋⁸", "-7": "₋⁷",
    "-6": "₋⁶", "-5": "₋⁵", "-4": "₋⁴", "-3": "₋³", "-2": "₋²", "-1": "₋¹", "0": "₀", 
    "2": "²", "3": "³", "4": "⁴", "5": "⁵", "6": "⁶", "7": "⁷", "8": "⁸",
    "9": "⁹", "10": "¹⁰", "11": "¹¹", "12": "¹²", "13": "¹³", "14": "¹⁴", "15": "¹⁵",
    "16": "¹⁶", "17": "¹⁷", "18": "¹⁸", "19": "¹⁹", "20": "²⁰", "21": "²¹", "22": "²²",
    "23": "²³", "24": "²⁴", "25": "²⁵", "26": "²⁶", "27": "²⁷", "28": "²⁸", "29": "²⁹",
    "30": "³⁰"
}

def standardize_physics_variables(text):
    # Dictionary of replacements
    replacements = {
        r'\bu\b': 'v₀',  # Replace 'u' with 'v₀' for initial velocity
        r'\bv_0\b': 'v₀',  # Replace 'v_0' with 'v₀'
        r'\bv_i\b': 'v₀',  # Replace 'v_i' with 'v₀'
        r'\ba\b': 'a',  # Keep 'a' for acceleration
        r'\bg\b': 'g',  # Keep 'g' for gravitational acceleration
        r'\bm\b': 'm',  # Keep 'm' for mass
        r'\bh\b': 'h',  # Keep 'h' for height
        r'\bt\b': 't',  # Keep 't' for time
        r'\bF\b': 'F',  # Keep 'F' for force
        r'\bE\b': 'E',  # Keep 'E' for energy
        r'\bp\b': 'p',  # Keep 'p' for momentum
    }
    
    for old, new in replacements.items():
        text = re.sub(old, new, text)
    
    return text

def replace_with_subscripts(text):
    # Replace occurrences of ^ followed by numbers with the subscript equivalent
    def subscript_replacement(match):
        number = match.group(1)  # Get the number afwith ter ^
        return subscript_map.get(number, match.group(0))  # Return the corresponding subscript or original if not found

    return re.sub(r'\^(-?\d+)', subscript_replacement, text)



def process_physics_response(problem):
    #global user_query
    client = OpenAI(api_key="sk-148cbd347b074031b384462738683ee8", base_url="https://api.deepseek.com")

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a physics expert"},
            {"role": "system", "content": "All messages sent through the user will be about physics, apply all problems and solutions through physics"},
            {"role": "system", "content": "I need you to make another section just for variables and what they are equal too, so all the variables at the end the solution. Any variable to do with the equation. Label the first word when you create this list, 'Variables:'"},
            {"role": "system", "content": "Always state the problem with the first words being 'Problem Statement:' , exactly like this, and the solution as 'Solution:' this will be the case every single time."},
            {"role": "system", "content": "Give everything separately, so the problem statement, you should restate the problem in better terms, outlining to the user what the question is and what it is asking. Next you will provide step by step explanation of how to get from the problem the user gives to the solution in a bullet pointed format with indents and tabs to the next line. This problem and step by step solution will be paired together. Next you give the solution, this solution will be by itself and start with the word solution and then indent again, this will be separately looked at not with the problem and step by step solution."},
            {"role": "user", "content": problem}
        ],
        stream=False
    )

    messages = [choice.message.content for choice in response.choices]

    problem_and_step_by_step = ""
    solution = ""
    variables=""
    in_solution = False
    in_variables= False

    for message in messages:
        # Remove the "---" separators
        message = message.replace("---", "")

        
        # Handle LaTeX-style text commands
        message = re.sub(r'\\text\{([^}]+)\}', r'\1', message)

        # Handle fractions and square roots
        message = re.sub(r'\\frac\{([^}]+)\}\{([^}]+)\}', r'(\1/\2)', message)
        message = re.sub(r'(\d+)/(\d+)', r'(\1/\2)', message)
        message = re.sub(r'sqrt\{([^}]+)\}', r'√{\1}', message)
        message = re.sub(r'sqrt\s*(\d+)', r'√{\1}', message)
        message = re.sub(r'√\{([^}]+)\}', r'√\1', message)

        # Replace cdot with x
        message = message.replace("cdot", "×")

        # Other replacements
        message = re.sub(r'\(\(', '(', message)  # Replace ((
        message = re.sub(r'\)\)', ')', message)
        
        # Add multiplication signs between numbers and parentheses
        message = re.sub(r'(\d+)\s*($$|$$)', r'\1 × \2', message)
        message = re.sub(r'($$|$$)\s*(\d+)', r'\1 × \2', message)

        # Add multiplication signs between adjacent numbers
        message = re.sub(r'(\d+)\s+(\d+)', r'\1 × \2', message)

        # Ensure proper spacing around × symbol
        message = re.sub(r'(\S)\s*×\s*(\S)', r'\1 × \2', message)

        # Improve handling of decimal fractions
        message = re.sub(r'(\d+)\.(\d+)\s*/\s*(\d+)\.(\d+)', r'(\1.\2/\3.\4)', message)
        message = re.sub(r'(\d+(?:\.\d+)?)\s*/\s*(\d+(?:\.\d+)?)', r'(\1/\2)', message)

        message = standardize_physics_variables(message)

        #Apply subscript replacements
        message = replace_with_subscripts(message)

        message = (message.replace("*", "×")
                   .replace("###", "")
                   .replace("\\", "")
                   .replace("times", "×")
                   .replace("××", "×")
                   .replace("[", "")
                   .replace("]", "")
                   .replace("((", "(")
                   .replace("))", ")")
                   .replace("sqrt", "√")
                   .replace("cdot", "×")
                   .replace(" , ", "")
                   .replace("/", " / ")
                   .replace("^2", "²")
                   .replace(" lambda", " λ")
                   .replace("  ", " ")
                   .replace("pi","π")
                   .replace(".(", ".")
                   .replace(").",".")
                   .replace(". ×", ". ")
                   .replace("^circ", "°")
                   .replace("theta", "θ")
                   .replace("v_{y}", "Vy")
                   .replace("v_{0y}", "v₀y")
                   .replace("v_{0x}", "v₀x")
                   .replace("v_y", "vy")
                   .replace("v_x", "vx")
                   .replace("t_{total}", "Ttotal")
                   .replace("}}", "} / ")
                   .replace("mu", "μ")
                   .replace("Omega", "Ω")
                   .replace("Phi", "Φ"))
        
        message = re.sub(r'^\s*×|\s*×\s*$', '', message, flags=re.MULTILINE)
        # Standardize physics variables
        message.replace("((", "(").replace("))",")")
        lines = message.split('\n')

        for line in lines:
            line = line.strip()  # Remove leading/trailing whitespace
            if line.startswith("Solution:"):
                in_solution = True
                in_variables = False
                solution = line[9:].strip() + '\n'  # Start from the 9th character to skip "Solution:"
            elif line.startswith("Variables:"):
                in_variables = True
                in_solution = False
                variables = line + '\n'
            elif in_solution:
                solution += line + '\n'
            elif in_variables:
                variables += line + '\n'
            elif line:  # Only add non-empty lines to problem_and_step_by_step
                if line.startswith("Step-by-Step Explanation:"):
                    problem_and_step_by_step += '\n\n' + line + '\n'
                else:
                    problem_and_step_by_step += line + '\n'

    problem_and_step_by_step = problem_and_step_by_step.strip()
    solution = solution.strip()
    variables = variables.strip()

    print(problem_and_step_by_step)
    print(solution)
    print(variables)

    return problem_and_step_by_step, solution, variables

if __name__ == '__main__':
    process_physics_response()
