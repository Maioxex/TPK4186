class Scheduler:
	def __init__(self):
		self.actions = []

	def getActions(self):
		return self.actions

	def getNumberOfActions(self):
		return len(self.actions)
	
	def isEmpty(self):
		return len(self.actions)==0

	def insertAction(self, action):
		position = 0
		while position<self.getNumberOfActions():
			scheduledAction = self.actions[position]
			if action.getCompletionDate()<scheduledAction.getCompletionDate():
				break
			position += 1
		self.actions.insert(position, action)

	def popFirstAction(self):
		if self.isEmpty():
			return None
		return self.actions.pop(0)

class Action:
	def __init__(self, name, completionDate):
		self.name = name
		self.completionDate = completionDate

	def getName(self):
		return self.name

	def getCompletionDate(self):
		return self.completionDate

	def setCompletionDate(self, date):
		self.completionDate = date