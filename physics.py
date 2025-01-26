"""
Physics Simulation System

A modular physics simulation framework using Pygame and Pymunk.
Contains multiple simulation scenarios: free bodies, pendulum, and centripetal motion.
"""

import pygame
import pymunk
import pymunk.pygame_util
import math
import pygame.freetype

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
GRAVITY = -981  # Pixels per second squared (y-down coordinate system)
COLORS = {
    'BACKGROUND': (255, 255, 255),
    'BALL': (200, 200, 200),
    'VELOCITY_ARROW': (255, 0, 0),
    'FORCE_ARROW': (0, 255, 0),
    'ANCHOR_POINT': (255, 0, 0),
    'CENTRAL_MASS': (255, 0, 0),
    'TEXT': (0, 0, 0)
}

class PhysicsBall:
    """Represents a physics-enabled ball with Pymunk integration"""
    
    def __init__(self, config, screen_height):
        """
        Initialize ball with physics properties
        :param config: Dictionary containing ball properties
        :param screen_height: Window height for coordinate conversion
        """
        self.screen_height = screen_height
        self.position = (config['x'], config['y'])
        self.velocity = (config['vx'], config['vy'])
        self.acceleration = (config['ax'], config['ay'])
        self.mass = config['mass']
        self.radius = config['radius']
        self.elasticity = config['elasticity']
        self.friction = config['friction']
        self.physics_body = None  # Will hold Pymunk Body reference

    def create_physics_body(self, space):
        """Create and register the Pymunk body/shape in the physics space"""
        moment = pymunk.moment_for_circle(self.mass, 0, self.radius)
        body = pymunk.Body(self.mass, moment)
        
        # Convert to Pymunk coordinates (y-up)
        body.position = (self.position[0], self.screen_height - self.position[1])
        body.velocity = (self.velocity[0], -self.velocity[1])
        
        shape = pymunk.Circle(body, self.radius)
        shape.elasticity = self.elasticity
        shape.friction = self.friction
        
        space.add(body, shape)
        self.physics_body = body
        return body

class SimulationUtils:
    @staticmethod
    def create_containment_walls(space, width, height):
        """Create boundary walls for the simulation space"""
        wall_thickness = 5
        walls = [
            pymunk.Segment(space.static_body, (0, 0), (0, height), wall_thickness),
            pymunk.Segment(space.static_body, (0, height), (width, height), wall_thickness),
            pymunk.Segment(space.static_body, (width, height), (width, 0), wall_thickness),
            pymunk.Segment(space.static_body, (width, 0), (0, 0), wall_thickness)
        ]
        
        for wall in walls:
            wall.elasticity = 0.9
            wall.friction = 0.5
            
        space.add(*walls)

    @staticmethod
    def draw_vector_arrow(surface, start_pos, vector, color, label, font, scale=1):
        """
        Draw a vector arrow with magnitude label
        :param vector: (x, y) in screen coordinates (y-down)
        """
        if vector == (0, 0):
            return

        # Calculate angle using screen coordinates (no y-flip)
        angle = math.atan2(vector[1], vector[0])
        magnitude = math.hypot(*vector) * scale
        arrow_length = max(magnitude, 10)

        # Calculate arrow components
        head = (
            start_pos[0] + arrow_length * math.cos(angle),
            start_pos[1] + arrow_length * math.sin(angle)
        )

        # Draw main arrow line
        pygame.draw.line(surface, color, start_pos, head, 2)
        
        # Draw arrowhead (no coordinate conversion needed)
        pygame.draw.polygon(surface, color, [
            (head[0] + 5 * math.cos(angle + math.pi/2),
             head[1] + 5 * math.sin(angle + math.pi/2)),
            (head[0] + 5 * math.cos(angle - math.pi/2),
             head[1] + 5 * math.sin(angle - math.pi/2)),
            (head[0] + 10 * math.cos(angle),
             head[1] + 10 * math.sin(angle))
        ])

        # Draw magnitude label
        label_pos = (
            (start_pos[0] + head[0])/2 + 10 * math.cos(angle + math.pi/2),
            (start_pos[1] + head[1])/2 + 10 * math.sin(angle + math.pi/2)
        )
        text_surface, _ = font.render(label, COLORS['TEXT'])
        surface.blit(text_surface, label_pos)

class BaseSimulation:
    """Base class for simulation scenarios"""
    
    def __init__(self, title):
        self.initialize_pygame(title)
        self.space = pymunk.Space()
        self.font = pygame.freetype.SysFont('Arial', 20)
        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)
        self.running = True
        
    def initialize_pygame(self, title):
        """Set up core Pygame components"""
        pygame.init()
        pygame.freetype.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        
    def handle_common_events(self, event):
        """Handle common simulation events"""
        if event.type == pygame.QUIT:
            self.running = False
            
    def run_main_loop(self):
        """Main simulation loop to be implemented by subclasses"""
        raise NotImplementedError

