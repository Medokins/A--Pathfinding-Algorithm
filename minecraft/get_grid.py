from mcpi.minecraft import Minecraft
import mcpi.block as block
import numpy as np
import pandas as pd
import os

from minecraft_settings import *

mc = Minecraft.create()
x, y, z = mc.player.getPos()

# if facing east it will create paramiter to the east and south of current position
if set_paramiter:
    mc.setBlocks(x, y - 1, z, x + LENGHT, y - 1 + HEIGHT, z + WIDTH, block.AIR.id)
    mc.setBlocks(x, y - 1, z, x + LENGHT, y, z + WIDTH, block.STONE.id)
else:
    x = np.floor(x)
    y = np.floor(y)
    z = np.floor(z)
    mc.player.setPos(x + 0.5, y + 1, z + 0.5)

grid_start = (x, y - 1, z)
grid_end = (x + LENGHT, y - 1 + HEIGHT, z + WIDTH)

grid_blocks = []

# outer loop for layers
for y in range(HEIGHT + 1):
    # now 2d grids
    for x in range(LENGHT):
        for z in range(WIDTH):
            grid_blocks.append(mc.getBlock(grid_start[0] + x, grid_start[1] + y, grid_start[2] + z))

grid = np.resize(grid_blocks, (HEIGHT + 1, LENGHT, WIDTH))

start_node = None
end_node = None
layer_counter = 0

df = pd.DataFrame(index=range(LENGHT), columns=range(WIDTH))

for layer in grid:
    row_counter = 0
    for row in layer:
        block_counter = 0
        for block_data in row:
            if block_data == 251:
                if mc.getBlockWithData(grid_start[0] + row_counter, grid_start[1] + layer_counter, grid_start[2] + block_counter).data == 5:
                    df[block_counter][LENGHT - row_counter - 1] = 'S'
                elif mc.getBlockWithData(grid_start[0] + row_counter, grid_start[1] + layer_counter, grid_start[2] + block_counter).data == 14:
                    df[block_counter][LENGHT - row_counter - 1] = 'E'
                elif mc.getBlockWithData(grid_start[0] + row_counter, grid_start[1] + layer_counter, grid_start[2] + block_counter).data == 15:
                    df[block_counter][LENGHT - row_counter - 1] = '-'
            block_counter += 1
        row_counter += 1
    layer_counter += 1

df.fillna(0, inplace=True)
df.to_csv(os.path.join("saved_mazes", "minecraft_maze.csv"))