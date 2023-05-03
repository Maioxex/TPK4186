class node:
    def __init__(self, time, predecessors = None, successors = None, finished = False):
        self.finished = finished
        self.predecessors = predecessors
        self.successors = successors
        self.time = time
        
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
    def getStartTime(self):
        return self.time[0]
    def setStartTime(self, starttime):
        self.time[0] = starttime
    def getEndTime(self):
        return self.time[2]
    def setEndTime(self, endtime):
        self.time[2] = endtime
    def getDuration(self):
        return self.time[1]
    def setDuration(self, duration):
        self.time[1] = duration
    def getFinished(self):
        return self.finished
    def setFinished(self, finished):
        self.finished = finished
    
        