import pygame
import pymunk
import pymunk.pygame_util
import math
import pygame.freetype

class Ball:
    def __init__(self, args, screen_height):
        self.position_x = args['x']
        self.position_y = args['y']
        self.velocity_x = args['vx']
        self.velocity_y = args['vy']
        self.acceleration_x = args['ax']
        self.acceleration_y = args['ay']
        self.mass = args['mass']
        self.radius = args['radius']
        self.screen_height = screen_height
        self.elasticity = args['elasticity']
        self.friction = args['friction']
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

def draw_arrow(screen, body, screen_height, font, velocity_display):
    # Velocity arrow (red)
    velocity = body.velocity
    position = body.position
    angle = math.atan2(-velocity.y, velocity.x)  # Flip y for pygame coordinates
    length = velocity.length / 8

    arrow_head = (
        position.x + length * math.cos(angle),
        screen_height - position.y + length * math.sin(angle)
    )
    arrow_tail = (position.x, screen_height - position.y)

    if velocity_display:
        pygame.draw.line(screen, (255, 0, 0), arrow_tail, arrow_head, 2)
        pygame.draw.polygon(screen, (255, 0, 0), [
            (arrow_head[0] + 5 * math.cos(angle + math.pi/2), arrow_head[1] + 5 * math.sin(angle + math.pi/2)),
            (arrow_head[0] + 5 * math.cos(angle - math.pi/2), arrow_head[1] + 5 * math.sin(angle - math.pi/2)),
            (arrow_head[0] + 10 * math.cos(angle), arrow_head[1] + 10 * math.sin(angle))
        ])

        # Velocity label
        vel_mag = round(velocity.length, 1)
        text_pos = (
            (arrow_tail[0] + arrow_head[0])/2 + 10 * math.cos(angle + math.pi/2),
            (arrow_tail[1] + arrow_head[1])/2 + 10 * math.sin(angle + math.pi/2)
        )
        text_surface, _ = font.render(f"{round(vel_mag/50, 2)} m/s", (0, 0, 0))
        screen.blit(text_surface, text_pos)

def draw_force_arrow(screen, position, force_vector, screen_height, font, acceleration_display):
    # Force arrow (green)
    fx, fy = force_vector
    angle = math.atan2(-fy, fx)  # Flip y for pygame coordinates
    length = math.hypot(fx, fy) / 25  # Different scale for forces

    arrow_head = (
        position.x + length * math.cos(angle),
        screen_height - position.y + length * math.sin(angle)
    )
    arrow_tail = (position.x, screen_height - position.y)

    if acceleration_display:
        pygame.draw.line(screen, (0, 255, 0), arrow_tail, arrow_head, 2)
        pygame.draw.polygon(screen, (0, 255, 0), [
            (arrow_head[0] + 5 * math.cos(angle + math.pi/2), arrow_head[1] + 5 * math.sin(angle + math.pi/2)),
            (arrow_head[0] + 5 * math.cos(angle - math.pi/2), arrow_head[1] + 5 * math.sin(angle - math.pi/2)),
            (arrow_head[0] + 10 * math.cos(angle), arrow_head[1] + 10 * math.sin(angle))
        ])

        # Force label
        force_mag = round(math.hypot(fx, fy), 1)
        text_pos = (
            (arrow_tail[0] + arrow_head[0])/2 - 15 * math.cos(angle + math.pi/2),
            (arrow_tail[1] + arrow_head[1])/2 - 15 * math.sin(angle + math.pi/2)
        )
        text_surface, _ = font.render(f"{force_mag} N", (0, 0, 0))
        screen.blit(text_surface, text_pos)

def bouncy_ball(num_balls, args_list, gravity):
    acceleration_display = False
    velocity_display = False

    pygame.init()
    pygame.freetype.init()
    font = pygame.freetype.SysFont('Arial', 20)
    
    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Physics Simulation")
    clock = pygame.time.Clock()
    
    space = pymunk.Space()
    space.gravity = (0, 0)
    balls = []
    
    create_walls(space, screen_width, screen_height)

    for i in range(num_balls):
        balls.append(Ball(args_list[i], screen_height))
        balls[i].acceleration_y -= gravity
        balls[i].object = balls[i].create_ball(space)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    if acceleration_display == True:
                        acceleration_display = False
                    else:
                        acceleration_display = True
                elif event.key == pygame.K_v:
                    if velocity_display == True:
                        velocity_display = False
                    else:
                        velocity_display = True

        # Apply forces and update physics
        for i in range(num_balls):
            force = (balls[i].mass * balls[i].acceleration_x,
                    balls[i].mass * -balls[i].acceleration_y)
            balls[i].object.apply_force_at_world_point(force, balls[i].object.position)
        space.step(1/60.0)
        
        # Draw all objects
        screen.fill((255, 255, 255))
        
        for ball in balls:
            # Draw ball
            body = ball.object
            ball_pos = (int(body.position.x), screen_height - int(body.position.y))
            pygame.draw.circle(screen, (200, 200, 200), ball_pos, ball.radius)
            
            # Draw arrows
            draw_arrow(screen, body, screen_height, font, velocity_display)
            current_force = (
                ball.mass * ball.acceleration_x,
                ball.mass * -ball.acceleration_y
            )
            draw_force_arrow(screen, body.position, current_force, screen_height, font, acceleration_display)
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

def create_walls(space, width, height):
    walls = [
        pymunk.Segment(space.static_body, (0, 0), (0, height), 5),
        pymunk.Segment(space.static_body, (0, height), (width, height), 5),
        pymunk.Segment(space.static_body, (width, height), (width, 0), 5),
        pymunk.Segment(space.static_body, (width, 0), (0, 0), 5)
    ]
    for wall in walls:
        wall.elasticity = 0.9
        wall.friction = 0.5
    space.add(*walls)

# Example configuration: two balls with different forces
num_balls = 1
args_list = [
    {   # Ball 1: Horizontal force to the right
        'x': 400, 'y': 100,
        'vx': 500, 'vy': 0,
        'ax': 0, 'ay': 50,
        'elasticity': 0.8, 'friction': 0.1,
        'mass': 2, 'radius': 15
    }
]

def main():
    bouncy_ball(num_balls, args_list, 0)

if __name__ == "__main__":
    main()