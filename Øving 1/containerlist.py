from containers import container
import random as rnd

class containerlist:
    def __init__(self):
        self.containerlist = []
    
    #function to add a container to the list
    def addContainer(self, container):
        self.containerlist.append(container)
    
    def getContainer(self, index):
        return self.containerlist[index]
    
    def getContainerList(self):
        return self.containerlist
    
    def getContainerListLength(self):
        length = 0
        for each in self.containerlist:
            length += each.getLength()     
        return length
    
    def getContainerListWeight(self):
        weight = 0
        for each in self.containerlist:
            weight += each.getTotalWeight()
        return weight    
        
    def findContainer(self, serialnumber):
        for each in self.containerlist:
            if each.getId() == serialnumber:
                return each
        return "Container not found"
    
    def removeContainer(self, serialnumber):
        for each in self.containerlist:
            if each.getId() == serialnumber:
                self.containerlist.remove(each)
                return "Container removed"
        return "Container not found"

def createRandomContainerList():
    list = containerlist()
    conts = rnd.randint(1,20)
    for i in range(conts):
        list.addContainer(container.createRandomContainer())
    return list

listo = createRandomContainerList()
for each in listo.getContainerList():
    print(each.getlength(), each.getId(), each.getLoad())