# Snake Game - Enhanced with Game Modes, High Score, and Sound Effects

## Import all the necessary libraries
import pygame, time, random, os

## Initialize pygame and mixer
pygame.init()
pygame.mixer.init()

## Set Screen dimensions
WIDTH, HEIGHT = 700, 450
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
YELLOW = (255, 255, 0)

## Set Clock and font
clock = pygame.time.Clock()
font_style = pygame.font.SysFont("arial", 20)
score_font = pygame.font.SysFont("arial", 20)
mode_font = pygame.font.SysFont("arial", 20)

## Set Snake parameters
snake_block = 10
snake_speeds = {"easy": 10, "medium": 15, "hard": 20}
current_mode = "medium"

## High score handling
HIGH_SCORE_FILE = "snake_highscore.txt"
high_score = 0

# Load high score from file
def load_high_score():
    global high_score
    if os.path.exists(HIGH_SCORE_FILE):
        try:
            with open(HIGH_SCORE_FILE, 'r') as f:
                high_score = int(f.read())
        except:
            high_score = 0
    return high_score

# Save high score to file
def save_high_score(score):
    with open(HIGH_SCORE_FILE, 'w') as f:
        f.write(str(score))

# Initialize high score
load_high_score()

## Sound effects
def load_sound(filename):
    try:
        return pygame.mixer.Sound(filename)
    except:
        print(f"Warning: Could not load sound {filename}")
        return None

eat_sound = load_sound("eat.wav")  # Placeholder - create these sound files
die_sound = load_sound("die.wav")  # or use pygame.mixer.Sound(buffer) for simple tones
high_score_sound = load_sound("high_score.wav")

# Simple sound generation if files are missing
if eat_sound is None:
    eat_sound = pygame.mixer.Sound(buffer=bytes([128] * 8000))
if die_sound is None:
    die_sound = pygame.mixer.Sound(buffer=bytes([128] * 16000))
if high_score_sound is None:
    high_score_sound = pygame.mixer.Sound(buffer=bytes([128] * 12000))

## Display score
def your_score(score):
    value = score_font.render(f"Score: {score}", True, BLUE)
    screen.blit(value, [10, 10])

## Display high score
def display_high_score():
    value = score_font.render(f"High Score: {high_score}", True, GREEN)
    screen.blit(value, [WIDTH - value.get_width() - 10, 10])

## Display current game mode
def display_game_mode():
    mode_text = f"Mode: {current_mode.capitalize()}"
    value = mode_font.render(mode_text, True, YELLOW)
    screen.blit(value, [WIDTH // 2 - value.get_width() // 2, 10])

## Main menu for game mode selection
def game_mode_menu():
    global current_mode
    
    menu = True
    selected = "medium"
    
    while menu:
        screen.fill(BLACK)
        
        title = score_font.render("SELECT GAME MODE", True, GREEN)
        screen.blit(title, [WIDTH//2 - title.get_width()//2, 50])
        
        modes = ["easy", "medium", "hard"]
        y_pos = 150
        for mode in modes:
            color = WHITE
            if mode == selected:
                color = YELLOW
            text = font_style.render(f"{mode.capitalize()} (Speed: {snake_speeds[mode]})", True, color)
            screen.blit(text, [WIDTH//2 - text.get_width()//2, y_pos])
            y_pos += 50
        
        instruction = font_style.render("Press UP/DOWN to select, ENTER to confirm", True, WHITE)
        screen.blit(instruction, [WIDTH//2 - instruction.get_width()//2, HEIGHT - 80])
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    index = modes.index(selected)
                    selected = modes[(index - 1) % len(modes)]
                elif event.key == pygame.K_DOWN:
                    index = modes.index(selected)
                    selected = modes[(index + 1) % len(modes)]
                elif event.key == pygame.K_RETURN:
                    current_mode = selected
                    menu = False
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
    
    return snake_speeds[current_mode]

## Create the main game loop
def gameLoop():
    global high_score
    
    speed = game_mode_menu()
    game_over = False
    game_close = False
    broke_record = False

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
            message = font_style.render("Game Over! Press C-Play Again, M-Menu, or Q-Quit", True, RED)
            screen.blit(message, [WIDTH // 6, HEIGHT // 3])
            your_score(length_of_snake - 1)
            display_high_score()
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_close = False
                        # Reset game state
                        x1, y1 = WIDTH // 2, HEIGHT // 2
                        x1_change, y1_change = 0, 0
                        snake_list = []
                        length_of_snake = 1
                        broke_record = False
                    if event.key == pygame.K_m:
                        game_close = False
                        game_over = True  # Exit to main menu

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
                # Change game mode during play
                elif event.key == pygame.K_m:
                    speed = game_mode_menu()
                    # Reset game state
                    x1, y1 = WIDTH // 2, HEIGHT // 2
                    x1_change, y1_change = 0, 0
                    snake_list = []
                    length_of_snake = 1
                    broke_record = False

        # Check if snake hits the boundary
        if x1 >= WIDTH or x1 < 0 or y1 >= HEIGHT or y1 < 0:
            die_sound.play()
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
                die_sound.play()
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
        display_high_score()
        display_game_mode()
        pygame.display.update()

        # Check if snake eats food
        if abs(x1 - foodx) < snake_block and abs(y1 - foody) < snake_block:
            eat_sound.play()
            foodx = round(random.randrange(0, WIDTH - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, HEIGHT - snake_block) / 10.0) * 10.0
            length_of_snake += 1
            
            # Check for new high score
            current_score = length_of_snake - 1
            if current_score > high_score:
                if not broke_record:  # Play sound only when first breaking record
                    high_score_sound.play()
                    broke_record = True
                high_score = current_score
                save_high_score(high_score)

        clock.tick(speed)

    # Return to main menu after game over
    gameLoop()

# Start the game
gameLoop()
