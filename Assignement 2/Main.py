import ChessGame as cg
import move as mv
import sys
import re
import matplotlib.pyplot as plt
from docx import Document
from docx.shared import Inches
import Newdoc as nd
from PIL import Image
import numpy as np
import chess.pgn
import tree as tr

#task 2: design functions to import a game from a text file
def ImportChessDataBase(filePath = "Assignement 2/Stockfish_15_64-bit.commented.[2600].pgn"):
    inputFile = open(filePath, "r")
    gameslist = ReadChessDataBase(inputFile, filePath)
    inputFile.flush()
    inputFile.close()
    return gameslist
        
def ReadLine(inputFile):
    line = inputFile.readline()
    if line=="":
        return None
    return line.rstrip()
    
def ReadChessDataBase(inputFile, filpath):
    antallgames = 100000
    listOfGames = []
    currentGame = cg.chessgame()
    step = 1
    line = ReadLine(inputFile)
    pgn = open(filpath)
    game = chess.pgn.read_game(pgn)
    board = game.board()
    moves = []
    i = 0
    while True:
        i +=1
        if step==1: # Read a game
            if line==None:
                break
            else:
                step = 2
        elif step==2: # Read meta-data
            if re.match("\[", line):
                match = re.search("\[([a-zA-Z]+)", line)
                if match:
                    key = match.group(1)
                match = re.search(r'"([^"]+)"', line)
                if match:
                    value = match.group(1)
                    if key == "White":
                        currentGame.setWhite(value)
                    elif key == "Black":
                        currentGame.setBlack(value)
                    elif key == "Result":
                        currentGame.setResult(value)
                        if value == "1-0":
                            currentGame.setWinner(currentGame.getWhite())
                        elif value == "0-1":
                            currentGame.setWinner(currentGame.getBlack())
                        else:
                            currentGame.setWinner("Draw")
                    elif key == "PlyCount":
                        currentGame.setPlyCount(value)
                        listOfGames.append(currentGame)
                        
                        for move in game.mainline_moves():
                            moves.append(board.san(move))
                            board.push(move)
                        currentGame.setMoves(moves)
                        moves = []
                        game = chess.pgn.read_game(pgn)
                        board = game.board()
                        currentGame = cg.chessgame()

                line = ReadLine(inputFile)
                if line==None:
                    break
                else:
                    step = 3
        elif step==3: # read moves
            line = ReadLine(inputFile)
            if line==None:
            # if line==None or antallgames*3 <= i:
                break
            elif re.match("\[", line):
                step = 2
    pgn.close()
    return listOfGames

def findstatsforstockfish(gameslist):
    #index 0 = wins, 1 = losses, 2 = draws
    whiteresults = [0,0,0]
    blackresults = [0,0,0]
    
    for each in gameslist:
        if each.getWhite() == "Stockfish 15 64-bit":
            if each.getResult() == "1-0":
                whiteresults[0] += 1
            elif each.getResult() == "0-1":
                whiteresults[1] += 1
            elif each.getResult() == "1/2-1/2":
                whiteresults[2] += 1
        else:
            if each.getResult() == "1-0":
                blackresults[0] += 1
            elif each.getResult() == "0-1":
                blackresults[1] += 1
            elif each.getResult() == "1/2-1/2":
                blackresults[2] += 1
    return whiteresults, blackresults

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
    plt.xlabel("Number of moves")
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
    for each in results:
        for i in range(len(each.getMoves())):
            if i ==0:
                currentTree = root
            currentTree.createChildren(each.getMoves()[i])
            currentTree = currentTree.getChild(each.getMoves()[i])
    return root

#testing of task 6 and 7
listresults = ImportChessDataBase()
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
doc.createtabletma4240doc(calculateaveragelengthofgame(listresults),calculatestandarddeviationoflenghthofgame(listresults),calculateaveragelengthofgame(listresults, "white"),calculateaveragelengthofgame(listresults, "black"),calculatestandarddeviationoflenghthofgame(listresults, "white"),calculatestandarddeviationoflenghthofgame(listresults, "black"), calculatestandarddeviationoflenghthofgame(listresults, "none", "wins"),calculateaveragelengthofgame(listresults, "none", "wins"), calculatestandarddeviationoflenghthofgame(listresults, "none", "losses"), calculateaveragelengthofgame(listresults, "none", "losses"))
doc.save("my_report.docx")
tree = createtree(listresults)
# tree.printTreetocount(20)
tree.printTreetodepth(10)

# while True:
#     root = tree
#     print(tree.getChildren())
#     for each in tree.getChildren():
#         print(each.getMove(), each.getCount(), each.getIsEndNode())
#     if root.getIsEndNode() != True:
#         tree = tree.getChildren()[0]
#     else:
#         break


