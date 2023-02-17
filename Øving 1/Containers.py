
import random as rnd
import numpy as np
#Task 1:

class container:
    def __init__(self, length, serialnumber, load =0):
        self.length = length
        self.serialnumber = serialnumber
        self.load =0
        self.selvvekt = 2
        self.loadlimit = 0
        if length == 20:
            self.selvvekt = 2
            self.loadlimit = 20
        else:
            self.selvvekt = 4
            self.loadlimit = 22
            
        if load>self.loadlimit:
            print(f"Error: load can't be more than {self.loadlimit}")
        elif load<0:
            print("Error: load can't be negative")
        else: self.load = load
    #make the getter and setter functions for container
    def getLength(self):
        return self.length
    
    def setLength(self, length):
        self.length = length
    
    def getId(self):
        return self.serialnumber
    
    def setId(self, serialnumber):
        self.serialnumber = serialnumber
    
    def getLoad(self):
        return self.load
    
    def setLoad(self, load):
        if load>self.load:
            print(f"Error: load can't be more than {self.loadlimit}")
        elif load<0:
            print("Error: load can't be negative")
        else: self.load = load
        
    def getselfvekt(self):
        return self.selvvekt
        
    def getTotalWeight(self):
        return self.load + self.selvvekt
    
    def addLoad(self, load):
        if self.load + load > self.loadlimit:
            print(f"Error: load can't be more than {self.loadlimit}")
        elif load+self.load<0:
            print("Error: load can't be less than 0")
        else: self.load += load
      


