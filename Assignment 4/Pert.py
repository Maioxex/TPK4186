import numpy as np
import pandas as pd
from Node import node as no

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

class loader():
    def __init__(self,filename):
        self.filename = filename
        self.nodes = []
        self.load()
    
    def addNode(self, node):
        self.nodes.append(node)
    def getNodeByName(self, name):
        for node in self.nodes:
            if node.getName() == name:
                return node
    def load(self):
        df = pd.read_excel(self.filename)
        df = df.dropna(how='all')
    #def __init__(self, name, time, duration = np.inf, predecessors = None, successors = None, finished = False, description = None):
        for index, rows in df.iterrows():
            #print(rows[1])
            name = rows["Codes"]
            description = rows["Descriptions"]
            time = rows["Durations"]
            predecessors = rows["Predecessors"]
            if name == "Start":
                predecessors = None
                time = None
                task  = no(name, time, predecessors, None, False, description)
            else: 
                predecessors = predecessors.split(", ")
                if name == "Completion":
                    time = None
                else:
                    time = str(time).strip("()")
                    time = time.split(", ")
                task  = no(name, time, predecessors, None, False, description)
            self.addNode(task)
        for node in self.nodes:
            sucsessors = []
            if node.getName() == "Completion":
                continue
            for node2 in self.nodes:
                if node2.getName() == "Start":
                    continue
                if node.getName() in node2.getPredecessor():
                    sucsessors.append(node2.getName())
            node.setSuccessor(sucsessors)

        # for task in self.nodes:
        #     task.printNode()

        for node in self.nodes:
            predecessors = []
            sucsessors = []
            if node.getName() != "Start":
                for i in range(len(node.getPredecessor())):
                    predecessors.append(self.getNodeByName(node.getPredecessor()[i]))
            if node.getName() != "Completion":
                for i in range(len(node.getSuccessor())):
                    sucsessors.append(self.getNodeByName(node.getSuccessor()[i]))
            node.setPredecessor(predecessors)
            node.setSuccessor(sucsessors)
        for node in self.nodes:
            node.printNode()
nodes = loader("Assignment 4\Villa.xlsx")

