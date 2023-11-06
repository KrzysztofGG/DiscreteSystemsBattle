import pygame
import sys

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
LIGHTGREEN = pygame.Color('#90EE90')

WIDTH, HEIGHT = 1350, 750
FPS = 60
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

def main():
    pygame.init()
    pygame.display.set_caption("Battle Simulator")
    CLOCK = pygame.time.Clock()
    WIN.fill(LIGHTGREEN)

    while True:
        drawGrid()
        CLOCK.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()


def drawGrid():
    blockSize = 10
    for x in range(0, WIDTH, blockSize):
        for y in range(0, HEIGHT, blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            pygame.draw.rect(WIN, GRAY, rect, 1)

if __name__ == "__main__":
    main()