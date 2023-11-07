import pygame
from enum import Enum
from math import sin, cos, pi, radians

import numpy as np
from collections import deque

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
BLUE = (0, 0, 255)
LIGHTGREEN = pygame.Color('#90EE90')

BLOCK_SIZE = 10
WIDTH, HEIGHT = 1800, 1000
FPS = 60
WIN = pygame.display.set_mode((WIDTH, HEIGHT))


class Side(Enum):
    RED=1
    GREEN=2

def distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


class Unit:
    def __init__(self, color, x, y, side):
        self.x = x
        self.y = y
        self.color = color
        self.side = side
        self.speedX = BLOCK_SIZE//5
        self.speedY = BLOCK_SIZE//5

    def update(self,arena, unit_locations):

        if self.side == Side.RED:
            side = "red"
        else:
            side = "green"
        

        arena[self.x//BLOCK_SIZE, self.y//BLOCK_SIZE].unit = None
        if arena[self.x//BLOCK_SIZE - 1, self.y//BLOCK_SIZE].unit != None or arena[self.x//BLOCK_SIZE + 1, self.y//BLOCK_SIZE].unit != None:
            self.speed = 0


        # finding nearest enemy
        if self.side == Side.GREEN:
            # enemy_x, enemy_y = find(arena, (self.x//BLOCK_SIZE, self.y//BLOCK_SIZE), Side.RED)
            enemy_x, enemy_y = min(unit_locations["red"], key = lambda coords: distance(coords, (self.x, self.y)))
        else:
            enemy_x, enemy_y = min(unit_locations["green"], key = lambda coords: distance(coords, (self.x, self.y)))
        
        print(unit_locations)
        #setting horizontal spped
        if enemy_x - self.x//BLOCK_SIZE > 0:
            self.speedX = BLOCK_SIZE//5
        elif enemy_x - self.x//BLOCK_SIZE == 0:
            self.speedX = 0
        else:
            self.speedX = -BLOCK_SIZE//5

        # setting vertical speed BEWARE MINUS DIFFERENCE
        if enemy_y - self.y//BLOCK_SIZE > 0:
            self.speedY = BLOCK_SIZE//5
        elif enemy_y - self.y//BLOCK_SIZE == 0: 
            self.speedY = 0
        else:
            self.speedY = -BLOCK_SIZE//5


        unit_locations[side].remove((self.x//BLOCK_SIZE, self.y//BLOCK_SIZE))

        self.x += self.speedX
        self.y += self.speedY

        unit_locations[side].append((self.x//BLOCK_SIZE, self.y//BLOCK_SIZE))

        # self.body = pygame.Rect(self.x, self.y,self.size, self.size)

        arena[self.x//BLOCK_SIZE, self.y//BLOCK_SIZE].unit = self.side




class Infantry(Unit):
    def __init__(self,color,x,y, side):
        # Unit.__init__(self,color,x,y)
        super().__init__(color, x, y, side)
        self.size=BLOCK_SIZE
        self.strength=10
        self.health=100
        self.speed=BLOCK_SIZE//3
        # self.body = pygame.Rect(self.x, self.y,self.size,self.size)
        self.body = (x, y)
      
    # def update(self,arena):
    #     arena[self.x//BLOCK_SIZE, self.y//BLOCK_SIZE].unit != None
    #     if arena[self.x//BLOCK_SIZE - 1, self.y//BLOCK_SIZE].unit != None or arena[self.x//BLOCK_SIZE + 1, self.y//BLOCK_SIZE].unit != None:
    #         self.speed = 0

    #     self.x -= self.speed
    #     self.body = pygame.Rect(self.x, self.y,self.size, self.size)

    #     arena[self.x//BLOCK_SIZE, self.y//BLOCK_SIZE].unit = self.side

    def draw(self, window):
        # pygame.draw.rect(window, self.color.value, self.body)
        pygame.draw.rect(window, self.color.value, pygame.Rect(self.x, self.y, self.size, self.size))


class Heavy(Unit):
    def __init__(self,color,x,y, side):
        super().__init__(color, x, y, side)
        self.size=BLOCK_SIZE
        self.strength=30
        self.health=200
        # self.x=x
        # self.y=y
        self.body=(x, y)
        self.speed=BLOCK_SIZE//5
        # Unit.__init__(self,color,x,y)

    # def update(self,arena):
    #     arena[self.x//BLOCK_SIZE, self.y//BLOCK_SIZE].unit != None
    #     if arena[self.x//BLOCK_SIZE - 1, self.y//BLOCK_SIZE].unit != None or arena[self.x//BLOCK_SIZE + 2, self.y//BLOCK_SIZE].unit != None:
    #         self.speed = 0

    #     self.x -= self.speed
    #     self.body = (self.x,self.y)

    #     arena[self.x//BLOCK_SIZE, self.y//BLOCK_SIZE].unit = self.side

    def draw(self, window):
        pygame.draw.circle(window, self.color.value, self.body ,self.size)



class Cavalry(Unit):
    def __init__(self, color, x, y, side):
        super().__init__(color, x, y, side)
        self.size=BLOCK_SIZE
        self.strength=60
        self.health=150
        self.speed=BLOCK_SIZE
        # Unit.__init__(self,color,x,y)
        self.body=makeTriangle(self.size,45,0)
        offsetTriangle(self.body, self.x, self.y)

    # def update(self,arena):
    #     arena[self.x//BLOCK_SIZE, self.y//BLOCK_SIZE].unit != None
    #     if arena[self.x//BLOCK_SIZE -2, self.y//BLOCK_SIZE].unit != None or arena[self.x//BLOCK_SIZE + 2, self.y//BLOCK_SIZE].unit != None:
    #         self.speed = 0

    #     self.x-=self.speed
    #     offsetTriangle(self.body, -self.speed,0)
       
    #     arena[self.x//BLOCK_SIZE, self.y//BLOCK_SIZE].unit = self.side

    def draw(self, window):
        drawTriangle(self.body, self.color.value)








class Triangle:
    def __init__(self, p1, p2, p3):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

def makeTriangle(scale, internalAngle, rotation):
    #define the points in a uint space
    ia = (radians(internalAngle) * 2) - 1
    p1 = (0, -1)
    p2 = (cos(ia), sin(ia))
    p3 = (cos(ia) * -1, sin(ia))

    #rotate the points
    ra = radians(rotation)
    rp1x = p1[0] * cos(ra) - p1[1] * sin(ra)
    rp1y = p1[0] * sin(ra) + p1[1] * cos(ra)                 
    rp2x = p2[0] * cos(ra) - p2[1] * sin(ra)
    rp2y = p2[0] * sin(ra) + p2[1] * cos(ra)                        
    rp3x = p3[0] * cos(ra) - p3[1] * sin(ra)                         
    rp3y = p3[0] * sin(ra) + p3[1] * cos(ra)
    rp1 = ( rp1x, rp1y )
    rp2 = ( rp2x, rp2y )
    rp3 = ( rp3x, rp3y )

    #scale the points 
    sp1 = [rp1[0] * scale, rp1[1] * scale]
    sp2 = [rp2[0] * scale, rp2[1] * scale]
    sp3 = [rp3[0] * scale, rp3[1] * scale]
                    
    return Triangle(sp1, sp2, sp3)

def drawTriangle(tri, color=(0, 0, 0)):
    pygame.draw.polygon(WIN, color, (tri.p1, tri.p2,tri.p3))

def offsetTriangle(triangle, offsetx, offsety):
    triangle.p1[0] += offsetx;  triangle.p1[1] += offsety
    triangle.p2[0] += offsetx;  triangle.p2[1] += offsety
    triangle.p3[0] += offsetx;  triangle.p3[1] += offsety

ADJACENT = [(0, 1), (1, 0), (0, -1), (-1, 0)]

def find(data: np.array, start: tuple, searched_side):
  
  queue = deque()
  queue.append(start)

  while queue:
    pos = queue.popleft()
    if data[pos[0], pos[1]] == searched_side:
      print(pos[0], pos[1])
      return (pos[0], pos[1])
    else:
      for dxy in ADJACENT:
        (x, y) = (pos[0] + dxy[0], pos[1] + dxy[1])
        if x >= 0 and x < data.shape[0] and y >= 0 and y < data.shape[1]:
          queue.append((x,y))

  return None