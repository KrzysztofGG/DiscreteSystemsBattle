# import pygame
from pygame.locals import *
import sys
import random
from unit import *
from utils import *
from grid import GroundElement
import grid
from color import Color
# import numpy as np

pygame.init()

FONT = pygame.font.SysFont('arial', 200)

MOVEMENT_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(MOVEMENT_EVENT, 200)

def main():
    pygame.display.set_caption("Battle Simulator")
    CLOCK = pygame.time.Clock()
    WIN.fill(Color.LIGHTGREEN.value)

    paused = False

    unit_r = Infantry(Color.RED,350,550, Side.RED)
    unit_r2 = Heavy(Color.RED,650,500, Side.RED)
    unit_b = Infantry(Color.BLUE,600,570, Side.GREEN, 1)
    unit_c = Infantry(Color.BLUE,380,400, Side.GREEN)
    # unit_b = Heavy(Color.BLUE,410,500, Side.GREEN)
    # unit_c = Cavalry(Color.BLACK,600,500, Side.GREEN)
    units = [unit_r, unit_b, unit_c, unit_r2]
    # grid.unit_locations[Side.RED].append((unit_r.x//BLOCK_SIZE, unit_r.y//BLOCK_SIZE))
    # grid.unit_locations[Side.GREEN].append((unit_b.x//BLOCK_SIZE, unit_b.y//BLOCK_SIZE))
    # grid.unit_locations[Side.GREEN].append((unit_c.x//BLOCK_SIZE, unit_c.y//BLOCK_SIZE))
    grid.unit_locations[Side.RED].append((unit_r.x, unit_r.y))
    grid.unit_locations[Side.RED].append((unit_r2.x, unit_r2.y))
    grid.unit_locations[Side.GREEN].append((unit_b.x, unit_b.y))
    grid.unit_locations[Side.GREEN].append((unit_c.x, unit_c.y))


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




