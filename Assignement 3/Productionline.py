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
    
    def loadBatchToInputBuffer(self, batch, f):
        self.buffers[0].add(batch)
        f.write(f"Batch {batch.getSize()} is loaded into inputbuffer at time {self.getTime()}\n")
    
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
            # print(unit)
            if buffer.getBufferNR() in unit.getTasks():
                buffers.append(buffer)
        return buffers
    
    def findUnitWithTask(self, task):
        for unit in self.units:
            if task in unit.getTasks():
                return unit
        return -1
    
    def increaseTime(self, time):
        a = self.getTime()
        b = time + a
        self.time = b
    
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
        # print("Checking lowest time units")
        # for unit in self.getUnits():
        #     print(f"Unit {unit.getId()} has time {unit.getTime()}")
        bestunit = None
        for unit in self.getUnits():
            if unit.getTime() < lowest and unit.getTime() != 0:
                lowest = unit.getTime()
                bestunit = unit
        if lowest == np.inf:
            return 0, bestunit
        return lowest, bestunit
                
    def progressTime(self, time):
        #print(f"Time: {time}")
        self.increaseTime(time)
        for unit in self.units:
            if unit.getTime() - time >= 0:
                unit.decreaseTime(time)
            elif unit.getTime() == 0:
                continue
            else:
                raise ValueError("Time is not possible")
            
    def getBufferWithTask(self, task):
        for buffer in self.buffers:
            if buffer.getBufferNR() == task:
                return buffer
        raise ValueError("No buffer with task")
    
    def loadTask(self, task, batch):
        unit = self.findUnitWithTask(task)
        if unit.isBusy() or unit.getTime() != 0:
            raise ValueError("Unit is busy")
        elif task not in unit.getTasks():
            raise ValueError("Task not possible")
        elif batch.getCurrentTask() != task:
            raise ValueError("Batch not possible")
        unit.setTask(task)
        unit.setTime(1)
        unit.setBatch(batch)
        batch.incrementCurrentTask()
        buffer = self.getBufferWithTask(task)
        buffer.remove(batch)
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
        self.getBufferWithTask(batch.getCurrentTask()).add(batch)
        unit.setBatch(-1)
        unit.setState("idle")
    
    def startTask(self, unit, f):
        if unit.time != 0:
            raise ValueError(f"Unit is busy being {unit.state}")
        if unit.getState() != "loading":
            raise ValueError("Unit is not loading")
        unit.setTime(unit.productiontimes[unit.getTask()]*unit.getBatch().getSize())
        unit.setState("processing")
        f.write(f"Time: {self.getTime()} started task {unit.getTask()} on unit {unit.getId()} with batch {unit.getBatch().getSize()}\n")  
    
    def loadUnitWithBatch(self, unit, batch, f):
        # print(f"Loading {unit} with batch {batch}")
        # print(unit)
        # print(batch)
        if self.canUnloadUnitWitchBatch(batch):
            self.loadTask(batch.getCurrentTask(), batch)
            f.write(f"Time: {self.getTime()} loading unit {unit.getId()} with batch {batch.getSize()}\n")
        else:
            raise ValueError(f"Unit {unit.getId()} cannot unload batch to next buffer {batch.getCurrentTask()+1}")
        
    def unloadBatchFromUnit(self, unit,f):
        if unit.getTime() != 0:
            raise ValueError("Unit cant unload a batch")
        else:
            batch = unit.getBatch()
            if unit.getState() == "processing":
                self.unloadTask(unit)
            elif unit.getState() == "unloading":
                self.unloadUnit(unit)
                f.write(f"Time: {self.getTime()} unloaded batch {batch.getSize()} from unit {unit.getId()}\n")
            return batch
        
    def canUnloadUnitWitchBatch(self, batch):
        nextBuffer = self.getBuffers()[batch.getCurrentTask()+1]
        unit = self.findUnitWithTask(batch.getCurrentTask())
        #print(f"Next buffer: {batch}")
        if nextBuffer.getBufferNR() == 9:
            return True
        elif nextBuffer.getLoad()+ batch.getSize() <= nextBuffer.getLimit() and unit.isBusy() == False:
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
    
    def checkState(self, unit, f):
        if unit.state == "idle":
            return
        if unit.state == "loading":
            if unit.time == 0:
                self.startTask(unit, f)
        elif unit.state == "processing" or unit.state == "unloading":
            if unit.time == 0:
                self.unloadBatchFromUnit(unit, f)
        else:
            raise ValueError("Unit in impossible state", unit.getState())
    
    def choosingHueristic1(self, unit):
        for buffer in self.findBuffersWithUnit(unit):
            if buffer.getLoad() > 0:
                return buffer.getBatches()[0]
    
    def choosingHueristic2(self, unit):
        for buffer in self.findBuffersWithUnit(unit):
            if buffer.getLoad() > 0:
                if self.canUnloadUnitWitchBatch(buffer.getBatchWithSmallestSize()):
                    return buffer.getBatchWithSmallestSize()
    
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
    
    def addToInputBufferHueristic_whenEmpty(self):
        if self.getInputBuffer().getLoad() == 0:
            return True
        else:
            return False

    
    def dividinghueristic1(self, num_wafers, size = 20):
        groups = []
        while num_wafers - size > 20:
            groups.append(size)
            num_wafers -= size
        if num_wafers/2 < 20:
            groups.append(num_wafers)
        else:
            groups.append(num_wafers/2)
            groups.append(num_wafers/2)
        batche = []
        print(groups)
        for group in groups:
            batche.append(batches(group))
            
        return batche
    
    def clear(self):
        self = productionline()
    
    def simulatorloop(self, wafers, dividinghueristic, choosinghueristic, choosingInputHueristic, addToInputBufferHueristic, filename, n = 20):
        self.numberofwafers = wafers
        batc = dividinghueristic(wafers, n)
        i = 0
        
        f = open(filename, "w")

        while self.checkIfDone() == False:
            for unit in self.units:
                if unit.isBusy() == False and choosinghueristic(unit) != None:
                    batch = choosinghueristic(unit)
                    self.loadUnitWithBatch(unit, batch, f)
                #print(addToInputBufferHueristic())
                if addToInputBufferHueristic() and len(batc) > 0:
                    batch = choosingInputHueristic(batc)
                    if batch != None:                
                        self.loadBatchToInputBuffer(batch, f)
                        batc.remove(batch)
            self.progressTime(self.checklowestTimeUnits()[0])
            for unit in self.units:
                self.checkState(unit, f)
            #self.printState()
            #print("Total Time:", self.getTime())
            # i += 1
            # if i == 100:
            #     print("itsa wrong, mario")
            #     break
        #print(batc)
        print("Done at time:", self.getTime())
        f.close()
        return self.getTime()
        
        
