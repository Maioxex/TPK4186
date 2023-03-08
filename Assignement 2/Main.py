import chessgame as cg
import move as mv
import sys
import re

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
print(ImportChessDataBase())