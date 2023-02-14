#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 22 11:39:12 2022

@author: markusvonheim
"""


# pseudo kode 
# {DTMCName:[probDist1,probDist2,...,probDistn]}

# Ikke ferdig. Må også jobbe med arkitekturen 
def ParseDTMCandProbdist(listOfTokens, DTMC_Container): 
  DTMC_name = Token_GetNameDTMCProbdist(listOfTokens)
  if DTMC_name not in DTMC_Container:
    DTMC_Container[DTMC_name]
    DTMC_New(DTMC_name)
    for line in listOfTokens:
        #Storing potential "TestName" of the ProbDist
        TestName = line[1][1]
        if line[0][1] == "MarkovChain":
            continue
        #elif line[0][1] == "end":
            #break
        else:
          # Retrieving the type of the first and third token in line i 
          Type1 = line[0][0]
          Type2 = line[2][0]
          string1 = line[0][1]
          string2 = line[2][1]
          if Type1 == "Identifier" and  Type2 == "Identifier": 
            DTMC_NewState(DTMC_name, string1)
            DTMC_NewState(DTMC_name, string2)
            sourceState = string1
            targetState = string2
            probabilityFrequency = int(line[4][1])
            DTMC_NewTransition(DTMC_name,sourceState,targetState,probabilityFrequencyCandidate)
          elif Type1 == "Identifier" and  Type2 == "Number":
            DTMC_ContainerNewProbDist(DTMC_Container,TestName,DTMC_name)
            #adding probabilities
            probability = int(string2)
            state = string1
            ProbDist_NewProbability(TestName,probability,state)
          else:
              print("An error occured when retrieving the \"Type\" of token(s)")   
  else:
      for line in listOfTokens:
          #Storing potential "TestName" of the ProbDist
          TestName = line[1][1]
          if line[0][1] == "MarkovChain":
              continue
          #elif line[0][1] == "end":
              #break
          else:
            # Retrieving the type of the first and third token in line i 
            Type1 = line[0][0]
            Type2 = line[2][0]
            string1 = line[0][1]
            string2 = line[2][1]
            if Type1 == "Identifier" and  Type2 == "Identifier": 
              DTMC_NewState(DTMC_name, string1)
              DTMC_NewState(DTMC_name, string2)
              sourceState = string1
              targetState = string2
              probabilityFrequency = int(line[4][1])
              DTMC_NewTransition(DTMC_name,sourceState,targetState,probabilityFrequencyCandidate)
            elif Type1 == "Identifier" and  Type2 == "Number":
              DTMC_ContainerNewProbDist(DTMC_Container,TestName,DTMC_name)
              #adding probabilities
              probability = int(string2)
              state = string1
              ProbDist_NewProbability(TestName,probability,state)
            else:
                print("An error occured when retrieving the \"Type\" of token(s)")
  return DTMC_Container              

      
            
        

# list of tokens. –> used for testing
testList1 = [['Reserved', 'MarkovChain', 1, 0], ['Identifier', 'DouglasSeaScale', 1, 12], ['Identifier', 'CALM', 2, 1], ['Arrow', '->', 2, 6], ['Identifier', 'MODERATE', 2, 9], ['Character', ':', 2, 17], ['Number', '0.4', 2, 19], ['Character', ';', 2, 22], ['Identifier', 'MODERATE', 3, 1], ['Arrow', '->', 3, 10], ['Identifier', 'CALM', 3, 13], ['Character', ':', 3, 17], ['Number', '0.6', 3, 19], ['Character', ';', 3, 22], ['Identifier', 'MODERATE', 4, 1], ['Arrow', '->', 4, 10], ['Identifier', 'ROUGH', 4, 13], ['Character', ':', 4, 18], ['Number', '0.1', 4, 20], ['Character', ';', 4, 23], ['Identifier', 'ROUGH', 5, 1], ['Arrow', '->', 5, 7], ['Identifier', 'MODERATE', 5, 10], ['Character', ':', 5, 18], ['Number', '0.9', 5, 20], ['Character', ';', 5, 23], ['Reserved', 'end', 6, 0], ['Reserved', 'MarkovChain', 8, 0], ['Identifier', 'DouglasSeaScale', 8, 12], ['Identifier', 'CALM', 9, 1], ['Arrow', '->', 9, 6], ['Identifier', 'MODERATE', 9, 9], ['Character', ':', 9, 17], ['Number', '0.4', 9, 19], ['Character', ';', 9, 22], ['Identifier', 'MODERATE', 10, 1], ['Arrow', '->', 10, 10], ['Identifier', 'CALM', 10, 13], ['Character', ':', 10, 17], ['Number', '0.6', 10, 19], ['Character', ';', 10, 22], ['Identifier', 'MODERATE', 11, 1], ['Arrow', '->', 11, 10], ['Identifier', 'ROUGH', 11, 13], ['Character', ':', 11, 18], ['Number', '0.1', 11, 20], ['Character', ';', 11, 23], ['Identifier', 'ROUGH', 12, 1], ['Arrow', '->', 12, 7], ['Identifier', 'MODERATE', 12, 10], ['Character', ':', 12, 18], ['Number', '0.9', 12, 20], ['Character', ';', 12, 23], ['Reserved', 'end', 13, 0]]  
testList2 = [['Reserved', 'ProbabilityDistribution', 1, 0], ['Identifier', 'TestName', 1, 24], ['Reserved', 'of', 1, 33], ['Identifier', 'DouglasSeaScale', 1, 36], ['Identifier', 'CALM', 2, 1], ['Character', ':', 2, 5], ['Number', '1.0', 2, 7], ['Character', ';', 2, 10], ['Identifier', 'MODERATE', 3, 1], ['Character', ':', 3, 9], ['Number', '0.0', 3, 11], ['Character', ';', 3, 14], ['Identifier', 'ROUGH', 4, 1], ['Character', ':', 4, 6], ['Number', '0.0', 4, 8], ['Character', ';', 4, 11], ['Reserved', 'end', 5, 0], ['Reserved', 'ProbabilityDistribution', 7, 0], ['Identifier', 'TestName', 7, 24], ['Reserved', 'of', 7, 33], ['Identifier', 'DouglasSeaScale', 7, 36], ['Identifier', 'CALM', 8, 1], ['Character', ':', 8, 5], ['Number', '1.0', 8, 7], ['Character', ';', 8, 10], ['Identifier', 'MODERATE', 9, 1], ['Character', ':', 9, 9], ['Number', '0.0', 9, 11], ['Character', ';', 9, 14], ['Identifier', 'ROUGH', 10, 1], ['Character', ':', 10, 6], ['Number', '0.0', 10, 8], ['Character', ';', 10, 11], ['Reserved', 'end', 11, 0], ['Reserved', 'ProbabilityDistribution', 13, 0], ['Identifier', 'TestName', 13, 24], ['Reserved', 'of', 13, 33], ['Identifier', 'DouglasSeaScale', 13, 36], ['Identifier', 'CALM', 14, 1], ['Character', ':', 14, 5], ['Number', '1.0', 14, 7], ['Character', ';', 14, 10], ['Identifier', 'MODERATE', 15, 1], ['Character', ':', 15, 9], ['Number', '0.0', 15, 11], ['Character', ';', 15, 14], ['Identifier', 'ROUGH', 16, 1], ['Character', ':', 16, 6], ['Number', '0.0', 16, 8], ['Character', ';', 16, 11], ['Reserved', 'end', 17, 0], ['Reserved', 'ProbabilityDistribution', 19, 0], ['Identifier', 'TestName', 19, 24], ['Reserved', 'of', 19, 33], ['Identifier', 'DouglasSeaScale', 19, 36], ['Identifier', 'CALM', 20, 1], ['Character', ':', 20, 5], ['Number', '1.0', 20, 7], ['Character', ';', 20, 10], ['Identifier', 'MODERATE', 21, 1], ['Character', ':', 21, 9], ['Number', '0.0', 21, 11], ['Character', ';', 21, 14], ['Identifier', 'ROUGH', 22, 1], ['Character', ':', 22, 6], ['Number', '0.0', 22, 8], ['Character', ';', 22, 11], ['Reserved', 'end', 23, 0]]
templateList = [['Reserved', 'MarkovChain', 1, 0, 0], ['Identifier', 'DouglasSeaScale', 1, 12, 1], ['Identifier', 'CALM', 2, 1, 0], ['Arrow', '->', 2, 6, 1], ['Identifier', 'MODERATE', 2, 9, 2], ['Character', ':', 2, 17, 3], ['Number', '0.4', 2, 19, 4], ['Character', ';', 2, 22, 5], ['Identifier', 'MODERATE', 3, 1, 0], ['Arrow', '->', 3, 10, 1], ['Identifier', 'CALM', 3, 13, 2], ['Character', ':', 3, 17, 3], ['Number', '0.6', 3, 19, 4], ['Character', ';', 3, 22, 5], ['Identifier', 'MODERATE', 4, 1, 0], ['Arrow', '->', 4, 10, 1], ['Identifier', 'ROUGH', 4, 13, 2], ['Character', ':', 4, 18, 3], ['Number', '0.1', 4, 20, 4], ['Character', ';', 4, 23, 5], ['Identifier', 'ROUGH', 5, 1, 0], ['Arrow', '->', 5, 7, 1], ['Identifier', 'MODERATE', 5, 10, 2], ['Character', ':', 5, 18, 3], ['Number', '0.9', 5, 20, 4], ['Character', ';', 5, 23, 5], ['Reserved', 'end', 6, 0, 0], ['Reserved', 'MarkovChain', 8, 0, 0], ['Identifier', 'DouglasSeaScale', 8, 12, 1], ['Identifier', 'CALM', 9, 1, 0], ['Arrow', '->', 9, 6, 1], ['Identifier', 'MODERATE', 9, 9, 2], ['Character', ':', 9, 17, 3], ['Number', '0.4', 9, 19, 4], ['Character', ';', 9, 22, 5], ['Identifier', 'MODERATE', 10, 1, 0], ['Arrow', '->', 10, 10, 1], ['Identifier', 'CALM', 10, 13, 2], ['Character', ':', 10, 17, 3], ['Number', '0.6', 10, 19, 4], ['Character', ';', 10, 22, 5], ['Identifier', 'MODERATE', 11, 1, 0], ['Arrow', '->', 11, 10, 1], ['Identifier', 'ROUGH', 11, 13, 2], ['Character', ':', 11, 18, 3], ['Number', '0.1', 11, 20, 4], ['Character', ';', 11, 23, 5], ['Identifier', 'ROUGH', 12, 1, 0], ['Arrow', '->', 12, 7, 1], ['Identifier', 'MODERATE', 12, 10, 2], ['Character', ':', 12, 18, 3], ['Number', '0.9', 12, 20, 4], ['Character', ';', 12, 23, 5], ['Reserved', 'end', 13, 0, 0], ['Reserved', 'MarkovChain', 15, 0, 0], ['Identifier', 'DouglasSeaScale', 15, 12, 1], ['Identifier', 'CALM', 16, 1, 0], ['Arrow', '->', 16, 6, 1], ['Identifier', 'MODERATE', 16, 9, 2], ['Character', ':', 16, 17, 3], ['Number', '0.4', 16, 19, 4], ['Character', ';', 16, 22, 5], ['Identifier', 'MODERATE', 17, 1, 0], ['Arrow', '->', 17, 10, 1], ['Identifier', 'CALM', 17, 13, 2], ['Character', ':', 17, 17, 3], ['Number', '0.6', 17, 19, 4], ['Character', ';', 17, 22, 5], ['Identifier', 'MODERATE', 18, 1, 0], ['Arrow', '->', 18, 10, 1], ['Identifier', 'ROUGH', 18, 13, 2], ['Character', ':', 18, 18, 3], ['Number', '0.1', 18, 20, 4], ['Character', ';', 18, 23, 5], ['Identifier', 'ROUGH', 19, 1, 0], ['Arrow', '->', 19, 7, 1], ['Identifier', 'MODERATE', 19, 10, 2], ['Character', ':', 19, 18, 3], ['Number', '0.9', 19, 20, 4], ['Character', ';', 19, 23, 5], ['Reserved', 'end', 20, 0, 0], ['Reserved', 'MarkovChain', 22, 0, 0], ['Identifier', 'DouglasSeaScale', 22, 12, 1], ['Identifier', 'CALM', 23, 1, 0], ['Arrow', '->', 23, 6, 1], ['Identifier', 'MODERATE', 23, 9, 2], ['Character', ':', 23, 17, 3], ['Number', '0.4', 23, 19, 4], ['Character', ';', 23, 22, 5], ['Identifier', 'MODERATE', 24, 1, 0], ['Arrow', '->', 24, 10, 1], ['Identifier', 'CALM', 24, 13, 2], ['Character', ':', 24, 17, 3], ['Number', '0.6', 24, 19, 4], ['Character', ';', 24, 22, 5], ['Identifier', 'MODERATE', 25, 1, 0], ['Arrow', '->', 25, 10, 1], ['Identifier', 'ROUGH', 25, 13, 2], ['Character', ':', 25, 18, 3], ['Number', '0.1', 25, 20, 4], ['Character', ';', 25, 23, 5], ['Identifier', 'ROUGH', 26, 1, 0], ['Arrow', '->', 26, 7, 1], ['Identifier', 'MODERATE', 26, 10, 2], ['Character', ':', 26, 18, 3], ['Number', '0.9', 26, 20, 4], ['Character', ';', 26, 23, 5], ['Reserved', 'end', 27, 0, 0], ['Reserved', 'MarkovChain', 29, 0, 0], ['Identifier', 'DouglasSeaScale', 29, 12, 1], ['Identifier', 'CALM', 30, 1, 0], ['Arrow', '->', 30, 6, 1], ['Identifier', 'MODERATE', 30, 9, 2], ['Character', ':', 30, 17, 3], ['Number', '0.4', 30, 19, 4], ['Character', ';', 30, 22, 5], ['Identifier', 'MODERATE', 31, 1, 0], ['Arrow', '->', 31, 10, 1], ['Identifier', 'CALM', 31, 13, 2], ['Character', ':', 31, 17, 3], ['Number', '0.6', 31, 19, 4], ['Character', ';', 31, 22, 5], ['Identifier', 'MODERATE', 32, 1, 0], ['Arrow', '->', 32, 10, 1], ['Identifier', 'ROUGH', 32, 13, 2], ['Character', ':', 32, 18, 3], ['Number', '0.1', 32, 20, 4], ['Character', ';', 32, 23, 5], ['Identifier', 'ROUGH', 33, 1, 0], ['Arrow', '->', 33, 7, 1], ['Identifier', 'MODERATE', 33, 10, 2], ['Character', ':', 33, 18, 3], ['Number', '0.9', 33, 20, 4], ['Character', ';', 33, 23, 5], ['Reserved', 'end', 34, 0, 0], ['Reserved', 'MarkovChain', 36, 0, 0], ['Identifier', 'DouglasSeaScale', 36, 12, 1], ['Identifier', 'CALM', 37, 1, 0], ['Arrow', '->', 37, 6, 1], ['Identifier', 'MODERATE', 37, 9, 2], ['Character', ':', 37, 17, 3], ['Number', '0.4', 37, 19, 4], ['Character', ';', 37, 22, 5], ['Identifier', 'MODERATE', 38, 1, 0], ['Arrow', '->', 38, 10, 1], ['Identifier', 'CALM', 38, 13, 2], ['Character', ':', 38, 17, 3], ['Number', '0.6', 38, 19, 4], ['Character', ';', 38, 22, 5], ['Identifier', 'MODERATE', 39, 1, 0], ['Arrow', '->', 39, 10, 1], ['Identifier', 'ROUGH', 39, 13, 2], ['Character', ':', 39, 18, 3], ['Number', '0.1', 39, 20, 4], ['Character', ';', 39, 23, 5], ['Identifier', 'ROUGH', 40, 1, 0], ['Arrow', '->', 40, 7, 1], ['Identifier', 'MODERATE', 40, 10, 2], ['Character', ':', 40, 18, 3], ['Number', '0.9', 40, 20, 4], ['Character', ';', 40, 23, 5], ['Reserved', 'end', 41, 0, 0]]
ListSeparated = [[['Reserved', 'MarkovChain', 1, 0, 0], ['Identifier', 'DouglasSeaScale', 1, 12, 1], ['Identifier', 'CALM', 2, 1, 0], ['Arrow', '->', 2, 6, 1], ['Identifier', 'MODERATE', 2, 9, 2], ['Character', ':', 2, 17, 3], ['Number', '0.4', 2, 19, 4], ['Character', ';', 2, 22, 5], ['Identifier', 'MODERATE', 3, 1, 0], ['Arrow', '->', 3, 10, 1], ['Identifier', 'CALM', 3, 13, 2], ['Character', ':', 3, 17, 3], ['Number', '0.6', 3, 19, 4], ['Character', ';', 3, 22, 5], ['Identifier', 'MODERATE', 4, 1, 0], ['Arrow', '->', 4, 10, 1], ['Identifier', 'ROUGH', 4, 13, 2], ['Character', ':', 4, 18, 3], ['Number', '0.1', 4, 20, 4], ['Character', ';', 4, 23, 5], ['Identifier', 'ROUGH', 5, 1, 0], ['Arrow', '->', 5, 7, 1], ['Identifier', 'MODERATE', 5, 10, 2], ['Character', ':', 5, 18, 3], ['Number', '0.9', 5, 20, 4], ['Character', ';', 5, 23, 5], ['Reserved', 'end', 6, 0, 0]], [['Reserved', 'MarkovChain', 8, 0, 0], ['Identifier', 'DouglasSeaScale', 8, 12, 1], ['Identifier', 'CALM', 9, 1, 0], ['Arrow', '->', 9, 6, 1], ['Identifier', 'MODERATE', 9, 9, 2], ['Character', ':', 9, 17, 3], ['Number', '0.4', 9, 19, 4], ['Character', ';', 9, 22, 5], ['Identifier', 'MODERATE', 10, 1, 0], ['Arrow', '->', 10, 10, 1], ['Identifier', 'CALM', 10, 13, 2], ['Character', ':', 10, 17, 3], ['Number', '0.6', 10, 19, 4], ['Character', ';', 10, 22, 5], ['Identifier', 'MODERATE', 11, 1, 0], ['Arrow', '->', 11, 10, 1], ['Identifier', 'ROUGH', 11, 13, 2], ['Character', ':', 11, 18, 3], ['Number', '0.1', 11, 20, 4], ['Character', ';', 11, 23, 5], ['Identifier', 'ROUGH', 12, 1, 0], ['Arrow', '->', 12, 7, 1], ['Identifier', 'MODERATE', 12, 10, 2], ['Character', ':', 12, 18, 3], ['Number', '0.9', 12, 20, 4], ['Character', ';', 12, 23, 5], ['Reserved', 'end', 13, 0, 0]], [['Reserved', 'MarkovChain', 15, 0, 0], ['Identifier', 'DouglasSeaScale', 15, 12, 1], ['Identifier', 'CALM', 16, 1, 0], ['Arrow', '->', 16, 6, 1], ['Identifier', 'MODERATE', 16, 9, 2], ['Character', ':', 16, 17, 3], ['Number', '0.4', 16, 19, 4], ['Character', ';', 16, 22, 5], ['Identifier', 'MODERATE', 17, 1, 0], ['Arrow', '->', 17, 10, 1], ['Identifier', 'CALM', 17, 13, 2], ['Character', ':', 17, 17, 3], ['Number', '0.6', 17, 19, 4], ['Character', ';', 17, 22, 5], ['Identifier', 'MODERATE', 18, 1, 0], ['Arrow', '->', 18, 10, 1], ['Identifier', 'ROUGH', 18, 13, 2], ['Character', ':', 18, 18, 3], ['Number', '0.1', 18, 20, 4], ['Character', ';', 18, 23, 5], ['Identifier', 'ROUGH', 19, 1, 0], ['Arrow', '->', 19, 7, 1], ['Identifier', 'MODERATE', 19, 10, 2], ['Character', ':', 19, 18, 3], ['Number', '0.9', 19, 20, 4], ['Character', ';', 19, 23, 5], ['Reserved', 'end', 20, 0, 0]], [['Reserved', 'MarkovChain', 22, 0, 0], ['Identifier', 'DouglasSeaScale', 22, 12, 1], ['Identifier', 'CALM', 23, 1, 0], ['Arrow', '->', 23, 6, 1], ['Identifier', 'MODERATE', 23, 9, 2], ['Character', ':', 23, 17, 3], ['Number', '0.4', 23, 19, 4], ['Character', ';', 23, 22, 5], ['Identifier', 'MODERATE', 24, 1, 0], ['Arrow', '->', 24, 10, 1], ['Identifier', 'CALM', 24, 13, 2], ['Character', ':', 24, 17, 3], ['Number', '0.6', 24, 19, 4], ['Character', ';', 24, 22, 5], ['Identifier', 'MODERATE', 25, 1, 0], ['Arrow', '->', 25, 10, 1], ['Identifier', 'ROUGH', 25, 13, 2], ['Character', ':', 25, 18, 3], ['Number', '0.1', 25, 20, 4], ['Character', ';', 25, 23, 5], ['Identifier', 'ROUGH', 26, 1, 0], ['Arrow', '->', 26, 7, 1], ['Identifier', 'MODERATE', 26, 10, 2], ['Character', ':', 26, 18, 3], ['Number', '0.9', 26, 20, 4], ['Character', ';', 26, 23, 5], ['Reserved', 'end', 27, 0, 0]], [['Reserved', 'MarkovChain', 29, 0, 0], ['Identifier', 'DouglasSeaScale', 29, 12, 1], ['Identifier', 'CALM', 30, 1, 0], ['Arrow', '->', 30, 6, 1], ['Identifier', 'MODERATE', 30, 9, 2], ['Character', ':', 30, 17, 3], ['Number', '0.4', 30, 19, 4], ['Character', ';', 30, 22, 5], ['Identifier', 'MODERATE', 31, 1, 0], ['Arrow', '->', 31, 10, 1], ['Identifier', 'CALM', 31, 13, 2], ['Character', ':', 31, 17, 3], ['Number', '0.6', 31, 19, 4], ['Character', ';', 31, 22, 5], ['Identifier', 'MODERATE', 32, 1, 0], ['Arrow', '->', 32, 10, 1], ['Identifier', 'ROUGH', 32, 13, 2], ['Character', ':', 32, 18, 3], ['Number', '0.1', 32, 20, 4], ['Character', ';', 32, 23, 5], ['Identifier', 'ROUGH', 33, 1, 0], ['Arrow', '->', 33, 7, 1], ['Identifier', 'MODERATE', 33, 10, 2], ['Character', ':', 33, 18, 3], ['Number', '0.9', 33, 20, 4], ['Character', ';', 33, 23, 5], ['Reserved', 'end', 34, 0, 0]], [['Reserved', 'MarkovChain', 36, 0, 0], ['Identifier', 'DouglasSeaScale', 36, 12, 1], ['Identifier', 'CALM', 37, 1, 0], ['Arrow', '->', 37, 6, 1], ['Identifier', 'MODERATE', 37, 9, 2], ['Character', ':', 37, 17, 3], ['Number', '0.4', 37, 19, 4], ['Character', ';', 37, 22, 5], ['Identifier', 'MODERATE', 38, 1, 0], ['Arrow', '->', 38, 10, 1], ['Identifier', 'CALM', 38, 13, 2], ['Character', ':', 38, 17, 3], ['Number', '0.6', 38, 19, 4], ['Character', ';', 38, 22, 5], ['Identifier', 'MODERATE', 39, 1, 0], ['Arrow', '->', 39, 10, 1], ['Identifier', 'ROUGH', 39, 13, 2], ['Character', ':', 39, 18, 3], ['Number', '0.1', 39, 20, 4], ['Character', ';', 39, 23, 5], ['Identifier', 'ROUGH', 40, 1, 0], ['Arrow', '->', 40, 7, 1], ['Identifier', 'MODERATE', 40, 10, 2], ['Character', ':', 40, 18, 3], ['Number', '0.9', 40, 20, 4], ['Character', ';', 40, 23, 5], ['Reserved', 'end', 41, 0, 0]]]

print(ParseDTMCandProbdist(testList2))

  #Get name of DTMC
  # If "DTMC-name" not in container: 
    # Append DTMC to container (with probability distribution)
    # Probability distribution[name, DTMC : {}, probability for each inital state ]
    # –> DTMC_NEW() 
    # –> for each state: DTMC_NewState(DTMC, "Name")
    # –> DTMC_NewTransition(DTMC,Sourcestate,Targetstate, frequenzy of change) 
    # 
    # Next step is to create probability distribution 
    # –> DTMC_ContainerNewProbDist(testcontainer, "Name prob dist", DTMC)
    # Add probabilities of states
    # ProbDist_NewProbability(ProbDist, probability, state)
    # 


#1. Create DTMC
#2. Probdist. 
#3. Combine ––> {"DTMC": Probdist}

    # else if DTMC name in container : 
    # –> DTMC_ContainerNewProbDist(testcontainer, "Name prob dist", DTMC)
    # Add probabilities of states
    # ProbDist_NewProbability(ProbDist, probability, state)


#def ParseListOfDTMC(listOfDTMC):
  # listOfDTMC architecture :  [[type, "string", linenumber, placement][][][], [][][][], [][][][],]
  # DTMC container = DTMC_Container()
  # for i in range len(listOfDTMC):
  #   ParseDTMC(listofDTMC[i], DTMC_Container)  
  #return DTMC container
  
  
  
  
  
  
  