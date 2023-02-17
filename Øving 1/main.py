import docks
import Ships as sh
import containerlist as cl
import containers as c

#example of task 2,3,4:
listo = cl.createRandomContainerList(10)
cl.printContainerListToCSV(listo.getContainerList())
listo = cl.loadContainerListFromCSV()
for each in listo.getContainerList():
    print(each.getId(), each.getLength(), each.getselfvekt(), each.getLoad(), each.getTotalWeight())

# example task 5:
ship = sh.ships(1, 18, 22, 23)

#example task 6 and 7
listo = cl.createRandomContainerList(150)
print(listo.getContainerListLength())
print(ship.loadShipWithContainerList(listo))
ship.printShipLoadToFile()
print(ship.unloadShipToList())
ship.printShipLoadToFile()

print(ship.calculateShipTotalWeight())
print(ship.calculateTotalWeightStarboard())
print(ship.calculateTotalWeightPortside())
print(ship.calculateTotalWeightFront())
print(ship.calculateTotalWeightCenter())
print(ship.calculateTotalWeightBack())
print(ship.isShipBalanced())

