#Light Control
#Controls the turning on and turning off of lights
#Lights are wired into Relay #4 (Pin 29)

import RPi.GPIO as GPIO
from logData import logData


def setLightOff():
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
    logData("Light_Switch", "Success", "light", "Off", '')
    
setLightOff()
            
    

