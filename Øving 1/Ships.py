import containers as c
import containerlist as cl
import numpy as np

#task 2.2.5
class ships:
    def __init__(self, id, height, width, length):
        self.size = [height, width, length]
        self.id = id
        self.grid = np.zeros((int(self.size[0]),int(self.size[1]),int(self.size[2])), dtype=c.container)
    
    def getGrid(self):
        return self.grid
    
    def getSize(self):
        return self.size
    
    def getid(self):
        return self.id
    
    def setGrid(self, grid):
        self.grid = grid
    
    def ShipLoadded(self):
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                for k in range(self.size[2]):
                    if self.grid[i][j][k] != 0:
                        return True
        return False
    
    def findcontainer(self, container):
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                for k in range(self.size[2]):
                    if self.grid[i][j][k] != 0:
                        if self.grid[i][j][k].getId() == container.getId():
                            if container.getLength() == 40:
                                return [i,j,k],[i,j,k+1]
                            return [i,j,k]
        return "Container not found"

    def loadContainer(self, container, placeing, fromfile = False):
        if placeing == "No available spot":
            return placeing
        elif fromfile:
            self.grid[placeing[0]][placeing[1]][placeing[2]] = container
        elif container.getLength() == 40:
            self.grid[placeing[0][0]][placeing[0][1]][placeing[0][2]] = container
            self.grid[placeing[1][0]][placeing[1][1]][placeing[1][2]] = container
        else:
            self.grid[placeing[0]][placeing[1]][placeing[2]] = container

    def findLighetsSide(self):
        if self.calculateTotalWeightPortside() -21 < self.calculateTotalWeightStarboard():
            return 11
        else:
            return 22

    def findLighetsSection(self):
        if (self.calculateTotalWeightFront() < self.calculateTotalWeightCenter()+0.5) and (self.calculateTotalWeightFront() < self.calculateTotalWeightBack()+0.5):
            return 8
        elif (self.calculateTotalWeightCenter() < self.calculateTotalWeightFront()+0.5) and (self.calculateTotalWeightCenter() < self.calculateTotalWeightBack()+0.5):
            return 15
        else:
            return 23 
        
    def findAvailableContainerSpot(self, container):
        section = self.findLighetsSection()
        #print(section)
        side = self.findLighetsSide()
        #task 10 by looking and weights we changed from the next two lines to the automatic sorting based on weight at each section
        # g=[0,22]
        # h=[0,23]
        if side == 11:
            g = [0,11]
        else:
            g = [11,22]
        if section == 8:
            h = [0,8]
        elif section == 15:
            h = [8,15]
        else:   
            h = [15,23]
        if container.getLength() == 20:
            for i in range(self.size[0]):
                for j in range(g[0], g[1]):
                    for k in range(h[0],h[1]):
                        if self.grid[i][j][k] == 0:
                            return [i,j,k]
        else:
            for i in range(self.size[0]):
                for j in range(g[0], g[1]):
                    for k in range(h[0],h[1]-1):
                        if self.grid[i][j][k] == 0 and self.grid[i][j][k+1] == 0:
                            if i > 0:
                                if self.grid[i-1][j][k] != 0 and self.grid[i-1][j][k+1] != 0:
                                    return [[i,j,k],[i,j,k+1]]
                                else:
                                    continue
                            else:
                                return [[i,j,k],[i,j,k+1]]
        return "No available spot"
    
    def getWeightCapacity(self, placeing):
        if len(placeing) == 3:
            if placeing[0] == 0:
                return 100
            elif self.grid[placeing[0]-1][placeing[1]][placeing[2]] == 0:
                return -1
            else:
                return self.grid[placeing[0]-1][placeing[1]][placeing[2]].getTotalWeight()
        else:
            if placeing[0][0] == 0:
                return 100
            else:
                return min(self.grid[placeing[0][0]-1][placeing[0][1]][placeing[0][2]].getTotalWeight(), self.grid[placeing[1][0]-1][placeing[1][1]][placeing[1][2]].getTotalWeight())
   
    def canRemoveContainer(self, container):
        placeing = self.findcontainer(container)
        if container.getLength() == 40:
            if self.grid[placeing[0][0]+1][placeing[0][1]][placeing[0][2]] != 0 or self.grid[placeing[1][0]+1][placeing[1][1]][placeing[1][2]] != 0:
                return False
            else: 
                return True
            
        else:
            if self.grid[placeing[0]+1][placeing[1]][placeing[2]] != 0:
                return False
            else: 
                return True
    
    def removeContainer(self, container):
        placeing = self.findcontainer(container)
        canremove = self.canRemoveContainer(container)
        if container.getLength() == 40:
            if canremove:
                self.grid[placeing[0][0]][placeing[0][1]][placeing[0][2]] = 0
                self.grid[placeing[1][0]][placeing[1][1]][placeing[1][2]] = 0
            
        else:
            if canremove:
                self.grid[placeing[0]][placeing[1]][placeing[2]] = 0
      
      #Task 2.2.6          
    def printShipLoadToFile(self, filename = "ShipList.csv"):
        file = open(filename, "w+")
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                for k in range(self.size[2]):
                    if self.grid[i][j][k] != 0:
                        file.write(f"{str(i)},{str(j)},{str(k)},{str(self.grid[i][j][k].getId())},{str(self.grid[i][j][k].getLength())},{str(self.grid[i][j][k].getselfvekt())},{str(self.grid[i][j][k].getLoad())},{str(self.grid[i][j][k].getTotalWeight())}\n")
        file.flush()
        file.close()
    
    def loadShipFromFile(self, filename = "ShipList.csv"):
        file = open(filename, "r")
        for line in file:
            line = line.split(",")
            # print(line)
            # print(int(line[4]))
            # print(int(line[3]))
            # print(int(line[7][:-1]))
            length = int(line[4])
            id = int(line[3])
            load = int(line[6])
            container = c.container(length,id,load)
            self.loadContainer(container, [line[0], line[1], line[2]], True)
        file.flush()
        file.close()
    
    def loadShipWithContainerList(self, containerList):
        #this line fixed weighted on top at the beginning
        containerList.setContainerList(sorted(containerList.getContainerList(), key=lambda x: x.getTotalWeight(), reverse=True))
        while containerList.getContainerListLength() > 0:
            ikkeplassertliste = cl.containerlist()
            addedcontainer = False
            for container in containerList.getContainerList():
                plass = self.findAvailableContainerSpot(container)
                #print(plass)
                if plass == "No available spot":
                    # print("added none")
                    ikkeplassertliste.addContainer(container)
                else:  
                    self.loadContainer(container, plass)
                    addedcontainer = True
                containerList.setContainerList(ikkeplassertliste.getContainerList())
            if addedcontainer == False:
                return "kunne ikke plassere alle containere" 
        return "Alle containere plassert"
    
    def unloadShipToList(self):
        containerList = cl.containerlist()
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                for k in range(self.size[2]):
                    if self.grid[self.size[0]-i-1][j][k] != 0:
                        containerList.addContainer(self.grid[self.size[0]-i-1][j][k])
                        self.removeContainer(self.grid[self.size[0]-i-1][j][k])
        return containerList
    
    def calculateShipTotalWeight(self):
        total = 0
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                for k in range(self.size[2]):
                    if self.grid[i][j][k] != 0:
                        if self.grid[i][j][k].getLength() == 40:
                            total += self.grid[i][j][k].getTotalWeight()/2
                        else: total += self.grid[i][j][k].getTotalWeight()
        return total

    def calculateTotalWeightPortside(self):
        total = 0
        for i in range(self.size[0]):
            for j in range(int(self.size[1]/2)):
                for k in range(self.size[2]):
                    if self.grid[i][j][k] != 0:
                        if self.grid[i][j][k].getLength() == 40:
                            total += self.grid[i][j][k].getTotalWeight()/2
                        else: total += self.grid[i][j][k].getTotalWeight()
        return total
    
    def calculateTotalWeightStarboard(self):
        total = 0
        for i in range(self.size[0]):
            for j in range(int(self.size[1]/2), int(self.size[1])):
                for k in range(self.size[2]):
                    if self.grid[i][j][k] != 0:
                        if self.grid[i][j][k].getLength() == 40:
                            total += self.grid[i][j][k].getTotalWeight()/2
                        else: total += self.grid[i][j][k].getTotalWeight()
        return total
    
    def calculateTotalWeightFront(self):
        total = 0
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                for k in range(round(self.size[2]/3)):
                    if self.grid[i][j][k] != 0:
                        if self.grid[i][j][k].getLength() == 40:
                            total += self.grid[i][j][k].getTotalWeight()/2
                        else: total += self.grid[i][j][k].getTotalWeight()
        return total
    
    def calculateTotalWeightCenter(self):
        total = 0
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                for k in range(round(self.size[2]/3), round(self.size[2]/3*2)):
                    if self.grid[i][j][k] != 0:
                        if self.grid[i][j][k].getLength() == 40:
                            total += self.grid[i][j][k].getTotalWeight()/2
                        else: total += self.grid[i][j][k].getTotalWeight()
        return total
    
        
    def calculateTotalWeightBack(self):
        total = 0
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                for k in range(round(self.size[2]/3*2), self.size[2]):
                    if self.grid[i][j][k] != 0:
                        if self.grid[i][j][k].getLength() == 40:
                            total += self.grid[i][j][k].getTotalWeight()/2
                        else: total += self.grid[i][j][k].getTotalWeight()
        return total
    
    def isShipBalanced(self, x = 5, y= 10):
        if self.calculateTotalWeightStarboard()/self.calculateTotalWeightPortside() > (1+x/100):
            print("starboard")
            return False
        elif (self.calculateShipTotalWeight()>750):
            if self.calculateTotalWeightFront()/self.calculateTotalWeightBack() > (1+y/100) or self.calculateTotalWeightFront()/self.calculateTotalWeightCenter() > (1+y/100):
                print(self.calculateTotalWeightFront()/self.calculateTotalWeightBack(), self.calculateTotalWeightFront()/self.calculateTotalWeightCenter())
                print("front")
                return False
            elif self.calculateTotalWeightCenter()/self.calculateTotalWeightBack() > (1+y/100) or self.calculateTotalWeightCenter()/self.calculateTotalWeightFront() > (1+y/100):
                print("center")
                return False
            elif self.calculateTotalWeightBack()/self.calculateTotalWeightFront() > (1+y/100) or self.calculateTotalWeightBack()/self.calculateTotalWeightCenter() > (1+y/100):
                print("back")
                return False
        return True
