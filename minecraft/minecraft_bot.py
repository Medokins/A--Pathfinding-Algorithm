from mcpi.minecraft import Minecraft
import time
import os
import sys
import pydirectinput
import numpy as np

from minecraft_settings import MARGIN
main_path = os.path.abspath(__file__)
sys.path.append(os.path.join(main_path, "..", ".."))
from maze import runMaze, get_instructions

path = runMaze()
instructions = get_instructions(path)

time.sleep(3)
mc = Minecraft.create()
x, y, z = mc.player.getPos()
x = np.floor(x)
y = np.floor(y)
z = np.floor(z)
mc.player.setPos(x + 0.5, y + 1, z + 0.5)
time.sleep(3)
delay = 0.1

def moveRight(duration):
    margin = MARGIN if duration >= 2 else 0.2
    z = mc.player.getPos().z
    print(f"z destination: {z + duration}")
    while mc.player.getPos().z < np.floor(z + duration) - margin:
        pydirectinput.keyDown("d")
    pydirectinput.keyUp("d")
    time.sleep(delay)

def moveLeft(duration):
    margin = MARGIN if duration >= 1 else 0
    z = mc.player.getPos().z
    print(f"z destination: {z - duration}")
    while mc.player.getPos().z > np.ceil(z - duration) + margin:
        pydirectinput.keyDown("a")
    pydirectinput.keyUp("a")
    time.sleep(delay)


def moveDown(duration):
    margin = MARGIN if duration >= 1 else 0
    x = mc.player.getPos().x
    print(f"x destination: {np.ceil(x - duration)}")
    while mc.player.getPos().x > np.ceil(x - duration) + margin:
        pydirectinput.keyDown("s")
    pydirectinput.keyUp("s")
    time.sleep(delay)

def moveUp(duration):
    margin = MARGIN if duration >= 1 else 0
    x = mc.player.getPos().x
    print(f"x destination: {np.floor(x + duration)}")
    while mc.player.getPos().x < np.floor(x + duration) - margin:
        pydirectinput.keyDown("w")
    pydirectinput.keyUp("w")
    time.sleep(delay)

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

x, y, z = mc.player.getPos()
mc.player.setPos(x, y + 25, z)