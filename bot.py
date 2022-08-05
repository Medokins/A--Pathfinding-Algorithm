from maze import runMaze
from maze_functions import get_instructions
import pydirectinput
import time

WALK_SPEED = 4.317

def moveRight(duration):
    pydirectinput.keyDown("d")
    time.sleep(duration/WALK_SPEED)
    pydirectinput.keyUp("d")
def moveLeft(duration):
    pydirectinput.keyDown("a")
    time.sleep(duration/WALK_SPEED)
    pydirectinput.keyUp("a")
def moveDown(duration):
    pydirectinput.keyDown("s")
    time.sleep(duration/WALK_SPEED)
    pydirectinput.keyUp("s")
def moveUp(duration):
    pydirectinput.keyDown("w")
    time.sleep(duration/WALK_SPEED)
    pydirectinput.keyUp("w")

path = runMaze()
instructions = get_instructions(path)
time.sleep(3)

# for smoother walk
def getDistance(instructions):
    counter = 0
    current_character = instructions[counter]

    if instructions[:-1] == instructions[1:]:
        return current_character, len(instructions)
    else:
        while current_character == instructions[counter]:
            counter += 1
        
    return current_character, counter

while len(instructions) > 0:
    instruction, duration = getDistance(instructions)

    if instruction == 'R':
        moveRight(duration)
    elif instruction == 'L':
        moveLeft(duration)
    elif instruction == 'D':
        moveDown(duration)
    elif instruction == 'U':
        moveUp(duration)
    else:
        print("Unknown instruction")
    
    instructions = instructions[duration:]
