#TPK4186-2023-Assignment1-Group32, Martin Kristiansen Tømt, Nikolay Westengen

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

#example task 6, 7 and 8:
listo = cl.createRandomContainerList(100)
print(listo.getContainerListLength())
ship.loadShipWithContainerList(listo)
ship.printShipLoadToFile()
print(ship.unloadShipToList())

#task 9 and 10:
listo = cl.createRandomContainerList(1000)
ship.loadShipWithContainerList(listo)
print("ship total weight: ", ship.calculateShipTotalWeight())
print("weight starboarad: ", ship.calculateTotalWeightStarboard())
print("weight portside: ", ship.calculateTotalWeightPortside())
print("weight  front: ",ship.calculateTotalWeightFront())
print("weight center: ",ship.calculateTotalWeightCenter())
print("weight back:", ship.calculateTotalWeightBack())
print("is balanced: ", ship.isShipBalanced())

#task 11:
ship = ship = sh.ships(1, 18, 22, 23)
listo = cl.createRandomContainerList(370)
ship.loadShipWithContainerList(listo)
crane = docks.docks()
print("time to load of with 1 crane: ", crane.calculateUnloadTime1Crane(ship))
#unfortunately we didnt quite get the 4 cranes to work, but we have tried our best, check out the entire docks.py file for how we tried to do it.
#print(crane.calculateUnloadTime4Crane(ship))