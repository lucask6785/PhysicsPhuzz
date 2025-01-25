from flask import Flask, render_template_string
from openai import OpenAI

app = Flask(__name__)

@app.route('/')
def chat_output():
    client = OpenAI(api_key="sk-148cbd347b074031b384462738683ee8", base_url="https://api.deepseek.com")

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a physics expert"},
            {"role": "system", "content": "All messages sent through the user will be about physics, apply all problems and solutions through physics"},
            {"role": "system", "content": "Always state the problem with the first words being 'Problem Statement:' , exactly like this, and the solution as 'Solution:' this will be the case every single time."},
            {"role": "system", "content": "Give everything separately, so the problem statement, you should restate the problem in better terms, outlining to the user what the question is and what it is asking. Next you will provide step by step explanation of how to get from the problem the user gives to the solution in a bullet pointed format with indents and tabs to the next line. This problem and step by step solution will be paired together. Next you give the solution, this solution will be by itself and start with the word solution and then indent again, this will be separately looked at not with the problem and step by step solution."},
            {"role": "user", "content": "Hello"},
            {"role": "user", "content": "Can you solve this physics problem (F=6 * 8) what is the force?"}
        ],
        stream=False
    )

    # Loop through the choices and clean up the messages
    messages = [choice.message.content for choice in response.choices]

    # Variables to store the different parts of the response, broken down between the problem and step by step solution, to the solution itself.
    problem_and_step_by_step = ""
    solution = ""

    # Flag to track when we encounter "Solution:"
    in_solution = False

    # Process each message
    for message in messages:
        # Clean up the multiplication symbol and slashes
        message = message.replace("*", "×")
        message = message.replace("###", "")
        message = message.replace("\\", "")  # Remove backslashes from LaTeX formatting
        message = message.replace("times", "×")
        message = message.replace("××", "")

        # Split the message into lines
        lines = message.split('\n')

        for line in lines:
            if line.startswith("Solution:"):
                in_solution = True
                solution = line + '\n'
            elif in_solution:
                solution += line + '\n'
            else:
                problem_and_step_by_step += line + '\n'

    # Render the output as an HTML string
    html_content = f"""
    <h1>Physics Problem Solver</h1>
    <h2>Problem Statement and Step-by-Step Explanation</h2>
    <pre>{problem_and_step_by_step}</pre>
    <h2>Solution</h2>
    <pre>{solution}</pre>
    """

    return render_template_string(html_content)

if __name__ == '__main__':
    app.run(debug=True)

