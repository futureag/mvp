#Light Control
#Controls the turning on and turning off of lights
#Lights are wired into Relay #4 (Pin 29)
# Author: Howard Webb
# Date: 3/5/2018

import RPi.GPIO as GPIO
from JsonUtil import makeEnvJson
import CouchDB



def setLightOff(test=False):
    "Check the time and determine if the lights need to be changed"
    lightPin = 29
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    print ("Turn lights Off")
    GPIO.setup(lightPin, GPIO.OUT)
# For the relaly board, use the first line
# For the Sparkfun PowerSwitch tail (https://www.sparkfun.com/products/10747)
# Uncomment the second line, and comment out the first
    GPIO.output(lightPin, GPIO.LOW)
#    GPIO.output(lightPin, GPIO.HIGH)
    logState("Off", test)

def logState(value, test=False):
    status_qualifier='Success'
    if test:
        status_qualifier='Test'
    jsn=makeEnvJson('State_Change', 'Lights', 'Top', 'State', value, 'Lights', status_qualifier)
    CouchDB.logEnvObsvJSON(jsn)

def test():
    print "Test Lights Off"
    setLightOff(True)    

if __name__=="__main__":
    setLightOff()
            
    

