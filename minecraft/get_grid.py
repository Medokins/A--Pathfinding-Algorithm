from mcpi.minecraft import Minecraft
import mcpi.block as block
import numpy as np

from minecraft_settings import *

mc = Minecraft.create()
x, y, z = mc.player.getPos()

# if facing east it will create paramiter to the east and south of current position
if set_paramiter:
    mc.setBlocks(x, y - 1, z, x + LENGHT, y - 1 + HEIGHT, z + WIDTH, block.AIR.id)
    mc.setBlocks(x, y - 1, z, x + LENGHT, y, z + WIDTH, block.STONE.id)
else:
    mc.player.setPos(x, y + 1, z)

grid_start = (x, y - 1 - HEIGHT, z)
grid_end = (x + LENGHT, y - 1 + HEIGHT, z + WIDTH)
grid_blocks = mc.getBlocks(grid_start, grid_end)

blocks = [block for block in grid_blocks]

if HEIGHT == 0:
    grid = np.resize(blocks, (LENGHT, WIDTH))
else:
    grid = np.resize(blocks, (HEIGHT * 2, LENGHT, WIDTH))
    
print(grid)