# Run time variables that constantly change
# Stored in a python file as a dictionary
# Author: Howard Webb
# Data: 11/02/2017

import os
import json
from saveGlobals import saveVars

env={}

def buildVars():
    env={'targetTemp': 25, 'priorFanOn': True}
    saveVars(env)

def loadDict(name, value):
    env[name]=value

def test():
    import variable as var
    print('env: ', var.env)
    
if __name__=="__main__":
    buildVars()
    test()
