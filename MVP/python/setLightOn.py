#!/usr/bin/python

#Light Control
#Controls the turning on and turning off of lights
#Lights are wired into Relay #4 (Pin 29)

import RPi.GPIO as GPIO
from logData import logData


def setLightOn():
    "Check the time and determine if the lights need to be changed"
    lightPin = 29
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    print ("Turn lights On")
    GPIO.setup(lightPin, GPIO.OUT)
    GPIO.output(lightPin, GPIO.HIGH)
    logData("LightChange", "Success", "light", "On", '')

setLightOn()    
