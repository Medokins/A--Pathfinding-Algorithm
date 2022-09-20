# A* Pathfinding-Algorithm

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)
* [Additional info](#additional-info)

## General info
Implementation and visualisation of an A* pathfinding algorithm with weights both in 2d and 3d.

## Technologies
pygame - visualisation/maze creation in 2d.</br>
Minecraft - visualisation/maze creation in 3d.</br>
mcpi - acquiring minecraft data. (althought it's really slow on big scale, and I'm looking for something better)</br>
numpy - for faster maze_functions.</br>
pandas - for clear in-file quick visualisation and maze saving.</br>
pydirectinput - for bot movement in game (it's not 100% precise yet)</br>
multithreading socket stuffing algorithm writted mostly [Joseph Reynolds](https://github.com/joseph-reynolds) with my minor tweaks to work in python3. </br>

## Setup
If you want to play around with 2d version just get required libraries and start main.py script.
You'll be greeted with main menu where you can choose your actions:
<img src="./imgs/main_menu.png" alt="menu" style="width:100%;" />

If you want to connect with minecraft, play around with 3d version and also visualise final path (and maze) in game
you'll need to download mcpi server and connect to "localhost" in direct connect in Minecraft menu. ([quick tutorial on this](https://www.youtube.com/watch?v=N6fm11LFUvk&ab_channel=Codeboosh))
<img src="./imgs/server.png" alt="server connect" style="width:100%;" />

## Additional info
Pressing said keys will trigger event stated to the right of it, pressing "I" (importing exising maze) will take you
to a screen with prompt box that'll be highlighted green once you click it, in here you can write existing in saved_mazes
file name (without extention)
<img src="./imgs/import_prompt.png" alt="import_prompt" style="width:100%;" />

if you write name of 3d maze it will automatically start 3d pathfinding but it has no visualization for it in pygame, so just press enter
after some time to see path directions printed onto console or built in minecraft. </br>
<img src="./imgs/3d_maze.png" alt="import_prompt_3d" style="width:100%;" />
Console output:
<img src="./imgs/console_output.png" alt="3d_maze_output" style="width:100%;" />
Where U is Up (in 3d space), D is Down (in 3d space), R is Righ, L is Left, F is front (it's like up when looking in 2d space) and B is back (it's like down when working in 2d space)

Drawing maze is done with keys shown in menu, you can choose between normal pathfinding and no-diagonal one (used to move around in minecraft)</br>
"big_maze" file with normal pathfinding:</br>
<img src="./imgs/maze.png" alt="exemplary maze" style="width:100%;" />

"big_maze" file with no_diagonals pathfinding:</br>
<img src="./imgs/no_diagonals.png" alt="exemplary maze without diagonals" style="width:100%;" />

Finally, you can change square_size when creating your own mazes in settings file, as well as changing LIVE_VIEW option to True if you want
to see algorithm working live, looking for shortest path and updating all the nodes accordingly.</br>
<img src="./imgs/settings.png" alt="settings file" style="width:100%;" />
PS. You can also change weights values and colors as you like.</br></br>

On the last note:</br>
2D version is working flawlessly, 3D pathfinding algorithm works great, but gathering data from Minecraft on a big scale is troubling, since it gives different values each time </br>
it is run with the same get_grid() function (it is most likely due to multithreading and mc server not keeping up). I might try to read into that in the future, but for now I'm leaving this working version as it is.