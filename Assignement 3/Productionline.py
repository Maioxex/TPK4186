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
            self.units.append(units(tasks[i]))
        for i in range(10):
            self.buffers.append(buffers(i))
        
    def findUnitWithTask(self, task):
        for unit in self.units:
            if task in unit.getTasks():
                return unit
        return -1
    
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
            if unit.time > 0:
                unit.decreaseTime(time)
    
    def choosebatch(self, unit):
        pass