class Node:
    def __init__(self, coordinates, walkable, weight = 0):
        # wall or path
        self.walkable = walkable
        # weight (for future adjustments)
        self.weight = weight
        # coordinates in maze
        self.coordinates = coordinates
        # distance from starting node
        self.G_cost = 0
        # distance from end node
        self.H_cost = 0
        # summ of G_cost nad H_cost
        self.F_cost = self.G_cost + self.H_cost

        # color of node
        self.color = None