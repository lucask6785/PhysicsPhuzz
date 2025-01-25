import pygame
import pymunk
import pymunk.pygame_util

args = {'x': 0,
        'y': 0,
        'vx': 10,
        'vy': 10,
        'ax': 0,
        'ay': 10}

def create_ball(space, pos, velocity):
    mass = 1
    radius = 15
    moment = pymunk.moment_for_circle(mass, 0, radius)
    body = pymunk.Body(mass, moment)
    body.position = pos
    body.velocity = velocity
    shape = pymunk.Circle(body, radius)
    shape.elasticity = 0.9
    shape.friction = 0.5
    space.add(body, shape)
    return body

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

def main():
    
    # Initialize Pygame
    pygame.init()
    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Physics Simulation")
    clock = pygame.time.Clock()
    
    # Initialize Pymunk space
    space = pymunk.Space()
    space.gravity = (0, 0)
    
    # Convert screen coordinates to Pymunk coordinates
    pymunk_pos = (args['x'], screen_height - args['y'])
    pymunk_vel = (args['vx'], -args['vy'])
    
    # Create physics objects
    create_walls(space, screen_width, screen_height)
    ball = create_ball(space, pymunk_pos, pymunk_vel)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Apply acceleration (convert screen coordinates to Pymunk forces)
        force = (ball.mass * args['ax'], ball.mass * -args['ay'])
        ball.apply_force_at_world_point(force, ball.position)
        
        # Update physics
        space.step(1/60.0)
        
        # Draw everything
        screen.fill((255, 255, 255))
        
        # Draw ball (convert Pymunk coordinates to screen coordinates)
        ball_pos = int(ball.position.x), screen_height - int(ball.position.y)
        pygame.draw.circle(screen, (0, 0, 255), ball_pos, 15)
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()