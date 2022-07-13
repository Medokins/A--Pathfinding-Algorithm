import pygame
import numpy as np
from node import Node

pygame.init()
WINDOW_SIZE = (1000, 1000)
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Maze Creator")

SQUARE_SIZE = 50

BG_COLOR = (253, 244, 220)
START = (0, 255, 0)
END = (255, 0, 0)
WALL = (0, 0, 0)

AVAILABLE = (118, 187, 104)
PATHED = (249, 56, 34)
FINAL_PATH = (144, 224, 247)

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
            pygame.draw.rect(screen, START, pygame.Rect(self.start_pos[0], self.start_pos[1], SQUARE_SIZE, SQUARE_SIZE))
        if self.end_pos != None:
            pygame.draw.rect(screen, END, pygame.Rect(self.end_pos[0], self.end_pos[1], SQUARE_SIZE, SQUARE_SIZE))
        for wall in self.walls:
            pygame.draw.rect(screen, WALL, pygame.Rect(wall[0], wall[1], SQUARE_SIZE, SQUARE_SIZE))
        # grid creation
        for x in range(0, WINDOW_SIZE[0], SQUARE_SIZE):
            # horizontal lines
            pygame.draw.line(screen, color = (0,0,0), start_pos = (0, x), end_pos = (WINDOW_SIZE[0], x))
            # vertical lines
            pygame.draw.line(screen, color = (0,0,0), start_pos = (x, 0), end_pos = (x, WINDOW_SIZE[1]))

        pygame.display.update()

def runMaze():
    # maze creation
    maze = Maze()
    while maze.state != 'ready':
        maze.x, maze.y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                maze.state = 'end'
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    if maze.start_pos != None and maze.end_pos != None:
                        maze.state = 'ready'
                if event.key == pygame.K_s:
                    maze.state = "choosing_start_pos"
                if event.key == pygame.K_e:
                    maze.state = "choosing_end_pos"
                if event.key == pygame.K_w:
                    maze.state = "creating_obstacles"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if maze.state == "choosing_start_pos":
                    maze.start_pos = (maze.x // SQUARE_SIZE * SQUARE_SIZE, maze.y // SQUARE_SIZE * SQUARE_SIZE)
                if maze.state == "choosing_end_pos":
                    maze.end_pos = (maze.x // SQUARE_SIZE * SQUARE_SIZE, maze.y // SQUARE_SIZE * SQUARE_SIZE)
                if maze.state == "creating_obstacles":
                    if (maze.x // SQUARE_SIZE * SQUARE_SIZE, maze.y // SQUARE_SIZE * SQUARE_SIZE) not in {maze.start_pos, maze.end_pos}:
                        maze.walls.append((maze.x // SQUARE_SIZE * SQUARE_SIZE , maze.y // SQUARE_SIZE * SQUARE_SIZE))
        try:
            maze.draw()
        except:
            print("Display turned off")
        
    # path finding   
    maze_nodes = []
    for x in range(0, WINDOW_SIZE[0], SQUARE_SIZE):
        for y in range(0, WINDOW_SIZE[1], SQUARE_SIZE):
            if (x,y) not in maze.walls:
                maze_nodes.append(Node(coordinates = (x,y), walkable = True))
            else:
                maze_nodes.append(Node(coordinates = (x,y), walkable = False))

    open = []
    closed = []

    print(len(maze_nodes))

    found_path = False
    # while not found_path:
    #     pass