# Snake Game - Fun project9

## Import all the necessary liabraries
import pygame,time,random

## Initialize pygame
pygame.init()

## Set Screen dimensions
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

## Set Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)
DARK_GREEN = (0, 200, 0)
HEAD_BLUE = (30, 120, 180)

## Set Clock and font
clock = pygame.time.Clock()
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

## Set Snake parameters
snake_block = 10
snake_speed = 15

## Display score
def your_score(score):
    value = score_font.render(f"Your Score: {score}", True, BLUE)
    screen.blit(value, [0, 0])

## Create the main game loop
def gameLoop():
    game_over = False
    game_close = False

    ### Snake initial position
    x1, y1 = WIDTH // 2, HEIGHT // 2
    x1_change, y1_change = 0, 0

    ### Snake body
    snake_list = []
    length_of_snake = 1

    ### Set random food position
    foodx = round(random.randrange(0, WIDTH - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, HEIGHT - snake_block) / 10.0) * 10.0

    while not game_over:
        while game_close:
            screen.fill(BLACK)
            message = font_style.render("Game Over! Press C-Play Again or Q-Quit", True, RED)
            screen.blit(message, [WIDTH // 6, HEIGHT // 3])
            your_score(length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                # Arrow keys and WASD controls with reversal prevention
                if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and x1_change == 0:
                    x1_change = -snake_block
                    y1_change = 0
                elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and x1_change == 0:
                    x1_change = snake_block
                    y1_change = 0
                elif (event.key == pygame.K_UP or event.key == pygame.K_w) and y1_change == 0:
                    y1_change = -snake_block
                    x1_change = 0
                elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and y1_change == 0:
                    y1_change = snake_block
                    x1_change = 0

        # Check if snake hits the boundary
        if x1 >= WIDTH or x1 < 0 or y1 >= HEIGHT or y1 < 0:
            game_close = True

        # Update snake position
        x1 += x1_change
        y1 += y1_change
        screen.fill(BLACK)
        
        # Draw food as an apple
        pygame.draw.rect(screen, RED, [foodx, foody, snake_block, snake_block])
        pygame.draw.circle(screen, (200, 0, 0), 
                          (foodx + snake_block//2, foody + snake_block//2), 
                          snake_block//2)
        
        # Update snake body
        snake_head = [x1, y1]
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        # Check if snake hits itself
        for block in snake_list[:-1]:
            if block == snake_head:
                game_close = True

        # Draw snake with improved appearance
        for i, segment in enumerate(snake_list):
            # Draw the head differently
            if i == len(snake_list) - 1:
                # Draw head as a rounded rectangle
                pygame.draw.rect(screen, HEAD_BLUE, 
                                [segment[0], segment[1], snake_block, snake_block], 
                                0, 5)
                
                # Draw eyes based on direction
                eye_size = 2
                if x1_change > 0:  # Moving right
                    pygame.draw.circle(screen, WHITE, 
                                      (segment[0] + snake_block - 2, segment[1] + 3), 
                                      eye_size)
                    pygame.draw.circle(screen, WHITE, 
                                      (segment[0] + snake_block - 2, segment[1] + snake_block - 3), 
                                      eye_size)
                elif x1_change < 0:  # Moving left
                    pygame.draw.circle(screen, WHITE, 
                                      (segment[0] + 2, segment[1] + 3), 
                                      eye_size)
                    pygame.draw.circle(screen, WHITE, 
                                      (segment[0] + 2, segment[1] + snake_block - 3), 
                                      eye_size)
                elif y1_change < 0:  # Moving up
                    pygame.draw.circle(screen, WHITE, 
                                      (segment[0] + 3, segment[1] + 2), 
                                      eye_size)
                    pygame.draw.circle(screen, WHITE, 
                                      (segment[0] + snake_block - 3, segment[1] + 2), 
                                      eye_size)
                elif y1_change > 0:  # Moving down
                    pygame.draw.circle(screen, WHITE, 
                                      (segment[0] + 3, segment[1] + snake_block - 2), 
                                      eye_size)
                    pygame.draw.circle(screen, WHITE, 
                                      (segment[0] + snake_block - 3, segment[1] + snake_block - 2), 
                                      eye_size)
            else:
                # Draw body with gradient color (darker toward tail)
                color_intensity = max(50, 200 - (len(snake_list) - i)//2)
                segment_color = (0, color_intensity, 0)
                
                # Draw body segment with rounded corners
                pygame.draw.rect(screen, segment_color, 
                                [segment[0], segment[1], snake_block, snake_block], 
                                0, 3)
                
                # Draw a pattern on the body
                if i % 2 == 0:
                    pygame.draw.line(screen, (0, 150, 0), 
                                   (segment[0] + 2, segment[1] + snake_block//2),
                                   (segment[0] + snake_block - 2, segment[1] + snake_block//2), 
                                   1)

        your_score(length_of_snake - 1)
        pygame.display.update()

        # Check if snake eats food
        if abs(x1 - foodx) < snake_block and abs(y1 - foody) < snake_block:
            foodx = round(random.randrange(0, WIDTH - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, HEIGHT - snake_block) / 10.0) * 10.0
            length_of_snake += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()

gameLoop()
