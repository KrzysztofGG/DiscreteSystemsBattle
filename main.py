import pygame
from pygame.locals import *
import sys



pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
BLUE = (0, 0, 255)
LIGHTGREEN = pygame.Color('#90EE90')


WIDTH, HEIGHT = 1800, 1000
BLOCK_SIZE = 10
FPS = 60
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

FONT = pygame.font.SysFont('arial', 200)

MOVEMENT_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(MOVEMENT_EVENT, 200)


class Unit:

    def __init__(self):
        self.x = WIDTH/2
        self.y = HEIGHT/2
        self.health = 100
        self.attack = 10
        self.speed = BLOCK_SIZE
        self.body = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
        self.side = "red" #ENUM?

    def draw(self, window):
        pygame.draw.rect(window, BLUE, self.body)

    def update(self):
        self.x -= self.speed
        self.body = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
    



def main():
    
    pygame.display.set_caption("Battle Simulator")
    CLOCK = pygame.time.Clock()
    WIN.fill(LIGHTGREEN)

    paused = False

    unit = Unit()

    while True:
        CLOCK.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_SPACE:
                paused = not paused
            elif event.type == MOVEMENT_EVENT:
                if not paused:
                    unit.update()
                
                    
        if paused:
            drawPause()
        else:
            drawGrid()
            unit.draw(WIN)
            pygame.display.update()
            

def drawPause():
    pause_text = FONT.render("PAUSED", 1, WHITE)
    WIN.blit(pause_text, (WIDTH/2 - pause_text.get_width()/2,    
                          HEIGHT/2 - pause_text.get_height()/2))
    
    pygame.display.update()
    
def drawGrid():

    for x in range(0, WIDTH, BLOCK_SIZE):
        for y in range(0, HEIGHT, BLOCK_SIZE):
            rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(WIN, GRAY, rect, 1)

if __name__ == "__main__":
    main()