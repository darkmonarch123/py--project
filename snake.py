import pygame
import random
import sys

# --------------------------------------------------------
# 1. Initialize Pygame and Setup Window
# --------------------------------------------------------
pygame.init()

WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Retro Snake Game")

# Colors (R, G, B format)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 50, 50)
GREEN = (50, 255, 50)

# Game Speed and Size
SNAKE_SIZE = 20
clock = pygame.time.Clock()

# --------------------------------------------------------
# 2. Main Game Function
# --------------------------------------------------------
def start_game():
    # Snake initial positions
    x = WIDTH // 2
    y = HEIGHT // 2
    
    # Movement speeds (starts stationary until a key is pressed)
    x_speed = 0
    y_speed = 0
    
    # Track the body blocks of the snake
    snake_body = [[x, y]]
    length_of_snake = 1
    
    # Spawn the first piece of food on a clean grid coordinate
    food_x = round(random.randrange(0, WIDTH - SNAKE_SIZE) / SNAKE_SIZE) * SNAKE_SIZE
    food_y = round(random.randrange(0, HEIGHT - SNAKE_SIZE) / SNAKE_SIZE) * SNAKE_SIZE
    
    score = 0

    # The Core Game Loop
    while True:
        # Check for keyboard inputs or window closing
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x_speed == 0:
                    x_speed = -SNAKE_SIZE
                    y_speed = 0
                elif event.key == pygame.K_RIGHT and x_speed == 0:
                    x_speed = SNAKE_SIZE
                    y_speed = 0
                elif event.key == pygame.K_UP and y_speed == 0:
                    x_speed = 0
                    y_speed = -SNAKE_SIZE
                elif event.key == pygame.K_DOWN and y_speed == 0:
                    x_speed = 0
                    y_speed = SNAKE_SIZE

        # Update the position of the snake head
        x += x_speed
        y += y_speed
        
        # --- Collision Checks ---
        # 1. Hit the boundaries?
        if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
            break 
            
        # Add new head position to the body array
        snake_body.append([x, y])
        
        # Maintain correct snake length (chop off the tail as it moves forward)
        if len(snake_body) > length_of_snake:
            del snake_body[0]
            
        # 2. Hit your own body?
        if [x, y] in snake_body[:-1]:
            break 

        # --- Rendering / Drawing Graphics ---
        screen.fill(BLACK) # Clear screen with black background
        
        # Draw Food (Red Square)
        pygame.draw.rect(screen, RED, [food_x, food_y, SNAKE_SIZE, SNAKE_SIZE])
        
        # Draw Snake (Green Squares)
        for segment in snake_body:
            pygame.draw.rect(screen, GREEN, [segment[0], segment[1], SNAKE_SIZE - 2, SNAKE_SIZE - 2])
            
        pygame.display.update() # Refresh the screen graphics

        # --- Eating Food Mechanism ---
        if x == food_x and y == food_y:
            # Re-spawn food in a new random spot
            food_x = round(random.randrange(0, WIDTH - SNAKE_SIZE) / SNAKE_SIZE) * SNAKE_SIZE
            food_y = round(random.randrange(0, HEIGHT - SNAKE_SIZE) / SNAKE_SIZE) * SNAKE_SIZE
            length_of_snake += 1
            score += 1

        clock.tick(10) # Game speed set to 10 Frames Per Second

    # If loops breaks, it means Game Over
    print(f"\n==============================")
    print(f" GAME OVER, SIR.")
    print(f" Final Score: {score}")
    print(f"==============================\n")
    pygame.quit()

# --------------------------------------------------------
# 3. Code Entry Point
# --------------------------------------------------------
if __name__ == "__main__":
    start_game()