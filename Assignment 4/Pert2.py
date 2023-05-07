import copy
import numpy as np
import pandas as pd
from Node import node as no


class pert:
    def __init__(self, nodes=None):
        self.nodes = nodes

    def getNodes(self):
        return self.nodes

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

    def getLengthOfProject(self):
        for node in self.getNodes():
            if node.getName() == "Completion" or node.getName() == "End":
                return node.getEarlyFinish()


class loader():
    def __init__(self, filename):
        self.filename = filename
        self.nodes = []
        self.load()

    def returnNodes(self):
        return self.nodes

    def addNode(self, node):
        self.nodes.append(node)

    def getNodeByName(self, name):
        for node in self.nodes:
            if node.getName() == name:
                return node

    def load(self):
        df = pd.read_excel(self.filename)
        df = df.dropna(how='all')
    # def __init__(self, name, time, duration = np.inf, predecessors = None, successors = None, finished = False, description = None):
        for index, rows in df.iterrows():
            # print(rows[1])
            name = rows["Codes"]
            try:
                description = rows["Descriptions"]
            except:
                description = rows["Description"]
            time = rows["Durations"]
            predecessors = rows["Predecessors"]
            if name == "Start":
                predecessors = None
                time = [0, 0, 0]
                task = no(name, time, predecessors, None, False, description)
            else:
                predecessors = predecessors.split(", ")
                if name == "Completion" or name == "End":
                    time = [0, 0, 0]
                else:
                    # print(rows)
                    time = str(time).strip("()")
                    time = time.split(", ")
                    for tall in time:
                        tall = float(tall)
                task = no(name, time, predecessors, None, False, description)
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
                    predecessors.append(
                        self.getNodeByName(node.getPredecessor()[i]))
            if node.getName() != "Completion":
                for i in range(len(node.getSuccessor())):
                    sucsessors.append(
                        self.getNodeByName(node.getSuccessor()[i]))
            node.setPredecessor(predecessors)
            node.setSuccessor(sucsessors)


class printer:
    def __init__(self, Pert=None):
        if Pert != None:
            self.nodes = Pert.getNodes()
        else:
            self.nodes = None
        self.printproject()

    def printproject(self):
        if self.nodes == None:
            print("No nodes")
        for node in self.nodes:
            self.printNode(node)

    def printNode(self, Node):
        predacessors = Node.getNamesofPredaecessors()
        successors = Node.getNamesofSuccessors()
        print(f"Name: {Node.getName()}, description: {Node.getDescription()}, durations: {Node.getTime()}, early dates: {Node.earlyStart, Node.earlyFinish}, late dates: {Node.lateStart, Node.lateFinish}, critical: {Node.isCritical()}, predecessors: {predacessors}, successors: {successors}")


class calculator:
    def __init__(self, project=None, index=1):
        print("Calculator created")
        self.index = index
        self.project = project
        self.calculate()

    def getNodeByName(self, name):
        for node in self.project.getNodes():
            if node.getName() == name:
                return node

    def calculate(self):
        startlist = copy.deepcopy(self.project.getNodes())
        while len(startlist) > 0:
            for node in startlist:
                checkedif = False
                for node2 in node.getPredecessor():
                    if node2 in startlist:
                        checkedif = True
                if checkedif:
                    continue
                self.calculateEarlyStart(self.getNodeByName(node.getName()))
                self.calculateEarlyFinish(self.getNodeByName(node.getName()))
                startlist.remove(node)
        endlist = copy.deepcopy(self.project.getNodes())
        while len(endlist) > 0:
            for node in endlist:
                checkedif = False
                for node2 in node.getSuccessor():
                    if node2 in endlist:
                        checkedif = True
                if checkedif:
                    continue
                self.calculateLateFinish(self.getNodeByName(node.getName()))
                self.calculateLateStart(self.getNodeByName(node.getName()))
                endlist.remove(node)
        for node in self.project.getNodes():
            self.checkIfCritical(node)

    def calculateEarlyStart(self, Node):
        # print(Node.getPredecessor())
        if Node.getName() == "Start":
            Node.setEarlyStart(0)
        else:
            if Node.getName() == "D" or Node.getName() == "A":
                print(Node.getName(), Node.getPredecessor()[0].getName())
            sorted_list = sorted(Node.getPredecessor(
            ), key=lambda pred: pred.earlyFinish, reverse=True)
            Node.setEarlyStart(sorted_list[0].earlyFinish)

    def calculateEarlyFinish(self, Node):
        if Node.getPredecessor() == []:
            Node.getEarlyFinish = Node.getTime()[self.index]
        Node.setEarlyFinish(Node.getEarlyStart() +
                            float(Node.getTime()[self.index]))

    def calculateLateFinish(self, Node):
        if Node.successors == []:
            Node.setLateFinish(Node.getEarlyFinish())
        else:
            Node.setLateFinish(min([x.getLateStart()
                               for x in Node.getSuccessor()]))

    def calculateLateStart(self, Node):
        Node.setLateStart(Node.getLateFinish() -
                          float(Node.getTime()[self.index]))

    def checkIfCritical(self, Node):
        if Node.getEarlyStart() == Node.getLateStart():
            Node.setCritical(True)
        else:
            Node.setCritical(False)

    def returnProject(self):
        return self.project


# loaderr = loader("Assignment 4\Warehouse.xlsx")
# nodes = loaderr.returnNodes()
# print("Nodes loaded")
# project = pert(nodes)
# print("Project loaded")
# calculatorr = calculator(project, 0)
# project = calculatorr.returnProject()
# printer(project)
# project = pert(nodes)
# print("Project loaded")
# calculatorr = calculator(project, 1)
# project = calculatorr.returnProject()
# printer(project)
# project = pert(nodes)
# print("Project loaded")
# calculatorr = calculator(project, 2)
# project = calculatorr.returnProject()
# printer(project)
loaderr = loader("Assignment 4\Villa.xlsx")
print("Nodes loaded")
project = pert(loaderr.returnNodes())
print("Project loaded")
calculatorr = calculator(project, 0)
project = calculatorr.returnProject()
# printer(project)
project = pert(loaderr.returnNodes())
print("Project loaded")
calculatorr = calculator(project, 1)
project = calculatorr.returnProject()
# printer(project)
project = pert(loaderr.returnNodes())
print("Project loaded")
calculatorr = calculator(project, 2)
project = calculatorr.returnProject()
# printer(project)
