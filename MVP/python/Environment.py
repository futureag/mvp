# Build dictionary structure variables for the environment
# A python file is generated that is 'read' by the logging program.
# Author: Howard Webb
# Data: 2/21/2018

import uuid
import json
def setup():
    '''One time setup of the environment - get UUID of Field"'''
    env={}
    env['field']=getField()
    env['thermostat'] = setTargetTemperature()
    env['lights'] = setLights()
    saveDict('env', '/home/pi/MVP/python/env.py', env)

def getField():
    '''Create Field UUID and Plots'''
    field={}
    field['field_id']=str(uuid.uuid4())
    return field

def setTargetTemperature(targetTemp=25):
    '''
       targetTemp is the desired temperature (may be the average for the day)
       setPoint is the temperature the thermostat reacts to
    '''        
    return {'targetTemp':targetTemp}

def setLights(on='06:30:00', off='22:00:00'):
	lights = {'On':on, 'Off': off}
	return lights

def prettyPrint(txt):
    '''Dump json in nice format'''
    #print type(txt)
    print json.dumps(txt, indent=4, sort_keys=True)

def saveDict(name, file_name, dict):
    #print(values)
    f = open(file_name, 'w+')
    tmp=name+'='+str(dict)
    f.write(tmp)
    f.close()    
    
def test():
    setup()
    from env import env
    prettyPrint(env)

if __name__=="__main__":
    test()
    
