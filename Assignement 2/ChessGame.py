from move import move

class chessgame:
    def __init__(self, moveset = [], player1 = None, player2 = None, result = None, plyCount = None):
        self.moveset = moveset
        self.white = player1
        self.black = player2
        self.result = result
        self.plyCount = plyCount
    
    def toString(self):
        if self.white == None:
            white = "None"
        else:
            white = self.white
        if self.black == None:
            black = "None"
        else:
            black = self.black
        if self.result == None:
            result = "None"
        else:
            result = self.result
        if self.plyCount == None:
            plyCount = "None"
        else:
            plyCount = str(self.plyCount)    
        return white + " " + black + " " + result + " " + plyCount

    
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
    
    def printgametofile(self, file = "chessgame.txt", state = "w"):
        file = open(file, state)
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
    
    def exporttoexcel(self, file = "chessgame.xlsx"):
        import pandas as pd
        data = {'White': [self.white],
                'Black': [self.black],
                'Result': [self.result],
                'PlyCount': [self.plyCount]}
        df = pd.DataFrame(data)
        df.to_excel(file, index=False)
    
    def importfromexcel(self, file = "chessgame.xlsx"):
        import pandas as pd
        df = pd.read_excel(file)
        self.setWhite(df['White'][0])
        self.setBlack(df['Black'][0])
        self.setResult(df['Result'][0])
        self.setPlyCount(df['PlyCount'][0])

# cg = chessgame([], "White", "Black", "1-0", 10)
# cg.exporttoexcel()
# cg2 = chessgame()
# print(cg2.toString())
# cg2.importfromexcel()
# print(cg2.toString())