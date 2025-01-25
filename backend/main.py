import pygame
import sys
import asyncio

# Initialize Pygame
pygame.init()

# Set the dimensions of the window
WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Ball")


# Game loop
async def main():
    # Define colors
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)

    # Ball settings
    ball_radius = 20
    ball_x = WIDTH // 2
    ball_y = HEIGHT // 2
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
        if ball_x - ball_radius <= 0 or ball_x + ball_radius >= WIDTH:
            ball_direction *= -1

        # Draw the ball
        pygame.draw.circle(screen, RED, (ball_x, ball_y), ball_radius)

        # Update the display
        pygame.display.flip()

        # Control the frame rate
        pygame.time.Clock().tick(60)
        await asyncio.sleep(0)

asyncio.run(main())