class PendulumSimulation(BaseSimulation):
    """Simulation of a pendulum using PhysicsBall"""
    
    def __init__(self):
        super().__init__("Pendulum Simulation")
        # Set gravity for physics space (y-up) to pull downward on screen
        self.space.gravity = (0, 981)  # Corrected gravity direction
        self.show_velocity = False
        self.setup_scene()

    def handle_input(self, event):
        """Process keyboard input"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_v:
                self.show_velocity = not self.show_velocity
        
    def setup_scene(self):
        """Create pendulum components"""
        SimulationUtils.create_containment_walls(self.space, SCREEN_WIDTH, SCREEN_HEIGHT)
        
        # Create pendulum anchor point in screen coordinates
        screen_anchor = (400, 300)
        # Convert to physics coordinates (y-up)
        physics_anchor = (screen_anchor[0], SCREEN_HEIGHT - screen_anchor[1])
        
        # Configure pendulum bob in screen coordinates
        bob_config = {
            'x': 500,  # Initial position x (100px right of anchor)
            'y': 300,  # Initial position y (same as anchor)
            'vx': 0,
            'vy': 0,
            'ax': 0,
            'ay': 0,
            'mass': 1,
            'radius': 15,
            'elasticity': 0.9,
            'friction': 0.5
        }
        
        # Create physics body with proper coordinate conversion
        self.bob = PhysicsBall(bob_config, SCREEN_HEIGHT)
        self.bob.create_physics_body(self.space)
        
        # Create pendulum constraint using physics coordinates
        self.joint = pymunk.PinJoint(self.space.static_body, 
                                   self.bob.physics_body, 
                                   physics_anchor)
        self.space.add(self.joint)

    def run_main_loop(self):
        while self.running:
            for event in pygame.event.get():
                self.handle_common_events(event)
                self.handle_input(event)

            # Physics step
            self.space.step(1/60.0)
            
            # Get current screen position of bob
            bob_screen_pos = (
                self.bob.physics_body.position.x,
                self.bob.physics_body.position.y
            )
            
            # Convert physics velocity to screen coordinates
            velocity = (
                self.bob.physics_body.velocity.x,
                self.bob.physics_body.velocity.y  # Flip y for screen
            )
            
            # Rendering
            self.screen.fill(COLORS['BACKGROUND'])
            self.space.debug_draw(self.draw_options)
            
            # Draw velocity vector attached to bob
            if self.show_velocity:
                SimulationUtils.draw_vector_arrow(
                    self.screen, 
                    bob_screen_pos,  # Correct screen position
                    velocity,         # Correct screen-relative direction
                    COLORS['VELOCITY_ARROW'], 
                    f"{math.hypot(*velocity)/50:.2f} m/s", 
                    self.font, 
                    1/8
                )
            
            # Draw anchor point in screen coordinates
            pygame.draw.circle(self.screen, COLORS['ANCHOR_POINT'], 
                             (400, 300),  # Original screen coordinates
                             5)

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

class FreeBallsSimulation(BaseSimulation):
    """Simulation of free-moving balls with various forces"""
    
    def __init__(self, ball_configs, gravity):
        super().__init__("Free Bodies Simulation")
        self.gravity = gravity
        self.ball_configs = ball_configs
        self.balls = []
        self.show_acceleration = False
        self.show_velocity = False
        self.setup_scene()
        
    def setup_scene(self):
        """Initialize simulation objects"""
        self.space.gravity = (0, 0)
        SimulationUtils.create_containment_walls(self.space, SCREEN_WIDTH, SCREEN_HEIGHT)
        
        # Create balls from configurations
        for config in self.ball_configs:
            ball = PhysicsBall(config, SCREEN_HEIGHT)
            ball.acceleration = (config['ax'], config['ay'] - self.gravity)
            ball.create_physics_body(self.space)
            self.balls.append(ball)

    def handle_input(self, event):
        """Process keyboard input"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                self.show_acceleration = not self.show_acceleration
            elif event.key == pygame.K_v:
                self.show_velocity = not self.show_velocity

    def run_main_loop(self):
        while self.running:
            for event in pygame.event.get():
                self.handle_common_events(event)
                self.handle_input(event)

            # Apply forces
            for ball in self.balls:
                force = (ball.mass * ball.acceleration[0],
                        ball.mass * -ball.acceleration[1])
                ball.physics_body.apply_force_at_world_point(force, ball.physics_body.position)

            # Physics step
            self.space.step(1/60.0)
            
            # Rendering
            self.screen.fill(COLORS['BACKGROUND'])
            
            # Draw all objects
            for ball in self.balls:
                # Draw ball body
                body = ball.physics_body
                ball_pos = (int(body.position.x), SCREEN_HEIGHT - int(body.position.y))
                pygame.draw.circle(self.screen, COLORS['BALL'], ball_pos, ball.radius)
                
                # Draw vectors
                if self.show_velocity:
                    velocity = (body.velocity.x, -body.velocity.y)
                    SimulationUtils.draw_vector_arrow(
                        self.screen, 
                        ball_pos, 
                        velocity,
                        COLORS['VELOCITY_ARROW'], 
                        f"{math.hypot(*velocity)/50:.2f} m/s",
                        self.font, 
                        1/8
                    )
                
                if self.show_acceleration:
                    physics_force = (
                    ball.mass * ball.acceleration[0],
                    ball.mass * -ball.acceleration[1]  # Physics y-up
                    )
                    screen_force = (physics_force[0], -physics_force[1])  # Flip y for display
                    SimulationUtils.draw_vector_arrow(
                        self.screen, ball_pos, screen_force,
                        COLORS['FORCE_ARROW'], f"{math.hypot(*physics_force):.1f} N",
                        self.font, 1/25
                    )

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

