# Authors: Martin Kristiansen Tømt og Nikolay Westengen group 32
import copy
import statistics
import numpy as np
import pandas as pd
import random
from Node import node as no
import xgboost as xgb
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler

# unchanged from pert 2


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

    def getNodeByName(self, name):
        for node in self.getNodes():
            if node.getName() == name:
                return node

    def getLengthOfProject(self):
        for node in self.getNodes():
            if node.getName() == "Completion" or node.getName() == "End":
                return node.getEarlyFinish()

# unchanged from pert 2


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

    def getNodesOrdered(self):
        df = pd.read_excel(self.filename)
        df = df.dropna(how='all')
        return df["Codes"].tolist()

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

# unchanged from pert 2


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

# minor changes from pert 2


class calculator:
    def __init__(self, project=None, index=1):
        self.index = index
        self.project = project
        self.calculate()
        # added basetime here as a convinience
        self.basetime = 371

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

    # now calculator also gives a classification of the project, thus why we need the basetime earlier
    def getClassifications(self):
        if self.returnTime() < self.basetime*1.05:
            return "Successfull"
        elif self.returnTime() < self.basetime*1.15:
            return "Acceptable"
        else:
            return "Failed"

# untouched from pert 2


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

    def appendFinishingTimes(self, time):
        self.finishingTimes.append(time)

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

# New class to solve task 4 and 5


class machinelearning:
    def __init__(self, project, nodes, basetime, algorithm, samples=1000):
        self.project = project
        self.projects = []
        self.risks = [0.8, 1, 1.2, 1.4]
        self.samples = samples
        # basetime have been checked multiple times to be 371 for villa when risk = 1.0
        self.basetime = basetime
        self.nodes = nodes
        self.algorithm = algorithm
        self.trainTestSplit = 0.2
        self.X_train = []
        self.X_test = []
        self.Y_train = []
        self.Y_test = []
        self.predictions = []
        print("Starting machine learning")
        self.addProjects(self.project)
        print("Finished adding projects")
        self.runAlgorithm(algorithm)
    # add the amount of randomly generated projects to the list of projects, as well as extract the data from them such that they can be used for machine learning prosesses

    def addProjects(self, project):
        for i in range(self.samples):
            self.addProject(project)
        self.extractData()

    # this allows us to change the algorithm used for machine learning, without having to create a new machinelearning object
    def setAlgorithm(self, algorithm):
        self.algorithm = algorithm

    # here we create the project, change it to fit a random risk, get the triangulated time for each node, calculate the time for the project, and then add it to the list of projects
    def addProject(self, project):
        project = copy.deepcopy(project)
        risk = random.choice(self.risks)
        for node in project.getNodes():
            if node.getName() == "Start" or node.getName() == "End" or node.getName() == "Completion":
                continue
            time = node.getTime()
            time[1] = float(time[1]) * risk
            if time[1] > float(time[2]):
                time[2] = time[1]
            elif time[1] < float(time[0]):
                time[0] = time[1]
            time[1] = random.triangular(
                float(time[0]), float(time[2]), float(time[1]))
            node.setTime(time)
        calculatorr = calculator(project)
        self.projects.append(
            [project, calculatorr.getClassifications(), calculatorr.returnTime()])

    # here we have the projects, their classification, and their time
    def extractData(self):
        for projectdata in self.projects:
            data = []
            for node in self.nodes:
                data.append(projectdata[0].getNodeByName(
                    node).getEarlyFinish())
            projectdata[0] = copy.deepcopy(data)
        # after cleaning out the data up to the gate point given by the user, we now format the data into training and testing data
        x = []
        y = []
        for projectdata in self.projects:
            x.append(projectdata[0])
            y.append([projectdata[1], projectdata[2]])
        self.X_train, self.X_test, self.Y_train, self.Y_test = train_test_split(
            x, y, test_size=self.trainTestSplit)

    # here we have an evaluation method that can be used to evaluate the performance of the machine learning algorithm
    # it takes in the type of algorithm, and then returns the accuracy of the algorithm
    def evaluate(self, type):
        ytest = []
        hits = 0
        misses = 0
        # here we do print the predicitons of the algorithm for the first two datasets, as well as the actual results, to see how well the algorithm is doing, as well as a sanity check
        print("Current predictions being:", self.predictions[0], self.predictions[1],
              "on these actual results:", self.Y_test[0], self.Y_test[1], "done by:")
        # if the algorithm is a classification algorithm, it will return the accuracy of the algorithm
        if type == "Classification":
            for datapoint in self.Y_test:
                ytest.append(datapoint[0])
            for i in range(len(self.predictions)):
                if self.predictions[i] == ytest[i]:
                    hits += 1
                else:
                    misses += 1
            return hits/(hits+misses)
        # if the algorithm is a regression algorithm, it will return the mean squared error of the algorithm
        elif type == "Regression":
            for datapoint in self.Y_test:
                ytest.append(datapoint[1])
            return mean_squared_error(ytest, self.predictions)

    # this function is meant to be used to run the machine learning algorithm, making sure that the correct algorithm is run
    def runAlgorithm(self, algorithm):
        if algorithm == "MLP":
            self.runMLPClassifier()
        elif algorithm == "DT":
            self.runDecisionTree()
        elif algorithm == "SVC":
            self.runSVC()
        elif algorithm == "Ridge":
            self.runRidge()
        elif algorithm == "RFR":
            self.runRandomForestRegressor()
        elif algorithm == "XGB":
            return self.runXGB()

    # first algorithm we chose to use was the MLPClassifier, which is a classification algorithm
    # we use the standard scaler to scale the data, and then we use the MLPClassifier to predict the classification of the data
    # we then evaluate the algorithm, and print the accuracy of the algorithm
    def runMLPClassifier(self):
        scaler = StandardScaler()
        scaler.fit(self.X_train)
        X_train_scaled = scaler.fit_transform(self.X_train)
        X_test_scaled = scaler.transform(self.X_test)
        mlp = MLPClassifier(hidden_layer_sizes=(
            80), activation="tanh", solver="lbfgs", max_iter=400)
        ytrain = []
        for value in self.Y_train:
            ytrain.append(value[0])
        mlp.fit(X_train_scaled, ytrain)
        self.predictions = mlp.predict(X_test_scaled)
        accuracy = self.evaluate("Classification")
        print(f"MLP accuracy: {accuracy}")

    # second algorithm we chose to use was the DecisionTreeClassifier, which is a classification algorithm
    def runDecisionTree(self):
        DT = DecisionTreeClassifier()
        ytrain = []
        for value in self.Y_train:
            ytrain.append(value[0])
        DT.fit(self.X_train, ytrain)
        self.predictions = DT.predict(self.X_test)
        accuracy = self.evaluate("Classification")
        print(f"Decision Tree accuracy: {accuracy}")

    # third algorithm we chose to use was the SVC, which is a classification algorithm
    def runSVC(self):
        SVM = SVC()
        ytrain = []
        for value in self.Y_train:
            ytrain.append(value[0])
        SVM.fit(self.X_train, ytrain)
        self.predictions = SVM.predict(self.X_test)
        accuracy = self.evaluate("Classification")
        print(f"SVM accuracy: {accuracy}")

    # fourth algorithm we chose to use was the Ridge, which is a regression algorithm
    # the regression algorithms are used to predict the time of the project, and not only if it will be within 5% of the actual time, or 15% of the actual time
    def runRidge(self):
        ridge = Ridge()
        ytrain = []
        for value in self.Y_train:
            ytrain.append(value[1])
        ridge.fit(self.X_train, ytrain)
        self.predictions = ridge.predict(self.X_test)
        accuracy = self.evaluate("Regression")
        print(f"Ridge MSE: {accuracy}")

    # fifth algorithm we chose to use was the RandomForestRegressor, which is a regression algorithm
    def runRandomForestRegressor(self):
        RFR = RandomForestRegressor()
        ytrain = []
        for value in self.Y_train:
            ytrain.append(value[1])
        RFR.fit(self.X_train, ytrain)
        self.predictions = RFR.predict(self.X_test)
        accuracy = self.evaluate("Regression")
        print(f"Random Forest Regressor MSE: {accuracy}")

    # sixth algorithm we chose to use was the XGBRegressor, which is a regression algorithm
    def runXGB(self):
        xgb_reg = xgb.XGBRegressor(
            objective='reg:squarederror', n_estimators=85, max_depth=3, learning_rate=0.085, min_child_weight=3, subsample=0.8, colsample_bytree=1.0)
        ytrain = []
        for value in self.Y_train:
            ytrain.append(value[1])
        xgb_reg.fit(self.X_train, ytrain)
        self.predictions = xgb_reg.predict(self.X_test)
        accuracy = self.evaluate("Regression")
        print(f"XGB MSE: {accuracy}")
        return accuracy


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

