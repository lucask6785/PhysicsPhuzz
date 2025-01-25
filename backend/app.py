from flask import Flask, render_template
from scripts import *

app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')

# Route to serve the HTML file
@app.route('/')
def home():
    return render_template('index.html')

# Route to handle the 'Solve' button functionality
@app.route('/solve', methods=['POST'])
def solve_route():
    return solve()  # Call the solve function from scripts.py

# Route to handle the 'Show Steps' button functionality
@app.route('/show-steps', methods=['POST'])
def show_steps_route():
    return show_steps()  # Call the show_steps function from scripts.py

if __name__ == '__main__':
    app.run(debug=True)
