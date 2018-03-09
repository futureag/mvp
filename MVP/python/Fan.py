# Acuator for the exhaust fan
# Author: Howard Webb
# Date: 2/15/2017

from env import env
from JsonUtil import makeEnvJson
from Relay import *
import time
import CouchDB

class Fan(object):

    relay=None
    target_temp=0

    def __init__(self):
        self.relay=Relay()
        self.fanRelay=fanPin

    def setFanOn(self):
        self.relay.setState(self.fanRelay, ON)
        
    def setFanOff(self):    
        self.relay.setState(self.fanRelay, OFF)

    def adjust(self, temp, test=False):
        '''Change state if different from current'''
        if test:
            print temp, self.relay.getState(self.fanRelay)
        if temp > env['thermostat']['setPoint'] and not self.relay.getState(self.fanRelay):
            self.setFanOn()
            self.logState("On", test)
            if test:
                print "Turn On"

        elif temp <= env['thermostat']['setPoint'] and self.relay.getState(self.fanRelay):
            self.setFanOff()
            self.logState("Off", test)
            if test:
                print "Turn Off"
        else:
            if test:
                print "No Change"

    def logState(self, value, test=False):
        status_qualifier='Success'
        if test:
            status_qualifier='Test'
        jsn=makeEnvJson('State_Change', 'Fan', 'Side', 'State', value, 'Fan', status_qualifier)
        CouchDB.logEnvObsvJSON(jsn)
        

    def test(self):
        print "Test"
        print "State: ", self.relay.getState(self.fanRelay)
        print "Turn Fan On"
        self.setFanOn()        
        print "State: ", self.relay.getState(self.fanRelay)
        time.sleep(2)

        print "Turn Fan Off"
        self.setFanOff()    
        print "State: ", self.relay.getState(self.fanRelay)
        time.sleep(2)

        print "Adj 45"
        self.adjust(45, True)        
        print "State: ", self.relay.getState(self.fanRelay)                

        print "Adj 45"
        self.adjust(45, True)        
        print "State: ", self.relay.getState(self.fanRelay)                

        print "Adj 10"
        self.adjust(10, True)        
        print "State: ", self.relay.getState(self.fanRelay)                

        print "Adj 45"
        self.adjust(45, True)        
        print "State: ", self.relay.getState(self.fanRelay)
        print "Done"


if __name__=="__main__":
    f=Fan()
    f.test()            

