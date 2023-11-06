import pygame
import sys
import random

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
LIGHTGREEN = pygame.Color('#90EE90')

WIDTH, HEIGHT = 1350, 750
FPS = 60
WIN = pygame.display.set_mode((WIDTH, HEIGHT))



class Actor:
    def __init__(self, screen, strength, type):
        self.screen=screen
        self.strength=strength
        self.type=type
    def draw( self, x , y , size):
        rect = pygame.Rect( x, y, size,size)
        if self.type ==1:
            color= (255,0,0)
        else:
            color= (0,255,0)
        pygame.draw.rect(WIN, color, rect)
    def find_enemy():
        return 0

def main():
    pygame.init()
    pygame.display.set_caption("Battle Simulator")
    CLOCK = pygame.time.Clock()
    WIN.fill(LIGHTGREEN)
    actor1=Actor(WIN,8,1)
    actor2=Actor(WIN,8,2)
    actor1.draw(100,200,50)
    actor2.draw(600,200,50)
    while True:
        drawGrid()
        CLOCK.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()


def drawGrid():
    blockSize = 10
    for x in range(0, WIDTH, blockSize):
        for y in range(0, HEIGHT, blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            pygame.draw.rect(WIN, GRAY, rect, 1)

if __name__ == "__main__":
    main()





