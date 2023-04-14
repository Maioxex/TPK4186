import ChessGame as cg
#task 1
class chessgames:
    def __init__(self, games = []):
        self.games = games

    def addGame(self, game):
        self.games.append(game)

    def addGames(self, games):
        self.games.extend(games)

    def getGames(self):
        return self.games

    def setGames(self, games):
        self.games = games

    def printgames(self):
        for game in self.games:
            print(game.getWhite(), game.getBlack(), game.getResult(), game.getPlyCount())

    #task 3
    def printgamesfile(self, file = "chessgames.txt", state = "w"):
        file = open(file, state)
        for game in self.games:
            file.write(game.getWhite() + "," + game.getBlack() + "," + game.getResult() + "," + str(game.getPlyCount()))
    
    def extractgamesfromfile(self, file = "chessgames.txt"):
        file = open(file, "r")
        for each in file:
            each = each.split(",")
            game = cg.chessgame()
            game.setWhite(each[0])
            game.setBlack(each[1])
            game.setResult(each[2])
            game.setPlyCount(each[3])
            self.addGame(game)
    
