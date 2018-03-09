# Author: Howard Webb
# Date: 7/25/2017
# Code for managing the relay switch

import RPi.GPIO as GPIO
import time

ON=1
OFF=0

Relay1 = 29 # Fan
Relay2 = 31
Relay3 = 33 # LED
Relay4 = 35 # Solenoid

class Relay(object):

    def __init__(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(Relay1, GPIO.OUT)
        GPIO.setup(Relay2, GPIO.OUT)
        GPIO.setup(Relay3, GPIO.OUT)
        GPIO.setup(Relay4, GPIO.OUT)        
    
    def setState(self, pin, state):
        '''Change state if different'''
#        print "Current ", state, GPIO.input(pin)
        if state==ON and not GPIO.input(pin):
            self.setOn(pin)
        elif state==OFF and GPIO.input(pin):
            self.setOff(pin)
        else:        
 #           print("No Change")
            pass

    def getState(self, pin):
        '''Get the current state of the pin'''
        state=GPIO.input(pin)
        return state

    def setOff(self, pin):
        GPIO.output(pin, GPIO.LOW)
#            print("Pin ", pin, " Off")

    def setOn(self, pin):
        GPIO.output(pin, GPIO.HIGH)
#            print("Pin ", pin, " On")

    def test(self):
        print "Test 2"
        print "Read #3 Unknown: ", self.getState(Relay3)
        print "Turn On"
        self.setState(Relay3, ON)
        print "Turn On"
        self.setState(Relay3, ON)

#        print "Read #3 On: ", self.getState(Relay3)    
        print "Turn Off"
        self.setState(Relay3, OFF)
        print "Turn Off"
        self.setState(Relay3, OFF)
        time.sleep(5)
#        print "Read #3 Off: ", self.getState(Relay3)    
        print "Turn On"
        self.setState(Relay3, ON)
#        print "Read #3 On: ", self.getState(Relay3)
        print "Turn Off"
        self.setOff(Relay3)

        print "Turn On"
        self.setOn(Relay3)




    def test1(self):
        self.setState(Relay1, ON)
        self.setState(Relay1, OFF)
        self.setState(Relay2, ON)
        self.setState(Relay2, OFF)
        self.setState(Relay3, ON)
        self.setState(Relay3, OFF)
        self.setState(Relay4, ON)
        self.setState(Relay4, OFF)

if __name__=="__main__":
    pass
    
            
    

