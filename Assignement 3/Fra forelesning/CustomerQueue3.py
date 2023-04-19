# CustomerQueue
#
# The objective of this program is to simulate the service of customers into a queue.
# New customers arrive in the queue with a frequency that is normally distributed (Poisson process) of rate m minutes.
# It takes between L and H minutes to serve a client.
# Only one customer can be served at a time.
# Customers are served first-in, first-out.
# The queue has an infinite capacity.

# 1. Imported Modules
# -------------------

import sys
import random
import matplotlib.pyplot as plt


# 2. Customers
# ------------

class Customer:
	NONE = 0
	WAITING = 1
	SERVING = 2
	SERVED = 3

	def __init__(self, identifier):
		self.identifier = identifier
		self.state = Customer.NONE
		self.arrivalTime = -1
		self.startServiceTime = -1
		self.completeServiceTime = -1

	def getIdentifier(self):
		return self.identifier

	def getState(self):
		return self.state

	def setState(self, state):
		self.state = state

	def serializeState(self):
		if self.state==Customer.NONE:
			return "None"
		if self.state==Customer.WAITING:
			return "waiting"
		if self.state==Customer.SERVING:
			return "serving"
		if self.state==Customer.SERVED:
			return "served"
		return "???"

	def getArrivalTime(self):
		return self.arrivalTime

	def setArrivalTime(self, time):
		self.arrivalTime = time

	def getStartServiceTime(self):
		return self.startServiceTime

	def setStartServiceTime(self, time):
		self.startServiceTime = time

	def getCompleteServiceTime(self):
		return self.completeServiceTime

	def setCompleteServiceTime(self, time):
		self.completeServiceTime = time

# 3. Queues
# ---------

class Queue:
	def __init__(self, capacity):
		self.capacity = capacity
		self.waitingCustomers = []
		self.currentlyServedCustomer = None

	def reset(self):
		self.waitingCustomers.clear()
		self.currentlyServedCustomer = None
		
	def getWaitingCustomers(self):
		return self.waitingCustomers

	def getNumberOfCustomersWaiting(self):
		return len(self.waitingCustomers)

	def isFull(self):
		return self.getNumberOfCustomersWaiting()==self.capacity

	def getCurrentlyServedCustomer(self):
		return self.currentlyServedCustomer

	def enqueueNewCustomer(self, customer, time):
		self.waitingCustomers.append(customer)
		customer.setState(Customer.WAITING)
		customer.setArrivalTime(time)

	def dequeueFirstWaitingCustomer(self):
		return self.waitingCustomers.pop(0)

	def startCustomerService(self, customer, time):
		self.currentlyServedCustomer = customer
		customer.setState(Customer.SERVING)
		customer.setStartServiceTime(time)

	def completeCustomerService(self, customer, time):
		self.currentlyServedCustomer = None
		customer.setState(Customer.SERVED)
		customer.setCompleteServiceTime(time)

# 4. Events
# ---------

class Event:
	NONE = 0
	CUSTOMER_ARRIVAL = 1
	START_CUSTOMER_SERVICE = 2
	COMPLETE_CUSTOMER_SERVICE = 3

	def __init__(self, type, customer, time):
		self.type = type
		self.customer = customer
		self.time = time

	def getType(self):
		return self.type

	def setType(self, type):
		self.type = type

	def serializeType(self):
		if self.type==Event.NONE:
			return "None"
		if self.type==Event.CUSTOMER_ARRIVAL:
			return "customerArrival"
		if self.type==Event.START_CUSTOMER_SERVICE:
			return "startCustomerService"
		if self.type==Event.COMPLETE_CUSTOMER_SERVICE:
			return "completeCustomerService"
		return "???"

	def getCustomer(self):
		return self.customer

	def getTime(self):
		return self.time

	def setTime(self, time):
		self.time = time

# 5. Scheduler
# ------------

