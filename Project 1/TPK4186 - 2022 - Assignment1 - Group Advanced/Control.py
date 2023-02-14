# Control probability distributions and DTMC before calculations

from File_Handling import *

# Task 9
# ----------------------------------------------------------------------------

def DTMCandProbDistCheck_sourceState(DTMC, sourceState):
    transitions = DTMC_GetTransitions(DTMC)
    for transitionName in transitions:
      transition = transitions[transitionName]
      if States_GetName(Transition_GetSourceState(transition))==States_GetName(sourceState):
        return True
    print("ERROR")
    print("DTMC: " + DTMC_GetName(DTMC))
    print("State: " + States_GetName(sourceState))
    print("The state is not the source state in any transition.\n")
    return False

def DTMCandProbDistCheck_targetState(DTMC, targetState):
    transitions = DTMC_GetTransitions(DTMC)
    for transitionName in transitions:
      transition = transitions[transitionName]
      if States_GetName(Transition_GetTargetState(transition))==States_GetName(targetState):
        return True
    print("ERROR")
    print("DTMC: " + DTMC_GetName(DTMC))
    print("State: " + States_GetName(targetState))
    print("The state is not the target state in any transition.\n")
    return False 

def DTMCandProbDistCheck_StateProbabilities(probDist, state):
    if ProbDist_GetStateProbability(probDist, state) == None:
        print("ERROR")
        print("DTMC: " + ProbDist_GetDTMC(DTMC_GetName(probDist)))
        print("Probability distribution: " +ProbDist_GetName(probDist))
        print("State: " + States_GetName(state))
        print("The state has no probability\n")
        return False
    return True

def DTMCandProbDistCheck_TransitionProbabilities(ProbDist):
    if ProbDist == None:
        print("ERROR")
        print("The probability distribution is a None-type object.")
        return False
    DTMCfromProbDist = ProbDist_GetDTMC(ProbDist)
    transitions = DTMC_GetTransitions(DTMCfromProbDist)
    for transitionName in transitions:
        transition = transitions[transitionName]
        if not Transition_CheckProbabilityValue(Transition_GetProbability(transition)):
            return False
        elif Transition_GetProbability(transition) == None:
            return False
    return True

def DTMCandProbDist_FinalCheckBeforeCalculations(probDist):
    if not DTMCandProbDistCheck_TransitionProbabilities(probDist):
        print("The DTMC is not ready for calculations. See Error-message.")
        return False
    elif probDist == None:
        print("ERROR: The probability distribution is a None-type object. ")
        return False
    DTMCfromProbDist = ProbDist_GetDTMC(probDist)
    states = DTMC_GetStates(DTMCfromProbDist)
    for stateName in states:
        state = states[stateName]
        if not DTMCandProbDistCheck_sourceState(DTMCfromProbDist, state):
           return False
        elif not DTMCandProbDistCheck_targetState(DTMCfromProbDist, state):
           return False
        elif not DTMCandProbDistCheck_StateProbabilities(probDist, state):
           return False
    return True
