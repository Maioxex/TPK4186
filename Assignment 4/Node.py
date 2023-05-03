import numpy as np

class node:
    def __init__(self, time,duration = np.inf, predecessors = None, successors = None, finished = False, description = None):
        self.finished = finished
        self.predecessors = predecessors
        self.successors = successors
        self.time = time
        self.earlyStart = False
        self.earlyFinish = False
        self.lateStart = False
        self.lateFinish = False
        self.duration = duration
        self.description = description
        
    def getPredecessor(self):
        return self.predecessors
    def setPredecessor(self, predecessors):
        self.predecessors = predecessors    
    def getSuccessor(self):
        return self.successors
    def setSuccessor(self, successors):
        self.successors = successors
    def setTime(self, time):
        self.time = time
    def getTime(self):
        return self.time
    def setMinTime(self, minTime):
        self.time[0] = minTime
    def getMinTime(self):
        return self.time[0]
    def getMaxTime(self):
        return self.time[2]
    def setMaxTime(self, endtime):
        self.time[2] = endtime
    def getExpected(self):
        return self.time[1]
    def setExpected(self, expected):
        self.time[1] = expected
    def getFinished(self):
        return self.finished
    def setFinished(self, finished):
        self.finished = finished
    def getEarlyStart(self):
        return self.earlyStart
    def getEarlyFinish(self):
        return self.earlyFinish
    def getLateStart(self):
        return self.lateStart
    def getLateFinish(self):
        return self.lateFinish
    def getDuration(self):
        return self.duration
    def setDuration(self, duration):
        self.duration = duration
    def getDescription(self):
        return self.description
    def setDescription(self, description):
        self.description = description
    
    def getAllPredaecessors(self):
        if self.predecessors == None:
            return []
        else:
            return list(set(self.predecessors + [x.getAllPredaecessors() for x in self.predecessors]))
    def getAllSuccessors(self):
        if self.successors == None:
            return []
        else:
            return list(set(self.successors + [x.getAllSuccessors() for x in self.successors]))
    
    def calculateEarlyStart(self):
        if self.predecessors == None:
            self.earlyStart = 0
        else:
            self.earlyStart = min([x.earlyFinish for x in self.predecessors])
        
    def calculateEarlyFinish(self):
        self.earlyFinish = self.earlyStart + self.duration
    
    def calculateLateFinish(self):
        if self.successors == None:
            self.lateFinish = self.lateFinish
        else:
            self.lateFinish = max([x.lateStart for x in self.successors])
    
    def calculateLateStart(self):
        self.lateStart = self.lateFinish - self.duration
    
    def checkIfCritical(self):
        if self.earlyStart == self.lateStart:
            return True
        else:
            return False