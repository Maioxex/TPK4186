import Ships as sh
import containerlist as cl

class docks:
    def __init__(self):
        pass
    
    def calculateUnloadTime1Crane(self, ship):
        containers = cl.containerlist()
        grid = ship.getGrid()
        for each in grid:
            for each2 in each:
                for each3 in each2:
                    if each3 != 0:
                        if containers.findContainer(each3.getId()) == "Container not found":
                            containers.addContainer(each3)
        return containers.getContainerListNrUniqs()*4

ship = ship = sh.ships(1, 18, 22, 23)
listo = cl.createRandomContainerList(500)
ship.loadShipWithContainerList(listo)
crane = docks()
print(crane.calculateUnloadTime1Crane(ship))
