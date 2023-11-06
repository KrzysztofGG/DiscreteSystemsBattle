import pygame
from pygame.locals import *
import sys
import random
from unit import Unit
import grid



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
            grid.drawPause()
        else:
            grid.drawGrid()
            unit.draw(WIN)
            pygame.display.update()
            
if __name__ == "__main__":
    main()