class CentripetalSimulation(BaseSimulation):
    """Simulation demonstrating centripetal force"""
    
    def __init__(self):
        super().__init__("Centripetal Force Simulation")
        self.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
        self.centripetal_force_enabled = True
        self.show_acceleration = False
        self.show_velocity = False
        self.setup_scene()
        
    def setup_scene(self):
        """Initialize simulation objects"""
        self.space.gravity = (0, 0)
        SimulationUtils.create_containment_walls(self.space, SCREEN_WIDTH, SCREEN_HEIGHT)
        
        # Create orbiting ball
        config = {
            'x': self.center[0] + 200,
            'y': self.center[1],
            'vx': 0,
            'vy': 100,
            'ax': 0,
            'ay': 0,
            'mass': 2,
            'radius': 15,
            'elasticity': 1.0,
            'friction': 0.0
        }
        
        self.ball = PhysicsBall(config, SCREEN_HEIGHT)
        self.ball.create_physics_body(self.space)

    def handle_input(self, event):
        """Process keyboard input"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                self.show_acceleration = not self.show_acceleration
            elif event.key == pygame.K_v:
                self.show_velocity = not self.show_velocity
            elif event.key == pygame.K_c:
                self.centripetal_force_enabled = not self.centripetal_force_enabled

    def apply_centripetal_force(self):
        """Calculate and apply centripetal force to maintain circular motion"""
        body = self.ball.physics_body
        dx = self.center[0] - body.position.x
        dy = self.center[1] - (SCREEN_HEIGHT - body.position.y)
        radius = math.hypot(dx, dy)
        
        if radius > 0:
            # Calculate required centripetal force (F = mv²/r)
            speed_sq = body.velocity.length**2
            force_mag = (self.ball.mass * speed_sq) / radius
            
            # Force direction towards center
            fx = force_mag * (dx / radius)
            fy = force_mag * (dy / radius)
            
            if self.centripetal_force_enabled:
                body.apply_force_at_world_point((fx, -fy), body.position)
                
            return (fx, -fy)  # Return force vector for drawing
        return (0, 0)

    def run_main_loop(self):
        while self.running:
            for event in pygame.event.get():
                self.handle_common_events(event)
                self.handle_input(event)

            # Physics calculations
            force_vector = self.apply_centripetal_force()
            self.space.step(1/60.0)
            
            # Rendering
            self.screen.fill(COLORS['BACKGROUND'])
            
            # Draw central mass
            pygame.draw.circle(self.screen, COLORS['CENTRAL_MASS'], self.center, 5)
            
            # Draw orbiting ball
            body = self.ball.physics_body
            ball_pos = (int(body.position.x), SCREEN_HEIGHT - int(body.position.y))
            pygame.draw.circle(self.screen, COLORS['BALL'], ball_pos, self.ball.radius)
            
            # Draw vectors
            if self.show_velocity:
                velocity = (body.velocity.x, -body.velocity.y)
                SimulationUtils.draw_vector_arrow(
                    self.screen, 
                    ball_pos, 
                    velocity,
                    COLORS['VELOCITY_ARROW'], 
                    f"{math.hypot(*velocity)/50:.2f} m/s",
                    self.font, 
                    1/8
                )
            
            if self.show_acceleration and force_vector != (0, 0):
                # Convert physics force to screen coordinates
                screen_force = (force_vector[0], -force_vector[1])
                
                SimulationUtils.draw_vector_arrow(
                    self.screen, ball_pos, screen_force,
                    COLORS['FORCE_ARROW'], f"{math.hypot(*force_vector):.1f} N",
                    self.font, 1/25
                )

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

# Simulation Configurations
BALL_CONFIGS = [
    {   # Large ball with horizontal velocity
        'x': 400, 'y': 100,
        'vx': 500, 'vy': 0,
        'ax': 0, 'ay': 0,
        'elasticity': 0.8, 'friction': 1,
        'mass': 2, 'radius': 15
    }
]

def main():
    """Main entry point for the application"""
    # Select simulation scenario:
    # simulation = PendulumSimulation()
    # simulation = FreeBallsSimulation(BALL_CONFIGS, GRAVITY)
    simulation = CentripetalSimulation()
    simulation.run_main_loop()

if __name__ == "__main__":
    main()