from Batch import batch
from Buffers import buffer
from Productionline import productionline as pl


class units:
    def __init__(self, tasks, id):
        self.id = id
        self.time = 0
        self.tasks = tasks
        self.productiontimes = [0.5,3.5,1.2,3,0.8,0.5,1,1.9,0.3]
        self.currenttask = -1
        self.batch = -1
        self.state = -1  
        self.possiblestates = ["idle", "loading", "processing", "unloading"]
    
    def getTasks(self):
        return self.tasks
    
    def getProductionTimes(self):
        return self.productiontimes
    
    def getTime(self):
        return self.time
    
    def getTask(self):
        return self.currenttask
    
    def setTask(self, task):
        self.currenttask = task
        
    def setTasks(self, tasks):
        self.tasks = tasks
        
    def setProductionTimes(self, productiontimes):
        self.productiontimes = productiontimes
        
    def setTime(self, time):
        self.time = time
    
    def decreaseTime(self, time):
        self.time -= time
    
    def TimeIncrement(self):
        self.time += 1
        
    
    def getState(self):
        return self.state
    
    def setState(self, state):
        if state not in self.possiblestates:
            raise ValueError("State not possible")
        self.state = state

        
        
    def getBatch(self):
        return self.batch
    
    def setBatch(self, batch):
        self.batch = batch
        
    def checkState(self):
        if self.state == "loading":
            if self.time == 0:
                self.state = "processing"
                self.startTask()
        elif self.state == "processing":
            if self.time == 0:
                self.state = "unloading"
                self.unloadTask()
        elif self.state == "unloading":
            if self.time == 0:
                self.state = "idle"
        elif self.state == "idle":
            pl.choosebatch(self)
        else:
            raise ValueError("State not possible")
        
    def isIdle(self):
        if self.state == "idle":
            return True
        else:
            return False
        
    def isBusy(self):
        if self.state == "idle":
            return False
        else:
            return True
    
    def getId(self):
        return self.id
    
    def setId(self, id):
        self.id = id
    
    def __str__(self):
        return f"Unit is {self.state} and is currently working on task {self.currenttask} with batch {self.batch} and has {self.time} time left"