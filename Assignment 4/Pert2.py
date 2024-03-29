# Authors: Martin Kristiansen Tømt og Nikolay Westengen Group 32
import copy
import statistics
import numpy as np
import pandas as pd
import random
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

    # change from Pert.py
    # here we added a function to get the time of the project, as that was the easiest way to get the length of the project for the statistics

    def getLengthOfProject(self):
        for node in self.getNodes():
            if node.getName() == "Completion" or node.getName() == "End":
                return node.getEarlyFinish()

# loader still the same


class loader:
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
        for index, rows in df.iterrows():
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
                    time = str(time).strip("()")
                    time = time.split(", ")
                    for tall in time:
                        tall = float(tall)
                task = no(name, time, predecessors, None, False, description)
            self.addNode(task)
        for node in self.nodes:
            sucsessors = []
            if node.getName() == "Completion" or node.getName() == "End":
                continue
            for node2 in self.nodes:
                if node2.getName() == "Start":
                    continue
                if node.getName() in node2.getPredecessor():
                    sucsessors.append(node2.getName())
            node.setSuccessor(sucsessors)

        for node in self.nodes:
            predecessors = []
            sucsessors = []
            if node.getName() != "Start":
                for i in range(len(node.getPredecessor())):
                    predecessors.append(
                        self.getNodeByName(node.getPredecessor()[i]))
            if node.getName() != "Completion" and node.getName() != "End":
                for i in range(len(node.getSuccessor())):
                    sucsessors.append(
                        self.getNodeByName(node.getSuccessor()[i]))
            node.setPredecessor(predecessors)
            node.setSuccessor(sucsessors)

# printer still the same


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

# calculator still the same


class calculator:
    def __init__(self, project=None, index=1):
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
        if Node.getName() == "Start":
            Node.setEarlyStart(0)
        else:
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

    def returnTime(self):
        return self.project.getNodes()[-1].getEarlyFinish()

# Task 4, the simulator for running the project 1000 times, with varying degrees of risk


class simulation:
    def __init__(self, project=None, index=1, risk=1, iterations=1000, basetime=0):
        self.project = project
        self.index = index
        self.risk = risk
        self.iterations = iterations
        self.finishingTimes = []
        self.stats = []
        if basetime == 0:
            calculatorr = calculator(copy.deepcopy(self.project), self.index)
            self.basetime = calculatorr.returnTime()
        self.simulate()
        self.runStats()

    # simple helping function
    def appendFinishingTimes(self, time):
        self.finishingTimes.append(time)
    # the main simulation function, it changes the times given for the projects nodes, and then runs the calculator to get the finishing time, before returning the time to the finishing times list

    def simulate(self):
        for i in range(self.iterations):
            project = copy.deepcopy(self.project)
            for node in project.getNodes():
                if node.getName() == "Start" or node.getName() == "End" or node.getName() == "Completion":
                    continue
                time = node.getTime()
                time[1] = float(time[1]) * self.risk
                if time[1] > float(time[2]):
                    time[2] = time[1]
                elif time[1] < float(time[0]):
                    time[0] = time[1]
                time[1] = random.triangular(
                    float(time[0]), float(time[2]), float(time[1]))
                node.setTime(time)
            calculatorr = calculator(project, self.index)
            self.appendFinishingTimes(calculatorr.returnTime())

    # this is the function that runs the statistics on the finishing times, to get the standard deviation, avarage, minimum, maximum, deciles and classification
    # classifications is stored in a list, with first index being sucsessfull, second acceptable, and third failed
    def runStats(self):
        std = statistics.stdev(self.finishingTimes)
        avarage = statistics.mean(self.finishingTimes)
        minimum = min(self.finishingTimes)
        maximum = max(self.finishingTimes)
        deciles = np.percentile(self.finishingTimes, np.arange(0, 100, 10))
        classification = [0, 0, 0]
        for time in self.finishingTimes:
            if time < self.basetime*1.05:
                classification[0] += 1
            elif time < self.basetime*1.15:
                classification[1] += 1
            else:
                classification[2] += 1
        self.stats = [std, avarage, minimum, maximum, deciles, classification]

    def returnStats(self):
        return self.stats


# Task 4 demonstration, the main function for running the simulation with the different risk values printed out in the terminal for easy reading
# deciles given in 10% intervals, with the first index being 10% and the last being 90% (as you already know the minimum and maximum there is no need for 0% and 100%)
def mainTask4():
    risk = [0.8, 1, 1.2, 1.4]
    loaderr = loader("Assignment 4\Villa.xlsx")
    print("Loaded Villa")
    for i in range(4):
        project = pert(loaderr.returnNodes())
        sim = simulation(project, 1, risk[i], 1000, 0)
        stats = sim.returnStats()
        print(
            f"simulation basetime: {sim.basetime} with risk {sim.risk}, avarage of {stats[1]}, classification of {stats[5][0]} sucsessfull, {stats[5][1]} acceptable and {stats[5][2]} failed, standard deviation of {stats[0]}, minimum of {stats[2]}, maximum of {stats[3]}, and deciles from 10-90%: {stats[4][1::]}\n")


mainTask4()
