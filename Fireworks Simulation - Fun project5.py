# Fireworks Simulation - Fun project5

## Import all the necessaru liabraries
import pygame,sys,random

## Initailize pygame variable
pygame.init()

## Set Screen dimensions
width,height = 800,600
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption('Fireworks Simulation')

## Set background color
black = (0,0,0)

## Define a class for firework particles
class firework_particles:
    ### Define the init function for firework particle class
    def __init__(self,x,y,color):
        self.x = x
        self.y = y
        self.color = color
        self.radius = random.randint(2,4)
        self.lifetime = random.randint(40,80)
        self.dx = random.uniform(-3,3)
        self.dy = random.uniform(-5,1)
        
    ### Define a function to control movement
    def move(self):
        self.x += self.dx
        self.y += self.dy
        self.y += 0.05
        self.lifetime -=1
    
    ### Define a function to draw 
    def draw(self,surface):
        if self.lifetime > 0:
          pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)
## Define a function to launch the fireworks
def launch_fireworks():
    particles = []
    for _ in range(random.randint(20,50)):
        x = random.randint(100, width - 100)   
        y = random.randint(100,height // 2)
        color = [random.randint(50,255) for _ in range(3)]
        for _ in range(100):
            particles.append(firework_particles(x,y,color))
    return particles
    
##  Create the main loop
clock = pygame.time.Clock() 
particles = []

while True:
    screen.fill(black)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
    ### Launch new fireworks periodically
    if random.randint(1,20) == 1:
        particles.extend(launch_fireworks())
        
    ### Update and draw particles
    for particle in particles[:]:
        particle.move()
        particle.draw(screen)
        if particle.lifetime <= 0:
            particles.remove(particle)
    ## Display Fireworks
    pygame.display.flip()
    clock.tick(30)