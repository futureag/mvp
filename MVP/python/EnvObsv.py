#Make and log Environmental Observations
from si7021 import *
from JsonUtil import makeEnvJson
from CouchDB import logEnvObsvJSON
import json
# Author: Howard Webb
# Date: 2018/02/17

si=si7021()
activity_type="Environmental_Observation"

def getAirTopTempObsv(test=False):
    '''Create json structure for temp'''
    temp = si.getTempC()
    
    status_qualifier='Success'
    cmt=''

    if temp==None:
        status_qualifier='Failure'
        cmt='Failure reading sensor'
    if test:
        status_qualifier='Test'
    return makeEnvJson(activity_type, 'Air', 'Top', 'Temperature', '{:3.1f}'.format(temp), 'SI7021', status_qualifier, comment=cmt)
    
def getAirTopHumidityObsv(test=False):
    '''Create json structure for humidity'''
    humid = si.getHumidity()
    status_qualifier='Success'
    cmt=''

    if humid==None:
        status_qualifier='Failure'
        cmt='Failure reading sensor'
    if test:
        status_qualifier='Test'
    return makeEnvJson(activity_type, 'Air', 'Top', 'Humidity', '{:3.1f}'.format(humid), 'SI7021', status_qualifier, comment=cmt)

def makeEnvObsv(test=False):
    '''Log all sensors'''
    jsn=getAirTopTempObsv(test)
    saveEnvObsv(jsn)
    if test:
        prettyPrint(jsn)
    
    jsn=getAirTopHumidityObsv(test)
    saveEnvObsv(jsn)
    if test:
        prettyPrint(jsn)

def saveEnvObsv(content):
    logEnvObsvJSON(content)

def prettyPrint(txt):
    '''Dump json in nice format'''
    #print type(txt)
    print json.dumps(txt, indent=4, sort_keys=True)

def test():
    print "Test"
    print "Make Env Obsv - JSON"
    makeEnvObsv(True)
    print "Done"

        
if __name__=="__main__":
    '''Setup for calling from script'''
    makeEnvObsv()
