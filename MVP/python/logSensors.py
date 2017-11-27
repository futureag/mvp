#Check sensors and log to file
from si7021 import *
from logData import logData

si=si7021()

try:
    temp = si.getTempC()
    logData("si7921_top", "Success", "temperature", "{:10.1f}".format(temp), '')
except Exception as e:
        logData("si7921_top", "Failure", "temperature", '', str(e))

try:
    humid = si.getHumidity()
    logData("si7021_top", "Success", "humidity", "{:10.1f}".format(humid), '')
except Exception as e:
        logData("si7921_top", "Failure", "humidity", '', str(e))
