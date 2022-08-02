from settings import *
import numpy as np
import os

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

# function that returns start_pos, target_pos, walls array, special_nodes 2d array (in that order!)
def decode_maze(file_name):
    start_pos = None
    target_pos = None
    walls = []
    special_nodes = [[] for _ in range(len(WEIGHTS))]
    print(special_nodes)

    file = os.path.join("saved_mazes", f"{file_name}.csv")

decode_maze("maze_1")