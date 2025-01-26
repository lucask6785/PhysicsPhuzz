import pygame
import sys
import asyncio
from app import VARIABLES
import math
import pymunk
import pymunk.pygame_util
from ball import Ball, create_walls, draw_arrow, draw_force_arrow

# Initialize Pygame
pygame.init()

# Set the dimensions of the window
screen_width, screen_height = 640, 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Moving Ball")

# Game loop
async def main():
    # Define colors
    WHITE = (255, 255, 255)
    RED = (0, 255, 0)

    while True:
        # Ball settings
        if not VARIABLES:
            ball_radius = 20
            ball_x = screen_width // 2
            ball_y = screen_height // 2
            ball_speed = 5  # Speed at which the ball moves
            ball_direction = 1  # 1 means moving right, -1 means moving left

            while True:
                screen.fill(WHITE)

                # Handle events (like closing the window)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                # Update ball position
                ball_x += ball_speed * ball_direction

                # Reverse direction if the ball hits the edge of the screen
                if ball_x - ball_radius <= 0 or ball_x + ball_radius >= screen_width:
                    ball_direction *= -1

                # Draw the ball
                pygame.draw.circle(screen, RED, (ball_x, ball_y), ball_radius)

                # Update the display
                pygame.display.flip()

                # Control the frame rate
                pygame.time.Clock().tick(60)
                await asyncio.sleep(0)
                if VARIABLES:
                    break
                
        else:
            screen.fill(WHITE)
            velocity_display = False
            acceleration_display = False
            centripetal = True

            font = pygame.freetype.SysFont('Arial', 20)
            pygame.display.set_caption("Centripetal Acceleration Simulation")
            clock = pygame.time.Clock()
            
            # Physics space
            space = pymunk.Space()
            space.gravity = (0, 0)
            
            create_walls(space, screen_width, screen_height)

            # Create rotating ball
            center = (screen_width//2, screen_height//2)
            radius = 200
            mass = 2
            tangential_speed = 100  # pixels/second
            
            args = {
                'x': center[0] + radius,
                'y': center[1],
                'vx': 0,
                'vy': tangential_speed,
                'ax': 0,
                'ay': 0,
                'elasticity': 1.0,
                'friction': 0.0,
                'mass': mass,
                'radius': 15
            }
            
            ball = Ball(args, screen_height)
            ball.object = ball.create_ball(space)
            
            running = True
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
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
                        elif event.key == pygame.K_c:
                            if centripetal == True:
                                centripetal = False
                            else:
                                centripetal = True
                
                # Calculate and apply centripetal force
                body = ball.object
                dx = center[0] - (body.position.x)
                dy = center[1] - (screen_height - body.position.y)
                r = math.hypot(dx, dy)
                
                if r > 0:  # Avoid division by zero
                    # Calculate required centripetal force (F = mv²/r)
                    vx, vy = body.velocity.x, body.velocity.y
                    speed_sq = vx**2 + vy**2
                    force_mag = (mass * speed_sq) / r
                    
                    # Force direction towards center
                    fx = force_mag * (dx / r)
                    fy = force_mag * (dy / r)
                    
                    # Apply force in Pymunk coordinates (flip y)
                    if centripetal:
                        body.apply_force_at_world_point((fx, -fy), body.position)
                
                # Physics step
                space.step(1/60.0)
                
                # Draw everything
                screen.fill((255, 255, 255))
                
                # Draw center point
                pygame.draw.circle(screen, (255, 0, 0), center, 5)
                
                # Draw ball and arrows
                ball_pos = (int(body.position.x), screen_height - int(body.position.y))
                pygame.draw.circle(screen, (0, 0, 255), ball_pos, ball.radius)
                
                # Draw velocity arrow (red)
                draw_arrow(screen, body, screen_height, font, velocity_display)
                
                # Draw centripetal force arrow (green)
                if r > 0:
                    force_vector = (fx, -fy)  # Convert to Pymunk coordinates
                    draw_force_arrow(screen, body.position, force_vector, screen_height, font, acceleration_display)
                
                pygame.display.flip()
                clock.tick(60)

asyncio.run(main())
