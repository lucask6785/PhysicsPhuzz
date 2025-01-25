from flask import Flask, request, jsonify
import sympy as sp
import matplotlib.pyplot as plt
import io
import base64
import re

app = Flask(__name__)

# Physics topic detection patterns
TOPIC_PATTERNS = {
    'kinematics': r'[vudast]',
    'dynamics': r'[Fma]',
    'energy': r'[Ekmgh]',
    'circular_motion': r'[ωθr]'
}

def detect_topic(formula):
    """Detect physics topic based on formula variables"""
    for topic, pattern in TOPIC_PATTERNS.items():
        if re.search(pattern, formula):
            return topic
    return 'general_physics'

def process_formula(formula, variables):
    """Process physics formula and generate solution"""
    try:
        # Parse formula and variables
        sym_vars = {var: sp.symbols(var) for var in variables}
        expr = sp.sympify(formula, locals=sym_vars)
        
        # Generate solution steps
        solution_steps = []
        for var in variables:
            try:
                solution = sp.solve(expr, sym_vars[var])
                solution_steps.append(f"{var} = {solution[0]}")
            except:
                continue
        
        # Generate visualization
        if len(variables) == 2:
            plt.figure()
            x = sp.symbols(variables[0])
            y = sp.symbols(variables[1])
            sp.plot(expr, (x, -10, 10), show=False)
            
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            visualization = base64.b64encode(buf.read()).decode('utf-8')
            plt.close()
        else:
            visualization = None
            
        return {
            'topic': detect_topic(formula),
            'solution': '\n'.join(solution_steps),
            'visualization': visualization
        }
        
    except Exception as e:
        return {'error': str(e)}

@app.route('/process-formula', methods=['POST'])
def handle_formula():
    data = request.json
    formula = data.get('formula')
    variables = data.get('variables')
    
    if not formula or not variables:
        return jsonify({'error': 'Missing formula or variables'}), 400
    
    result = process_formula(formula, variables)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
