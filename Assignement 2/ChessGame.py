from move import move

class chessgame:
    def __init__(self, moveset = [], player1 = None, player2 = None, result = None, plyCount = None):
        self.moveset = moveset
        self.white = player1
        self.black = player2
        self.result = result
        self.plyCount = plyCount
    
    
    def addMove(self, move):
        self.moveset.append(move)
        
    def addMoves(self, moves):
        self.moveset.extend(moves)
    
    def getMoves(self):
        return self.moveset
    
    def setMoves(self, moves):
        self.moveset = moves
    
    def getWhite(self):
        return self.white
    
    def setWhite(self, player):
        self.white = player
    
    def getBlack(self):
        return self.black

    def setBlack(self, player):
        self.black = player
    
    def getResult(self):
        return self.result

    def setResult(self, result):
        self.result = result
    
    def getPlyCount(self):
        return self.plyCount
    
    def setPlyCount(self, plyCount):
        self.plyCount = plyCount
    
    def printgametofile(self, file = "chessgame.txt"):
        file = open(file, "w")
        file.write(self.white, self.black, self.result, self.plyCount)
        file.flush()
        file.close()
        
    def extractgamefromfile(self, file = "chessgame.txt"):
        file = open(file, "r")
        for each in file:
            each = each.split(",")
            self.setWhite(each[0])
            self.setBlack(each[1])
            self.setResult(each[2])
            self.setPlyCount(each[3])
        file.flush()
        file.close()