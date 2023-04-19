import numpy as np

class buffers:
    def __init__(self, bufferNR):
        self.bufferNR = bufferNR
        self.load = 0
        if bufferNR == 9 or bufferNR == 0:
            self.limit = np.inf
        else:
            self.limit = 120
        self.batches = []
        
    def add(self, batch):
        if self.load + batch.getSize() <= self.limit:
            self.load += batch.getSize()
            self.batches.append(batch)   
        else:
            raise ValueError("Batch does not fit in buffer")         
            
    def remove(self, batch):
        if batch in self.batches:
            self.load -= batch.getSize()
            self.batches.remove(batch)
        else:
            raise ValueError("Batch not in buffer")
        
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
    
    def updateLoad(self):
        self.load = 0
        for batch in self.batches:
            self.load += batch.getSize()
        if self.load > self.limit:
            raise ValueError("Load is larger than limit")
    
    def getLoadRatio(self, totalwafers, nr1 = False,):
        if nr1:
            return self.load/totalwafers
        else:
            return self.load/self.limit    
    
    def __str__(self):
        return "Buffer " + str(self.bufferNR) + " has a load of " + str(self.load) + " and a limit of " + str(self.limit)