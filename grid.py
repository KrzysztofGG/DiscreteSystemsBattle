import pygame
import numpy as np
from color import Color
from utils import *
from unit import Side
from math import sqrt, pow
import random
class GroundElement:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.border = BLOCK_SIZE
        # self.height = 0.2
        self.height = 0
        # self.color = (0, min(255, int(255*(self.height + 0.1))), 0)
        self.color = (0, 255, 0)
        self.unit = None
        self.body = pygame.Rect(self.x, self.y, self.border, self.border)
    
    def draw(self, window):
        pygame.draw.rect(window, self.color, self.body)
    
    def updateColor(self):
        pct_diff = 1.0 - self.height
        red_color = min(255, self.height * 2 * 255)
        green_color = min(255, pct_diff * 2 * 255)
        col = (red_color, green_color, 0)
        self.color = col
        # green_value = min(255, int(255*(self.height + 0.1)))
        # self.color = (0, green_value, 0)

    # def update():

def create_circle_hill_on_arena(centerX, centerY, radius, arena, max_height):
    diameter = (radius * 2) + 1
    radiusSq = (radius * radius) / 4

    for y in range(centerY - radius, centerY + radius):
        yDiff = y - centerY
        # threshold = radiusSq - (yDiff * yDiff)
        threshold = radius*radius - (yDiff * yDiff)
        for x in range(centerX - radius, centerX + radius):

            if( y >= 0 and y < arena.shape[0]  and
                x >= 0 and x < arena.shape[1] ):
              
              xDiff = x - centerX
              if xDiff * xDiff <= threshold:
                  dist = sqrt(pow(yDiff, 2) + pow(xDiff, 2))
                  height_increase = max_height - max_height*(dist/radius)

                  arena[y, x].height += height_increase
                  if arena[y, x].height > 1:
                      arena[y, x].height = 1

                  arena[y, x].updateColor()

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


def fill_arena_with_hills(n_hills, min_radius, max_radius, arena):

    current_hill = n_hills
    while(current_hill):
        # r = min(arena.shape[0], arena.shape[1])

        first_range = (n_hills - current_hill)/n_hills
        second_range = (n_hills - current_hill + 1)/n_hills

        x = random.randint(int(arena.shape[1] * first_range), int(arena.shape[1] * second_range))
        y = random.randint(int(min_radius/2), int(arena.shape[0] - min_radius/2))

        if x > arena.shape[1] or y > arena.shape[0]:
            continue
        else:
            radius = random.randint(min_radius, max_radius)
            max_height = random.uniform(0.6, 0.8)
            create_circle_hill_on_arena(x, y, radius, arena, max_height)
            current_hill -= 1
    

#deprecated will be using units_dict
# unit_locations = {Side.RED: [], Side.GREEN: []}
units_dict = {Side.RED: [], Side.GREEN: []}

arena = np.zeros((HEIGHT//BLOCK_SIZE, WIDTH//BLOCK_SIZE), dtype=object)
for y in range(0, arena.shape[0]):
    for x in range(0, arena.shape[1]):
        arena[y, x] = GroundElement(x*BLOCK_SIZE, y*BLOCK_SIZE)


fill_arena_with_hills(3, 40, 60, arena)

def drawPause():
    FONT = pygame.font.SysFont('arial', 200)
    pause_text = FONT.render("PAUSED", 1, Color.WHITE.value)
    WIN.blit(pause_text, (WIDTH/2 - pause_text.get_width()/2,    
                          HEIGHT/2 - pause_text.get_height()/2))

def draw_end_screen():
    FONT = pygame.font.SysFont('arial', 200)
    if len(units_dict[Side.GREEN]) > 0:
        winner = "GREEN"
    else:
        winner = "RED"
    text = f'{winner} UNITS WIN'
    text_render = FONT.render(text, 1, Color.WHITE.value)
    WIN.blit(text_render, (WIDTH/2 - text_render.get_width()/2,
                           HEIGHT/2 - text_render.get_height()/2))
    pygame.time.delay(1000)

def draw_all_units_details():
    for s in units_dict.keys():
        for u in units_dict[s]:
            if pygame.Rect(u.x-u.size/2, u.y-u.size/2, u.size*2, u.size*2).collidepoint(pygame.mouse.get_pos()):
                u.show_unit_details(arena)
    
def drawGrid():

    # for x in range(0, arena.shape[0]):
    #     for y in range(0, arena.shape[1]):
    #         arena[y, x].draw(WIN)
    for row in arena:
        for val in row:
            val.draw(WIN)
            
    for y in range(0, HEIGHT, BLOCK_SIZE):
        for x in range(0, WIDTH, BLOCK_SIZE):
            rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(WIN, Color.GRAY.value, rect, 1)