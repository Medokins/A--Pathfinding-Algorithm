from mcpi.minecraft import Minecraft
from minecraft_settings import PATH
import numpy as np
import sys
import os

main_path = os.path.abspath(__file__)
sys.path.append(os.path.join(main_path, "..", ".."))
from maze import runMaze, get_instructions

mc = Minecraft.create()
path = runMaze()

x, y, z = mc.player.getPos()
x = np.floor(x)
y = np.floor(y)
z = np.floor(z)
mc.player.setPos(x + 0.5, y + 1, z + 0.5)

y -= 1

for move in get_instructions(path):
    if move == "R": z += 1
    elif move == "L": z -= 1
    elif move == "B": x -= 1
    elif move == "F": x += 1
    elif move == "U": y += 1
    elif move == "D": y -= 1
    else:
        print("Unknown instruction")
    mc.setBlock(x, y, z, PATH)
