import pygame
import numpy as np
from node import Node
import time
from settings import *

pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Maze Creator")
speed = 30

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

    def update(self, avaialable, path):
        screen.fill(BG_COLOR)
        pygame.draw.rect(screen, START, pygame.Rect(self.start_pos[0], self.start_pos[1], SQUARE_SIZE, SQUARE_SIZE))
        pygame.draw.rect(screen, END, pygame.Rect(self.end_pos[0], self.end_pos[1], SQUARE_SIZE, SQUARE_SIZE))


        for wall in self.walls:
            pygame.draw.rect(screen, WALL, pygame.Rect(wall[0], wall[1], SQUARE_SIZE, SQUARE_SIZE))

        for node in avaialable:
            if (node.x * SQUARE_SIZE, node.y * SQUARE_SIZE) not in {self.start_pos, self.end_pos}:
                pygame.draw.rect(screen, AVAILABLE, pygame.Rect(node.x * SQUARE_SIZE, node.y * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        for node in path:
            if (node.x * SQUARE_SIZE, node.y * SQUARE_SIZE) not in {self.start_pos, self.end_pos}:
                pygame.draw.rect(screen, FINAL_PATH, pygame.Rect(node.x * SQUARE_SIZE, node.y * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

        for x in range(0, WINDOW_SIZE[0], SQUARE_SIZE):
            pygame.draw.line(screen, color = (0,0,0), start_pos = (0, x), end_pos = (WINDOW_SIZE[0], x))
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
                    neighbours.append(maze_nodes[checkX][checkY])

    return neighbours

def getDistance(nodeA, nodeB):
    distance_x = np.abs(nodeA.x - nodeB.x)
    distance_y = np.abs(nodeA.y - nodeB.y)
    if distance_x > distance_y:
        return 14 * distance_y + 10 * (distance_x - distance_y)
    else:
        return 14 * distance_x + 10 * (distance_y - distance_x)

def getPath(startNode, endNode):
    path = []
    current_node = endNode
    while current_node != startNode:
        path.append(current_node)
        current_node = current_node.parent
    return path.reverse()

def runMaze():
    ######################################################## maze creation
    maze = Maze()
    while maze.state != 'end':
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

        if maze.state == 'ready':
            # path finding
            maze_nodes = np.empty((ARRAY_SIZE), dtype = Node)

            # creating grid of nodes
            for x in range(int(WINDOW_SIZE[0] / SQUARE_SIZE)):
                for y in range(int(WINDOW_SIZE[1] / SQUARE_SIZE)):
                    if (x*SQUARE_SIZE,y*SQUARE_SIZE) == maze.start_pos:
                        start_node = Node((x,y), walkable = True)
                        maze_nodes[x][y] = start_node
                    elif (x*SQUARE_SIZE,y*SQUARE_SIZE) == maze.end_pos:
                        target_node = Node((x,y), walkable = True)
                        maze_nodes[x][y] = target_node
                    elif (x*SQUARE_SIZE,y*SQUARE_SIZE) not in maze.walls:
                        maze_nodes[x][y] = Node(coordinates = (x,y), walkable = True)
                    else:
                        maze_nodes[x][y] = Node(coordinates = (x,y), walkable = False)

            # list of nodes to process, starting with start_node
            open_set = [start_node]
            # list of nodes that have been already processed
            closed_set = []

            while len(open_set) > 0:
                current_node = open_set[0]
                # searching for lowest cost node
                for node in open_set[1:]:
                    if node.get_F_cost() < current_node.get_F_cost() or node.get_F_cost() == current_node.get_F_cost() and node.H_cost < current_node.H_cost:
                        current_node = node

                open_set.remove(current_node)
                closed_set.append(current_node)

                if current_node == target_node:
                    getPath(start_node, target_node)
                    quit()

                for neighbour in getNeighbours(current_node, maze_nodes):
                    if not neighbour.walkable or neighbour in closed_set:
                        continue

                    newCostToNeighbour = current_node.G_cost + getDistance(current_node, neighbour)
                    if (newCostToNeighbour < neighbour.G_cost) or (neighbour not in open_set):
                        neighbour.G_cost = newCostToNeighbour
                        neighbour.H_cost = getDistance(neighbour, target_node)
                        neighbour.parent = current_node

                        if neighbour not in open_set:
                            open_set.append(neighbour)
                            maze.update(open_set, closed_set)
                            time.sleep(1/speed)

        else:
            maze.draw()