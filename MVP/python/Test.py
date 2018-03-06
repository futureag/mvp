# Author: Howard Webb
# Data: 7/25/2017
# Thermostat controller that reads the temperature sensor and adjusts the exhaust fan

from si7021 import si7021
from DewPoint import getDewPoint
from Relay import Relay
from Environment import test as eTest
from Fan import Fan
from Thermostat import test as tTest
from EnvObsv import test as enTest




def test():
    print "System Test"
    print('\n*** Test Sensors ***\n')
    si=si7021()
    si.test()
    print('\n*** Test Dewpoint ***\n')
    t=si.getTempC()
    h=si.getHumidity()
    dp=getDewPoint(t, h)
    print "Dewpoint: ", dp
    print('\n*** Test Relay ***\n')    
    r=Relay()
    r.test()
    print('\n*** Test Fan ***\n')        
    f=Fan()
    f.test()
    print('\n*** Test Environment ***\n')
    eTest()
    print('\n*** Test Thermostat ***\n')
    tTest()
    print('\n*** Test Environmental Observation ***\n')
    enTest()
    print "Done"

if __name__=="__main__":
    test()

  
    
