from Batch import batch
from Buffers import buffer
from Productionline import productionline as pl


class units:
    def __init__(self, tasks):
        self.time = 0
        self.tasks = tasks
        self.productiontimes = [0.5,3.5,1.2,3,0.8,0.5,1,1.9,0.3]
        self.currenttask = -1
        self.batch = -1
    
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
    
    def TimeIncrement(self):
        self.time += 1
        
    def loadTask(self, task):
        if self.time != 0:
            raise ValueError("Unit is busy")
        if task not in self.tasks:
            raise ValueError("Task not possible")
        else: 
            self.currenttask = task
            self.time = self.productiontimes[task]
        self.time = 1
        pl.choosebatch(self)
        self.batch = batch

    def unloadTask(self):
        if self.time != 0:
            raise ValueError("Unit is busy")
        self.currenttask = -1
        self.time = 1
    
    def starttask(self):
        if self.time != 0:
            raise ValueError("Unit is busy")
        self.time = self.productiontimes[self.currenttask]*self.batch.getSize()