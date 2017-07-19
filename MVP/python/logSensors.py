#Check sensors and log to file
from oneWireTemp import getTempC
from logData import logData

boxTemp = 0
topTemp = 1
reservoirTemp = 2
ambientTemp = 3

try:
    temp = getTempC(ambientTemp)
    logData("ambient_temp", "Success", "temperature", "{:10.1f}".format(temp), '')
except (IOError, e):
        logData("ambient_temp", "Failure", "temperature", '', str(e))

try:
    temp = getTempC(boxTemp)
    logData("box_temp", "Success", "temperature", "{:10.1f}".format(temp), '')
except (IOError, e):
        logData("box_temp", "Failure", "temperature", '', str(e))

try:
    temp = getTempC(topTemp)
    logData("box_top_temp", "Success", "temperature", "{:10.1f}".format(temp), '')
except (IOError, e):
        logData("box_top_temp", "Failure", "temperature", '', str(e))

try:
    temp = getTempC(reservoirTemp)
    logData("reservoir_temp", "Success", "temperature", "{:10.1f}".format(temp), '')
except (IOError, e):
        logData("reservoir_temp", "Failure", "temperature", '', str(e))        
