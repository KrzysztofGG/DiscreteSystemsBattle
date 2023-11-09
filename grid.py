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
        self.height = 0.2
        self.color = (0, min(255, int(255*self.height)), 0)
        self.unit = None
        self.body = pygame.Rect(self.x, self.y, self.border, self.border)
    
    def draw(self, window):
        pygame.draw.rect(window, self.color, self.body)
    
    def updateColor(self):
        green_value = min(255, int(255*self.height)*0.9)
        self.color = (0, green_value, 0)

    # def update():

def create_hill_on_arena(centerX, centerY, radius, arena, max_height):
    diameter = (radius * 2) + 1
    radiusSq = (radius * radius) / 4

    # centerX = arena_start_x 
    # centerY = arena_start_y 

    for y in range(centerY - radius, centerY + radius):
        yDiff = y - centerY
        threshold = radiusSq - (yDiff * yDiff)
        for x in range(centerX - radius, centerX + radius):

            if (y + centerY > 0 and y + centerY < arena.shape[0] and
                x + centerX > 0 and x + centerX < arena.shape[1]):
              
              xDiff = x - centerX
              if xDiff * xDiff <= threshold:
                  dist = sqrt(pow(yDiff, 2) + pow(xDiff, 2))
                  height_increase = max_height - dist/radius + random.uniform(0, 0.03)
                  arena[y + centerY, x + centerX].height += height_increase
                  if arena[y + centerY, x + centerX].height > 1:
                      arena[y + centerY, x + centerX].height = 1

                  arena[y + centerY, x + centerX].updateColor()

def fill_arena_with_hills(n_hills, min_radius, max_radius, arena):

    while(n_hills):
        r = min(arena.shape[0], arena.shape[1])

        x = random.randint(min_radius/2, arena.shape[0] - min_radius/2)
        y = random.randint(min_radius/2, arena.shape[1] - min_radius/2)

        if x > arena.shape[0] or y > arena.shape[1]:
            continue
        else:
            radius = random.randint(min_radius, max_radius)
            max_height = random.uniform(0.5, 1)
            create_hill_on_arena(x, y, radius, arena, max_height)
            n_hills -= 1


unit_locations = {Side.RED: [], Side.GREEN: []}

arena = np.zeros((WIDTH//BLOCK_SIZE, HEIGHT//BLOCK_SIZE), dtype=object)
for x in range(0, arena.shape[0]):
    for y in range(0, arena.shape[1]):
        arena[x, y] = GroundElement(x*BLOCK_SIZE, y*BLOCK_SIZE)

fill_arena_with_hills(3, 60, 80, arena)
# for x in range(0, arena.shape[0]):
#     for y in range(0, arena.shape[1]):
#         if arena[x, y].height > 0:
            # print("XD")

def drawPause():
    FONT = pygame.font.SysFont('arial', 200)
    pause_text = FONT.render("PAUSED", 1, Color.WHITE.value)
    WIN.blit(pause_text, (WIDTH/2 - pause_text.get_width()/2,    
                          HEIGHT/2 - pause_text.get_height()/2))
    pygame.display.update()
    
def drawGrid():
    for x in range(0, arena.shape[0]):
        for y in range(0, arena.shape[1]):
            arena[x, y].draw(WIN)
            
    for x in range(0, WIDTH, BLOCK_SIZE):
        for y in range(0, HEIGHT, BLOCK_SIZE):
            rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(WIN, Color.GRAY.value, rect, 1)