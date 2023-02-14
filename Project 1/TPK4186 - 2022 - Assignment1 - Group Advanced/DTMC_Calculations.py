# Calculations on DTMC and probability distribturion

from Parser import*

#Task 10  Function that calculates the product of a probability distribution by the sparse matrix. 
# ----------------------------------------------------------------------------

def Calculate_Product(DTMC, statesProbabilities):
  returnStatesProbabilities = dict()
  for stateName in statesProbabilities:
    stateProbability = statesProbabilities[stateName]
    transitions = DTMC_GetTransitions(DTMC)
    transitionOut = 0
    for transitionName in transitions:
      transition = transitions[transitionName]
      if States_GetName(Transition_GetSourceState(transition)) == stateName:
        transitionOut += Transition_GetProbability(transition) 
    stateProbability *= (1-transitionOut)


    for transitionName in transitions:
      transitionIn = 0
      transition = transitions[transitionName]
      if States_GetName(Transition_GetTargetState(transition)) == stateName:
        transitionIn += Transition_GetProbability(transition)
        sourceStateName=States_GetName(Transition_GetSourceState(transition))
        sourceStateProb = statesProbabilities[sourceStateName]
        stateProbability+=sourceStateProb*transitionIn  
      
    returnStatesProbabilities[stateName]=stateProbability
  return returnStatesProbabilities
  
#Task 11
# ----------------------------------------------------------------------------

def Calculate_nSteps(probDist, n):
    if not DTMCandProbDist_FinalCheckBeforeCalculations(probDist):
        return None
    DTMC=ProbDist_GetDTMC(probDist)
    initialProbabilities=ProbDist_GetProbabilityDistribution(probDist)
    returnStatesProbabilities = initialProbabilities
    for i in range(n):
       returnStatesProbabilities = Calculate_Product(DTMC, returnStatesProbabilities)
    return returnStatesProbabilities
    return None

def Calculate_nSteps_Printer(stateProbabilities):
    if stateProbabilities == None:
        return None
    for state in stateProbabilities:
        print("State: %20s \t %s" %(state,stateProbabilities.get(state)))
