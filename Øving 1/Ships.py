from containers import container
import numpy as np

class ships:
    def __init__(self, id, length, width, height):
        self.size = []
        self.size[0] = height
        self.size[1] = width
        self.size[2] = length
        self.id = id
        self.grid = np.zeros((height, width, length))
    
    def findcontainer(self, container):
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                for k in range(self.size[2]):
                    if self.grid[i][j][k].getid() == container.getid():
                        if container.getlength() == 40:
                            return [i,j,k],[i,j,k+1]
                        return [i,j,k]
        return "Container not found"

    def loadContainer(self, container, placeing):
        if placeing == "No available spot":
            return placeing
        elif container.getlength() == 40:
            self.grid[placeing[0][0]][placeing[0][1]][placeing[0][2]] = container
            self.grid[placeing[1][0]][placeing[1][1]][placeing[1][2]] = container
        else:
            self.grid[placeing[0]][placeing[1]][placeing[2]] = container

    def findAvailableContainerSpot(self, container):
        if container.getlength() == 20:
            for i in range(self.size[0]):
                for j in range(self.size[1]):
                    for k in range(self.size[2]):
                        if self.grid[i][j][k] == 0:
                            return [i,j,k]
        else:
            for i in range(self.size[0]):
                for j in range(self.size[1]):
                    for k in range(self.size[2]-1):
                        if self.grid[i][j][k] == 0 and self.grid[i][j][k+1] == 0:
                            if i > 0:
                                if self.grid[i-1][j][k] == 0 and self.grid[i-1][j][k+1] == 0:
                                    return [[i,j,k],[i,j,k+1]]
        return "No available spot"
    
    def removeContainer(self, container):
        placeing = self.findcontainer(container)
        if container.getlength() == 40:
            if self.grid[placeing[0][0]+1][placeing[0][1]][placeing[0][2]] != 0 or self.grid[placeing[1][0]+1][placeing[1][1]][placeing[1][2]] != 0:
                return "Container blocked from above"
            else: 
                self.grid[placeing[0][0]][placeing[0][1]][placeing[0][2]] = 0
                self.grid[placeing[1][0]][placeing[1][1]][placeing[1][2]] = 0
            
        else:
            if self.grid[placeing[0]+1][placeing[1]][placeing[2]] != 0:
                return "Container blocked from above"
            else: 
                self.grid[placeing[0]][placeing[1]][placeing[2]] = 0
                        
