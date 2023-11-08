import pygame
import numpy as np
from color import Color
from utils import *
from unit import Side

class GroundElement:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.border = BLOCK_SIZE
        self.color = Color.GREEN.value
        # self.units = dict()
        # temporal boolean
        self.unit = None
        self.body = pygame.Rect(self.x, self.y, self.border, self.border)
    
    def draw(self, window):
        pygame.draw.rect(window, self.color, self.body)

    # def update():

unit_locations = {Side.RED: [], Side.GREEN: []}
arena = np.zeros((WIDTH//BLOCK_SIZE, HEIGHT//BLOCK_SIZE), dtype=object)

for x in range(0, arena.shape[0]):
    for y in range(0, arena.shape[1]):
        arena[x, y] = GroundElement(x*BLOCK_SIZE, y*BLOCK_SIZE)


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