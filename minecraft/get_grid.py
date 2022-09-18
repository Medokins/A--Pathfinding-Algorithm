from mcpi.minecraft import Minecraft
import mcpi.block as block
import numpy as np
import pandas as pd
import os

from minecraft_settings import *
from get_blocks import get_blocks

#run this file from project's main directory not from minecraft directory!
mc = Minecraft.create()
x, y, z = mc.player.getPos()
maze_3d_name = "big_3d_maze"
maze_2d_name = "minecraft_maze"

# if facing east it will create paramiter to the east and south of current position
if set_paramiter:
    mc.setBlocks(x, y - 1, z, x + LENGHT - 1, y - 1 + HEIGHT, z + WIDTH -1 , block.AIR.id)
    mc.setBlocks(x, y - 1, z, x + LENGHT - 1, y - 1, z + WIDTH - 1, block.STONE.id)
else:
    x = np.floor(x)
    y = np.floor(y)
    z = np.floor(z)
    mc.player.setPos(x + 0.5, y + 1, z + 0.5)

grid_start = (int(x),int(y - 1), int(z))
grid_end = (int(x + LENGHT), int(y + HEIGHT), int(z + WIDTH))
grid_blocks = get_blocks(grid_start, grid_end)
# sorting because of multithreading, bias for sorting mazes up to BIAS x BIAS size
grid_blocks = dict(sorted(grid_blocks.items(), key=lambda x: x[0][1]*BIAS + x[0][0]))

grid = []
for item in grid_blocks:
    grid.append(grid_blocks[item])

grid = np.resize(grid, (HEIGHT + 1, LENGHT, WIDTH))
# flipping by x axis
for i in range(len(grid)):
    grid[i] = np.flip(grid[i],0)

if HEIGHT > 1:
    try:
        os.mkdir(os.path.join("3d_mazes", maze_3d_name))     
    except FileExistsError:
        print("Directory with that name already exists")

start_node = None
target_node = None
layer_counter = 0
for layer in grid:
    df = pd.DataFrame(index=range(LENGHT), columns=range(WIDTH))
    row_counter = 0
    for row in layer:
        block_counter = 0
        for block_data in row:
            current_block = grid[layer_counter][row_counter][block_counter]
            # checking if block is AIR or not
            if current_block != 0:
                df[block_counter][row_counter] = '-'
            if current_block == 251:
                if mc.getBlockWithData(grid_start[0] + LENGHT - row_counter - 1, grid_start[1] + layer_counter, grid_start[2] + block_counter).data == 5:
                    df[block_counter][row_counter] = 'S'
                    start_node = (block_counter, row_counter)
                if mc.getBlockWithData(grid_start[0] + LENGHT - row_counter - 1, grid_start[1] + layer_counter, grid_start[2] + block_counter).data == 14:
                    df[block_counter][row_counter]= 'E'
                    target_node = (block_counter, row_counter)

            block_counter += 1
        row_counter += 1
    
    df.fillna(0, inplace=True)
    if HEIGHT > 1:
        df.to_csv(os.path.join("3d_mazes", maze_3d_name, f"layer_{layer_counter}.csv"))
    else:
         df.to_csv(os.path.join("saved_mazes", f"{maze_2d_name}.csv"))
    layer_counter += 1