#Light Control
#Controls the turning on and turning off of lights
#Lights are wired into Relay #4 (Pin 29)
# Author: Howard Webb
# Date: 3/5/2018

from JsonUtil import makeEnvJson
import CouchDB
import Relay

def setLightOff(test=False):
    "Check the time and determine if the lights need to be changed"
    r=Relay.Relay()
    r.setOff(Relay.Relay4)
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
            
    

