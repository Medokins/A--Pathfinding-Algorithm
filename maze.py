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
        self.state = 'menu'
        self.maze_file = None
        self.no_diagonals_pathfinding = False

        # for importing/saving maze files
        self.active = False

        # dragin variables
        self.wall_draging = False
        self.obstacle_draging = False

        # maze variables
        self.start_pos = None
        self.target_pos = None
        self.walls = []
        self.special_nodes = [[] for _ in range(len(WEIGHTS))]

    def draw(self, available = None, path = None, color = None, start_menu = False, save = False, square_size = SQUARE_SIZE):
        # set color to bg of maze
        screen.fill(BG_COLOR)
        font = pygame.font.SysFont('Calibri', 24)

        # draw weigts first since they are walkable and path my go over them
        for i in range(len(WEIGHTS)):
            for node in self.special_nodes[i]:
                pygame.draw.rect(screen, WEIGHTS_COLORS[i], pygame.Rect(node[0], node[1], square_size, square_size))

        # live-draw of working algorithm
        if available != None:
            for i in range(available.currentItemCount):
                node = available.items[i]
                if (node.x * square_size, node.y * square_size) not in {self.start_pos, self.target_pos}:
                    pygame.draw.rect(screen, AVAILABLE, pygame.Rect(node.x * square_size, node.y * square_size, square_size, square_size))
        if color == None:
            color = PATHED
        if path != None:
            for node in path:
                pygame.draw.rect(screen, color, pygame.Rect(node.x * square_size, node.y * square_size, square_size, square_size))

        # draw of start_node, target_node, walls and weights
        if self.start_pos != None:
            pygame.draw.rect(screen, START, pygame.Rect(self.start_pos[0], self.start_pos[1], square_size, square_size))
        if self.target_pos != None:
            pygame.draw.rect(screen, END, pygame.Rect(self.target_pos[0], self.target_pos[1], square_size, square_size))
        for wall in self.walls:
            pygame.draw.rect(screen, WALL, pygame.Rect(wall[0], wall[1], square_size, square_size))


        # grid creation
        for x in range(0, WINDOW_SIZE[0] - SPACING + 1, square_size):
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
            pygame.draw.rect(screen, WEIGHTS_COLORS[counter], pygame.Rect(WINDOW_SIZE[0] - SPACING + 10, y, 50, 50))
            pygame.draw.rect(screen, (0,0,0), pygame.Rect(WINDOW_SIZE[0] - SPACING + 10, y, 50, 50), 2)
            counter += 1

        if start_menu:
            font = pygame.font.Font(None, 32)
            file_text = ''
            color = INACTIVE_COLOR
            input_box = pygame.Rect((WINDOW_SIZE[0] - 600)/2, (WINDOW_SIZE[1] - 200)/2, 600, 100)

            self.active = False
            done = False
            show_file_promt = False
            while not done:           
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        done = True
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if input_box.collidepoint(event.pos):
                            self.active = not self.active
                        else:
                            self.active = False
                        color = ACTIVE_COLOR if self.active else INACTIVE_COLOR

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_i:
                            show_file_promt = True
                        if event.key == pygame.K_n and not self.active:
                            self.no_diagonals_pathfinding = not self.no_diagonals_pathfinding
                        if self.active:
                            if event.key == pygame.K_RETURN:
                                done = True
                                self.maze_file = file_text
                            elif event.key == pygame.K_BACKSPACE:
                                file_text = file_text[:-1]
                            else:
                                file_text += event.unicode
                        elif event.key == pygame.K_RETURN:
                            done = True

                screen.fill(SAVING_BG_COLOR)

                # import-file square
                if show_file_promt:
                    header = font.render("Enter file name: ", True, INACTIVE_COLOR, SAVING_BG_COLOR)
                    headerRect = header.get_rect()
                    headerRect.center = ((WINDOW_SIZE[0] - 600)/2 + 90,  (WINDOW_SIZE[1] - 200)/2 - 25)
                    screen.blit(header, headerRect)

                    file_txt_surface = font.render(file_text, True, color, SAVING_BG_COLOR)
                    width = max(600, file_txt_surface.get_width() + 10)
                    input_box.w = width
                    screen.blit(file_txt_surface, ((WINDOW_SIZE[0] - 600)/2 + 10, (WINDOW_SIZE[1] - 200)/2 + 35))
                    pygame.draw.rect(screen, color, input_box, 2)

                # headers
                else:
                    header = font.render("Key bindings: ", True, ACTIVE_COLOR, SAVING_BG_COLOR)
                    headerRect = header.get_rect()
                    headerRect.center = (100,  50)
                    screen.blit(header, headerRect)

                    # Key-bindings
                    text_1 = font.render("I: Import maze_file (use now)", True, INACTIVE_COLOR, SAVING_BG_COLOR)
                    text_2 = font.render("S: Save maze_file (use after complition)", True, INACTIVE_COLOR, SAVING_BG_COLOR)
                    text_3 = font.render("Q/ENTER: Quit (use after complition)", True, INACTIVE_COLOR, SAVING_BG_COLOR)
                    text_4 = font.render("S: Set start position", True, INACTIVE_COLOR, SAVING_BG_COLOR)
                    text_5 = font.render("E: Set target position", True, INACTIVE_COLOR, SAVING_BG_COLOR)
                    text_6 = font.render("W: Draw walls", True, INACTIVE_COLOR, SAVING_BG_COLOR)
                    text_7 = font.render("Numbers [0 - 9]: Draw weights", True, INACTIVE_COLOR, SAVING_BG_COLOR)
                    text_8 = font.render("D: Delete walls/weights", True, INACTIVE_COLOR, SAVING_BG_COLOR)
                    text_9 = font.render("R: Run pathfinding algorithm", True, INACTIVE_COLOR, SAVING_BG_COLOR)
                    text_10 = font.render("N: No-diagonals pathfinding option (currenty: ON)",  True, ACTIVE_COLOR, SAVING_BG_COLOR) if self.no_diagonals_pathfinding else \
                              font.render("N: No-diagonals pathfinding option (currenty: OFF)", True, INACTIVE_COLOR, SAVING_BG_COLOR)
                    texts = [text_1, text_2, text_3, text_4, text_5, text_6, text_7, text_8, text_9, text_10]

                    spacing = 150
                    for text in texts:
                        textRect = text.get_rect()
                        textRect.left = 50
                        textRect.bottom = spacing
                        screen.blit(text, textRect)
                        spacing += 50

                    # Continue text
                    contiune_text= font.render("Press ENTER to conitune", True, INACTIVE_COLOR, SAVING_BG_COLOR)
                    contiune_textRect = contiune_text.get_rect()
                    contiune_textRect.left = 40
                    contiune_textRect.bottom = spacing + 20
                    screen.blit(contiune_text, contiune_textRect)

                pygame.display.flip()

            self.state = "passive"

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

