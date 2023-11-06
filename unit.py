import pygame
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
BLUE = (0, 0, 255)
LIGHTGREEN = pygame.Color('#90EE90')


WIDTH, HEIGHT = 1800, 1000
BLOCK_SIZE = 10
FPS = 60
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

class Unit:


    def __init__(self):
        self.x = WIDTH/2
        self.y = HEIGHT/2
        self.health = 100
        self.attack = 10
        self.speed = BLOCK_SIZE
        self.body = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
        self.side = "red" #ENUM?

    def draw(self, window):
        pygame.draw.rect(window, BLUE, self.body)

    def update(self):
        self.x -= self.speed
        self.body = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
    
