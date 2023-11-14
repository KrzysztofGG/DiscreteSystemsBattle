# import pygame
from pygame.locals import *
import sys
import random
from unit import *
from utils import *
from grid import Grid
from color import Color
from layout import choose_units_layout

pygame.init()

pygame.mixer.music.load(os.path.join('Assets', 'background-music.mp3'))
pygame.mixer.music.set_volume(0.2)
# pygame.mixer.music.play()

FONT = pygame.font.SysFont('arial', 200)

MOVEMENT_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(MOVEMENT_EVENT, 200)



def main():


    units_list = list(choose_units_layout())
    units_dict = {Side.RED: [], Side.GREEN: []}
    for u in units_list:
        units_dict[u.side].append(u)

    grid = Grid(units_dict)
    grid.fill_arena_with_hills(3, 40, 60)

    pygame.display.set_caption("Battle Simulator")
    CLOCK = pygame.time.Clock()

    paused = False
    ended = False

    # unit_r = Infantry(Color.RED,350,550, Side.RED)
    # unit_r2 = Heavy(Color.RED,650,500, Side.RED)
    # unit_b = Heavy(Color.BLUE,600,570, Side.GREEN)
    # unit_c = Infantry(Color.BLUE,380,400, Side.GREEN)
    # unit_b1 = Heavy(Color.BLUE,410,500, Side.GREEN)
    # unit_c1 = Cavalry(Color.RED,600,500, Side.RED)

    # grid.units_dict[Side.RED].append(unit_r)
    # grid.units_dict[Side.RED].append(unit_r2)
    # grid.units_dict[Side.GREEN].append(unit_b)
    # grid.units_dict[Side.GREEN].append(unit_c)
    # grid.units_dict[Side.GREEN].append(unit_b1)
    # grid.units_dict[Side.RED].append(unit_c1)
    
    while True:
        CLOCK.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == GAME_ENDS_EVENT:
                grid.draw_end_screen()
                ended = True
                # break
            elif event.type == KEYDOWN and event.key == K_SPACE:
                paused = not paused
            elif event.type == MOVEMENT_EVENT:
                if not paused:
                    update_units(grid)

        if not ended:      
            grid.drawGrid()
            for s in grid.units_dict.keys():
                for u in grid.units_dict[s]:
                    u.draw(WIN)

            if paused:
                grid.drawPause()
                
            grid.draw_all_units_details()


        pygame.display.update()

def update_units(grid):
    if random.randint(0, 1) == 0:
        iterate_green(grid)
        iterate_red(grid)
    else:
        iterate_red(grid)
        iterate_green(grid)

def iterate_green(grid):
    if len(grid.units_dict[Side.GREEN]) > 0:
        for u in grid.units_dict[Side.GREEN]:
            u.update(grid.arena, grid.units_dict)

def iterate_red(grid):
    if len(grid.units_dict[Side.RED]) > 0:
        for u in grid.units_dict[Side.RED]:
            u.update(grid.arena, grid.units_dict)

if __name__ == "__main__":
    main()




