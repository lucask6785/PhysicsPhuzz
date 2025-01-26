let physicsVariables = null;

// Function to initialize the visualization
function initVisualization(variables) {
    physicsVariables = variables;

    // Clear any existing visualization
    const container = document.getElementById('visualization-container');
    container.innerHTML = ''; // Clear previous content

    // Create a new p5.js instance
    new p5((sketch) => {
        sketch.setup = () => {
            const canvas = sketch.createCanvas(640, 480);
            canvas.parent('visualization-container'); // Attach canvas to the container
        };

        sketch.draw = () => {
            sketch.background(255);

            if (physicsVariables) {
                // Draw a circle representing the object
                const { x, y, radius } = physicsVariables;
                sketch.fill(100, 150, 250);
                sketch.noStroke();
                sketch.ellipse(x, y, radius * 2, radius * 2);

                // Draw velocity vector
                const { vx, vy } = physicsVariables;
                sketch.stroke(255, 0, 0);
                sketch.strokeWeight(2);
                sketch.line(x, y, x + vx * 10, y + vy * 10);

                // Draw acceleration vector
                const { ax, ay } = physicsVariables;
                sketch.stroke(0, 255, 0);
                sketch.strokeWeight(2);
                sketch.line(x, y, x + ax * 10, y + ay * 10);
            }
        };
    });
}

// Fetch physics variables from the backend and initialize visualization
function fetchAndVisualize() {
    fetch('/solve', { method: 'GET' })
        .then(response => response.json())
        .then(variables => {
            console.log("Variables for visualization:", variables);
            initVisualization(variables); // Initialize visualization
        })
        .catch(error => {
            console.error('Error fetching variables:', error);
        });
}