import pygame
from enum import Enum
from math import sin, cos, pi, radians
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


class Unit:
    def __init__(self,color,x,y):
        self.x=x
        self.y=y
        self.color=color


class Infantry(Unit):
    def __init__(self,color,x,y):
        Unit.__init__(self,color,x,y)
        self.size=BLOCK_SIZE
        self.strength=10
        self.health=100
        self.speed=BLOCK_SIZE//3
        self.body = pygame.Rect(self.x, self.y,self.size,self.size)
      
    def update(self,arena):
        arena[self.x//BLOCK_SIZE, self.y//BLOCK_SIZE].has_units = False
        if arena[self.x//BLOCK_SIZE - 1, self.y//BLOCK_SIZE].has_units or arena[self.x//BLOCK_SIZE + 1, self.y//BLOCK_SIZE].has_units:
            self.speed = 0

        self.x -= self.speed
        self.body = pygame.Rect(self.x, self.y,self.size, self.size)

        arena[self.x//BLOCK_SIZE, self.y//BLOCK_SIZE].has_units = True

    def draw(self, window):
        pygame.draw.rect(window, self.color.value, self.body)


class Heavy(Unit):
    def __init__(self,color,x,y):
        self.size=BLOCK_SIZE
        self.strength=30
        self.health=200
        self.x=x
        self.y=y
        self.body=(x,y)
        self.speed=BLOCK_SIZE//5
        Unit.__init__(self,color,x,y)

    def update(self,arena):
        arena[self.x//BLOCK_SIZE, self.y//BLOCK_SIZE].has_units = False
        if arena[self.x//BLOCK_SIZE - 1, self.y//BLOCK_SIZE].has_units or arena[self.x//BLOCK_SIZE + 2, self.y//BLOCK_SIZE].has_units:
            self.speed = 0

        self.x -= self.speed
        self.body = (self.x,self.y)

        arena[self.x//BLOCK_SIZE, self.y//BLOCK_SIZE].has_units = True
    def draw(self, window):
        pygame.draw.circle(window, self.color.value,self.body,self.size)



class Cavalery(Unit):
    def __init__(self,color,x,y):
        self.size=BLOCK_SIZE
        self.strength=60
        self.health=150
        self.speed=BLOCK_SIZE
        Unit.__init__(self,color,x,y)
        self.body=makeTriangle(self.size,45,0)
        offsetTriangle(self.body, self.x,self.y)

    def update(self,arena):
        arena[self.x//BLOCK_SIZE, self.y//BLOCK_SIZE].has_units = False
        if arena[self.x//BLOCK_SIZE -2, self.y//BLOCK_SIZE].has_units or arena[self.x//BLOCK_SIZE + 2, self.y//BLOCK_SIZE].has_units:
            self.speed = 0

        self.x-=self.speed
        offsetTriangle(self.body, -self.speed,0)
       
        arena[self.x//BLOCK_SIZE, self.y//BLOCK_SIZE].has_units = True

    def draw(self, window):
        drawTriangle(self.body,self.color.value)








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