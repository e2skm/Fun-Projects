# Pong game - Improved Version with difficulty-based ball speed and expanded options

# Import all the necessary libraries
import pygame, sys, time, numpy, random

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
# Clock for frame rate
clock = pygame.time.Clock()

# Sound effects
def create_sound(frequency=440, duration=100):
    sample_rate = 44100
    samples = int(sample_rate * duration / 1000)
    buffer = numpy.zeros((samples, 2), dtype=numpy.int16)
    for s in range(samples):
        t = float(s)/sample_rate
        buffer[s][0] = int(32767 * 0.5 * numpy.sin(2 * numpy.pi * frequency * t))
        buffer[s][1] = int(32767 * 0.5 * numpy.sin(2 * numpy.pi * frequency * t))
    return pygame.mixer.Sound(buffer)

hit_sound = create_sound(660, 50)
score_sound = create_sound(880, 100)
game_over_sound = create_sound(220, 500)

# Game state
game_state = "main_menu"
game_mode = "medium"
players = 1
game_condition = "score"
end_score = 10  # Changed default to new middle option
game_duration = 300  # Changed default to 5 minutes (300 seconds)
game_start_time = 0
paused_time = 0
is_paused = False

# Track who serves next (player or opponent)
serve_to = "player"  # Start by serving to player

