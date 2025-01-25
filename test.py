import pygame
import pymunk
import pymunk.pygame_util

args = {'x': 200,
        'y': 500,
        'vx': 1000,
        'vy': 0,
        'ax': 50,
        'ay': 0}

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
    pendulum_simulation()

if __name__ == "__main__":
    main()