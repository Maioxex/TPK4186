import chessgame as cg
import move as mv
import sys
import re
import matplotlib.pyplot as plt
from docx import Document
from docx.shared import Inches
import Newdoc as nd
from PIL import Image

#task 2: design functions to import a game from a text file
def ImportChessDataBase(filePath = "Assignement 2/Stockfish_15_64-bit.commented.[2600].pgn"):
    inputFile = open(filePath, "r")
    gameslist = ReadChessDataBase(inputFile)
    inputFile.flush()
    inputFile.close()
    return gameslist
    
def ReadLine(inputFile):
    line = inputFile.readline()
    if line=="":
        return None
    return line.rstrip()
    
def ReadChessDataBase(inputFile):
    listOfGames = []
    currentGame = cg.chessgame()
    step = 1
    line = ReadLine(inputFile)
    while True:
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
                    elif key == "PlyCount":
                        currentGame.setPlyCount(value)
                        listOfGames.append(currentGame)
                        currentGame = cg.chessgame()
                # print(key + " " + value)
                line = ReadLine(inputFile)
            # if re.match("\[", line):
            #     match = re.search("\[([a-zA-Z]+)", line)
            #     if match:
            #         key = match.group(1)
            #     match = re.search(r'"([^"]+)"', line)
            #     if match:
            #         value = match.group(1)
            #     print(key + " " + value)
            #     line = ReadLine(inputFile)
                if line==None:
                    break
                else:
                    step = 3
        elif step==3: # read moves
            line = ReadLine(inputFile)
            if line==None:
                break
            elif re.match("\[", line):
                step = 2
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

def getlengthofgames(gameslist):
    lengthofgames = []
    for each in gameslist:
        lengthofgames.append(each.getPlyCount())
    i = 0
    sortedliste = []
    midlertidigliste = []
    while len(lengthofgames)>0:
        for each in lengthofgames:
            if int(each) == i:
                midlertidigliste.append(int(each))
            sortedliste.append(len(midlertidigliste))
            print(len(midlertidigliste))
        for each in midlertidigliste:
            lengthofgames.remove(each)
        i += 1
        midlertidigliste = []
    return sortedliste
                
    
#testing of task 6 and 7
listresults = ImportChessDataBase()
print(findstatsforstockfish(listresults))
print("Total number of games: ", findtotalstatsstockfish(listresults))
doc = nd.report()
doc.addTitle("My Report")
doc.addParagraph("Stockfish 15 64-bit")
doc.addParagraph("Total number of games: " + str(findtotalstatsstockfish(listresults)))
doc.addParagraph("Wins, Losses, Draws")
doc.createtablestatdoc(findstatsforstockfish(listresults)[0], findstatsforstockfish(listresults)[1], findtotalstatsstockfish(listresults))
doc.save("my_report.docx")
gamesending = getlengthofgames(listresults)
print(gamesending)