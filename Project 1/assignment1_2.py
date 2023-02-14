# Markus testing av ListOfTokens

import sys
import re 


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
          elif re.match(r"[0-9][0-9]*\.[0-9][0-9]*", newLine):
              tmpCount = count
              number = re.match(r"[0-9][0-9]*\.[0-9][0-9]*", newLine).group()
              count += len(number)
              newLine = re.sub(r"[0-9][0-9]*\.[0-9][0-9]*", "", newLine)
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



def Token_GetType(ListOfTokens, tokenNb):
  return ListOfTokens[[tokenNb][0]][0]

def Token_GetString(ListOfTokens, tokenNb):
  return ListOfTokens[[tokenNb][0]][1]

def Token_GetPlacement(ListOfTokens, tokenNb):
  return [ListOfTokens[[tokenNb][0]][2],ListOfTokens[[tokenNb][0]][3]]


print(Reader_TextfileToListOfTokens("test4.txt"))


print(Token_GetType(Reader_TextfileToListOfTokens("test4.txt"), 0))
print(Token_GetString(Reader_TextfileToListOfTokens("test4.txt"), 0))
print(Token_GetPlacement(Reader_TextfileToListOfTokens("test4.txt"), 0))



#print(Token_GetType(Reader_TextfileToListOfTokens("test2.txt"), 0))
#print(Token_GetString(Reader_TextfileToListOfTokens("test2.txt"), 0))
#print(Token_GetPlacement(Reader_TextfileToListOfTokens("test2.txt"), 0))

