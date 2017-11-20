#A script to test the functions of the OpenAg-MVP routines
#Run this to validate code and that things are working correctly

from adjustThermostat import *
from setLightOn import *
from setLightOff import *
from getTempChart import *
from getHumidityChart import *
from getMultiTempChart import *

try:
    print ("Check Thermostat Low")
    print (adjustThermostat(15))
except (RuntimeError, e):
    print ("Failure adjusting thermostat: Low", e)

try:
    print ("Check Thermostat High")
    print (adjustThermostat(75))
except (RuntimeError, e):
    print ("Failure adjusting thermostat: High", e)

try:
    print ("Turn Light On")
    print (setLightOn())
except (RuntimeError, e):
    print ("Failure to turn light ON", e)    
   
try:
    print ("Turn Light OFF")
    print (setLightOff())
except (RuntimeError, e):
    print ("Failure to turn light OFF", e)

try:
    print ("Turn Light On")
    print (setLightOn())
except (RuntimeError, e):
    print ("Failure to turn light ON", e) 

try:
    print ("Build Humidity Chart")
    print (getHumidityChart())
except (RuntimeError, e)    
    print ("Failure to build humidity chart", e)    

try:
    print ("Build Temp Chart")
except (RuntimeError, e):
    print ("Failure to build temp chart", e)  

try:
    print ("Build Multi Temp Chart")
except (RuntimeError, e):
    print ("Failure to build multi temp chart", e)      
   


