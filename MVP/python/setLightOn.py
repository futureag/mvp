#Light Control
#Controls the turning on and turning off of lights
#Lights are wired into Relay #4 (Pin 29)

from JsonUtil import makeEnvJson
import CouchDB
import Relay

def setLightOn(test=False):
    "Check the time and determine if the lights need to be changed"
    r=Relay.Relay()
    r.setOn(Relay.Relay4)
    logState("On", test)

def logState(value, test=False):
    status_qualifier='Success'
    if test:
        status_qualifier='Test'
    jsn=makeEnvJson('State_Change', 'Lights', 'Top', 'State', value, 'Lights', status_qualifier)
    CouchDB.logEnvObsvJSON(jsn)

def test():
    print "Test Lights On"
    setLightOn(True)

if __name__=="__main__":
    setLightOn()    
    
            
    

