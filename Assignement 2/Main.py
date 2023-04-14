#Martin Kristiansen Tømt og Nikolay Westengen assignment 2

import chessgame as cg
import re
import matplotlib.pyplot as plt
from docx import Document
from docx.shared import Inches
import Newdoc as nd
import numpy as np
import tree as tr


#pgn parser:
class PGNGame:
    def __init__(self, headers, moves):
        self.headers = headers
        self.moves = moves
#task 
def ImportChessDataBase(filePath = "Assignement 2/Stockfish_15_64-bit.commented.[2600].pgn"):
    # inputFile = open(filePath, "r")
    gameslist = ReadChessDataBase(filePath)
    # inputFile.flush()
    # inputFile.close()
    return gameslist
        
def ReadLine(inputFile):
    line = inputFile.readline()
    if line=="":
        return None
    return line.rstrip()

#the parsing functions
def parse_pgn_headers(lines):
    headers = {}
    for line in lines:
        if line.startswith("["):
            key, value = line[1:-1].split(" ", 1)
            if headers.get(key) is None:
                headers[key.strip()] = [value.strip('"')]
            else:
                headers[key.strip()].append(value.strip('"'))
    return headers


def parse_pgn_moves(lines):
    moves = []
    for line in lines:
        if not line.startswith("["):
            moves.extend(line.strip().split())
    return moves


def read_chess_game(filePath):
    with open(filePath, "r", encoding="utf-8") as file:
        content = file.read()

    pattern = re.compile(r'\{[^}]*\}')
    content = pattern.sub('', content).replace("  ", " ")

    lines = content.splitlines()
    headers = parse_pgn_headers(lines)
    moves = parse_pgn_moves(lines)

    return PGNGame(headers, moves)


def ReadChessDataBase(inputFile):
    datafrompgn = read_chess_game(inputFile)
    datafrompgn.moves = [move for move in datafrompgn.moves if not move.endswith(".")]
    # print(datafrompgn.moves)
    # print(len(datafrompgn.moves))
    listOfGames = []
    movescount = 0
    # for i in range(0, 2):
    for i in range(0, len(datafrompgn.headers["Event"])):
        moves = []
        currentGame = cg.chessgame()
        currentGame.setWhite(datafrompgn.headers["White"][i])
        currentGame.setBlack(datafrompgn.headers["Black"][i])
        currentGame.setResult(datafrompgn.headers["Result"][i])
        if datafrompgn.headers["Result"][i] == "1-0":
            currentGame.setWinner(currentGame.getWhite())
        elif datafrompgn.headers["Result"][i] == "0-1":
            currentGame.setWinner(currentGame.getBlack())
        else:
            currentGame.setWinner("Draw")
        currentGame.setPlyCount(datafrompgn.headers["PlyCount"][i])
        for j in range(movescount, movescount + int(datafrompgn.headers["PlyCount"][i])):
            moves.append(datafrompgn.moves[j])
            movescount += 1
        movescount +=  1
        currentGame.setMoves(moves)
        
        listOfGames.append(currentGame)

    
    return listOfGames

    
        
    
    
    # i = 0
    # while True:
    #     if step==1: # Read a game
    #         if line==None:
    #             break
    #         else:
    #             step = 2
    #     elif step==2: # Read meta-data
    #         if re.match("\[", line):
    #             match = re.search("\[([a-zA-Z]+)", line)
    #             if match:
    #                 key = match.group(1)
    #             match = re.search(r'"([^"]+)"', line)
    #             if match:
    #                 value = match.group(1)
    #                 #print(key, value)
    #                 if key == "White":
    #                     currentGame.setWhite(value)
    #                 elif key == "Black":
    #                     currentGame.setBlack(value)
    #                 elif key == "Result":
    #                     currentGame.setResult(value)
    #                     if value == "1-0":
    #                         currentGame.setWinner(currentGame.getWhite())
    #                     elif value == "0-1":
    #                         currentGame.setWinner(currentGame.getBlack())
    #                     else:
    #                         currentGame.setWinner("Draw")
    #                 elif key == "PlyCount":
    #                     currentGame.setPlyCount(value)
    #                     listOfGames.append(currentGame)
    #                     #Task 10: add moves to game
    #                     for move in game.mainline_moves():
    #                         moves.append(board.san(move))
    #                         board.push(move)
    #                     currentGame.setMoves(moves)
    #                     moves = []
    #                     game = chess.pgn.read_game(pgn)
    #                     board = game.board()
    #                     currentGame = cg.chessgame()
    #         #line = ReadLine(inputFile)
    #         if line==None:
    #             break
    #         else:
    #                 step = 3
    #     elif step==3:
    #         line = ReadLine(inputFile)
    #         i += 1
    #         if i == 144202:
    #             #print("hei")
    #             break
    #         if line==None:
    #         #if line==None or antallgames*3 <= i:
    #             break
    #         elif re.match("\[", line):
    #             step = 2
    # pgn.close()
    # return listOfGames

