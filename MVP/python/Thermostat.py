# Author: Howard Webb
# Data: 7/25/2017
# Thermostat controller that reads the temperature sensor and adjusts the exhaust fan

from Fan import Fan
from si7021 import *



def adjustThermostat(temp=None, test=False):
    if temp==None:
        si=si7021()
        temp = si.getTempC()
    fan=Fan()
    fan.adjust(temp, test)        
        

def test():
    print "Test"
    adjustThermostat(40, True)
    print "Adjust Thermostat 40"
    adjustThermostat(20, True)
    print "Adjust Thermostat 20"
    adjustThermostat(None, True)
    print "Adjust Thermostat None"

if __name__=="__main__":
    adjustThermostat()

  
    
