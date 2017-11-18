# Create global variables as a dictionary, used when logging sensors that give the unique id of the system (MAC address) and the experiment started.
# A python file is generated that is 'read' by the logging program.
# Author: Howard Webb
# Data: 11/02/2017

import os
import json
from getMAC import getMAC
from geoLocate import getLocation
from saveGlobals import saveEnv

env={}

def buildEnv():
    buildMac()
    buildLocation()
    # Add experiment
    loadDict('exp', 'experiment_1')    
    buildReservoir()
    saveEnv(env)

def buildMac():    

    mac=getMAC()
    loadDict('mac', mac)


def buildLocation():
    jloc=getLocation()
    loadDict('location', jloc)
    
def buildReservoir():
# Note: water levels may need to be adjusted for seedlings (without roots) and plants (with roots)
# This is a starting point, and can be adjusted through recipes
    reservoir_full=175  # Highest desired water level
    reservoir_empty=220 # Lowest level water is allowed to drop
    reservoir_timeout=1200 # Max time to wait for filling
    reservoir_change=3  # Number of mm needed to indicate water level change
    # Build reservoir levels
    reservoir={'full':reservoir_full, 'empty':reservoir_empty, 'timeout': reservoir_timeout, 'change': reservoir_change}
    loadDict('reservoir', reservoir)

def loadDict(name, value):
    env[name]=value

def test():
    import env
    print('env: ', env.env)
    print('location: ', env.env['location'])
    print("city: ", env.env['location']['city'])
    print("lattitude: ", env.env['location']['latitude'])
    print("longitude: ", env.env['location']['longitude'])
    print("mac: ", env.env['mac'])    
    print("exp: ", env.env['exp'])
    print("reservoir: ", env.env['reservoir'])
    
    
if __name__=="__main__":
    buildEnv()
    test()
