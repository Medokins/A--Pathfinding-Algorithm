from settings import *
import numpy as np
import pandas as pd
import os

def get_settings_square_size():
    return SQUARE_SIZE

# get neighbours with diagonals on a 2d grid
def getNeighboursDiag(node, maze_nodes, array_size):
    neighbours = []
    for x in range(-1, 2):
        for y in range(-1, 2):
            if x == 0 and y == 0:
                pass
            else:
                checkX = node.x + x
                checkY = node.y + y
                if (checkX >= 0 and checkX < array_size[1]) and (checkY >= 0 and checkY < array_size[2]):
                    neighbours.append(maze_nodes[0][checkX][checkY])
    return neighbours

# get neighbours without diagonals IN PROGRESS FOR NOW DUE TO 3D CHANGE
def getNeighboursNoDiag(node, maze_nodes, array_size):
    neighbours = []
    addition = [0,0]
    numbers = [-1,1]
    for i in range(2):
        for number in numbers:
            addition[i] = number
            checkX, checkY = np.add([node.x, node.y], addition)
            addition = [0,0]
            if (checkX >= 0 and checkX < array_size[1]) and (checkY >= 0 and checkY < array_size[2]):
                neighbours.append(maze_nodes[0][checkX][checkY])
    return neighbours

# used with 3d pathfinding
def getNeighbours3d(node, maze_nodes, array_size):
    neighbours = []
    addition = [0,0,0]
    numbers = [-1,1]
    for i in range(3):
        for number in numbers:
            addition[i] = number
            checkX, checkY, checkZ = np.add([node.x, node.y, node.z], addition)
            addition = [0,0,0]
            if (checkZ >= 0 and checkZ < array_size[0]) and (checkX >= 0 and checkX < array_size[1]) and (checkY >= 0 and checkY < array_size[2]):
                neighbours.append(maze_nodes[checkZ][checkX][checkY])

    return neighbours

def getDistance(nodeA, nodeB):
    distance_x = np.abs(nodeA.x - nodeB.x)
    distance_y = np.abs(nodeA.y - nodeB.y)
    disntace_z = np.abs(nodeA.z - nodeB.z)
    if distance_x > distance_y:
        return 14 * distance_y + 10 * (distance_x - distance_y) + 10 * disntace_z
    else:
        return 14 * distance_x + 10 * (distance_y - distance_x) + 10 * disntace_z


def getPath(startNode, endNode):
    path = []
    current_node = endNode
    while current_node != startNode:
        path.append(current_node)
        current_node = current_node.parent
    path.append(startNode)
    path.reverse()
    return path

# function that returns start_pos, target_pos, walls array, special_nodes 2d array (in that order)
def decode_maze(file_name):
    layers = 1
    try:
        file = os.path.join("saved_mazes", f"{file_name}.csv")
        df = pd.read_csv(file)
        df.drop("Unnamed: 0", axis = 1, inplace=True)
        df.columns = range(df.columns.size)
    except:
        try:
            directory = os.path.join("3d_mazes", file_name)
            layers = len([entry for entry in os.listdir(directory) if os.path.isfile(os.path.join(directory, entry))])
            df = pd.read_csv(os.path.join("3d_mazes", file_name, "layer_0.csv"))
            df.drop("Unnamed: 0", axis = 1, inplace=True)
            df.columns = range(df.columns.size)
        except:
            print(f"Import Error: There is no file named: {file_name}.csv in saved_mazes directory nor there is no directory named: {file_name} in 3d_mazes directory")
            quit()

    start_pos = None
    target_pos = None
    walls = []
    special_nodes = [[] for _ in range(len(WEIGHTS))]
    square_size = WINDOW_SIZE[1] // df.shape[1]

    for z in range(layers):
        if layers > 1:
            df = pd.read_csv(os.path.join("3d_mazes", file_name, f"layer_{z}.csv"))
            df.drop("Unnamed: 0", axis = 1, inplace=True)
            df.columns = range(df.columns.size)
        for x in range(df.shape[1]):
            for y in range(df.shape[0]):
                character = df[x][y]
                if character == "S":
                    start_pos = (x*square_size,y*square_size,z)
                elif character == "E":
                    target_pos = (x*square_size,y*square_size,z)
                elif character == "-":
                    walls.append((x*square_size,y*square_size,z))
                else:
                    # had to do this bcs for some reason some zeros where strings
                    character = int(character)
                    if character != 0:
                        special_nodes[WEIGHTS.index(character)].append((x*square_size,y*square_size,z))

    return start_pos, target_pos, walls, special_nodes, df.shape, layers

def get_instructions(path):
    # R - right, L - left, B - back, F - front, U - up, D -  down
    instructions = []
    current_node = path[0]
    for next_node in path[1:]:
        # go right
        if next_node.x > current_node.x:
            instructions.append('R')
        # go left
        elif next_node.x < current_node.x:
            instructions.append('L')
        # go back
        elif next_node.y > current_node.y:
            instructions.append('B')
        # go front
        elif next_node.y < current_node.y:
            instructions.append('F')
        # go up
        elif next_node.z > current_node.z:
            instructions.append('U')
        # go down
        elif next_node.z < current_node.z:
            instructions.append('D')

        current_node = next_node

    return instructions