class units:
    def __init__(self, tasks):
        self.time = 0
        self.tasks = tasks
        self.productiontimes = [0.5,3.5,1.2,3,0.8,0.5,1,1.9,0.3]
        self.currenttask = -1
    
    def getTasks(self):
        return self.tasks
    def getProductionTimes(self):
        return self.productiontimes
    def getTime(self):
        return self.time
    def getTask(self):
        return self.currenttask
    def setTask(self, task):
        self.currenttask = task
    def setTasks(self, tasks):
        self.tasks = tasks
    def setProductionTimes(self, productiontimes):
        self.productiontimes = productiontimes
    def setTime(self, time):
        self.time = time
