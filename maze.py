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
        self.state = 'choosing'

        # maze variables
        self.start_pos = None
        self.end_pos = None
        self.walls = []
    
    def draw(self):
        # set color to bg of maze
        screen.fill(BG_COLOR)

        if self.start_pos != None:
            pygame.draw.rect(screen, START, pygame.Rect(self.start_pos[0], self.start_pos[1], 50, 50))
        if self.end_pos != None:
            pygame.draw.rect(screen, END, pygame.Rect(self.end_pos[0], self.end_pos[1], 50, 50))
        for wall in self.walls:
            pygame.draw.rect(screen, WALL, pygame.Rect(wall[0], wall[1], 50, 50))
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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    maze.state = "choosing_start_pos"
                if event.key == pygame.K_e:
                    maze.state = "choosing_end_pos"
                if event.key == pygame.K_w:
                    maze.state = "creating_obstacles"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if maze.state == "choosing_start_pos":
                    maze.start_pos = (maze.x // 50 * 50, maze.y // 50 * 50)
                if maze.state == "choosing_end_pos":
                    maze.end_pos = (maze.x // 50 * 50, maze.y // 50 * 50)
                if maze.state == "creating_obstacles":
                    if (maze.x // 50 * 50, maze.y // 50 * 50) not in {maze.start_pos, maze.end_pos}:
                        maze.walls.append((maze.x // 50 * 50 , maze.y // 50 * 50))

        try:
            maze.draw()
        except:
            print("Display turned off")