def runMaze():
    ######################################################## maze creation
    maze = Maze()
    while maze.state != 'end':
        if maze.state == "menu":
            maze.draw(start_menu=True)
        if maze.maze_file == None:
            # than draw your own maze:
            maze.x, maze.y = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    maze.state = 'end'
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        if maze.start_pos != None and maze.target_pos != None:
                            layers = 1
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
                    square_size = get_settings_square_size()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if maze.state == "choosing_start_pos":
                                maze.start_pos = (maze.x // square_size * square_size, maze.y // square_size * square_size, 0)
                        if maze.state == "choosing_target_pos":
                                maze.target_pos = (maze.x // square_size * square_size, maze.y // square_size * square_size, 0)

                    elif event.type == pygame.MOUSEMOTION:
                        if maze.state == "creating_obstacles":
                            if (maze.x // square_size * square_size, maze.y // square_size * square_size) not in {maze.start_pos, maze.target_pos}:
                                maze.walls.append((maze.x // square_size * square_size , maze.y // square_size * square_size, 0))
                        if maze.state == "choosing_weights":
                            # row in my 2d array is corresponding to weight of given node
                            if (maze.x // square_size * square_size, maze.y // square_size * square_size) not in {maze.start_pos, maze.target_pos}:
                                maze.special_nodes[weight].append((maze.x // square_size * square_size, maze.y // square_size * square_size, 0)) 
                        if maze.state == "deleting":
                            node = (maze.x // square_size * square_size, maze.y // square_size * square_size, 0)
                            if node in maze.walls:
                                maze.walls.remove(node)
                            try:
                                if node in maze.special_nodes[weight]:
                                    maze.special_nodes[weight].remove(node)
                            # Weight variable was not chosen yet
                            except:
                                pass
        else:
            # get an exisitng file
            maze.start_pos, maze.target_pos, maze.walls, maze.special_nodes, shape, layers = decode_maze(maze.maze_file)
            square_size = WINDOW_SIZE[1] // shape[1]
            maze.state = 'ready'
        
        if maze.state == 'ready':
            # path finding
            array_size = [layers, int((WINDOW_SIZE[0] - SPACING) / square_size), int(WINDOW_SIZE[1] / square_size)]
            maze_nodes = np.empty((array_size), dtype = Node)

            # creating grid of nodes
            for z in range(layers):
                for x in range(int((WINDOW_SIZE[0] - SPACING) / square_size)):
                    for y in range(int(WINDOW_SIZE[1] / square_size)):
                        # because when reading from file indexes are automatically correct
                        check = (x*square_size,y*square_size, z)

                        if check == maze.start_pos:
                            start_node = Node(coordinates = (x,y,z), walkable = True)
                            maze_nodes[z][x][y] = start_node
                        elif check == maze.target_pos:
                            target_node = Node(coordinates = (x,y,z), walkable = True)
                            maze_nodes[z][x][y] = target_node
                        elif check in maze.walls:
                            maze_nodes[z][x][y] = Node(coordinates = (x,y,z), walkable = False)
                        else:
                            maze_nodes[z][x][y] = Node(coordinates = (x,y,z), walkable = True)
                        for i in range(len(WEIGHTS)):
                            if check in maze.special_nodes[i]:
                                maze_nodes[z][x][y] = Node(coordinates = (x,y,z), walkable = True, weight = WEIGHTS[i])

            # list of nodes to process, starting with start_node
            open_set = Heap(array_size[0] * array_size[1] * array_size[1])
            open_set.add(start_node)
            # list of nodes that have been already processed
            closed_set = []

            getNeighbours = getNeighboursNoDiag if maze.no_diagonals_pathfinding else getNeighboursDiag
            if layers > 1:
                getNeighbours = getNeighbours3d
            
            refresh_rate = 1/SPEED

            while open_set.currentItemCount > 0:
                current_node = open_set.removeFirst()
                closed_set.append(current_node)

                if current_node == target_node:
                    final_path = getPath(start_node, target_node)
                    if layers == 1:
                        maze.draw(available = None, path = final_path, color = FINAL_PATH, square_size = square_size)
                    while True:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                return final_path

                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_s:
                                    name = maze.draw(save=True)
                                    df = pd.DataFrame(index=range(array_size[1]), columns=range(array_size[2]))
                                    for x in range(array_size[1]):
                                        for y in range(array_size[2]):
                                            # if it's not a wall => it's walkable => check if it has weight to it
                                            # else, mark wall as "-" (for better visualisation in dataframe)
                                            if maze_nodes[0][x][y].walkable:
                                                df[x][y] = int(maze_nodes[0][x][y].weight)
                                            else:
                                                df[x][y] = "-"

                                    # at the end, override start_pos and target_pos with S and E accordingly
                                    df[start_node.x][start_node.y] = "S"
                                    df[target_node.x][target_node.y] = "E"

                                    df.columns = [f"|{i:03}|" for i in range(array_size[1])]
                                    df.index = [f"|{i:03}|" for i in range(array_size[2])]
                                    df.to_csv(os.path.join("saved_mazes", f"{name}.csv"))

                                    pygame.quit()
                                    return final_path

                                if event.key == pygame.K_q or event.key == pygame.K_RETURN:
                                    pygame.quit()
                                    return final_path

                for neighbour in getNeighbours(current_node, maze_nodes, array_size):
                    if not neighbour.walkable or neighbour in closed_set:
                        continue
                    
                    newCostToNeighbour = current_node.G_cost + getDistance(current_node, neighbour) + neighbour.weight
                    if (newCostToNeighbour < neighbour.G_cost) or (not open_set.contains(neighbour)):
                        neighbour.G_cost = newCostToNeighbour
                        neighbour.H_cost = getDistance(neighbour, target_node)
                        neighbour.parent = current_node

                        if not open_set.contains(neighbour):
                            open_set.add(neighbour)
                            if LIVE_VIEW:
                                maze.draw(open_set, closed_set, square_size = square_size)
                                time.sleep(refresh_rate)
                        else:
                            # if better path to given node is found, update that node's costs accordingly
                            open_set.updateItem(neighbour)

        else:
            maze.draw()