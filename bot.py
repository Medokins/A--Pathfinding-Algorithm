from maze import runMaze
from maze_functions import get_instructions
import pydirectinput as pdi

def moveRight():
    pass
def moveLeft():
    pass
def moveDown():
    pass
def moveUp():
    pass

path = runMaze()
instructions = get_instructions(path)

for instruction in instructions:
    if instruction == 'R':
        moveRight()
    elif instruction == 'L':
        moveLeft()
    elif instruction == 'D':
        moveDown()
    elif instruction == 'U':
        moveUp()
    else:
        print("Unknown instruction")