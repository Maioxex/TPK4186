from Unit import units
from Batch import batches
from Buffers import buffers
import numpy as np

class productionline:
    def __init__(self, numberofwafers):
        self.numberofwafers = numberofwafers
        self.units = []
        self.batches = []
        self.buffers = []
        self.time = 0
        tasks = [[0,2,5,8],[1,4,6],[3,7]]
        for i in range(3):
            self.units.append(units(tasks[i]), i)
        for i in range(10):
            self.buffers.append(buffers(i))
    
    def loadBatchToInputBuffer(self, batch):
        self.buffers[0].addBatch(batch)
        
    def findUnitWithTask(self, task):
        for unit in self.units:
            if task in unit.getTasks():
                return unit
        return -1
    
    def increaseTime(self, time):
        self.time += time
    
    def findUnitWithBatch(self, batch):
        for unit in self.units:
            if unit.getBatch() == batch:
                return unit
        return -1
    
    def findBufferWithBatch(self, batch):
        for buffer in self.buffers:
            if batch in buffer.batches:
                return buffer
        return -1
    
    def checklowestTimeUnits(self):
        lowest = np.inf
        bestunit = None
        for unit in self.units:
            if unit.getTime() < lowest:
                lowest = unit.getTime()
                bestunit = unit
        return lowest, bestunit
                
    def progressTime(self, time):
        for unit in self.units:
            if unit.getTime() - time >= 0:
                unit.decreaseTime(time)
                self.increaseTime(time)
            elif unit.getTime() == 0:
                pass
            else:
                raise ValueError("Time is not possible")
            
    def getBufferWithTask(self, task):
        for buffer in self.buffers:
            if buffer.getTask() == task:
                return buffer
        raise ValueError("No buffer with task")
    
    def loadTask(self, task, batch, unit):
        if unit.isBusy() or unit.getTime() != 0:
            raise ValueError("Unit is busy")
        elif task not in unit.getTasks():
            raise ValueError("Task not possible")
        elif batch.getTask() != task:
            raise ValueError("Batch not possible")
        unit.setTask(task)
        unit.setTime(1)
        unit.setBatch(batch)
        batch.incrementCurrentTask()
        unit.setState("loading")

    def unloadTask(self, unit):
        if unit.getTime() != 0:
            raise ValueError(f"Unit is busy being {unit.state}")
        unit.setTask(-1)
        unit.setTime(1)
        tempbatch = unit.getBatch()
        unit.setState("unloading")
        return tempbatch
    
    def unloadUnit(self, unit):
        if unit.getTime() != 0:
            raise ValueError(f"Unit is busy being {unit.state}")
        if unit.getState() != "unloading":
            raise ValueError("Unit is not unloading")
        unit.setTask(-1)
        batch = unit.getBatch()
        self.getBufferWithTask(batch.getTask()).addBatch(batch)
        unit.setBatch(-1)
        unit.setState("idle")
    
    def startTask(self, unit):
        if self.time != 0:
            raise ValueError(f"Unit is busy being {unit.state}")
        if unit.getState() != "loading":
            raise ValueError("Unit is not loading")
        unit.setTime(unit.productiontimes[unit.getTask()]*unit.getBatch().getSize())
        unit.setState("processing")
    