# Task 5:
# default is that we set the gate (or as we have called it stopnode) to be K.1, but we can change it to be whatever node we want
# the stopnode is used to find out how many nodes to collect data from, which is then used in the machine learning algorithms


def maintask5(stopnode="K.1"):
    print(f"\n\nStopnode is {stopnode}")
    loaderr = loader("Assignment 4\Villa.xlsx")
    project = pert(loaderr.returnNodes())
    nodes = loaderr.getNodesOrdered()
    templist = []
    # this is the different algorithms we used, and we run the MLPClassifier first, and then the rest of the algorithms
    algorithms = ["MLP", "DT", "SVC", "Ridge", "RFR", "XGB"]
    for node in nodes:
        if node == "Start":
            continue
        if node == stopnode:
            break
        templist.append(node)
    nodes = templist
    # when we instance a machinelearning object, we give it the project, the nodes, the stopnode, the first algorithm, and the number of simulations
    machine = machinelearning(project, nodes, 371, algorithms[0], 20000)
    # to avoid using differnt data for the different algorithms, so they are comparable, as well as saving time, we are instead of making a new object with new data, we just change the algorithm
    for algorithm in algorithms[1::]:
        print("\n")
        machine.setAlgorithm(algorithm)
        machine.runAlgorithm(algorithm)


# we here run it from three different gate nodes, to see if the results are different
maintask5("G.1")
maintask5("K.1")
maintask5("M.1")
