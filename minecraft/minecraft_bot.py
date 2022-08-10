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
# set correct rotation
while True:
        # different rotation is based on screen size for some reason
        if np.ceil(mc.player.getRotation()) in {-90, 270}:
            break
        pydirectinput.moveRel(-1)
delay = 1.5

def moveRight(distance):
    start_z_pos = mc.player.getPos().z
    pydirectinput.keyDown("d")
    while mc.player.getPos().z < start_z_pos + distance - MARGIN:
        pass
    pydirectinput.keyUp("d")
    time.sleep(delay)

def moveLeft(distance):
    start_z_pos = mc.player.getPos().z
    pydirectinput.keyDown("a")
    while mc.player.getPos().z > start_z_pos - distance + MARGIN:
        pass
    pydirectinput.keyUp("w")
    time.sleep(delay)

def moveDown(distance):
    start_x_pos = mc.player.getPos().x
    pydirectinput.keyDown("s")
    while mc.player.getPos().x > start_x_pos - distance + MARGIN:
        pass
    pydirectinput.keyUp("s")
    time.sleep(delay)

def moveUp(distance):
    start_x_pos = mc.player.getPos().x
    pydirectinput.keyDown("w")
    while mc.player.getPos().x < start_x_pos + distance - MARGIN:
        pass
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
    instruction, distance = getDistance(instructions)
    if instruction == 'R':
        moveRight(distance)
    elif instruction == 'L':
        moveLeft(distance)
    elif instruction == 'D':
        moveDown(distance)
    elif instruction == 'U':
        moveUp(distance)
    else:
        print("Unknown instruction")
        
    instructions = instructions[distance:]

x, y, z = mc.player.getPos()
mc.player.setPos(x, y + 25, z)