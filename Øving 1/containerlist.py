from containers import container

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
    

    