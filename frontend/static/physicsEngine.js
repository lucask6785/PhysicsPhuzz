// Ball class representing a single ball in the simulation
class Ball {
    constructor(params) {
        this.x = params.x || 0;
        this.y = params.y || 0;
        this.vx = params.vx || 0;
        this.vy = params.vy || 0;
        this.ax = params.ax || 0;
        this.ay = params.ay || 0;
        this.elasticity = params.elasticity || 0.9; // Default elasticity
        this.friction = params.friction || 0.99; // Default friction
        this.mass = params.mass || 1; // Default mass
        this.radius = params.radius || 20; // Default radius
        this.color = params.color || 'blue'; // Default color
    }

    // Draw the ball on the canvas
    draw(ctx) {
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
        ctx.fillStyle = this.color;
        ctx.fill();
        ctx.closePath();
    }

    // Update the ball's position and velocity
    update(canvasWidth, canvasHeight) {
        // Update velocity with acceleration
        this.vx += this.ax;
        this.vy += this.ay;

        // Update position with velocity
        this.x += this.vx;
        this.y += this.vy;

        // Collision with walls
        if (this.x + this.radius > canvasWidth || this.x - this.radius < 0) {
            this.vx = -this.vx * this.elasticity; // Reverse velocity with elasticity
            this.x = Math.max(this.radius, Math.min(this.x, canvasWidth - this.radius)); // Keep within bounds
        }
        if (this.y + this.radius > canvasHeight || this.y - this.radius < 0) {
            this.vy = -this.vy * this.elasticity; // Reverse velocity with elasticity
            this.y = Math.max(this.radius, Math.min(this.y, canvasHeight - this.radius)); // Keep within bounds
        }

        // Apply friction
        this.vx *= this.friction;
        this.vy *= this.friction;
    }
}
class Pendulum {
    constructor(x, y, len) {
        this.r = 12;
        this.len = len;
        this.anchor = Bodies.circle(x, y, this.r, { isStatic: true });
        this.bob = Bodies.circle(x + len, y - len, this.r, { restitution: 0.6 });
    
        let options = {
          bodyA: this.anchor,
          bodyB: this.bob,
          length: this.len,
        };
        this.arm = Constraint.create(options);
    
        Composite.add(engine.world, this.anchor);
        Composite.add(engine.world, this.bob);
        Composite.add(engine.world, this.arm);
      }
    
      // Drawing the box
      show() {
        fill(127);
        stroke(0);
        strokeWeight(2);
    
        line(
          this.anchor.position.x,
          this.anchor.position.y,
          this.bob.position.x,
          this.bob.position.y
        );
    
        push();
        translate(this.anchor.position.x, this.anchor.position.y);
        rotate(this.anchor.angle);
        circle(0, 0, this.r * 2);
        line(0, 0, this.r, 0);
        pop();
    
        push();
        translate(this.bob.position.x, this.bob.position.y);
        rotate(this.bob.angle);
        circle(0, 0, this.r * 2);
        line(0, 0, this.r, 0);
        pop();
      }
}

// PhysicsEngine class to manage the simulation
class PhysicsEngine {
    constructor(canvasId, ballsData) {
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas.getContext('2d');
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
        this.balls = ballsData.map(params => new Ball(params));
    }

    // Update the simulation
    update() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

        for (let ball of this.balls) {
            ball.update(this.canvas.width, this.canvas.height);
            ball.draw(this.ctx);
        }

        requestAnimationFrame(() => this.update());
    }

    // Start the simulation
    start() {
        this.update();
    }
}

// Global variable to store the physics engine instance
let engine = null;

// Function to initialize or refresh the simulation
function initializeSimulation(ballsData) {
    if (engine) {
        engine = null; // Destroy the existing simulation
    }
    engine = new PhysicsEngine('physics-canvas', ballsData);
    engine.start();
}

// Default simulation data
const defaultBallsData = [
    { x: 100, y: 100, vx: 0, vy: 0, ax: 0, ay: 0.5, elasticity: 0.9, friction: 0.99, mass: 1, radius: 20, color: 'red' },
    { x: 200, y: 200, vx: 0, vy: 0, ax: 0, ay: 0.5, elasticity: 0.9, friction: 0.99, mass: 1, radius: 30, color: 'blue' }
];

// Initialize the simulation with default data
initializeSimulation(defaultBallsData);

// Function to handle messages from the parent window
window.addEventListener('message', function(event) {
    if (event.data && event.data.variables) {
        // Refresh the simulation with new variables
        const ballsData = [event.data.variables];
        initializeSimulation(ballsData);
    }
});
