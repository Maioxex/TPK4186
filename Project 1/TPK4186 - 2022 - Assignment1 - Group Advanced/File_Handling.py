# Structure for handling reading and writing to file

from Data_Structure import *

#Task 5. Printing DTMC and probability distributions into file 
# ----------------------------------------------------------------------------

def Printer_ToFile_DTMC(DTMC,filename):
  f = open(filename,"a") 
  f.write("MarkovChain " + DTMC_GetName(DTMC)+"\n")
  transitions= DTMC_GetTransitions(DTMC)
  for transitionName in transitions:
      transition = transitions[transitionName]
      f.write("\t"+ States_GetName(Transition_GetSourceState(transition))+" -> "+States_GetName(Transition_GetTargetState(transition))+": "+str(Transition_GetProbability(transition))+";\n")
  f.write("end\n")
  f.write("\n")
  f.close()
  
def Printer_ToFile_ProbDist(probDist,filename):
  f=open(filename,"a")
  f.write("ProbabilityDistribution "+ ProbDist_GetName(probDist)+ " of " + DTMC_GetName(ProbDist_GetDTMC(probDist))+"\n")
  probabilities=ProbDist_GetProbabilityDistribution(probDist)
  for key in probabilities:
    f.write("\t"+key+": "+str(probabilities[key])+";\n")
  f.write("end\n")
  f.write("\n")
  f.close()

def Printer_ToFile_ListOfDTMC(listOfDTMC,filename):
  f=open(filename,"a")
  for DTMC in listOfDTMC:
    Printer_ToFile_DTMC(DTMC,filename)
  f.close()

def Printer_ToFile_ListOfProbDist(listOfProbDist,filename):
  f=open(filename,"a")
  for probDist in listOfProbDist:
    Printer_ToFile_ProbDist(probDist,filename)
  f.close()
  
  
def Printer_ToFile_Container(container, filename):
    if container == None:
        return None
    f=open(filename,"w")
    for key in container:
        listofProbDist = container[key]
        DTMC = DTMCandProbDist_ReturnDTMCFromContainer(container,key)
        Printer_ToFile_DTMC(DTMC, filename)
        Printer_ToFile_ListOfProbDist(listofProbDist,filename)
    f.close()
    
def Printer_ToConsole_Container(container):
  if container == None:
      return None
  for key in container:
    listOfProbDist = container[key]
    DTMC = DTMCandProbDist_ReturnDTMCFromContainer(container,key)
    Printer_PrintMarkovGraph(DTMC)
    print("\n")
    for probDist in listOfProbDist:
        print("ProbabilityDistribution "+ ProbDist_GetName(probDist)+ " of " + DTMC_GetName(ProbDist_GetDTMC(probDist))+"\n")
        probabilities=ProbDist_GetProbabilityDistribution(probDist)
        for key in probabilities:
            print("\t"+key+": "+str(probabilities[key])+";\n")
    print("\n")

