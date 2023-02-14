# Creating time series and Markov chain from the time series

from DTMC_Calculations import *

#Task 12
# ----------------------------------------------------------------------------

import random

def Bound_New(lowerBound, upperBound):
    return [lowerBound,upperBound]

def Bound_Lower(bound):
    return bound[0]

def Bound_Upper(bound):
    return bound[1]

def Bound_Check(bound, randomValue):
  if randomValue < Bound_Upper(bound) and randomValue >= Bound_Lower(bound):
    return True
  else:
    return False 

def TimeSeries_NextState(DTMC,initialState): #Denne funker nÃ¥
  intervalProbabilities = dict() 
  transitions = DTMC_GetTransitions(DTMC)
  value = 0
  for transitionName in transitions:
    transition = transitions[transitionName]
    if States_GetName(Transition_GetSourceState(transition)) == States_GetName(initialState):
      LB=value
      UB=value + Transition_GetProbability(transition)
      intervalProbabilities[States_GetName(Transition_GetTargetState(transition))] = Bound_New(LB,UB)
      value += Transition_GetProbability(transition)
  intervalProbabilities[States_GetName(initialState)]= Bound_New(value,1)
  randomValue= random.random() 
  for stateName in intervalProbabilities:
    if Bound_Check(intervalProbabilities[stateName],randomValue):
      return DTMC_LookForState(DTMC,stateName)
  return None #no legal interval exists 

def TimeSeries_nSequences(DTMC,initialState,n):
  sequenceOfStates=[initialState]
  nextState=initialState
  for i in range(n):
    nextState=TimeSeries_NextState(DTMC,nextState)
    sequenceOfStates.append(nextState)
  return sequenceOfStates

#Task 13
# ----------------------------------------------------------------------------

def Transition_New_Temp(transitionName, sourceState, targetState, nTraversed):
  return[transitionName, sourceState, targetState, nTraversed]

def Transition_TempStorage():
  tempTransitions = dict()
  return tempTransitions

def MarkovFromTimeSeries_Generator(timeSeries, dtmcName):
  DTMC = DTMC_New(dtmcName)
  temporaryTransitions = Transition_TempStorage()
  initialState = timeSeries[0]
  DTMC_NewState(DTMC,States_GetName(initialState))
  for i in range(1,len(timeSeries)): 
    if DTMC_LookForState(DTMC,States_GetName(timeSeries[i])) == None: #the state does not already exist
      DTMC_NewState(DTMC, States_GetName(timeSeries[i]))
    sourceState = timeSeries[i-1]
    targetState = timeSeries[i]
    transitionName = States_GetName(sourceState) + "_" + States_GetName(targetState)
    transition= Transition_New_Temp(transitionName,sourceState,targetState,1)
    if temporaryTransitions.get(transitionName,None) == None: #the transition does not already exist
      temporaryTransitions[transitionName] = transition #add a new transition with nTraversed = 1 
    else:
      temporaryTransitions[transitionName][3]+=1 # nTraversed is increased with 1
  for transitionName in temporaryTransitions:
    dividend=temporaryTransitions[transitionName][3]
    divisor=0
    for possibleTransition in temporaryTransitions:
      if temporaryTransitions[possibleTransition][1]==temporaryTransitions[transitionName][1]: #i.e. the transitions have the same sourceNode
        divisor+=temporaryTransitions[possibleTransition][3]
    probability = dividend/divisor
    DTMC_NewTransition(DTMC,temporaryTransitions[transitionName][1],temporaryTransitions[transitionName][2],probability)
  return DTMC