class Scheduler:
	def __init__(self):
		self.events = []

	def reset(self):
		self.events.clear()

	def getEvents(self):
		return self.events

	def getNumberOfEvents(self):
		return len(self.events)
	
	def isEmpty(self):
		return len(self.events)==0

	def insertEvent(self, event):
		position = 0
		while position<self.getNumberOfEvents():
			scheduledEvent = self.events[position]
			if event.getTime()<scheduledEvent.getTime():
				break
			position += 1
		self.events.insert(position, event)

	def popFirstEvent(self):
		if self.isEmpty():
			return None
		return self.events.pop(0)

	def scheduleCustomerArrival(self, customer, time):
		event = Event(Event.CUSTOMER_ARRIVAL, customer, time)
		self.insertEvent(event)
		return event

	def scheduleStartCustomerService(self, customer, time):
		event = Event(Event.START_CUSTOMER_SERVICE, customer, time)
		self.insertEvent(event)
		return event

	def scheduleCompleteCustomerService(self, customer, time):
		event = Event(Event.COMPLETE_CUSTOMER_SERVICE, customer, time)
		self.insertEvent(event)
		return event

# 7. Printer
# ----------

class Printer:
	def __init__(self):
		self.separator = "\t"

	def printQueue(self, queue, outputFile):
		outputFile.write("Waiting customers\n")
		for customer in queue.getWaitingCustomers():
			self.printCustomer(customer, outputFile)
		outputFile.write("Served customer\n");
		customer = queue.getCurrentlyServedCustomer()
		if customer==None:
			outputFile.write("None\n")
		else:
			self.printCustomer(customer, outputFile)

	def printCustomer(self, customer, outputFile):
		outputFile.write("{0:s}".format(customer.getIdentifier()))
		outputFile.write(self.separator)
		outputFile.write("{0:s}".format(customer.serializeState()))
		outputFile.write(self.separator)
		outputFile.write("{0:g}".format(customer.getArrivalTime()))
		outputFile.write(self.separator)
		outputFile.write("{0:g}".format(customer.getStartServiceTime()))
		outputFile.write(self.separator)
		outputFile.write("{0:g}".format(customer.getCompleteServiceTime()))
		outputFile.write("\n")

	def printSchedule(self, scheduler, outputFile):
		outputFile.write("Scheduled events\n")
		for event in scheduler.getEvents():
			self.printEvent(event, outputFile)

	def printEvent(self, event, outputFile):
		outputFile.write("{0:s}".format(event.serializeType()))
		outputFile.write(self.separator)
		outputFile.write("{0:g}".format(event.getTime()))
		outputFile.write(self.separator)
		outputFile.write("{0:s}".format(event.getCustomer().getIdentifier()))
		outputFile.write("\n")

# 9. Simulator
# ------------

class Simulator:
	def __init__(self, queueCapacity):
		self.queue = Queue(queueCapacity)
		self.scheduler = Scheduler()
		self.printer = Printer()
		self.outputFile = sys.stdout
		self.customerMeanTimeBetweenArrivals = 2
		self.customerStandardDeviationArrivalIntervals = 1
		self.minimumCustomerServiceTime = 2
		self.maximumCustomerServiceTime = 5
		self.customers = []

	def reset(self):
		self.queue.reset()
		self.scheduler.reset()
		self.customers.clear()
		
	def getQueue(self):
		return self.queue

	def scheduleCustomerArrivals(self, arrivalTimes):
		customerIndex = 0
		for arrivalTime in arrivalTimes:
			customerIndex += 1
			customer = Customer("customer" + str(customerIndex))
			self.customers.append(customer)
			self.scheduler.scheduleCustomerArrival(customer, arrivalTime)

	def simulationLoop(self):
		ok = True
		try:
			while not self.scheduler.isEmpty():
				event = self.scheduler.popFirstEvent()
				self.performEvent(event)
		except:
			ok = False
		return ok

	def performEvent(self, event):
		customer = event.getCustomer()
		time = event.getTime()
		if event.getType()==Event.CUSTOMER_ARRIVAL:
			if self.queue.isFull():
				raise Exception("Queue is full")
			else:
				self.queue.enqueueNewCustomer(customer, time)
				self.updateCustomerService(time)
		elif event.getType()==Event.START_CUSTOMER_SERVICE:
			self.queue.startCustomerService(customer, time)
			completionTime = time + random.randrange(self.minimumCustomerServiceTime, self.maximumCustomerServiceTime)
			self.scheduler.scheduleCompleteCustomerService(customer, completionTime)
		elif event.getType()==Event.COMPLETE_CUSTOMER_SERVICE:
			self.queue.completeCustomerService(customer, time)
			self.updateCustomerService(time)

	def updateCustomerService(self, time):
		if self.queue.getCurrentlyServedCustomer()!=None:
			return
		if self.queue.getNumberOfCustomersWaiting()==0:
			return
		customer = self.queue.dequeueFirstWaitingCustomer()
		self.scheduler.scheduleStartCustomerService(customer, time)

	def printQueue(self):
		self.printer.printQueue(self.queue, self.outputFile)

	def printSchedule(self):
		self.printer.printSchedule(self.scheduler, self.outputFile)

	def printCustomerHistory(self):
		self.outputFile.write("Customers\n")
		for customer in self.customers:
			self.printer.printCustomer(customer, self.outputFile)

