import numpy as np

class buffers:
    def __init__(self, bufferNR):
        self.bufferNR = bufferNR
        self.load = 0
        if bufferNR == 10:
            self.limit = np.inf
        else:
            self.limit = 120
        
    def add(self, load):
        if load + self.load <= self.limit:
            self.load += load
            
    
    def add1(self):
        if self.load + 1 <= self.limit:
            self.load += 1
            
    def remove1(self, load):
        if self.load - load >= 0:
            self.load -= load
            
    def getLoad(self):
        return self.load
    
    def getBufferNR(self):
        return self.bufferNR
    
    def getLimit(self):
        return self.limit
    
    def setLoad(self, load):
        self.load = load
    
    def setLimit(self, limit):
        self.limit = limit
    
    def setBufferNR(self, bufferNR):
        self.bufferNR = bufferNR
    
    def __str__(self):
        return "Buffer " + str(self.bufferNR) + " has a load of " + str(self.load) + " and a limit of " + str(self.limit)