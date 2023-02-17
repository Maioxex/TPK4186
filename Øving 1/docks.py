import Ships as sh
import containerlist as cl

class docks:
    def __init__(self):
        pass
    
    def calculateUnloadTime1Crane(self, ship):
        #returnerer tid i minutter
        containers = cl.containerlist()
        grid = ship.getGrid()
        for each in grid:
            for each2 in each:
                for each3 in each2:
                    if each3 != 0:
                        if containers.findContainer(each3.getId()) == "Container not found":
                            containers.addContainer(each3)
        return containers.getContainerListNrUniqs()*4

    def calculateUnloadTime4Crane(self, ship, times = 0):
        sections = [[0,5],[6,11],[12,16],[17,22]]
        print(ship.calculateShipTotalWeight())
        dimensions = ship.getSize()
        # bays = [0,0,0,0]
        activebays=[[False,-2],[False,-2],[False,-2],[False,-2]]
        grid = ship.getGrid()
        time = times
        for i in range(ship.getSize()[0]):
            for j in range(ship.getSize()[1]):
                for k in range(ship.getSize()[2]):
                    if grid[ship.getSize()[0]-i-1][j][k] != 0:
                        if k >= 0 and k <= 5 and not activebays[0][0]:
                            activebays[0] = [True, k]
                            ship.removeContainer(grid[ship.getSize()[0]-i-1][j][k])
                        if k >= 6 and k <= 11 and not activebays[1][0]:
                            activebays[1] = [True, k]
                            ship.removeContainer(grid[ship.getSize()[0]-i-1][j][k])
                        if k >= 12 and k <= 16 and not activebays[2][0]:
                            activebays[2] = [True, k]
                        if k >= 17 and k <= 22 and not activebays[3][0]:
                            activebays[3] = [True, k]
        time += 4
        ship.setGrid(grid)
        if ship.ShipLoadded():
            return time + self.calculateUnloadTime4Crane(ship, time)
        return time
        
            
       
            

