import pygame
import time

from node import Node
from heap import Heap
from maze_functions import *

pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Maze Creator")

class Maze:
    def __init__(self):
        # mouse position
        self.x = 0
        self.y = 0

        # state
        self.state = 'choosing'

        # dragin variables
        self.wall_draging = False
        self.obstacle_draging = False

        # maze variables
        self.start_pos = None
        self.target_pos = None
        self.walls = []
        self.special_nodes = [[] for _ in range(len(WEIGHTS))]

    def draw(self, available = None, path = None, color = None, save = False):
        # set color to bg of maze
        screen.fill(BG_COLOR)
        font = pygame.font.SysFont('Calibri', 24)

        if self.start_pos != None:
            pygame.draw.rect(screen, START, pygame.Rect(self.start_pos[0], self.start_pos[1], SQUARE_SIZE, SQUARE_SIZE))
        if self.target_pos != None:
            pygame.draw.rect(screen, END, pygame.Rect(self.target_pos[0], self.target_pos[1], SQUARE_SIZE, SQUARE_SIZE))
        for wall in self.walls:
            pygame.draw.rect(screen, WALL, pygame.Rect(wall[0], wall[1], SQUARE_SIZE, SQUARE_SIZE))

        for i in range(len(WEIGHTS)):
            for node in self.special_nodes[i]:
                pygame.draw.rect(screen, WEIGHTS_COLORS[i], pygame.Rect(node[0], node[1], SQUARE_SIZE, SQUARE_SIZE))

        # live-draw of working algorithm
        if available != None:
            for i in range(available.currentItemCount):
                node = available.items[i]
                if (node.x * SQUARE_SIZE, node.y * SQUARE_SIZE) not in {self.start_pos, self.target_pos}:
                    pygame.draw.rect(screen, AVAILABLE, pygame.Rect(node.x * SQUARE_SIZE, node.y * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        if color == None:
            color = PATHED
        if path != None:
            for node in path:
                if (node.x * SQUARE_SIZE, node.y * SQUARE_SIZE) not in {self.start_pos, self.target_pos}:
                    pygame.draw.rect(screen, color, pygame.Rect(node.x * SQUARE_SIZE, node.y * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

        # grid creation
        for x in range(0, WINDOW_SIZE[0] - SPACING + 1, SQUARE_SIZE):
            # horizontal lines
            pygame.draw.line(screen, color = (0,0,0), start_pos = (0, x), end_pos = (WINDOW_SIZE[0] - SPACING, x))
            # vertical lines
            pygame.draw.line(screen, color = (0,0,0), start_pos = (x, 0), end_pos = (x, WINDOW_SIZE[1]))


        # quick menu on the right side:
        # separating lines
        for y in range(0, WINDOW_SIZE[1], WINDOW_SIZE[1] // 10):
            pygame.draw.line(screen, color = SEPARATING_LINE, start_pos = (WINDOW_SIZE[0] - SPACING, y), end_pos = (WINDOW_SIZE[0], y))

        # weights-colors with black border + weights text next to them
        counter = 0
        for y in range(WINDOW_SIZE[1] // 40, WINDOW_SIZE[1], WINDOW_SIZE[1] // 10):
            text = font.render(f"Weight = {WEIGHTS[counter]}", False, SEPARATING_LINE, BG_COLOR)
            textRect = text.get_rect()
            textRect.center = (WINDOW_SIZE[0] - SPACING/2, y + WINDOW_SIZE[1] // 40)
            screen.blit(text, textRect)
            pygame.draw.rect(screen, WEIGHTS_COLORS[counter], pygame.Rect(WINDOW_SIZE[0] - SPACING + 10, y, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.rect(screen, (0,0,0), pygame.Rect(WINDOW_SIZE[0] - SPACING + 10, y, SQUARE_SIZE, SQUARE_SIZE), 2)
            counter += 1

        if save:
            input_box = pygame.Rect((WINDOW_SIZE[0] - 600)/2, (WINDOW_SIZE[1] - 200)/2, 600, 100)
            color = INACTIVE_COLOR
            active = False
            text = ''
            done = False

            while not done:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        done = True
                        return text
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if input_box.collidepoint(event.pos):
                            active = not active
                        else:
                            active = False
                        color = ACTIVE_COLOR if active else INACTIVE_COLOR
                    if event.type == pygame.KEYDOWN:
                        if active:
                            if event.key == pygame.K_RETURN:
                                done = True
                                return text
                            elif event.key == pygame.K_BACKSPACE:
                                text = text[:-1]
                            else:
                                text += event.unicode

                screen.fill(SAVING_BG_COLOR)

                header = font.render("Enter file name: ", True, INACTIVE_COLOR, SAVING_BG_COLOR)
                headerRect = header.get_rect()
                headerRect.center = ((WINDOW_SIZE[0] - 600)/2 + 90,  (WINDOW_SIZE[1] - 200)/2 - 25)
                screen.blit(header, headerRect)
                
                font = pygame.font.Font(None, 32)
                txt_surface = font.render(text, True, color)
                width = max(600, txt_surface.get_width()+10)
                input_box.w = width
                screen.blit(txt_surface, ((WINDOW_SIZE[0] - 600)/2 + 10, (WINDOW_SIZE[1] - 200)/2 + 35))
                pygame.draw.rect(screen, color, input_box, 2)
                pygame.display.flip()


        pygame.display.update()

def runMaze(maze_file = None):
    ######################################################## maze creation
    maze = Maze()
    while maze.state != 'end':
        if maze_file == None:
            maze.x, maze.y = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    maze.state = 'end'
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        if maze.start_pos != None and maze.target_pos != None:
                            maze.state = 'ready'
                    if event.key == pygame.K_s:
                        maze.state = "choosing_start_pos"
                    if event.key == pygame.K_e:
                        maze.state = "choosing_target_pos"
                    if event.key == pygame.K_w:
                        if maze.state == "creating_obstacles":
                            maze.state = "passive"
                        else:
                            maze.state = "creating_obstacles"
                    if event.key == pygame.K_d:
                        maze.state = "deleting"
                        
                    # if event is number being pressed => number = weight and user is choosing weighted nodes
                    # based on the number that has been pressed
                    if event.unicode.isdigit():
                        if maze.state == "choosing_weights":
                            maze.state = "passive"
                        else:
                            weight = int(event.unicode)
                            maze.state = "choosing_weights"
                
                if maze.x < WINDOW_SIZE[0] - SPACING:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if maze.state == "choosing_start_pos":
                                maze.start_pos = (maze.x // SQUARE_SIZE * SQUARE_SIZE, maze.y // SQUARE_SIZE * SQUARE_SIZE)
                        if maze.state == "choosing_target_pos":
                                maze.target_pos = (maze.x // SQUARE_SIZE * SQUARE_SIZE, maze.y // SQUARE_SIZE * SQUARE_SIZE)

                    elif event.type == pygame.MOUSEMOTION:
                        if maze.state == "creating_obstacles":
                            if (maze.x // SQUARE_SIZE * SQUARE_SIZE, maze.y // SQUARE_SIZE * SQUARE_SIZE) not in {maze.start_pos, maze.target_pos}:
                                maze.walls.append((maze.x // SQUARE_SIZE * SQUARE_SIZE , maze.y // SQUARE_SIZE * SQUARE_SIZE))
                        if maze.state == "choosing_weights":
                            # row in my 2d array is corresponding to weight of given node
                            if (maze.x // SQUARE_SIZE * SQUARE_SIZE, maze.y // SQUARE_SIZE * SQUARE_SIZE) not in {maze.start_pos, maze.target_pos}:
                                maze.special_nodes[weight].append((maze.x // SQUARE_SIZE * SQUARE_SIZE , maze.y // SQUARE_SIZE * SQUARE_SIZE)) 
                        if maze.state == "deleting":
                            node = (maze.x // SQUARE_SIZE * SQUARE_SIZE, maze.y // SQUARE_SIZE * SQUARE_SIZE)
                            if node in maze.walls:
                                maze.walls.remove(node)
                            try:
                                if node in maze.special_nodes[weight]:
                                    maze.special_nodes[weight].remove(node)
                            # Weight variable was not chosen yet
                            except:
                                pass
        else:
            # in progress
            maze.start_pos, maze.target_pos, maze.walls, maze.special_nodes = decode_maze(maze_file)
            maze.state = 'ready'
        
        if maze.state == 'ready':
            # path finding
            maze_nodes = np.empty((ARRAY_SIZE), dtype = Node)

            # creating grid of nodes
            for x in range(int((WINDOW_SIZE[0] - SPACING) / SQUARE_SIZE)):
                for y in range(int(WINDOW_SIZE[1] / SQUARE_SIZE)):
                    # because when reading from file indexes are automatically correct
                    check = (x*SQUARE_SIZE,y*SQUARE_SIZE)

                    if check == maze.start_pos:
                        start_node = Node((x,y), walkable = True)
                        maze_nodes[x][y] = start_node
                    elif check == maze.target_pos:
                        target_node = Node((x,y), walkable = True)
                        maze_nodes[x][y] = target_node
                    elif check in maze.walls:
                        maze_nodes[x][y] = Node(coordinates = (x,y), walkable = False)
                    else:
                        maze_nodes[x][y] = Node(coordinates = (x,y), walkable = True)
                    for i in range(len(WEIGHTS)):
                        if check in maze.special_nodes[i]:
                            maze_nodes[x][y] = Node(coordinates = (x,y), walkable = True, weight = WEIGHTS[i])

            # list of nodes to process, starting with start_node
            open_set = Heap(ARRAY_SIZE[0] * ARRAY_SIZE[1])
            open_set.add(start_node)
            # list of nodes that have been already processed
            closed_set = []

            while open_set.currentItemCount > 0:
                current_node = open_set.removeFirst()
                closed_set.append(current_node)

                if current_node == target_node:
                    final_path = getPath(start_node, target_node)
                    maze.draw(available = None, path = final_path, color = FINAL_PATH)
                    while True:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                return final_path

                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_s:
                                    name = maze.draw(save=True)
                                    df = pd.DataFrame(index=range(ARRAY_SIZE[0]), columns=range(ARRAY_SIZE[1]))
                                    for x in range(ARRAY_SIZE[0]):
                                        for y in range(ARRAY_SIZE[1]):
                                            # if it's not a wall => it's walkable => check if it has weight to it
                                            # else, mark wall as "-" (for better visualisation in dataframe)
                                            if maze_nodes[x][y].walkable:
                                                df[x][y] = int(maze_nodes[x][y].weight)
                                            #print(f"Column {node.x}, Row {node.y}, Walkable: {node.walkable}, Weight {node.weight}")
                                            else:
                                                df[x][y] = "-"

                                    # at the end, override start_pos and target_pos with S and E accordingly
                                    df[start_node.x][start_node.y] = "S"
                                    df[target_node.x][target_node.y] = "E"

                                    df.columns = [f"|{i:03}|" for i in range(ARRAY_SIZE[0])]
                                    df.index = [f"|{i:03}|" for i in range(ARRAY_SIZE[1])]
                                    df.to_csv(os.path.join("saved_mazes", f"{name}.csv"))

                                    pygame.quit()
                                    return final_path

                                if event.key == pygame.K_q:
                                    pygame.quit()
                                    return final_path



                for neighbour in getNeighboursDiag(current_node, maze_nodes):
                    if not neighbour.walkable or neighbour in closed_set:
                        continue
                    
                    newCostToNeighbour = current_node.G_cost + getDistance(current_node, neighbour) + neighbour.weight
                    if (newCostToNeighbour < neighbour.G_cost) or (not open_set.contains(neighbour)):
                        neighbour.G_cost = newCostToNeighbour
                        neighbour.H_cost = getDistance(neighbour, target_node)
                        neighbour.parent = current_node

                        if not open_set.contains(neighbour):
                            open_set.add(neighbour)
                            maze.draw(open_set, closed_set)
                            time.sleep(1/SPEED)
                        else:
                            # if better path to given node is found, update that node's costs accordingly
                            open_set.updateItem(neighbour)

        else:
            maze.draw()