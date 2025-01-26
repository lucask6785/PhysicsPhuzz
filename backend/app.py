from flask import Flask, render_template, request, jsonify
from Chat_API import *  # Assuming the necessary functions are in this module
import ast
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import requests
from flask_cors import CORS

app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///variables.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Variable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    x = db.Column(db.Float, nullable=False)
    y = db.Column(db.Float, nullable=False)
    vx = db.Column(db.Float, nullable=False)
    vy = db.Column(db.Float, nullable=False)
    ax = db.Column(db.Float, nullable=False)
    ay = db.Column(db.Float, nullable=False)
    mass = db.Column(db.Float, nullable=False)
    radius = db.Column(db.Float, nullable=False)
    elasticity = db.Column(db.Float, nullable=False)
    friction = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(80), nullable=False)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

# Route to serve the HTML files
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ballDropSimulation')
def ball_drop_simulation():
    return render_template('ballDropSimulation.html')


# Route to handle the 'Solve' button functionality
@app.route('/solve', methods=['POST', 'GET'])
def solve_route():
    if request.method == "POST":
        # Get the problem data from the frontend
        data = request.get_json()
        problem = data.get('problem', '')
        print('solve button clicked')

        # If no problem is provided, try to extract text from an image
        if not problem:
            # Send image as a POST request to the upload-image route
            image_file_path = "./assets/physicsprob.png"  # Path to your image file
            with open(image_file_path, 'rb') as f:
                files = {'image': f}
                response = requests.post('http://127.0.0.1:5000/upload-image', files=files)
            
            if response.status_code == 200 and response.json().get('success'):
                problem = response.json().get('text', '')
                print("Extracted Text from Image:", problem)
            else:
                return jsonify({'success': False, 'message': 'Failed to extract text from image'})

        # Solve the problem and get the solution and steps
        solution, steps, variables = process_physics_response(problem)
        #print(solution)
        VARIABLES = variables
        print("Variables :D :", VARIABLES)
        val = VARIABLES.find("{")
        val2 = VARIABLES.find("}")
        var = ast.literal_eval(VARIABLES[val:val2+1])
        variable = Variable(x=var['x'], y=var['y'], vx=var['vx'], vy=var['vy'], ax=var['ax'], ay=var['ay'], mass=var['mass'], radius=var['radius'], elasticity=var['elasticity'], friction=var['friction'], type=var['type'])
        db.session.add(variable)
        db.session.commit() 

        # Return the solution and steps as JSON
        return jsonify({
            'solution': solution,
            'steps': steps,
            'message': 'Solution calculated!'
        })
    if request.method == "GET":
        variables = Variable.query.all()
        return jsonify(variables[-1].to_dict())

if __name__ == '__main__':
    app.run(debug=True)
