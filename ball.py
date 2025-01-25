import pygame
import pygame.freetype
import pymunk
import pymunk.pygame_util
import math

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

def draw_arrow(screen, body, screen_height, font):
    velocity = body.velocity
    position = body.position
    angle = math.atan2(velocity.y, velocity.x)
    length = velocity.length / 8  # Scale the length of the arrow

    # Calculate positions
    arrow_head = (position.x + length * math.cos(angle), screen_height - position.y - length * math.sin(angle))
    arrow_tail = (position.x, screen_height - position.y)
    
    # Calculate midpoint for text placement
    text_pos = (
        (arrow_tail[0] + arrow_head[0])/2 + 10 * math.cos(angle + math.pi/2),
        (arrow_tail[1] + arrow_head[1])/2 + 10 * math.sin(angle + math.pi/2)
    )

    # Draw arrow
    pygame.draw.line(screen, (255, 0, 0), arrow_tail, arrow_head, 2)
    pygame.draw.polygon(screen, (255, 0, 0), [
        (arrow_head[0] + 5 * math.cos(angle + math.pi / 2), arrow_head[1] - 5 * math.sin(angle + math.pi / 2)),
        (arrow_head[0] + 5 * math.cos(angle - math.pi / 2), arrow_head[1] - 5 * math.sin(angle - math.pi / 2)),
        (arrow_head[0] + 10 * math.cos(angle), arrow_head[1] - 10 * math.sin(angle))
    ])

    # Calculate and draw velocity magnitude
    velocity_mag = round(velocity.length, 1)  # In pymunk units
    text_surface, _ = font.render(f"{round(velocity_mag/50, 2)} m/s", (0, 0, 0)) # 50 pixels: 1 meter
    screen.blit(text_surface, text_pos)

def bouncy_ball(num_balls, args_list, gravity):
    # Initialize Pygame
    pygame.init()
    pygame.freetype.init()
    font = pygame.freetype.SysFont('Arial', 16)

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
        balls.append(Ball(args_list[i], screen_height))
        balls[i].acceleration_y -= gravity
        balls[i].object = balls[i].create_ball(space)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        for i in range(num_balls):
            # Apply acceleration (convert screen coordinates to Pymunk forces)
            force = (balls[i].mass * balls[i].acceleration_x, balls[i].mass * -balls[i].acceleration_y)
            balls[i].object.apply_force_at_world_point(force, balls[i].object.position)

        # Update physics
        space.step(1/60.0)
        
        # Draw everything
        screen.fill((255, 255, 255))
        
        # Draw ball (convert Pymunk coordinates to screen coordinates)
        for i in range(num_balls):
            ball_pos = int(balls[i].object.position.x), screen_height - int(balls[i].object.position.y)
            pygame.draw.circle(screen, (173, 216, 230), ball_pos, balls[i].radius)
            draw_arrow(screen, balls[i].object, screen_height, font)
        
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

num_balls = 3
args_list = [{'x': 200,'y': 300,'vx': 100,'vy': 0,'ax': 0,'ay': 0,'elasticity': 1,'friction': 0.0,'mass': 2,'radius': 15},
             {'x': 200,'y': 200,'vx': 300,'vy': 0,'ax': 0,'ay': 0,'elasticity': 1,'friction': 0.0,'mass': 2,'radius': 15},
             {'x': 200,'y': 100,'vx': 500,'vy': 0,'ax': 0,'ay': 0,'elasticity': 1,'friction': 0.0,'mass': 2,'radius': 15}]

def main():
    bouncy_ball(num_balls, args_list, 0)

if __name__ == "__main__":
    main()