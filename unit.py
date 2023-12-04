import pygame
from enum import Enum
from math import sin, cos, pi, radians, sqrt, pow
from utils import *
import random
import os
from color import Color

class Side(Enum):
    RED=1
    BLUE=2
    
pygame.mixer.init()
DEATH_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'death-sound.mp3'))
DEATH_SOUND.set_volume(0.2)

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
        self.min_speed = BLOCK_SIZE//6
        self.speed = (self.max_speed + self.min_speed)//2
        self.speedX = self.max_speed
        self.speedY = self.max_speed
        self.goind_around = False
        self.body = (x, y)
        self.critical_health = self.health * 0.2
        self.running = False
        self.enemy_heights = []

    def distance(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    def get_location(self):
        return (self.x, self.y)
    
    def show_unit_details(self, arena):
        FONT = pygame.font.SysFont('arial', 10)
        box_width, box_height = 60, 50

        rect = pygame.draw.rect(WIN, Color.WHITE.value, (self.x, self.y, box_width, box_height))
        text1 = f'Health: {int(self.health)}'
        text2 = f'Strength: {int(self.strength)}'
        text3 = f'Speed: {int(self.speed)}'
        text4 = f'Height: {arena[int(self.y//BLOCK_SIZE), int(self.x//BLOCK_SIZE)].height:.2f}'

        text_render1 = FONT.render(text1, 1, self.color.value)
        text_render2 = FONT.render(text2, 1, self.color.value)
        text_render3 = FONT.render(text3, 1, self.color.value)
        text_render4 = FONT.render(text4, 1, self.color.value)
        
        WIN.blit(text_render1, (rect.x, rect.y))
        WIN.blit(text_render2, (rect.x, rect.y + text_render1.get_height()))
        WIN.blit(text_render3, (rect.x, rect.y + text_render2.get_height() * 2))
        WIN.blit(text_render4, (rect.x, rect.y + text_render2.get_height() * 3))

    
    def hit_enemy(self, enemy, units_dict):
        enemy.health -= self.strength + random.uniform(0, self.strength/2)
        if enemy.health <= 0:
            DEATH_SOUND.play()
            units_dict[enemy.side].remove(enemy)
        # return len(units_dict[enemy.side]) == 0

    def count_height_diff(self, arena):
        future_x = int((self.x + self.speedX)//BLOCK_SIZE)
        future_y = int((self.y + self.speedY)//BLOCK_SIZE)
        current_x = int(self.x//BLOCK_SIZE)
        current_y = int(self.y//BLOCK_SIZE)
        height_diff = arena[future_y, future_x].height - arena[current_y, current_x].height

        return height_diff
    
    def check_if_river(self, arena):
        future_x = int((self.x + self.speedX * 4)//BLOCK_SIZE)
        future_y = int((self.y + self.speedY * 4)//BLOCK_SIZE)

        expected_x1 = int((self.x)//BLOCK_SIZE + 1)
        expected_x2 = int((self.x)//BLOCK_SIZE - 1)
        expected_y1 = int((self.y)//BLOCK_SIZE + 1)
        expected_y2 = int((self.y)//BLOCK_SIZE - 1)

        current_x = int(self.x//BLOCK_SIZE)
        current_y = int(self.y//BLOCK_SIZE)



        # if self.goind_around:
        #     if self.id == 1:
        #         print(self.x_to_go, self.x)
        #     if abs(self.y_to_go - self.y) < 2 or abs(self.x_to_go - self.x) < 2:
        #         self.goind_around = False
        #         return
        # else:
            # self.y_to_go = self.y
            # self.x_to_go = self.x
            # return

        if self.goind_around:
            if (self.going_horizontal and abs(self.x_to_go - self.x) < 3) or (self.going_vertical and abs(self.y_to_go - self.y) < 3):
                self.goind_around = False
                self.going_vertical = False
                self.going_horizontal = False
                return
            
        if arena[current_y, future_x].river or arena[current_y, expected_x1].river or arena[current_y, expected_x2].river :


            if not self.goind_around:
                self.y_to_go = self.find_way_around_vertical(arena, current_y, future_x) * BLOCK_SIZE
                self.x_to_go = self.x
                self.going_vertical = True
                self.going_horizontal = False

                self.count_speed(current_x * BLOCK_SIZE, self.y_to_go, arena)
                self.goind_around = True
        elif arena[future_y, current_x].river or arena[expected_y1, current_x].river or arena[expected_y2, expected_x2].river:

            if not self.goind_around:
                self.x_to_go = self.find_way_around_horizontal(arena, current_x, future_y) * BLOCK_SIZE
                self.y_to_go = self.y
                self.going_horizontal = True
                self.going_vertical = False

                self.count_speed(self.x_to_go, current_y * BLOCK_SIZE, arena)
                self.goind_around = True

        # else:
        #     self.goind_around = False

    def find_way_around_vertical(self, arena, current_y, future_x):

        index = 0
        while current_y - index >= 0 or current_y + index < arena.shape[0]:

            if not arena[current_y + index, future_x].river:
                # return True
                return current_y + index + 1
            
            elif not arena[current_y - index, future_x].river:
                # return False
                return current_y - index - 1
            
            index += 1
        return -1
    def find_way_around_horizontal(self, arena, current_x, future_y):

        index = 0
        while current_x - index >= 0 or current_x + index < arena.shape[1]:
            if not arena[future_y, current_x + index].river:
                return current_x + index + 1
            elif not arena[future_y, current_x - index].river:
                return current_x - index - 1
            
            index += 1
        return -1
    def count_speed_change(self, arena): #based on changing height of terrain
        
        height_diff = self.count_height_diff(arena)

        #preety sure it can be done nicer
        SPEED_CHANGE_MODIFIER = 10
        if abs(height_diff) < 0.05:
            speed_change = (self.max_speed - self.speed)/80
        else:
            speed_change =  -height_diff * self.max_speed * SPEED_CHANGE_MODIFIER

        return speed_change
    
    def count_speed(self, unit_x, unit_y, arena):

        dx = unit_x - self.x
        dy = unit_y - self.y

        dist = sqrt(pow(dx, 2) + pow(dy, 2))
        sinus = abs(dy)/dist
        cosinus = abs(dx)/dist

        #count speed in direction to target
        self.speed += self.count_speed_change(arena)
        if self.speed > self.max_speed:
            self.speed = self.max_speed
        if self.speed < self.min_speed:
            self.speed = self.min_speed
        
        # make unit run away when low on healt
        if self.running:
            self.speed *= 0.7
            self.speed *= -1

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
        self.strength = self.max_strength/2 + self.max_strength * (self.speed/self.max_speed)/2

    def wait_if_above_enemy(self, arena, enemy):

        self_height = arena[int(self.y//BLOCK_SIZE), int(self.x//BLOCK_SIZE)].height
        enemy_height = arena[int(enemy.y//BLOCK_SIZE), int(enemy.x//BLOCK_SIZE)].height

        if self_height < 0.3 + enemy_height: #if not high enough just go
            return
        
        self.enemy_heights.append(enemy.count_height_diff(arena))
        if len(self.enemy_heights) > 5:
            self.enemy_heights.pop()

        if(sum(self.enemy_heights) > 0): #enemy started goind up the hill, attack
            return
        else: #wait for enemy
            self.speed = 0
            self.speedX = 0
            self.speedY = 0


    def choose_direction(self, squad_units, arena, enemy):
        if len(squad_units) > 0:

            squad_unit_closest = min(squad_units, key = lambda u: self.distance(u.get_location(), (self.x, self.y)))

            if (self.distance(squad_unit_closest.get_location(), (self.x, self.y)) > 25 and not squad_unit_closest.running):
                self.count_speed(squad_unit_closest.x, squad_unit_closest.y, arena)
            else:
                self.count_speed(enemy.x, enemy.y, arena)

        else:
            self.count_speed(enemy.x, enemy.y, arena)

    def update(self, arena, units_dict):

        if self.health <= self.critical_health:
            self.running = True

        # finding nearest enemy
        if self.side == Side.BLUE:
            enemy_side = Side.RED
        else:
            enemy_side = Side.BLUE

        if len(units_dict[enemy_side]) == 0:
            self.speedX = 0
            self.speedY = 0
            return 
        
        enemy = min(units_dict[enemy_side], key = lambda e: self.distance(e.get_location(), (self.x, self.y)))
        enemy_x, enemy_y = enemy.x, enemy.y

        squad_units = list(filter(lambda u: u.max_strength == self.max_strength and u != self, units_dict[self.side]))
        
        # head to the nearest enemy of same type, if close enough head for enemies

        #stop for fighting
        if (pygame.Rect.colliderect(pygame.Rect(self.x, self.y, self.size, self.size),
            pygame.Rect(enemy_x, enemy_y, self.size, self.size)) and not self.running):
            self.speed = 0
            self.speedX = 0
            self.speedY = 0
            self.hit_enemy(enemy, units_dict)



        self.check_if_river(arena)
        if not self.goind_around:     
            self.choose_direction(squad_units, arena, enemy)
            # self.wait_if_above_enemy(arena, enemy)

        self.x += self.speedX
        self.y += self.speedY

        #remove unit if ran out of the arena
        if self.x < 0 or self.x > WIDTH or self.y < 0 or self.y > HEIGHT:
            units_dict[self.side].remove(self)

        if len(units_dict[enemy.side]) == 0:
            pygame.event.post(pygame.event.Event(GAME_ENDS_EVENT)) 

        self.body = (self.x, self.y)        


    
        

class Infantry(Unit):
    def __init__(self, color, x, y, side, id=0):
        super().__init__(color, x, y, side, id)
        self.size=BLOCK_SIZE
        self.max_strength = 12
        self.strength = self.max_strength/2
        self.health=100
        self.max_speed = BLOCK_SIZE//2
        self.min_speed = BLOCK_SIZE//6
        # self.range = 2

    def draw(self, window):
        pygame.draw.rect(window, self.color.value, pygame.Rect(self.x, self.y, self.size, self.size))


class Heavy(Unit):
    def __init__(self,color,x,y, side, id=0):
        super().__init__(color, x, y, side, id)
        self.size=BLOCK_SIZE//2
        # self.max_strength = 30
        self.max_strength = 16
        self.strength = self.max_strength/2
        self.health=200
        self.max_speed=BLOCK_SIZE//3
        self.min_speed=BLOCK_SIZE//8
        # self.range = 2

    def draw(self, window):
        pygame.draw.circle(window, self.color.value, self.body, self.size)



class Cavalry(Unit):
    def __init__(self, color, x, y, side):
        super().__init__(color, x, y, side)
        self.size=BLOCK_SIZE
        # self.max_strength=60
        self.max_strength=20
        self.strength = self.max_strength / 2
        self.health=150
        self.max_speed=BLOCK_SIZE
        self.min_speed=BLOCK_SIZE//2
        # self.range = 2
        self.triangle=makeTriangle(self.size, 45, 0)
        self.body=offsetTriangle(self.triangle, self.x, self.y)

    def update(self, arena, unit_locations):
        super().update(arena, unit_locations)
        offsetTriangle(self.triangle, self.speedX, self.speedY)

    def draw(self, window):
        drawTriangle(self.triangle, self.color.value)


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
    x=(triangle.p1[0]+triangle.p2[0]+triangle.p3[0])/3
    y=(triangle.p1[1]+triangle.p2[1]+triangle.p3[1])/3
    return (x,y)


def addFormation(grid,x,y,amount,size,Side,type):
    units=[]
    if Side==Side.RED: 
        color=Color.RED
    else:
        color=Color.BLUE
    for i in range(0,amount):
        rand=random.randrange(-size,size)
        rand2=random.random()
        offset_x=x +rand*rand2
        rand=random.randrange(-size,size)
        rand2=random.random()
        offset_y=y +rand*rand2
        if type =="infantry":
            units.append(Infantry(color,offset_x,offset_y, Side))
        elif type=="heavy":
            units.append(Heavy(color,offset_x,offset_y, Side))
        elif type=="cavalry":
             units.append(Cavalry(color,offset_x,offset_y,Side))
        else:
            pass
    for unit in units:
        grid.units_dict[Side].append(unit)