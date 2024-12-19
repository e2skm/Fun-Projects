# Snake Game - Fun project9

## Import all the necessary liabraries
import pygame,time,random

## Initialize pygame
pygame.init()

## Set Screen dimensions
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

#$# Set Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)

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
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        if x1 >= WIDTH or x1 < 0 or y1 >= HEIGHT or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        screen.fill(BLACK)
        pygame.draw.rect(screen, GREEN, [foodx, foody, snake_block, snake_block])
        snake_head = [x1, y1]
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for block in snake_list[:-1]:
            if block == snake_head:
                game_close = True

        for block in snake_list:
            pygame.draw.rect(screen, WHITE, [block[0], block[1], snake_block, snake_block])

        your_score(length_of_snake - 1)
        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, WIDTH - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, HEIGHT - snake_block) / 10.0) * 10.0
            length_of_snake += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()

gameLoop()
