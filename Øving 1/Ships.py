from containers import container
import containerlist as cl
import numpy as np

class ships:
    def __init__(self, id, length, width, height):
        self.size = [0,0,0]
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

    def loadContainer(self, container, placeing, fromfile = False):
        if placeing == "No available spot":
            return placeing
        elif fromfile:
            self.grid[placeing[0]][placeing[1]][placeing[2]] = container
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
                
    def printShipLoadToFile(self, filename = "ShipList.csv"):
        file = open(filename, "w+")
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                for k in range(self.size[2]):
                    if self.grid[i][j][k] != 0:
                        file.write(f"{str(i)},{str(j)},{str(k)},{str(self.grid[i][j][k].getid())},{str(self.grid[i][j][k].getlength())},{str(self.grid[i][j][k].getselvvekt())},{str(self.grid[i][j][k].getLoad())},{str(self.grid[i][j][k].getTotalWeight())}\n")
        file.flush()
        file.close()
    
    def loadShipFromFile(self, filename = "ShipList.csv"):
        file = open(filename, "r")
        for line in file:
            line = line.split(",")
            self.loadContainer(container(line[3], line[4], line[5]), [line[0], line[1], line[2]])
        file.flush()
        file.close()
    
    def loadShipWithContainerList(self, containerList):
        while containerList.getContainerListLength() > 0:
            addedcontainer = False
        for container in containerList:
            plass = self.findAvailableContainerSpot(container)
            if plass == "No available spot":
                print("added none")
                continue
            else:  
                self.loadContainer(container, plass)
                containerList.removeContainer(container.getid())
                addedcontainer = True
            if addedcontainer == False:
                print("added 1")
                return "kunne ikke plassere alle containere" 
        return "Alle containere plassert"
    
    def unloadShipToList(self):
        containerList = cl.containerlist()
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                for k in range(self.size[2]):
                    if self.grid[self.size[0]-i][j][k] != 0:
                        containerList.addContainer(self.grid[i][j][k])
                        self.grid[i][j][k] = 0
        return containerList

ship = ships(1, 18, 22, 23)
print("step")
listo = cl.createRandomContainerList(100)
print("step")
print(ship.loadShipWithContainerList(listo))
print("step")
ship.printShipLoadToFile()
print("step")
print(ship.unloadShipToList())
print[ship.grid]
