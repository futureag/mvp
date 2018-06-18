# Recorder - create JSON structure and route to one or more destinations
# Author: Howard Webb
# Date 6/18/2018
"""
    To modify where data is stored (ie MQTT, CouchDB, SQL)
      Import a new recorder
      Add the recorder's function to the array in the record function
"""      

from CouchDB import logEnvObsvJSON
from JsonUtil import make_env_json


def record_env(activity_type, subject, subject_location, attribute, value, participant, status_qualifier, timestamp=None, status='Complete', status_qualifier_reason='', comment='', validate=False):
    """
    Create JSON record and route to storage
    """

    jsn=make_env_json(activity_type, subject, subject_location, attribute, value, participant, status_qualifier)
    record_env_router(jsn)

def  mqtt_recorder(msg):
    """
    Dummy stand in for mqtt messaging
    """
    print msg

def display_recorder(msg):
    print msg

def record_env_router(msg):
    recorders=[mqtt_recorder, display_recorder, logEnvObsvJSON]     
    for recorder in recorders:
        recorder(msg)    

def test():
    record_env('State_Change', 'Lights', 'Top', 'State', 0, 'Lights','Test')

if __name__=="__main__":
    test()
