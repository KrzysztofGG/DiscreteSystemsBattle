import pygame
from enum import Enum
from math import sin, cos, pi, radians, sqrt, pow
from utils import *
import random
import os

class Side(Enum):
    RED=1
    GREEN=2
    
pygame.mixer.init()
DEATH_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'death-sound.mp3'))

GAME_ENDS_EVENT = pygame.USEREVENT + 2

class Unit:
    def __init__(self, color, x, y, side, id=0):
        self.id = id
        self.x = x
        self.y = y
        self.health = 100
        self.max_strength = 20
        self.strength = self.max_strength
        self.color = color
        self.side = side
        self.max_speed = BLOCK_SIZE//2
        self.min_speed = BLOCK_SIZE//2
        self.speed = (self.max_speed + self.min_speed)//2
        self.speedX = self.max_speed
        self.speedY = self.max_speed
        self.range = 1
        self.body = (x, y)

    def distance(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    def get_location(self):
        return (self.x, self.y)
    
    def hit_enemy(self, enemy, units_dict):
        enemy.health -= self.strength + random.uniform(0, self.strength)
        if enemy.health <= 0:
            DEATH_SOUND.play()
            units_dict[enemy.side].remove(enemy)
        return len(units_dict[enemy.side]) == 0

    def count_speed_change(self, arena): #based on changing height of terrain
        
        future_x = int((self.x + self.speedX)//BLOCK_SIZE)
        future_y = int((self.y + self.speedY)//BLOCK_SIZE)
        current_x = int(self.x//BLOCK_SIZE)
        current_y = int(self.y//BLOCK_SIZE)
        height_diff = arena[future_y, future_x].height - arena[current_y, current_x].height

        #preety sure it can be done nicer
        SPEED_CHANGE_MODIFIER = 10
        speed_change =  -height_diff * self.max_speed * SPEED_CHANGE_MODIFIER

        return speed_change
    
    def count_speed(self, enemy_x, enemy_y, arena):

        dx = enemy_x - self.x
        dy = enemy_y - self.y
        
        dist = sqrt(pow(dx, 2) + pow(dy, 2))
        sinus = abs(dy)/dist
        cosinus = abs(dx)/dist

        #count speed in direction to target
        self.speed += self.count_speed_change(arena)
        if self.speed > self.max_speed:
            self.speed = self.max_speed
        if self.speed < self.min_speed:
            self.speed = self.min_speed

        #count horizontal speed component
        if dx > 0:
            self.speedX = self.speed * cosinus
        elif dx == 0:
            self.speedX = 0
        else:
            self.speedX = -self.speed * cosinus

        #count vertical speed component
        if dy > 0:
            self.speedY = self.speed * sinus
        elif dy == 0:
            self.speedY = 0
        else:
            self.speedY = -self.speed * sinus

        #update strengh based on speed
        self.strength = self.max_strength * (self.speed/self.max_speed)

    def update(self, arena, units_dict):
        
        # arena[self.x//BLOCK_SIZE, self.y//BLOCK_SIZE].unit = None

        # finding nearest enemy
        if self.side == Side.GREEN:
            enemy_side = Side.RED
        else:
            enemy_side = Side.GREEN
        # enemy_x, enemy_y = min(unit_locations[enemy_side], key = lambda coords: self.distance(coords, (self.x, self.y)))
        # units_locations = list(map(lambda u: (u.x, u.y), units_dict[enemy_side]))
        if len(units_dict[enemy_side]) == 0:
            self.speedX = 0
            self.speedY = 0
            return 
        
        enemy = min(units_dict[enemy_side], key = lambda e: self.distance(e.get_location(), (self.x, self.y)))
        enemy_x, enemy_y = enemy.x, enemy.y
        # enemy_x, enemy_y = min(units_locations, key = lambda coords: self.distance(coords, (self.x, self.y)))

        self.count_speed(enemy_x, enemy_y, arena)
        
        if (pygame.Rect.colliderect(pygame.Rect(self.x, self.y, self.size, self.size),
            pygame.Rect(enemy_x, enemy_y, self.size, self.size))):
            self.speedX = 0
            self.speedY = 0
            if self.hit_enemy(enemy, units_dict):
                pygame.event.post(pygame.event.Event(GAME_ENDS_EVENT))

        
        
        # adjusting speed if enemy nearby
        # if (arena[self.x//BLOCK_SIZE - self.range, self.y//BLOCK_SIZE].unit != None or 
        #     arena[self.x//BLOCK_SIZE + self.range, self.y//BLOCK_SIZE].unit != None or
        #     arena[self.x//BLOCK_SIZE, self.y//BLOCK_SIZE - self.range].unit != None or
        #     arena[self.x//BLOCK_SIZE, self.y//BLOCK_SIZE + self.range].unit != None):
        #     self.speedX = 0
        #     self.speedY = 0

        # unit_locations[self.side].remove((self.x, self.y))

        self.x += self.speedX
        self.y += self.speedY

        # unit_locations[self.side].append((self.x, self.y))
        self.body = (self.x, self.y)

        # arena[self.x//BLOCK_SIZE, self.y//BLOCK_SIZE].unit = self.side
        

class Infantry(Unit):
    def __init__(self, color, x, y, side, id=0):
        # Unit.__init__(self,color,x,y)
        super().__init__(color, x, y, side, id)
        self.size=BLOCK_SIZE
        self.strength=10
        self.health=100
        # self.default_speed = BLOCK_SIZE//5
        # self.speedX = self.default_speed
        # self.speedY = self.default_speed
        self.range = 1
        
    def draw(self, window):
        # pygame.draw.rect(window, self.color.value, self.body)
        pygame.draw.rect(window, self.color.value, pygame.Rect(self.x, self.y, self.size, self.size))


class Heavy(Unit):
    def __init__(self,color,x,y, side):
        super().__init__(color, x, y, side)
        self.size=BLOCK_SIZE//2
        self.strength=30
        self.health=200
        # self.default_speed = BLOCK_SIZE//10
        # self.speedX = self.default_speed
        # self.speedY = self.default_speed
        self.range = 2

    def draw(self, window):
        pygame.draw.circle(window, self.color.value, self.body, self.size)



class Cavalry(Unit):
    def __init__(self, color, x, y, side):
        super().__init__(color, x, y, side)
        self.size=BLOCK_SIZE
        self.strength=60
        self.health=150
        self.default_speed = BLOCK_SIZE
        self.speedX = self.default_speed
        self.speedY = self.default_speed
        self.range = 2
        self.body=makeTriangle(self.size, 45, 0)
        offsetTriangle(self.body, self.x, self.y)

    # def update(self,arena):
    #     arena[self.x//BLOCK_SIZE, self.y//BLOCK_SIZE].unit != None
    #     if arena[self.x//BLOCK_SIZE -2, self.y//BLOCK_SIZE].unit != None or arena[self.x//BLOCK_SIZE + 2, self.y//BLOCK_SIZE].unit != None:
    #         self.speed = 0

    #     self.x-=self.speed
    #     offsetTriangle(self.body, -self.speed,0)
       
    #     arena[self.x//BLOCK_SIZE, self.y//BLOCK_SIZE].unit = self.side

    def update(self, arena, unit_locations):
        super().update(arena, unit_locations)
        offsetTriangle(self.body, -self.speedX,0)


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

# ADJACENT = [(0, 1), (1, 0), (0, -1), (-1, 0)]

# def find(data: np.array, start: tuple, searched_side):
  
#   queue = deque()
#   queue.append(start)

#   while queue:
#     pos = queue.popleft()
#     if data[pos[0], pos[1]] == searched_side:
#       print(pos[0], pos[1])
#       return (pos[0], pos[1])
#     else:
#       for dxy in ADJACENT:
#         (x, y) = (pos[0] + dxy[0], pos[1] + dxy[1])
#         if x >= 0 and x < data.shape[0] and y >= 0 and y < data.shape[1]:
#           queue.append((x,y))

#   return None