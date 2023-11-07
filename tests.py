def circle_around(arr):

    index = 0
    s = arr.shape
    x, y = 1, 1
    r = 1
    i, j = x- 1, y - 1
    while index < 10:
        while i < x + r and i < s[0]:
            print(arr[i, j])
            i += 1
        while j < y + r and j < s[1]:
            print(arr[i, j])
            j += 1
        while i > x - r and i >= 0:
            print(arr[i, j])
            i -= 1
        while j > y - r and j >=0:
            print(arr[i, j])
            j -=1
        r += 1
        j -= 1
        index += 1
        if j < 0:
            break
        # print(i, j)

import numpy as np
from collections import deque

ADJACENT = [(0, 1), (1, 0), (0, -1), (-1, 0)]

def find(data: np.array, start: tuple):
  
  queue = deque()
  queue.append(start)

  while queue:
    pos = queue.popleft()
    if data[pos[0], pos[1]]:
      return (pos[0], pos[1])
    else:
      for dxy in ADJACENT:
        (x, y) = (pos[0] + dxy[0], pos[1] + dxy[1])
        if x >= 0 and x < data.shape[0] and y >= 0 and y < data.shape[1]:
          queue.append((x,y))
          print(x, y)

  return None


arr = np.zeros([180, 100])
arr[0, 3] = 1
arr[0, 0] = 1
print(find(arr, (100,30)))