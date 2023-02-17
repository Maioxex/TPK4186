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

#Task 2.1.3  
def createRandomContainer(liste = False, serialnumberimp = 0):
    length = rnd.randint(1,2)
    serialnumber = rnd.randint(100000,999999)
    if liste:
        serialnumber = serialnumberimp
    if length==1:
        load = rnd.randint(0,20)
    else:
        load = rnd.randint(0,22)
    return container(length*20, serialnumber, load)

def createRandomContainerList(len = -1):
    list = containerlist()
    if len == -1:
        len = rnd.randint(5,20)
    ids = createuniqlist(len)
    for i in range(len):
        list.addContainer(createRandomContainer(True, ids[i]))
    return list

def createuniqlist(conts):
    ids  = []
    for i in range(conts):
        ids.append(rnd.randint(100000,999999))
    if len(ids) == len(set(ids)):
        return ids
    else: 
        while len(ids) != len(set(ids)):
            ids = list(set(ids))
            parselist = createuniqlist(conts-len(ids))
            for each in parselist:
                ids.append(each)
            print(len(set(ids)))
                    
        return ids
        
#task 2.1.4

#not sure if by "weight loaded you mean the added weight, or the weight of both the load and the container, so I made both
def printContainerListToCSV(listo):
    file = open("ContainerList.csv", "w+")
    for each in listo:
        file.write(f"{each.getId()},{each.getLength()},{each.getselfvekt()},{each.getLoad()},{each.getTotalWeight()} \n")
    file.flush()
    file.close()

def loadContainerListFromCSV():
    file = open("ContainerList.csv", "r")
    listo = containerlist()
    for each in file:
        each = each.split(",")
        listo.addContainer(container(int(each[1]), int(each[0]), int(each[3])))
    file.flush()
    file.close()
    return listo

listo = createRandomContainerList()
printContainerListToCSV(listo.getContainerList())
listo = loadContainerListFromCSV()
for each in listo.getContainerList():
    print(each.getId(), each.getLength(), each.getselfvekt(), each.getLoad(), each.getTotalWeight())