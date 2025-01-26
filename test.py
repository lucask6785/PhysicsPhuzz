import pygame
import pymunk
import pymunk.pygame_util
import math

args = {"x": 200, "y": 500, "vx": 0, "vy": 0, "ax": 0, "ay": 0}


def create_walls(space, width, height):
    walls = [
        pymunk.Segment(space.static_body, (0, 0), (0, height), 5),  # Left
        pymunk.Segment(space.static_body, (0, height), (width, height), 5),  # Top
        pymunk.Segment(space.static_body, (width, height), (width, 0), 5),  # Right
        pymunk.Segment(space.static_body, (width, 0), (0, 0), 5),  # Bottom
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
    bob = create_pendulum(space, anchor_point, bob_position, bob_velocity)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update physics
        space.step(1 / 60.0)

        # Draw everything
        screen.fill((255, 255, 255))
        space.debug_draw(draw_options)
        draw_arrow(screen, bob)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


def create_car(space, pos, velocity):
    # Collision types
    COLLTYPE_DEFAULT = 0
    COLLTYPE_CAR = 1
    COLLTYPE_WHEEL = 2

    # Car body
    mass = 10000
    vs = [(-50, -30), (50, -30), (50, 30), (-50, 30)]
    moment = pymunk.moment_for_box(mass, (100, 60))
    body = pymunk.Body(mass, moment)
    body.position = pos
    body.velocity = velocity
    chassis = pymunk.Poly(body, vs)
    chassis.elasticity = 0.9
    chassis.friction = 0.5
    chassis.collision_type = COLLTYPE_CAR
    space.add(body, chassis)

    # Wheels
    wheel_radius = 20
    wheel_mass = 500
    wheel_moment = pymunk.moment_for_circle(wheel_mass, 0, wheel_radius)
    wheel1 = pymunk.Body(wheel_mass, wheel_moment)
    wheel2 = pymunk.Body(wheel_mass, wheel_moment)
    wheel1.position = (pos[0] - 50, pos[1] + 40)  # Adjusted position
    wheel2.position = (pos[0] + 50, pos[1] + 40)  # Adjusted position
    wheel_shape1 = pymunk.Circle(wheel1, wheel_radius)
    wheel_shape2 = pymunk.Circle(wheel2, wheel_radius)
    wheel_shape1.elasticity = 0.9
    wheel_shape1.friction = 1.0
    wheel_shape2.elasticity = 0.9
    wheel_shape2.friction = 1.0
    wheel_shape1.collision_type = COLLTYPE_WHEEL
    wheel_shape2.collision_type = COLLTYPE_WHEEL
    space.add(wheel1, wheel_shape1, wheel2, wheel_shape2)

    # Joints
    pivot1 = pymunk.PivotJoint(body, wheel1, (-50, 30), (0, 0))
    pivot2 = pymunk.PivotJoint(body, wheel2, (50, 30), (0, 0))
    motor1 = pymunk.SimpleMotor(body, wheel1, 5)
    motor2 = pymunk.SimpleMotor(body, wheel2, 5)
    space.add(pivot1, pivot2, motor1, motor2)

    # Collision handler to ignore collisions between car body and wheels
    handler = space.add_collision_handler(COLLTYPE_CAR, COLLTYPE_WHEEL)
    handler.begin = lambda arbiter, space, data: False

    return body, wheel1, wheel2


def car_simulation():
    # Initialize Pygame
    pygame.init()
    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Car Simulation")
    clock = pygame.time.Clock()
    draw_options = pymunk.pygame_util.DrawOptions(screen)

    # Initialize Pymunk space
    space = pymunk.Space()
    space.gravity = (0, 981)  # Gravity pointing downwards

    # Create physics objects
    create_walls(space, screen_width, screen_height)
    car, wheel1, wheel2 = create_car(space, (200, 500), (100, 0))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Apply acceleration
        force = (car.mass * args["ax"], 0)  # Apply a force to the right
        car.apply_force_at_world_point(force, car.position)

        # Update physics
        space.step(1 / 60.0)

        # Draw everything
        screen.fill((255, 255, 255))
        space.debug_draw(draw_options)
        draw_arrow(screen, car)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

def draw_arrow(screen, body):
    velocity = body.velocity
    position = body.position
    angle = math.atan2(velocity.y, velocity.x)
    length = velocity.length / 10  # Scale the length of the arrow

    arrow_head = (position.x + length * math.cos(angle), position.y + length * math.sin(angle))
    arrow_tail = (position.x, position.y)

    pygame.draw.line(screen, (255, 0, 0), arrow_tail, arrow_head, 2)
    pygame.draw.polygon(screen, (255, 0, 0), [
        (arrow_head[0] + 5 * math.cos(angle + math.pi / 2), arrow_head[1] + 5 * math.sin(angle + math.pi / 2)),
        (arrow_head[0] + 5 * math.cos(angle - math.pi / 2), arrow_head[1] + 5 * math.sin(angle - math.pi / 2)),
        (arrow_head[0] + 10 * math.cos(angle), arrow_head[1] + 10 * math.sin(angle))
    ])

def main():
    pendulum_simulation()


if __name__ == "__main__":
    main()