# 10. Optimizer
# -------------

class Optimizer:
	def __init__(self, queueCapacity):
		self.simulator = Simulator(queueCapacity)

	def runExperiment(self, arrivalTimes, numberOfExecutions):
		successfulExecutionCount = 0
		for _ in range(numberOfExecutions):
			self.simulator.reset()
			self.simulator.scheduleCustomerArrivals(arrivalTimes)
			successful = self.simulator.simulationLoop()
			if successful:
				successfulExecutionCount += 1
		return successfulExecutionCount

	def createArrivalTimes(self, numberOfCustomers, timeBetweenCustomers):
		return [i*timeBetweenCustomers for i in range(numberOfCustomers)]

	def studyTimeBetweenCustomers(self, numberOfCustomers, timeBetweenCustomers, numberOfExecutions):
		arrivalTimes = self.createArrivalTimes(numberOfCustomers, timeBetweenCustomers)
		count = self.runExperiment(arrivalTimes, numberOfExecutions)
		return count

	def studyTimesBetweenCustomers(self, numberOfCustomers, minimumTime, maximumTime, step, numberOfExecutions):
		times = []
		counts = []
		timeBetweenCustomers = minimumTime
		while timeBetweenCustomers<=maximumTime:
			count = self.studyTimeBetweenCustomers(numberOfCustomers, timeBetweenCustomers, numberOfExecutions)
			times.append(timeBetweenCustomers)
			counts.append(count)
			timeBetweenCustomers += step
		return (times, counts)

	def dichotomicStudyTimesBetweenCustomers(self, numberOfCustomers, minimumTime, maximumTime, numberOfExecutions, minimumExpectedSuccessProbability, maximumExpectedSuccessProbability):
		points = []

		lowTime = minimumTime
		count = self.studyTimeBetweenCustomers(numberOfCustomers, lowTime, numberOfExecutions)
		lowProbability = count/numberOfExecutions
		points.append((lowTime, lowProbability))

		highTime = maximumTime
		count = self.studyTimeBetweenCustomers(numberOfCustomers, highTime, numberOfExecutions)
		highProbability = count/numberOfExecutions
		points.append((highTime, highProbability))

		while True:
			mediumTime = (lowTime + highTime) / 2
			count = self.studyTimeBetweenCustomers(numberOfCustomers, mediumTime, numberOfExecutions)
			mediumProbability = count/numberOfExecutions
			points.append((mediumTime, mediumProbability))
			if mediumProbability<minimumExpectedSuccessProbability:
				lowTime = mediumTime
			elif mediumProbability>maximumExpectedSuccessProbability:
				highTime = mediumTime
			else:
				break

		points.sort(key = lambda point: point[0])
		times = []
		successProbabilities = []
		for point in points:
			times.append(point[0])
			successProbabilities.append(point[1])

		return (times, successProbabilities)



# 11. Test
# -------



queueCapacity = 3
optimizer = Optimizer(queueCapacity)

(times, successProbabilities) = optimizer.dichotomicStudyTimesBetweenCustomers(10, 1, 5, 100, 0.94, 0.96)
print(times)
print(successProbabilities)

plt.plot(times, successProbabilities)
plt.show()


		

