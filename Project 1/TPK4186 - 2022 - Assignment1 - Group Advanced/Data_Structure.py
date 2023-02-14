# Task 1 to 3: Data structure to encode data types

# 1.1 States
# ----------------------------------------------------------------------------

def States_New(name):
  return [name]

def States_GetName(state):
  return state[0]

# 1.2 Transitions
# ----------------------------------------------------------------------------

def Transition_New(name,sourceState, targetState, transitionProbability):
  return [name, sourceState, targetState, transitionProbability]

def Transition_GetName(transition):
  return transition[0]

def Transition_GetSourceState(transition):
  return transition[1]

def Transition_GetTargetState(transition):
  return transition[2]

def Transition_GetProbability(transition):
  return transition[3]

def Transition_CheckProbabilityValue(transitionProbability):
  value = True
  if transitionProbability<0 or transitionProbability >1:
    value =False
  return value 
  

# 1.3 Discrete time Markov chain (DTMC)
# ----------------------------------------------------------------------------

def DTMC_New(name):
  states = dict()
  transitions = dict()
  return [name, states, transitions]

def DTMC_GetName(graph):
  return graph[0]

def DTMC_GetStates(graph):
  return graph[1]

def DTMC_LookForState(graph, name):
  states = DTMC_GetStates(graph)
  return states.get(name, None)

def DTMC_NewState(graph, stateName):
  state = DTMC_LookForState(graph, stateName)
  if state!=None:
    return None
  state = States_New(stateName)
  states = DTMC_GetStates(graph)
  states[stateName] = state
  return state

def DTMC_GetTransitions(graph):
  return graph[2]

def DTMC_LookForTransition(graph, name):
  transitions = DTMC_GetTransitions(graph)
  return transitions.get(name, None)

def DTMC_CheckExistingTransition(graph, sourceState, targetState):
    transitions = DTMC_GetTransitions(graph)
    for transitionName in transitions:
        transition = transitions[transitionName]
        if Transition_GetSourceState(transition) == sourceState and Transition_GetTargetState(transition) == targetState:
            return True
    else:
        return False

def DTMC_NewTransition(graph, sourceState, targetState, transitionProbability):
  transitionName = States_GetName(sourceState) + "_" + States_GetName(targetState)
  transition = DTMC_LookForTransition(graph, transitionName)
  if transition!=None:
    return None
  elif sourceState == targetState:
      return None
  elif DTMC_CheckExistingTransition(graph, sourceState, targetState):
      return None
  transition = Transition_New(transitionName, sourceState, targetState, transitionProbability)
  transitions = DTMC_GetTransitions(graph)
  transitions[transitionName] = transition
  return transition

# 1.4. Printer functions for DTMC
# ----------------------------------------------------------------------------

def Printer_PrintMarkovGraph(graph):
  name = DTMC_GetName(graph)
  print("Graph: " + name)
  for stateNames in DTMC_GetStates(graph):
    print("  State: " + stateNames)
  transitions = DTMC_GetTransitions(graph)
  for transitionName in transitions:
    transition = transitions[transitionName]
    Printer_PrintTransition(transition)

def Printer_PrintTransition(transition):
  name = Transition_GetName(transition)
  sourceState = Transition_GetSourceState(transition)
  sourceStateName = States_GetName(sourceState)
  targetState = Transition_GetTargetState(transition)
  targetStateName = States_GetName(targetState)
  transitionProbability=Transition_GetProbability(transition)
  print("  Transition: %s %-10s -> \t %s %s" %(name,sourceStateName,targetStateName + ":",transitionProbability))

# Task 2. Probability distribution
# ----------------------------------------------------------------------------

def ProbDist_New(name, DTMC):
    probabilities = dict()
    return [name, DTMC, probabilities]

def ProbDist_GetName(probDist):
    return probDist[0]

def ProbDist_GetDTMC(probDist):
    return probDist[1]

def ProbDist_GetProbabilityDistribution(probDist):
    return probDist[2]

def ProbDist_CheckStateProbability(stateProbability): #Task 9
    if stateProbability < 0 or stateProbability > 1:
        return False
    return True

def ProbDist_GetStateProbability(probDist, state):
    probabilities = ProbDist_GetProbabilityDistribution(probDist)
    stateName = States_GetName(state)
    if probabilities.get(stateName,None) == None:
        return None
    return probabilities[stateName]

def ProbDist_NewProbability(probDist, probability, state):
    #prob = probability_New(probability)
    if not ProbDist_CheckStateProbability(probability):
        print("ERROR")
        print("DTMC: " + DTMC_GetName(ProbDist_GetDTMC(probDist)))
        print("Probability distribution: " + ProbDist_GetName(probDist))
        print("State: " + States_GetName(state))
        print("State probability is not between 0 and 1.\n")
        return None
    probabilities = ProbDist_GetProbabilityDistribution(probDist)
    probabilities[state[0]] = probability
    return probabilities[state[0]]

# Task 3. Dictionary for DTMC and probability distributions
# ----------------------------------------------------------------------------

def DTMCandProbDist_Container():
    DTMCandProbDist = dict()
    return DTMCandProbDist

def DTMCTemp_Container():
    DTMC_Container = dict()
    return DTMC_Container

def DTMCTemp_Container_NewDTMC(dtmcTemp_container,DTMCName):
    dtmcNew = DTMC_New(DTMCName)
    if dtmcTemp_container.get(DTMCName) == None:
       dtmcTemp_container[DTMCName] = dtmcNew
    return dtmcTemp_container[DTMCName]


def DTMC_Container_NewProdDist(dtmc_container,probDistName, DTMC):
    dtmcName = DTMC_GetName(DTMC)
    probDist_New = ProbDist_New(probDistName,DTMC)
    if dtmc_container.get(dtmcName) == None:
       dtmc_container[dtmcName] = [probDist_New]
    else:
       dtmc_container[dtmcName].append(probDist_New)
    return probDist_New

def DTMCTemp_GetDTMC(DTMCTemp_container,DTMCName):
    return DTMCTemp_container(DTMCName,None)

def DTMC_ReturnProbDistFromContainer(dtmcName, probDistName, DTMCContainer):
    if DTMCContainer == None:
        return None
    probDistforDTMC_list = DTMCContainer.get(dtmcName,None)
    if probDistforDTMC_list == None:
        return None
    for distribution in probDistforDTMC_list:
        if ProbDist_GetName(distribution) == probDistName:
            return distribution
    return None

def DTMCandProbDist_ReturnDTMCFromContainer(DTMCContainer,key):
    return ProbDist_GetDTMC(DTMCContainer[key][0])

