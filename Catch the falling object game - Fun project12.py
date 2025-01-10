# Catch the falling object game - Fun project12

## Import the necessary liabraries
import random,pygame

## Initialize pygame
pygame.init()

## Set Screen dimensions
WIDTH = 800
HEIGHT = 600

## Set colors
WHITE = (255,255,255)
BLACK = (0,0,0)
RED =  (255,0,0)

## Create the screen and caption
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Catch the falling object')

## Set clock to control the frame rate
clock = pygame.time.Clock()

## Set player properties
playerWidth = 100
playerHeight = 20
playerX = WIDTH // 2 - playerWidth // 2
playerY = HEIGHT - 50 
playerSpeed = 7

## Set falling object properties
objectWidth = 30
objectHeight = 30 
objectX = random.randint(0,WIDTH - objectWidth)
objectY = 0
objectSpeed = 5

## Create a variable to keep the score 
score = 0

## Set font for displaying the score
font = pygame.font.Font(None,36)

## Main game loop
running = True
while running:
    for event in pygame.event.get():
        ### Event handling
        if event.type == pygame.QUIT:
            running = False
            
    ### Enable player movement: set player controls
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and playerX > 0:
        playerX -= playerSpeed
    if keys[pygame.K_RIGHT] and playerX < WIDTH - playerWidth:
        playerX += playerSpeed
        
    ### Update the falling object's postions
    objectY += objectSpeed
    
    ### Check if there is a collision
    if (playerX < objectX + objectWidth and 
        playerX + playerWidth > objectX and 
        playerY < objectY + objectHeight and 
        playerY + playerHeight > objectY):
        score += 1
        objectX = random.randint(0, WIDTH - objectWidth)
        objectY = 0 
        
    ### Reset object whenever it falls off the screen
    if objectY > HEIGHT:
        objectX = random.randint(0, WIDTH - objectWidth)
        objectY = 0 
        
    ### Clear the screen
    screen.fill(WHITE) 
        
    ### Draw the Player
    pygame.draw.rect(screen, BLACK, (playerX, playerY, playerWidth, playerHeight))
        
    ### Draw the falling Object
    pygame.draw.rect(screen, RED, (objectX, objectY, objectWidth, objectHeight))
        
    ### Display the score
    scoreText = font.render(f'Score: {score}',True,BLACK)
    screen.blit(scoreText,(10,10))
        
    ### Update the screen
    pygame.display.flip()
        
    ### Control frame rate
    clock.tick(30)
        
## Quit the game
pygame.quit()
        