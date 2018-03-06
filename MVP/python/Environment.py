# Build dictionary structure variables for the environment
# A python file is generated that is 'read' by the logging program.
# Author: Howard Webb
# Data: 2/21/2018

import uuid
from datetime import tzinfo, datetime
from geoLocate import getLocation
import json
from config import config

# Default to one trial with six plots
trials={1:{'plots':[1, 2, 3, 4, 5, 6]}}
python_dir=config['python_dir']
env_file=python_dir + 'env.py'

def setup():
    '''One time setup of the environment - get UUID of Field"'''
    env={}
    env['field']=getField()
    env['location']=str(getLocation())
    saveDict('env', env_file, env)

def startTrial():
    '''Configure env for a particular trial run'''
    from env import env
    env['reservoir']=getReservoir()
    env['trials']=getTrials()
    updatePlotUse(env['field']['plots'], env['trials'])
    env['thermostat']=setTargetTemperature()
    saveDict('env', env_file, env)    
    return env

def endTrial(trial, date):
    '''set the end date of the trial'''
    from env import env
    if date == None:
        date = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.utcnow())
    env['trials'][trial]['end_date']=date
    saveDict('env', env_file, env)    
    return env

def getField():
    '''Create Field UUID and Plots'''
    field={}
    field['uuid']=str(uuid.uuid4())
    field['name']='Field Name'
    field['plots']=getPlots(2,3)
    return field

def getPlots(rows, columns):
    '''Create individual plot, assumes row column configuration'''
    plots={}
    id=1
    for r in range(1, rows+1):
        for c in range(1, columns+1):
            plot={'plot_id':id, 'row':r, 'column':c, 'name':'Plant_'+ str(id)}
            plots[id]=plot
            id+=1
    return plots

def getTrials():
    '''Create one or more trials for a growth run'''
    for trial in trials:
#        print trials[trial]
        getTrial(trials[trial])
    return trials

def getTrial(trial, start_date=None):
    '''Configure an individual trial activity'''
    trial['uuid']=str(uuid.uuid4())
    if start_date==None:
        start_date = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.utcnow())
    trial['start_date']=start_date        
    status={}
    status['status']='in process'
    status['comment']=''
    trial['status']=status

def setTargetTemperature(targetTemp=25, setPoint=25):
    '''
       targetTemp is the desired temperature (may be the average for the day)
       setPoint is the temperature the thermostat reacts to
    '''        
    return {'targetTemp':targetTemp, 'setPoint':setPoint}

def getReservoir():
# Note: water levels may need to be adjusted for seedlings (without roots) and plants (with roots)
# This is a starting point, and can be adjusted through recipes
    reservoir_full=175  # Highest desired water level
    reservoir_empty=220 # Lowest level water is allowed to drop
    reservoir_timeout=1200 # Max time to wait for filling
    reservoir_change=3  # Number of mm needed to indicate water level change
    # Build reservoir levels
    return {'full':reservoir_full, 'empty':reservoir_empty, 'timeout': reservoir_timeout, 'change': reservoir_change}
    loadDict('reservoir', reservoir)

def updatePlotUse(plots, trials):
    '''Put the trial uuid on the plot'''
    for trial in trials:
#        print trials[trial]
        for plot in trials[trial]['plots']:
#            print plots[plot]
            plots[plot]['use']={'trial_id':trials[trial]['uuid']}
            
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
    
def test1():
    print "Test"
    print "Setup Env"
    setup()
    from env import env
    prettyPrint(env)
    print "Start Trial Config"
    startTrial()
    prettyPrint(env)
    print "Done"

def test():
    from env import env
    prettyPrint(env)

def test3():
    '''Test working of Json parts'''
    print "Test 3"
    from env import env
    print env
    prs=json.loads(env)
    print json.dumps(prs, indent=4, sort_keys=False)
    trials=env['trials']
    
    for trial in trials:
        for plot in trial['plots']:
            print field['plots'][plot]
    field=env['field']    
    for plot in field['plots']:
        for trial in trials:
            if plot['plot_id'] in trial['plots']:
                print "Trial ", trial['uuid']


def test2():
    '''Test individual functions'''
    print "Test Environment"
    print "Trial"
    trial=getTrials()
    print trial
    prettyPrint(trial)
    print "Plots"
    plots=getPlots(2,3)
    print plots
    prettyPrint(str(plots))
    print "Reservoir"
    prettyPrint(getReservoir())
    print "Location"
    loc= getLocation()
    print loc
    prettyPrint( loc)

def adjust():
    from env import env
    '''Code to adjust the structure without changing other parts'''
    print "Adjust"
    for plot in env['field']['plots']:
        env['field']['plots'][plot]['name']='Plant_'+str(plot)
    print env['field']['plots']
#    saveDict('env', env_file, env)    

if __name__=="__main__":
    test1()
    
