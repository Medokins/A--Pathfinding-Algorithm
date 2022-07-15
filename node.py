from settings import *

class Node:
    def __init__(self, coordinates, walkable, weight = 0):
        # wall or path
        self.walkable = walkable
        # weight (for future adjustments)
        self.weight = weight
        # coordinates in maze
        self.x, self.y = coordinates
        # distance from starting node
        self.G_cost = 0
        # distance from end node
        self.H_cost = 0

        # color of node
        if walkable:
            self.color = BG_COLOR
        else:
            self.color = WALL
    
    def get_F_cost(self):
        return self.G_cost + self.H_cost