

import numpy as np
from math import sqrt, pow

def create_hill_on_arena(centerX, centerY, radius, arena, arena_start_x, arena_start_y, max_height):
    radius = (radius * 2) + 1
    radiusSq = (radius * radius) / 4
    for y in range(0, radius):
        yDiff = y - centerY
        threshold = radiusSq - (yDiff * yDiff)
        for x in range(0, radius):
            if (y + arena_start_y > 0 and y + arena_start_y < arena.shape[0] and
                x + arena_start_x > 0 and x + arena_start_x < arena.shape[1]):
              xDiff = x - centerX
              if xDiff * xDiff <= threshold:
                  dist = sqrt(pow(yDiff, 2) + pow(xDiff, 2))
                  height_increase = max_height - dist/radius
                  # arena[y, x].height += height_increase
                  arena[y + arena_start_y, x + arena_start_x] += height_increase



A = np.array([[1,2, 3],
              [5,6, 3]])
print(A.shape)

def create_hill_on_arena_og(centerX, centerY, radius, arr, arena, max_height):
    radius = (radius * 2) + 1
    radiusSq = (radius * radius) / 4
    for y in range(0, arr.shape[0]):
        yDiff = y - centerY
        threshold = radiusSq - (yDiff * yDiff)
        for x in range(0, arr.shape[1]):
            xDiff = x - centerX
            if xDiff * xDiff <= threshold:
                dist = sqrt(pow(yDiff, 2) + pow(xDiff, 2))
                height_increase = max_height - dist/radius
                # arena[y, x].height += height_increase
                arena[y, x] += height_increase

