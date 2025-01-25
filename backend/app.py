from flask import Flask, render_template, request, jsonify
from scripts import *  # Assuming the necessary functions are in this module

app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')

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

    solution, steps = solve(problem)
    # Return the solution as JSON
    return jsonify({'solution': solution, 'message': 'Solution calculated!'})

# Route to handle the 'Show Steps' button functionality
@app.route('/show-steps', methods=['POST'])
def show_steps_route():
    return show_steps()  # Call the show_steps function from scripts.py


if __name__ == '__main__':
    app.run(debug=True)
