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

    