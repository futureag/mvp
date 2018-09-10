""" Log standard MVP sensors
"""

from SI7021 import *
from CouchUtil import saveList


def log_sensors(test = False):

    si=SI7021()

    try:
        temp = si.get_tempC()

        status = 'Success'
        if test:
            status = 'Test'
        saveList(['Environment_Observation', '', 'Top', 'Air', 'Temperature', "{:10.1f}".format(temp), 'Farenheight', 'SI7021', status, ''])                
    except Exception as e:
        status = 'Failure'
        if test:
            status = 'Test'
        saveList(['Environment_Observation', '', 'Top', 'Air', 'Temperature', '', 'Farenheight', 'SI7021', status, str(e)])                            

    try:
        humid = si.get_humidity()

        status = 'Success'
        if test:
            status = 'Test'
        saveList(['Environment_Observation', '', 'Top', 'Air', 'Humidity', "{:10.1f}".format(humid), 'Percent', 'SI7021', status, ''])                
        
    except Exception as e:
        status = 'Failure'
        if test:
            status = 'Test'
        saveList(['Environment_Observation', '', 'Top', 'Air', 'Humidity', '', 'Percent', 'SI7021', status, str(e)])
            

def test():
    log_sensors(True)

if __name__=="__main__":
    log_sensors()    
