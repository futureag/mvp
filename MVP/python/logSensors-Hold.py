#Check sensors and log to file
from si7021 import getTempC, getHumidity
from logData import logData
#from ds18B29 import getTempC as getTempC_ds

try:
    temp = getTempC()
    logData("si7921_top", "Success", "temperature", "{:10.1f}".format(temp), '')
except (IOError, e):
        logData("si7921_top", "Failure", "temperature", '', str(e))

try:
    humid = getHumidity()
    logData("si7021_top", "Success", "humidity", "{:10.1f}".format(humid), '')
except (IOError, e):
        logData("si7921_top", "Failure", "humidity", '', str(e))

#try:
#    tempDS = getTempC_ds()
#    logData("DS18B29_temp", "Success", "temperature", "{:.1f}".format(tempDS), '')
#except (IndexError):    
#    logData("DS18B29_temp", "Failure", "temperature", '', "Data file not found or not read")
 
