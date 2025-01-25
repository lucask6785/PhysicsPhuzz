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

def bouncy_ball(num_balls, args_list):
    # Initialize Pygame
    pygame.init()
    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Physics Simulation")
    clock = pygame.time.Clock()
    
    # Initialize Pymunk space
    space = pymunk.Space()
    space.gravity = (0, 0)
    balls = []
    
    # Create physics objects
    create_walls(space, screen_width, screen_height)

    for i in range(num_balls):
        balls.append(Ball(args_list[i], 1, 15, 1, 0, screen_height))
        balls[i].object = balls[i].create_ball(space)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        for i in range(num_balls):
            # Apply acceleration (convert screen coordinates to Pymunk forces)
            if i < num_balls - 1:
                force = (balls[i].mass * balls[i].acceleration_x, balls[i].mass * -balls[i].acceleration_y)
                balls[i].object.apply_force_at_world_point(force, balls[i].object.position)
            else:
                force = (balls[i].mass )

        # Update physics
        space.step(1/60.0)
        
        # Draw everything
        screen.fill((255, 255, 255))
        
        # Draw ball (convert Pymunk coordinates to screen coordinates)
        for i in range(num_balls):
            ball_pos = int(balls[i].object.position.x), screen_height - int(balls[i].object.position.y)
            pygame.draw.circle(screen, (0, 0, 255), ball_pos, balls[i].radius)
        
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

num_balls = 2
args_list = [{'x': 400, 'y': 300, 'vx': 0, 'vy': 0, 'ax': 0, 'ay': 0},
             {'x': 400, 'y': 500, 'vx': -100, 'vy': 0, 'ax': 0, 'ay': 0}]

def main():
    bouncy_ball(num_balls, args_list)

if __name__ == "__main__":
    main()