# Author: Howard Webb
# Data: 7/25/2017
# Fan actuator controlled by thermometer

from thermostat import adjustThermostat
from si7021 import *
from logData import logData

try:
    si=si7021()
    temp = si.getTempC()
    adjustThermostat(temp)  
except IOError as e:
    print("Failure to get temperature, no sensor found; check pins and sensor")
    logData('si7021-top', 'Failure', 'temperature', "", str(e))

  
    