def findstatsforstockfish(gameslist):
    #index 0 = wins, 1 = losses, 2 = draws
    stockstatsWhite = [0,0,0]
    stockstatsBlack = [0,0,0]
    for game in gameslist:
        if game.getWinner() == "Draw":
            if game.getWhite() == "Stockfish 15 64-bit":
                stockstatsWhite[2] += 1
            else:
                stockstatsBlack[2] += 1
        elif game.getWinner() == "Stockfish 15 64-bit":
            if game.getWhite() == "Stockfish 15 64-bit":
                stockstatsWhite[0] += 1
            else:
                stockstatsBlack[0] += 1
        else:
            if game.getWhite() == "Stockfish 15 64-bit":
                stockstatsWhite[1] += 1
            else:
                stockstatsBlack[1] += 1
    #print(stockstatsWhite, stockstatsBlack)
    
    return stockstatsWhite, stockstatsBlack

def findtotalstatsstockfish(gameslist):
    whiteresults, blackresults = findstatsforstockfish(gameslist)
    total =[0,0,0]
    total[0] = int(whiteresults[0] + blackresults[0])
    total[1] = int(whiteresults[1] + blackresults[1])
    total[2] = int(whiteresults[2] + blackresults[2])
    return total

def getlengthofgames(gameslist, string = "none", wins = "none"):
    lengthofgames = []
    for each in gameslist:
        if string == "none":
            if wins == "wins":
                if each.getWinner() == "Stockfish 15 64-bit":
                    lengthofgames.append(int(each.getPlyCount()))
            elif wins == "losses":
                if each.getWinner() != "Stockfish 15 64-bit" and each.getWinner() != "Draw":
                    lengthofgames.append(int(each.getPlyCount()))
            elif wins == "none":
                lengthofgames.append(int(each.getPlyCount()))
        elif string == "white":
            if each.getWhite() == "Stockfish 15 64-bit":
                lengthofgames.append(int(each.getPlyCount()))
        elif string == "black":
            if each.getWhite() != "Stockfish 15 64-bit" :
                lengthofgames.append(int(each.getPlyCount()))
    endingstates = {}
    for each in lengthofgames:
        if each in endingstates:
            endingstates[each] += 1
        else:
            endingstates[each] = 1
    endlist = []
    # print(lengthofgames)
    for i in range(1, np.max(lengthofgames) + 1):
        if i in endingstates:
            endlist.append(endingstates[i])
        else:
            endlist.append(0)
    return endlist

def howmanystillgoing(gameslist, string = "none", wins = "none"):
    total = len(gameslist)
    whitegames, blackgames = findstatsforstockfish(gameslist)
    winess = whitegames[0] + blackgames[0]
    losses = whitegames[1] + blackgames[1]
    if string == "white":
        total = sum(whitegames)
    elif string == "black":
        total = sum(blackgames)
    elif wins == "wins":
        total = winess
    elif wins == "losses":
        total = losses
    current = total
    endingeach = getlengthofgames(gameslist, string, wins)
    eachleft = []
    #if wins == "losses":
    #    print(sum(endingeach))
    for each in endingeach:
        current -= each
        eachleft.append(current/total*100)
    return eachleft



def plotting(gameslist, name,  string = "none", wins = "none"):
    # plt.plot(getlengthofgames(gameslist))
    # plt.xlabel("Number of moves")
    # plt.ylabel("Number of games")
    # plt.title("Number of games that end with each number of moves")
    # plt.show()
    
    if string == "white":
        colors = "cyan"
    elif string == "black":
        colors = "black"
    elif string == "none":
        if wins == "wins":
            colors = "green"
        elif wins == "losses":
            colors = "red"    
        else: colors = "gray"
    if string == "none" and wins == "none":
        plt.figure(figsize=(10, 6))
    plt.plot(howmanystillgoing(gameslist, string, wins), color = colors)
    plt.xlabel("Number of half moves")
    plt.ylabel("Percentage of games still going")
    plt.title("Number of games that are still going after each number of moves")
    plt.legend(["All","White", "Black",  "Wins", "Losses"])
    plt.savefig(name)

