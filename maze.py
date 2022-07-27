import pygame
import numpy as np
from node import Node
import time
from settings import *

from heap import Heap

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
        self.special_nodes = []
        for _ in range(len(WEIGHTS)):
            self.special_nodes.append([])

    def draw(self, available = None, path = None, color = None):
        # set color to bg of maze
        screen.fill(BG_COLOR)
        font = pygame.font.SysFont('Calibri', 24)

        if self.start_pos != None:
            pygame.draw.rect(screen, START, pygame.Rect(self.start_pos[0], self.start_pos[1], SQUARE_SIZE, SQUARE_SIZE))
        if self.end_pos != None:
            pygame.draw.rect(screen, END, pygame.Rect(self.end_pos[0], self.end_pos[1], SQUARE_SIZE, SQUARE_SIZE))
        for wall in self.walls:
            pygame.draw.rect(screen, WALL, pygame.Rect(wall[0], wall[1], SQUARE_SIZE, SQUARE_SIZE))

        for i in range(len(WEIGHTS)):
            for node in self.special_nodes[i]:
                pygame.draw.rect(screen, WEIGHTS_COLORS[i], pygame.Rect(node[0], node[1], SQUARE_SIZE, SQUARE_SIZE))

        # live-draw of working algorithm
        if available != None:
            for i in range(available.currentItemCount):
                node = available.items[i]
                if (node.x * SQUARE_SIZE, node.y * SQUARE_SIZE) not in {self.start_pos, self.end_pos}:
                    pygame.draw.rect(screen, AVAILABLE, pygame.Rect(node.x * SQUARE_SIZE, node.y * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        if color == None:
            color = PATHED
        if path != None:
            for node in path:
                if (node.x * SQUARE_SIZE, node.y * SQUARE_SIZE) not in {self.start_pos, self.end_pos}:
                    pygame.draw.rect(screen, color, pygame.Rect(node.x * SQUARE_SIZE, node.y * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

        # grid creation
        for x in range(0, WINDOW_SIZE[0] - SPACING + 1, SQUARE_SIZE):
            # horizontal lines
            pygame.draw.line(screen, color = (0,0,0), start_pos = (0, x), end_pos = (WINDOW_SIZE[0] - SPACING, x))
            # vertical lines
            pygame.draw.line(screen, color = (0,0,0), start_pos = (x, 0), end_pos = (x, WINDOW_SIZE[1]))


        # quick menu on the right side:
        # separating lines
        for y in range(0, WINDOW_SIZE[1], WINDOW_SIZE[1] // 10):
            pygame.draw.line(screen, color = SEPARATING_LINE, start_pos = (WINDOW_SIZE[0] - SPACING, y), end_pos = (WINDOW_SIZE[0], y))

        # weights-colors with black border + weights text next to them
        counter = 0
        for y in range(WINDOW_SIZE[1] // 40, WINDOW_SIZE[1], WINDOW_SIZE[1] // 10):
            text = font.render(f"Weight = {WEIGHTS[counter]}", False, SEPARATING_LINE, BG_COLOR)
            textRect = text.get_rect()
            textRect.center = (WINDOW_SIZE[0] - SPACING/2, y + WINDOW_SIZE[1] // 40)
            screen.blit(text, textRect)
            pygame.draw.rect(screen, WEIGHTS_COLORS[counter], pygame.Rect(WINDOW_SIZE[0] - SPACING + 10, y, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.rect(screen, (0,0,0), pygame.Rect(WINDOW_SIZE[0] - SPACING + 10, y, SQUARE_SIZE, SQUARE_SIZE), 2)
            counter += 1

        pygame.display.update()

# get neighbours with diagonals
def getNeighboursDiag(node, maze_nodes):
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

# get neighbours without diagonals
def getNeighboursNoDiag(node, maze_nodes):
    neighbours = []

    checkX = node.x
    checkY = node.y - 1
    if (checkX >= 0 and checkX < ARRAY_SIZE[0]) and (checkY >= 0 and checkY < ARRAY_SIZE[1]):
        neighbours.append(maze_nodes[checkX][checkY])

    checkX = node.x
    checkY = node.y + 1
    if (checkX >= 0 and checkX < ARRAY_SIZE[0]) and (checkY >= 0 and checkY < ARRAY_SIZE[1]):
        neighbours.append(maze_nodes[checkX][checkY])
    
    checkX = node.x - 1
    checkY = node.y
    if (checkX >= 0 and checkX < ARRAY_SIZE[0]) and (checkY >= 0 and checkY < ARRAY_SIZE[1]):
        neighbours.append(maze_nodes[checkX][checkY])
    
    checkX = node.x + 1
    checkY = node.y
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

    return path

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
                # if event is number being pressed => number = weight and user is choosing weighted nodes
                # based on the number that has been pressed
                if event.unicode.isdigit():
                    weight = int(event.unicode)
                    maze.state = "choosing_weights"

            if event.type == pygame.MOUSEBUTTONDOWN:
                if maze.x < WINDOW_SIZE[0] - SPACING:
                    if maze.state == "choosing_start_pos":
                            maze.start_pos = (maze.x // SQUARE_SIZE * SQUARE_SIZE, maze.y // SQUARE_SIZE * SQUARE_SIZE)
                    if maze.state == "choosing_end_pos":
                            maze.end_pos = (maze.x // SQUARE_SIZE * SQUARE_SIZE, maze.y // SQUARE_SIZE * SQUARE_SIZE)
                    if maze.state == "creating_obstacles":
                        if (maze.x // SQUARE_SIZE * SQUARE_SIZE, maze.y // SQUARE_SIZE * SQUARE_SIZE) not in {maze.start_pos, maze.end_pos}:
                            maze.walls.append((maze.x // SQUARE_SIZE * SQUARE_SIZE , maze.y // SQUARE_SIZE * SQUARE_SIZE))
                    if maze.state == "choosing_weights":
                        if (maze.x // SQUARE_SIZE * SQUARE_SIZE, maze.y // SQUARE_SIZE * SQUARE_SIZE) not in {maze.start_pos, maze.end_pos}:
                            maze.special_nodes[weight].append((maze.x // SQUARE_SIZE * SQUARE_SIZE , maze.y // SQUARE_SIZE * SQUARE_SIZE))

        if maze.state == 'ready':
            # path finding
            maze_nodes = np.empty((ARRAY_SIZE), dtype = Node)

            # creating grid of nodes
            for x in range(int((WINDOW_SIZE[0] - SPACING) / SQUARE_SIZE)):
                for y in range(int(WINDOW_SIZE[1] / SQUARE_SIZE)):
                    for i in range(len(WEIGHTS)):
                        if (x*SQUARE_SIZE,y*SQUARE_SIZE) in maze.special_nodes[i]:
                            maze_nodes[x][y] = Node(coordinates = (x,y), walkable = True, weight = i + 1)
                    if (x*SQUARE_SIZE,y*SQUARE_SIZE) == maze.start_pos:
                        start_node = Node((x,y), walkable = True)
                        maze_nodes[x][y] = start_node
                    elif (x*SQUARE_SIZE,y*SQUARE_SIZE) == maze.end_pos:
                        target_node = Node((x,y), walkable = True)
                        maze_nodes[x][y] = target_node
                    elif (x*SQUARE_SIZE,y*SQUARE_SIZE) in maze.walls:
                        maze_nodes[x][y] = Node(coordinates = (x,y), walkable = False)
                    else:
                        maze_nodes[x][y] = Node(coordinates = (x,y), walkable = True)

            # list of nodes to process, starting with start_node
            open_set = Heap(ARRAY_SIZE[0] * ARRAY_SIZE[1])
            open_set.add(start_node)
            # list of nodes that have been already processed
            closed_set = []

            while open_set.currentItemCount > 0:
                current_node = open_set.removeFirst()
                closed_set.append(current_node)

                if current_node == target_node:
                    final_path = getPath(start_node, target_node)
                    maze.draw(available = None, path = final_path, color = FINAL_PATH)
                    time.sleep(5)
                    quit()

                for neighbour in getNeighboursDiag(current_node, maze_nodes):
                    if not neighbour.walkable or neighbour in closed_set:
                        continue

                    newCostToNeighbour = current_node.G_cost + getDistance(current_node, neighbour)
                    if (newCostToNeighbour < neighbour.G_cost) or (not open_set.contains(neighbour)):
                        neighbour.G_cost = newCostToNeighbour
                        neighbour.H_cost = getDistance(neighbour, target_node)
                        neighbour.parent = current_node

                        if not open_set.contains(neighbour):
                            open_set.add(neighbour)
                            maze.draw(open_set, closed_set)
                            time.sleep(1/SPEED)

        else:
            maze.draw()