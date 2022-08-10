from mcpi.minecraft import Minecraft
import numpy as np
import pydirectinput
import time

mc = Minecraft.create()
mc.player.setPos(0.5, 81, 0.5)
# margin was tested in range 0 - 1, with 0.001 step and this is the closest one
margin = 0.545

for distance in range(1, 50):
    # set correct rotation
    while True:
        # different rotation is based on screen size for some reason
        if np.ceil(mc.player.getRotation()) in {-90, 270}:
            break
        pydirectinput.moveRel(-1)

    pydirectinput.keyDown("w")
    while mc.player.getPos().x < distance + 0.5 - margin:
        pass
    pydirectinput.keyUp("w")
    time.sleep(1.5)
    print(f"For margin = {margin} after stopping {mc.player.getPos().x} off perfect (distance: {distance}): {distance + 0.5 - mc.player.getPos().x}")
    time.sleep(1.5)
    mc.player.setPos(0.5, 81, 0.5)