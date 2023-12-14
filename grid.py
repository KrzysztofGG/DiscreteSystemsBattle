import numpy as np
from color import Color
from utils import *
from unit import Side
from math import sqrt, pow
import random
import os

pygame.mixer.init()
WIN_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'polska-gurom-3.mp3'))
WIN_SOUND.set_volume(5)

class GroundElement:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.border = BLOCK_SIZE
        self.height = 0
        self.color = (0, 255, 0)
        # self.unit = None
        self.river = False
        self.body = pygame.Rect(self.x, self.y, self.border, self.border)
    
    def draw(self, window):
        pygame.draw.rect(window, self.color, self.body)
    
    def updateColor(self):
        pct_diff = 1.0 - self.height
        red_color = min(255, self.height * 2 * 255)
        green_color = min(255, pct_diff * 2 * 255)
        col = (red_color, green_color, 0)
        self.color = col

    def setColor(self, color):
        self.color = color

class Grid():

    def __init__(self, units_dict = {Side.RED: [], Side.BLUE: []}):
        self.end_played = False
        self.units_dict = units_dict
        self.arena = np.zeros((HEIGHT//BLOCK_SIZE, WIDTH//BLOCK_SIZE), dtype=object)
        for y in range(0, self.arena.shape[0]):
            for x in range(0, self.arena.shape[1]):
                self.arena[y, x] = GroundElement(x*BLOCK_SIZE, y*BLOCK_SIZE)

    def drawRiver(self,x1,x2,y1,y2):
        for x  in range(x1,x2):
            for y in range(y1,y2):
                self.arena[x,y].color=(0, 0, 255)

    def create_circle_hill_on_arena(self, centerX, centerY, radius, max_height):

        for y in range(centerY - radius, centerY + radius):
            yDiff = y - centerY
            threshold = radius*radius - (yDiff * yDiff)
            for x in range(centerX - radius, centerX + radius):

                if( y >= 0 and y < self.arena.shape[0]  and
                    x >= 0 and x < self.arena.shape[1] ):
                
                    xDiff = x - centerX
                    if xDiff * xDiff <= threshold:
                        dist = sqrt(pow(yDiff, 2) + pow(xDiff, 2))
                        height_increase = max_height - max_height*(dist/radius)

                        self.arena[y, x].height += height_increase
                        if self.arena[y, x].height > 1:
                            self.arena[y, x].height = 1

                        self.arena[y, x].updateColor()

    def create_river(self, start, end, width, is_vertical):

        if is_vertical:
            range_y = end[0] - start[0]
            range_x = width
        else:
            range_y = width
            range_x = end[1] - start[1]

        for y in range(range_y):
            for x in range(range_x):

                # if( y >= 0 + start[0] and y + start[0] < self.arena.shape[0]  and
                #     x + start[1]>= 0 and x + start[1]< self.arena.shape[1] ):
                    
                    if is_vertical:
                        dist = abs(x - width/2)/width  
                    else:
                        dist = abs(y - width/2)/width 

                    diff = 1 - dist - 0.2
                    r = 0
                    g = min(255, 255 * 2 * dist)
                    b = min(255, 255 * 2 * diff)
 
                    color = (r, g, b)
                    self.arena[y + start[0], x + start[1]].setColor(color)
                    self.arena[y + start[0], x + start[1]].river = True

    def create_polygon_river(self, points):
        pygame.draw.polygon(WIN, Color.BLUE.value, points)

    def fill_arena_with_hills(self, n_hills, min_radius, max_radius):

        current_hill = n_hills
        while(current_hill):
            # r = min(arena.shape[0], arena.shape[1])

            first_range = (n_hills - current_hill)/n_hills
            second_range = (n_hills - current_hill + 1)/n_hills

            x = random.randint(int(self.arena.shape[1] * first_range), int(self.arena.shape[1] * second_range))
            y = random.randint(int(min_radius/2), int(self.arena.shape[0] - min_radius/2))

            if x > self.arena.shape[1] or y > self.arena.shape[0]:
                continue
            else:
                radius = random.randint(min_radius, max_radius)
                max_height = random.uniform(0.6, 0.8)
                self.create_circle_hill_on_arena(x, y, radius, max_height)
                current_hill -= 1
    
    def drawPause(self):
        FONT = pygame.font.SysFont('arial', 200)
        pause_text = FONT.render("PAUSED", 1, Color.WHITE.value)
        WIN.blit(pause_text, (WIDTH/2 - pause_text.get_width()/2,    
                            HEIGHT/2 - pause_text.get_height()/2))

    def draw_end_screen(self):
        FONT = pygame.font.SysFont('arial', 200)
        if len(self.units_dict[Side.BLUE]) > 0:
            winner = "BLUE"
        else:
            winner = "RED"
        text = f'{winner} UNITS WIN'
        text_render = FONT.render(text, 1, Color.WHITE.value)
        WIN.blit(text_render, (WIDTH/2 - text_render.get_width()/2,
                            HEIGHT/2 - text_render.get_height()/2))
        
        FONT_SMALL = pygame.font.SysFont('arial', 50)
        text_small = "Press space to restart"
        text_small_render = FONT_SMALL.render(text_small, 1, Color.WHITE.value)
        WIN.blit(text_small_render, (WIDTH/2 - text_small_render.get_width()/2,
                                HEIGHT/2 - text_small_render.get_height()/2 + text_render.get_height()/2))
        
        if "BLUE" in text and not self.end_played:
            WIN_SOUND.play()
            self.end_played = True

    def draw_all_units_details(self):
        for s in self.units_dict.keys():
            for u in self.units_dict[s]:
                if pygame.Rect(u.x-u.size/2, u.y-u.size/2, u.size*2, u.size*2).collidepoint(pygame.mouse.get_pos()):
                    u.show_unit_details(self.arena)
        
    def drawGrid(self):
        for y in range(0, self.arena.shape[0]):
            for x in range(0, self.arena.shape[1]):
                self.arena[y, x].draw(WIN)
                
        for y in range(0, HEIGHT, BLOCK_SIZE):
            for x in range(0, WIDTH, BLOCK_SIZE):
                rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
                pygame.draw.rect(WIN, Color.GRAY.value, rect, 1)
    


def create_elipse_hill_on_arena(centerX, centerY, radiusX, radiusY, arena, max_height):
    for y in range(centerY - radiusY, centerY + radiusY):
        for x in range(centerX - radiusX, centerX + radiusX):
            if( y >= 0 and y < arena.shape[0] and
                x >= 0 and x < arena.shape[1]):
                eq1 = pow(x/radiusX, 2)
                eq2  = pow(y/radiusY, 2)
                if eq1 + eq2 - 1 < 0:
                    
                    #need to find a smart way of distributing color evenly
                    # dist = sqrt(pow(yDiff, 2) + pow(xDiff, 2))
                    # height_increase = max_height - dist/radius + random.uniform(0, 0.03)
                    pass
                    arena[y, x].height += height_increase
                    if arena[y, x].height > 1:
                        arena[y, x].height = 1

                    arena[y, x].updateColor()







