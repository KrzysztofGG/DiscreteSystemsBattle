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
# pygame.time.set_timer(MOVEMENT_EVENT, 200)
pygame.time.set_timer(MOVEMENT_EVENT, 100)

def init_simulation(grid):
    paused = False
    ended = False
    u_dict = {Side.RED: [], Side.BLUE: []}
    grid.units_dict = u_dict

    unit_r = Infantry(Color.RED,350,550, Side.RED)
    unit_r2 = Heavy(Color.RED,650,500, Side.RED, 1)
    unit_r3 = Heavy(Color.RED,750,500, Side.RED)
    unit_b = Heavy(Color.WHITE,600,570, Side.BLUE)
    unit_c = Infantry(Color.BLUE,380,400, Side.BLUE)
    unit_b1 = Heavy(Color.BLUE,410,500, Side.BLUE)
    unit_b2 = Infantry(Color.BLUE,400,510, Side.BLUE)
    unit_c1 = Cavalry(Color.RED,600,500, Side.RED)

    grid.units_dict[Side.RED].append(unit_r)
    grid.units_dict[Side.RED].append(unit_r2)
    # grid.units_dict[Side.RED].append(unit_r3)
    # grid.units_dict[Side.BLUE].append(unit_b)
    grid.units_dict[Side.BLUE].append(unit_c)
    grid.units_dict[Side.BLUE].append(unit_b1)
    grid.units_dict[Side.BLUE].append(unit_b2)
    grid.units_dict[Side.RED].append(unit_c1)
    return paused, ended

def main():
    pygame.display.set_caption("Battle Simulator")
    CLOCK = pygame.time.Clock()

    # grid = Grid()
    # grid.fill_arena_with_hills(3, 40, 60)
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

    addFormation(grid,300,800,10,50,Side.BLUE,"infantry")
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

    addFormation(grid,300,200,5,50,Side.BLUE,"infantry")  
    addFormation(grid,400,620,15,50,Side.BLUE,"cavalry") 
    addFormation(grid,500,600,15,50,Side.BLUE,"heavy")  
    addFormation(grid,300,600,20,50,Side.BLUE,"infantry")  
    addFormation(grid,400,700,30,20,Side.BLUE,"cavalry") 
    addFormation(grid,300,400,15,50,Side.BLUE,"infantry")  
    addFormation(grid,400,420,20,70,Side.BLUE,"cavalry") 
    addFormation(grid,500,200,40,60,Side.BLUE,"heavy")  
    addFormation(grid,300,300,30,70,Side.BLUE,"infantry")  
    addFormation(grid,400,300,80,35,Side.BLUE,"cavalry") 
    addFormation(grid,200,400,20,60,Side.BLUE,"infantry") 
    addFormation(grid,200,100,10,60,Side.BLUE,"infantry")
    # grid.create_river((10, 45), (100, 45), 10, True)
    # grid.create_river((50, 50), (50, 10), 10, True)
    # grid.create_polygon_river([(10, 10), (20, 10), (30, 20), (20, 20)])
    # paused, ended = init_simulation(grid)
    paused, ended = False, False

    while True:
        CLOCK.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == GAME_ENDS_EVENT:
                ended = True
            elif event.type == KEYDOWN and event.key == K_SPACE and ended:
                paused, ended = init_simulation(grid)

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
        else:
            grid.draw_end_screen()

        pygame.display.update()

def update_units(grid):
    if random.randint(0, 1) == 0:
        iterate_green(grid)
        iterate_red(grid)
    else:
        iterate_red(grid)
        iterate_green(grid)

def iterate_green(grid):
    if len(grid.units_dict[Side.BLUE]) > 0:
        for u in grid.units_dict[Side.BLUE]:
            u.update(grid.arena, grid.units_dict)

def iterate_red(grid):
    if len(grid.units_dict[Side.RED]) > 0:
        for u in grid.units_dict[Side.RED]:
            u.update(grid.arena, grid.units_dict)
if __name__ == "__main__":
    main()




