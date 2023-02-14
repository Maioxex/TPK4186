class container:
    def __init__(length, id, load =0):
        self.length = length
        self.id = id
        self.load = load
        if length == 20:
            self.selvvekt = 2
        else:
            self.selvvekt = 4
    
    #make the getter and setter functions for container
    def getLength(self):
        return self.length
    
    def setLength(self, length):
        self.length = length
    
    def getId(self):
        return self.id
    
    def setId(self, id):
        self.id = id
    
    def getLoad(self):
        return self.load
    
    def setLoad(self, load):
        self.load = load
        
    def getTotalWeight(self):

        return self.load + selv
    
    