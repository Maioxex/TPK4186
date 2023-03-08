class chessgame:
    def __init__(self, moveset = [], player1 = None, player2 = None, result = None):
        self.moveset = moveset
        self.white = player1
        self.black = player2
        self.result = result
    
    
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