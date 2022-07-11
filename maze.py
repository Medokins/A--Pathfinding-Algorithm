import pygame
import numpy as np

pygame.init()
WINDOW_SIZE = (1000, 1000)
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Maze Creator")

BG_COLOR = (253, 244, 220)
START = (0, 255, 0)
END = (255, 0, 0)
WALL = (0, 0, 0)

class Maze:
    def __init__(self):
        # mouse position
        self.x = 0
        self.y = 0

        # state
        self.state = 'choosig'
    
    def draw(self):
        # set color to bg of maze
        screen.fill(BG_COLOR)

        # grid creation
        for x in range(0, 1000, 50):
            # horizontal lines
            pygame.draw.line(screen, color = (0,0,0), start_pos = (0, x), end_pos = (WINDOW_SIZE[0], x))
            # vertical lines
            pygame.draw.line(screen, color = (0,0,0), start_pos = (x, 0), end_pos = (x, WINDOW_SIZE[1]))

        pygame.display.update()

def runMaze():
    maze = Maze()
    while maze.state != 'end':
        maze.x, maze.y = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                maze.state = 'end'
                pygame.quit()

        try:
            maze.draw()
        except:
            print("Display turned off")