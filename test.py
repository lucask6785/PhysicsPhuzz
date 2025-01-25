import pygame
import pymunk
import pymunk.pygame_util

class Ball:
    def __init__(self, args, mass, radius, elasticity, friction, screen_height):
        self.position_x = args['x']
        self.position_y = args['y']
        self.velocity_x = args['vx']
        self.velocity_y = args['vy']
        self.acceleration_x = args['ax']
        self.acceleration_y = args['ay']
        self.mass = mass
        self.radius = radius
        self.screen_height = screen_height
        self.elasticity = elasticity
        self.friction = friction
        self.object = None

    def create_ball(self, space):
        moment = pymunk.moment_for_circle(self.mass, 0, self.radius)
        body = pymunk.Body(self.mass, moment)
        body.position = (self.position_x, self.screen_height - self.position_y)
        body.velocity = (self.velocity_x, -self.velocity_y)
        shape = pymunk.Circle(body, self.radius)
        shape.elasticity = self.elasticity
        shape.friction = self.friction
        space.add(body, shape)
        return body

args = {'x': 200,
        'y': 500,
        'vx': 1000,
        'vy': 0,
        'ax': 50,
        'ay': 0}

def bouncy_ball():
    # Initialize Pygame
    pygame.init()
    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Physics Simulation")
    clock = pygame.time.Clock()
    
    # Initialize Pymunk space
    space = pymunk.Space()
    space.gravity = (0, -981)
    
    # Create physics objects
    create_walls(space, screen_width, screen_height)
    ball = Ball(args, 1, 15, 0.9, 0.5, screen_height)
    ball.object = ball.create_ball(space)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Apply acceleration (convert screen coordinates to Pymunk forces)
        force = (ball.mass * ball.acceleration_x, ball.mass * -ball.acceleration_y)
        ball.object.apply_force_at_world_point(force, ball.object.position)
        
        # Update physics
        space.step(1/60.0)
        
        # Draw everything
        screen.fill((255, 255, 255))
        
        # Draw ball (convert Pymunk coordinates to screen coordinates)
        ball_pos = int(ball.object.position.x), screen_height - int(ball.object.position.y)
        pygame.draw.circle(screen, (0, 0, 255), ball_pos, ball.radius)
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

def create_walls(space, width, height):
    walls = [
        pymunk.Segment(space.static_body, (0, 0), (0, height), 5),          # Left
        pymunk.Segment(space.static_body, (0, height), (width, height), 5), # Top
        pymunk.Segment(space.static_body, (width, height), (width, 0), 5),  # Right
        pymunk.Segment(space.static_body, (width, 0), (0, 0), 5)            # Bottom
    ]
    for wall in walls:
        wall.elasticity = 0.9
        wall.friction = 0.5
    space.add(*walls)


def create_pendulum(space, anchor_point, bob_position, bob_velocity):
    mass = 1
    radius = 15
    moment = pymunk.moment_for_circle(mass, 0, radius)
    bob = pymunk.Body(mass, moment)
    bob.position = bob_position
    bob.velocity = bob_velocity
    bob_shape = pymunk.Circle(bob, radius)
    bob_shape.elasticity = 0.9
    bob_shape.friction = 0.5
    space.add(bob, bob_shape)

    # Pendulum joint
    joint = pymunk.PinJoint(space.static_body, bob, anchor_point, (0, 0))
    space.add(joint)

    return bob

def pendulum_simulation():
    # Initialize Pygame
    pygame.init()
    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Pendulum Simulation")
    clock = pygame.time.Clock()
    draw_options = pymunk.pygame_util.DrawOptions(screen)

    # Initialize Pymunk space
    space = pymunk.Space()
    space.gravity = (0, 981)  # Gravity pointing downwards

    # Create physics objects
    create_walls(space, screen_width, screen_height)
    anchor_point = (400, 300)
    bob_position = (500, 300)
    bob_velocity = (0, 0)
    create_pendulum(space, anchor_point, bob_position, bob_velocity)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update physics
        space.step(1/60.0)

        # Draw everything
        screen.fill((255, 255, 255))
        space.debug_draw(draw_options)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

def main():
    bouncy_ball()

if __name__ == "__main__":
    main()