def calculateaveragelengthofgame(gameslist, string = "none", wins = "none"):
    endingeach = getlengthofgames(gameslist, string, wins)
    weightedsum = 0
    whitegames, blackgames = findstatsforstockfish(gameslist)
    lens = len(gameslist)
    if string == "white":
        lens = sum(whitegames)
    elif string == "black":
        lens = sum(blackgames)
    elif wins == "wins":
        lens = whitegames[0] + blackgames[0]
    elif wins == "losses":
        lens = whitegames[1] + blackgames[1]
    for i in range(len(endingeach)):
        weightedsum += (i+1)*endingeach[i]
    return weightedsum/lens

def calculatestandarddeviationoflenghthofgame(gameslist, string = "none", wins = "none"):
    endingeach = getlengthofgames(gameslist, string, wins)
    whitegames, blackgames = findstatsforstockfish(gameslist)
    lens = len(gameslist)
    if string == "white":
        lens = sum(whitegames)
    elif string == "black":
        lens = sum(blackgames)
    weightedsum = 0
    for i in range(len(endingeach)):
        weightedsum += (i+1)*endingeach[i]
    average = weightedsum/lens
    weightedsum = 0
    for i in range(len(endingeach)):
        weightedsum += ((i+1)-average)**2*endingeach[i]
    return np.sqrt(weightedsum/lens)        

def plotssss(name, listresults):
    plotting(listresults,name)
    plotting(listresults,name, "white")# 
    plotting(listresults,name, "black")
    plotting(listresults,name, "none", "wins")
    plotting(listresults,name, "none", "losses")   
    
def createtree(results):
    root = tr.tree("start")
    root.setRoot(True)
    # a = 1
    for each in results:
        # print(a)
        # a +=1
        if each.getWinner() == "Draw":
            stat = [0,0,1]
        elif each.getWinner() == each.getWhite():
            stat = [1,0,0]
        elif each.getWinner() == each.getBlack():
            stat = [0,1,0]
        for i in range(len(each.getMoves())):
            if i == 0:
                currentTree = root
            currentTree.createChildren(each.getMoves()[i], stat)
            # baby = currentTree.getChild(each.getMoves()[i])
            # if each.getWinner() == each.getWhite():
            #     baby.addwin()
            # elif each.getWinner() == each.getBlack():
            #     baby.addloss()
            #     print(currentTree.getChild(each.getMoves()[i]).getMetadata())
            # elif each.getWinner() == "Draw":
            #     baby.adddraw()
            currentTree = currentTree.getChild(each.getMoves()[i])
    return root
#testing task 4:
listresults = ImportChessDataBase()
#testing task 3:
listresults[0].printgametofile("game1.txt")
cg1 = cg.chessgame()
print("step 1")
cg1.extractgamefromfile("game1.txt")
print("step 2")
print(cg1.toString(), listresults[0].toString())
#testing task 5:
listresults[1].exporttoexcel("game2.xlsx")
print("step 3")
cg2 = cg.chessgame()
cg2.importfromexcel("game2.xlsx")
print("step 4")
print(cg2.toString(), listresults[1].toString())

#testing of task 6 and 7 
print("step 5")
plotssss("gamesstillgoing.png", listresults)
doc=nd.report()
doc.addTitle("My Report")
doc.addParagraph("Stockfish 15 64-bit")
doc.addParagraph("Total number of games: " + str(findtotalstatsstockfish(listresults)))
doc.addParagraph("Wins, Losses, Draws")
doc.createtablestatdoc(findstatsforstockfish(listresults)[0], findstatsforstockfish(listresults)[1], findtotalstatsstockfish(listresults))
gamesending = howmanystillgoing(listresults)
plotssss("gamesstillgoing.png", listresults)
doc.addPlot("gamesstillgoing.png")
print("step 6")
#task 8
doc.createtabletma4240doc(calculateaveragelengthofgame(listresults),calculatestandarddeviationoflenghthofgame(listresults),calculateaveragelengthofgame(listresults, "white"),calculateaveragelengthofgame(listresults, "black"),calculatestandarddeviationoflenghthofgame(listresults, "white"),calculatestandarddeviationoflenghthofgame(listresults, "black"), calculatestandarddeviationoflenghthofgame(listresults, "none", "wins"),calculateaveragelengthofgame(listresults, "none", "wins"), calculatestandarddeviationoflenghthofgame(listresults, "none", "losses"), calculateaveragelengthofgame(listresults, "none", "losses"))
#task 9 and 10
print("step 7")
tree = createtree(listresults)
print("step 8")
#task 11 and 12 functions showing the moves given depth and count
tree.printTreetodepth(3, doc)
tree.printTreetocount(300, doc)
print("step 9")
doc.save("my_report.docx")
print("done")



