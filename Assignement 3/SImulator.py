import Productionline as pl


class simulator:
    def __init__(self, numberofwafers):
        self.pl = pl.productionline(numberofwafers)
    
    def getPL(self):
        return self.pl
       
    def set(self, pl):
        self.pl = pl
    
    def getTime(self):
        return self.pl.time
    
    def loadBatchToInputBuffer(self, batch):
        self.pl.loadBatchToInputBuffer(batch)
        timeCompleted = self.pl.getTime() + self.pl.findUnitWithBatch(batch).getTime()
        return timeCompleted
    
    def loadUnitWithBatch(self, unit, batch):
        if self.canUnloadUnitWitchBatch(unit, batch):
            self.pl.loadTask(batch.getTask(), batch)
        else:
            raise ValueError("Unit cannot unload batch")
        
    def unloadBatchFromUnit(self, unit):
        if unit.getTime() != 0:
            raise ValueError("Unit cant unload a batch")
        else:
            batch = unit.getBatch()
            if unit.getState() == "processing":
                self.pl.unloadTask()
            elif unit.getState() == "unloading":
                self.pl.unloadUnit()
            return batch
                
    def chooseBatchForUnit(self, unit, delta = 0.1):
        if unit.isBusy():
            raise ValueError("Unit is busy")
        else:
            unitID = unit.getID()
            unitbuffers = []
            for buffernr in self.pl.tasks[unitID]:
                unitbuffers.append(self.pl.getBufferWithTask(buffernr))
            bufferlist = []
            for buffer in unitbuffers:
                if not buffer.isBusy():
                    bufferlist.append(buffer)
            if len(bufferlist) == 0:
                return "No buffer loaded"
            else:
                bufferlist.sort(key  = lambda x: x.getLoadRatio())
                if (self.pl.buffers[0].getLoadRatio(self.pl.numberofwafers, True) >= 1-delta or self.pl.buffers[0].getLoadRatio(self.pl.numberofwafers, True) >= 1-delta) and self.pl.buffers[0] in bufferlist:
                    buffer = self.pl.buffers[0]
                    batch = self.pl.chooseBatchForBuffer(buffer, smallest = True)
                    unit.loadTask(batch.getTask(), batch)
                    return batch
                else:
                    buffer = bufferlist[0]
                    batch = self.pl.chooseBatchForBuffer(buffer, smallest = False)
                    unit.loadTask(batch.getTask(), batch)
                return batch
    
    def chooseBatchForBuffer(self, buffer, smallest = False):
        if buffer.isBusy():
            raise ValueError("Buffer is busy")
        else:
            proofedlist = []
            for batch in buffer.batches:
                if self.pl.canUnloadUnitWitchBatch(batch):
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
        nextBuffer = self.pl.buffer[batch.getTask()+1]
        unit = self.pl.findUnitWithBuffer(nextBuffer)
        if nextBuffer.getLoad()+batch.getLoad() <= nextBuffer.getLimit() and unit.isBusy() == False:
            return True
        else:
            return False
        