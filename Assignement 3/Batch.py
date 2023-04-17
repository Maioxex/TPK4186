class batches:
    def __init__(self, size, state = "idle", currenttask = 0
                 ):
        if size < 0:
            raise ValueError("Size of batch cannot be negative")
        elif size > 50:
            raise ValueError("Size of batch cannot be larger than 50")
        else:
            self.size = size
        self.state = state
        self.currenttask = currenttask
        self.possiblestates = ["idle", "loading", "processing", "unloading"]
    
    def getSize(self):
        return self.size
    
    def getState(self):
        return self.state
    
    def setState(self, state):
        if state not in self.possiblestates:
            raise ValueError("State not possible")
        else: 
            self.state = state
            
    def getCurrentTask(self):
        return self.currenttask
    
    def setCurrentTask(self, currenttask):
        self.currenttask = currenttask
        
    def incrementCurrentTask(self):
        self.currenttask += 1
        
    def __str__(self):
        return "Batch of size " + str(self.size) + " is " + str(self.state) + " and is currently working on task " + str(self.currenttask)
        
        
