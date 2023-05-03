class pert:
    def __init__(self, nodes = None):
        self.nodes = nodes
        
    def getNodes(self):
        return  self.nodes
    
    def setNodes(self, nodes):
        self.nodes = nodes
    
    def changepredecessor(self, node, predecessor):
        node.setPredecessor(predecessor)
    def changesuccessor(self, node, successor):
        node.setSuccessor(successor)
    def changetime(self, node, time):
        node.setTime(time)
    def changemintime(self, node, starttime):
        node.setMinTime(starttime)
    def changemaxtime(self, node, endtime):
        node.setEndTime(endtime)
    def changeexpectedtime(self, node, expected):
        node.setExpected(expected)
    def changefinished(self, node, finished):
        node.setFinished(finished)
    
    def calculateLateDates(self):
        nodes = self.getNodes()
        while len(nodes) > 0:
            for node in nodes:
                for successor in node.getSuccessor():
                    if successor not in nodes:
                        successor.calculateLateFinish()
                        successor.calculateLateStart()
                        nodes.remove(successor)
        print("Late dates calculated")
    
    def calculateEarlyDates(self):
        nodes = self.getNodes()
        while len(nodes) > 0:
            for node in nodes:
                for predecessor in node.getPredecessor():
                    if predecessor not in nodes:
                        predecessor.calculateEarlyStart()
                        predecessor.calculateEarlyFinish()
                        nodes.remove(predecessor)
        print("Early dates calculated")
        
