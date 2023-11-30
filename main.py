# import pygame
from pygame.locals import *
import sys
import random
from unit import *
from utils import *
from grid import Grid
from color import Color

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

    grid = Grid()
    grid.create_circle_hill_on_arena(20,10,500,0.22)
    grid.create_circle_hill_on_arena(0,50,200,0.3)
    grid.create_circle_hill_on_arena(0,70,80,0.4)
    grid.drawRiver(90,100,0,180)
    grid.drawRiver(89,100,80,180)
    grid.drawRiver(88,100,100,180)
    grid.drawRiver(87,100,120,180)
    paused = False
    ended = False

    addFormation(grid,300,800,10,50,Side.GREEN,"infantry")
    addFormation(grid,1300,800,15,50,Side.RED,"infantry")  
    addFormation(grid,1400,820,15,50,Side.RED,"cavalry") 
    addFormation(grid,1500,600,15,50,Side.RED,"heavy")  
    addFormation(grid,1300,600,20,50,Side.RED,"infantry")  
    addFormation(grid,1400,700,10,20,Side.RED,"cavalry") 
    addFormation(grid,1300,500,15,50,Side.RED,"infantry")  
    addFormation(grid,1400,420,15,50,Side.RED,"cavalry") 
    addFormation(grid,1500,400,10,50,Side.RED,"heavy")  
    addFormation(grid,1300,500,30,70,Side.RED,"infantry")  
    addFormation(grid,1400,300,15,35,Side.RED,"cavalry") 
    addFormation(grid,1200,400,18,60,Side.RED,"infantry") 
    addFormation(grid,1200,100,12,60,Side.RED,"infantry") 

    addFormation(grid,1500,400,10,50,Side.RED,"heavy")  
    addFormation(grid,1200,550,10,70,Side.RED,"infantry")  
    addFormation(grid,1400,350,15,35,Side.RED,"cavalry") 
    addFormation(grid,1200,450,18,60,Side.RED,"infantry") 
    addFormation(grid,1200,150,12,60,Side.RED,"heavy") 

    addFormation(grid,300,200,5,50,Side.GREEN,"infantry")  
    addFormation(grid,400,620,15,50,Side.GREEN,"cavalry") 
    addFormation(grid,500,600,15,50,Side.GREEN,"heavy")  
    addFormation(grid,300,600,20,50,Side.GREEN,"infantry")  
    addFormation(grid,400,700,30,20,Side.GREEN,"cavalry") 
    addFormation(grid,300,400,15,50,Side.GREEN,"infantry")  
    addFormation(grid,400,420,20,70,Side.GREEN,"cavalry") 
    addFormation(grid,500,200,40,60,Side.GREEN,"heavy")  
    addFormation(grid,300,300,30,70,Side.GREEN,"infantry")  
    addFormation(grid,400,300,80,35,Side.GREEN,"cavalry") 
    addFormation(grid,200,400,20,60,Side.GREEN,"infantry") 
    addFormation(grid,200,100,10,60,Side.GREEN,"infantry") 
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




