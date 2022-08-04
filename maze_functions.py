from settings import *
import numpy as np
import pandas as pd
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

# function that returns start_pos, target_pos, walls array, special_nodes 2d array (in that order)
def decode_maze(file_name):
    try:
        file = os.path.join("saved_mazes", f"{file_name}.csv")
        df = pd.read_csv(file)
        df.drop("Unnamed: 0", axis = 1, inplace=True)
        df.columns = range(df.columns.size)
    except:
        print(f"Import Error: there is no file named: {file_name}.csv in saved_mazes directory")
        quit()

    start_pos = None
    target_pos = None
    walls = []
    special_nodes = [[] for _ in range(len(WEIGHTS))]

    for x in range(df.shape[1]):
        for y in range(df.shape[0]):
            character = df[x][y]
            if character == "S":
                start_pos = (x*SQUARE_SIZE,y*SQUARE_SIZE)
            elif character == "E":
                target_pos = (x*SQUARE_SIZE,y*SQUARE_SIZE)
            elif character == "-":
                walls.append((x*SQUARE_SIZE,y*SQUARE_SIZE))
            else:
                # had to do this bcs for some reason some zeros where strings
                character = int(character)
                if character != 0:
                    special_nodes[WEIGHTS.index(character)].append((x*SQUARE_SIZE,y*SQUARE_SIZE))
        
    return start_pos, target_pos, walls, special_nodes