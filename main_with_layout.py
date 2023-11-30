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




def main():
    pygame.display.set_caption("Battle Simulator")
    CLOCK = pygame.time.Clock()

    grid = Grid()
    units_list = list(choose_units_layout())

    grid.fill_arena_with_hills(3, 40, 60)
    for u in units_list:
        grid.units_dict[u.side].append(u)

    pygame.time.set_timer(MOVEMENT_EVENT, 200)


    paused = False
    ended = False


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
                    print(len(grid.units_dict[Side.RED]) + len(grid.units_dict[Side.GREEN]))

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




