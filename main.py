import pygame
from pygame.locals import *
import sys
import random
from unit import *

from grid import GroundElement
import grid
from color import Color
# import numpy as np

pygame.init()



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
    WIN.fill(Color.LIGHTGREEN.value)

    paused = False

    unit_r = Infantry(Color.RED,400,550, Side.RED)
    unit_b = Infantry(Color.BLUE,450,570, Side.GREEN)
    # unit_b = Heavy(Color.BLUE,410,500, Side.GREEN)
    # unit_c = Cavalry(Color.BLACK,600,500, Side.GREEN)
    units = [unit_r, unit_b]
    grid.unit_locations["red"].append((unit_r.x//BLOCK_SIZE, unit_r.y//BLOCK_SIZE))
    grid.unit_locations["green"].append((unit_b.x//BLOCK_SIZE, unit_b.y//BLOCK_SIZE))


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
                    # map(lambda u: u.update(), units)
                    for u in units:
                        u.update(grid.arena, grid.unit_locations)
                    
                
                    
        if paused:
            grid.drawPause()
        else:
            grid.drawGrid()
            # map(lambda u: u.draw(WIN), units)
            for u in units:
                u.draw(WIN)

            pygame.display.update()
            
if __name__ == "__main__":
    main()




