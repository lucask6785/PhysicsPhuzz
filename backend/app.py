from flask import Flask, render_template, request, jsonify
from Chat_API import *  # Assuming the necessary functions are in this module
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')
db = SQLAlchemy(app)

class Variables(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    variables = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"Variables('{self.name}', '{self.value}')"

# Route to serve the HTML file
@app.route('/')
def home():
    return render_template('index.html')

# Route to handle the 'Solve' button functionality
@app.route('/solve', methods=['POST'])
def solve_route():
    if request.method == "POST":
        # Get the problem data from the frontend
        data = request.get_json()
        problem = data.get('problem', '')
        print('solve button clicked')

        # Solve the problem and get the solution and steps
        solution, steps, variables = process_physics_response(problem)
        print(solution)
        new_variable = Variables(variables=variables)
        db.session.add(new_variable)
        db.session.commit()
        # Return the solution and steps as JSON
        return jsonify({
            'solution': solution,
            'steps': steps,
            'message': 'Solution calculated!'
        })
    else:
        result = db.session.query(Variables).all()
        return jsonify(result[-1].variables)

if __name__ == '__main__':
    app.run(debug=True)