# Task41 = productionline()
# Task41.simulatorloop(20, Task41.dividinghueristic1,  Task41.choosingHueristic1, Task41.choosingInputHueristic1, Task41.addToInputBufferHueristic1, "Task41output.txt")
# Task42 = productionline()
# Task42.simulatorloop(60, Task42.dividinghueristic1,  Task42.choosingHueristic1, Task42.choosingInputHueristic1, Task42.addToInputBufferHueristic1, "Task42output.txt")
# Task43 = productionline()
# Task43.simulatorloop(1000, Task43.dividinghueristic1,  Task43.choosingHueristic1, Task43.choosingInputHueristic1, Task43.addToInputBufferHueristic1, "Task43output.txt")
# Task44 = productionline()
# Task44.simulatorloop(1000, Task44.dividinghueristic1,  Task44.choosingHueristic1, Task44.choosingInputHueristic1, Task44.addToInputBufferHueristic1, "Task44output.txt", 30)

# Task5 = productionline()
# value = [None]
# num = np.inf
# for i in range(20,51):
#     tid = Task5.simulatorloop(1000, Task5.dividinghueristic1,  Task5.choosingHueristic1, Task5.choosingInputHueristic1, Task5.addToInputBufferHueristic1, "Task5output.txt", i)
#     if tid < num:
#         num = tid
#         value[0] = i
#     Task5 = productionline()
Task5 = productionline()
value = [None]
num = np.inf
for i in range(20, 51):
    tid = Task5.simulatorloop(1000, Task5.dividinghueristic1, Task5.choosingHueristic2, Task5.choosingInputHueristic1, Task5.addToInputBufferHueristic_whenEmpty, "Task5output.txt", i)
    if tid < num:
        num = tid
        value[0] = i
    Task5 = productionline()