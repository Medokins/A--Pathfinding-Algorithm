from maze import runMaze
from maze_functions import get_instructions

if __name__ == "__main__":
    path = runMaze()
    for move in get_instructions(path):
        print(move, end = " | ")