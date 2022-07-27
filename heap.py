import numpy as np
from node import Node

class Heap:
    def __init__(self, maxSize):
        self.items = np.empty(maxSize, dtype = Node)
        self.currentItemCount = 0
    
    def add(self, item):
        item.heapIndex = self.currentItemCount
        self.items[self.currentItemCount] = item
        self.sortUp(item)
        self.currentItemCount += 1

    def removeFirst(self):
        firstItem = self.items[0]
        self.currentItemCount -= 1
        self.items[0] = self.items[self.currentItemCount]
        self.items[0].heapIndex = 0
        self.sortDown(self.items[0])

        return firstItem

    def updateItem(self, item):
        self.sortUp(item)

    def contains(self, item):
        return self.items[item.heapIndex] == item
    
    def sortUp(self, item):
        parentIndex = int((item.heapIndex-1)/2)

        while True:
            parentItem = self.items[parentIndex]
            if item.compareTo(parentItem) > 0:
                self.swap(item, parentItem)
            else:
                break
            parentIndex = int((item.heapIndex-1)/2)

    def sortDown(self, item):
        while True:
            childIndexLeft = item.heapIndex * 2 + 1
            childIndexRight = item.heapIndex * 2 + 2
            swapIndex = 0

            if childIndexLeft < self.currentItemCount:
                swapIndex = childIndexLeft
                if childIndexRight < self.currentItemCount:
                    if self.items[childIndexLeft].compareTo(self.items[childIndexRight]) < 0:
                        swapIndex = childIndexRight
                        
                if item.compareTo(self.items[swapIndex]) < 0:
                    self.swap(item, self.items[swapIndex])
                else:
                    return
            else:
                return

    def swap(self, itemA, itemB):
        self.items[itemA.heapIndex] = itemB
        self.items[itemB.heapIndex] = itemA

        temp = itemA.heapIndex
        itemA.heapIndex = itemB.heapIndex
        itemB.heapIndex = temp