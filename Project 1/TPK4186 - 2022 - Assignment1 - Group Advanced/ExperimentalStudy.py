# Comparing and checking error of actual DTMC and DTMC created from time series

from MarkovChain_TimeSeries import*

#Task 14
# ----------------------------------------------------------------------------

def Compare_absNumbers(n1,n2):
    return abs(n1-n2)

def Compare_States(DTMC,DTMC_FromTimeSeries):
    states = DTMC_GetStates(DTMC)
    #print(states)
    for stateName in states:
        if DTMC_LookForState(DTMC_FromTimeSeries, stateName) == None:
            return False
    return True
            
def Compare_TransitionsPair(transition_DTMC, transition_DTMC_FromTimeSeries):
    if Transition_GetName(transition_DTMC) == Transition_GetName(transition_DTMC_FromTimeSeries):
        check = Compare_absNumbers(Transition_GetProbability(transition_DTMC) , Transition_GetProbability(transition_DTMC_FromTimeSeries))
        return check
    return None
 
def Compare_nTransitions(transitions_DTMC, transitions_DTMC_FromTimeSeries):
    sumErrors = 0
    numTransitions = 0
    for transition_DTMC in transitions_DTMC:
        numTransitions += 1
        if transitions_DTMC_FromTimeSeries.get(transition_DTMC) == None:
            sumErrors = None
            return None
        sumErrors += Compare_TransitionsPair(transitions_DTMC.get(transition_DTMC), transitions_DTMC_FromTimeSeries.get(transition_DTMC))
    epsilon = sumErrors / numTransitions
    return epsilon
              
def Compare_Actual_and_TimeSeries(DTMC, initialState, n):
    timeSeriesForDTMC = TimeSeries_nSequences(DTMC,initialState,n)
    DTMC_FromTimeSeries = MarkovFromTimeSeries_Generator(timeSeriesForDTMC, "DTMC_FromTimeSeries")
    if Compare_States(DTMC, DTMC_FromTimeSeries):
        transitions_DTMC = DTMC_GetTransitions(DTMC)
        transitions_DTMC_FromTimeSeries = DTMC_GetTransitions(DTMC_FromTimeSeries)
        epsilon = Compare_nTransitions(transitions_DTMC, transitions_DTMC_FromTimeSeries)
        if epsilon != None:
            return epsilon
    return None   

def Compare_Printer(DTMC,initialState):
    n = 10
    print("DTMC: "+DTMC_GetName(DTMC))
    for i in range(1,6):
        epsilon = Compare_Actual_and_TimeSeries(DTMC, initialState , n)
        print("Epsilon: %20s \t %s" %(str(n)+" steps",str(epsilon)))
        #print("Epsilon_" + str(n) + "\t" + str(epsilon))
        n*=10
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    