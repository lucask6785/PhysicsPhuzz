from openai import OpenAI
import re

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

def solve(problem):
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
                   .replace("×", "")
                   .replace("cdot", "×"))
        
        
        # Add multiplication signs between numbers and parentheses
        message = re.sub(r'(\d+)\s*($$|$$)', r'\1 × \2', message)
        message = re.sub(r'($$|$$)\s*(\d+)', r'\1 × \2', message)

        # Add multiplication signs between adjacent numbers
        message = re.sub(r'(\d+)\s+(\d+)', r'\1 × \2', message)

        # Ensure proper spacing around × symbol
        message = re.sub(r'(\S)\s*×\s*(\S)', r'\1 × \2', message)


        # Standardize physics variables
        message = standardize_physics_variables(message)

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

    return solution, problem_and_step_by_step, variables

def show_steps():
    # Your code to get the solution steps based on the input
    # For now, let's return placeholder steps
    print("Steps")
    return "Step 1: Analyze the problem\nStep 2: Apply the formula\nStep 3: Solve!"

