from mcpi.minecraft import Minecraft
import mcpi.block as block
import numpy as np
import pandas as pd
import os

from minecraft_settings import *

def build_maze(file_name, clear_area = False):
    try:
        file = os.path.join("saved_mazes", f"{file_name}.csv")
        df = pd.read_csv(file)
        df.drop("Unnamed: 0", axis = 1, inplace=True)
        df.columns = range(df.columns.size)
    except:
        print(f"Import Error: there is no file named: {file_name}.csv in saved_mazes directory")
        quit()

    mc = Minecraft.create()
    x, y, z = mc.player.getPos()

    # preparing area for maze
    if clear_area:
        mc.setBlocks(x, y - 1, z, x + df.shape[0], y + 2, z + df.shape[1], block.AIR.id)
        mc.setBlocks(x, y - 1, z, x + df.shape[0], y - 1, z + df.shape[1], block.STONE.id)

    player_x = np.floor(x)
    player_y = np.floor(y)
    player_z = np.floor(z)
    mc.player.setPos(player_x + 0.5, player_y + 1, player_z + 0.5)

    for z in range(df.shape[1]):
        for x in range(df.shape[0]):
            character = df[z][x]
            if character == "S":
                mc.setBlock(player_x + df.shape[1] - x - 1, player_y - 1, player_z + z, START)
                mc.player.setPos(player_x + df.shape[1] - x - 0.5, player_y + 1, player_z + z)
            elif character == "E":
                mc.setBlock(player_x + df.shape[1] - x - 1, player_y - 1, player_z + z, END)
            elif character == "-":
                mc.setBlock(player_x + df.shape[1] - x - 1, player_y, player_z + z, WALL)
                mc.setBlock(player_x + df.shape[1] - x - 1, player_y + 1, player_z + z, WALL)
            else:
                character = int(character)
                if character != 0:
                    print(f"Specia; at: {z,x} with weight {character}")

build_maze("bot_maze",  clear_area = True)