from Unit import units
from Batch import batches
from Buffers import buffers
import numpy as np

class productionline:
    def __init__(self):
        self.numberofwafers = 0
        self.units = []
        self.batches = []
        self.buffers = []
        self.time = 0
        self.tasks = [[0,2,5,8],[1,4,6],[3,7]]
        for i in range(3):
            self.units.append(units(self.tasks[i], i))
        for i in range(10):
            self.buffers.append(buffers(i))
    
    def loadBatchToInputBuffer(self, batch):
        self.buffers[0].addBatch(batch)
    
    def getBuffers(self):
        return self.buffers
    
    def getUnits(self):
        return self.units
    
    def getTime(self):
        return self.time
    
    def getInputBuffer(self):
        return self.buffers[0]
    
    def getOutputBuffer(self):
        return self.buffers[9]
    
    def getNumberOfWafers(self):
        return self.numberofwafers
    
    def findBuffersWithUnit(self, unit):
        buffers = []
        for buffer in self.buffers:
            print(unit)
            if buffer.getBufferNR() in unit.getTasks():
                buffers.append(buffer)
        return buffers
    
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
        lowest = 10000000000000000
        print("Checking lowest time units")
        for unit in self.getUnits():
            print(f"Unit {unit.getId()} has time {unit.getTime()}")
        bestunit = None
        for unit in self.getUnits():
            if unit.getTime() < lowest and unit.getTime() != 0:
                lowest = unit.getTime()
                bestunit = unit
        return lowest, bestunit
                
    def progressTime(self, time):
        print(f"Time: {time}")
        for unit in self.units:
            if unit.getTime() - time >= 0:
                unit.decreaseTime(time)
                self.increaseTime(time)
            elif unit.getTime() == 0:
                return
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
    
    def loadUnitWithBatch(self, unit, batch):
        # print(f"Loading {unit} with batch {batch}")
        print(unit)
        print(batch)
        if self.canUnloadUnitWitchBatch(batch):
            self.loadTask(batch.getTask(), batch)
        else:
            raise ValueError("Unit cannot unload batch")
        
    def unloadBatchFromUnit(self, unit):
        if unit.getTime() != 0:
            raise ValueError("Unit cant unload a batch")
        else:
            batch = unit.getBatch()
            if unit.getState() == "processing":
                self.unloadTask()
            elif unit.getState() == "unloading":
                self.unloadUnit()
            return batch
        
    def canUnloadUnitWitchBatch(self, batch):
        nextBuffer = self.getBuffers()[batch.getTask()+1]
        unit = self.findUnitWithTask(batch.getTask()+1)
        print(f"Next buffer: {batch}")
        if nextBuffer.getLoad()+ batch.getLoad() <= nextBuffer.getLimit() and unit.isBusy() == False:
            return True
        else:
            return False
    
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
                if (self.getInputBuffer().getLoadRatio(self.numberofwafers, True) >= 1-delta or self.getInputBuffer().getLoadRatio(self.numberofwafers, True) >= 1-delta) and self.getInputBuffer() in bufferlist:
                    buffer = self.buffers[0]
                    batch = self.chooseBatchForBuffer(buffer, smallest = True)
                    unit.loadTask(batch.getTask(), batch)
                    return batch
                else:
                    buffer = self.getInputBuffer()
                    batch = self.chooseBatchForBuffer(buffer, smallest = False)
                    unit.loadTask(batch.getTask(), batch)
                return batch
    
    def chooseBatchForBuffer(self, buffer, smallest = False):
        if buffer.isBusy():
            raise ValueError("Buffer is busy")
        else:
            proofedlist = []
            for batch in buffer.getBatches():
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
    
    def loadInputHueristic1(self, batch):
        if self.getLoad(self.getInputBuffer()) > 0:
            return False
        else:
            return True
    
    def checkIfDone(self):
        if self.getOutputBuffer().getLoad() == self.getNumberOfWafers():
            return True
        return False
    
    def printState(self):
        for unit in self.units:
            print(unit)
        for buffer in self.buffers:
            print(buffer)
    
    def checkState(self, unit):
        if unit.state == "idle":
            return
        if unit.state == "loading":
            if unit.time == 0:
                unit.startTask()
        elif unit.state == "processing" or unit.state == "unloading":
            if unit.time == 0:
                self.unloadBatchFromUnit(unit)
        else:
            raise ValueError("Unit in impossible state", unit.getState())
    
    def choosingHueristic1(self, unit):
        for buffer in self.findBuffersWithUnit(unit):
            if buffer.getLoad() > 0:
                return buffer.getBatches()[0]
    
    def choosingInputHueristic1(self, batches):
        batches.sort(key = lambda x: x.getSize())
        return batches[0]
    
    def addToInputBufferHueristic1(self):
        for buffer in self.getBuffers():
            if buffer.getLoad() > 0 and buffer.getBufferNR() != 9:
                return False
        for unit in self.getUnits():
            if unit.isBusy():
                return False

        return True
    
    def dividinghueristic1(self, wafers, size = 20):
        if size <20 or size > 50:
            raise ValueError("Size is not between 20 and 50")
        batche = []
        while wafers > 0 and wafers//size > 1 and wafers%size > 50-size:
            batche.append(batches(size))
            wafers -= size
        if wafers > 0:
            batche.append(batches(wafers))
            
        return batche
    
    def simulatorloop(self, wafers, dividinghueristic, choosinghueristic, choosingInputHueristic, addToInputBufferHueristic):
        self.numberofwafers = wafers
        batc = dividinghueristic(wafers)
        i = 0
        
        while self.checkIfDone() == False:
            for unit in self.units:
                if unit.isBusy() == False:
                    batch = choosinghueristic(unit)
                    self.loadUnitWithBatch(unit, batch)
                #print(addToInputBufferHueristic())
                if addToInputBufferHueristic():
                    batch = choosingInputHueristic(batc)                
                    self.loadInputBuffer(batch)
                    batc.remove(batch)
            self.progressTime(self.checklowestTimeUnits()[0])
            self.printState()
            i += 1
            if i == 10:
                print("itsa wrong, mario")
                break
        print(batc)
        print("Done at time:", self.getTime())
        
Task41 = productionline()
Task41.simulatorloop(20, Task41.dividinghueristic1,  Task41.choosingHueristic1, Task41.choosingInputHueristic1, Task41.addToInputBufferHueristic1)
