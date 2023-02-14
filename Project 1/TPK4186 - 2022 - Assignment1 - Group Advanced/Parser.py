# Structure to read tokens from a file and create DTMC's and probability distributions
#Task 6 and 7

import sys
import re 
from Control import *

def Reader_TextfileToListOfTokens(filename):
  reservedWords = ["MarkovChain", "ProbabilityDistribution", "of", "end"] 
  sourceName = filename
  input = open(sourceName, "r")
  tokens = []
  lineNumber = 0
  for line in input:
      count = 0
      lineNumber += 1
      line = line.rstrip()
      newLine = re.sub(r"#.*", r"", line)
      while newLine!="":
          if re.match(r"^[ \t]+", newLine):
              match = re.match(r"^[ \t]+", newLine).group()
              count += len(match)
              newLine = re.sub(r"^[ \t]+", "", newLine)
          elif re.match(r"[a-zA-Z_][a-zA-Z0-9_]*", newLine):
              tmpCount = count
              identifier = re.match(r"[a-zA-Z_][a-zA-Z0-9_]*", newLine).group()
              count += len(identifier)
              newLine = re.sub(r"^[a-zA-Z_][a-zA-Z0-9_]*", "", newLine)
              if identifier in reservedWords:
                tokens.append(["Reserved",identifier,lineNumber, tmpCount])
              else: 
                tokens.append(["Identifier",identifier,lineNumber, tmpCount])
          elif re.match(r'"[^"]*"', newLine):
              tmpCount = count
              string = re.match(r'"[^"]*"', newLine).group()
              count += len(string)
              newLine = re.sub(r'"[^"]*"', "", newLine)
              tokens.append(["String",string,lineNumber, tmpCount])
          elif re.match(r"[\-0-9][0-9]*\.[0-9][0-9]*", newLine):
              tmpCount = count
              number = re.match(r"[\-0-9][0-9]*\.[0-9][0-9]*", newLine).group()
              count += len(number)
              newLine = re.sub(r"[\-0-9][0-9]*\.[0-9][0-9]*", "", newLine)
              tokens.append(["Number",number,lineNumber, tmpCount])
          elif re.match(r"[\-][\>]", newLine):
              tmpCount = count
              arrow = re.match(r"[\-][\>]", newLine).group()
              count += len(arrow)
              newLine = re.sub(r"[\-][\>]", "", newLine)
              tokens.append(["Arrow",arrow,lineNumber, tmpCount])
          else:              
              tmpCount = count
              character = newLine[0]
              count += len(character)
              newLine = newLine[1:]
              tokens.append(["Character", character,lineNumber, tmpCount])     
  input.close()
  return tokens

def Token_GetNameDTMCProbdist(ListOfTokens):
  if ListOfTokens[0][0][1] == "MarkovChain":
    return ListOfTokens[0][1][1]
  else:
    return ListOfTokens[0][3][1]


#Production of 4D lists, now working. 
def Token_SplitNestedList(NestedListOfTokens):
    newList = []
    tmpList = []
    for List in NestedListOfTokens:
        if List[1] == "end":
            tmpList.append(List)
            newList.append(tmpList)  
            tmpList = []
            continue
        else: 
            tmpList.append(List)
    return newList

def Format2LineList(paragraph):
    newList = []
    lineList = []
    lineCount = paragraph[0][2]
    for token in paragraph:
      if token[2] == lineCount: 
        lineList.append(token)
      else: 
        newList.append(lineList)
        lineList = []
        lineCount += 1
        lineList.append(token)
        if token[1] == "end":
          newList.append(lineList)
          lineList = []
          lineCount += 1 
    return newList

def createReadableTokenList(ParagraphTokens):
    finalList = []
    for paragraph in ParagraphTokens:
      finalList.append(Format2LineList(paragraph))
    return finalList



#---------------------------------------------------------------

# Task 8

def Parse_GetDTMC_or_ProbDist(listOfTokens):
  return listOfTokens[0][0][1]

def ParseDTMCandProbdistOnce(paragraph, DTMCandProbDist_Container,dtmcContainer):
  DTMC_name = Token_GetNameDTMCProbdist(paragraph)
  if Parse_GetDTMC_or_ProbDist(paragraph) == "MarkovChain":
    return ParseDTMC(paragraph, dtmcContainer, DTMC_name)
  elif Parse_GetDTMC_or_ProbDist(paragraph) == "ProbabilityDistribution":
    return ParseProbDist(paragraph,DTMCandProbDist_Container, dtmcContainer, DTMC_name)
  return None

def ParseDTMC(listOfTokens, dtmcContainer, DTMC_name):
  if dtmcContainer.get(DTMC_name) == None:
      for line in listOfTokens:
        if line[0][1] == "MarkovChain":
          DTMC = DTMCTemp_Container_NewDTMC(dtmcContainer,DTMC_name)
          continue 
        if line[0][1] == "end":
          dtmcContainer[DTMC_name] = DTMC
          return DTMC
        sourceState = States_New(line[0][1])
        targetState = States_New(line[2][1])
        DTMC_NewState(DTMC, States_GetName(sourceState))
        DTMC_NewState(DTMC, States_GetName(targetState))
        probabilityFrequency = float(line[4][1])
        DTMC_NewTransition(DTMC,sourceState,targetState,probabilityFrequency)
  else:
    return None

def ParseProbDist(paragraph,container, dtmcContainer, DTMC_name):
  DTMC = dtmcContainer.get(DTMC_name)
  for line in paragraph:
    if line[0][1] == "ProbabilityDistribution":
      testName = line[1][1]
      Probdist = DTMC_Container_NewProdDist(container,testName,DTMC)
      continue
    elif line[0][1] == "end":
      if DTMCandProbDistCheck_TransitionProbabilities(Probdist):
        return Probdist
      else:
        return None
    probability = float(line[2][1])
    state = States_New(line[0][1])
    ProbDist_NewProbability(Probdist,probability,state)
  return None

def Parse_TokensFromFile(filename):
  listOfTokensFromFile = Reader_TextfileToListOfTokens(filename)
  listOfParagraphsFromTokens = Token_SplitNestedList(listOfTokensFromFile)
  listOfReadableParagraphs = createReadableTokenList(listOfParagraphsFromTokens)
  container = DTMCandProbDist_Container()
  dtmcContainer = DTMCTemp_Container()
  for paragraph in listOfReadableParagraphs:
    ParseDTMCandProbdistOnce(paragraph, container, dtmcContainer)   
  return container
