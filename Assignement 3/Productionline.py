#Martin Kristiansen Tømt og Nikolay Westengen assignment 3

import numpy as np
from Batch import batches
from Buffers import buffers
from Unit import units
import itertools

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
    
    #task 2
    #the printer for the system, will print out the state of the entire production line at the time of calling
    #we are not using it activly in  our main function, as it increases the runtime of the program by a lot, espescially when using the optimization function that brute forces
    def printState(self):
        for unit in self.units:
            print(unit)
        for buffer in self.buffers:
            print(buffer)
    
    #task 3
    #here we have implemented the different actions, but as functions in the productionline class instead of an entire new class
    def loadBatchToInputBuffer(self, batch, f):
        self.buffers[0].add(batch)
        f.write(f"Batch {batch.getSize()} is loaded into inputbuffer at time {self.getTime()}\n")
        
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
    
    #helping functions for the actions
    #this checks if you can unload a batch to the next buffer
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
    
    #this checks if the output buffer is full, thus meaning the loop should break
    def checkIfDone(self):
        if self.getOutputBuffer().getLoad() == self.getNumberOfWafers():
            return True
        return False

    
    #checks the state of a unit, and calls the correct action if there is a natural next step
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
    
    #this is the choosing hueristic for choosing a batch to load into a unit without any prior order or logic
    def choosingHueristic1(self, unit, priorOrder):
        for buffer in self.findBuffersWithUnit(unit):
            if buffer.getLoad() > 0:
                return buffer.getBatches()[0]
    
    #this is the choosing hueristic for choosing a batch to load into a unit without a prior order, but always choosing the smallest batch as we found that was helpfull to start loading the production line at the start
    def choosingHueristic2(self, unit, priorOrder):
        for buffer in self.findBuffersWithUnit(unit):
            if buffer.getLoad() > 0:
                if self.canUnloadUnitWitchBatch(buffer.getBatchWithSmallestSize()):
                    return buffer.getBatchWithSmallestSize()
    
    #this is the choosing hueristic for choosing a batch to load into a unit with a prior order, but always choosing the smallest batch as we found that was helpfull to start loading the production line at the start
    def choosingHueristic3(self, unit, priorOrder):
        orderedBuffers = []
        for task in priorOrder:
            orderedBuffers.append(self.getBufferWithTask(task))
        for buffer in orderedBuffers:
            if buffer.getLoad() > 0:
                if self.canUnloadUnitWitchBatch(buffer.getBatchWithSmallestSize()):
                    return buffer.getBatchWithSmallestSize()
    
    #this is the hueristic which chooses what batch to into the input buffer, it is always the smallest batch
    #can be expanded to be more complex, but not within the scope of the assignement
    #we found that this was the best hueristic for the input buffer, as it helped the system get started
    #a natural next step would be to implement a hueristic that takes in a delta so that it chooses smallest batches at the start and end, while bigger between
    def choosingInputHueristic1(self, batches):
        batches.sort(key = lambda x: x.getSize())
        return batches[0]
    
    #this is the hueristic which chooses when to input a batch into the input buffer, it only does so when the entire system is idle
    def addToInputBufferHueristic1(self):
        for buffer in self.getBuffers():
            if buffer.getLoad() > 0 and buffer.getBufferNR() != 9:
                return False
        for unit in self.getUnits():
            if unit.isBusy():
                return False

        return True
    
    #task 5
    #this is the hueristic which chooses when to input a batch into the input buffer, it only does so when the input buffer is empty
    #this is now the optimal hueristic for the input buffer, as it has no chance of blocking the system at the start, and will always keep it running
    #thus being greatly more efficient than the other hueristic, over half the runtime with the same number of wafers. 
    #we found this was a better way to deal with than timesteps, as it is more dynamic and can be used in more situations, thus always being optimal timed to input a batch
    def addToInputBufferHueristic_whenEmpty(self):
        if self.getInputBuffer().getLoad() == 0:
            return True
        else:
            return False

    #this is the hueristic to divide the wafers into batches. default size is 20, but can be changed with input
    def dividinghueristic1(self, num_wafers, size = 20):
        groups = []
        while num_wafers - size >= 20 and not num_wafers == size:
            groups.append(size)
            num_wafers -= size
        if num_wafers == size:
            groups.append(size)
        elif num_wafers/2 <= 20:
            groups.append(num_wafers)
        else:
            if num_wafers%2 == 1:
                groups.append(num_wafers//2+1)
                groups.append(num_wafers//2)
            else:
                groups.append(num_wafers/2)
                groups.append(num_wafers/2)
        batche = []
        for group in groups:
            batche.append(batches(group))
        return batche
    
    #simulator for task 3
    #this is the simulator loop, it will run the simulation until all wafers are processed
    #it takes in the amount of wafers, how to divide the wafers, how to choose a batch to load into a unit, when to add a batch to the input buffer, the file it should print to, the prefered size of batches, and the prioritation order for the units
    #it gives out the time it took to process all wafers
    def simulatorloop(self, wafers, dividinghueristic, choosinghueristic, choosingInputHueristic, addToInputBufferHueristic, filename, n = 20, prioOrder = [[0,2,5,8],[1,4,6],[3,7]]):
        self.numberofwafers = wafers
        batc = dividinghueristic(wafers, n)
        i = 0
        
        f = open(filename, "w")

        while self.checkIfDone() == False:
            for unit in self.units:
                if unit.isBusy() == False and choosinghueristic(unit, prioOrder[unit.getId()]) != None:
                    batch = choosinghueristic(unit, prioOrder[unit.getId()])
                    self.loadUnitWithBatch(unit, batch, f)
                if addToInputBufferHueristic() and len(batc) > 0:
                    batch = choosingInputHueristic(batc)
                    if batch != None:                
                        self.loadBatchToInputBuffer(batch, f)
                        batc.remove(batch)
            self.progressTime(self.checklowestTimeUnits()[0])
            for unit in self.units:
                self.checkState(unit, f)
        f.close()
        return self.getTime()
    
    
#testing task 4, first with 1 batch, then with 3 batches, then with 1000 wafers, then with 1000 wafers with possibility to set batch size (44)    
Task41 = productionline()
Task41.simulatorloop(20, Task41.dividinghueristic1,  Task41.choosingHueristic1, Task41.choosingInputHueristic1, Task41.addToInputBufferHueristic1, "Task41output.txt")
Task42 = productionline()
Task42.simulatorloop(60, Task42.dividinghueristic1,  Task42.choosingHueristic1, Task42.choosingInputHueristic1, Task42.addToInputBufferHueristic1, "Task42output.txt")
Task43 = productionline()
Task43.simulatorloop(1000, Task43.dividinghueristic1,  Task43.choosingHueristic1, Task43.choosingInputHueristic1, Task43.addToInputBufferHueristic1, "Task43output.txt")
Task44 = productionline()
Task44.simulatorloop(1000, Task44.dividinghueristic1,  Task44.choosingHueristic1, Task44.choosingInputHueristic1, Task44.addToInputBufferHueristic1, "Task44output.txt", 30)

#testing task 5 for dynamic inputbufferloading (is also done with all possible combinations of dividing the batches)
Task5 = productionline()
value = [None]
num = np.inf
for i in range(20, 51):
    tid = Task5.simulatorloop(1000, Task5.dividinghueristic1, Task5.choosingHueristic2, Task5.choosingInputHueristic1, Task5.addToInputBufferHueristic_whenEmpty, "Task5output.txt", i)
    if tid < num:
        num = tid
        value[0] = i
    Task5 = productionline()
print(f"best dviding size: {value} giving time: {num} with dynamic loading")


#task 6 and 7
#optimalization function to find the best parameters of both dividng wafers and choosing priorities for the units by brute forcing all possible combinations
def findOptimalSolution():
    baselist = [[0,2,5,8],[1,4,6],[3,7]]
    basedlist = []
    basedlist.append(list(itertools.permutations(baselist[0])))
    basedlist.append(list(itertools.permutations(baselist[1])))
    basedlist.append(list(itertools.permutations(baselist[2])))
    Task5 = productionline()
    value = [None, None]
    num = np.inf
    j = 0
    for u1priorities in basedlist[0]:
        for u2priorities in basedlist[1]:
            for u3priorities in basedlist[2]:
                for i in range(20, 51):
                    tid = Task5.simulatorloop(1000, Task5.dividinghueristic1, Task5.choosingHueristic3, Task5.choosingInputHueristic1, Task5.addToInputBufferHueristic_whenEmpty, "Task6output.txt", i, [u1priorities, u2priorities, u3priorities])
                    j += 1
                    if tid < num:
                        num = tid
                        value[0] = i
                        value[1] = [u1priorities, u2priorities, u3priorities]
                        print(j, value, num)
                    if j%1400 == 0:
                        print(j, value, num)
                    Task5 = productionline()
    return value

#main function to run the optimalization function and then run the simulation with the optimal parameters
def main():
    values = findOptimalSolution()
    print(values)
    print(values[1])            
    Task7 = productionline()
    tid = Task7.simulatorloop(1000, Task7.dividinghueristic1, Task7.choosingHueristic3, Task7.choosingInputHueristic1, Task7.addToInputBufferHueristic_whenEmpty, "Task7output.txt", values[0], values[1])
    print(tid)

main()