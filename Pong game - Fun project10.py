# Pong game - Fun project10 

## Import the necessary libraries
import pygame, sys

## Initialize pygame
pygame.init()

## Set Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Game")

## Set Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

## Set clock to control the frame rate
clock = pygame.time.Clock()

## Game state variables
game_state = "menu"  # menu, playing
game_mode = "medium"  # easy, medium, hard
players = 1  # 1 or 2

## Set ball attributes
ball = pygame.Rect(WIDTH // 2 - 15, HEIGHT // 2 - 15, 30, 30)
ball_speed_x = 4 * (1 if pygame.time.get_ticks() % 2 == 0 else -1)
ball_speed_y = 4 * (1 if pygame.time.get_ticks() % 2 == 0 else -1)

## Set paddle attributes
player = pygame.Rect(WIDTH - 20, HEIGHT // 2 - 70, 10, 140)
opponent = pygame.Rect(10, HEIGHT // 2 - 70, 10, 140)
player_speed = 0
opponent_speed = 7
player2_speed = 0  # For second player in 2-player mode

## Set Scores
player_score = 0
opponent_score = 0
font = pygame.font.Font(None, 50)
menu_font = pygame.font.Font(None, 36)

## Define a function to reset the ball
def ball_reset():
    global ball_speed_x, ball_speed_y
    ball.center = (WIDTH // 2, HEIGHT // 2)
    ball_speed_x *= -1
    ball_speed_y = 4 * (1 if pygame.time.get_ticks() % 2 == 0 else -1)

## Function to draw menu
def draw_menu():
    screen.fill(BLACK)
    
    # Title
    title = menu_font.render("PONG GAME", True, WHITE)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 50))
    
    # Difficulty selection
    diff_text = menu_font.render("Select Difficulty:", True, WHITE)
    screen.blit(diff_text, (WIDTH//2 - diff_text.get_width()//2, 150))
    
    easy_text = menu_font.render("1 - Easy", True, WHITE if game_mode != "easy" else BLUE)
    medium_text = menu_font.render("2 - Medium", True, WHITE if game_mode != "medium" else BLUE)
    hard_text = menu_font.render("3 - Hard", True, WHITE if game_mode != "hard" else BLUE)
    
    screen.blit(easy_text, (WIDTH//2 - easy_text.get_width()//2, 200))
    screen.blit(medium_text, (WIDTH//2 - medium_text.get_width()//2, 250))
    screen.blit(hard_text, (WIDTH//2 - hard_text.get_width()//2, 300))
    
    # Player selection
    player_text = menu_font.render("Select Players:", True, WHITE)
    screen.blit(player_text, (WIDTH//2 - player_text.get_width()//2, 350))
    
    one_player = menu_font.render("4 - 1 Player (vs Computer)", True, WHITE if players != 1 else BLUE)
    two_players = menu_font.render("5 - 2 Players", True, WHITE if players != 2 else BLUE)
    
    screen.blit(one_player, (WIDTH//2 - one_player.get_width()//2, 400))
    screen.blit(two_players, (WIDTH//2 - two_players.get_width()//2, 450))
    
    # Start game
    start_text = menu_font.render("Press SPACE to Start Game", True, WHITE)
    screen.blit(start_text, (WIDTH//2 - start_text.get_width()//2, 520))

## Main game loop
while True:
    ### Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if game_state == "menu":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    game_mode = "easy"
                elif event.key == pygame.K_2:
                    game_mode = "medium"
                elif event.key == pygame.K_3:
                    game_mode = "hard"
                elif event.key == pygame.K_4:
                    players = 1
                elif event.key == pygame.K_5:
                    players = 2
                elif event.key == pygame.K_SPACE:
                    game_state = "playing"
                    # Set opponent speed based on difficulty
                    if game_mode == "easy":
                        opponent_speed = 5
                    elif game_mode == "medium":
                        opponent_speed = 7
                    elif game_mode == "hard":
                        opponent_speed = 9
        else:  # game_state == "playing"
            if event.type == pygame.KEYDOWN:
                if players == 1:
                    if event.key == pygame.K_UP:
                        player_speed = -7
                    if event.key == pygame.K_DOWN:
                        player_speed = 7
                else:  # 2 players
                    if event.key == pygame.K_UP:
                        player_speed = -7
                    if event.key == pygame.K_DOWN:
                        player_speed = 7
                    if event.key == pygame.K_w:
                        player2_speed = -7
                    if event.key == pygame.K_s:
                        player2_speed = 7
            if event.type == pygame.KEYUP:
                if players == 1:
                    if event.key in [pygame.K_UP, pygame.K_DOWN]:
                        player_speed = 0
                else:  # 2 players
                    if event.key in [pygame.K_UP, pygame.K_DOWN]:
                        player_speed = 0
                    if event.key in [pygame.K_w, pygame.K_s]:
                        player2_speed = 0
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                game_state = "menu"
                player_score = 0
                opponent_score = 0
                ball_reset()

    if game_state == "menu":
        draw_menu()
    else:  # game_state == "playing"
        ### Move player paddle (right)
        player.y += player_speed
        if player.top < 0:
            player.top = 0
        if player.bottom > HEIGHT:
            player.bottom = HEIGHT

        ### Move opponent paddle (left)
        if players == 1:  # Computer opponent
            if opponent.top < ball.y:
                opponent.y += opponent_speed
            if opponent.bottom > ball.y:
                opponent.y -= opponent_speed
        else:  # Human opponent (player 2)
            opponent.y += player2_speed
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
        pygame.draw.rect(screen, BLUE, player)  # Right paddle is blue
        pygame.draw.rect(screen, RED, opponent)  # Left paddle is red
        pygame.draw.ellipse(screen, WHITE, ball)
        pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

        ### Render scores
        player_text = font.render(f"{player_score}", True, BLUE)
        opponent_text = font.render(f"{opponent_score}", True, RED)
        screen.blit(player_text, (WIDTH // 2 + 20, 20))
        screen.blit(opponent_text, (WIDTH // 2 - 40, 20))

        ### Display game mode and controls
        mode_text = menu_font.render(f"Mode: {game_mode.capitalize()} | Players: {players}", True, WHITE)
        screen.blit(mode_text, (10, HEIGHT - 30))
        esc_text = menu_font.render("ESC: Menu", True, WHITE)
        screen.blit(esc_text, (WIDTH - esc_text.get_width() - 10, HEIGHT - 30))

    ### Update the display
    pygame.display.flip()

    ### Control frame rate
    clock.tick(60)
