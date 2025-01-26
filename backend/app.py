from flask import Flask, render_template, request, jsonify
from Chat_API import *  # Assuming the necessary functions are in this module

app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')
VARIABLES = None

# Route to serve the HTML file
@app.route('/')
def home():
    return render_template('index.html')

# Route to handle the 'Solve' button functionality
@app.route('/solve', methods=['POST'])
def solve_route():
    # Get the problem data from the frontend
    data = request.get_json()
    problem = data.get('problem', '')
    print('solve button clicked')

    # Solve the problem and get the solution and steps
    solution, steps, variables = process_physics_response(problem)
    print(solution)
    global VARIABLES
    VARIABLES = variables
    print(VARIABLES)
    # Return the solution and steps as JSON
    return jsonify({
        'solution': solution,
        'steps': steps,
        'message': 'Solution calculated!'
    })

if __name__ == '__main__':
    app.run(debug=True)
