// DOM Elements
const formulaInput = document.getElementById('formula');
const variablesInput = document.getElementById('variables');
const topicDisplay = document.getElementById('topic-display');
const solutionDisplay = document.getElementById('solution-display');
const plotImage = document.getElementById('plot-image');

// Example formula handler
function useExample(formula, variables) {
    formulaInput.value = formula;
    variablesInput.value = variables;
    processFormula();
}

// Main formula processing function
async function processFormula() {
    const formula = formulaInput.value.trim();
    const variables = variablesInput.value.split(',').map(v => v.trim());
    
    if (!formula || variables.length === 0) {
        alert('Please enter both a formula and variables');
        return;
    }

    try {
        const response = await fetch('http://localhost:5000/process-formula', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                formula: formula,
                variables: variables
            })
        });

        const data = await response.json();
        
        if (data.error) {
            throw new Error(data.error);
        }

        // Display results
        topicDisplay.textContent = `Physics Topic: ${data.topic}`;
        solutionDisplay.textContent = `Solution: ${data.solution}`;
        
        // Display visualization if available
        if (data.visualization) {
            plotImage.src = `data:image/png;base64,${data.visualization}`;
            plotImage.style.display = 'block';
        } else {
            plotImage.style.display = 'none';
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error processing formula: ' + error.message);
    }
}

// Event listeners for Enter key
formulaInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') processFormula();
});

variablesInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') processFormula();
});
