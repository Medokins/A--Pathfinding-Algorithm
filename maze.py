import pygame
import numpy as np
from node import Node
from settings import *

pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Maze Creator")

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

def getNeighbours(node, maze_nodes):
    neighbours = []

    for x in range(-1, 2):
        for y in range(-1, 2):
            if x == 0 and y == 0:
                pass
            else:
                checkX = node.x + x
                checkY = node.y + y

                if (checkX >= 0 and checkX < ARRAY_SIZE[0]) and (checkY >= 0 and checkY < ARRAY_SIZE[1]):
                    if maze_nodes[checkX][checkY].walkable:
                        neighbours.append(Node(coordinates = (checkX, checkY), walkable = True))
                    else:
                        neighbours.append(Node(coordinates = (checkX, checkY), walkable = False))

    return neighbours

def runMaze():
    ######################################################## maze creation
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
        
    ######################################################## path finding
    maze_nodes = np.empty((ARRAY_SIZE), dtype = Node)
    # creating grid of nodes
    for x in range(int(WINDOW_SIZE[0] / SQUARE_SIZE)):
        for y in range(int(WINDOW_SIZE[1] / SQUARE_SIZE)):
            if (x*SQUARE_SIZE,y*SQUARE_SIZE) == maze.start_pos:
                start_node = Node((x,y), walkable = True)
            elif (x*SQUARE_SIZE,y*SQUARE_SIZE) == maze.end_pos:
                target_node = Node((x,y), walkable = True)
            elif (x*SQUARE_SIZE,y*SQUARE_SIZE) not in maze.walls:
                maze_nodes[x][y] = Node(coordinates = (x,y), walkable = True)
            else:
                maze_nodes[x][y] = Node(coordinates = (x,y), walkable = False)

    open_set = [start_node]
    closed_set = []

    while len(open_set) > 0:
        current_node = open_set[0]
        for node in open_set[1:]:
            if (node.get_F_cost() < current_node.get_F_cost()) or (node.get_F_cost() == current_node.get_F_cost() and node.H_cost < current_node.H_cost):
                current_node = node

        open_set.remove(current_node)
        closed_set.append(current_node)

        if current_node == target_node:
            quit()

        for neighbour in getNeighbours(current_node, maze_nodes):
            if (not neighbour.walkable) or (neighbour in closed_set):
                pass
