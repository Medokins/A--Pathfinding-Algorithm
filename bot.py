from maze import runMaze

# if you want to draw your own maze, leave maze_file as None:
# maze_file = None

path = runMaze()

for node in path:
    print(node.x, node.y)