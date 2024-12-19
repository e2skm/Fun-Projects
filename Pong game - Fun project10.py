# Pong game - Fun project10

## Import the necessary liabraries
import pygame,sys

## Initialize pygame
pygame.init()

## Set Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Game")

## Set Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

## Set clock to control the frame rate
clock = pygame.time.Clock()

## Set ball attributes
ball = pygame.Rect(WIDTH // 2 - 15, HEIGHT // 2 - 15, 30, 30)
ball_speed_x = 4 * (1 if pygame.time.get_ticks() % 2 == 0 else -1)
ball_speed_y = 4 * (1 if pygame.time.get_ticks() % 2 == 0 else -1)

## Set paddle attributes
player = pygame.Rect(WIDTH - 20, HEIGHT // 2 - 70, 10, 140)
opponent = pygame.Rect(10, HEIGHT // 2 - 70, 10, 140)
player_speed = 0
opponent_speed = 7

## Set Scores
player_score = 0
opponent_score = 0
font = pygame.font.Font(None, 50)

## Define a function to reset the ball
def ball_reset():
    global ball_speed_x, ball_speed_y
    ball.center = (WIDTH // 2, HEIGHT // 2)
    ball_speed_x *= -1
    ball_speed_y = 4 * (1 if pygame.time.get_ticks() % 2 == 0 else -1)

## Main game loop
while True:
    ### Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player_speed = -7
            if event.key == pygame.K_DOWN:
                player_speed = 7
        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_UP, pygame.K_DOWN]:
                player_speed = 0

    ### Move player paddle
    player.y += player_speed
    if player.top < 0:
        player.top = 0
    if player.bottom > HEIGHT:
        player.bottom = HEIGHT

    ### Move opponent paddle
    if opponent.top < ball.y:
        opponent.y += opponent_speed
    if opponent.bottom > ball.y:
        opponent.y -= opponent_speed
    if opponent.top < 0:
        opponent.top = 0
    if opponent.bottom > HEIGHT:
        opponent.bottom = HEIGHT

    ### Ball movement
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    ### Ball collision with top and bottom
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed_y *= -1

    ### Ball collision with paddles
    if ball.colliderect(player) or ball.colliderect(opponent):
        ball_speed_x *= -1

    ### Scoring
    if ball.left <= 0:
        player_score += 1
        ball_reset()
    if ball.right >= WIDTH:
        opponent_score += 1
        ball_reset()

    ### Draw everything
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, player)
    pygame.draw.rect(screen, WHITE, opponent)
    pygame.draw.ellipse(screen, WHITE, ball)
    pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

    ### Render scores
    player_text = font.render(f"{player_score}", True, WHITE)
    opponent_text = font.render(f"{opponent_score}", True, WHITE)
    screen.blit(player_text, (WIDTH // 2 + 20, 20))
    screen.blit(opponent_text, (WIDTH // 2 - 40, 20))

    ### Update the display
    pygame.display.flip()

    ### Control frame rate
    clock.tick(60)
