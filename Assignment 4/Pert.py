# Authors: Martin Kristiansen Tømt og Nikolay Westengen Group 32
import copy
import pandas as pd
from Node import node as no

# Task 1
# the Pert class for the pert Diagram


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

# Task 2 making a loader class for loading the excel file


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
    # we decided on using pandas as this is what we are most used to from earlier projects

    def load(self):
        df = pd.read_excel(self.filename)
        df = df.dropna(how='all')
        # we start with adding all the tasks to the pert diagram
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
                # we found out that the end node had different names in different files, so we had to make a check for this
                if name == "Completion" or name == "End":
                    time = [0, 0, 0]
                else:
                    # as the time was in a tuple, we decided to turn it into a list, to have everything we worked on in the same format
                    time = str(time).strip("()")
                    # There was some incosistencies in the file when it came to how time was written, som was written with a comma, and some with a comma and a space. We changed the data to make it consistentas we guessed this was simply a small mistake
                    time = time.split(", ")
                    for tall in time:
                        tall = int(tall)
                task = no(name, time, predecessors, None, False, description)
            self.addNode(task)
        # here we add the successors to the nodes
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
        # here we add the predecessors, and sucsessors to the nodes as node objects to make referencing easier
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

# Task 2 part 2 making the printer class for printing the pert diagram


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
            return
        print("Project:")
        for node in self.nodes:
            self.printNode(node)

    def printNode(self, Node):
        predacessors = Node.getNamesofPredaecessors()
        successors = Node.getNamesofSuccessors()
        print(f"Name: {Node.getName()}, description: {Node.getDescription()}, durations: {Node.getTime()}, early dates: {Node.earlyStart, Node.earlyFinish}, late dates: {Node.lateStart, Node.lateFinish}, critical: {Node.isCritical()}, predecessors: {predacessors}, successors: {successors}")

# task 3 making the calculator class for calculating the early and late start and finish


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
        # we start by calculating the early start and finish, we did this by adding flagged double for loops, to make sure that we only calculated the early start and finish for nodes that had no predecessors in the list we were working on
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
    # helping fucntions for calculating the early and late start and finish

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
                            int(Node.getTime()[self.index]))

    def calculateLateFinish(self, Node):
        if Node.successors == []:
            Node.setLateFinish(Node.getEarlyFinish())
        else:
            Node.setLateFinish(min([x.getLateStart()
                               for x in Node.getSuccessor()]))

    def calculateLateStart(self, Node):
        Node.setLateStart(Node.getLateFinish() -
                          int(Node.getTime()[self.index]))
    # helping function for checking if a node is critical

    def checkIfCritical(self, Node):
        if Node.getEarlyStart() == Node.getLateStart():
            Node.setCritical(True)
        else:
            Node.setCritical(False)

    # two other helping functions we got the need for
    def returnProject(self):
        return self.project

    def returnTime(self):
        return self.project.getNodes()[-1].getEarlyFinish()

# for the part of the assignment saying "Design functions to calculate the shortest,the expected and the longest duration of a project", we made a function for a calculatur giving us the time of that project
# by calling this with different initial values, we can get the shortest, expected and longest duration of the project (is all done as a part of the statistics of task 4, but baked into the code and not as seperate functions)
# as we can see all the times in the terminal for these durations when running the main function, we thought it was not necessary to make seperate functions for this in addition to what we do for task 4

# Here we have the main function, where we print out both the warehouse and the villa project, with the minimum, expected and maximum time as the base for calculations


def main():
    loaderr = loader("Assignment 4\Warehouse.xlsx")
    nodes = loaderr.returnNodes()
    print("Nodes loaded")
    project = pert(nodes)
    print("\n\nProject loaded: warehouse minimum time")
    calculatorr = calculator(project, 0)
    project = calculatorr.returnProject()
    printer(project)
    project = pert(nodes)
    print("\n\nProject loaded: warehouse expected time")
    calculatorr = calculator(project, 1)
    project = calculatorr.returnProject()
    printer(project)
    project = pert(nodes)
    print("\n\nProject loaded: warehouse maximum time")
    calculatorr = calculator(project, 2)
    project = calculatorr.returnProject()
    printer(project)
    loaderr = loader("Assignment 4\Villa.xlsx")
    nodes = loaderr.returnNodes()
    print("Nodes loaded:")
    project = pert(nodes)
    print("\n\nProject loaded: villa minimum time")
    calculatorr = calculator(project, 0)
    project = calculatorr.returnProject()
    printer(project)
    project = pert(nodes)
    print("\n\nProject loaded: villa expected time")
    calculatorr = calculator(project, 1)
    project = calculatorr.returnProject()
    printer(project)
    project = pert(nodes)
    print("\n\nProject loaded: villa maximum time")
    calculatorr = calculator(project, 2)
    project = calculatorr.returnProject()
    printer(project)


main()
