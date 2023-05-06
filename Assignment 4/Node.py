import numpy as np

class node:
    def __init__(self, name, time, predecessors = None, successors = None, finished = False, description = None):
        self.name = name
        self.finished = finished
        self.predecessors = predecessors
        self.successors = successors
        self.time = time
        self.earlyStart = False
        self.earlyFinish = False
        self.lateStart = False
        self.lateFinish = False
        if self.time != None:
            self.duration = time[1]
        else: 
            self.duration = None
        self.description = description
        self.critical = False
    
    def isCritical(self):
        return self.critical
    def setCritical(self, critical):
        self.critical = critical
    def getName(self):
        return self.name
    def setName(self, name):
        self.name = name
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
    def setEarlyStart(self, earlyStart):
        self.earlyStart = earlyStart
    def getEarlyFinish(self):
        return self.earlyFinish
    def setEarlyFinish(self, earlyFinish):
        self.earlyFinish = earlyFinish
    def getLateStart(self):
        return self.lateStart
    def getLateFinish(self):
        return self.lateFinish
    def setLateStart(self, lateStart):
        self.lateStart = lateStart
    def setLateFinish(self, lateFinish):
        self.lateFinish = lateFinish
    def getDuration(self):
        return self.duration
    def setDuration(self, duration):
        self.duration = duration
    def getDescription(self):
        return self.description
    def setDescription(self, description):
        self.description = description
    def appendPredecessor(self, predecessor):
        if self.predecessors == None:
            self.predecessors = [predecessor]
        else: 
            self.predecessors.append(predecessor)
    def appendSuccessor(self, successor):
        if self.successors == None:
            self.successors = [successor]
        else:
            self.successors.append(successor)
        
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
    
    def getNamesofPredaecessors(self):
        if self.predecessors == None or self.predecessors == []:
            return []
        else:
            return [x.getName() for x in self.predecessors]
    
    def getNamesofSuccessors(self):
        if self.successors == None or self.successors == []:
            return []
        else:
            return [x.getName() for x in self.successors]
        
    