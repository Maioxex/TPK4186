#TPK4186 - 2022 - Assignment 1- Jonas Lund, Markus Vonheim and Simen Møller
# Main document for running and testing functions

from ExperimentalStudy import *

def main():
    # First, we import a benchmark file, and create a container of DTMC's and probability distributions
    print("-----------Reading from a becnhmark file-----------")
    container = Parse_TokensFromFile("Benchmark.txt")
    
    print("------Print the DTMC's from the benchmark file------")
    Printer_ToConsole_Container(container)
    
    # Second, after the benchmark file has been handled, we can write the container to a new file
    Printer_ToFile_Container(container, 'Results.txt')

    # Third, we can do calculations to find the probability distribution for a given DTMC and initial probability distribution
    steps = 1000
    print("\n--Calculating state probabilities after " + str(steps) + " steps--")
    probDist = DTMC_ReturnProbDistFromContainer('TrondheimWindCondition', 'pWINDY', container)
    stateProbabilities = Calculate_nSteps(probDist, steps)
    Calculate_nSteps_Printer(stateProbabilities)
    
    # Fourth, we perform experimental study to find the error-term for different number of elements in a time series
    print('\n-----------------Experimental study-----------------')
    DTMC = ProbDist_GetDTMC(probDist)
    initialState = DTMC_LookForState(DTMC, 'WINDY')
    Compare_Printer(DTMC,initialState)
    print("\n")
    probDist = DTMC_ReturnProbDistFromContainer('SeaCondition', 'p3', container)
    DTMC_2 = ProbDist_GetDTMC(probDist)
    initialState = DTMC_LookForState(DTMC_2, 'CALM')
    Compare_Printer(DTMC_2,initialState)


    
main()
