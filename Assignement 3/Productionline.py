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
        
        
    def findUnitWithTask(self, task):
        for unit in self.units:
            if task in unit.getTasks():
                return unit
        return -1
    
    def increaseTime(self, time):
        self.time += time
    
    def findUnitWithBatch(self, batch):
        for unit in self.units:
            if unit.batch == batch:
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
            if unit.time < lowest:
                lowest = unit.time
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
        if unit.isBusy():
            raise ValueError("Unit is busy")
        elif task not in unit.getTasks():
            raise ValueError("Task not possible")
        unit.setTask(task)
        unit.setTime(1)
        unit.setBatch(batch)
        unit.setState("loading")

    def unloadTask(self, unit):
        if unit.getTime() != 0:
            raise ValueError(f"Unit is busy being {unit.state}")
        unit.setTask(-1)
        unit.setTime(1)
        tempbatch = unit.getBatch()
        unit.setBatch(-1)
        unit.setState("unloading")
        return tempbatch
    
    def startTask(self, unit):
        if self.time != 0:
            raise ValueError(f"Unit is busy being {unit.state}")
        unit.setTime(unit.productiontimes[unit.getTask()]*unit.getBatch().getSize())
        unit.setState("processing")
    
    def loadUnitWithBatch(self, batch, unit):
        unit.loadTask(batch.getTask(), batch)
    
    
    
    
    
    
    
    def chooseBatchForUnit(self, unit, delta = 0.1):
        if unit.isBusy():
            raise ValueError("Unit is busy")
        else:
            unitID = unit.getID()
            unitbuffers = []
            for buffernr in self.tasks[unitID]:
                unitbuffers.append(self.getBufferWithTask(buffernr))
            bufferlist = []
            for buffer in unitbuffers:
                if not buffer.isBusy():
                    bufferlist.append(buffer)
            if len(bufferlist) == 0:
                return "No buffer loaded"
            else:
                bufferlist.sort(key  = lambda x: x.getLoadRatio())
                if (self.buffers[0].getLoadRatio(self.numberofwafers, True) >= 1-delta or self.buffers[0].getLoadRatio(self.numberofwafers, True) >= 1-delta) and self.buffers[0] in bufferlist:
                    buffer = self.buffers[0]
                    batch = self.chooseBatchForBuffer(buffer, smallest = True)
                    unit.loadTask(batch.getTask(), batch)
                    return batch
                else:
                    buffer = bufferlist[0]
                    batch = self.chooseBatchForBuffer(buffer, smallest = False)
                    unit.loadTask(batch.getTask(), batch)
                return batch
    
    def chooseBatchForBuffer(self, buffer, smallest = False):
        if buffer.isBusy():
            raise ValueError("Buffer is busy")
        else:
            proofedlist = []
            for batch in buffer.batches:
                if self.canUnloadUnitWitchBatch(batch):
                    proofedlist.append(batch)
            if len(proofedlist) == 0:
                return "No batch can be unloaded"
            else:
                if smallest:
                    proofedlist.sort(key = lambda x: x.getSize())
                    return proofedlist[0]
                else:
                    proofedlist.sort(key = lambda x: x.getSize(), reverse = True)
                    return proofedlist[0]    
    
    def canUnloadUnitWitchBatch(self, batch):
        nextBuffer = self.buffer[batch.getTask()+1]
        unit = self.findUnitWithBuffer(nextBuffer)
        if nextBuffer.getLoad()+batch.getLoad() <= nextBuffer.getLimit():
            return True
        else:
            return False