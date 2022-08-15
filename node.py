from settings import *

class Node:
    def __init__(self, coordinates, walkable, weight = 0):
        # wall or path
        self.walkable = walkable
        # weight (for future adjustments)
        self.weight = weight
        # coordinates in maze
        self.x, self.y, self.z = coordinates
        # distance from starting node
        self.G_cost = 0
        # distance from end node
        self.H_cost = 0
        # parent
        self.parent = None

        # color of node
        if walkable:
            self.color = BG_COLOR
        else:
            self.color = WALL

        self.heapIndex = 0

    def cmp(self, a, b):
        return int(a > b) - int(a < b) 
    
    def get_F_cost(self):
        return self.G_cost + self.H_cost

    def compareTo(self, nodeToCompare):
        compare = self.cmp(self.get_F_cost(), nodeToCompare.get_F_cost())

        if compare == 0:
            compare = self.cmp(self.H_cost, nodeToCompare.H_cost)
        
        return -compare