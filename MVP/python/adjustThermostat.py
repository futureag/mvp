from thermostat import adjustThermostat
from si7021 import getTempC
from logData import logData

boxTemp = 1

try:
    temp = getTempC()
    adjustThermostat(temp)  
except IOError as e:
    print("Failure to get temperature, no sensor found; check pins and sensor")
    logData('si7921-top', 'Failure', 'temperature', "", str(e))

  
    