# Game objects
ball = pygame.Rect(WIDTH//2 - 15, HEIGHT//2 - 15, 30, 30)
# Base speeds for medium difficulty
base_ball_speed_x = 4
base_ball_speed_y = 4
ball_speed_x = base_ball_speed_x * (1 if pygame.time.get_ticks() % 2 == 0 else -1)
ball_speed_y = base_ball_speed_y * (1 if pygame.time.get_ticks() % 2 == 0 else -1)

player = pygame.Rect(WIDTH - 20, HEIGHT//2 - 70, 10, 140)
opponent = pygame.Rect(10, HEIGHT//2 - 70, 10, 140)
player_speed = 0
opponent_speed = 7
player2_speed = 0

# Scores
player_score = 0
opponent_score = 0
font = pygame.font.Font(None, 50)
menu_font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

def ball_reset():
    global ball_speed_x, ball_speed_y, base_ball_speed_x, base_ball_speed_y
    
    # Adjust base speed based on difficulty
    if game_mode == "easy":
        base_ball_speed_x = 3
        base_ball_speed_y = 3
    elif game_mode == "medium":
        base_ball_speed_x = 4
        base_ball_speed_y = 4
    elif game_mode == "hard":
        base_ball_speed_x = 6
        base_ball_speed_y = 6
    
    ball.center = (WIDTH//2, HEIGHT//2)
    
    # Determine serve direction based on who should serve
    if serve_to == "player":  # Serve to player (from left)
        ball_speed_x = abs(base_ball_speed_x)  # Moving right toward player
    else:  # Serve to opponent (from right)
        ball_speed_x = -abs(base_ball_speed_x)  # Moving left toward opponent
    
    # Random vertical angle
    ball_speed_y = base_ball_speed_y * random.choice([-1, 1]) * random.uniform(0.7, 1.3)

def play_sound(sound):
    sound.play()

def draw_main_menu():
    screen.fill(BLACK)
    title = menu_font.render("PONG GAME", True, WHITE)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))
    start_text = menu_font.render("Press SPACE to Start", True, WHITE)
    screen.blit(start_text, (WIDTH//2 - start_text.get_width()//2, 300))
    instr_text = small_font.render("Use arrow keys to navigate, SPACE to select", True, WHITE)
    screen.blit(instr_text, (WIDTH//2 - instr_text.get_width()//2, 500))

def draw_mode_menu():
    screen.fill(BLACK)
    title = menu_font.render("SELECT GAME MODE", True, WHITE)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))
    
    easy_text = menu_font.render("Easy", True, GREEN if game_mode == "easy" else WHITE)
    medium_text = menu_font.render("Medium", True, GREEN if game_mode == "medium" else WHITE)
    hard_text = menu_font.render("Hard", True, GREEN if game_mode == "hard" else WHITE)
    
    screen.blit(easy_text, (WIDTH//2 - easy_text.get_width()//2, 200))
    screen.blit(medium_text, (WIDTH//2 - medium_text.get_width()//2, 250))
    screen.blit(hard_text, (WIDTH//2 - hard_text.get_width()//2, 300))

def draw_players_menu():
    screen.fill(BLACK)
    title = menu_font.render("SELECT PLAYERS", True, WHITE)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))
    
    one_player = menu_font.render("1 Player", True, GREEN if players == 1 else WHITE)
    two_players = menu_font.render("2 Players", True, GREEN if players == 2 else WHITE)
    
    screen.blit(one_player, (WIDTH//2 - one_player.get_width()//2, 200))
    screen.blit(two_players, (WIDTH//2 - two_players.get_width()//2, 250))

def draw_condition_menu():
    screen.fill(BLACK)
    title = menu_font.render("GAME CONDITION", True, WHITE)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))
    
    score_text = menu_font.render("First to Score", True, GREEN if game_condition == "score" else WHITE)
    time_text = menu_font.render("Time Limit", True, GREEN if game_condition == "time" else WHITE)
    
    screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 200))
    screen.blit(time_text, (WIDTH//2 - time_text.get_width()//2, 250))
    
    if game_condition == "score":
        value_text = menu_font.render(f"Target: {end_score}", True, YELLOW)
        screen.blit(value_text, (WIDTH//2 - value_text.get_width()//2, 350))
    else:
        mins, secs = divmod(game_duration, 60)
        value_text = menu_font.render(f"Duration: {mins:02d}:{secs:02d}", True, YELLOW)
        screen.blit(value_text, (WIDTH//2 - value_text.get_width()//2, 350))

def draw_game_over():
    screen.fill(BLACK)
    title = menu_font.render("GAME OVER", True, WHITE)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))
    
    if players == 1:
        result_text = menu_font.render(f"Player: {player_score}  Computer: {opponent_score}", True, WHITE)
    else:
        result_text = menu_font.render(f"Player 1: {player_score}  Player 2: {opponent_score}", True, WHITE)
    screen.blit(result_text, (WIDTH//2 - result_text.get_width()//2, 200))
    
    winner = None
    if player_score > opponent_score:
        winner = "Player 1 Wins!" if players == 2 else "You Win!"
    elif opponent_score > player_score:
        winner = "Player 2 Wins!" if players == 2 else "Computer Wins!"
    else:
        winner = "It's a Tie!"
    
    winner_text = menu_font.render(winner, True, YELLOW)
    screen.blit(winner_text, (WIDTH//2 - winner_text.get_width()//2, 300))
    
    restart_text = menu_font.render("Press SPACE to return to menu", True, WHITE)
    screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, 400))

def get_remaining_time():
    if is_paused:
        return game_duration - (paused_time - game_start_time)
    return max(0, game_duration - (time.time() - game_start_time))

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if game_state == "playing":
                    is_paused = not is_paused
                    if is_paused:
                        paused_time = time.time()
                    else:
                        game_start_time += time.time() - paused_time
                else:
                    if game_state == "mode_menu":
                        game_state = "main_menu"
                    elif game_state == "players_menu":
                        game_state = "mode_menu"
                    elif game_state == "condition_menu":
                        game_state = "players_menu"
            
            if event.key == pygame.K_SPACE:
                if game_state == "main_menu":
                    game_state = "mode_menu"
                elif game_state == "mode_menu":
                    game_state = "players_menu"
                elif game_state == "players_menu":
                    game_state = "condition_menu"
                elif game_state == "condition_menu":
                    game_state = "playing"
                    game_start_time = time.time()
                    player_score = 0
                    opponent_score = 0
                    serve_to = "player"  # Reset serve direction to initial (serve to player)
                    ball_reset()
                elif game_state == "game_over":
                    game_state = "main_menu"
            
            if event.key == pygame.K_UP:
                if game_state == "mode_menu":
                    if game_mode == "medium":
                        game_mode = "easy"
                    elif game_mode == "hard":
                        game_mode = "medium"
                elif game_state == "players_menu":
                    players = 1
                elif game_state == "condition_menu":
                    game_condition = "score"
            
            if event.key == pygame.K_DOWN:
                if game_state == "mode_menu":
                    if game_mode == "easy":
                        game_mode = "medium"
                    elif game_mode == "medium":
                        game_mode = "hard"
                elif game_state == "players_menu":
                    players = 2
                elif game_state == "condition_menu":
                    game_condition = "time"
            
            if event.key == pygame.K_LEFT:
                if game_state == "condition_menu":
                    if game_condition == "score" and end_score > 5:
                        end_score -= 5
                    elif game_condition == "time" and game_duration > 120:
                        game_duration -= 180  # Decrease by 3 minutes (180 seconds)
            
            if event.key == pygame.K_RIGHT:
                if game_state == "condition_menu":
                    if game_condition == "score":
                        end_score += 5
                    elif game_condition == "time":
                        game_duration += 180  # Increase by 3 minutes (180 seconds)
            
            if game_state == "playing" and not is_paused:
                # Player 1 controls (both in 1P and 2P modes)
                if event.key == pygame.K_UP:
                    player_speed = -7
                if event.key == pygame.K_DOWN:
                    player_speed = 7
                # Alternative controls for Player 1 in 1P mode
                if players == 1:
                    if event.key == pygame.K_w:
                        player_speed = -7
                    if event.key == pygame.K_s:
                        player_speed = 7
                # Player 2 controls (only in 2P mode)
                if players == 2:
                    if event.key == pygame.K_w:
                        player2_speed = -7
                    if event.key == pygame.K_s:
                        player2_speed = 7
        
        if event.type == pygame.KEYUP:
            if game_state == "playing":
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    player_speed = 0
                # Handle alternative controls release in 1P mode
                if players == 1:
                    if event.key == pygame.K_w or event.key == pygame.K_s:
                        player_speed = 0
                if players == 2:
                    if event.key == pygame.K_w or event.key == pygame.K_s:
                        player2_speed = 0

    if game_state == "playing" and not is_paused:
        # Paddle movement
        player.y += player_speed
        player.y = max(0, min(player.y, HEIGHT - player.height))
        
        if players == 1:  # Computer opponent
            if game_mode == "easy":
                if pygame.time.get_ticks() % 20 == 0:
                    if opponent.centery < ball.centery:
                        opponent.y += opponent_speed
                    elif opponent.centery > ball.centery:
                        opponent.y -= opponent_speed
            else:
                if opponent.centery < ball.centery:
                    opponent.y += opponent_speed
                elif opponent.centery > ball.centery:
                    opponent.y -= opponent_speed
            opponent.y = max(0, min(opponent.y, HEIGHT - opponent.height))
        else:  # Human opponent
            opponent.y += player2_speed
            opponent.y = max(0, min(opponent.y, HEIGHT - opponent.height))

        # Ball movement with strict boundary checking
        ball.x += ball_speed_x
        ball.y += ball_speed_y

        # Vertical boundary check - keep ball on screen
        if ball.top <= 0:
            ball.top = 0
            ball_speed_y *= -1
            play_sound(hit_sound)
        elif ball.bottom >= HEIGHT:
            ball.bottom = HEIGHT
            ball_speed_y *= -1
            play_sound(hit_sound)

        # Horizontal boundary check - scoring
        if ball.left <= 0:
            player_score += 1  # Player 1 (right) scores
            play_sound(score_sound)
            serve_to = "player"  # Next serve goes to player (from left)
            ball_reset()
        elif ball.right >= WIDTH:
            opponent_score += 1  # Player 2/Computer (left) scores
            play_sound(score_sound)
            serve_to = "opponent"  # Next serve goes to opponent (from right)
            ball_reset()

        # Paddle collisions
        if ball.colliderect(player) or ball.colliderect(opponent):
            ball_speed_x *= -1
            # Add slight angle variation
            ball_speed_y += 0.5 * (1 if pygame.time.get_ticks() % 2 == 0 else -1)
            play_sound(hit_sound)
            # Ensure ball doesn't get stuck in paddle
            if ball.colliderect(player):
                ball.left = player.left - ball.width
            else:
                ball.left = opponent.right

        # Game end conditions
        if game_condition == "score":
            if player_score >= end_score or opponent_score >= end_score:
                game_state = "game_over"
                play_sound(game_over_sound)
        else:
            if get_remaining_time() <= 0:
                game_state = "game_over"
                play_sound(game_over_sound)

    # Drawing
    screen.fill(BLACK)
    if game_state == "main_menu":
        draw_main_menu()
    elif game_state == "mode_menu":
        draw_mode_menu()
    elif game_state == "players_menu":
        draw_players_menu()
    elif game_state == "condition_menu":
        draw_condition_menu()
    elif game_state == "playing":
        pygame.draw.rect(screen, BLUE, player)
        pygame.draw.rect(screen, RED, opponent)
        pygame.draw.ellipse(screen, WHITE, ball)
        pygame.draw.aaline(screen, WHITE, (WIDTH//2, 0), (WIDTH//2, HEIGHT))
        
        # Scores
        player_text = font.render(f"{player_score}", True, BLUE)
        opponent_text = font.render(f"{opponent_score}", True, RED)
        screen.blit(player_text, (WIDTH//2 + 20, 20))
        screen.blit(opponent_text, (WIDTH//2 - 40, 20))
        
        # Game info
        mode_text = small_font.render(f"Mode: {game_mode.capitalize() if players == 1 else 'PVP'}", True, WHITE)
        screen.blit(mode_text, (10, HEIGHT - 60))
        
        if game_condition == "score":
            condition_text = small_font.render(f"Target: {end_score}", True, WHITE)
        else:
            mins, secs = divmod(int(get_remaining_time()), 60)
            condition_text = small_font.render(f"Time: {mins:02d}:{secs:02d}", True, WHITE)
        screen.blit(condition_text, (WIDTH - condition_text.get_width() - 10, HEIGHT - 60))
        
        if is_paused:
            # Draw pause overlay
            s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            s.fill((0, 0, 0, 180))
            screen.blit(s, (0, 0))
            pause_text = menu_font.render("PAUSED", True, WHITE)
            screen.blit(pause_text, (WIDTH//2 - pause_text.get_width()//2, HEIGHT//2 - 50))
    elif game_state == "game_over":
        draw_game_over()
    
    pygame.display.flip()
    clock.tick(60)
