# import pygame
from pygame.locals import *
import sys
import random
from unit import *
from utils import *
from grid import GroundElement
import grid
from color import Color
# import os
# import numpy as np

pygame.init()

pygame.mixer.music.load(os.path.join('Assets', 'background-music.mp3'))
pygame.mixer.music.set_volume(0.2)
# pygame.mixer.music.play()

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
    unit_b = Heavy(Color.BLUE,600,570, Side.GREEN)
    unit_c = Infantry(Color.BLUE,380,400, Side.GREEN)
    unit_b1 = Heavy(Color.BLUE,410,500, Side.GREEN)
    unit_c1 = Cavalry(Color.RED,600,500, Side.RED)

    grid.units_dict[Side.RED].append(unit_r)
    grid.units_dict[Side.RED].append(unit_r2)
    grid.units_dict[Side.GREEN].append(unit_b)
    grid.units_dict[Side.GREEN].append(unit_c)
    grid.units_dict[Side.GREEN].append(unit_b1)
    grid.units_dict[Side.RED].append(unit_c1)
    
    while True:
        CLOCK.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == GAME_ENDS_EVENT:
                grid.draw_end_screen()
                break
            elif event.type == KEYDOWN and event.key == K_SPACE:
                paused = not paused
            elif event.type == MOVEMENT_EVENT:
                if not paused:
                    if random.randint(0, 1) == 0:
                        for u in grid.units_dict[Side.GREEN]:
                            u.update(grid.arena, grid.units_dict)
                        for u in grid.units_dict[Side.RED]:
                            u.update(grid.arena, grid.units_dict)
                    else:
                        for u in grid.units_dict[Side.RED]:
                            u.update(grid.arena, grid.units_dict)
                        for u in grid.units_dict[Side.GREEN]:
                            u.update(grid.arena, grid.units_dict)
                    
        grid.drawGrid()
        for s in grid.units_dict.keys():
            for u in grid.units_dict[s]:
                u.draw(WIN)
        grid.draw_all_units_details()

        if paused:
            grid.drawPause()

        pygame.display.update()
            
if __name__ == "__main__":
    main()




