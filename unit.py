import pygame
from color import Color


WIDTH, HEIGHT = 1800, 1000
BLOCK_SIZE = 10
FPS = 60
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

class Unit:
    def __init__(self, side):
        self.x = WIDTH/2
        self.y = HEIGHT/2
        self.health = 100
        self.attack = 10
        self.speed = BLOCK_SIZE
        self.side = side #ENUM?
        self.color = Color.BLUE.value

        if self.side == 'r':
            self.x -= 200
            self.speed *= -1
            self.color = Color.RED.value
        else:
            self.x += 200


        self.body = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)

    def draw(self, window):
        pygame.draw.rect(window, self.color, self.body)

    def update(self):
        self.x -= self.speed
        self.body = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
    
